from typing import Any

from mag_db.handler.type_handler import T, TypeHandler


class BytesTypeHandler(TypeHandler):
    def set_parameter(self, parameter: T) -> Any | None:
        return parameter