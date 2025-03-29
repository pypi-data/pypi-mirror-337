from dataclasses import dataclass

from hipercow.dide.auth import check as check_auth
from hipercow.dide.mounts import Mount, PathMap, remap_path
from hipercow.root import Root
from hipercow.util import check_python_version


@dataclass
class DideConfiguration:
    path_map: PathMap
    python_version: str

    def __init__(
        self,
        root: Root,
        *,
        mounts: list[Mount],
        python_version: str | None = None,
        check_credentials: bool = True,
    ):
        if check_credentials:
            check_auth()
        self.path_map = remap_path(root.path, mounts)
        self.python_version = check_python_version(python_version)
