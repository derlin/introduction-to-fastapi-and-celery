# Poetry

Before getting started, we need a Python project.

[poetry](https://python-poetry.org) is the trendy package manager
which superseded setuptools and pyenv in the heart of pythonistas.

## Installation

If you haven't done so, install poetry: [https://python-poetry.org/docs/#installation](
https://python-poetry.org/docs/#installation).
On a Mac:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

I currently use:
```bash
poetry --version
Poetry (version 1.3.0)
```

The installation will create a new virtualenv especially for poetry somewhere in your system.
On a Mac, use `cat $(which poetry)` and look at the first line. In my case:

* `poetry` executable installed in `~/.local/bin/poetry`
* poetry's virtualenv installed in `~/Library/Application Support/pypoetry/venv/`

## Initializing a project

Once poetry is installed, initializing a new project is as easy as running:
```bash
mkdir fastapi-celery && cd fastapi-celery
poetry init
```

Follow the prompts. You can already start adding dependencies (`fastapi`, `celery`)
and dev-dependencies (`bandit`, `black`) or choose to do that later.

Once you finished with the prompt, have a look at what was generated:
```bash
cat pyproject.toml
```

## Adding dependencies

You can add a dependency at any time using: `poetry add <package-name>`.
If the dependency is for development only, use the `--group dev` flag (or any other group name).

You can also edit the `pyproject.toml` directly and run `poetry install`.

I use `poetry add` with a name (no version) and then update the `pyprojet.toml`
manually to pin only the minor version (instead of the full version).
This means replacing e.g. `fastapi = "^0.93.0"` with `fastapi = "^0.93"` (notice the `.0` is missing).
This way, I can still beneficiate from patch updates by running `poetry update` at any time.
I also often use '*' for dev dependencies.

See [Dependency specification](https://python-poetry.org/docs/dependency-specification/) for more information.

## Creating a virtualenv

This only set up the project. Now, we need to create a virtualenv and install those dependencies.
Poetry can do this for us using:
```bash
poetry install
```

Poetry will automatically create a virtualenv, located in a central place on your system.
I will be blunt: I :face_vomiting: this; I like to have virtualenvs at the root of each project instead.
This ensures all is cleaned up if I delete a project and I can always use `source .venv/bin/activate`
from any repo to have my virtualenv selected.

To change poetry's default behavior to something more suited to my tastes,
create a `poetry.toml` at the root of the project with the following:
```toml
[virtualenvs]
in-project = true
path = ".venv"
```

!!! warning

    If you already ran the install, remove the old virtualenv first (`poetry env list` + `poetry env remove <name>`),
    and run `poetry install` again.

## And more

Other nice things about poetry:

* `poetry show --latest` will show the current and latest available versions of your dependencies
* `poetry env` allows you to manage environments: remove, list, info, etc.
* running `poetry install --sync` ensures that the locked dependencies in the `poetry.lock` are the only ones
  present in the environment, removing anything that’s not necessary.
* you can choose to install only certain groups (in addition to main) using `poetry install --with dev`, 
  or only a specific group using `poetry install --only main`.
* running `poetry update` will fetch the latest matching versions (according to the `pyproject.toml` file) and update
  the lock file with the new versions. This is equivalent to deleting the `poetry.lock` file and running `install` again.
* you can build the project using `poetry build`, and publish it to PyPI using `poetry publish` (given you have [set up
  you credentials](https://python-poetry.org/docs/repositories/#configuring-credentials) properly)

The documentation is amazing, so I will stop here.

## BONUS

### formatting with black

[black](https://github.com/psf/black) is a strict formatter. From their docs:

> Black is the uncompromising Python code formatter.
> By using it, you agree to cede control over minutiae of hand-formatting.
> In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting.
> You will save time and mental energy for more important matters.

To install it:
```bash
poetry add black='*' --group dev
```

Now, all you have to do is run:
```bash
poetry run black fastapi_celery
```

Note that you can also configure VSCode to use black by default.

The default line length is 88. If for some reason you want to change this, you can use:
```bash
poetry run black --line-length 100 --experimental-string-processing fastapi_celery
```

The `--experimental-string-processing` is still under development. Without it, black won't
split long strings...

To only perform checks (without formatting anyhting, e.g. in CI), use:
```bash
poetry run black --check fastapi_celery
```

### linting with ruff

I just discovered [ruff](https://beta.ruff.rs/docs/), which is just awesome!

It basically replaces all the other tools (except formatting, but it is coming soon) such as:

* `isort` - sorts imports
* `bandit` - finds common security issues
* `flake8` - linter
* etc.

Ruff is implemented in Rust and is really (really!) fast. The configuration can be done from the
`pyproject.toml` directly, but the defaults are already quite nice.


[Full list of available rules here](https://beta.ruff.rs/docs/rules/){ .md-button }

Get started by installing it:
```bash
poetry add ruff='*' --group dev
```

Now, run it using:
```bash
# Check only
poetry run ruff fastapi_celery
# Automatically fix what can be fixed
poetry run ruff --fix fastapi_celery
```

I played a bit with the options, and currently decided to use:

```toml
# in pyproject.toml

[tool.ruff]
select = [
    "E",   # pycodestyle error
    "W",   # pycodestyle warning
    "F",   # pyflakes
    "A",   # flakes8-builtins
    "COM", # flakes8-commas
    "C4",  # flake8-comprehensions
    "Q",   # flake8-quotes
    "SIM", # flake8-simplify
    "PTH", # flake8-use-pathlib
    "I",   # isort
    "N",   # pep8 naming
    "UP",  # pyupgrade  
    "S",   # bandit
]
```

Have a look at the docs, it is really good!
