#!/usr/bin/env python3
"""Atomically deploy the validated QtDragon Spanish TS/QM to torno_v3."""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat

import paramiko


HOST = "cnc.taila1b901.ts.net"
CONFIG = PurePosixPath("/home/cnc/linuxcnc/configs/torno_v3")
LANGUAGES = CONFIG / "qtdragon" / "languages"
PROCESS_QUERY = r"""
ps -eo pid=,ppid=,comm=,args= | grep -E \
  '[l]inuxcnc|[l]inuxcncsvr|[q]tvcp|[m]illtask|[r]tapi_app|[h]alui|[Q]tWebEngineProcess'
"""
PROTECTED_FILES = (
    CONFIG / "torno_v3.ini",
    CONFIG / "torno_v3.hal",
    CONFIG / "custom.hal",
    CONFIG / "qtvcp_postgui.hal",
)


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(client: paramiko.SSHClient, command: str) -> tuple[int, str, str]:
    _, stdout, stderr = client.exec_command(command, timeout=30)
    output = stdout.read().decode("utf-8", errors="replace")
    error = stderr.read().decode("utf-8", errors="replace")
    return stdout.channel.recv_exit_status(), output, error


def read_remote(sftp: paramiko.SFTPClient, path: PurePosixPath) -> bytes:
    with sftp.open(str(path), "rb") as stream:
        return stream.read()


def remote_hashes(
    sftp: paramiko.SFTPClient, paths: tuple[PurePosixPath, ...]
) -> dict[str, str]:
    return {str(path): sha256(read_remote(sftp, path)) for path in paths}


