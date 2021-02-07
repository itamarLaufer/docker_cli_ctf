class Level:
    def __init__(self, id, pass_code, instructions=None):
        self.id = id
        self.pass_code = pass_code
        self.instructions = instructions

    def __call__(self):
        pass


class RunLevel(Level):
    def __call__(self, *args, **kwargs):
        print(f"You passed level{self.id}! the code is {self.pass_code}")
        print("From now on, when running the image for the next level the container should run with the last level code as its command")


class RunWithLastCodeLevel(Level):
    def __call__(self, *args, **kwargs):
        print(f"You passed level{self.id}! the code is {self.pass_code}")


class InteractiveLevel(Level):
    def __call__(self, *args, **kwargs):
        try:
            name = input("Hi there! What's your name?\n")
        except EOFError:
            return
        if name:
            print(f"Well done {name}! You have just passed level{self.id}! the code is {self.pass_code}")


class PsLevel(Level):
    def __call__(self, *args, **kwargs):
        import sys
        print("The level's code is going to be my exit code:)")
        sys.exit(int(self.pass_code))


class StopKillLevel(Level):
    def __init__(self, id, pass_code, signal, instructions=None):
        super().__init__(id, pass_code, instructions)
        self.signal = signal

    def receiveSignal(self, signalNumber, frame):
        raise SystemExit(f"You completed level{self.id} the code is {self.pass_code}")

    def __call__(self, *args, **kwargs):
        import time
        import signal
        print(self.instructions)
        signal.signal(self.signal, self.receiveSignal)
        while True:
            time.sleep(1)


class EnvVarLevel(Level):
    FRUIT_ENV_VAR_NAME = 'FRUIT'

    def __call__(self, *args, **kwargs):
        import os
        fruit = os.environ.get(self.FRUIT_ENV_VAR_NAME)
        if fruit:
            print(f"Wow I like {fruit} too! you completed level{self.id}! the code is {self.pass_code}")
        else:
            print(f"I want to know what's your favourite fruit pass it as an environment variable called {self.FRUIT_ENV_VAR_NAME}")


class ServerLevel(Level):
    def __call__(self, *args, **kwargs):
        import os
        import sys

        print("Running http server")
        os.system(rf'cd /opt/code/http_server && {sys.executable} -m http.server 7979')


class VolumeLevel(Level):
    NAME_FILE_NAME = 'name.txt'
    CODE_FILE_NAME = 'code.txt'
    DIR_PATH = '/var/cool_staff/'

    def __call__(self, *args, **kwargs):
        try:
            with open(f'{self.DIR_PATH}{self.NAME_FILE_NAME}', 'r') as f:
                name = f.read()
                if name == '':
                    print(f"{self.NAME_FILE_NAME} must contain at least one character!")
                    return
            with open(f'{self.DIR_PATH}{self.CODE_FILE_NAME}', 'r') as f:
                content = f.read()
                if content != '':
                    print(f'{self.CODE_FILE_NAME} must be empty!')
                    return
            with open(f'{self.DIR_PATH}{self.CODE_FILE_NAME}', 'w') as f:
                f.write(f'Great job {name}, You finished  level{self.id}! the code is {self.pass_code}')
        except FileNotFoundError as error:
            print(error)


class ExecLevel(Level):
    CODE_FILE_PATH = '/etc/logs/other/.secret/'
    CODE_FILE_NAME = 'code.secret'
    CODE_FULL_NAME = f'{CODE_FILE_PATH}{CODE_FILE_NAME}'

    def _store_code(self):
        import os

        os.makedirs(os.path.dirname(self.CODE_FULL_NAME), exist_ok=True)
        with open(self.CODE_FULL_NAME, "w") as f:
            f.write(f"You have found the hidden code! You completed level{self.id} the code is {self.pass_code}")

    def __call__(self, *args, **kwargs):
        import time

        self._store_code()
        print(f'The code is hidden on the container the file is called {self.CODE_FILE_NAME}')
        while True:
            time.sleep(1)
