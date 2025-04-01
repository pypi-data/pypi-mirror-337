from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Annotated, Any, TypeVar, get_args, get_origin


if TYPE_CHECKING:
    from pydantic import BaseModel
    from pydantic.fields import FieldInfo


T = TypeVar("T", bound="BaseModel")


@dataclass
class ValidationConstraints:
    """Encapsulation of field validation constraints."""

    min_value: float | None = None
    """Minimum allowed value for numeric fields."""

    max_value: float | None = None
    """Maximum allowed value for numeric fields."""

    exclusive_min: bool = False
    """If True, the minimum value is exclusive (value must be greater than min_value)."""

    exclusive_max: bool = False
    """If True, the maximum value is exclusive (value must be less than max_value)."""

    multiple_of: float | None = None
    """If set, the value must be a multiple of this number."""

    min_length: int | None = None
    """Minimum length for strings or collections."""

    max_length: int | None = None
    """Maximum length for strings or collections."""

    pattern: str | None = None
    """Regular expression pattern that strings must match."""

    min_items: int | None = None
    """Minimum number of items for array/list types."""

    max_items: int | None = None
    """Maximum number of items for array/list types."""

    allowed_values: list[Any] | None = None
    """List of allowed values (for enums, literals, or constrained types)."""

    @classmethod
    def from_pydantic_field(cls, field_info: FieldInfo) -> ValidationConstraints:
        """Extract constraints directly from Pydantic field info."""
        constraints: dict[str, Any] = {}

        from annotated_types import Ge, Gt, Le, Lt, MaxLen, MinLen, MultipleOf

        for meta in field_info.metadata:
            match meta:
                case Gt():
                    constraints["min_value"] = meta.gt
                    constraints["exclusive_min"] = True
                case Ge():
                    constraints["min_value"] = meta.ge
                case Lt():
                    constraints["max_value"] = meta.lt
                    constraints["exclusive_max"] = True
                case Le():
                    constraints["max_value"] = meta.le
                case MultipleOf():
                    constraints["multiple_of"] = meta.multiple_of
                case MinLen():
                    constraints["min_length"] = meta.min_length
                case MaxLen():
                    constraints["max_length"] = meta.max_length
                # Easy to extend with more cases as needed

        return cls(**constraints)


@dataclass
class PyField[T]:
    """Generic representation of a field focused on type semantics."""

    name: str
    """The name of the field in the model."""

    raw_type: Any
    """The Python type annotation of the field."""

    parent_model: type[T] | None = None
    """The parent model class containing this field."""

    field_type: str | None = None
    """The field type, based on Annoated convention."""

    title: str | None = None
    """Display title for the field."""

    description: str | None = None
    """Detailed description of the field."""

    placeholder: str | None = None
    """Placeholder text to show when the field is empty."""

    examples: list[Any] | None = None
    """Example values for the field."""

    hidden: bool = False
    """Whether the field should be hidden from serialization or presentation."""

    readonly: bool = False
    """Whether the field is immutable after initialization."""

    deprecated: bool = False
    """Whether the field is marked as deprecated."""

    is_required: bool = True
    """Whether the field is required for validation."""

    default_value: Any = None
    """The default value for the field."""

    has_default: bool = False
    """Whether the field has a default value defined."""

    constraints: ValidationConstraints = field(default_factory=ValidationConstraints)
    """Validation constraints for the field."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata associated with the field."""

    @classmethod
    def from_pydantic(
        cls,
        name: str,
        field_info: FieldInfo,
        parent_model: type[BaseModel] | None = None,
    ) -> PyField:
        """Create a PyField from Pydantic field information."""
        raw_type = field_info.annotation
        field_type = None
        if get_origin(raw_type) == Annotated:  # Direct comparison with the actual type
            args = get_args(raw_type)
            raw_type = args[0]  # Actual type is first argument

            # Extract field_type from any dict arguments
            for arg in args[1:]:
                if isinstance(arg, dict) and "field_type" in arg:
                    field_type = arg["field_type"]
                    break

        # Check json_schema_extra as an alternative source for field_type
        if (
            field_type is None
            and field_info.json_schema_extra
            and (
                isinstance(field_info.json_schema_extra, dict)
                and "field_type" in field_info.json_schema_extra
            )
        ):
            field_type = field_info.json_schema_extra["field_type"]

        # Get required status (we still need model_json_schema for this)
        is_required = True  # Default to True
        if parent_model:
            schema = parent_model.model_json_schema()
            is_required = name in schema.get("required", [])

        from pydantic.fields import PydanticUndefined

        has_default = field_info.default is not PydanticUndefined
        default_value = field_info.default if has_default else None
        constraints = ValidationConstraints.from_pydantic_field(field_info)
        examples = field_info.examples

        # Use first example as placeholder if available
        placeholder = str(examples[0]) if examples and examples[0] is not None else None

        return cls(
            name=name,
            raw_type=raw_type,
            parent_model=parent_model,
            field_type=field_type,
            title=field_info.title or name.replace("_", " ").capitalize(),
            description=field_info.description,
            placeholder=placeholder,
            examples=examples,
            hidden=field_info.exclude is True,
            readonly=field_info.frozen is True,
            deprecated=field_info.deprecated is not None,
            is_required=is_required,
            default_value=default_value,
            has_default=has_default,
            constraints=constraints,
            metadata={},
        )
