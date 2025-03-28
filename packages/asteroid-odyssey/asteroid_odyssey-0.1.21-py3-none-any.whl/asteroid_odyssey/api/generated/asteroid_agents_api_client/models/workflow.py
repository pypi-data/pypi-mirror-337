import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.result_schema import ResultSchema
    from ..models.workflow_fields import WorkflowFields


T = TypeVar("T", bound="Workflow")


@_attrs_define
class Workflow:
    """
    Attributes:
        id (UUID): Workflow identifier.
        user_id (UUID): The ID of the user who created the workflow. Example: 123e4567-e89b-12d3-a456-426614174000.
        result_schema (ResultSchema): A JSON Schema that defines the expected structure and validation rules for
            workflow results. Example: {'$schema': 'https://json-schema.org/draft/2020-12/schema#', 'type': 'object',
            'required': ['name', 'age', 'skills'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'age':
            {'type': 'integer', 'minimum': 18, 'maximum': 120}, 'email': {'type': 'string', 'format': 'email'}, 'skills':
            {'type': 'array', 'items': {'type': 'string'}, 'minItems': 1}}}.
        agent_id (UUID): Identifier of the associated agent.
        name (str): Workflow name.
        fields (WorkflowFields): Workflow configuration. Example: {'model': 'gpt-4o', 'version': '2024-02-01'}.
        prompts (List[str]): The prompts for the workflow. They can have variables in them. They will be merged with the
            dynamic data passed when the workflow is executed. Example: ['Your name is {{.name}}, you speak {{.language}}',
            'Your task is {{.task}}'].
        created_at (Union[Unset, datetime.datetime]): The date and time the workflow was created.
        prompt_variables (Union[Unset, List[str]]): The variables in the prompts. Example: ['name', 'language', 'task'].
    """

    id: UUID
    user_id: UUID
    result_schema: "ResultSchema"
    agent_id: UUID
    name: str
    fields: "WorkflowFields"
    prompts: List[str]
    created_at: Union[Unset, datetime.datetime] = UNSET
    prompt_variables: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = str(self.id)

        user_id = str(self.user_id)

        result_schema = self.result_schema.to_dict()

        agent_id = str(self.agent_id)

        name = self.name

        fields = self.fields.to_dict()

        prompts = self.prompts

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        prompt_variables: Union[Unset, List[str]] = UNSET
        if not isinstance(self.prompt_variables, Unset):
            prompt_variables = self.prompt_variables

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_id": user_id,
                "result_schema": result_schema,
                "agent_id": agent_id,
                "name": name,
                "fields": fields,
                "prompts": prompts,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if prompt_variables is not UNSET:
            field_dict["prompt_variables"] = prompt_variables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.result_schema import ResultSchema
        from ..models.workflow_fields import WorkflowFields

        d = src_dict.copy()
        id = UUID(d.pop("id"))

        user_id = UUID(d.pop("user_id"))

        result_schema = ResultSchema.from_dict(d.pop("result_schema"))

        agent_id = UUID(d.pop("agent_id"))

        name = d.pop("name")

        fields = WorkflowFields.from_dict(d.pop("fields"))

        prompts = cast(List[str], d.pop("prompts"))

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        prompt_variables = cast(List[str], d.pop("prompt_variables", UNSET))

        workflow = cls(
            id=id,
            user_id=user_id,
            result_schema=result_schema,
            agent_id=agent_id,
            name=name,
            fields=fields,
            prompts=prompts,
            created_at=created_at,
            prompt_variables=prompt_variables,
        )

        workflow.additional_properties = d
        return workflow

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
