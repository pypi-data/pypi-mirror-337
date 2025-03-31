import unittest
from dataclasses import dataclass, field

from mag_db.data.column_names_mapping import ColumnNamesMapping
from mag_db.data.db_output import DbOutput
from mag_db.data.result_set_helper import ResultSetHelper


class TestResultSetHelper(unittest.TestCase):
    def setUp(self):
        self.query_result = [
            {'id': 1, 'name': 'Alice', "age": 30},
            {'id': 2, 'name': 'Bob', "age": 25},
            {'id': 3, 'name': 'Charlie', "age": 35}
        ]

        self.db_output = DbOutput()
        self.db_output.column_names = ['id', 'name', 'age']
        column_mapping = ColumnNamesMapping()
        column_mapping.put('id', int, 'id')
        column_mapping.put('name', str, 'name')
        column_mapping.put('age', int, 'age')
        self.db_output.column_name_mapping = column_mapping
        self.db_output.result_class = TestBean

    def test_to_maps(self):
        expected_result = [
            {'id': 1, 'name': 'Alice', 'age': 30},
            {'id': 2, 'name': 'Bob', 'age': 25},
            {'id': 3, 'name': 'Charlie', 'age': 35}
        ]
        result = ResultSetHelper.to_maps(self.query_result, self.db_output)
        self.assertEqual(result, expected_result)

    def test_to_beans(self):
        expected_result = [
            TestBean(id=1, name='Alice', age=30),
            TestBean(id=2, name='Bob', age=25),
            TestBean(id=3, name='Charlie', age=35)
        ]
        result = ResultSetHelper.to_beans(self.query_result, self.db_output)
        self.assertEqual(result, expected_result)
        print(result)

@dataclass
class TestBean:
    id: int = field()
    name: str = field()
    age: int = field()

if __name__ == '__main__':
    unittest.main()
