#!/usr/bin/env python3
"""Start torno_v3 in the existing desktop session and capture startup evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time

import paramiko


HOST = "cnc.taila1b901.ts.net"
INI = "/home/cnc/linuxcnc/configs/torno_v3/torno_v3.ini"
PROCESS_QUERY = r"""
ps -eo pid=,ppid=,comm=,args= | grep -E \
  '[l]inuxcnc|[l]inuxcncsvr|[q]tvcp|[m]illtask|[r]tapi_app|[h]alui|[Q]tWebEngineProcess'
"""


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def run(client: paramiko.SSHClient, command: str, timeout: int = 30) -> dict[str, object]:
    _, stdout, stderr = client.exec_command(command, timeout=timeout)
    output = stdout.read().decode("utf-8", errors="replace")
    error = stderr.read().decode("utf-8", errors="replace")
    return {
        "exit": stdout.channel.recv_exit_status(),
        "stdout": output,
        "stderr": error,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--confirm-start", action="store_true")
    args = parser.parse_args()
    if not args.confirm_start:
        parser.error("--confirm-start is required")

    repository = Path(__file__).resolve().parents[2]
    env = read_env(repository / ".env")
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(
        HOST,
        username=env["CNC_SSH_USER"],
        password=env["CNC_SSH_PASSWORD"],
        timeout=10,
        banner_timeout=10,
        auth_timeout=10,
        allow_agent=False,
        look_for_keys=False,
    )

    before = run(client, PROCESS_QUERY)
    if str(before["stdout"]).strip():
        client.close()
        raise RuntimeError("LinuxCNC is already active; duplicate start refused")

    desktop = run(
        client,
        r"""
uid="$(id -u)"
test -S /tmp/.X11-unix/X0
test -r /home/cnc/.Xauthority
test -S "/run/user/$uid/bus"
printf 'DISPLAY=:0\nXAUTHORITY=/home/cnc/.Xauthority\nDBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%s/bus\n' "$uid"
""",
    )
    if desktop["exit"] != 0:
        client.close()
        raise RuntimeError("graphical desktop preflight failed: " + str(desktop["stderr"]))

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    remote_log = f"/tmp/qtdragon-es-start-{timestamp}.log"
    launch = run(
        client,
        f"""
umask 077
setsid -f env \
  DISPLAY=:0 \
  XAUTHORITY=/home/cnc/.Xauthority \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus \
  LANG=es_CO.UTF-8 LANGUAGE=es_CO:es \
  /usr/bin/linuxcnc {INI} >{remote_log} 2>&1 </dev/null
""",
    )
    if launch["exit"] != 0:
        client.close()
        raise RuntimeError("launch command failed: " + str(launch["stderr"]))

    processes = ""
    ready = False
    for _ in range(45):
        check = run(client, PROCESS_QUERY)
        processes = str(check["stdout"]).strip()
        ready = all(name in processes for name in ("linuxcncsvr", "milltask", "qtvcp"))
        if ready:
            break
        time.sleep(1)

    sftp = client.open_sftp()
    try:
        with sftp.open(remote_log, "rb") as stream:
            log_text = stream.read().decode("utf-8", errors="replace")
    finally:
        sftp.close()
        client.close()

    translation_path = (
        "/home/cnc/linuxcnc/configs/torno_v3/qtdragon/languages/qtdragon_es.qm"
    )
    translation_selected = (
        "Using LOCAL translation file" in log_text and translation_path in log_text
    )
    traceback = "Traceback (most recent call last)" in log_text
    segfault = "Violación de segmento" in log_text or "Segmentation fault" in log_text

    evidence = repository / "backups" / f"{timestamp}-qtdragon-es-start"
    evidence.mkdir(parents=True, exist_ok=False)
    (evidence / "startup.log").write_text(log_text, encoding="utf-8")
    report = {
        "schema_version": 1,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "ini": INI,
        "remote_log": remote_log,
        "desktop_preflight": desktop,
        "launch": launch,
        "ready": ready,
        "processes": processes,
        "translation_selected": translation_selected,
        "translation_path": translation_path,
        "traceback": traceback,
        "segmentation_fault": segfault,
    }
    (evidence / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"evidence": str(evidence), **report}, ensure_ascii=False, indent=2))
    return 0 if ready and translation_selected and not traceback and not segfault else 1


if __name__ == "__main__":
    raise SystemExit(main())
