from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResultSchema")


@_attrs_define
class ResultSchema:
    """A JSON Schema that defines the expected structure and validation rules for workflow results.

    Example:
        {'$schema': 'https://json-schema.org/draft/2020-12/schema#', 'type': 'object', 'required': ['name', 'age',
            'skills'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'age': {'type': 'integer', 'minimum': 18,
            'maximum': 120}, 'email': {'type': 'string', 'format': 'email'}, 'skills': {'type': 'array', 'items': {'type':
            'string'}, 'minItems': 1}}}

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        result_schema = cls()

        result_schema.additional_properties = d
        return result_schema

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
