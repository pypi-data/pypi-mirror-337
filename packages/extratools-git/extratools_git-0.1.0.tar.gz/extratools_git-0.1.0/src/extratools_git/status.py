from pathlib import Path
from typing import Any

import sh


def get_status(path: str = '.') -> dict[str, Any] | None:
    try:
        output: str = str(sh.git(
            "status", "--short", "--branch", "--porcelain=2",
            _cwd=Path(path).expanduser(),
        ))
    except Exception:
        return None

    return {
        "path": path,
        **parse_status(output),
    }


def parse_status(output: str) -> dict[str, Any]:
    oid: str | None = None

    head: str | None = None
    upstream: str | None = None

    ahead: int = 0
    behind: int = 0

    staged: list[str] = []
    unstaged: list[str] = []
    untracked: list[str] = []

    for line in output.rstrip('\n').splitlines():
        if line.startswith('#'):
            if line.startswith("# branch.oid "):
                oid = line.rsplit(' ', 1)[1]
            if line.startswith("# branch.head "):
                branch = line.rsplit(' ', 1)[1]
                if branch != "(detached)":
                    head = branch
            elif line.startswith("# branch.upstream "):
                branch = line.rsplit(' ', 1)[1]
                if branch != "(detached)":
                    upstream = branch
            elif line.startswith("# branch.ab "):
                ahead, behind = [abs(int(x)) for x in line.rsplit(' ', 2)[1:]]
        elif line.startswith('?'):
            untracked.append(line.rsplit(' ', -1)[1])
        elif not line.startswith('!'):
            vals: list[str] = line.split(' ')

            path: str = vals[-1]

            submodule_flags: str = vals[2]
            if submodule_flags[0] == 'S' and submodule_flags[3] == 'U':
                untracked.append(path)

            stage_flags: str = vals[1]
            if stage_flags[0] != '.':
                staged.append(path)
            if stage_flags[1] != '.':
                unstaged.append(path)

    return {
        "oid": oid,
        "branch": {
            "head": head,
            "upstream": upstream,
        },
        "commits": {
            "ahead": ahead,
            "behind": behind,
        },
        "files": {
            "staged": staged,
            "unstaged": unstaged,
            "untracked": untracked,
        },
    }
