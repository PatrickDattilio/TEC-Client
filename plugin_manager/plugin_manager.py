import os
import sys

__author__ = 'pat'


class PluginManager():
    path = "plugin_manager/plugins"
    plugins = {}

    def __init__(self):
        self.find_plugins(self.path, )
        print(self.plugins)

    def find_plugins(self, current_path):
        sys.path.insert(0, current_path)
        for root, dirs, files in os.walk(current_path, topdown=True):
            for name in files:
                if name.endswith(".py"):
                    print(os.path.join(root, name))
                    name = name.strip(".py")
                    # if ext == '.py':
                    try:
                        mod = __import__(name)
                        self.plugins[name] = mod.Plugin()
                    except Exception as e:
                        print(e.__doc__)
            for name in dirs:
                self.find_plugins(current_path + "/" + name)
        sys.path.pop(0)

    def pre_draw_plugins(self, line, tags, send_command):
        for plugin in self.plugins.values():
            plugin.process(line, send_command)

        #Maybe we do something like AND the result of all the process calls? if any of them return that they handled it and we should not draw
        return False

    def post_draw_plugin(self, line, tags):
        pass

    def create_plugin_area(self, plugin_area):
        for plugin in self.plugins.values():
            plugin.draw(plugin_area)
