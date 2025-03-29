import json
from enum import Enum
from typing import Dict, Any, List, Literal, Callable
from decimal import Decimal

from pydantic import BaseModel, StringConstraints, Field, model_validator
from typing_extensions import Annotated


class PutItem(BaseModel):
    change_type: Literal["put_item"]
    key: Dict[str, str | int | float]
    item: Dict[str, Any]


class UpdateTypeEnum(str, Enum):
    ADDED = "added"
    UPDATED = "updated"
    REMOVED = "removed"


class FieldUpdate(BaseModel):
    field: Annotated[str, StringConstraints(min_length=1)]
    update_type: UpdateTypeEnum
    new_value: Annotated[Any | None, Field(default=None)]

    @model_validator(mode="after")
    def validate_model(self):

        match self.update_type:
            case UpdateTypeEnum.ADDED:
                if self.new_value is None:
                    raise Exception("Update type 'ADDED' requires 'new_value'.")  # noqa

            case UpdateTypeEnum.UPDATED:
                if self.new_value is None:
                    raise Exception(
                        "Update type 'UPDATED' requires 'new_value' and 'old_value'."  # noqa
                    )

        return self


class UpdatedItem(BaseModel):
    change_type: Literal["updated_item"]
    key: Dict[str, str | int | float]
    updated_fields: List[FieldUpdate]


class DeletedItem(BaseModel):
    change_type: Literal["deleted_item"]
    key: Dict[str, str | int | float]


class ChangeSet(BaseModel):
    changes: Annotated[
        List[PutItem | UpdatedItem | DeletedItem], Field(discriminator="change_type")
    ]

    @classmethod
    def from_json(
        cls,
        path: str,
        parse_float: Callable | None = Decimal,
        parse_int: Callable | None = Decimal,
    ):
        with open(path, "r") as f:
            changes = json.load(f, parse_float=parse_float, parse_int=parse_int)
        return cls(changes=changes)


[
    {
        "location": "siloes/silo_id=snJIZE2z/file0.parquet",
        "name": "file0.parquet",
        "size": Decimal("0"),
        "uploadedBy": "eeee3183-69ca-47e7-9826-00e9111f4efd",
        "lastModifiedTs": "2025-02-22T08:15:52.384006Z",
    },
    {
        "location": "siloes/silo_id=snJIZE2z/file1.parquet",
        "name": "file1.parquet",
        "size": Decimal("0"),
        "uploadedBy": "eeee3183-69ca-47e7-9826-00e9111f4efd",
        "lastModifiedTs": "2025-02-22T08:15:52.384006Z",
    },
    {
        "location": "siloes/silo_id=snJIZE2z/file2.parquet",
        "name": "file2.parquet",
        "size": Decimal("1024"),
        "uploadedBy": "eeee3183-69ca-47e7-9826-00e9111f4efd",
        "lastModifiedTs": "2025-02-22T08:15:52.384006Z",
    },
    {
        "location": "siloes/silo_id=snJIZE2z/file4.parquet",
        "name": "file4.parquet",
        "size": Decimal("0"),
        "uploadedBy": "eeee3183-69ca-47e7-9826-00e9111f4efd",
        "lastModifiedTs": "2025-02-22T08:15:52.384006Z",
    },
]
[
    {
        "name": "file0.parquet",
        "location": "siloes/silo_id=snJIZE2z/file0.parquet",
        "size": Decimal("0"),
        "uploadedBy": "eeee3183-69ca-47e7-9826-00e9111f4efd",
        "lastModifiedTs": "2025-02-22T08:15:52.384006Z",
    },
    {
        "name": "file1.parquet",
        "location": "siloes/silo_id=snJIZE2z/file1.parquet",
        "size": Decimal("0"),
        "uploadedBy": "eeee3183-69ca-47e7-9826-00e9111f4efd",
        "lastModifiedTs": "2025-02-22T08:15:52.384006Z",
    },
    {
        "name": "file2.parquet",
        "location": "siloes/silo_id=snJIZE2z/file2.parquet",
        "size": Decimal("0"),
        "uploadedBy": "eeee3183-69ca-47e7-9826-00e9111f4efd",
        "lastModifiedTs": "2025-02-22T08:15:52.384006Z",
    },
    {
        "name": "file4.parquet",
        "location": "siloes/silo_id=snJIZE2z/file4.parquet",
        "size": Decimal("0"),
        "uploadedBy": "eeee3183-69ca-47e7-9826-00e9111f4efd",
        "lastModifiedTs": "2025-02-22T08:15:52.384006Z",
    },
]
