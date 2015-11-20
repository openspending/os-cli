# Guide

This is a brief guide to help developers get their data in shape for publication
to Open Spending.

It is designed to accompany the `osensure` CLI, which automates the process of
ensuring that the data in a data package conforms to the schema that describes
the data.

## JSON Table Schema - what's that then?

[JSON Table Schema](http://dataprotocols.org/json-table-schema/) is a
lightweight specification of describing schemas for tabular data. It is the
canonical way to describe data in a [Data Package]() (which is what Open Spending
uses to describe data).

If you are encountering issues modeling your data, we recommend you take a
look at the specification (it is quite short), particularly the section on
[Types and Formats](http://dataprotocols.org/json-table-schema/#field-types-and-formats).

## Open Spending Data Package

Open Spending Data Package is a [Tabular Data Package](http://dataprotocols.org/tabular-data-package/).

Open Spending Data Package is described in [OSEP #4](http://labs.openspending.org/osep/04-openspending-data-package.html).

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

## Common issues

There are several common issues encountered due to mismatch between the schema
and the data.

This can especially be true of the schema was inferred as part of the `osmodel`
CLI. There is only so much a computer can get right ;).

### ID fields

ID fields must be unique. There is no way around this :).

### Date fields

Date fields (which we use here to mean date, time, and datetime fields as
described by the JSON Table Schema specification), can be tricky to get right.

If you know that your data has dates, but that they do not all necessarily
conform to a consistent format, you will have to adjust the `format` of such
fields in the schema object to the value of `any`. For example:

```
...
"fields": [
    ...
    {
        "name": "payment_date",
        "type": "date",
        "format": "any"
    }
    ...
]
...
```

### Currency fields

Like date fields, currency fields can be tricky to get right.

We commonly see cases where additional characters are used to make amounts more
readable (e.g.: commas in 17,916,3482.90), or where currency symbols are
included in the data (e.g.: $41.99).

By default, both of these would be considered incorrect when the data is checked.

If you know your data has such values that are causing errors, and you want to
allow them to stay, you will have to change the `format` of such fields in the
schema object to the value of `currency`. For example:

```
...
"fields": [
    ...
    {
        "name": "amount",
        "type": "number",
        "format": "currency"
    }
    ...
]
...
```
