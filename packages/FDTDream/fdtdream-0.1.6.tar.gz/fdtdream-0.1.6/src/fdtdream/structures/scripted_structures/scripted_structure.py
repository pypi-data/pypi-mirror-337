from abc import ABC
from copy import copy
from typing import TypeVar, Type, Self, Any
from ...resources.errors import FDTDreamParameterNotFound

from ..structure import Structure

T = TypeVar("T")


class ScriptedStructure(Structure, ABC):

    # region Class Body

    _name: str

    # Positional
    _x: float
    _y: float
    _z: float
    _use_relative_coordinates: bool

    # Rotational
    _first_axis: str
    _second_axis: str
    _third_axis: str
    _rotation_1: float
    _rotation_2: float
    _rotation_3: float

    # Material
    _material: str
    _index: str
    _index_units: str
    _mesh_order: int
    _grid_attribute_name: str | None

    __slots__ = ["_name", "_x", "_y", "_z", "_use_relative_coordinates",
                 "_first_axis", "_second_axis", "_third_axis", "_rotation_1", "_rotation_2", "_rotation_3",
                 "_material", "_index", "_index_units", "_mesh_order", "_grid_attribute_name",
                 "_closest_parent"]

    # endregion Class Body

    # region Dev. Methods

    def _add_parent(self, parent) -> None:
        """Adds a group type object to the scripted structure and updates the parent."""
        self._parents.append(parent)
        self._closest_parent = parent
        parent._structures.append(self)
        parent._update()

    def _remove_parent(self):
        """Removes the scripted structure from the parent group and updates the parent group."""
        self._parents.remove(self._closest_parent)
        closest_parent = self._closest_parent
        self._closest_parent = None
        closest_parent._structures.remove(self)
        closest_parent._update()

    def _initialize_variables(self) -> None:
        """Initializes default attributes common for all structure types."""

        self._closest_parent = None
        self._use_relative_coordinates = True
        self._x, self._y, self._z = 0, 0, 0
        self._first_axis, self._second_axis, self._third_axis = "none", "none", "none"
        self._rotation_1, self._rotation_2, self._rotation_3 = 0, 0, 0
        self._material = "<Object defined dielectric>"
        self._index = "1.4"
        self._grid_attribute_name = None

    def _get(self, parameter: str, parameter_type: Type[T]) -> T:
        return getattr(self, "_" + parameter.replace(" ", "_"))

    def _set(self, parameter: str, value: Type[T]) -> T:

        # Correctly format
        parameter = f"_{parameter.replace(' ', '_')}"

        # Check if parameter exists
        if parameter not in ScriptedStructure.__slots__ + self.__slots__:
            raise FDTDreamParameterNotFound(f"Parameter {parameter} is not a valid parameter for class "
                                            f"{self.__class__.__name__}")

        setattr(self, parameter, value)

        # Update the script of the parent object if one has been assigned.
        for parent in self._parents:
            parent._update()  # type: ignore

        return value

    # endregion Dev. Methods

    # region User Methods

    def copy(self, name: str, **kwargs: Any) -> Self:

        # Create a copy of the object.
        copied = copy(self)

        # Remove the reference to the parent group from the copy (to avoid unneccesary update() calls).
        closest_parent = self._closest_parent
        copied._closest_parent = None

        # Copy over the settings modules.
        copied.settings = self.settings._copy(copied)

        # Apply kwargs
        copied._process_kwargs(copied=True, **kwargs)

        # Reassign the reference to the parent group.
        if closest_parent is not None:
            copied._add_parent(closest_parent)

        return copied

    # endregion User Methods
