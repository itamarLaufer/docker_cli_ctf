class Level:
    def __init__(self, id, pass_code, instructions=None):
        self.id = id
        self.pass_code = pass_code
        self.instructions = instructions
        self.levels = []

    @property
    def next_level(self):
        try:
            return self.levels[self.id]
        except IndexError:
            return None

    @property
    def next_instructions(self):
        return None if not self.next_level else self.next_level.instructions

    def print_next_instructions(self):
        if self.next_instructions:
            print(self.next_instructions)

    def __call__(self):
        pass


class RunLevel(Level):
    def __call__(self, *args, **kwargs):
        print(f"You passed level{self.id}! the code is {self.pass_code}")
        self.print_next_instructions()


class RunWithLastCodeLevel(Level):
    def __call__(self, *args, **kwargs):
        print(f"You passed level{self.id}! the code is {self.pass_code}")
        self.print_next_instructions()


class InteractiveLevel(Level):
    def __call__(self, *args, **kwargs):
        name = input("Hi there! What's your name?")
        if name:
            print(f"Well done {name}! You have just passed level{self.id}! the code is {self.pass_code}")
            self.print_next_instructions()


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
        output = f"You completed level{self.id} the code is {self.pass_code}"
        if self.next_instructions:
            output += f"\n{self.next_instructions}"
        raise SystemExit(output)

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
        os.system(rf'cd /opt/code/http_server && {sys.executable} -m http.server 7979')


class VolumeLevel(Level):
    def __call__(self, *args, **kwargs):
        try:
            with open('/var/cool_staff/name.txt') as f:
                name = f.read()
            with open('/var/cool_staff/code.txt') as f:
                f.write(f'You finished the level! the code is {self.pass_code}')
