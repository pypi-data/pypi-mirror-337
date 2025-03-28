import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execution_dynamic_data import ExecutionDynamicData
    from ..models.execution_result import ExecutionResult
    from ..models.execution_status import ExecutionStatus


T = TypeVar("T", bound="Execution")


@_attrs_define
class Execution:
    """
    Attributes:
        id (UUID): Execution identifier.
        run_id (UUID): Run ID.
        workflow_id (UUID): Workflow ID.
        result (ExecutionResult): The result of the execution.
        created_at (datetime.datetime): The date and time the execution was created.
        dynamic_data (Union[Unset, ExecutionDynamicData]): Dynamic data to be merged into the saved workflow
            configuration. Example: {'name': 'Alice', 'model': 'gpt-4o'}.
        status (Union[Unset, ExecutionStatus]):
        error (Union[Unset, str]): The error that occurred during the execution.
    """

    id: UUID
    run_id: UUID
    workflow_id: UUID
    result: "ExecutionResult"
    created_at: datetime.datetime
    dynamic_data: Union[Unset, "ExecutionDynamicData"] = UNSET
    status: Union[Unset, "ExecutionStatus"] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = str(self.id)

        run_id = str(self.run_id)

        workflow_id = str(self.workflow_id)

        result = self.result.to_dict()

        created_at = self.created_at.isoformat()

        dynamic_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dynamic_data, Unset):
            dynamic_data = self.dynamic_data.to_dict()

        status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "run_id": run_id,
                "workflow_id": workflow_id,
                "result": result,
                "created_at": created_at,
            }
        )
        if dynamic_data is not UNSET:
            field_dict["dynamic_data"] = dynamic_data
        if status is not UNSET:
            field_dict["status"] = status
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.execution_dynamic_data import ExecutionDynamicData
        from ..models.execution_result import ExecutionResult
        from ..models.execution_status import ExecutionStatus

        d = src_dict.copy()
        id = UUID(d.pop("id"))

        run_id = UUID(d.pop("run_id"))

        workflow_id = UUID(d.pop("workflow_id"))

        result = ExecutionResult.from_dict(d.pop("result"))

        created_at = isoparse(d.pop("created_at"))

        _dynamic_data = d.pop("dynamic_data", UNSET)
        dynamic_data: Union[Unset, ExecutionDynamicData]
        if isinstance(_dynamic_data, Unset):
            dynamic_data = UNSET
        else:
            dynamic_data = ExecutionDynamicData.from_dict(_dynamic_data)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExecutionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExecutionStatus.from_dict(_status)

        error = d.pop("error", UNSET)

        execution = cls(
            id=id,
            run_id=run_id,
            workflow_id=workflow_id,
            result=result,
            created_at=created_at,
            dynamic_data=dynamic_data,
            status=status,
            error=error,
        )

        execution.additional_properties = d
        return execution

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
