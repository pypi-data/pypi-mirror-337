import json
from decimal import Decimal

import pytest
import boto3
from moto import mock_aws


@pytest.fixture
def mock_dynamodb_resource():
    with mock_aws():
        yield boto3.resource("dynamodb")


@pytest.fixture
def mock_dynamo_table(mock_dynamodb_resource):
    with open("tests/data/table_schema.json", "r") as f:
        schema = json.load(f)

    table = mock_dynamodb_resource.create_table(**schema)
    with open("tests/data/initial_db_items.json", "r") as f:
        data = json.load(f, parse_float=Decimal)

    for item in data:
        table.put_item(Item=item)
    yield table
