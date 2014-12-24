import docopt
from common.modes.calibration_mode import CalibrationMode
from common.modes.daemon_mode import DaemonMode
from common.modes.learning_mode import LearningMode
from common.modes.test_mode import TestMode

USAGE = '''Usage:
    PROG calibrate [-h]
    PROG new <name>
    PROG teach <name>
    PROG recalculate
    PROG test
    PROG daemon [-d] [--actions FILE]

Options:
    -h, --histogram             Use histogram based calibration
    -d, --display               Display camera image with tracking preview
    -a=FILE --actions=FILE      Use custom actions file instead of default (default: ~/SW14/default.actions)
'''

def main(args=[]):
    parsed = docopt.docopt(USAGE, args)
    if parsed['calibrate']:
        CalibrationMode(parsed['--histogram']).run()
    if parsed['new'] or parsed['teach']:
        LearningMode(parsed['<name>'], parsed['new']).run()
    elif parsed['test']:
        TestMode().run()
    elif parsed['daemon']:
        DaemonMode(parsed['--display'], parsed['--actions']).run()
