"""Narrow, read-only **view Protocols** over winter-cli's domain and status models.

A winter TUI plugin never receives winter-cli's concrete model objects as a
type — it receives one of these views, which expose *only* the attributes a
plugin may read. The views are deliberately narrow: a plugin that types its
decorator against `IEnvironmentStatusView` can read `env_status.environment.name`
and write `env_status.extensions[...]`, and nothing else is on the contract.

Because every member here is a plain attribute or a read-only property of a
primitive / another view, the package has **zero dependency on winter-cli**. The
real objects winter-cli passes (`FeatureEnvironmentStatus`, `WorktreeRepoStatus`,
`FeatureWorktree`, `StandaloneRepository`, …) structurally satisfy these
Protocols; winter-cli pins that with conformance sentinels so a model rename that
breaks the seam fails *its* typecheck (see the package README, "Drift").
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol


class IWorkspaceView(Protocol):
    """The workspace a plugin can read — name band and identity only."""

    @property
    def root_path(self) -> Path: ...

    @property
    def session_prefix(self) -> str: ...

    @property
    def main_branch(self) -> str: ...


class IProjectRepositoryView(Protocol):
    """A project repository a worktree belongs to."""

    @property
    def name(self) -> str: ...


class IStandaloneRepositoryView(Protocol):
    """A standalone repository (singleton or user-declared)."""

    @property
    def name(self) -> str: ...

    @property
    def path(self) -> Path: ...


class IEnvironmentView(Protocol):
    """A feature environment (alpha, beta, …)."""

    @property
    def name(self) -> str: ...

    @property
    def index(self) -> int: ...

    @property
    def path(self) -> Path: ...

    @property
    def workspace(self) -> IWorkspaceView: ...


class IFeatureWorktreeView(Protocol):
    """One repo worktree within a feature environment."""

    @property
    def path(self) -> Path: ...

    @property
    def repository(self) -> IProjectRepositoryView: ...

    @property
    def environment(self) -> IEnvironmentView: ...

    @property
    def workspace(self) -> IWorkspaceView: ...


class IEnvironmentWorktreesView(Protocol):
    """All worktrees in an environment — the env handle plus its worktree list."""

    @property
    def environment(self) -> IEnvironmentView: ...

    @property
    def worktrees(self) -> Sequence[IFeatureWorktreeView]: ...


class IEnvironmentStatusView(Protocol):
    """The payload an `IEnvironmentDecorator` receives.

    Read `environment` to decide what to render; write a short badge string into
    `extensions[<your-key>]` to surface it in the env's column header. Renderers
    append every `extensions` value to the cell verbatim, joined by spaces.
    """

    @property
    def environment(self) -> IEnvironmentView: ...

    extensions: dict[str, str]


class IWorktreeRepoStatusView(Protocol):
    """The payload an `IWorktreeRepoDecorator` receives.

    Read the git-status fields to decide what to render; write a badge into
    `extensions[<your-key>]` to surface it in the repo's status row.
    """

    @property
    def worktree(self) -> IFeatureWorktreeView: ...

    @property
    def branch(self) -> str | None: ...

    @property
    def ahead(self) -> int: ...

    @property
    def behind(self) -> int: ...

    @property
    def dirty_count(self) -> int: ...

    extensions: dict[str, object]
