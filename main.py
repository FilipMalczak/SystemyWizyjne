if __name__ == "__main__":
    import vision.something
    import pattern.recognition_demo_test

    print "This should be main program"
    print "It should be split into 2 main packages:"
    print "\tvision:"
    vision.something.describe_me()
    print "\tpattern:"
    pattern.something.describe_me()
    print "It would be best to keep all logic inside packages and make their API public in"
    print "__init__.py files, so this script can set up infrastructure while only importing"
    print "those 2 packages (without submodules)."
