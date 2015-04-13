# OSCLI

The is a minimal, command line implementation to load data into an Open Spending
flat file datastore.

**This is not compatible with the current version of Open Spending**.

Rather, it is based on ideas in the following Open Spending Enhancement
Proposals:

* [OSEP #4](http://labs.openspending.org/osep/04-openspending-data-package.html)
* [OSEP #5](http://labs.openspending.org/osep/05-etl-workflow.html)


## Setup

### Install

Ensure you have Python 2.7, 3.3 or 3.4 installed. A virtual environment is good too.

Move into your directory and:

```
# Get the code
git clone https://github.com/openspending/oscli.git .

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

### Get data

You'll need some spend data in CSV format.

The `examples` directory contains some data to test with.

## Using the CLI

Once you have fully configured your setup, we can get to work.

`openspending` can be used with new data in the following sequence.

Alternatively, you can start at any step if you know your data conforms
with the previous steps.

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

META.
Name: structure

###

RESULTS.
No results were generated.
```

### Step 2. Model the data

Use the `makemodel` subcommand to model the data.

Modeling the data involves two related steps:

* Creating an [Open Spending Data Package](http://labs.openspending.org/osep/04-openspending-data-package.html)
* Inferring a schema for the data resources therein (Data Packages use [JSON Table Schema](http://dataprotocols.org/json-table-schema/)).

```
you@machine:~$ openspending makemodel /examples/data_valid.csv --mapping id=my_id,amount=my_amount
```

**Note:** If your data features both `id` and `amount` fields, then you are not required to provide a mapping via the command line.

### Step 3. Check the model

Use the `checkmodel` subcommand to ensure that the Data Package descriptor is valid.

Now we actually have a data package and an initial schema for our data,
let's check that our data package descriptor is a valid Open Spending
Data Package (which it obviously will be if it was created at step 2...
but let's do it anyway).

```
you@machine:~$ openspending checkmodel /examples/test_data_package
```

### Step 4. Check the Data Schema

Use the `checkdata` subcommand to ensure that the data conforms to the schema.

```
you@machine:~$ openspending checkdata /examples/test_data_package
```

### Step 4. Authenticate with Open Spending

Use the `auth` subcommand to authenticate with Open Spending.

The previous steps are completely local.

In order to interact with an Open Spending service, we need to authenticate ourselves.

The next step is to upload our new data package to the datastore.

So, we need to authenticate.

This is the first step that uses the .openspendingrc file.

This configuration file contains a JSON object.

For specifics, see the section below.

```
you@machine:~$ openspending auth get_token
```

### Step 5. Upload to the Open Spending datastore

Use the `upload` subcommand to upload a data package to Open Spending.

```
you@machine:~$ openspending upload /examples/test_data_package
```


## Mock services

Seeing as this is still at proof-of-concept stage, the code contains some
basic mocks for services that it requires.

#### base.OpenSpendingService

`_mock.base.OpenSpendingService` is the base service that others inherit from.

It provides two methods:

* `gatekeeper`: accepts a token as an argument, and returns True or False
based on whether the token is valid. Currently wraps `_accept_token`
* `_accept_token`: accepts a token as an argument, and returns True or False
based on whether the token is valid.

#### AuthService

`_mock.AuthService` provides services for login and logout.

* `login`: Return a dummy token. Currently, having a token indicates the user
is authenticated. In a proper implementation, tokens would be signed, have
expiry, and so on.
* `logout`: Logs out a user by invalidating the user's token. Currently, this
means removing the token from .openspendingrc.

#### StorageService

`_mock.StorageService` provides services for interacting with Open Spending
file storage. This includes connecting to a bucket, and providing methods to
manage uploads of data packages.
