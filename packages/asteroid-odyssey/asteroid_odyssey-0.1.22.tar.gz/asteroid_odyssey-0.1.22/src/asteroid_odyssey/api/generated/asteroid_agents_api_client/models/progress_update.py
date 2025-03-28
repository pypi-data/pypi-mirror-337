import datetime
from typing import Any, Dict, List, Type, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ProgressUpdate")


@_attrs_define
class ProgressUpdate:
    """
    Attributes:
        execution_id (UUID): The execution ID
        progress (str): The progress of the execution Example: Step 1 of 3.
        created_at (datetime.datetime): The date and time the progress was created
    """

    execution_id: UUID
    progress: str
    created_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        execution_id = str(self.execution_id)

        progress = self.progress

        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "execution_id": execution_id,
                "progress": progress,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        execution_id = UUID(d.pop("execution_id"))

        progress = d.pop("progress")

        created_at = isoparse(d.pop("created_at"))

        progress_update = cls(
            execution_id=execution_id,
            progress=progress,
            created_at=created_at,
        )

        progress_update.additional_properties = d
        return progress_update

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
