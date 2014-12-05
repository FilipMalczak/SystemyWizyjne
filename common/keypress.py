from unicurses import *

class KeypressReactor:
    def __init__(self):
        self._listeners = {}
        self.default_action = None
        self._stop_condition = False

    def _println(self, *txt):
        addstr(" ".join(txt)+"\n")

    def set_action(self, key, action):
        '''
        action should be callable taking two parameter: function "println" (with p3k-like signature), and
        parameterless function "stop" (to be called when listening should stop).
        '''
        if (isinstance(key, str)):
            key = ord(key.lower())
        self._listeners[key] = action

    def listen(self, init):
        '''
        :param init callable with one parameter: "println" (same as in set_action), executed at the
        beginning of listening
        '''
        stdscr = initscr()
        cbreak()
        init(self._println)
        while not self._stop_condition:
            key = getch()
            addstr("\b \b")
            acted = False
            for k, a in self._listeners.iteritems():
                if k == key:
                    a(self._println, self._stop)
                    acted = True
                    break
            if not acted and self.default_action is not None:
                self.default_action(self._println, self._stop)
        nocbreak()
        stdscr.keypad(0)
        echo()
        endwin()
        self._stop_condition = False

    def _stop(self):
        self._stop_condition = True


# def do_loop():
#
#     addstr("Press C to cheer, L to leave or anything else to be shouted on.\n")
#
#     while 1:
#         s = chr(getch())
#         if s == "c":
#             addstr("Yay!\n")
#         elif s == "l":
#             addstr("Leaving... :(\n")
#             nocbreak()
#             stdscr.keypad(0)
#             echo()
#             endwin()
#             return
#         else:
#             addstr("LOUND NOISES! YOU WENT DARK SIDE, MUTHAFUCKA!\n")
