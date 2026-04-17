import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from dash import html, dcc
from soul_foods_visualiser import app


def find_component(layout, component_type, prop=None, value=None):
    """Recursively search a Dash layout tree for a component."""
    if isinstance(layout, component_type):
        if prop is None:
            return True
        return getattr(layout, prop, None) == value
    children = getattr(layout, "children", None)
    if children is None:
        return False
    if not isinstance(children, list):
        children = [children]
    return any(find_component(c, component_type, prop, value) for c in children)


def test_header_present():
    """The app layout must contain an H1 element."""
    assert find_component(app.layout, html.H1), "H1 header not found in layout"


def test_chart_present():
    """The app layout must contain a dcc.Graph visualisation."""
    assert find_component(app.layout, dcc.Graph), "dcc.Graph chart not found in layout"


def test_region_picker_present():
    """The app layout must contain a dcc.RadioItems region picker."""
    assert find_component(app.layout, dcc.RadioItems), "dcc.RadioItems region picker not found in layout"
