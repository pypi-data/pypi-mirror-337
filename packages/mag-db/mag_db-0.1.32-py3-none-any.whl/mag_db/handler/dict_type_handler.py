from mag_tools.jsonparser.json_parser import JsonParser

from mag_db.handler.type_handler import T, TypeHandler


class DictTypeHandler(TypeHandler):
    def set_parameter(self, parameter: T) -> str | None:
        return JsonParser.from_bean(parameter) if isinstance(parameter, dict) else None