import os


class Plugin:
    def __init__(self):
        print("CritSaver enabled")
        self.crits = open(os.path.dirname(__file__) + '/crits', 'w')

    def process(self, line, send_command):
        if "Critical Hit!" in line:
            position = str(line).find("Critical Hit!")
            self.crits.write(line[position+len("Critical Hit!"):])

    def draw(self, plugin_area):
        pass