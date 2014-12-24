import docopt

USAGE = '''Usage:
    PROG calibrate
    PROG new <name>
    PROG teach <name>
    PROG recalculate
    PROG test
    PROG daemon [-d] [--actions FILE]

Options:
    -d, --display               Display camera image with tracking preview
    -a=FILE --actions=FILE      Use custom actions file instead of default (default: ~/.gestures.actions)
'''

def main(args=[]):
    parsed = docopt.docopt(USAGE, args)
    print parsed