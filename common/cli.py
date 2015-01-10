import docopt
from common.modes.calibration_mode import CalibrationMode
from common.modes.daemon_mode import DaemonMode
from common.modes.learning_mode import LearningMode
from common.modes.test_mode import TestMode
from common.context import recognizer

USAGE = '''Usage:
    PROG calibrate [-h]
    PROG new <name>
    PROG teach <name>
    PROG test [-s]
    PROG daemon [-d] [-s] [--actions FILE]
    PROG pattern (activate|deactivate|remove) <name>

Options:
    -h, --histogram             Use histogram based calibration
    -d, --display               Display camera image with tracking preview
    -s, --standby               Enable hands-free standby mode
    -a=FILE --actions=FILE      Use custom actions file instead of default (default: ~/SW14/default.actions)
'''

def main(args=[]):
    parsed = docopt.docopt(USAGE, args)
    if parsed['calibrate']:
        CalibrationMode(parsed['--histogram']).run()
    if parsed['new'] or parsed['teach']:
        LearningMode(parsed['<name>'], parsed['new']).run()
    if parsed['test']:
        TestMode(parsed['--standby']).run()
    if parsed['daemon']:
        DaemonMode(parsed['--display'], parsed['--standby'], parsed['--actions']).run()
    if parsed['pattern']:
        if parsed['activate']:
            recognizer.activate(parsed['<name>'])
        if parsed['deactivate']:
            recognizer.deactivate(parsed['<name>'])
        if parsed['remove']:
            recognizer.remove(parsed['<name>'])