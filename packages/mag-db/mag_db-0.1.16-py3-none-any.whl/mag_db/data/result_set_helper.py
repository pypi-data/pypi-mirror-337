from typing import Any, Dict, List, get_args

from mag_tools.utils.common.class_utils import ClassUtils
from mag_tools.jsonparser.json_parser import JsonParser

from mag_db.data.db_output import DbOutput


class ResultSetHelper:
    @staticmethod
    def to_maps(result_set: list[Dict[str, Any]], db_output: DbOutput) -> List[Dict[str, Any]]:
        return [
            {
                db_output.column_name_mapping.get_target_name(column_name) or column_name:
                    row_map[column_name] for column_name in db_output.column_names
            }
            for row_map in result_set
        ]

    @staticmethod
    def to_beans(result_set: list[Dict[str, Any]], db_output: DbOutput) -> List[Any]:
        result_list = []
        for row_map in result_set:
            kwargs = {}
            for column_name in db_output.column_names:
                target_name = db_output.get_target_name(column_name)
                target_type = ClassUtils.get_field_type_of_class(db_output.result_class, target_name)
                target_type = ClassUtils.get_origin_type(target_type)
                value = row_map.get(column_name)

                if target_type == tuple:
                    args = get_args(target_type)
                    if args:
                        kwargs[target_name] = JsonParser.to_tuple(value, args[0])
                elif target_type == list:
                    args = get_args(target_type)
                    if args:
                        kwargs[target_name] = JsonParser.to_list(value, args[0])
                elif target_type == dict:
                    args = get_args(target_type)
                    if args:
                        kwargs[target_name] = JsonParser.to_map(value, str, args[0])
                else:
                    kwargs[target_name] = value

            result_list.append(db_output.result_class(**kwargs))

        return result_list
