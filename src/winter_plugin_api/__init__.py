"""Public, semver-versioned contract for winter TUI plugins.

A plugin imports its **entire** contribution surface from this package and
typechecks `create_plugin() -> IWinterPlugin` in its own repo, with no
dependency on winter-cli. Two layers:

- **Views** (`views`) — narrow, read-only Protocols over winter-cli's domain and
  status models. A decorator/panel receives one of these, never a concrete
  model, so the package stands alone.
- **Seam** (`seam`) — the dataclasses, enums, and Protocols a plugin constructs
  or implements: `PluginRegistration`, `TuiAction`, `ActionScope`, the action
  contexts, the decorator / panel / plugin Protocols.

winter-cli keeps its own runtime copy of the seam, kept in sync with this package
by hand; this package is the versioned source of truth plugin authors code
against. See the README for the versioning policy.
"""

from __future__ import annotations

from winter_plugin_api.seam import (
    ActionContext,
    ActionHandler,
    ActionInvocation,
    ActionScope,
    DetailPanelContext,
    FeatureEnvironmentContext,
    FeatureWorktreeContext,
    IDetailPanel,
    IEnvironmentDecorator,
    IWinterPlugin,
    IWorktreeRepoDecorator,
    PluginRegistration,
    StandaloneRepoContext,
    SuspendFn,
    TuiAction,
    WorkspaceContext,
)
from winter_plugin_api.views import (
    IEnvironmentStatusView,
    IEnvironmentView,
    IEnvironmentWorktreesView,
    IFeatureWorktreeView,
    IProjectRepositoryView,
    IStandaloneRepositoryView,
    IWorkspaceView,
    IWorktreeRepoStatusView,
)

__version__ = "0.1.0"

__all__ = [
    "ActionContext",
    "ActionHandler",
    "ActionInvocation",
    "ActionScope",
    "DetailPanelContext",
    "FeatureEnvironmentContext",
    "FeatureWorktreeContext",
    "IDetailPanel",
    "IEnvironmentDecorator",
    "IEnvironmentStatusView",
    "IEnvironmentView",
    "IEnvironmentWorktreesView",
    "IFeatureWorktreeView",
    "IProjectRepositoryView",
    "IStandaloneRepositoryView",
    "IWinterPlugin",
    "IWorkspaceView",
    "IWorktreeRepoDecorator",
    "IWorktreeRepoStatusView",
    "PluginRegistration",
    "StandaloneRepoContext",
    "SuspendFn",
    "TuiAction",
    "WorkspaceContext",
    "__version__",
]
