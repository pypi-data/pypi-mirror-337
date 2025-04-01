# Actions

Actions are the atomic units of work that when combined allow one to
perform the tasks required by the project.

They are defined inside the `actions` directory in a hierarchical way.

There are several types of actions predefined and also new ones can be
added.

Actions are declared with a configuration file with the name of the
action, for instance `preprocessor.yaml`.

Inside this configuration file the action type must be declared using
the `type` setting. For instance:

```yaml
type: python_script
```

Alternatively, `plpipes` can autodetect an action type when it finds a
file with the action name and some recognized extension (for example,
`model_training.py`). In that case the configuration file is not
required.

The list of currently supported action types follows:

## `python_script`

Extension: `.py`

The python code in the file is executed.

The following objects are directly available in the script:

- `plpipes`: the main `plpipes` package.

- `cfg`: the configuration object.

- `action_cfg`: the action configuration (read from the action yaml
    file or from the global configuration).

- `db`: a shortcut for the `plpipes.database` package.

## `sql_script`

Extension `.sql`

Runs the SQL sentences in the action file against the `work` database.

The SQL code is preprocessed using
[Jinja](https://jinja.palletsprojects.com/en/3.1.x/). That feature can
be used to for instance, set values from the configuration:

```sql
CREATE TABLE foo AS
SELECT * FROM bar
WHERE data >= "{{ cfg["data.limits.date.low.cutoff"] }}"
```

*Currently this action type is only supported when `work` is backed by
a SQLite database.*

## `sql_table_creator`

Extension `.table.sql`

Runs the SQL query in the file and stores the output data frame in a
new table with the name of the action.

Jinja is also used to preprocess the SQL statement.

## `qrql_script`

Extension: `.prql`

[PRQL](https://prql-lang.org/) (Pipelined Relational Query Language)
is an alternative query language for relational databases.

This action runs the PRQL sentences in the file against the `work`
database.

Jinja is used to preprocess the PRQL statement.

*Currently this action type is only supported when `work` is backed up
by a SQLite database.*

## `qrql_table_creator`

Runs the PRQL query in the file and stores the output data frame in a
new table with the name of the action.

Jinja is also used to preprocess the PRQL statement.

## `quarto`

Extension: `.qmd`

Processes the file using [quarto](https://quarto.org/).

The following configuration options can be used:

- `dest`:
    - `key`: any of `work`, `input` or `output`

    - `dir`: destination dir to store the generated files.

    - `file`: destination file name. Defaults to the action name with
        the extension associated to the output format.

    - `format`: output format.

The action configuration can also be included directly in the `qmd`
yaml header, under the `plpipes` branch.

## `sequence`

Runs a set of actions in sequence.

The list of actions to be run are declared as an array under the
`sequence` setting.

Relative action names (starting by a dot) are also accepted.

Example `yaml` configuration:

```yaml
type: sequence
sequence:
    - .bar
    - miau.gloglo
```

## `loop`

The `loop` action is a construct for creating action loops.

It runs a set of subactions in sequence repeatedly according to
specified iterators, enabling one to perform repetitive operations
following several strategies and with varying parameters.

The configuration specifies the subactions to be executed in the loop
and the iterators that control the iterations. These are the accepted
keys:

- `sequence`: Specifies the names of the subactions to be executed in
    the loop. The subactions will be executed in the order specified.

- `iterator`: Specifies the iterators to be used for the loop.

    Each iterator is defined by a key and its corresponding
    configuration, which includes the type of the iterator and any
    required parameters.

    The supported iterator types are:

    - `values`: Iterates over a list of specific values.

    - `configkeys`: Iterates over the keys of a specific path in the
        configuration.

- `ignore_errors` (optional): If set to `true`, any errors that occur
    during an iteration will be logged but will not stop the loop. If
    not specified or set to `false`, an error during iteration will
    raise an exception and halt the loop.

Sample configuration:

```yaml
loop:
  sequence:
    - subaction1
    - subaction2
    - subaction3

  iterator:
    one:
      type: values
      values:
        - value1
        - value2
        - value3
    two:
      type: configkeys
      path: my_config.path

  ignore_errors: true
```
