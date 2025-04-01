from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type

from mag_db.data.column_names_mapping import ColumnNamesMapping

@dataclass
class DbOutput:
    """
    数据库输出信息类

    @description: 提供基础的分页操作
    @version: 2.5
    @date: 2015
    """
    # start_column_index: int = 1
    __result_class: Optional[Type] = None
    __column_name_mapping: ColumnNamesMapping = field(default_factory=ColumnNamesMapping)
    __is_multi_table: bool = False
    __column_names: List[str] = field(default_factory=list)

    @property
    def column_names(self) -> List[str]:
        return self.__column_names

    @property
    def result_class(self) -> Optional[Type]:
        return self.__result_class

    @property
    def is_multi_table(self) -> bool:
        return self.__is_multi_table

    @classmethod
    def from_class(cls, bean_class: Optional[Type], col_names: List[str], col_name_map: Optional[Dict[str, str]] = None):
        output = cls()
        output.__column_names = col_names

        if bean_class:
            mapping_from_bean = ColumnNamesMapping.get_by_class(bean_class, col_names, col_name_map)
            output.__column_name_mapping = mapping_from_bean
            output.__result_class = bean_class

        return output

    def get_target_name(self, column_name):
        target_name = self.__column_name_mapping.get_target_name(column_name) if self.__column_name_mapping else column_name
        return target_name if target_name else column_name

    def set_multi_table(self, is_multi_table: bool):
        self.__is_multi_table = is_multi_table