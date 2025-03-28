from decimal import Decimal

from mag_db.handler.type_handler import T, TypeHandler


class DecimalTypeHandler(TypeHandler):
    def set_parameter(self, parameter: T) -> Decimal | None:
        return parameter