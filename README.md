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

If you do have errors, you'll get a report simialr to the one below: use it to fix the errors, and
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

Use the information to fix the errors until you get something like:

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
