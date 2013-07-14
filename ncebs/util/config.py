import optparse

parser = optparse.OptionParser()
class OptionsParser(object):
    def __init__(self):
        self._options=None

    def __getattr__(self, name):
        return getattr(self._options, name)

    def parse_command_line(self):
        (self._options, args) = parser.parse_args()

    def define(self, *opt_str, **kwargs):

        dest=None
        type=None
        help=None
        if 'name' in kwargs:
            dest=kwargs['name']
        elif 'type' in kwargs:
            type=kwargs['type']
        elif 'help' in kwargs:
            help=kwargs['help']

        parser.add_option(*opt_str, dest=dest, type=type,
                            help=help)

options=OptionsParser()


def define(*opt_str, **kwargs):

    options.define(*opt_str, **kwargs)

def parse_command_line():
    options.parse_command_line()
