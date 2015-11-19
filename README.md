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

* [Usage](#usage)
* [Development](#development)
* [Open Spending Data Package](#open-spending-data-package)
* [Next Steps](#next-steps)

## Usage

This section is intended to be used by non-tech users uploading
data to Open Spending flat data storage.

### Getting Started

Ensure you have `Python 2.7, 3.3 or 3.4` installed.

To get started activate virtual environments and install
dependencies by command:

```
source activate.sh
```

You now have `openspending` and `os` (an alias) on your path.

See the help:

```
openspending --help
```

See `GUIDE.md` for more information.

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
you@machine:~$ goodtables structure examples/data_invalid.csv

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
you@machine:~$ goodtables structure examples/data_valid.csv

WELL DONE! THE DATA IS VALID :)

```

See the [Good Tables documentation](http://goodtables.readthedocs.org/) for more.

#### Step 2. Model the data

Use the `makemodel` subcommand to model the data.

Modeling the data means:

* Creating an [Open Spending Data Package](#open-spending-data-package) to "house" the data
* Inferring a schema for the data resources therein (Data Packages use [JSON Table Schema](http://dataprotocols.org/json-table-schema/)).

```
you@machine:~$ openspending makemodel examples/data_valid.csv --mapping id=my_id,amount=my_amount
```

**Note:** If your data features both `id` and `amount` fields, then you are not required to provide a mapping via the command line.

See the [makemodel docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

#### Step 3. Check the model

Use the `checkmodel` subcommand to ensure that the Data Package descriptor is valid.

Now we actually have a data package and an initial schema for our data,
let's check that our data package descriptor is a valid Open Spending
Data Package (which it obviously will be if it was created at step 2...
but let's do it anyway).

```
you@machine:~$ openspending checkmodel examples/dp-valid
# or
you@machine:~$ openspending checkmodel examples/dp-invalid
```

See the [checkmodel docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

#### Step 4. Check the Data Schema

Use the `checkdata` subcommand to ensure that the data conforms to the schema.

```
you@machine:~$ openspending checkdata examples/dp-valid
# or
you@machine:~$ openspending checkdata examples/dp-invalid
```

See the [checkdata docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

#### Step 5. Authenticate with Open Spending

ignore this step for now, but do ensure that you configured your .openspendingrc as described above.

<del>
Use the `auth` subcommand to authenticate with Open Spending.

The previous steps are completely local.

In order to interact with an Open Spending service, you must be an
authenticated user.

The next step is to upload our new data package to the datastore,
so, we need to authenticate.

This is the first step that uses the .openspendingrc file.
</del>

```
you@machine:~$ openspending auth get_token
```

See the [auth docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

#### Step 5. Upload to the Open Spending datastore

Use the `upload` subcommand to upload a data package to Open Spending.

```
you@machine:~$ openspending upload examples/dp-valid
```

See the [upload docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

## Development

This section is intended to be used by tech users collaborating
on this project.

### Getting Started

Ensure you have `nvm` and `Python 2.7, 3.3 or 3.4` installed.

To get started activate virtual environments and install
dependencies by command:

```
source activate.dev.sh
```

To debug the CLI use:

```
python debug.py --help
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

## Open Spending Data Package

Open Spending Data Package is a [Tabular Data Package](http://dataprotocols.org/tabular-data-package/).

Open Spending Data Package is described in [OSEP #4](http://labs.openspending.org/osep/04-openspending-data-package.html).

It extends and modifies [Budget Data Package](https://github.com/openspending/budget-data-package/blob/master/specification.md).

The following fields are `REQUIRED` in an Open Spending Data Package:

**Metadata fields**

Metadata fields are located directly on the descriptor object. These required
fields are in addition to the required fields for all
[Tabular Data Packages](http://dataprotocols.org/tabular-data-package/).

* `owner`: The `owner` field is a `STRING` which is the username of the
person or organization entity in Open Spending that the package belongs to.
* `openspending`: The `openspending` field is a `HASH` which `MAY` have a key named `mapping`.
* `openspending.mapping`: The `openspending.mapping` field is a `HASH` where each
key is a resource field, and the value is a field fond in the resource.
In this way, it is possible to provide compliant Open Spending data without making extensive
changes to existing data files.
* `currency`: The currency of the data.

**Resource fields**

Resource fields are located on each object in the `resources` array.

The only required fields are `id` and `amount`. However, of the `openspending.mapping`
object in the metadata declares a mapping for one or both of `id` and `amount`, then
those fields are required; not `id` and `amount`.

* `id`: A string which is a unique identifier for this line
* `amount`: The monetary amount of this line

The code for handling Open Spending Data Packages is [here](https://github.com/openspending/oscli-poc/tree/master/oscli/osdatapackage).

## Next steps

* Build out actual Storage and Auth services
* Build a web UI based around this CLI
* Extract out components into their own packages; Remove existing mocks
* Provide or describe and API for accessing Data Packages directly from the flat file store
