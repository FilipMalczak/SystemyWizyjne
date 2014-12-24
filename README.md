Systemy Wizyjne
===============

Nasze dane do uzupełnienia

Dane testowe na tą chwile
-------------------------

Żeby nie zaśmiecać repo na swojej lokalnej kopii wrzuciłem nagrania z prezentacji do <repo root>/klipy/(...).avi - zrób prosze to samo, to będzie łatwiej testować.
Na tą chwilę .gitignore ma zapisane, żeby nie dodawać tego katalogu do repo - w przyszłości pomyślimy co zrobić z danymi testowymi.

Current dependencies
--------------------

* SimpleCV
* hmmlearn
* docopt

**Proposal:** Let's try using https://github.com/rags/pynt

CLI
---

    Usage:
        PROG calibrate [-h]
        PROG new <name>
        PROG teach <name>
        PROG test
        PROG daemon [-d] [--actions FILE]
        PROG pattern (activate|deactivate|remove) <name>

    Options:
        -h, --histogram             Use histogram based calibration
        -d, --display               Display camera image with tracking preview
        -a=FILE --actions=FILE      Use custom actions file instead of default (default: ~/SW14/default.actions)