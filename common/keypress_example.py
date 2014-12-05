from common.keypress import KeypressReactor

reactor = KeypressReactor()

def startup(println):
    println("Press 'c' to cheer, 'l' to leave and anything else to be shouted on.")

def cheer(println, stop):
    println("Yay!")

def leave(println, stop):
    println("Buh-bye... :(")
    stop()

def default(println, stop):
    println("WUBBA LUBBA DUB DUB!")

def main(args=[]):
    reactor.default_action = default
    reactor.set_action("c", cheer)
    reactor.set_action("L", leave)
    reactor.listen(startup)