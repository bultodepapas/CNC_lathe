"""Capture a read-only operational inventory from the CNC controller.

The command set is intentionally static.  This script does not accept arbitrary
remote commands, use sudo, update APT metadata, write remote files, or mutate
HAL state.  Evidence is written only to the local repository's ignored
``backups`` directory unless ``--output`` is provided.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from datetime import datetime
from pathlib import Path

import paramiko


DEFAULT_HOST = "cnc.taila1b901.ts.net"


READ_ONLY_COMMANDS: dict[str, str] = {
    "identity": """
        hostname
        date --iso-8601=seconds
        id
        uname -a
        cat /etc/os-release
        cat /etc/debian_version
    """,
    "versions": """
        linuxcnc_var LINUXCNCVERSION 2>&1 || true
        dpkg-query -W -f='${Package}|${Version}|${Architecture}|${Status}\n' \
          linuxcnc-uspace linuxcnc-uspace-dev \
          linuxcnc-doc-de linuxcnc-doc-en linuxcnc-doc-es linuxcnc-doc-fr \
          linux-image-rt-amd64 mesaflash 2>/dev/null || true
        python3 --version 2>&1 || true
    """,
    "apt_sources": """
        for f in /etc/apt/sources.list \
                 /etc/apt/sources.list.d/*.list \
                 /etc/apt/sources.list.d/*.sources; do
          if [ -r "$f" ]; then
            printf '\nFILE:%s\n' "$f"
            sed -n '1,240p' "$f"
          fi
        done
    """,
    "apt_policy": """
        apt-cache policy \
          linuxcnc-uspace linuxcnc-uspace-dev \
          linuxcnc-doc-de linuxcnc-doc-en linuxcnc-doc-es linuxcnc-doc-fr \
          linux-image-rt-amd64 mesaflash
        printf '\nUPGRADABLE_FROM_CURRENT_CACHE\n'
        apt list --upgradable 2>/dev/null || true
    """,
    "package_audit": """
        dpkg --audit 2>&1 || true
        printf '\nHELD_PACKAGES\n'
        apt-mark showhold 2>/dev/null || true
        printf '\nMANUAL_LINUXCNC_PACKAGES\n'
        apt-mark showmanual 2>/dev/null | grep -E 'linuxcnc|mesa|python3-pyqt|qtvcp' || true
        printf '\nAPT_PRIORITIES\n'
        apt-cache policy
        printf '\nAPT_PREFERENCES\n'
        for f in /etc/apt/preferences /etc/apt/preferences.d/*; do
          if [ -r "$f" ]; then
            printf 'FILE:%s\n' "$f"
            sed -n '1,240p' "$f"
          fi
        done
    """,
    "rollback_package_state": """
        find /var/cache/apt/archives -maxdepth 1 -type f \
          -name 'linuxcnc*.deb' -printf '%s|%TY-%Tm-%TdT%TH:%TM:%TS|%p\n' \
          2>/dev/null | sort
        printf '\nSIMULATE_REINSTALL_2_9_7\n'
        apt-get -s --reinstall install \
          linuxcnc-uspace=1:2.9.7 linuxcnc-uspace-dev=1:2.9.7 \
          linuxcnc-doc-de=1:2.9.7 linuxcnc-doc-en=1:2.9.7 \
          linuxcnc-doc-es=1:2.9.7 linuxcnc-doc-fr=1:2.9.7 2>&1 || true
    """,
    "rtapi_permissions": """
        stat -c '%a|%U:%G|%s|%y|%n' \
          /usr/bin/rtapi_app /usr/bin/linuxcnc_module_helper 2>&1 || true
        getcap /usr/bin/rtapi_app /usr/bin/linuxcnc_module_helper 2>&1 || true
    """,
    "package_conffiles": """
        for f in \
          /etc/X11/app-defaults/TkLinuxCNC \
          /etc/linuxcnc/rtapi.conf \
          /etc/xdg/menus/applications-merged/CNC.menu; do
          if [ -e "$f" ]; then
            stat -c '%a|%U:%G|%s|%y|%n' "$f"
            sha256sum "$f"
          else
            printf 'MISSING|%s\n' "$f"
          fi
        done
        printf '\nDPKG_VERIFY_LINUXCNC_USPACE\n'
        dpkg --verify linuxcnc-uspace 2>&1 || true
    """,
    "runtime_processes": """
        ps -eo pid=,ppid=,lstart=,stat=,comm=,args= \
          | grep -E '[l]inuxcnc|[l]inuxcncsvr|[q]tvcp|[m]illtask|[r]tapi|[h]al'
    """,
    "network": """
        ip -brief address
        printf '\nROUTES\n'
        ip route show
        printf '\nMESA_NIC_COUNTERS\n'
        ip -s link show eno1
        printf '\nMESA_NEIGHBOR\n'
        ip neigh show 192.168.1.121 || true
    """,
    "system_health": """
        df -h
        printf '\nFAILED_UNITS\n'
        systemctl --failed --no-pager 2>&1 || true
        printf '\nBOOT_WARNINGS\n'
        journalctl -b --priority=warning..alert --no-pager 2>&1 || true
        printf '\nKERNEL_WARNINGS\n'
        dmesg --level=err,warn 2>&1 || true
    """,
    "linuxcnc_logs": """
        journalctl -b --no-pager 2>&1 \
          | grep -Ei 'linuxcnc|rtapi|hostmot2|hm2|watchdog|realtime|latency|packet|error' \
          | tail -n 1200 || true
    """,
    "config_identity": """
        readlink -f /home/cnc/linuxcnc/configs/torno_v3/torno_v3.ini
        stat -c '%a|%U:%G|%s|%y|%n' \
          /home/cnc/linuxcnc/configs/torno_v3/torno_v3.ini \
          /home/cnc/linuxcnc/configs/torno_v3/torno_v3.hal \
          /home/cnc/linuxcnc/configs/torno_v3/custom.hal \
          /home/cnc/linuxcnc/configs/torno_v3/tool.tbl \
          /home/cnc/linuxcnc/configs/torno_v3/linuxcnc.var \
          /home/cnc/linuxcnc/configs/torno_v3/qtdragon.pref 2>&1 || true
        printf '\nLAUNCHERS\n'
        for f in /home/cnc/Escritorio/*.desktop; do
          if [ -r "$f" ]; then
            printf 'FILE:%s\n' "$f"
            sed -n '1,120p' "$f"
          fi
        done
    """,
    "config_hashes": """
        find /home/cnc/linuxcnc/configs/torno_v3 -type f -print0 2>/dev/null \
          | sort -z \
          | xargs -0 sha256sum
    """,
    "qtdragon_overrides": """
        find /home/cnc/linuxcnc/configs/torno_v3/qtvcp \
          -maxdepth 6 -type f \
          -printf '%m|%U:%G|%s|%TY-%Tm-%TdT%TH:%TM:%TS|%p\n' 2>/dev/null \
          | sort
        printf '\nSYSTEM_QTDRAGON\n'
        find /usr/share/qtvcp/screens/qtdragon \
          -maxdepth 2 -type f \
          -printf '%m|%U:%G|%s|%TY-%Tm-%TdT%TH:%TM:%TS|%p\n' 2>/dev/null \
          | sort
    """,
    "hal_threads": """
        halcmd show thread 2>&1 || true
        printf '\nCOMPONENTS\n'
        halcmd show comp 2>&1 || true
    """,
    "hal_signals": """
        halcmd show sig 2>&1 || true
    """,
    "hal_critical_pins": """
        for pin in \
          motion.motion-enabled motion.in-position \
          iocontrol.0.user-enable-out iocontrol.0.emc-enable-in \
          joint.0.amp-enable-out halui.joint.0.is-homed \
          joint.1.amp-enable-out halui.joint.1.is-homed joint.1.amp-fault-in \
          joint.2.amp-enable-out halui.joint.2.is-homed joint.2.amp-fault-in \
          carousel.0.homed carousel.0.ready carousel.0.current-position \
          carousel.0.pocket-number carousel.0.enable \
          spindle.0.on spindle.0.at-speed spindle.0.speed-in \
          hm2_7i76e.0.7i76.0.0.input-08 \
          hm2_7i76e.0.7i76.0.0.input-08-not; do
          printf '%s=' "$pin"
          halcmd getp "$pin" 2>&1 || true
        done
    """,
    "hm2_health": """
        halcmd show pin 2>&1 \
          | grep -Ei 'hm2_.*(packet|error|fault|watchdog|timeout)' || true
        printf '\nHM2_PARAMETERS\n'
        halcmd show param 2>&1 \
          | grep -Ei 'hm2_.*(packet|error|fault|watchdog|timeout)' || true
    """,
}


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument(
        "--output",
        type=Path,
        help="Local JSON path. Defaults below backups/<timestamp>-readonly-audit/.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repository = Path(__file__).resolve().parent.parent
    env = read_env(repository / ".env")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output = args.output or (
        repository / "backups" / f"{timestamp}-readonly-audit" / "remote-audit.json"
    )
    output = output.resolve()

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(
        args.host,
        username=env["CNC_SSH_USER"],
        password=env["CNC_SSH_PASSWORD"],
        timeout=10,
        banner_timeout=10,
        auth_timeout=10,
        allow_agent=False,
        look_for_keys=False,
    )

    result: dict[str, object] = {
        "captured_at_local": datetime.now().astimezone().isoformat(),
        "host": args.host,
        "policy": "static read-only command allowlist; no sudo; no remote writes",
        "commands": {},
    }

    transport = client.get_transport()
    if transport is not None:
        host_key = transport.get_remote_server_key()
        result["ssh_host_key"] = {
            "type": host_key.get_name(),
            "sha256": base64.b64encode(hashlib.sha256(host_key.asbytes()).digest()).decode(
                "ascii"
            ),
        }

    command_results = result["commands"]
    assert isinstance(command_results, dict)
    for name, command in READ_ONLY_COMMANDS.items():
        normalized = "\n".join(line.strip() for line in command.strip().splitlines())
        _, stdout, stderr = client.exec_command(normalized, timeout=60)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        command_results[name] = {
            "exit": stdout.channel.recv_exit_status(),
            "stdout": out,
            "stderr": err,
        }

    client.close()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{digest}  {output.name}\n", encoding="ascii"
    )
    print(json.dumps({"output": str(output), "sha256": digest, "sections": len(command_results)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
