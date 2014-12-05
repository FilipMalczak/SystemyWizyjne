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
* pygame (in progress)

**Proposal:** Let's try using https://github.com/rags/pynt

CLI
---

    Usage:

    PROG calibrate
    PROG new <name> [-d]
    PROG teach <name> [-d]
    PROG test
    PROG daemon

    Options:
    -d --display            Display camera image with tracking preview
    -a, --actions=<FILE>     Use custom actions file instead of default (default: ~/.gestures.actions)