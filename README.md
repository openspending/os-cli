# OSCLI

[![Travis](https://img.shields.io/travis/openspending/os-datastore-cli.svg)](https://travis-ci.org/openspending/os-datastore-cli)
[![Coveralls](http://img.shields.io/coveralls/openspending/os-datastore-cli.svg?branch=master)](https://coveralls.io/r/openspending/os-datastore-cli?branch=master)

The is a minimal, command line implementation to load data into an Open Spending
flat file datastore.

Rather, it is based on ideas in the following Open Spending Enhancement
Proposals:

* [OSEP #4](http://labs.openspending.org/osep/04-openspending-data-package.html)
* [OSEP #5](http://labs.openspending.org/osep/05-etl-workflow.html)

## Jump to section

* [Guide](GUIDE.md)
* [Usage](#usage)
* [Development](#development)
* [Next Steps](#next-steps)

## Usage

This section is intended to be used by non-tech users uploading
data to Open Spending flat data storage.

### Getting Started

Ensure you have `Python 2.7, 3.3 or 3.4` installed system-wide
or using virtualenv.

To get started install cli:

```
$ python setup.py install
```

You now have `openspending` and `os` (an alias) on your path.

See the help:

```
$ openspending --help
```

### Config

The `openspending` CLI uses an `.openspendingrc` file to manage various settings
related to you, the user. When using the CLI, it will look for an
`.openspendingrc` file in one of two places, in order:

* The current working directory
* The executing user's $HOME
* If not found, services that require settings from the config file will fail.

A config file looks something like this:

```
# .openspendingrc

{
    "api_key": ""
}
```

The CLI has a helper command for working with config files: `openspending config`.

* `openspending config locate`: return the filepath of the currently active config as JSON,
or null.
* `openspending config ensure`: return the currently active config as JSON, creating
a skeleton config first in $HOME if no config is found.
* `openspending config read`: return the currently active config as JSON, or null.
* `openspending config write '<json>'`: write additional data to config or create a new config file and return the currently active config as JSON.

So, to configure correctly, do the following:

* Create an `.openspendingrc` file as per the above description, or, run
`openspending config ensure` to add a skeleton file in your $HOME directory

### Data

You'll need some spend data in CSV format.

The `examples` directory contains some data to test with.

### Upload

Once you have fully configured your setup, we can get to work.

Here I'll describe the linear sequence for using the CLI, where you can start
from having a CSV of spend data, and proceeed through modeling and upload
of that data as part of an Open Spending Data Package.

Of course, you can start at any step in the sequence if you know that your
data conforms with the previous steps.

#### Step 1. Ensure resources are well formed

Use the Good Tables CLI to ensure there are no obvious structural errors in
your resource.

```
$ goodtables structure examples/data_invalid.csv

OOPS.THE DATA IS INVALID :(

META.
Name: structure

###

RESULTS.
+-------------+-----------------------------------------------------------------------+---------------+---------------+
|   row_index | result_message                                                        | result_id     | result_name   |
+=============+=======================================================================+===============+===============+
|           2 | Row 2 is empty.                                                       | structure_005 | Empty Row     |
+-------------+-----------------------------------------------------------------------+---------------+---------------+
|           3 | Row 3 is defective: the dimensions are incorrect compared to headers. | structure_003 | Defective Row |
+-------------+-----------------------------------------------------------------------+---------------+---------------+
```

If you do have errors, you'll get a report similar to that above.

Use that information to fix the errors until you get something like:

```
$ goodtables structure examples/data_valid.csv

WELL DONE! THE DATA IS VALID :)

```

See the [Good Tables documentation](http://goodtables.readthedocs.org/) for more.

#### Step 2. Model the data

Use the `jsontableschema` CLI to infer a model from the data.

Modeling the data means:

* Creating an [Open Spending Data Package](#open-spending-data-package) to "house" the data
* Inferring a schema for the data resources therein (Data Packages use [JSON Table Schema](http://dataprotocols.org/json-table-schema/)).

```
$ jsontableschema infer examples/data_valid.csv
```

**Note:** If your data features both `id` and `amount` fields, then you are not required to provide a mapping via the command line.

See the [jsontableschema documentation](https://github.com/okfn/jsontableschema-py) for more.

#### Step 3. Validate the model

Use the `validate model` subcommand to ensure that the Data Package descriptor is valid.

Now we actually have a data package and an initial schema for our data,
let's check that our data package descriptor is a valid Open Spending
Data Package (which it obviously will be if it was created at step 2...
but let's do it anyway).

```
$ openspending validate model examples/dp-valid
```

To see how it looks for invalid model:

```
$ openspending validate model examples/dp-invalid
```

See the [validate docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/cli.py) for more documentation.

#### Step 4. Check the Data Schema

Use the `validate data` subcommand to ensure that the data conforms to the schema.

```
$ openspending validate data examples/dp-valid
```

To see how it looks for invalid data:

```
$ openspending validate data examples/dp-invalid
```

See the [validate docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/cli.py) for more documentation.

#### Step 5. Upload to the Open Spending datastore

Use the `upload` subcommand to upload a data package to Open Spending.

To make it done there has to be an `api_key` setting in your .openspendingrc.

```
$ openspending upload examples/dp-valid
```

See the [upload docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/cli.py) for more documentation.

## Development

This section is intended to be used by tech users collaborating
on this project.

### Getting Started

Ensure you have `nvm` and `Python` installed.

To get started activate virtual environments, install
dependencies and add pre-commit hook to review and test code
by command:

```
$ source activate.sh
```

To debug the CLI use:

```
$ python -m oscli/cli --help
```

### Reviewing

The project follow the next style guides:
- [Open Knowledge Coding Standards and Style Guide](https://github.com/okfn/coding-standards)
- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

To check the project against Python style guide:
```
$ npm run review
```
### Testing

To run tests with coverage check:
```
$ npm run test
```
Coverage data will be in the `.coverage` file.

## Next steps

* ~~Build out actual Storage and Auth services~~
* Build a web UI based around this CLI
* Extract out components into their own packages; Remove existing mocks
* Provide or describe and API for accessing Data Packages directly from the flat file store
