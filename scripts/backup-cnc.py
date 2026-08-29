from __future__ import annotations

import json
import os
import stat
from datetime import datetime
from pathlib import Path, PurePosixPath

import paramiko


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def download_tree(sftp: paramiko.SFTPClient, remote: PurePosixPath, local: Path) -> tuple[int, int]:
    local.mkdir(parents=True, exist_ok=True)
    count = 0
    total_bytes = 0
    for item in sftp.listdir_attr(str(remote)):
        remote_item = remote / item.filename
        local_item = local / item.filename
        if stat.S_ISDIR(item.st_mode):
            nested_count, nested_bytes = download_tree(sftp, remote_item, local_item)
            count += nested_count
            total_bytes += nested_bytes
        elif stat.S_ISREG(item.st_mode):
            sftp.get(str(remote_item), str(local_item))
            os.utime(local_item, (item.st_atime, item.st_mtime))
            count += 1
            total_bytes += item.st_size
    return count, total_bytes


def main() -> int:
    repository = Path(__file__).resolve().parent.parent
    env = read_env(repository / ".env")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = repository / "backups" / f"{timestamp}-cnc" / "linuxcnc"

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(
        "cnc.taila1b901.ts.net",
        username=env["CNC_SSH_USER"],
        password=env["CNC_SSH_PASSWORD"],
        timeout=10,
        banner_timeout=10,
        auth_timeout=10,
        allow_agent=False,
        look_for_keys=False,
    )
    inventory_commands = {
        "identity": "hostname; id; uname -a; cat /etc/debian_version",
        "packages": "dpkg-query -W -f='${Package}|${Version}\\n' linuxcnc-uspace mesaflash 2>/dev/null || true",
        "processes": "ps -eo pid=,args= | grep -E '[l]inuxcnc|[q]tvcp|[m]illtask' || true",
        "launchers": "for f in /home/cnc/Escritorio/*.desktop; do [ -f \"$f\" ] && { echo FILE:$f; sed -n '1,120p' \"$f\"; }; done",
        "modes": "find /home/cnc/linuxcnc -printf '%m|%u:%g|%y|%p\\n' 2>/dev/null | sort",
    }
    inventory: dict[str, dict[str, object]] = {}
    for name, command in inventory_commands.items():
        _, stdout, stderr = client.exec_command(command, timeout=30)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        inventory[name] = {
            "exit": stdout.channel.recv_exit_status(),
            "stdout": out,
            "stderr": err,
        }
    transport = client.get_transport()
    if transport is not None:
        inventory["ssh"] = {
            "host": "cnc.taila1b901.ts.net",
            "host_key_sha256": __import__("base64").b64encode(
                __import__("hashlib").sha256(transport.get_remote_server_key().asbytes()).digest()
            ).decode("ascii"),
        }

    destination.parent.mkdir(parents=True, exist_ok=True)
    (destination.parent / "remote-inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    sftp = client.open_sftp()
    count, total_bytes = download_tree(
        sftp, PurePosixPath("/home/cnc/linuxcnc"), destination
    )
    sftp.close()
    client.close()

    hashes = []
    import hashlib

    for path in sorted(destination.rglob("*")):
        if not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.append(f"{digest}  {path.relative_to(destination.parent).as_posix()}")
    (destination.parent / "sha256.txt").write_text("\n".join(hashes) + "\n", encoding="ascii")

    print(json.dumps({"destination": str(destination.parent), "files": count, "bytes": total_bytes}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
