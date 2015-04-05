from __future__ import unicode_literals, absolute_import
from bokeh.models import (
    ColumnDataSource,
    Line,
    Range1d,
    Plot,
    Patches,
    HoverTool,
    TapTool,
)
from bokeh.models import Text, Rect, Triangle
from bokeh.models import LinearAxis, SingleIntervalTicker
from bokeh.models.widgets import VBox, HBox

from .chart_constants import (
    PLOT_FORMATS, ORANGE, BLUE, DARK_GRAY, FONT, AXIS_FORMATS, ORANGE_SHADOW
)


def construct_map(source):
    assert isinstance(source, ColumnDataSource), "Require ColumnDataSource"
    # Plot and axes
    x_start, x_end = (-20, 60)
    y_start, y_end = (-40, 40)
    xdr = Range1d(x_start, x_end)
    ydr = Range1d(y_start, y_end)

    aspect_ratio = (x_end - x_start) / (y_end - y_start)
    plot_height = 600
    plot_width = int(plot_height * aspect_ratio)
    plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=plot_width,
        plot_height=plot_height,
        **PLOT_FORMATS
    )

    borders = Patches(
        xs='xs', ys='ys',
        fill_color='color_for_active_year', fill_alpha=1,
        line_color="#FFFFFF", line_width=1,
    )
    selected_borders = Patches(
        xs='xs', ys='ys',
        fill_color='color_for_active_year', fill_alpha=1,
        line_color=ORANGE, line_width=5,
    )

    plot.add_glyph(source, borders, selection_glyph=selected_borders, nonselection_glyph=borders)  # nopep8
    plot.add_tools(HoverTool(tooltips="@active_year<br />@name<br />@active_year_value"))  # nopep8
    plot.add_tools(TapTool())
    return plot


def construct_text_box(source, bar_color=BLUE):

    # Plot and axes
    xdr = Range1d(0, 220)
    ydr = Range1d(0, 80)

    plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=250,
        plot_height=80,
        min_border=0,
        **PLOT_FORMATS
    )
    font_props_lg = dict(
        text_color=DARK_GRAY,
        text_font=FONT,
        text_font_style="bold",
        text_font_size='25pt',
    )
    font_props_sm = dict(
        text_color=DARK_GRAY,
        text_font=FONT,
        text_font_style="normal",
        text_font_size='10pt',
    )
    # Add the writing
    percent = Text(x=0, y=0, text='active_year_value', **font_props_lg)
    percent_sign = Text(x=54, y=0, text=['%'], **font_props_lg)
    line_one = Text(x=85, y=20, text=['of people had'], **font_props_sm)
    line_two_p1 = Text(x=85, y=5, text=['access in'], **font_props_sm)
    line_two_p2 = Text(x=131, y=5, text='active_year', **font_props_sm)
    plot.add_glyph(source, percent)
    plot.add_glyph(percent_sign)
    plot.add_glyph(line_one)
    plot.add_glyph(line_two_p1)
    plot.add_glyph(source, line_two_p2)

    # Add the blue bar
    rect = Rect(x=75, y=55, width=150, height=5, fill_color=bar_color, line_color=None)  # nopep8
    plot.add_glyph(rect)

    # Add the orange box with year
    shadow = Triangle(x=150, y=65, size=25, fill_color=ORANGE_SHADOW, line_color=None)  # nopep8
    plot.add_glyph(shadow)
    box = Rect(x=200, y=60, width=100, height=40, fill_color=ORANGE, line_color=None)  # nopep8
    plot.add_glyph(box)
    year = Text(x=160, y=45, text='active_year', text_font_size='18pt', text_color="#FFFFF", text_font_style="bold")  # nopep8
    plot.add_glyph(source, year)

    return plot


def construct_line_single(source, line_color=BLUE):
    xdr = Range1d(1990, 2013)
    ydr = Range1d(0, 100)
    line_plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=250,
        plot_height=250,
        min_border_right=10,
        **PLOT_FORMATS
    )
    xaxis = LinearAxis(SingleIntervalTicker(interval=50), **AXIS_FORMATS)
    yaxis = LinearAxis(SingleIntervalTicker(interval=10), **AXIS_FORMATS)
    line_plot.add_layout(xaxis, 'left')
    line_plot.add_layout(yaxis, 'below')

    line = Line(
        x='year', y='watsan',
        line_width=5, line_cap="round",
        line_color=source.data['color_for_active_year'][0],
    )
    line_plot.add_glyph(source.data['line_source'][0], line)

    return line_plot


def layout_components(map_plot, line_plot, text_box):
    detail = VBox(children=[text_box, line_plot])
    mapbox = VBox(children=[map_plot])
    composed = HBox(children=[mapbox, detail])
    return composed


"""
def construct_line(data=None, source=None, palette=WATER_COLOR_RANGE):
    year_range = range(1990, 2013)

    if data is None:
        data = get_sanitation_data_with_countries()
    data = data[data.name == 'South Africa']
    data = data[year_range].transpose()
    data['country'] = data.iloc[:,0]

    if source is None:
        source = ColumnDataSource(data)

    xdr = Range1d(1990, 2013)
    ydr = Range1d(0, 100)
    line_plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=250,
        plot_height=250,
        min_border_right=10,
        **PLOT_FORMATS
    )
    xaxis = LinearAxis(SingleIntervalTicker(interval=50), **AXIS_FORMATS)
    yaxis = LinearAxis(SingleIntervalTicker(interval=10), **AXIS_FORMATS)
    line_plot.add_layout(xaxis, 'left')
    line_plot.add_layout(yaxis, 'below')

    line = Line(
        x='index', y='country',
        line_width=5, line_cap="round",
        line_color=palette[int(data['country'].mean() / 10)]
    )
    line_plot.add_glyph(source, line)

    return line_plot
"""