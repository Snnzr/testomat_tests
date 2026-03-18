from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProjectAttributes:
    title: str | None = None
    status: str | None = None
    tests_count: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectAttributes":
        return cls(
            title=data.get("title"),
            status=data.get("status"),
            tests_count=data.get("tests_count"),
            extra={
                key: value
                for key, value in data.items()
                if key not in {"title", "status", "tests_count"}
            },
        )


@dataclass(frozen=True)
class Project:
    id: str
    type: str
    title: str | None = None
    status: str | None = None
    tests_count: int | None = None
    attributes: ProjectAttributes | None = None
    relationships: dict[str, Any] = field(default_factory=dict)
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Project":
        attributes_data = data.get("attributes") or {}
        attributes = ProjectAttributes.from_dict(attributes_data)
        return cls(
            id=str(data.get("id")),
            type=data.get("type", "project"),
            title=attributes.title or data.get("title"),
            status=attributes.status or data.get("status"),
            tests_count=attributes.tests_count,
            attributes=attributes,
            relationships=data.get("relationships") or {},
            extra={
                key: value
                for key, value in data.items()
                if key not in {"id", "type", "attributes", "relationships"}
            },
        )


@dataclass(frozen=True)
class ProjectsResponse:
    data: list[Project]
    meta: dict[str, Any] = field(default_factory=dict)
    links: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProjectsResponse":
        return cls(
            data=[Project.from_dict(item) for item in payload.get("data", [])],
            meta=payload.get("meta") or {},
            links=payload.get("links") or {},
        )

    def __iter__(self):
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> Project:
        return self.data[index]
