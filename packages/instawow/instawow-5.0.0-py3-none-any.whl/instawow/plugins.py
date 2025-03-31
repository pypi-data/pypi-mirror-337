from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache
from typing import Protocol

import click
import pluggy

from . import NAME, resolvers

_entry_point = f'{NAME}.plugins'

hookspec = pluggy.HookspecMarker(NAME)
hookimpl = pluggy.HookimplMarker(NAME)


class InstawowPlugin(Protocol):  # pragma: no cover
    "The plug-in interface."

    @hookspec
    def instawow_add_commands(self) -> Iterable[click.Command]:
        "Additional commands to register with ``click``."
        ...

    @hookspec
    def instawow_add_resolvers(self) -> Iterable[type[resolvers.Resolver]]:
        "Additional resolvers to load."
        ...


@lru_cache(1)
def _load_plugins():
    plugin_manager = pluggy.PluginManager(NAME)
    plugin_manager.add_hookspecs(InstawowPlugin)
    plugin_manager.load_setuptools_entrypoints(_entry_point)
    return plugin_manager.hook


def get_plugin_commands() -> Iterable[Iterable[click.Command]]:
    plugin_hook = _load_plugins()
    return plugin_hook.instawow_add_commands()


def get_plugin_resolvers() -> Iterable[Iterable[type[resolvers.Resolver]]]:
    plugin_hook = _load_plugins()
    return plugin_hook.instawow_add_resolvers()
