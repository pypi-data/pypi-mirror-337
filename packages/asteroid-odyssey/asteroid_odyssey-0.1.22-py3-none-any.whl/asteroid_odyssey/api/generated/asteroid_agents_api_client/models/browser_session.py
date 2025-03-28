from typing import Any, Dict, List, Type, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BrowserSession")


@_attrs_define
class BrowserSession:
    """
    Attributes:
        id (Union[Unset, UUID]): Browser session identifier.
        browser_name (Union[Unset, str]): Browser name (Anchor, Browserbase, etc.)
        execution_id (Union[Unset, UUID]): Execution ID.
        cdp_url (Union[Unset, str]): CDP URL.
        debugger_url (Union[Unset, str]): Debugger URL.
        session_id (Union[Unset, str]): Session ID.
        session_url (Union[Unset, str]): Session URL.
        recording_url (Union[Unset, str]): Recording URL.
    """

    id: Union[Unset, UUID] = UNSET
    browser_name: Union[Unset, str] = UNSET
    execution_id: Union[Unset, UUID] = UNSET
    cdp_url: Union[Unset, str] = UNSET
    debugger_url: Union[Unset, str] = UNSET
    session_id: Union[Unset, str] = UNSET
    session_url: Union[Unset, str] = UNSET
    recording_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        browser_name = self.browser_name

        execution_id: Union[Unset, str] = UNSET
        if not isinstance(self.execution_id, Unset):
            execution_id = str(self.execution_id)

        cdp_url = self.cdp_url

        debugger_url = self.debugger_url

        session_id = self.session_id

        session_url = self.session_url

        recording_url = self.recording_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if browser_name is not UNSET:
            field_dict["browser_name"] = browser_name
        if execution_id is not UNSET:
            field_dict["execution_id"] = execution_id
        if cdp_url is not UNSET:
            field_dict["cdp_url"] = cdp_url
        if debugger_url is not UNSET:
            field_dict["debugger_url"] = debugger_url
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if session_url is not UNSET:
            field_dict["session_url"] = session_url
        if recording_url is not UNSET:
            field_dict["recording_url"] = recording_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        browser_name = d.pop("browser_name", UNSET)

        _execution_id = d.pop("execution_id", UNSET)
        execution_id: Union[Unset, UUID]
        if isinstance(_execution_id, Unset):
            execution_id = UNSET
        else:
            execution_id = UUID(_execution_id)

        cdp_url = d.pop("cdp_url", UNSET)

        debugger_url = d.pop("debugger_url", UNSET)

        session_id = d.pop("session_id", UNSET)

        session_url = d.pop("session_url", UNSET)

        recording_url = d.pop("recording_url", UNSET)

        browser_session = cls(
            id=id,
            browser_name=browser_name,
            execution_id=execution_id,
            cdp_url=cdp_url,
            debugger_url=debugger_url,
            session_id=session_id,
            session_url=session_url,
            recording_url=recording_url,
        )

        browser_session.additional_properties = d
        return browser_session

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
