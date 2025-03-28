**The package is of alpha currently...**

noopy.folio is a library that works on financial portfolios including assessment, optimization and etc.

noopy.folio is a subpackage that can be installed alone under the root package name "noopy"


# Install

## As a user
install via pip:
```
pip install noopy-folio
```

## As a developer 
to set for coding the package
* git clone the repo to you local machine
* set variable: `PYTHONPATH=<repo-root-folder>/src/`

to run unit tests:
* `cd <repo-root-folder>`
* `python -m unittest discover -s src/noopy -v`

to build locally
* install the package `pip install build`, if it's not present yet
* `cd <repo-root-folder>`
* `python -m build`


# Usage

Start with ```from noopy.folio as noofolio```

Use High-level API in ```noofolio.analyse```, e.g.:
```
pc.analyse.asset_recommendations(...)
```

More flexible usage can be directed to sub-modules, e.g.:
```
pc.marketdata.get_md_observable(...)
```

# Design
Design principles:
- open minded
- model driven

## APIs
- noofolio.screen(data)
- noofolio.select(candidates)
- noofolio.optimise(portfolio)
- noofolio.monitor(portfolio)

## Flow

monitor (warning?)
  - yes: try in order
    - attempt re-optimise
    - attempt re-select
    - attempt re-screen

optimise (meet risk aversion?)
  - yes: try in order
    - attempt re-select
    - attempt re-screen

select (rating high enough?)
  - yes: try in order
    - attempt re-screen

