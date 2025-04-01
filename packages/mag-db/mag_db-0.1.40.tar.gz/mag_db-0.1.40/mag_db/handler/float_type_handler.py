from mag_db.handler.type_handler import T, TypeHandler


class FloatTypeHandler(TypeHandler):
    def set_parameter(self, parameter: T) -> float | None:
        return parameter