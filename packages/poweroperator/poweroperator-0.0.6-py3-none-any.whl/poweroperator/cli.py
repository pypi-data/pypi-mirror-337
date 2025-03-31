#!/usr/bin/env python3
import sys
import traceback
import tempfile
import os
import atexit
import json
import getpass
import socket
from typing import List, Dict, Set
from pathlib import Path
from scalene import scalene_profiler  # type: ignore
from .poweroperator_api import upload_mark_with_file
from .local_module_indexer import collect_module_data


def should_trace(s: str) -> bool:
    # TODO: is this used? the sclane_profiler.__main__.main function has it
    if scalene_profiler.Scalene.is_done():
        return False
    return scalene_profiler.Scalene.should_trace(s)


def get_temp_profile_path() -> str:
    temp_file = tempfile.NamedTemporaryFile(
        suffix=".json", prefix="profile_", delete=False
    )
    temp_filename = temp_file.name
    temp_file.close()  # close but keep the name

    def cleanup():
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    atexit.register(cleanup)
    return temp_filename


def fix_cmdline_args(profile_path: str) -> None:
    sys.argv[1:1] = ["--cli", "--no-browser", "--json", f"--outfile={profile_path}"]


def file_exists_and_not_empty(file_path: str) -> bool:
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0


def find_entry_points_from_args(argv: List[str]) -> List[Path]:
    entry_points = []
    for arg in argv:
        if arg.endswith(".py") and Path(arg).is_file():
            entry_points.append(Path(arg).resolve())
    return entry_points


def collect_all_modules(project_root: Path, entry_points: List[Path]) -> List[Dict]:
    seen_paths: Set[Path] = set()
    all_modules: List[Dict] = []

    for entry in entry_points:
        modules = collect_module_data(project_root, entry)
        for mod in modules:
            path = Path(mod["file_name"]).resolve()
            if path not in seen_paths:
                seen_paths.add(path)
                all_modules.append(mod)

    return all_modules


def main() -> None:
    print("[poweroperator] Starting program under benchmarking...")
    profile_path = get_temp_profile_path()
    fix_cmdline_args(profile_path)

    try:
        from scalene import scalene_profiler  # type: ignore

        try:
            scalene_profiler.Scalene.main()
        finally:
            if not file_exists_and_not_empty(profile_path):
                print(
                    "[poweroperator] Benchmarked program exited but no benchmarks available, skipping upload."
                )
            else:
                print(
                    "[poweroperator] Benchmarked program exited. Collecting benchmarks and context..."
                )

                entry_points = find_entry_points_from_args(sys.argv)
                if not entry_points:
                    print("[poweroperator] No Python entry point files found")

                project_root = Path.cwd()
                modules = collect_all_modules(project_root, entry_points)

                user = getpass.getuser()
                hostname = socket.gethostname()
                cwd = os.getcwd()
                upload_mark_with_file(
                    user,
                    "function-1",
                    profile_path,
                    hostname,
                    sys.argv,
                    os.environ,
                    cwd,
                    modules,
                )
                print("[poweroperator] Upload successful")
    except Exception as exc:
        sys.stderr.write(
            "[poweroperator] Error: calling Scalene profiler main function failed: %s\n"
            % exc
        )
        traceback.print_exc()


if __name__ == "__main__":
    main()