def ensure_directory(sftp: paramiko.SFTPClient, path: PurePosixPath) -> bool:
    try:
        attributes = sftp.lstat(str(path))
    except FileNotFoundError:
        sftp.mkdir(str(path), mode=0o755)
        return True
    if stat.S_ISLNK(attributes.st_mode):
        raise RuntimeError(f"refusing symlink in deployment path: {path}")
    if not stat.S_ISDIR(attributes.st_mode):
        raise RuntimeError(f"deployment path is not a directory: {path}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--confirm-deploy",
        action="store_true",
        help="Required acknowledgement that LinuxCNC is stopped and deployment is authorized.",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Replace existing TS/QM atomically after saving them in local evidence.",
    )
    parser.add_argument(
        "--include-handler",
        action="store_true",
        help="Also deploy the reviewed local qtdragon_handler.py as a separate layer.",
    )
    args = parser.parse_args()
    if not args.confirm_deploy:
        parser.error("--confirm-deploy is required")

    repository = Path(__file__).resolve().parents[2]
    sources = {
        "qtdragon_es.ts": repository / "i18n" / "qtdragon-2.9.7" / "qtdragon_es.ts",
        "qtdragon_es.qm": repository / "i18n" / "qtdragon-2.9.7" / "qtdragon_es.qm",
    }
    targets = {
        "qtdragon_es.ts": LANGUAGES / "qtdragon_es.ts",
        "qtdragon_es.qm": LANGUAGES / "qtdragon_es.qm",
    }
    if args.include_handler:
        sources["qtdragon_handler.py"] = (
            repository / "i18n" / "qtdragon-2.9.7" / "qtdragon_handler.py"
        )
        targets["qtdragon_handler.py"] = CONFIG / "qtdragon" / "qtdragon_handler.py"
    payloads = {name: path.read_bytes() for name, path in sources.items()}
    if not payloads["qtdragon_es.qm"]:
        raise RuntimeError("refusing to deploy an empty QM")

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
    exit_code, processes, process_error = run(client, PROCESS_QUERY)
    if processes.strip():
        client.close()
        raise RuntimeError("LinuxCNC runtime is active; deployment refused:\n" + processes)

    transport = client.get_transport()
    if transport is None:
        client.close()
        raise RuntimeError("SSH transport was not established")
    host_key = base64.b64encode(
        hashlib.sha256(transport.get_remote_server_key().asbytes()).digest()
    ).decode("ascii")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    evidence = repository / "backups" / f"{timestamp}-qtdragon-es-deploy"
    evidence.mkdir(parents=True, exist_ok=False)
    sftp = client.open_sftp()
    created_directories: list[str] = []
    existing: dict[str, dict[str, object]] = {}
    temporary_paths: list[PurePosixPath] = []
    deployed: list[str] = []
    try:
        base_attributes = sftp.lstat(str(CONFIG))
        if stat.S_ISLNK(base_attributes.st_mode) or not stat.S_ISDIR(base_attributes.st_mode):
            raise RuntimeError(f"invalid configuration root: {CONFIG}")
        protected_before = remote_hashes(sftp, PROTECTED_FILES)

        for directory in (CONFIG / "qtdragon", LANGUAGES):
            if ensure_directory(sftp, directory):
                created_directories.append(str(directory))

        for name in payloads:
            target = targets[name]
            try:
                old_data = read_remote(sftp, target)
            except FileNotFoundError:
                continue
            existing[name] = {"bytes": len(old_data), "sha256": sha256(old_data)}
            (evidence / f"before-{name}").write_bytes(old_data)
            if not args.replace_existing:
                raise RuntimeError(f"target already exists; refusing implicit replacement: {target}")

        for name, data in payloads.items():
            target = targets[name]
            temporary = target.parent / f".{name}.upload-{timestamp}"
            temporary_paths.append(temporary)
            with sftp.open(str(temporary), "wb") as stream:
                stream.write(data)
                stream.flush()
            sftp.chmod(str(temporary), 0o644)
            remote_data = read_remote(sftp, temporary)
            if sha256(remote_data) != sha256(data):
                raise RuntimeError(f"remote temporary hash mismatch: {temporary}")

        # The runtime artifact is renamed last. Both uploads have already been
        # verified, so QtDragon can never observe a partial QM file.
        deployment_order = ["qtdragon_es.ts"]
        if args.include_handler:
            deployment_order.append("qtdragon_handler.py")
        deployment_order.append("qtdragon_es.qm")
        for name in deployment_order:
            target = targets[name]
            temporary = target.parent / f".{name}.upload-{timestamp}"
            if name in existing:
                sftp.posix_rename(str(temporary), str(target))
            else:
                sftp.rename(str(temporary), str(target))
            temporary_paths.remove(temporary)
            deployed.append(str(target))

        protected_after = remote_hashes(sftp, PROTECTED_FILES)
        if protected_after != protected_before:
            raise RuntimeError("protected INI/HAL hashes changed during deployment")

        installed: dict[str, dict[str, object]] = {}
        for name, local_data in payloads.items():
            target = targets[name]
            attributes = sftp.lstat(str(target))
            remote_data = read_remote(sftp, target)
            installed[str(target)] = {
                "bytes": len(remote_data),
                "sha256": sha256(remote_data),
                "expected_sha256": sha256(local_data),
                "mode": oct(stat.S_IMODE(attributes.st_mode)),
                "uid": attributes.st_uid,
                "gid": attributes.st_gid,
            }

        manifest = {
            "schema_version": 1,
            "deployed_at_utc": datetime.now(timezone.utc).isoformat(),
            "remote_host_key_sha256": host_key,
            "runtime_processes_before": processes,
            "runtime_query_exit": exit_code,
            "runtime_query_stderr": process_error,
            "config_root": str(CONFIG),
            "created_directories": created_directories,
            "existing_targets": existing,
            "deployed": deployed,
            "installed": installed,
            "protected_hashes_before": protected_before,
            "protected_hashes_after": protected_after,
            "remote_writes": ["mkdir", "upload temporary", "chmod", "rename"],
            "system_paths_modified": [],
        }
        (evidence / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    finally:
        for temporary in temporary_paths:
            try:
                sftp.remove(str(temporary))
            except OSError:
                pass
        sftp.close()
        client.close()

    print(json.dumps({"evidence": str(evidence), "deployed": deployed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
