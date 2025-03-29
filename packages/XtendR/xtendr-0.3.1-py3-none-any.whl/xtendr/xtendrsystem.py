import importlib
import sys
import os
import json
import threading
from xtendr.xtendrbase import XtendRBase

__version__ = "0.3.1"

class XtendRSystem:
    """Plugin system to manage plugins.
    
    Example:
    >>> system = XtendRSystem()
    >>> system.version()
    XtendR v0.1.3
    >>> system.attach("example_plugin")  # Assuming 'example_plugin/example_plugin.json' exists
    >>> system.run("example_plugin")
    ExamplePlugin is running!
    >>> system.stop("example_plugin")
    ExamplePlugin has stopped!
    >>> system.detach("example_plugin")
    Detached plugin 'example_plugin'.
    """
    def __init__(self, pluginpath = "plugins"):
        self.pluginspath = pluginpath
        self.plugins = {}
    
    def version(self) -> str:
        return "XtendR v" + __version__
    
    def attach(self, name: str, callback) -> None:
        """Dynamically load a plugin from its folder."""
        if name in self.plugins:
            print(f"Plugin '{name}' is already attached.")
            return
        
        plugin_path = os.path.join(os.getcwd(), self.pluginspath, name)
        info_path = os.path.join(plugin_path, name + ".json")
        print(plugin_path + "\n" + info_path)
        
        if not os.path.isdir(plugin_path) or not os.path.isfile(info_path):
            print(f"Failed to attach plugin '{name}', folder or info file not found.")
            return
        
        try:
            with open(info_path, "r", encoding="utf-8") as f:
                plugin_info = json.load(f)
                module_name = plugin_info.get("module")
                class_name = plugin_info.get("class")
                if not module_name or not class_name:
                    print(f"Plugin '{name}' info file is missing 'module' or 'class' key.")
                    return
                
                sys.path.insert(0, plugin_path)
                module = importlib.import_module(module_name)
                plugin_class = getattr(module, class_name)
                instance = plugin_class()
                
                if not isinstance(instance, XtendRBase):
                    print(f"Plugin '{name}' does not inherit from PluginBase.")
                    return
                
                self.plugins[name] = {
                    'instance': instance,
                    'running': False,
                    'info': plugin_info,
                    'autorun': False
                }
                print(f"Attached plugin '{name}'.")
                print(f"Running pre-load on '{name}'.")
                thread = threading.Thread(target=self.plugins[name]['instance'].pre_load, args=(callback,))
                thread.start()
        except (ModuleNotFoundError, json.JSONDecodeError, AttributeError) as e:
            print(f"Failed to attach plugin '{name}': {e}")
    
    def run(self, name: str, *args, **kwargs):
        """Run the plugin's 'run' method if available."""
        if name in self.plugins:
            self.plugins[name]['running'] = True
            return self.plugins[name]['instance'].run(*args, **kwargs)
        print(f"Plugin '{name}' not found or has no 'run' method.")
    
    def stop(self, name: str) -> None:
        """Stop the plugin if it's running."""
        if name in self.plugins and self.plugins[name]['running']:
            self.plugins[name]['running'] = False
            self.plugins[name]['instance'].stop()
        else:
            print(f"Plugin '{name}' is not running.")
    
    def detach(self, name: str) -> None:
        """Unload a plugin."""
        if name in self.plugins:
            del self.plugins[name]
            sys.modules.pop(name, None)
            print(f"Detached plugin '{name}'.")
        else:
            print(f"Plugin '{name}' is not attached.")
