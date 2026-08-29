#!/usr/bin/env python3
"""Fetch the installed QtDragon translation sources without modifying the CNC.

The remote side is accessed through SFTP reads and fixed diagnostic commands.
No remote file is created, changed, renamed, or removed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import paramiko


REMOTE_FILES = (
    PurePosixPath("/usr/bin/qtvcp"),
    PurePosixPath("/usr/lib/python3/dist-packages/qtvcp/qt_pstat.py"),
    PurePosixPath("/usr/share/qtvcp/screens/qtdragon/qtdragon.ui"),
    PurePosixPath("/usr/share/qtvcp/screens/qtdragon/qtdragon_handler.py"),
    PurePosixPath("/usr/share/qtvcp/screens/qtdragon/qtdragon.qss"),
    PurePosixPath("/usr/share/qtvcp/screens/qtdragon/qtdragon_ABOUT"),
    PurePosixPath("/usr/share/qtvcp/screens/qtdragon/version.txt"),
    PurePosixPath("/usr/lib/python3/dist-packages/qtvcp/widgets/action_button.py"),
    PurePosixPath("/usr/lib/python3/dist-packages/qtvcp/widgets/file_manager.py"),
    PurePosixPath("/usr/lib/python3/dist-packages/qtvcp/widgets/gcode_editor.py"),
    PurePosixPath("/usr/lib/python3/dist-packages/qtvcp/widgets/jog_increments.py"),
    PurePosixPath("/usr/lib/python3/dist-packages/qtvcp/widgets/status_label.py"),
    PurePosixPath("/usr/lib/python3/dist-packages/qtvcp/widgets/tool_offsetview.py"),
)

READ_ONLY_DIAGNOSTICS = {
    "packages": (
        "dpkg-query -W linuxcnc-uspace linuxcnc-doc-es locales "
        "qttranslations5-l10n 2>&1 || true"
    ),
    "locale": "locale; python3 -c 'from PyQt5.QtCore import QLocale; print(QLocale.system().name())'",
    "screen_languages": (
        "find /usr/share/qtvcp/screens/qtdragon -maxdepth 3 -type f "
        "\\( -name '*.ts' -o -name '*.qm' \\) -print 2>/dev/null | sort"
    ),
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        description="Read the installed QtDragon sources from the CNC."
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=repository / "vendor" / "linuxcnc-2.9.7-qtdragon",
        help="Local snapshot directory.",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=repository / ".env",
        help="Local credential file excluded from Git.",
    )
    parser.add_argument(
        "--host",
        default="cnc.taila1b901.ts.net",
        help="SSH host already present in known_hosts.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing local snapshot. Never changes the remote host.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    destination = args.destination.resolve()
    if destination.exists() and any(destination.iterdir()) and not args.force:
        raise SystemExit(
            f"Destination is not empty: {destination}. Use --force to replace local files."
        )

    env = read_env(args.env_file.resolve())
    username = env["CNC_SSH_USER"]
    password = env["CNC_SSH_PASSWORD"]

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(
        args.host,
        username=username,
        password=password,
        timeout=10,
        banner_timeout=10,
        auth_timeout=10,
        allow_agent=False,
        look_for_keys=False,
    )

    transport = client.get_transport()
    if transport is None:
        client.close()
        raise RuntimeError("SSH transport was not established")
    host_key_sha256 = __import__("base64").b64encode(
        hashlib.sha256(transport.get_remote_server_key().asbytes()).digest()
    ).decode("ascii")

    diagnostics: dict[str, dict[str, object]] = {}
    for name, command in READ_ONLY_DIAGNOSTICS.items():
        _, stdout, stderr = client.exec_command(command, timeout=30)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        diagnostics[name] = {
            "exit": stdout.channel.recv_exit_status(),
            "stdout": out,
            "stderr": err,
        }

    destination.mkdir(parents=True, exist_ok=True)
    manifest_files: list[dict[str, object]] = []
    sftp = client.open_sftp()
    try:
        for remote_path in REMOTE_FILES:
            attributes = sftp.stat(str(remote_path))
            with sftp.open(str(remote_path), "rb") as remote_file:
                data = remote_file.read()
            relative = Path(*remote_path.parts[1:])
            local_path = destination / relative
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(data)
            os.utime(local_path, (attributes.st_atime, attributes.st_mtime))
            manifest_files.append(
                {
                    "remote_path": str(remote_path),
                    "local_path": relative.as_posix(),
                    "bytes": len(data),
                    "mtime_utc": datetime.fromtimestamp(
                        attributes.st_mtime, tz=timezone.utc
                    ).isoformat(),
                    "sha256": sha256_bytes(data),
                }
            )
    finally:
        sftp.close()
        client.close()

    manifest = {
        "captured_at_utc": datetime.now(tz=timezone.utc).isoformat(),
        "remote_host": args.host,
        "remote_access": "SFTP read-only plus fixed diagnostic commands",
        "host_key_sha256": host_key_sha256,
        "files": manifest_files,
        "diagnostics": diagnostics,
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "destination": str(destination),
                "files": len(manifest_files),
                "bytes": sum(int(item["bytes"]) for item in manifest_files),
                "remote_writes": 0,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
