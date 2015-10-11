import os


class Plugin:
    def __init__(self):
        self.crits = open(os.path.dirname(__file__) + '/crits', 'w')

    def set_send_command(self, send_command):
        self.send_command = send_command

    def set_echo(self, echo):
        self.echo = echo

    def process(self, line):
        if "Critical Hit!" in line:
            position = str(line).find("Critical Hit!")
            self.crits.write(line[position+len("Critical Hit!"):])

    def draw(self, plugin_area):
        pass