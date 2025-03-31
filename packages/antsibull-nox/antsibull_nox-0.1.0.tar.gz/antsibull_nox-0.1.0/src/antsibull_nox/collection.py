# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project

"""
Handle Ansible collections.
"""

from __future__ import annotations

import functools
import json
import os
import typing as t
from collections.abc import Collection, Iterable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

from antsibull_fileutils.yaml import load_yaml_file, store_yaml_file

from .paths import copy_collection as _paths_copy_collection
from .paths import remove_path as _remove

# Function that runs a command (and fails on non-zero return code)
# and returns a tuple (stdout, stderr)
Runner = t.Callable[[list[str]], tuple[bytes, bytes]]


@dataclass
class CollectionData:  # pylint: disable=too-many-instance-attributes
    """
    An Ansible collection.
    """

    collections_root_path: Path | None
    path: Path
    namespace: str
    name: str
    full_name: str
    version: str | None
    dependencies: dict[str, str]
    current: bool

    @classmethod
    def create(
        cls,
        *,
        collections_root_path: Path | None = None,
        path: Path,
        full_name: str,
        version: str | None = None,
        dependencies: dict[str, str] | None = None,
        current: bool = False,
    ):
        """
        Create a CollectionData object.
        """
        namespace, name = full_name.split(".", 1)
        return CollectionData(
            collections_root_path=collections_root_path,
            path=path,
            namespace=namespace,
            name=name,
            full_name=full_name,
            version=version,
            dependencies=dependencies or {},
            current=current,
        )


def _load_galaxy_yml(galaxy_yml: Path) -> dict[str, t.Any]:
    try:
        data = load_yaml_file(galaxy_yml)
    except Exception as exc:
        raise ValueError(f"Cannot parse {galaxy_yml}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{galaxy_yml} is not a dictionary")
    return data


def _load_manifest_json_collection_info(manifest_json: Path) -> dict[str, t.Any]:
    try:
        with open(manifest_json, "br") as f:
            data = json.load(f)
    except Exception as exc:
        raise ValueError(f"Cannot parse {manifest_json}: {exc}") from exc
    ci = data.get("collection_info")
    if not isinstance(ci, dict):
        raise ValueError(f"{manifest_json} does not contain collection_info")
    return ci


def load_collection_data_from_disk(
    path: Path,
    *,
    namespace: str | None = None,
    name: str | None = None,
    root: Path | None = None,
    current: bool = False,
    accept_manifest: bool = True,
) -> CollectionData:
    """
    Load collection data from disk.
    """
    galaxy_yml = path / "galaxy.yml"
    manifest_json = path / "MANIFEST.json"
    found: Path
    if galaxy_yml.is_file():
        found = galaxy_yml
        data = _load_galaxy_yml(galaxy_yml)
    elif not accept_manifest:
        raise ValueError(f"Cannot find galaxy.yml in {path}")
    elif manifest_json.is_file():
        found = manifest_json
        data = _load_manifest_json_collection_info(manifest_json)
    else:
        raise ValueError(f"Cannot find galaxy.yml or MANIFEST.json in {path}")

    ns = data.get("namespace")
    if not isinstance(ns, str):
        raise ValueError(f"{found} does not contain a namespace")
    n = data.get("name")
    if not isinstance(n, str):
        raise ValueError(f"{found} does not contain a name")
    v = data.get("version")
    if not isinstance(v, str):
        v = None
    d = data.get("dependencies") or {}
    if not isinstance(d, dict):
        raise ValueError(f"{found}'s dependencies is not a mapping")

    if namespace is not None and ns != namespace:
        raise ValueError(
            f"{found} contains namespace {ns!r}, but was hoping for {namespace!r}"
        )
    if name is not None and n != name:
        raise ValueError(f"{found} contains name {n!r}, but was hoping for {name!r}")
    return CollectionData(
        collections_root_path=root,
        path=path,
        namespace=ns,
        name=n,
        full_name=f"{ns}.{n}",
        version=v,
        dependencies=d,
        current=current,
    )


def force_collection_version(path: Path, *, version: str) -> bool:
    """
    Make sure galaxy.yml contains this version.

    Returns ``True`` if the version was changed, and ``False`` if the version
    was already set to this value.
    """
    galaxy_yml = path / "galaxy.yml"
    try:
        data = load_yaml_file(galaxy_yml)
    except Exception as exc:
        raise ValueError(f"Cannot parse {galaxy_yml}: {exc}") from exc
    if data.get("version") == version:
        return False
    data["version"] = version
    store_yaml_file(galaxy_yml, data)
    return True


def _list_adjacent_collections_ansible_collections_tree(
    root: Path,
    *,
    directories_to_ignore: Collection[Path] | None = None,
) -> Iterator[CollectionData]:
    directories_to_ignore = directories_to_ignore or ()
    for namespace in root.iterdir():  # pylint: disable=too-many-nested-blocks
        try:
            if namespace.is_dir() or namespace.is_symlink():
                for name in namespace.iterdir():
                    if name in directories_to_ignore:
                        continue
                    try:
                        if name.is_dir() or name.is_symlink():
                            yield load_collection_data_from_disk(
                                name,
                                namespace=namespace.name,
                                name=name.name,
                                root=root,
                            )
                    except Exception:  # pylint: disable=broad-exception-caught
                        # If name doesn't happen to be a (symlink to a) directory, ...
                        pass
        except Exception:  # pylint: disable=broad-exception-caught
            # If namespace doesn't happen to be a (symlink to a) directory, ...
            pass


