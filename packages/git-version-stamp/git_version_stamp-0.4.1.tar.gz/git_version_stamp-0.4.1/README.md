# git-version-stamp

This small utility (written in Python) creates a simple version code based
on the status of a git repo/tree for files of interest, mostly for use in
build scripts to embed into build output and/or name build artifacts.

You should also consider these more established tools:
- [dunamai](https://github.com/mtkennerly/dunamai#readme)
- [git describe](https://git-scm.com/docs/git-describe)
- [setuptools-git-versioning](https://setuptools-git-versioning.readthedocs.io/)
- [setuptools-scm](https://github.com/pypa/setuptools-scm#readme)
- [versioneer](https://github.com/python-versioneer/python-versioneer#readme)
- [versioningit](https://versioningit.readthedocs.io/)

The main differences with this one:
- In general it's much less developed than any of those
- It doesn't integrate with setuptools, it just spits out a version string
- It uses timestamp-oriented versioning (rather than last-tag-plus-change-count)
  for untagged builds, which is more useful for apps or firmware images
  but less appropriate for libraries
- It lets you pick a subset of files in the repo via include and exclude
  lists, and the version is based on the status of those files

If you actually use this, maybe let me (egnor@ofb.net) know so I'm a bit
more motivated to make it a proper project with docs and tests and stuff?
PRs welcome in any case.

## Usage

Install this package:
- `pip install git-version-stamp` (or use any pip-compatible installer)
- OR just copy `git_version_stamp.py` (it has no dependencies)

Invoke the utility from inside a git working tree:
- `git-version-stamp .` if installed with `pip` or similar
- OR `python -m git_version_stamp .`
- OR `./git_version_stamp.py .` if you copied the file
- OR `import git_version_stamp` and use the API described below

By default, it prints a version stamp to stdout reflecting the (sub)tree state:
- `YYYYMMDD-<tag>` if the tree is synced to a tagged version with no changes
- `YYYYMMDD.HHMMSS-git-<hash>` if the tree is synced to an untagged commit
- `YYYYMMDD.HHMMSS-mod-<user>@<host>` if the tree has been modified locally

The timestamp will be the committer time of the relevant commit, or the
latest local file modification time.

Command line arguments:
- list files/subtrees to scan (files in `.gitignore` will be skipped)
- `--exclude <dir/file> ...` (default: none) - ignore these files/subtrees
- `--wrap <format>` (default: `text`) - instead of plain text, use:
  - `text` - plain text (default)
  - `json` or `c_string` - JSON quoted string (also valid C/C++)
  - `cpp_flag` - `-DGIT_VERSION_STAMP=...` for C/C++ compiler
  - `cpp_macro` - `#define GIT_VERSION_STAMP "..."` for C/C++
  - `cpp_symbol` - `extern char GIT_VERSION_STAMP[] = "..."` for C/C++
  - `arduino_cli_flag` - `--build-property=compiler.cpp.extra_flags=-D...`
    for Arduino CLI
  - `shell` - quoted for shell scripts (or append `_shell` to any above)
- `--debug` - enable debug logging

## API

After importing the `git_version_stamp` in Python, you can invoke
`git_version_stamp.get(include=["."], exclude=[])` to get a `Stamp` object
representing the repo state.

The `Stamp` object has these properties/methods:
- `stamp.tag` - name of the most recent tag (`""` if untagged)
- `stamp.tag_commit` - SHA-1 of the commit that was tagged (`""` if untagged)
- `stamp.tag_time` - Unix time of the commit that was tagged (`0` if untagged)
- `stamp.commit` - SHA-1 of the most recent commit since the tag (`""` if none)
- `stamp.commit_time` - Unix time of that commit (`0` if none)
- `stamp.local_mod_time` - Unix time of the most recent local edit (`0` if none)
- `str(stamp)` - the version string as printed by the CLI
- `stamp.wrap(format="text")` - a re-encoded string as output by `--wrap`
