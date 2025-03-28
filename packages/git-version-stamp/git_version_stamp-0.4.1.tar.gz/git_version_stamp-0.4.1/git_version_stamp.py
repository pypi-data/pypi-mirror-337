#!/usr/bin/env python3

import copy
import dataclasses
import getpass
import json
import logging
import platform
import re
import shlex
import subprocess
import time
from pathlib import Path


LOGGER = logging.getLogger("git_version_stamp")


@dataclasses.dataclass
class Stamp:
    tag: str = ""
    tag_commit: str = ""
    tag_time: int = 0
    commit: str = ""
    commit_time: int = 0
    local_mod_time: int = 0

    def __bool__(self):
        return bool(self.tag or self.commit or self.local_mod_time)

    def __str__(self):
        return _format(self)

    def wrap(self, wrapping: str, **kwargs) -> str:
        return _wrap(wrapping, _format(self), **kwargs)


def _format(stamp):
    # YYYYMMDD.HHMMSS-mod-user@host  (modified local client)
    if stamp.local_mod_time:
        t = time.strftime('%Y%m%d.%H%M%S', time.gmtime(stamp.local_mod_time))
        user = f"{getpass.getuser()}@{platform.node()}"
        return f"{t}-mod-{user}"

    # YYYYMMDD.HHMMSS-git-HASHHASH   (clean but untagged commit)
    if stamp.commit:
        t = time.strftime("%Y%m%d.%H%M%S", time.gmtime(stamp.commit_time))
        return f"{t}-git-{stamp.commit[:8]}"

    # YYYYMMDD-<tag>                 (clean tagged commit)
    if stamp.tag:
        t = time.strftime("%Y%m%d", time.gmtime(stamp.tag_time))
        return f"{t}-{stamp.tag}"

    return ""  # no commit info


def _wrap(wrapping: str, text: str, symbol="GIT_VERSION_STAMP") -> str:
    if wrapping in ("", "text"):
        return text
    if wrapping in ("json", "c_string"):
        return json.dumps(text)
    if wrapping == "cpp_flag":
        return f"-D{symbol}={_wrap('c_string', text)}"
    if wrapping == "cpp_macro":
        return f"#define {symbol} {_wrap('c_string', text)}"
    if wrapping == "cpp_symbol":
        return f"extern char const {symbol}[] = {_wrap('c_string', text)};"
    if wrapping == "cpp_flag_shell":
        return f"-D{symbol}={_wrap('c_string_shell', text)}"
    if wrapping == "arduino_cli_flag":
        cpp = _wrap("cpp_flag", text)
        return f"--build-property=compiler.cpp.extra_flags={cpp}"
    if wrapping == "arduino_cli_flag_shell":
        cpp = _wrap("cpp_flag_shell", text)
        return f"--build-property=compiler.cpp.extra_flags={cpp}"
    if wrapping == "shell" or wrapping.endswith("_shell"):
        return shlex.quote(_wrap(wrapping[:-6], text))
    raise ValueError(f"Bad wrapper format: {wrapping}")


