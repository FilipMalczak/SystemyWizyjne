from common.config import recognizer
from common.keypress import KeypressReactor
from common.placeholder import show_display, hide_display
import unicurses


def calibrate():
    print "Do the calibration"

USAGE = '''Usage:
    PROG calibrate
    PROG new <name>
    PROG teach <name>
    PROG test
    PROG daemon [-d] [--actions FILE]

Options:
    -d, --display               Display camera image with tracking preview
    -a=FILE --actions=FILE      Use custom actions file instead of default (default: ~/.gestures.actions)
'''

NEXT_EXAMPLE_KEY = " "
STOP_KEY = unicurses.KEY_ENTER
MIN_EXAMPLES = 10

class GestureLearningReactor(KeypressReactor):
    def __init__(self, gesture_name, check_for_min_examples=True):
        KeypressReactor.__init__(self)
        self._name = gesture_name
        self._check_for_min_examples = check_for_min_examples
        self.observations = []
        self.add_action(NEXT_EXAMPLE_KEY, self.next_example)
        self.add_action(STOP_KEY, self.end_learning)

    def _get_last_observation(self):
        #todo: implement this properly, with vision component
        return [1]*10 + [3]*8 + [5]*7

    def init(self, println):
        println("Learning new gesture:", self._name)
        println("Press Space to end one example; Press Enter to use all examples to learn gesture.")

    def next_example(self, println, stop):
        println("Example", str(len(self.observations)), "saved!")
        self.observations.append(self._get_last_observation())

    def end_learning(self, println, stop):
        self.next_example(println, stop)
        if self._check_for_min_examples and len(self.observations)<MIN_EXAMPLES:
            println("Provide at least", str(MIN_EXAMPLES), " of this gesture!")
        else:
            println(str(len(self.observations)), "saved. Using them to learn gesture", self._name+".")
            recognizer.learn(self._name, self.observations)
            stop()

    def listen(self):
        KeypressReactor.listen(self, self.init)

def new_gesture(name, display):
    if recognizer.is_pattern_known(name):
        raise Exception("Pattern "+name+" is already known! Use 'teach' mode instead!")
    if display:
        show_display()
    reactor = GestureLearningReactor(name)
    reactor.listen()
    print "Successfully learned gesture", name, "basing on", len(reactor.observations), "examples."
    if display:
        hide_display()

def teach(name, display):
    if not recognizer.is_pattern_known(name):
        raise Exception("Pattern "+name+" is unknown! Use 'new' mode instead!")
    if display:
        show_display()
    reactor = GestureLearningReactor(name, False)
    reactor.listen()
    print "Successfully learned ",str(len(reactor.observations)), "more examples for gesture", name+"."
    if display:
        hide_display()
