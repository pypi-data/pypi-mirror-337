from abc import ABC, abstractmethod

class XtendRBase(ABC):
    """Abstract base class for all plugins.
    
    Example:
    >>> class TestPlugin(XtendRBase):
    ...     def run(self):
    ...         print("Running TestPlugin")
    ...     def stop(self):
    ...         print("Stopping TestPlugin")
    
    >>> plugin = TestPlugin()
    >>> plugin.run()
    Running TestPlugin
    >>> plugin.stop()
    Stopping TestPlugin
    """
    @abstractmethod
    def run(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pre_load(self, *args):
        pass
        