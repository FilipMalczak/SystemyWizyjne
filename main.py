if __name__ == "__main__":
    # from common.cli import main
    # import sys
    # main(sys.argv[1:])
    # main(["teach", "CIRCLE", "-a", "XXX"])
    # from common.keypress_example import main
    # main()
    from common.modes import calibration_mode
    calibration_mode.CalibrationMode().run()
