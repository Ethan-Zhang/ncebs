import optparse

parser = optparse.OptionParser()
options = None

def define(opt_str, name=None, type=None, help=None):
    parser.add_option(opt_str, dest=name, type=type, help=help)

def parse_command_line():
    global options
    (options, args) = parser.parse_args()

