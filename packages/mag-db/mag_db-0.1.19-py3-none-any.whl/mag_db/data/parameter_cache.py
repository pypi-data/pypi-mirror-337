from dataclasses import dataclass, field
from typing import List, Optional, Any, Tuple, TypeVar


from mag_db.handler.type_handler import TypeHandler

T = TypeVar('T')

@dataclass
class DbParameter:
    """
    一条记录的参数及类型的列表
    """
    value: Optional[Any] = field(default=None, metadata={'description': '参数值'})
    type_handler: TypeHandler = field(default=None, metadata={'description': '参数类型'})
    
@dataclass
class RowParameter:
    """
    单条记录的参数信息
    """
    __parameters: List[DbParameter] = field(default_factory=list, metadata={'description': '一条记录的参数清单'})

    def append(self, parameter: Any, type_handler: TypeHandler) -> None:
        parameter = type_handler.set_parameter(parameter)
        self.__parameters.append(DbParameter(parameter, type_handler))
        
    @property
    def values(self) -> List[Any]:
        return [parameter.value for parameter in self.__parameters]
    
    @property
    def type_handlers(self) -> List[TypeHandler]:
        return [parameter.type_handler for parameter in self.__parameters]

@dataclass
class ParameterCache:
    row_parameters: List[RowParameter] = field(default_factory=list, metadata={'description': '多条记录的参数清单'})
    sum_of_params: int = field(default=0, metadata={'description': '记录数'})
    field_of_where: List[Any] = field(default_factory=list, metadata={'description': '条件语句中的被占位符替代的字段数值'})

    def set_parameter(self, parameter: Any, type_handler: TypeHandler, row_index: int = 0) -> None:
        if row_index < len(self.row_parameters):
            row_parameter = self.row_parameters[row_index]
        else:
            row_parameter = RowParameter()
            self.row_parameters.append(row_parameter)

        row_parameter.append(parameter, type_handler)

        self.sum_of_params += 1

    @property
    def values(self) -> tuple[tuple[Any, ...], ...]:
        rows = [tuple(row.values) for row in self.row_parameters]
        return tuple(rows)
    
    def get_values(self)-> tuple[tuple[Any, ...], ...]:
        all_values: List[Tuple[Any, ...]] = []

        for row_parameter in self.row_parameters:
            parameters_of_fow = list(row_parameter.values)
            if self.field_of_where:
                parameters_of_fow.extend(self.field_of_where)

            all_values.append(tuple(parameters_of_fow))

        if len(self.row_parameters) == 0 and len(self.field_of_where) > 0:
            all_values.append(tuple(self.field_of_where))

        return tuple(all_values)
    
    def type_handlers(self, row_index: int = 0)->List[TypeHandler]:
        return self.row_parameters[row_index].type_handlers if row_index < len(self.row_parameters) else []