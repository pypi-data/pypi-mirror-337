from db_delta import ChangeSet, validate_dynamodb_changeset


def example_function(table):
    table.put_item(
        Item={
            "PK": "ITEM_ID#6",
            "SK": "ITEM#6",
            "id": 4,
            "name": "Test 4",
            "description": "Description 4",
        }
    )

    table.update_item(
        Key={
            "PK": "ITEM_ID#2",
            "SK": "ITEM#2",
        },
        UpdateExpression="SET #name = :name, REMOVE description",
        ExpressionAttributeNames={"#name": "name"},
        ExpressionAttributeValues={":name": "Test 2 Updated"},
    )

    table.delete_item(
        Key={
            "PK": "ITEM_ID#3",
            "SK": "ITEM#3",
        },
    )


def test_example(mock_dynamo_table):
    # load changeset from local JSON file
    changeset = ChangeSet.from_json("sample_changeset.json")

    with validate_dynamodb_changeset(mock_dynamo_table, changeset):
        # run function that executes DynamoDB operations
        example_function(mock_dynamo_table)
