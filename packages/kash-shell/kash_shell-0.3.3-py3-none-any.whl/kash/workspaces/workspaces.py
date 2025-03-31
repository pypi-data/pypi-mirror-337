from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, TypeAlias, TypeVar

from prettyfmt import fmt_path

from kash.config.api_keys import print_api_key_setup
from kash.config.logger import get_logger, reset_log_root
from kash.config.settings import (
    GLOBAL_WS_NAME,
    get_global_ws_dir,
    global_settings,
    resolve_and_create_dirs,
)
from kash.errors import FileNotFound, InvalidInput, InvalidState
from kash.file_storage.metadata_dirs import MetadataDirs
from kash.model.params_model import GLOBAL_PARAMS, RawParamValues
from kash.utils.common.format_utils import fmt_loc
from kash.utils.file_utils.ignore_files import IgnoreFilter, is_ignored_default
from kash.workspaces.workspace_names import check_strict_workspace_name, to_ws_name
from kash.workspaces.workspace_registry import WorkspaceInfo, get_ws_registry

if TYPE_CHECKING:
    from kash.file_storage.file_store import FileStore

log = get_logger(__name__)


# Currently the same thing as a FileStore, but may want to change
# this in the future.
Workspace: TypeAlias = "FileStore"


def is_ws_dir(path: Path) -> bool:
    dirs = MetadataDirs(path, False)
    return dirs.is_initialized()


def enclosing_ws_dir(path: Path = Path(".")) -> Path | None:
    """
    Get the workspace directory enclosing the given path (itself or a parent or None).
    """
    path = path.absolute()
    while path != Path("/"):
        if is_ws_dir(path):
            return path
        path = path.parent

    return None


def resolve_ws(name: str | Path) -> WorkspaceInfo:
    """
    Parse and resolve the given workspace path or name and return a tuple containing
    the workspace name and a resolved directory path.

    "example" -> "example", Path("example")  [if example already exists]
    "/path/to/example" -> "example", Path("/path/to/example")
    "." -> "current_dir", Path("/path/to/current_dir") [if cwd is /path/to/current_dir]
    """
    if not name:
        raise InvalidInput("Workspace name is required.")

    name = str(name).strip().rstrip("/")

    # Check if name is a full path. Otherwise, we'll resolve it relative to the
    # current directory.
    if "/" in name or name.startswith("."):
        resolved = Path(name).resolve()
        parent_dir = resolved.parent
        name = resolved.name
    else:
        parent_dir = Path(".").resolve()

    if (parent_dir / name).exists():
        ws_name = to_ws_name(name)
        ws_path = parent_dir / name
    else:
        ws_name = to_ws_name(name)
        ws_path = parent_dir / ws_name

    is_global_ws = ws_name.lower() == GLOBAL_WS_NAME.lower()

    return WorkspaceInfo(ws_name, ws_path, is_global_ws)


def get_ws(name_or_path: str | Path, auto_init: bool = True) -> Workspace:
    """
    Get a workspace by name or path. Adds to the in-memory registry so we reuse it.
    With `auto_init` true, will initialize the workspace if it is not already initialized.
    """
    path = Path(name_or_path)
    name = path.name
    name = check_strict_workspace_name(name)
    info = resolve_ws(path)
    if not is_ws_dir(info.base_dir) and not auto_init:
        raise FileNotFound(f"Not a workspace directory: {fmt_path(info.base_dir)}")

    ws = get_ws_registry().load(info.name, info.base_dir, info.is_global_ws)
    return ws


@cache
def global_ws_dir() -> Path:
    kb_path = resolve_and_create_dirs(get_global_ws_dir(), is_dir=True)
    log.info("Global workspace path: %s", kb_path)
    return kb_path


def get_global_ws() -> Workspace:
    """
    Get the global_ws workspace.
    """
    return get_ws_registry().load(GLOBAL_WS_NAME, global_ws_dir(), True)


def _infer_ws_info() -> tuple[Path | None, bool]:
    dir = enclosing_ws_dir()
    is_global_ws = not dir
    if is_global_ws:
        dir = global_ws_dir()
    return dir, is_global_ws


def _switch_current_workspace(base_dir: Path) -> Workspace:
    """
    Switch the current workspace to the given directory.
    Updates logging and cache directories to be within that workspace.
    Does not reload the workspace if it's already loaded and does not
    use the global_ws for logs (since it's )
    """
    from kash.media_base.media_tools import reset_media_cache_dir
    from kash.web_content.file_cache_utils import reset_content_cache_dir

    info = resolve_ws(base_dir)
    ws_dirs = MetadataDirs(info.base_dir, info.is_global_ws)

    # Use the global log root for the global_ws, and the workspace log root otherwise.
    reset_log_root(None, info.name if not info.is_global_ws else None)

    if info.is_global_ws:
        # If not in a workspace, use the global cache locations.
        reset_media_cache_dir(global_settings().media_cache_dir)
        reset_content_cache_dir(global_settings().content_cache_dir)
    else:
        reset_media_cache_dir(ws_dirs.media_cache_dir)
        reset_content_cache_dir(ws_dirs.content_cache_dir)

    return get_ws_registry().load(info.name, info.base_dir, info.is_global_ws)


def current_ws(silent: bool = False) -> Workspace:
    """
    Get the current workspace based on the current working directory.
    Also updates logging and cache directories if this has changed.
    """

    base_dir, _is_global_ws = _infer_ws_info()
    if not base_dir:
        raise InvalidState(
            f"No workspace found in {fmt_loc(Path('.').absolute())}.\n"
            "Create one with the `workspace` command."
        )

    ws = _switch_current_workspace(base_dir)

    if not silent:
        # Delayed, once-only logging of any setup warnings.
        print_api_key_setup(once=True)
        ws.log_store_info(once=True)

    return ws


def current_ignore() -> IgnoreFilter:
    """
    Get the current ignore filter.
    """
    try:
        return current_ws().is_ignored
    except InvalidState:
        return is_ignored_default


T = TypeVar("T")


def ws_param_value(param_name: str, type: type[T] = str) -> T | None:
    """
    Get a global parameter value, checking if it is set in the current workspace first.
    """
    try:
        params = current_ws().params.get_raw_values()
    except InvalidState:
        params = RawParamValues()

    return params.get_parsed_value(param_name, type=type, param_info=GLOBAL_PARAMS)
