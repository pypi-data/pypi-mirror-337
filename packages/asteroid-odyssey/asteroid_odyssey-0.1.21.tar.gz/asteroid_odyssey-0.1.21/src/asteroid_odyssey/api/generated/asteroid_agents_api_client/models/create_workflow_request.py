from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_workflow_request_provider import CreateWorkflowRequestProvider
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_workflow_request_fields import CreateWorkflowRequestFields
    from ..models.result_schema import ResultSchema


T = TypeVar("T", bound="CreateWorkflowRequest")


@_attrs_define
class CreateWorkflowRequest:
    """
    Attributes:
        name (str): The name of the workflow. Example: My workflow.
        result_schema (ResultSchema): A JSON Schema that defines the expected structure and validation rules for
            workflow results. Example: {'$schema': 'https://json-schema.org/draft/2020-12/schema#', 'type': 'object',
            'required': ['name', 'age', 'skills'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'age':
            {'type': 'integer', 'minimum': 18, 'maximum': 120}, 'email': {'type': 'string', 'format': 'email'}, 'skills':
            {'type': 'array', 'items': {'type': 'string'}, 'minItems': 1}}}.
        fields (CreateWorkflowRequestFields): JSON object containing static workflow configuration (e.g. a
            prompt_template). Example: {'model': 'gpt-4o', 'version': '2024-02-01'}.
        prompts (List[str]): The prompts for the workflow. They can have variables in them. They will be merged with the
            dynamic data passed when the workflow is executed. Example: ['Your name is {{.name}}, you speak {{.language}}',
            'Your task is {{.task}}'].
        provider (CreateWorkflowRequestProvider): The Language Model Provider for the Workflow Example: openai.
        user_id (Union[Unset, UUID]): The ID of the user that this workflow belongs to. Example:
            123e4567-e89b-12d3-a456-426614174000.
    """

    name: str
    result_schema: "ResultSchema"
    fields: "CreateWorkflowRequestFields"
    prompts: List[str]
    provider: CreateWorkflowRequestProvider
    user_id: Union[Unset, UUID] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        result_schema = self.result_schema.to_dict()

        fields = self.fields.to_dict()

        prompts = self.prompts

        provider = self.provider.value

        user_id: Union[Unset, str] = UNSET
        if not isinstance(self.user_id, Unset):
            user_id = str(self.user_id)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "result_schema": result_schema,
                "fields": fields,
                "prompts": prompts,
                "provider": provider,
            }
        )
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_workflow_request_fields import CreateWorkflowRequestFields
        from ..models.result_schema import ResultSchema

        d = src_dict.copy()
        name = d.pop("name")

        result_schema = ResultSchema.from_dict(d.pop("result_schema"))

        fields = CreateWorkflowRequestFields.from_dict(d.pop("fields"))

        prompts = cast(List[str], d.pop("prompts"))

        provider = CreateWorkflowRequestProvider(d.pop("provider"))

        _user_id = d.pop("user_id", UNSET)
        user_id: Union[Unset, UUID]
        if isinstance(_user_id, Unset):
            user_id = UNSET
        else:
            user_id = UUID(_user_id)

        create_workflow_request = cls(
            name=name,
            result_schema=result_schema,
            fields=fields,
            prompts=prompts,
            provider=provider,
            user_id=user_id,
        )

        create_workflow_request.additional_properties = d
        return create_workflow_request

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
