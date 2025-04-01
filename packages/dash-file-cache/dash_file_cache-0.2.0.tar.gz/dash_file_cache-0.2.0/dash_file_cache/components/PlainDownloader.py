# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class PlainDownloader(Component):
    """A PlainDownloader component.
PlainDownloader is a plain and native React component.
*
This component is implemented by a temporarily created magic link referring to a
given URL.
*
Since the implementation of this PlainDownloader is simply based on the HTML `<a>`
tag, the request headers and authentication of this downloader is not customizable.

Keyword arguments:

- id (string; default PropTypes.string):
    The ID used to identify this component in Dash callbacks.

- loading_state (dict; default PropTypes.shape({    /**     * Determines if the component is loading or not     */    is_loading: PropTypes.bool,    /**     * Holds which property is loading     */    prop_name: PropTypes.string,    /**     * Holds the name of the component that is loading     */    component_name: PropTypes.string,  })):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:


      Or dict with keys:

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

    - component_name (string; optional):
        Holds the name of the component that is loading.

- url (string; default ''):
    The URL used to access the data to be downloaded.  Each time when
    this value is set, a download event will be triggered. After
    triggering the download event, this value will be reset by a blank
    string."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_file_cache'
    _type = 'PlainDownloader'
    LoadingState = TypedDict(
        "LoadingState",
            {
            "is_loading": NotRequired[bool],
            "prop_name": NotRequired[str],
            "component_name": NotRequired[str]
        }
    )

    @_explicitize_args
    def __init__(
        self,
        url: typing.Optional[str] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        loading_state: typing.Optional[typing.Union["LoadingState"]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'loading_state', 'url']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'loading_state', 'url']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(PlainDownloader, self).__init__(**args)
