class Plugin:
    def __init__(self):
        pass

    def set_send_command(self, send_command):
        self.send_command = send_command

    def set_echo(self, echo):
        self.echo = echo

    def post_process(self, line):
        if line.strip() == "look":
            self.echo("You looked!")
