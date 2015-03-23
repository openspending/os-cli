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

The full workflow we are going for is outlined below in [Describing the workflow](#describing-the-workflow).

Here we'll just outline the commands.

1. `goodtables structure /path/to/file.csv`
    * Ensures that the CSV is well formed (no obvious structural errors).
    * The response is a valid JSON object, giving a report of what the
      `goodtables structure` processor found.
    * If `report.results` is an empty array, then no errors were detected.
      You can proceed. If there are errors, use the report to fix them, and
      repeat until your data source is well formed.
2. `osmodel /path/to/file.csv my-package-name --datapackage_path /path/to/my-local-datapackages --mapping my_id=your_id,my_amount=your_amount`
    * In progress


## Describing the workflow

Flow (moving from step to step) will be manual for now.

### Step 1. Ensure resources are well formed

In MVP, only check CSV file. Next iteration will for example support a
data package with potentially multiple CSVs that are each run through this step.

* Resource is CSV
* Resource is well formed (structure validator from goodtables)
    * Based on a sample of, say, max. 20,000 rows
* IF well formed, can move to next step
* IF NOT well formed, use the report from goodtables to fix the issues, and repeat this step until good.

![Step 1: Valid data](https://dl.dropboxusercontent.com/u/13029373/okfn/os/step1_valid.gif)

![Step 1: Invalid data](https://dl.dropboxusercontent.com/u/13029373/okfn/os/step1_invalid.gif)


### Step 2. Model the data

* User has a CSV of data on some local path
* User can also pass path to archive of data for this data package
* User can pass in path to her data packages directory, otherwise we create one in HOME
* If CSV does not have minimal required fields, needs to pass a mapping
* User needs to also pass required metadata (eg: currency)
* From the CSV data, infer a JSON Table Schema
* For the data package, create a mapping of given fields to required fields (eg: amounts, ids)
* For the data package, create additional meta data (name, currency)
* Generate an OS Budget Data Package
* Persist the data package (descriptor + data + archive) into the data packages directory under name

![Step 2: Valid mapping](https://dl.dropboxusercontent.com/u/13029373/okfn/os/step2_mapping_valid.gif)

![Step 2: Invalid mapping](https://dl.dropboxusercontent.com/u/13029373/okfn/os/step2_mapping_invalid.gif)

![Step 2: Full](https://dl.dropboxusercontent.com/u/13029373/okfn/os/step2_full.gif)

### Step 3. Validate data against model

* Valid data itself based on JTS and DP
    * eg: all id fields unique
* A lot of this is in goodtables already

### Step 4. Push datapackage to OS Datastore

(strictly speaking, this step requires the user to be authed; previous steps do not)

* everything referenced in the data package
    * data/*
    * archive/*
* goes to /datasets/{username}/{packagename}/
* user gets back ref to location
* probably have some basic browser UI over this raw data store when it is accessed directly on web
