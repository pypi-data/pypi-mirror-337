from typing import Any

from mag_tools.utils.data.date_utils import DateUtils

from mag_db.handler.type_handler import T, TypeHandler


class DateTypeHandler(TypeHandler):
    def set_parameter(self, parameter: T) -> Any | None:
        return DateUtils.to_string(parameter, '%Y-%m-%d')