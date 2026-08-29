#!/usr/bin/env python3
"""Capture read-only runtime evidence and one desktop screenshot of QtDragon."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path, PurePosixPath
import time

import paramiko


HOST = "cnc.taila1b901.ts.net"
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


def run(client: paramiko.SSHClient, command: str) -> dict[str, object]:
    _, stdout, stderr = client.exec_command(command, timeout=30)
    output = stdout.read().decode("utf-8", errors="replace")
    error = stderr.read().decode("utf-8", errors="replace")
    return {
        "exit": stdout.channel.recv_exit_status(),
        "stdout": output,
        "stderr": error,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wait-seconds", type=int, default=8)
    args = parser.parse_args()
    time.sleep(max(0, min(args.wait_seconds, 30)))

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
    processes = run(client, PROCESS_QUERY)
    if "qtvcp" not in str(processes["stdout"]):
        client.close()
        raise RuntimeError("QtDragon is not running; screenshot refused")

    installed = run(
        client,
        r"""
stat -c '%a|%U:%G|%s|%n' \
  /home/cnc/linuxcnc/configs/torno_v3/qtdragon/languages/qtdragon_es.ts \
  /home/cnc/linuxcnc/configs/torno_v3/qtdragon/languages/qtdragon_es.qm
sha256sum \
  /home/cnc/linuxcnc/configs/torno_v3/qtdragon/languages/qtdragon_es.ts \
  /home/cnc/linuxcnc/configs/torno_v3/qtdragon/languages/qtdragon_es.qm
""",
    )
    tool = run(
        client,
        "command -v scrot || command -v gnome-screenshot || command -v xfce4-screenshooter || command -v import",
    )
    capture_tool = str(tool["stdout"]).strip().splitlines()
    if not capture_tool:
        client.close()
        raise RuntimeError("no supported screenshot utility is installed")
    executable = capture_tool[0]

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    remote_image = PurePosixPath(f"/tmp/qtdragon-es-{timestamp}.png")
    prefix = "DISPLAY=:0 XAUTHORITY=/home/cnc/.Xauthority"
    if executable.endswith("scrot"):
        command = f"{prefix} {executable} {remote_image}"
    elif executable.endswith("gnome-screenshot"):
        command = f"{prefix} {executable} -f {remote_image}"
    elif executable.endswith("xfce4-screenshooter"):
        command = f"{prefix} {executable} -f -s {remote_image}"
    else:
        command = f"{prefix} {executable} -window root {remote_image}"
    capture = run(client, command)
    if capture["exit"] != 0:
        client.close()
        raise RuntimeError("screenshot failed: " + str(capture["stderr"]))

    evidence = repository / "backups" / f"{timestamp}-qtdragon-es-visual"
    evidence.mkdir(parents=True, exist_ok=False)
    local_image = evidence / "desktop.png"
    sftp = client.open_sftp()
    try:
        sftp.get(str(remote_image), str(local_image))
        sftp.remove(str(remote_image))
    finally:
        sftp.close()
        client.close()

    report = {
        "schema_version": 1,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "processes": processes,
        "installed": installed,
        "capture_tool": executable,
        "capture": capture,
        "image": str(local_image),
        "remote_temporary_removed": True,
    }
    (evidence / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"evidence": str(evidence), "image": str(local_image)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
