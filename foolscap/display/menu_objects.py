from datetime import datetime
from collections import OrderedDict

from foolscap.display.render_composite import Widget


default_settings = {
    'title': {
        'name': 'title',
        'size': 20,
        'align': 'left'
    },
    'description': {
        'name': 'description',
        'size': 40,
        'align': 'left'
    },
    'created': {
        'name': 'created',
        'size': 10,
        'align': 'centre'
    },
    'views': {
        'name': 'views',
        'size': 4,
        'align': 'centre'
    },
    'more': {
        'name': 'more',
        'size': 2,
        'align': 'centre'
    }
}

tag_settings = {
    'title': {
        'name': 'title',
        'size': 32,
        'align': 'centre'
    },
    'description': {
        'name': 'description',
        'size': 32,
        'align': 'centre'
    },
    'more': {
        'name': 'more',
        'size': 2,
        'align': 'centre'
    }
}


class ColumnType:
    """Prototypical column."""

    name = 'title'

    def clone(self, **attrs):
        obj = self.__class__()
        obj.__dict__.update(attrs)
        return obj


class ColumnRegistry:

    def __init__(self):
        self._objects = OrderedDict()

    def get_type(self, name):
        """Get a single item from the registry."""
        return self._objects[name]

    def get_column_names(self):
        """Get all objects."""
        for obj in self._objects:
            yield obj

    def register_object(self, name, obj):
        """Register an object."""
        self._objects[name] = obj

    def unregister_object(self, name):
        """Unregister an object."""
        del self._objects[name]


def display_text(x):
    """Converts x to str in order to display."""
    if isinstance(x, datetime):
        return x.strftime("%d-%b-%Y")
    else:
        return str(x)


class Columns(Widget):
    """ Responsible for drawing the information available for each note.
    """
    configuration = ['more', 'title', 'description', 'created']
    default_display = '-'

    def __init__(self, menu_type, menu):
        if menu_type == 'tags':
            self.settings = tag_settings
            self.configuration = ['more', 'title', 'description']
        else:
            self.settings = default_settings
        self.construct_columns(self.settings)

    def construct_columns(self, settings):
        """Construct concrete columns."""
        self.registry = ColumnRegistry()
        prototype = ColumnType()
        for column_name in self.configuration:
            setting = self.settings[column_name]
            column = prototype.clone(**setting)
            self.registry.register_object(column_name, column)

    def left_align(self, text, size):
        """Left align the column contents."""
        text_size = len(text)
        if text_size > size:
            text = text[:size]
            text_size = len(text)
        text = text + (' ' * (size - text_size + 1))
        return text

    def centre_align(self, text, size):
        """Centre align the column contents."""
        text_size = len(text)
        buffer_size = (size) - (text_size) + 1
        column_buffer = (int(buffer_size / 2)) * ' '

        return column_buffer + text + column_buffer

    def draw(self, item, line, line_colour):
        align = {'left': self.left_align,
                 'centre': self.centre_align}

        left_x = 2
        for column in self.registry.get_column_names():
            cln_setting = self.registry.get_type(column)
            size = cln_setting.size
            if left_x + size + 5 < self.max_x:
                if hasattr(item, column):
                    pline = getattr(item, column)
                    pline = display_text(pline)
                else:
                    pline = self.default_display

                alignment = cln_setting.align
                pline = align[alignment](pline, size)
                self.screen.addstr(line, left_x, pline, line_colour)
                left_x += size + 2
                self.screen.addstr(line, left_x, '|', line_colour)
                left_x += 2
            else:
                break


class MenuItem:

    def __init__(self, **config):

        self.title = config.get('title')
        try:
            if isinstance(config['model'].tags, dict):
                data = config['model'].tags[self.title]
            else:
                data = config['model'].notes[self.title]
        except AttributeError:
            data = config['model']
        for key in data:
            setattr(self, key, data[key])

        self.more = '   '
        sub_headings = data.get('sub_headings')
        if sub_headings:
            self.expand = False
            self.more = '(+)'
            self.create_sub_items(sub_headings)

    def toggle_drop_down(self):
        if self.sub_items:
            self._toggle_dd()

    def _toggle_dd(self):
        if self.expand:
            self.expand = False
            self.more = '(+)'
        else:
            self.expand = True
            self.more = '<->'

    def create_sub_items(self, items):
        self.sub_items = []
        for index, item in enumerate(items):
            sub_item = {'title': item[0], 'model': {'description': item[1]}}
            if len(item) > 3:
                sub_item['model']['start_index'] = item[2]
                sub_item['model']['end_index'] = item[3]
            sub_item = MenuItem(**sub_item)
            sub_item.title = '──{}'.format(sub_item.title)
            if index == len(items) - 1:
                sub_item.more = ' └─'
                sub_item.description = '└─{}'.format(sub_item.description)
            else:
                sub_item.more = ' ├─'
                sub_item.description = '├─{}'.format(sub_item.description)
            self.sub_items.append(sub_item)

