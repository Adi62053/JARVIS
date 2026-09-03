from abc import ABC, abstractmethod


class Tool(ABC):
    """
    Base class for all JARVIS tools.
    """

    @property
    @abstractmethod
    def name(self):
        """Unique name of the tool."""
        pass

    @property
    @abstractmethod
    def description(self):
        """Human-readable description of what the tool does."""
        pass

    @abstractmethod
    def execute(self, **kwargs):
        """Execute the tool action."""
        pass