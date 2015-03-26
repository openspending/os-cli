# ETL CLI

An MVP implementation of a CLI to load data into Open Spending.

Based on ideas in [OSEP #4](http://labs.openspending.org/osep/04-openspending-data-package.html) and
[OSEP #5](http://labs.openspending.org/osep/05-etl-workflow.html).


## Start

### Install

Ensure you have Python 2.7, 3.3 or 3.4 installed. A virtual environment is good too.

Move into your directory and:

```
# Get the code
git clone https://github.com/openspending/etlcli-mvp.git .

# Install the dependencies
pip install -r requirements/base.txt

# Additionally, if you want some extra tools for local development
pip install -r requirements/local.txt

# Additionally, if you want to run the tests
pip install -r requirements/test.txt
```

### Get data

You'll need some spend data in CSV format. The `examples` directory contains some data to test with.

### Start work

With that done, let's get to work.

#### Step 1. Ensure resources are well formed

Use the Good Tables CLI to ensure there are no obvious structural errors in your resource.

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

#### Step 2. Model the data

Use the `osmodel` CLI to infer a [JSON Table Schema](http://dataprotocols.org/json-table-schema/) from the data, create an OpenSpending-compatible Budget [Data Package](https://github.com/openspending/budget-data-package/blob/master/specification.md).

```
you@machine:~$ osmodel /examples/data_valid.csv my-package --datapackage_path /path/to/my-local-datapackages --mapping id=my_id,amount=my_amount
```

### Step 3. Validate the data

Now that we have a valid data package, including a schema for our data, we want to use this information to check the data in our file.

This is done with the `osensure` CLI.

```
you@machine:~$ osensure /examples/test_data_package
```

### Step 4. Authenticate with Open Spending

The previous steps are completely local.

In order to interact with an Open Spending service, we need to authenticate ourselves.

The next step is to upload our new data package. So, in order to do this, we need to authenticate.

```
you@machine:~$ osauth me@example.com
```

### Step 5. Upload to the Open Spending data store

Ok, time to upload!

```
you@machine:~$ osstore /examples/test_data_package
```
