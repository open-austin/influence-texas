from django.shortcuts import reverse
from django.test import Client, RequestFactory
from django.urls import resolve


def response_from_view(view_name, args=None, kwargs=None):
    """Return http response from a view with the given `view_name`."""
    args = () if args is None else args
    kwargs = {} if kwargs is None else kwargs

    url = reverse(view_name, args=args, kwargs=kwargs)

    factory = RequestFactory()
    request = factory.get(url)

    view = resolve(url).func

    response = view(request, *args, **kwargs)
    response.client = Client()
    return response


def render_view(view_name, encoding='utf8', args=None, kwargs=None):
    """Return html string from a view with the given `view_name`."""
    response = response_from_view(view_name, args=args, kwargs=kwargs)
    # TemplateViews have a render method and need to be rendered before accessing content.
    if hasattr(response, 'render'):
        response.render()

    return response.content.decode(encoding)

