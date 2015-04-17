# OSCLI

The is a minimal, command line implementation to load data into an Open Spending
flat file datastore.

**This is not compatible with the current version of Open Spending**.

Rather, it is based on ideas in the following Open Spending Enhancement
Proposals:

* [OSEP #4](http://labs.openspending.org/osep/04-openspending-data-package.html)
* [OSEP #5](http://labs.openspending.org/osep/05-etl-workflow.html)

## Jump to section

* [Getting started](#getting-started)
    * [Installation](#installation)
    * [Configuration](#configuration)
    * [Data](#data)
* [Usage](#usage)
* [Open Spending Data Package](#open-spending-data-package)
* [Mock Services](#mock-services)

## Getting started

### Installation

Ensure you have Python 2.7, 3.3 or 3.4 installed. A virtual environment is good too.

Move into your directory and:

```
# Get the code
git clone https://github.com/openspending/oscli-poc.git .

# Install the dependencies
pip install -r requirements/base.txt

# Additionally, if you want some extra tools for local development
pip install -r requirements/local.txt

# Additionally, if you want to run the tests
pip install -r requirements/test.txt
```

Now, let's install the `openspending` CLI:

```
python setup.py install
```

You now have `openspending` and `os` (an alias) on your path.

See the help:

```
openspending --help
```

### Configuration

#### User settings

The `openspending` CLI uses an `.openspendingrc` file to manage various settings
related to you, the user. When using the CLI, it will look for an
`.openspendingrc` file in one of two places, in order:

* The current working directory
* The executing user's $HOME
* If not found, an error will be raised

```
# .openspendingrc

{
    "api_key": "",
    "token": "SOME_TOKEN_FROM_AUTH_SERVICE"
}
```

#### Mock services

The code has some mock interfaces for services that do not exist yet. One is the
storage service that will provide access to the Open Spending datastore.

Therefore, if you are testing the upload functionality, you will need to do some
additional configuration:

* Get an AWS account
* Get an AWS key pair
* Create a bucket for Open Spending data in your AWS account
* Export the following environment variables:

```
OPENSPENDING_STORAGE_BUCKET_NAME={YOUR_AWS_BUCKET_NAME}
OPENSPENDING_ACCESS_KEY_ID={YOUR_AWS_ACCESS_KEY_ID}
OPENSPENDING_SECRET_ACCESS_KEY={YOUR_AWS_SECRET_ACCESS_KEY}
```

### Data

You'll need some spend data in CSV format.

The `examples` directory contains some data to test with.

## Usage

Once you have fully configured your setup, we can get to work.

Here I'll describe the linear sequence for using the CLI, where you can start
from having a CSV of spend data, and proceeed through modeling and upload
of that data as part of an Open Spending Data Package.

Of course, you can start at any step in the sequence if you know that your
data conforms with the previous steps.

### Step 1. Ensure resources are well formed

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

### Step 2. Model the data

Use the `makemodel` subcommand to model the data.

Modeling the data means:

* Creating an [Open Spending Data Package](#open-spending-data-package) to "house" the data
* Inferring a schema for the data resources therein (Data Packages use [JSON Table Schema](http://dataprotocols.org/json-table-schema/)).

```
you@machine:~$ openspending makemodel /examples/data_valid.csv --mapping id=my_id,amount=my_amount
```

**Note:** If your data features both `id` and `amount` fields, then you are not required to provide a mapping via the command line.

See the [makemodel docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

### Step 3. Check the model

Use the `checkmodel` subcommand to ensure that the Data Package descriptor is valid.

Now we actually have a data package and an initial schema for our data,
let's check that our data package descriptor is a valid Open Spending
Data Package (which it obviously will be if it was created at step 2...
but let's do it anyway).

```
you@machine:~$ openspending checkmodel /examples/test_data_package
```

See the [checkmodel docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

### Step 4. Check the Data Schema

Use the `checkdata` subcommand to ensure that the data conforms to the schema.

```
you@machine:~$ openspending checkdata /examples/test_data_package
```

See the [checkdata docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

### Step 4. Authenticate with Open Spending

Use the `auth` subcommand to authenticate with Open Spending.

The previous steps are completely local.

In order to interact with an Open Spending service, you must be an
authenticated user.

The next step is to upload our new data package to the datastore,
so, we need to authenticate.

This is the first step that uses the .openspendingrc file.

```
you@machine:~$ openspending auth get_token
```

See the [auth docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

### Step 5. Upload to the Open Spending datastore

Use the `upload` subcommand to upload a data package to Open Spending.

```
you@machine:~$ openspending upload /examples/test_data_package
```

See the [upload docstring](https://github.com/openspending/oscli-poc/blob/master/oscli/main.py) for more documentation.

## Mock services

Seeing as this is still at proof-of-concept stage, the code contains some
basic mocks for services that it requires.

### base.OpenSpendingService

`_mock.base.OpenSpendingService` is the base service that others inherit from.

It provides two methods:

* `gatekeeper`: accepts a token as an argument, and returns True or False
based on whether the token is valid. Currently wraps `_accept_token`
* `_accept_token`: accepts a token as an argument, and returns True or False
based on whether the token is valid.

### AuthService

`_mock.AuthService` provides services for login and logout.

* `get_token`: Return a dummy token. Currently, having a token indicates the user
is authenticated. In a proper implementation, tokens would be signed, have
expiry, and so on.

### StorageService

`_mock.StorageService` provides services for interacting with Open Spending
file storage. This includes connecting to a bucket, and providing methods to
manage uploads of data packages.

* `get_upload_access`: Ultimately provides temporary URLs that are used to upload
files in data packages.

## Open Spending Data Package

Open Spending Data Package is a [Tabular Data Package](http://dataprotocols.org/tabular-data-package/).

It extends and modifies [Budget Data Package](https://github.com/openspending/budget-data-package/blob/master/specification.md).

The enhancement proposal for Open Spending Data Package is [here](http://labs.openspending.org/osep/04-openspending-data-package.html).

Ultimately, Open Spending should support Budget Data Packages proper.

Having an Open Spending Data Package allows us to:

* Add new properties that are desirable for Open Spending before they are added upstream
* Flexibility to not require some of the things that are required in Budget Data Package
* Provide a testing ground for ideas that may ultimately get merged into Budget Data Package

The code for handling Open Spending Data Packages is [here](https://github.com/openspending/oscli-poc/tree/master/oscli/osdatapackage).

## Next steps

* Build out actual Storage and Auth services
* Build a web UI based around this CLI
* Extract out components into their own packages; Remove existing mocks
* Provide or describe and API for accessing Data Packages directly from the flat file store
