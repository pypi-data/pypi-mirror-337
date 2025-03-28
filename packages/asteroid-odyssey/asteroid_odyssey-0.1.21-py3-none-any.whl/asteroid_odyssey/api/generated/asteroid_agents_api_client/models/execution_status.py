import datetime
from typing import Any, Dict, List, Type, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.status import Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExecutionStatus")


@_attrs_define
class ExecutionStatus:
    """
    Attributes:
        execution_id (UUID): Execution ID.
        status (Status): Status of the execution.
        created_at (datetime.datetime): The date and time the execution status was created.
        reason (Union[Unset, str]): Reason for the status.
    """

    execution_id: UUID
    status: Status
    created_at: datetime.datetime
    reason: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        execution_id = str(self.execution_id)

        status = self.status.value

        created_at = self.created_at.isoformat()

        reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "execution_id": execution_id,
                "status": status,
                "created_at": created_at,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        execution_id = UUID(d.pop("execution_id"))

        status = Status(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        reason = d.pop("reason", UNSET)

        execution_status = cls(
            execution_id=execution_id,
            status=status,
            created_at=created_at,
            reason=reason,
        )

        execution_status.additional_properties = d
        return execution_status

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
