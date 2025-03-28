from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.credential import Credential


T = TypeVar("T", bound="CredentialsResponse")


@_attrs_define
class CredentialsResponse:
    """
    Attributes:
        workflow_name (str): The name of the workflow
        credentials (List['Credential']):
    """

    workflow_name: str
    credentials: List["Credential"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_name = self.workflow_name

        credentials = []
        for credentials_item_data in self.credentials:
            credentials_item = credentials_item_data.to_dict()
            credentials.append(credentials_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflow_name": workflow_name,
                "credentials": credentials,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.credential import Credential

        d = src_dict.copy()
        workflow_name = d.pop("workflow_name")

        credentials = []
        _credentials = d.pop("credentials")
        for credentials_item_data in _credentials:
            credentials_item = Credential.from_dict(credentials_item_data)

            credentials.append(credentials_item)

        credentials_response = cls(
            workflow_name=workflow_name,
            credentials=credentials,
        )

        credentials_response.additional_properties = d
        return credentials_response

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
