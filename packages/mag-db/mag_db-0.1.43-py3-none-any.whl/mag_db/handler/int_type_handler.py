
from mag_db.handler.type_handler import T, TypeHandler


class IntTypeHandler(TypeHandler):
    def set_parameter(self, parameter: T) -> int | None:
        return parameter