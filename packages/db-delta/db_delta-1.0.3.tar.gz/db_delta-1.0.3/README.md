# DB Delta

`db-delta` is a Python testing utility package designed to be used alongside `moto` that evaluates and validates database changesets in tests that execute AWS DynamoDB operations to ensure that only the changes that you define are executed against your database, no more and no less.

Usage is simple.

#### Step 1: Define a changeset in JSON format:

```json
[
    {
        "change_type": "updated_item",
        "key":{
            "PK": "FOO",
            "SK": "BAR"
        },
        "updated_fields": [
            {
                "field": "bar",
                "update_type": "updated",
                "new_value": "bar-foo"
            },
            {
                "field": "foo",
                "update_type": "removed",
            }
        ]
    }
]
```

#### Step 2: Execute test function with the `validate_dynamodb_changeset` context manager

```python

from db_delta import ChangeSet, validate_dynamodb_changeset

def test_function_foo(table):

    expected_changeset = ChangeSet.from_json("path_to_changeset.json")

    with validate_dynamodb_changeset(table, expected_changeset):
        # call your function that modifies the contents of your database.
        # db_delta will ensure that only the changes specified are executed.
        execute_function(table, "foo", "bar")
```

`db_delta` will scan your DynamoDB table before and after the execution of your function. It will then verify that only the changes defined in the changeset have been executed. If any of the specified changes are not found, or if any changes have been made that are not defined in the changeset, an `AssertionException` is raised.

### Why use `db_delta`?

Writing exhaustive unittests to test database operations is just that. Exhausting. Unittests end up being either incomplete, or extremely verbose and repetitive. `db_delta` not ony makes tests far more readable, it also makes them far more robust. If any change is made to any item in your database that has not been defined in the changeset, your tests will fail. No exceptions and no surprises.

Consider the following example code.

```python

def example_function(table, new_name: str):
    table.update_item(
        Key={
            "PK": "FOO",
            "SK": "BAR",
        },
        UpdateExpression="SET #name = :name",
        ExpressionAttributeNames={
            "#name": "name",
        },
        ExpressionAttributeValues={
            ":name": new_name,
        },
    )
```

A typical unittest would look like the following.

```python

def test_example_function(table):

    item = table.get_item(
        Key={
            "PK": "FOO",
            "SK": "BAR",
        },
    )["Item"]
    assert item["name"] == "name"

    example_function(table, "name V2")

    item = table.get_item(
        Key={
            "PK": "FOO",
            "SK": "BAR",
        },
    )["Item"]
    assert item["name"] == "name V2"
```

There are two issues with the above.

1. Tests like the above quickly become extremely repetitive, with a great deal of duplicated code to read from your DynamoDB table and compare the difference in responses.
2. The test only checks if one field in one item has been updated as expected. Every other item from the database could have been deleted and the test would still pass.

The second point is critical and can lead to serious issues in your data. While the above example is trivial, real-life codebases often have more complex functions that execute multiple database operations in multiple places, and it quickly becomes difficult to test everything without writing long unittests that check for every possible outcome.

This is where `db_delta` comes in. Because it scans your table before and after the function you are testing is executed, it generates a complete picture of the changes made to your database as the result of running the code you are testing. It can then compare the initial and final state of your table to make sure that only the changes you expect have actually been executed.

It also neatens up the code. With `db_delta`, the above test now becomes

```python

def test_example_function(table):

    expected_changeset = ChangeSet(
        changes=[
            {
                "change_type": "updated_item",
                "key": {
                    "PK": "FOO",
                    "SK": "BAR",
                },
                "updated_fields": [
                    {
                        "field": "name",
                        "update_type": "updated",
                        "new_value": "name V2"
                    }
                ]
            }
        ]
    )

    with validate_dynamodb_changeset(table, expected_changeset):
        example_function(table, "name V2")

```

The test no longer contains any logic to retrieve and validate changes from your database. Additionally, if any other changes are made other than the specified update, `validate_dynamodb_changeset` will raise an exception and the test will fail.


### Installation

`db_delta` is available on `PyPi` and can be installed using

```bash
$ pip install db-delta
```

Alternatively, you can clone the repo and install the package manually with

```bash
$ pip install .
```

### Usage

The only two components required to use `db_delta` is the `ChangeSet` object and the `validate_dynamodb_changeset` function.

#### `ChangeSet` Object

The `ChangeSet` object is a `pydantic` data model that contains the database changes that you expect your function to produce. Expected changes are provided as an array of objects collectively referred to as a changeset. Each object within the changeset has a `change_type` field indicating the type of change. Currently, `db_delta` supports three distinct `change_type` values

- `put_item` - represent a new item inserted into your table using a `PutItem` operation.
- `updated_item` - represents a change to an existing item using a `UpdateItem` operation.
- `deleted_item` - represents an item deleted from your table using a `DeleteItem` operation.

Along with `change_type`, each update contains a `key` attribute that tells `db_delta` what hash and range key the update is referring to.

For example, if you have a function that creates a new item and updates an existing item, you can represent the result of that function with a changeset that looks like the following:

```json
[
	{
		"change_type": "put_item",
		 "key":{
            "PK": "BAR",
            "SK": "FOO"
        },
        "item": {
	        "PK": "BAR",
            "SK": "FOO",
            "bar": foo
        }
	},
    {
        "change_type": "updated_item",
        "key":{
            "PK": "FOO",
            "SK": "BAR"
        },
        "updated_fields": [
            {
                "field": "bar",
                "update_type": "updated",
                "new_value": "bar-foo"
            },
            {
                "field": "foo",
                "update_type": "removed",
            }
        ]
    }
]
```