def get(*, include, exclude=[]):
    git_toplevel = _shell_lines("git", "rev-parse", "--show-toplevel")[0]
    top_dir = Path(git_toplevel).resolve()
    include_rel, exclude_rel = [], []
    for paths, add_to in ((include, include_rel), (exclude, exclude_rel)):
        for path in (paths or []):
            add_to.append(Path(path).resolve().relative_to(top_dir))

    LOGGER.debug("  Working tree: %s", top_dir)
    LOGGER.debug("  INC %s", ", ".join(str(p) for p in include_rel) or "(none)")
    LOGGER.debug("  exc %s", ", ".join(str(p) for p in exclude_rel) or "(none)")

    is_included = lambda name: (
        any(path.is_relative_to(r) for r in include_rel) and
        not any(path.is_relative_to(r) for r in exclude_rel)
        if (path := Path(name)) else False
    )

    ref_list_lines = _shell_lines(
        "git", "for-each-ref", "--sort=-creatordate", "--merged=HEAD",
        "refs/tags/",
        "--format=%(objectname) %(objecttype) %(creatordate:unix) %(refname)"
    )

    # <sha> "tag" <time> <name>   (note, ref names may not have spaces)
    ver_ref_rx = re.compile(
        r"^(?P<sha>[0-9a-f]+) tag (?P<time>\d+) refs/tags/(?P<name>\S+)"
    )

    out = Stamp()
    for ref_line in ref_list_lines:
        if rev_match := ver_ref_rx.match(ref_line):
            out.tag_commit = rev_match.group("sha") or ""
            out.tag = rev_match.group("name") or ""
            out.tag_time = int(rev_match.group("time") or 0)
            LOGGER.debug("  Latest: %s", out.tag)
            break
        else:
            LOGGER.debug("  Skipping ref: %s", ref_line)

    if not out.tag_commit: LOGGER.debug("  No version tags found")

    rev_range = f"{out.tag_commit}..HEAD" if out.tag_commit else "HEAD"
    rev_list_lines = _shell_lines("git", "rev-list", rev_range)
    diff_tree_lines = _shell_lines(
        "git", "diff-tree", "-r", "--stdin", "--format=%H %ct",
        *(["--root"] if not out.tag_commit else []),
        input="".join(f"{l}\n" for l in rev_list_lines),
    )

    # <sha> <time>
    commit_rx = re.compile(r"^(?P<sha>[0-9a-f]+) (?P<time>\d+)$")

    # :<a_mode> <b_mode> <a_sha> <b_sha> <op><score> \t <a> \t <b>
    file_change_rx = re.compile(
        r"^:\d+ \d+ [0-9a-f]+ [0-9a-f]+ (?P<op>[A-Z]+)\d*"
        r"\t(?P<a>[^\t]+)(\t(?P<b>[^\t]+))?$"
    )

    current_sha = ""
    current_time = 0
    out.commit = ""
    out.commit_time = 0
    for line in diff_tree_lines:
        if commit_match := commit_rx.match(line):
            current_sha = commit_match.group("sha")
            current_time = int(commit_match.group("time"))
            LOGGER.debug(
                "  Commit: %s (%s)", current_sha[:8],
                time.strftime("%Y%m%d.%H%M%S", time.gmtime(current_time))
            )

        elif file_match := file_change_rx.match(line):
            for name in filter(None, file_match.group("a", "b")):
                if not current_time:
                    raise ValueError(f"Early git-diff-tree output: {line}")
                if is_included(name):
                    LOGGER.debug("    INC %s", name)
                    if current_time > out.commit_time:
                        out.commit_time = current_time
                        out.commit = current_sha
                else:
                    LOGGER.debug("    exc %s", name)

        elif line:
            raise ValueError(f"Bad git-diff-tree output: {line}")

    if out.commit_time:
        LOGGER.debug(
            "  => Last included commit %s (%s)", out.commit[:8],
            time.strftime("%Y%m%d.%H%M%S", time.gmtime(out.commit_time)),
        )
    else:
        LOGGER.debug("  => Unchanged since %s", out.tag or "repo start")

    diff_index_lines = _shell_lines("git", "diff-index", "HEAD")
    name_op = {}
    for line in diff_index_lines:
        if file_match := file_change_rx.match(line):
            for name in filter(None, file_match.group("a", "b")):
                if is_included(name):
                    LOGGER.debug("  INC %s", name)
                    name_op[name] = file_match.group("op")
                else:
                    LOGGER.debug("  exc %s", name)

        elif line:
            raise ValueError(f"Bad git-diff-index output: {line}")

    ls_files_lines = _shell_lines(
        "git", "ls-files", "--others", "--exclude-standard", cwd=top_dir
    )
    for name in ls_files_lines:
        if name and is_included(name):
            LOGGER.debug("  INC %s", name)
            name_op[name] = "?"
        elif name:
            LOGGER.debug("  exc %s", name)

    name_op_stat = {}
    while name_op:
        name, op = name_op.popitem()
        path = top_dir / name
        try:
            name_op_stat[name] = (op, path.stat())
            continue
        except FileNotFoundError:
            name_op_stat[name] = (op, None)

        try:
            parent_name = str(path.parent.relative_to(top_dir))
        except ValueError:
            continue

        if parent_name not in name_op_stat:
            name_op.setdefault(parent_name, "PD")

    debug_lines = []
    for name, (op, st) in sorted(name_op_stat.items()):
        out.local_mod_time = max(out.local_mod_time, st.st_mtime if st else 0)
        mdate = st and time.strftime('%Y%m%d.%H%M%S', time.gmtime(st.st_mtime))
        debug_lines.append(f"{mdate or '               '} {op} {name}")
    LOGGER.debug(
        "%d modified files in scope%s", len(name_op_stat),
        "".join(f"\n  {line}" for line in debug_lines),
    )

    return out


def _shell_lines(*a, **kw):
    LOGGER.debug("🐚 %s", " ".join(shlex.quote(str(arg)) for arg in a))
    ret = subprocess.run(a, stdout=subprocess.PIPE, text=True, check=True, **kw)
    return ret.stdout.strip("\n").split("\n")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("include", metavar="DIR", nargs="+", type=Path)
    parser.add_argument("--exclude", metavar="DIR", nargs="+", type=Path)
    parser.add_argument("--wrap", metavar="FORMAT", default="")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level)

    stamp = get(include=args.include, exclude=args.exclude)
    if not stamp: raise SystemExit("No files found")
    print(stamp.wrap(args.wrap))


if __name__ == "__main__":
    main()
