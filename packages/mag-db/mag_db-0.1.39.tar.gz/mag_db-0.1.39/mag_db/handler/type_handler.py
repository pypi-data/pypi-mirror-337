from typing import TypeVar, Any

T = TypeVar('T')

class TypeHandler:
    def set_parameter(self, parameter: T) -> Any | None:
        raise NotImplementedError("set_parameter() must be implemented by subclasses")