#!/usr/bin/env python3
"""Request a controlled LinuxCNC shutdown and verify every runtime exits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
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
    parser.add_argument(
        "--confirm-controlled-shutdown",
        action="store_true",
        help="Required acknowledgement that the operator authorized shutdown.",
    )
    parser.add_argument(
        "--terminate-qtdragon",
        action="store_true",
        help="Send SIGTERM only to the exact torno_v3 QtDragon process.",
    )
    parser.add_argument(
        "--close-error-dialog",
        action="store_true",
        help="Capture LinuxCNC temporary logs and SIGTERM only show_errors.tcl.",
    )
    parser.add_argument(
        "--close-window",
        action="store_true",
        help="Request WM_DELETE_WINDOW for the exact QtDragon window title.",
    )
    args = parser.parse_args()
    if not args.confirm_controlled_shutdown:
        parser.error("--confirm-controlled-shutdown is required")

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
    if not str(before["stdout"]).strip():
        client.close()
        print(json.dumps({"already_stopped": True, "remaining": ""}))
        return 0

    # `linuxcnc -k` is LinuxCNC's own stale-runtime cleanup mode.
    shutdown = run(client, "/usr/bin/linuxcnc -k", timeout=45)

    window_close: dict[str, object] | None = None
    if args.close_window:
        window_close = run(
            client,
            r"""
if command -v wmctrl >/dev/null 2>&1; then
    DISPLAY=:0 XAUTHORITY=/home/cnc/.Xauthority \
      wmctrl -F -c 'QTvcp-Screen-qtdragon'
elif command -v xdotool >/dev/null 2>&1; then
    DISPLAY=:0 XAUTHORITY=/home/cnc/.Xauthority \
      xdotool search --name '^QTvcp-Screen-qtdragon$' windowclose
else
    printf 'No window-close utility found\n' >&2
    exit 127
fi
""",
        )

    qtvcp_term: dict[str, object] | None = None
    if args.terminate_qtdragon:
        qtvcp_term = run(
            client,
            r"""
pid="$(pgrep -f '^/usr/bin/python3 /usr/bin/qtvcp -ini /home/cnc/linuxcnc/configs/torno_v3/torno_v3.ini qtdragon$' || true)"
if [ -n "$pid" ]; then
    kill -TERM "$pid"
fi
""",
        )

    temporary_logs: dict[str, object] | None = None
    error_dialog_term: dict[str, object] | None = None
    if args.close_error_dialog:
        temporary_logs = run(
            client,
            r"""
for file in /tmp/linuxcnc.debug.* /tmp/linuxcnc.print.*; do
    if [ -r "$file" ]; then
        printf '\nFILE:%s\n' "$file"
        tail -n 240 "$file"
    fi
done
""",
        )
        error_dialog_term = run(
            client,
            r"""
pid="$(pgrep -f '^/usr/bin/wish8.6 /usr/lib/tcltk/linuxcnc/show_errors.tcl ' || true)"
if [ -n "$pid" ]; then
    kill -TERM "$pid"
fi
""",
        )

    remaining = ""
    for _ in range(30):
        check = run(client, PROCESS_QUERY)
        remaining = str(check["stdout"]).strip()
        if not remaining:
            break
        time.sleep(1)
    client.close()

    result = {
        "already_stopped": False,
        "before": str(before["stdout"]).strip(),
        "shutdown_exit": shutdown["exit"],
        "shutdown_stdout": str(shutdown["stdout"]).strip(),
        "shutdown_stderr": str(shutdown["stderr"]).strip(),
        "window_close": window_close,
        "qtvcp_sigterm": qtvcp_term,
        "temporary_logs": temporary_logs,
        "error_dialog_sigterm": error_dialog_term,
        "remaining": remaining,
        "used_sigkill": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if remaining else 0


if __name__ == "__main__":
    raise SystemExit(main())
