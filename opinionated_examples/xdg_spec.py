import os
import pathlib

# Full XDG spec details here:
# https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
def _xdg_dir(env_variable, default):
    str_path = os.environ.get(env_variable, os.path.expandvars(default))
    return pathlib.Path(str_path)

# Where user-specific configurations should be written
CONFIG_HOME = _xdg_dir("XDG_CONFIG_HOME", "$HOME/.config")
# Where user-specific non-essential (cached) data should be written
CACHE_HOME = _xdg_dir("XDG_CACHE_HOME", "$HOME/.cache")
# Where user-specific data files should be written
DATA_HOME = _xdg_dir("XDG_DATA_HOME", "$HOME/.local/share")
# Where user-specific state files should be written (persistent between app
# restarts)
STATE_HOME = _xdg_dir("XDG_STATE_HOME", "$HOME/.local/state")
# Used for non-essential, user-specific data files such as sockets, named
# pipes, etc.
RUNTIME_DIR = _xdg_dir("XDG_RUNTIME_DIR", "/run/user/$UID")


# If none of these dirs exist when writing, attempt to create it with
# permission 0o700:
# CONFIG_HOME.mkdir(exist_ok=True, mode=0o700)
