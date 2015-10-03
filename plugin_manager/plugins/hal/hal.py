import tkinter as tk

from plugin_manager.plugins.hal.action import Action
from plugin_manager.plugins.hal.combat import Combat


class Plugin:
    def __init__(self):
        print("AutoCombat: init")
        self.in_combat = False
        self.free = True
        self.action = Action.nothing
        self.queue = []
        self.combat = Combat(self.hal_print, self.add_action, self.remove_action, self.queue, self.free,
                             self.action)
        self.combat_enabled = tk.BooleanVar()

    def process(self, line, send_command):
        if self.in_combat and self.combat_enabled.get():
            self.combat.handle_combat_line(line, send_command)
        elif "You are no longer busy" in line:
            self.hal_print("Not Busy")
            self.free = True
            # self.perform_action()
        elif ("] A" in line or "] An" in line) and "You retrieve the line" not in line:
            self.hal_print("Combat")
            self.in_combat = True
        elif "retreat" in line and "You retreat." not in line and "retreat first" not in line and "retreats." not in line:
            self.hal_print("Retreating")
            self.add_action(Action.retreat)

    def add_action(self, action):
        if action not in self.queue:
            self.queue.append(action)
            self.queue.sort()

    def remove_action(self, action):
        if action in self.queue:
            self.queue.remove(action)
            self.queue.sort()

    def draw(self, plugin_area):
        label_frame = tk.LabelFrame(plugin_area, text="Hal")
        label_frame.grid(row=0, column=0, sticky=tk.N)
        self.draw_toggles(label_frame)
        self.draw_text(label_frame)

    def draw_toggles(self, label_frame):
        combat_toggle = tk.Checkbutton(label_frame, text="Combat", variable=self.combat_enabled,
                                       command=self.combat.perform_action())
        combat_toggle.grid(row=0, column=0, sticky=tk.N)

    def draw_text(self, label_frame):
        scrollbar = tk.Scrollbar(label_frame)
        scrollbar.grid(row=1, column=1, sticky=tk.N + tk.S)
        self.hal_output = tk.Text(
            label_frame,
            state=tk.DISABLED,
            name="hal_output",
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        scrollbar.config(command=self.hal_output.yview)
        self.hal_output.scrollbar = scrollbar
        self.hal_output.grid(row=1, column=0, sticky=tk.N + tk.W)

    def scroll_output(self):
        self.hal_output.see(tk.END)

    def hal_print(self, line):
        self.hal_output.configure(state="normal")
        self.hal_output.insert(tk.END, line + "\n", None)
        self.hal_output.configure(state="disabled")
        self.scroll_output()

    def perform_action(self):
        if self.in_combat and self.combat_enabled.get():
            self.combat.perform_action()
