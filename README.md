Systemy Wizyjne
===============

Nasze dane do uzupełnienia


Default gestures
----------------

Up, down, left, right, up_left, up_right, down_left, down_right

CLI
---

    Usage:
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