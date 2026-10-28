# winter-plugin-api

The narrow, separately-versioned **typed contract for winter TUI plugins**. A
plugin depends on this package (via a pinned git URL), imports its entire
contribution surface from `winter_plugin_api`, and typechecks
`create_plugin() -> IWinterPlugin` in its own repo — with **zero dependency on
winter-cli**.

## Why it exists

winter loads a plugin's `plugin.py` into its own process, so at runtime
`from winter_plugin_api import ...` resolves against whatever winter ships. But a
plugin's *own* repo doesn't depend on winter-cli, so without this package its
author gets no types, no autocomplete, and no checking — and the in-tree contract
deliberately typed its decorator payloads as bare `object`. This package gives
authors a resolvable, **narrow, read-only** contract, and decouples the *seam*
from winter-cli's *domain model* so the model can evolve freely while only the
seam carries a version.

## What's in it

- **Views** (`winter_plugin_api.views`) — narrow read-only Protocols over
  winter-cli's domain/status models (`IEnvironmentStatusView`,
  `IWorktreeRepoStatusView`, `IFeatureWorktreeView`, `IStandaloneRepositoryView`,
  `IEnvironmentView`, `IWorkspaceView`, …). A decorator/panel receives one of
  these, never a concrete model.
- **Seam** (`winter_plugin_api.seam`) — everything a plugin constructs or
  implements: `PluginRegistration`, `TuiAction`, `ActionScope`, the action
  contexts + `ActionInvocation`, and the `IWinterPlugin` / `IDetailPanel` /
  `IWorktreeRepoDecorator` / `IEnvironmentDecorator` Protocols + `DetailPanelContext`.

Everything is re-exported from the top-level `winter_plugin_api` package; import
from there.

## Consuming it (plugin authors)

Add it as a **dev dependency** pinned to a tag, then import the contract:

```toml
# pyproject.toml
[dependency-groups]
dev = [
    "winter-plugin-api @ git+https://github.com/paul-gross/winter-plugin-api@v0.1.0",
]
```

```python
from winter_plugin_api import IWinterPlugin, PluginRegistration, IEnvironmentStatusView


def create_plugin() -> IWinterPlugin:
    return MyPlugin()
```

It is a dev/test dependency, not a runtime one: winter supplies the contract at
runtime when it loads your `plugin.py`. You pin it only so your own typechecker
resolves the imports.

## Relationship to winter-cli

This package is a **deliberate, hand-curated copy** of winter-cli's seam — not a
re-export of it. Keeping it separate is the whole point: it lets the seam be
versioned (semver) independently of winter-cli's **unversioned** domain model, so
a plugin pins this package and never winter-cli itself.

The mechanics of that decoupling — how winter-cli's own runtime copy of the seam
(`winter_cli/plugins/types.py`, imported by its loader) is kept in sync with this
package by hand, and the conformance checks that might one day wire the two
together — are part of winter's plugin-authoring process, not this package's
contract. See winter's **plugin-author conventions** for that side.

## Versioning policy

The package follows **semver**, and the version a plugin pins is a contract:

- **Major bump (`1.x` → `2.0`)** — a breaking change to the contract: a removed
  or renamed public name, a narrowed view (a property a plugin could read is
  gone), a changed `__call__` / `register` signature, or a removed dataclass
  field. Plugins must be updated before moving to the new major.
- **Minor bump (`0.1` → `0.2`, `1.1` → `1.2`)** — a backward-compatible
  addition: a new view property, a new optional `PluginRegistration` field, a new
  decorator/panel Protocol, a new `ActionScope` member. Existing plugins keep
  working unchanged.
- **Patch bump** — docs, typing-only fixes, no surface change.

Pre-1.0 (`0.x`) the surface is still settling: treat a **minor** `0.x` bump as
potentially breaking. A plugin should pin the **lowest** api version exposing
every name it uses, so it stays loadable against the widest range of winter
builds. (winter-cli does not depend on the package today; should it later pin a
version to conform against, it would bump that pin in the same change that adapts
it to a new api release.)

## Development

```bash
uv sync              # install
uv run pyright       # typecheck
uv run pytest        # test
uv run ruff check .  # lint
```

## License

Source-available under the Functional Source License 1.1 (FSL-1.1-ALv2). Each release converts to Apache License 2.0 two years after it ships. See LICENSE.