def _list_adjacent_collections_outside_tree(
    directory: Path,
    *,
    directories_to_ignore: Collection[Path] | None = None,
) -> Iterator[CollectionData]:
    directories_to_ignore = directories_to_ignore or ()
    for collection_dir in directory.iterdir():
        if collection_dir in directories_to_ignore:
            continue
        if not collection_dir.is_dir() and not collection_dir.is_symlink():
            continue
        parts = collection_dir.name.split(".")
        if len(parts) != 2:
            continue
        namespace, name = parts
        if not namespace.isidentifier() or not name.isidentifier():
            continue
        try:
            yield load_collection_data_from_disk(
                collection_dir,
                namespace=namespace,
                name=name,
            )
        except Exception:  # pylint: disable=broad-exception-caught
            # If collection_dir doesn't happen to be a (symlink to a) directory, ...
            pass


def _fs_list_local_collections() -> Iterator[CollectionData]:
    root: Path | None = None

    # Determine potential root
    cwd = Path.cwd()
    parents: Sequence[Path] = cwd.parents
    if len(parents) > 2 and parents[1].name == "ansible_collections":
        root = parents[1]

    # Current collection
    try:
        current = load_collection_data_from_disk(cwd, root=root, current=True)
        if root and current.namespace == parents[0].name and current.name == cwd.name:
            yield current
        else:
            root = None
            current = load_collection_data_from_disk(cwd, current=True)
            yield current
    except Exception as exc:
        raise ValueError(
            f"Cannot load current collection's info from {cwd}: {exc}"
        ) from exc

    # Search tree
    if root:
        yield from _list_adjacent_collections_ansible_collections_tree(
            root, directories_to_ignore=(cwd,)
        )
    elif len(parents) > 0:
        yield from _list_adjacent_collections_outside_tree(
            parents[0], directories_to_ignore=(cwd,)
        )


def _galaxy_list_collections(runner: Runner) -> Iterator[CollectionData]:
    try:
        stdout, _ = runner(["ansible-galaxy", "collection", "list", "--format", "json"])
        data = json.loads(stdout)
        for collections_root_path, collections in data.items():
            root = Path(collections_root_path)
            for collection in collections:
                namespace, name = collection.split(".", 1)
                try:
                    yield load_collection_data_from_disk(
                        root / namespace / name,
                        namespace=namespace,
                        name=name,
                        root=root,
                        current=False,
                    )
                except:  # noqa: E722, pylint: disable=bare-except
                    # Looks like Ansible passed crap on to us...
                    pass
    except Exception as exc:
        raise ValueError(f"Error while loading collection list: {exc}") from exc


@dataclass
class CollectionList:
    """
    A list of Ansible collections.
    """

    collections: list[CollectionData]
    collection_map: dict[str, CollectionData]
    current: CollectionData

    @classmethod
    def create(cls, collections_map: dict[str, CollectionData]):
        """
        Given a dictionary mapping collection names to collection data, creates a CollectionList.

        One of the collections must have the ``current`` flag set.
        """
        collections = sorted(collections_map.values(), key=lambda cli: cli.full_name)
        current = next(c for c in collections if c.current)
        return cls(
            collections=collections,
            collection_map=collections_map,
            current=current,
        )

    @classmethod
    def collect(cls, runner: Runner) -> CollectionList:
        """
        Search for a list of collections. The result is not cached.
        """
        found_collections = {}
        for collection_data in _fs_list_local_collections():
            found_collections[collection_data.full_name] = collection_data
        for collection_data in _galaxy_list_collections(runner):
            # Similar to Ansible, we use the first match
            if collection_data.full_name not in found_collections:
                found_collections[collection_data.full_name] = collection_data
        return cls.create(found_collections)

    def find(self, name: str) -> CollectionData | None:
        """
        Find a collection for a given name.
        """
        return self.collection_map.get(name)


@functools.cache
def get_collection_list(runner: Runner) -> CollectionList:
    """
    Search for a list of collections. The result is cached.
    """
    return CollectionList.collect(runner)


def _add_all_dependencies(
    collections: dict[str, CollectionData], all_collections: CollectionList
) -> None:
    to_process = list(collections.values())
    while to_process:
        collection = to_process.pop(0)
        for dependency_name in collection.dependencies:
            if dependency_name not in collections:
                dependency_data = all_collections.find(dependency_name)
                if dependency_data is None:
                    raise ValueError(
                        f"Cannot find collection {dependency_name},"
                        f" a dependency of {collection.full_name}!"
                    )
                collections[dependency_name] = dependency_data
                to_process.append(dependency_data)


def _install_collection(collection: CollectionData, path: Path) -> None:
    if path.is_symlink():
        if path.readlink() == collection.path:
            return
        path.unlink()
    else:
        _remove(path)
    path.symlink_to(collection.path)


