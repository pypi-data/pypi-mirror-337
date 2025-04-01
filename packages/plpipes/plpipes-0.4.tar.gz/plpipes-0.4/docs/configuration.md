# Configuration

The configuration module is one of the core components of PLPipes
pervasively used by `plpipes` itself, so even if you don't want to use
it directly in your project it would be used internally by the
framework.

Configuration data is structured in a global tree-like object which is
initialized from data read from several files in sequence and from the
command line.

Both YAML and JSON files are supported (though, we recommended YAML
usage as it is usually easier to read by humans).

When the same setting appears in several configuration files, the last
one read is the one that prevails.

## File structure

The list of files from with the configuration is read is dynamically
calculated based on two settings:

* The script "stem": It is the name of the script run without the
    extension (for instance, the stem for `run.py` is `run`).

    When `plpipes` is used from a Jupyter notebook, the stem can be
    passed on the `%plpipes` line magic:

    ```python
    %plpipes foobalizer
    ```

- The deployment environment (`dev`, `pre`, `pro`, etc.): this can be
    set from the command line or using the environment variable
    `PLPIPES_ENV` (see [Environment variables](#Environment-variables)
    below). It defaults to `dev`.

Also, there are two main directories where configuration files are
stored:

- `default`: This directory should contain configuration files that
    are considered defaults and that are not going to be changed by the
    project users. We think of it as the place where to place setting
    that otherwise would be hard-coded.

- `config`: This directory contains configuration files which are
    editable by the project users or where developers can put temporary
    settings they don't want to push into git.

*We are currently considering whether this division makes sense or if
we should otherwise replace it by something better*

When PLPipes configuration module is initialized it looks in those two
directories for files whose names follow the following rules:

1. Base name: the base name is taken as `common` or the stem so that,
    for instance, when loading the configuration from `run.py`, both
    `common.yaml` and `run.yaml` files would be taken into account.

2. Secrets: files with a `-secrets` post-fix are also loaded (for
    instance, `common-secrets.yaml` and `run-secrets.yaml`).

2. Environment: files with the deployment environment attached as a
    post-fix are also loaded (`run-dev.yaml` or `run-secrets-dev.yaml`).

Additionally two user-specific configuration files are
considered. Those are expected to contain global configuration
settings which are not project specific as API keys, common database
definitions, etc.

```
~/.config/plpipes/plpipes.yaml
~/.config/plpipes/plpipes-secrets.yaml
```

Finally, when using the default runner (See [Runner](#Runner) below),
the user can request additional configuration files to be loaded.

In summary, the full set of files which are consider for instance,
when the `run.py` script is invoked in the `dev` environment is as
follows (and in this particular order):

```
~/.config/plpipes/plpipes.json
~/.config/plpipes/plpipes.yaml
~/.config/plpipes/plpipes-secrets.json
~/.config/plpipes/plpipes-secrets.yaml
default/common.json
default/common.yaml
default/common-dev.json
default/common-dev.yaml
default/common-secrets.json
default/common-secrets.yaml
default/common-secrets-dev.json
default/common-secrets-dev.yaml
default/run.json
default/run.yaml
default/run-dev.json
default/run-dev.yaml
default/run-secrets.json
default/run-secrets.yaml
default/run-secrets-dev.json
default/run-secrets-dev.yaml
config/common.json
config/common.yaml
config/common-dev.json
config/common-dev.yaml
config/common-secrets.json
config/common-secrets.yaml
config/common-secrets-dev.json
config/common-secrets-dev.yaml
config/run.json
config/run.yaml
config/run-dev.json
config/run-dev.yaml
config/run-secrets.json
config/run-secrets.yaml
config/run-secrets-dev.json
config/run-secrets-dev.yaml
```

## Automatic configuration

There are some special settings that are automatically set by the
framework when the configuration is initialized:

- `fs`: The file system sub-tree, contains entries for the main project
    subdirectories (`root` which points to the project root directory,
    `bin`, `lib`, `config`, `default`, `input`, `work`, `output` and
    `actions`).

- `env`: The deployment environment

- `logging.level`: The logging level.

All those entries can be overridden in the configuration files.

## Wildcards

In order to simplify the declaration of similar configuration
subtrees, a wildcard mechanism is provided.

Entries named `*` (an asterisk) are copied automatically into sibling
configurations.

For instance, in the following configuration most of the database
connection parameters for `input` and `work` instances are obtained
from the `*` entry.

```yaml
db:
  instance:
    '*':
      driver: azure_sql
      server: example.databse.windows.net
      user: jtravolta
      password: grease78

    input:
      database: data_source

    work:
      database: tempdb
```

## Python usage

The configuration is exposed through the `plpipes.cfg` object.

It works as a dictionary which accepts dotted entries as keys. For
instance:

```python
from plpipes import cfg
print(f"Project root dir: {cfg['fs.root']}")
```

A sub-tree view can be created using the `cd` method:

```python
cfs = cfg.cd('fs')
print(f"Project root dir: {cfs['root']}")
```

Most dictionary methods work as expected. For instance it is possible
to mutate the configuration or to set defaults:

```python
cfg["my.conf.key"] = 7
cfg.setdefault("my.other.conf.key", 8)
```

Though note that configuration changes are not backed to disk.

## Config Initialization

The method `init` of the module `plpipes.init` is the one in charge of
populating the `cfg` object and should be called explicitly in scripts
that want to use the configuration module without relying in other
parts of the framework.

`plpipes.init.init` is where the set of files to be loaded based on
the stem and on the deployment environment is calculated and where
they are loaded into the configuration object.

[Automatic configuration](#automatic-configuration) is also performed by
this method.

Note that `plpipes.init` is a low level package that is not expected
to be used directly from user code. Instead you should use the methods
provided in `plpipes.runner` which take care of initializing the
environment and also the configuration subsystem.
