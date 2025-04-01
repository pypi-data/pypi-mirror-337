# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Downloader(Component):
    """A Downloader component.
Downloader is a React component based on StreamSaver.
*
The StreamSaver.js project provides a customizable way to access and download
an online stream. This is the recommended downloader for practical uses. It has
the optimized performance for triggering multiple downloading events.

Keyword arguments:

- id (string; default PropTypes.string):
    The ID used to identify this component in Dash callbacks.

- allow_cross_origin (boolean; default False):
    A flag determineing whether the cross-origin downloading link can
    be used.  If the data to be downloaded is from a cross-domain
    site, need to configure this value as `True` while the remote site
    needs to configure the headers Access-Control-Allow-Origin.

- headers (dict; default PropTypes.object):
    The extra headers to be used when submitting the request of the
    downloading event.  This property may need to be configured when
    the downloading event needs to add authentication information.

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

- mitm (string; default undefined):
    The MITM-IFrame used for maintaining the status of the downloader.
    It prevents the downloader to be closed when the broswer is idle.
    See details here:
    https://github.com/jimmywarting/StreamSaver.js/blob/master/README.md#best-practice
    If not specified, will use the default MITM service of
    StreamSaver.js, which needs the internet.

- status (dict; default PropTypes.exact({    /**     * The status code of the event. If the event is successful, this value should     * be "success" once the downloading event is finalized.     */    code: PropTypes.oneOf([      "success",      "error-connect",      "error-config",      "error-io",      "error-unknown",    ]),    /**     * The HTTP code from the response. If the event is successful, this value should     * be in the range of 200-299.     */    http_code: PropTypes.number,  })):
    The status code when a downloading event is finalized.  If
    multiple downloading events are triggered by the same downloader,
    the later event will overwrite the status from the former events.

    `status` is a dict with keys:

    - code (string; required):
        The status code of the event. If the event is successful, this
        value should be \"success\" once the downloading event is
        finalized.

    - http_code (number; required):
        The HTTP code from the response. If the event is successful,
        this value should be in the range of 200-299.

- url (dict; default ''):
    The URL used to access the data to be downloaded.  Each time when
    this value is set, a download event will be triggered. After
    triggering the download event, this value will be reset by a blank
    string.

    `url` is a string | dict with keys:

    - url (string; required):
        The URL used to access the data to be downloaded.

    - file_name_fallback (string; required):
        A maunally configured file name. If this file name is
        configured, it will be used when the file name cannot be
        parsed in the headers. This configuration is useful when the
        URL is from a cross-origin site."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_file_cache'
    _type = 'Downloader'
    Url = TypedDict(
        "Url",
            {
            "url": str,
            "file_name_fallback": str
        }
    )

    Status = TypedDict(
        "Status",
            {
            "code": str,
            "http_code": typing.Union[int, float, numbers.Number]
        }
    )

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
        url: typing.Optional[typing.Union[str, "Url"]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        headers: typing.Optional[dict] = None,
        allow_cross_origin: typing.Optional[bool] = None,
        status: typing.Optional["Status"] = None,
        mitm: typing.Optional[str] = None,
        loading_state: typing.Optional[typing.Union["LoadingState"]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'allow_cross_origin', 'headers', 'loading_state', 'mitm', 'status', 'url']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allow_cross_origin', 'headers', 'loading_state', 'mitm', 'status', 'url']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Downloader, self).__init__(**args)