def _install_current_collection(collection: CollectionData, path: Path) -> None:
    if path.exists() and (path.is_symlink() or not path.is_dir()):
        path.unlink()
    path.mkdir(exist_ok=True)
    present = {p.name for p in path.iterdir()}
    for source_entry in collection.path.iterdir():
        if source_entry.name == ".nox":
            continue
        dest_entry = path / source_entry.name
        if source_entry.name in present:
            present.remove(source_entry.name)
            if dest_entry.is_symlink() and dest_entry.readlink() == source_entry:
                continue
            _remove(dest_entry)
        dest_entry.symlink_to(source_entry)
    for name in present:
        dest_entry = path / name
        _remove(dest_entry)


def _install_collections(
    collections: Iterable[CollectionData], root: Path, *, with_current: bool
) -> None:
    for collection in collections:
        namespace_dir = root / collection.namespace
        namespace_dir.mkdir(exist_ok=True)
        path = namespace_dir / collection.name
        if not collection.current:
            _install_collection(collection, path)
        elif with_current:
            _install_current_collection(collection, path)


def _extract_collections_from_extra_deps_file(path: str | os.PathLike) -> list[str]:
    if not os.path.exists(path):
        return []
    try:
        data = load_yaml_file(path)
        result = []
        if data.get("collections"):
            for index, collection in enumerate(data["collections"]):
                if isinstance(collection, str):
                    result.append(collection)
                    continue
                if not isinstance(collection, dict):
                    raise ValueError(
                        f"Collection entry #{index + 1} must be a string or dictionary"
                    )
                if not isinstance(collection.get("name"), str):
                    raise ValueError(
                        f"Collection entry #{index + 1} does not have a 'name' field of type string"
                    )
                result.append(collection["name"])
        return result
    except Exception as exc:
        raise ValueError(
            f"Error while loading collection dependency file {path}: {exc}"
        ) from exc


@dataclass
class SetupResult:
    """
    Information on how the collections are set up.
    """

    # The path of the ansible_collections directory.
    root: Path

    # Data on the current collection (as in the repository).
    current_collection: CollectionData

    # If it was installed, the path of the current collection inside the collection tree below root.
    current_path: Path | None


def setup_collections(
    destination: str | os.PathLike,
    runner: Runner,
    *,
    extra_collections: list[str] | None = None,
    extra_deps_files: list[str | os.PathLike] | None = None,
    with_current: bool = True,
) -> SetupResult:
    """
    Setup all collections in a tree structure inside the destination directory.
    """
    all_collections = get_collection_list(runner)
    destination_root = Path(destination) / "ansible_collections"
    destination_root.mkdir(exist_ok=True)
    current = all_collections.current
    collections_to_install = {current.full_name: current}
    if extra_collections:
        for collection in extra_collections:
            collection_data = all_collections.find(collection)
            if collection_data is None:
                raise ValueError(
                    f"Cannot find collection {collection} required by the noxfile!"
                )
            collections_to_install[collection_data.full_name] = collection_data
    if extra_deps_files is not None:
        for extra_deps_file in extra_deps_files:
            for collection in _extract_collections_from_extra_deps_file(
                extra_deps_file
            ):
                collection_data = all_collections.find(collection)
                if collection_data is None:
                    raise ValueError(
                        f"Cannot find collection {collection} required in {extra_deps_file}!"
                    )
                collections_to_install[collection_data.full_name] = collection_data
    _add_all_dependencies(collections_to_install, all_collections)
    _install_collections(
        collections_to_install.values(), destination_root, with_current=with_current
    )
    return SetupResult(
        root=destination_root,
        current_collection=current,
        current_path=(
            (destination_root / current.namespace / current.name)
            if with_current
            else None
        ),
    )


def _copy_collection(collection: CollectionData, path: Path) -> None:
    _paths_copy_collection(collection.path, path)


def _copy_collection_rsync_hard_links(
    collection: CollectionData, path: Path, runner: Runner
) -> None:
    _, __ = runner(
        [
            "rsync",
            "-av",
            "--delete",
            "--exclude",
            ".nox",
            "--link-dest",
            str(collection.path) + "/",
            "--",
            str(collection.path) + "/",
            str(path) + "/",
        ]
    )


def setup_current_tree(
    place: str | os.PathLike, current_collection: CollectionData
) -> SetupResult:
    """
    Setup a tree structure with the current collection in it.
    """

    path = Path(place)
    root = path / "ansible_collections"
    root.mkdir(exist_ok=True)
    namespace = root / current_collection.namespace
    namespace.mkdir(exist_ok=True)
    collection = namespace / current_collection.name
    _copy_collection(current_collection, collection)
    # _copy_collection_rsync_hard_links(current_collection, collection, runner)
    return SetupResult(
        root=root,
        current_collection=current_collection,
        current_path=collection,
    )


__all__ = [
    "CollectionData",
    "CollectionList",
    "SetupResult",
    "get_collection_list",
    "load_collection_data_from_disk",
    "setup_collections",
    "setup_current_tree",
]
