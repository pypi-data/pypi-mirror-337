import datetime
from typing import Any, Dict, List, Type, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="File")


@_attrs_define
class File:
    """
    Attributes:
        id (UUID): Unique file identifier. Example: 1.
        execution_id (UUID): Execution ID associated with the file. Example: 123e4567-e89b-12d3-a456-426614174000.
        file_path (str): Full GCS object path (e.g., "2023-10-21_14-05-01/1697892305-screenshot.png"). Example:
            2023-10-21_14-05-01/1697892305-screenshot.png.
        file_ext (str): File extension. Example: png.
        file_name (str): File name. Example: 1697892305-screenshot.png.
        file_size (int): Size of the file in bytes. Example: 2048.
        mime_type (str): MIME type of the file. Example: image/png.
        created_at (datetime.datetime): Timestamp when the file record was created. Example: 2023-10-21T14:05:01Z.
        signed_url (str): Signed URL to download the file. Example: https://storage.googleapis.com/asteroid-
            files/123e4567-e89b-12d3-a456-426614174000/2023-10-21_14-05-01/1697892305-screenshot.png.
    """

    id: UUID
    execution_id: UUID
    file_path: str
    file_ext: str
    file_name: str
    file_size: int
    mime_type: str
    created_at: datetime.datetime
    signed_url: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = str(self.id)

        execution_id = str(self.execution_id)

        file_path = self.file_path

        file_ext = self.file_ext

        file_name = self.file_name

        file_size = self.file_size

        mime_type = self.mime_type

        created_at = self.created_at.isoformat()

        signed_url = self.signed_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "execution_id": execution_id,
                "file_path": file_path,
                "file_ext": file_ext,
                "file_name": file_name,
                "file_size": file_size,
                "mime_type": mime_type,
                "created_at": created_at,
                "signed_url": signed_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = UUID(d.pop("id"))

        execution_id = UUID(d.pop("execution_id"))

        file_path = d.pop("file_path")

        file_ext = d.pop("file_ext")

        file_name = d.pop("file_name")

        file_size = d.pop("file_size")

        mime_type = d.pop("mime_type")

        created_at = isoparse(d.pop("created_at"))

        signed_url = d.pop("signed_url")

        file = cls(
            id=id,
            execution_id=execution_id,
            file_path=file_path,
            file_ext=file_ext,
            file_name=file_name,
            file_size=file_size,
            mime_type=mime_type,
            created_at=created_at,
            signed_url=signed_url,
        )

        file.additional_properties = d
        return file

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
