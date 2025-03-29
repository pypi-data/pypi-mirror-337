# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class ResizableNode(Component):
    """A ResizableNode component.


Keyword arguments:

- data (dict; required)

    `data` is a dict with keys:

    - label (boolean | number | string | dict | list; optional)

    - handles (list of dicts; required)

        `handles` is a list of dicts with keys:

        - id (string; required)

        - type (string; required)

        - position (string; required)

        - style (dict; optional)

        - isConnectable (boolean; optional)

        - isConnectableStart (boolean; optional)

        - isConnectableEnd (boolean; optional)

        - onConnect (optional)

        - isValidConnection (optional)

- selected (boolean; default False)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'ResizableNode'
    DataHandles = TypedDict(
        "DataHandles",
            {
            "id": str,
            "type": str,
            "position": str,
            "style": NotRequired[dict],
            "isConnectable": NotRequired[bool],
            "isConnectableStart": NotRequired[bool],
            "isConnectableEnd": NotRequired[bool],
            "onConnect": NotRequired[typing.Any],
            "isValidConnection": NotRequired[typing.Any]
        }
    )

    Data = TypedDict(
        "Data",
            {
            "label": NotRequired[typing.Any],
            "handles": typing.Sequence["DataHandles"]
        }
    )

    @_explicitize_args
    def __init__(
        self,
        data: typing.Optional["Data"] = None,
        selected: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['data', 'selected']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['data', 'selected']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ResizableNode, self).__init__(**args)