##### `change_type: put_item`

`put_item` represents a new item in your database. When a changeset contains a `change_type: put_item` update, `db_delta` will check that the item did not exist in the initial table state, but does exist in the final state, and that the created item matches the expected structure. The JSON structure for a `put_item` update is given below.

```json
{
    "change_type": "put_item",
    "key": {
        "foo": "bar",
        "bar": "foo"
    },
    "item": {
        "foo": "bar",
        "bar": "foo",
        "id": 1,
        "description": "An example"
    }
}
```

Note that the `item` attribute must contain the entire item, including the hash and sort key.
##### `change_type: updated_item`

`updated_item` represents an item in your database that has been updated. When a changeset contains a `change_type: updated_item` update, `db_delta` will check that the item exists in both the initial table state and in the final state, and that the changes made to the item match the changes defined in the changeset. The JSON structure for an `updated_item` update is given below.

```json
{
    "change_type": "updated_item",
    "key": {
        "foo": "bar",
        "bar": "foo"
    },
    "updated_fields": [
        {
            "field": "newField",
            "update_type": "added",
            "new_value": "bar-foo"
        },
        {
            "field": "updatedField",
            "update_type": "updated",
            "new_value": "bar-foo"
        },
        {
            "field": "removedField",
            "update_type": "removed",
        }
    ]
}
```

All expected updates to the item must be defined in the `updated_fields` column, where each update has the following structure

```json
{
    "field": "String",
    "update_type": "added|updated|removed",
    "new_value": "String | Integer | Float | Object"
}
```

The `field` parameter specifies the attribute of the item that the update is referring to, while the `update_type` parameter indicates what type of change is expected. There are three possible values for the `update_type` parameter

- `added`- an attribute that has been created as the result of the `UpdatedItem` operation. It must __NOT__ exist in the initial item.
- `updated` - an attribute that existed in both the initial and final item, but was updated to a new value.
- `removed` - an attribute that was present in the initial item, but was removed using a `REMOVE :key` statement within your DynamoDB update. It __MUST__ exist in the initial item.

The `new_value` parameter is required when `update_type` is one of `[added,updated]` and must match the final value of the specified field. `new_value` can be omitted if the `update_type` is `removed`.

##### `change_type: deleted_item`


`deleted_item` represents an item that has been deleted from your database. When a changeset contains a `DeletedItem` update, `db_delta` will check that the item exists in the initial table state, but does not exist in the final state.

```json
{
    "change_type": "deleted_item",
    "key": {
        "foo": "bar",
        "bar": "foo"
    },
}
```

##### Generating `ChangeSet` instance

A `ChangeSet` instance can be generated one of two ways. Either define your changeset in code

```python
expected_changeset = ChangeSet(
    changes=[
        {
            "change_type": "updated_item",
            "key": {
                "PK": "FOO",
                "SK": "BAR",
            },
            "updated_fields": [
                {
                    "field": "name",
                    "update_type": "updated",
                    "new_value": "name V2"
                }
            ]
        }
    ]
)
```

or define your changeset in a JSON file and use the `from_json` class method

```python
expected_changeset = ChangeSet.from_json("path_to_changeset.json")
```

The `from_json` method is generally recommended as it keeps unittests smaller and allows you to re-use predefined changesets.

#### `validate_dynamodb_changeset` Function

Once you have a `ChangeSet` instance constructed with your expected changes, simply execute your function in the `validate_dynamodb_changeset` context manager.

```python
from db_delta import ChangeSet, validate_dynamodb_changeset


def test_function_foo(table):

    expected_changeset = ChangeSet.from_json("path_to_changeset.json")

    with validate_dynamodb_changeset(table, expected_changeset):
        # call your function that modifies the contents of your database.
        # db_delta will ensure that only the changes specified are executed.
        execute_function(table, "foo", "bar")
```

If `execute_function` results in any changes that are not defined in the changeset, `validate_dynamodb_changeset` will raise an `AssertionException`.

Note that the `validate_dynamodb_changeset` requires both a configured DynamoDB table resource as well as the expected changeset. The table resource should be created using `boto3`.

```python
table = boto3.resource("dynamodb").Table("example-table")
```

### Test Setup

In order to get the most out of `db_delta` its critical that you set up your unittests correctly. `db_delta` is designed to be used alongside `moto` and `pytest`. We strongly recommend that you get familiar with both before integrating `db_delta` into your unittests. For a basic example, see the `examples/basic` folder in this repository, which shows you how to configure a basic testing environment with the required tools.

### Advanced Usage

`validate_dynamodb_changeset` accepts an optional formatting function that is called on all items before making comparisons. This is especially useful if your code adds certain metadata fields such as created and update timestamps that you want to exclude from any comparisons.

For example:

```python

def strip_metadata(row: Dict) -> Dict:
    for key in ["createdTs", "updatedTs"]:
        row.pop(key)
    return row


def test_function_foo(table):

    expected_changeset = ChangeSet.from_json("path_to_changeset.json")

    with validate_dynamodb_changeset(table, expected_changeset, formatter=strip_metadata):
        # call your function that modifies the contents of your database.
        # db_delta will ensure that only the changes specified are executed.
        execute_function(table, "foo", "bar")
```

The `strip_metadata` function is called on all items before any comparisons are made. In this case, both the `createdTs` and `updatedTs` timestamps are removed from any items, ensuring that your changesets do not need to include the updated values for mocked timestamps. This can help to keep the changesets compact.
