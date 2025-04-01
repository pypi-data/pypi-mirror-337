# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class DashPerspectiveComponent(Component):
    """A DashPerspectiveComponent component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- config (dict; optional):
    The config used in the component.

- data (list; optional):
    The data being rendered in the component."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_perspective_component'
    _type = 'DashPerspectiveComponent'

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        data: typing.Optional[typing.Sequence] = None,
        config: typing.Optional[dict] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'config', 'data', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'config', 'data', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashPerspectiveComponent, self).__init__(**args)
