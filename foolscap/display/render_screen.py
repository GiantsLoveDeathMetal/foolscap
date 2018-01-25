import os

from .root_widget import Displayable


class Frame(Displayable):
    def __init__(self, screen, frame_type='default'):
        Displayable.__init__(self, screen)

    def draw(self):
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def update(self):
        Displayable.update(self)


class HelpBar(Displayable):
    def __init__(self, screen):
        Displayable.__init__(self, screen)
        # help_options = [
        #     ' [q]uit ',
        #     ' [e]dit ',
        #     ' [d]elete ',
        #     ' [->]expand ',
        # ]
        # DO I NEED A REFRESH METHOD? (This will be handled in update)
        # while len(help_string) < self.max_x:
        #     help_string = [key for key in help_options]
        self.help_string = " [q]uit --- [e]dit --- [d]elete --- [->]expand "

    def draw(self):
        self.screen.addstr(self.bottom_line, 2, self.help_string)

    def update(self):
        Displayable.update(self)


class TitleBar(Displayable):
    def __init__(self, screen):
        Displayable.__init__(self, screen)
        self.heading = "|   FoolScap   |"
        path = os.path.normpath(os.getcwd())
        self.cwd = self.format_path(path)

    def format_path(self, path):
        path = path.split(os.sep)
        if 'home' in path[1]:
            path = os.sep.join(['~'] + path[3:])
            return '| ' + path + ' |'

    def draw(self):
        self.screen.addstr(self.top_line, self.centre_header, self.heading)
        self.screen.addstr(self.top_line, self.centre_header + 20, self.cwd)

    def update(self):
        Displayable.update(self)
        self.centre_header = int((self.max_x - len(self.heading)) / 2)


class StatusBar(Displayable):
    def __init__(self, screen, n_notes):
        Displayable.__init__(self, screen)
        display_text = "Notes: {}".format(n_notes)
        self.display_text = display_text

    def draw(self):
        self.screen.addstr(self.bottom_line - 1, 2, self.display_text)

    def update(self):
        Displayable.update(self)

