"""Smoke + self-conformance tests for the plugin contract.

These exercise the package the way a plugin author does: build the seam objects,
implement a decorator against the view payloads, and confirm a `create_plugin()`
factory typechecks as `IWinterPlugin`. The fakes below stand in for winter-cli's
concrete models — they satisfy the view Protocols structurally, the same way the
real models do.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from winter_plugin_api import (
    ActionScope,
    DetailPanelContext,
    IEnvironmentStatusView,
    IWinterPlugin,
    PluginRegistration,
    TuiAction,
)


@dataclasses.dataclass
class _FakeWorkspace:
    root_path: Path = Path("/ws")
    session_prefix: str = "mp"
    main_branch: str = "master"


@dataclasses.dataclass
class _FakeEnvironment:
    name: str = "alpha"
    index: int = 1
    path: Path = Path("/ws/alpha")
    workspace: _FakeWorkspace = dataclasses.field(default_factory=_FakeWorkspace)


@dataclasses.dataclass
class _FakeEnvStatus:
    environment: _FakeEnvironment = dataclasses.field(default_factory=_FakeEnvironment)
    extensions: dict[str, str] = dataclasses.field(default_factory=dict)


def _badge(env_status: IEnvironmentStatusView, env_path: Path) -> None:
    env_status.extensions["t"] = f"{env_status.environment.name}@{env_path.name}"


def test_decorator_reads_views_and_writes_extensions() -> None:
    status = _FakeEnvStatus()
    _badge(status, Path("/ws/alpha"))
    assert status.extensions["t"] == "alpha@alpha"


def test_fake_status_satisfies_view_protocol() -> None:
    # Structural conformance: the fake stands in for FeatureEnvironmentStatus.
    status: IEnvironmentStatusView = _FakeEnvStatus()
    assert status.environment.workspace.session_prefix == "mp"


def test_tui_action_normalizes_scope_to_frozenset() -> None:
    action = TuiAction(
        name="demo",
        scope=ActionScope.feature_worktree,
        key="d",
        description="Demo",
        handler=lambda inv: None,
    )
    assert action.scopes == frozenset({ActionScope.feature_worktree})


def test_detail_panel_context_holds_one_focus() -> None:
    ctx = DetailPanelContext()
    assert ctx.worktree is None and ctx.repo is None


class _DemoPlugin:
    name = "demo"

    def register(self, config: object) -> PluginRegistration:
        return PluginRegistration(environment_decorators=[_badge])


def create_plugin() -> IWinterPlugin:
    return _DemoPlugin()


def test_create_plugin_conforms_to_iwinterplugin() -> None:
    plugin = create_plugin()
    registration = plugin.register({})
    assert registration.environment_decorators == [_badge]
