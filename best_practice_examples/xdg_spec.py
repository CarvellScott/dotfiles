import os

# Full XDG spec details here:
# https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
# Where user-specific configurations should be written
XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", os.path.expandvars("$HOME/.config"))
# Where user-specific non-essential (cached) data should be written
XDG_CACHE_HOME = os.environ.get("XDG_CACHE_HOME", os.path.expandvars("$HOME/.cache"))
# Where user-specific data files should be written
XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME", os.path.expandvars("$HOME/.local/share"))
# Where user-specific state files should be written (persistent between app
# restarts)
XDG_STATE_HOME = os.environ.get("XDG_STATE_HOME", os.path.expandvars("$HOME/.local/state"))
# Used for non-essential, user-specific data files such as sockets, named
# pipes, etc.
XDG_RUNTIME_DIR = os.environ.get("XDG_RUNTIME_DIR", os.path.expandvars("/run/user/$UID"))

# If none of these dirs exist when writing, attempt to create it with
# permission 0700 (pathlib.Path.chmod(0o700)
