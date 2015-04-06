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
