from typing import Any

from colors import color

from .status import get_status


def get_prompt() -> str:
    status: dict[str, Any] | None = get_status()
    if status is None:
        return ""

    branch: str | None = status["branch"]["head"]
    has_remote: bool = status["branch"]["upstream"] is not None
    ahead: int = status["commits"]["ahead"]
    behind: int = status["commits"]["behind"]
    staged = bool(status["files"]["staged"])
    unstaged = bool(status["files"]["unstaged"])
    untracked = bool(status["files"]["untracked"])

    prompt: str = ""

    if branch is None:
        prompt += color("(detached)", fg="red")
    else:
        prompt += color(branch, fg=(
            "green" if has_remote else "cyan"
        ))

        if has_remote:
            remote_flags: str = ""

            if ahead > 0:
                remote_flags += color('↑', fg="blue", style="bold")
            if behind > 0:
                remote_flags += color('↓', fg="yellow", style="bold")

            if remote_flags:
                prompt += remote_flags

    local_flags: str = ""

    if staged:
        local_flags += color('+', fg="green", style="bold")
    if unstaged:
        local_flags += color('*', fg="red", style="bold")
    if untracked:
        local_flags += color('?', fg="cyan", style="bold")

    if local_flags:
        prompt += ':' + local_flags

    return prompt


def print_prompt() -> None:
    print(get_prompt(), end="")
