import sys
import signal

from level import InteractiveLevel, PsLevel, RunLevel, RunWithLastCodeLevel, StopKillLevel, EnvVarLevel, ServerLevel


def wrong_level():
    print("You have inserted the wrong key!")


LEVELS = (
    RunLevel(1, 'GReatSTaRt'),
    RunWithLastCodeLevel(2, 'coMMander', "From now on, when running the image for the next level the container should run with the last level code as its command"),
    InteractiveLevel(3, 'INTerACTIVISM'),
    PsLevel(4, '49'),
    StopKillLevel(5, 'DontST0pMEn0w', signal.SIGINT, "Try to stop me!"),
    StopKillLevel(6, 'imalIve!', signal.SIGINT, "Can you kill me with SIGHUP?"),
    # StopKillLevel(6, 'imalIve!', signal.SIGHUP, "Can you kill me with SIGHUP?"),
    EnvVarLevel(7, 'GloBAlWARMMINg'),
    ServerLevel(8, 'TelePOrTEr'),
          )

for level in LEVELS:
    level.levels = LEVELS


def get_level():
    if len(sys.argv) > 1:
        pass_code = sys.argv[1]
        for level in LEVELS:
            if level.pass_code == pass_code:
                return LEVELS[level.id]
        return wrong_level
    return LEVELS[0]


def main():
    get_level()()


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except Exception as error:
    #     pass
    # systemExit
