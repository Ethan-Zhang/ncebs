import optparse

parser = optparse.OptionParser()
options = None

def define(*opt_str, **kwargs):

    dest=None
    type=None
    default=None
    help=None
    if 'name' in kwargs:
        dest=kwargs['name']
    elif 'type' in kwargs:
        type=kwargs['type']
    elif 'default' in kwargs:
        default=kwargs['default']
    elif 'help' in kwargs:
        help=kwargs['help']

    parser.add_option(*opt_str, dest=dest, type=type,
                        default=default, help=help)

def parse_command_line():
    global options
    (options, args) = parser.parse_args()

