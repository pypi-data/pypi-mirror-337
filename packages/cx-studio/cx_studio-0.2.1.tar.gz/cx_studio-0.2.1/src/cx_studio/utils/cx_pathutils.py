import os
from pathlib import Path


def normalize_path(path: Path, anchor: Path = None, follow_symlinks=True) -> Path:
    path = Path(path)
    andchor = Path(anchor) if anchor else Path.cwd()
    if not path.is_absolute():
        path = andchor.joinpath(path)
    return (
        path.resolve(follow_symlinks=follow_symlinks)
        if follow_symlinks
        else path.absolute()
    )


def normalize_suffix(suffix: str, with_dot=True) -> str:
    s = str(suffix).strip().strip(".").lower()
    return "." + s if with_dot else s


def force_suffix(source: Path, suffix: str) -> Path:
    if not source:
        return None
    source = Path(source)
    suffix = normalize_suffix(suffix)
    return source if source.suffix == suffix else source.with_suffix(suffix)


def take_dir(source: Path) -> Path:
    source = normalize_path(source)
    return source if source.is_dir() else source.parent


def is_excutable(cmd: Path) -> bool:
    cmd = normalize_path(cmd)
    return cmd.exists() and os.access(cmd, os.X_OK)


def is_file_in_dir(file: Path, dir: Path) -> bool:
    f = str(normalize_path(file).resolve().absolute())
    d = str(normalize_path(dir).resolve().absolute())
    # TODO: 考虑使用pathlib的relative_to方法，避免使用字符串比较
    return f in d
