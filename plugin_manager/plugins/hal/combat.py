from enum import IntEnum
import random
import time

import re
from plugin_manager.plugins.hal.Action import Action


class HuntingGround(IntEnum):
    Island = 0
    Sewers = 1


class Combat:
    def __init__(self, send_command, hal_print, add_action, remove_action, queue, free, action):
        self.rotation = [['zzh', 'zxh', 'zch', 'zvh', 'zbh', 'znh', 'zmh', 'za', 'zsh'],
                         ['zz', 'zx', 'zc', 'zv', 'zb', 'zn', 'za', 'zm', 'zs', 'zd', 'zd', 'zm']]
        self.retreat = False
        self.hal_print = hal_print
        self.hunting_ground = HuntingGround.Sewers
        self.send_command = send_command
        self.add_action = add_action
        self.remove_action = remove_action
        self.queue = queue
        self.free = free
        self.action = action
        self.rollPattern = re.compile('Success: (\d+), Roll: (\d+)')

    def recover(self):
        self.send_command("get tin dagg")
        time.sleep(random.randrange(1234, 2512) / 1000)
        self.send_command("wie tin dagg")

    def handle_recover(self, recover_now):
        self.add_action(Action.recover)
        if recover_now:
            self.perform_action()

    def attack(self):
        index = random.randrange(0, len(self.rotation[self.hunting_ground]))
        cmd = self.rotation[self.hunting_ground][index]
        self.send_command(cmd)
        self.add_action(Action.attack)

    def retreat(self, isRetreating):
        retreat = isRetreating
        pass

    def perform_action(self):
        if self.free and len(self.queue) > 0:
            self.action = self.queue.pop()
            self.hal_print("CAction: " + str(self.action))
            if self.action == Action.recover:
                self.recover()
            elif self.action == Action.retreat:
                self.free = False
            elif self.action == Action.kill:
                self.free = False
                self.add_action(Action.kill)
                self.send_command("kl")
            elif self.action == Action.attack:
                self.free = False
                self.attack()
            elif self.action == Action.release:
                self.send_command("release")
            else:
                self.perform_action()

    # We are in combat
    def handle_combat_line(self, line):
        me = True
        if "You are no longer busy." in line:
            self.hal_print("Not Busy")
            self.free = True
            self.perform_action()
        elif "expires." in line:
            self.remove_action(Action.kill)
            self.hal_print("Dead")
            self.in_combat = False
        elif "falls unconscious" in line:
            self.hal_print("Unconscious")
            self.remove_action(Action.attack)
            self.add_action(Action.kill)
            if self.free:
                self.perform_action()
        elif "You fumble!" in line:
            self.handle_recover(False)
        elif "You must be wielding a weapon to attack." in line or "You can't do that right now." in line:
            self.handle_recover(True)
        elif "clamped onto you" in line:
            self.add_action(Action.release)
        elif "You manage to break free!" in line:
            self.remove_action(Action.release)
        elif "must be unconscious first" in line:
            self.remove_action(Action.kill)
            self.free = True
        elif "[" in line and "Success" in line:
            if "] A" in line or "] An" in line:
                self.add_action(Action.attack)
                me = False
                if self.free:
                    self.hal_print("Free, attacking")
                    self.perform_action()
            elif "You slit" in line:
                self.hal_print("Killed")
                self.remove_action(Action.kill)
                self.in_combat = False
            roll = self.rollPattern.search(line)
            if me:
                self.action_status = int(roll.group(1)) < int(roll.group(2))
