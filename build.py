#!/usr/bin/env python3

import sys
from pathlib import Path
from subprocess import run, PIPE
from hashlib import sha256

from functools import cache

input_dir = Path("mffm11_v2024.04.04_HarmonyOSSans/")
output_file = Path("./dist/Lovemilk-MFFMv11-HarmonyOSSans-{version}.zip")
cache_dir = Path(".cache/")

module_prop_file = input_dir / "module.prop"
commit_cache_file = cache_dir / "last_commit.id"
module_prop_cache_file = cache_dir / f"{module_prop_file.name}.hash"


def make_dir(path: Path):
    if path.is_dir():
        return

    if path.exists():
        path.unlink(missing_ok=True)
    path.mkdir(parents=True, exist_ok=True)

@cache  # 这个函数在 build 时期应该返回同一个版本号
def get_version():
    with module_prop_file.open("r", encoding="u8") as fp:
        while line := fp.readline():
            if not line.startswith("version="):
                continue

            data = line.split("=", 1)[1].strip()
            return data.split("-", 1)[0] if "-" in data else data


def get_last_commit():
    process = run("git rev-parse HEAD", stdout=PIPE, shell=True)
    assert process.returncode == 0, "failed to get last commit"
    return process.stdout.decode("u8").strip()


def get_last_commit_message():
    process = run("git log -1 --pretty=%B", stdout=PIPE, shell=True)
    assert process.returncode == 0, "failed to get last commit message"
    return process.stdout.decode("u8").strip()


def hash_file(path: Path, *, chunk_size: int = 4096):
    hasher = sha256()
    with path.open("rb") as fp:
        while chunk := fp.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def build(force: bool = False) -> tuple[Path, bool]:
    version = get_version()
    _output_file = Path(str(output_file.absolute().resolve()).format(version=version))

    make_dir(_output_file.parent)
    make_dir(cache_dir)

    if not force and (
        _output_file.is_file()
        and (
            commit_cache_file.read_text()
            if commit_cache_file.is_file()
            else None
        )
        == get_last_commit()
        and (
            module_prop_cache_file.read_text()
            if module_prop_cache_file.is_file()
            else None
        )
        == hash_file(module_prop_file)
    ):
        print("no changes detected, skipping build")
        return _output_file, False

    # _output_file.unlink(missing_ok=True)

    process = run(
        [
            "7z",
            "a",
            str(_output_file),
            f"{str(input_dir.absolute())}/*",
        ]
    )
    assert process.returncode == 0, "failed to create zip file"

    commit_cache_file.write_text(get_last_commit())
    module_prop_cache_file.write_text(hash_file(module_prop_file))

    print(f"build completed, output file name: {_output_file.name}")
    return _output_file, True


def release(*files: Path):
    print("\ncreating release...\n")
    version = get_version()
    release_files = map(lambda p: str(p.absolute().resolve()), files)
    process = run(
        [
            "gh",
            "release",
            "create",
            f"V{version}",
            "--title",
            f"V{version}",
            "--notes",
            f"{get_last_commit_message()}",
        ] + list(release_files)
    )

    assert process.returncode == 0, "failed to create release"
    print("\nrelease created successfully")


if __name__ == "__main__":
    args = tuple(map(lambda s: s.lower(), sys.argv[1:]))

    release_file, has_built = build(("--force" in args or "-f" in args))

    if "--release" in args or "-r" in args:
        if not has_built and input("no changes detected, are you sure to release? (y/N): ").lower() != "y":
            sys.exit(0)

        release(release_file)
