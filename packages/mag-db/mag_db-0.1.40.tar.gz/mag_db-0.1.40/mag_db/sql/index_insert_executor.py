from typing import List

from mag_tools.log.logger import Logger
from mag_tools.enums.log_type import LogType

from mag_db.core.db_session import DBSession
from mag_db.core.transaction_cache import TransactionCache
from mag_db.sql.base_executor import BaseExecutor


class IndexInsertExecutor(BaseExecutor):
    def __init__(self, sql: str, session: DBSession):
        super().__init__(sql, session)

    def execute(self)->List[int]:
        self.check()

        try:
            values = self.prepare()

            tx = TransactionCache.get_current_tx(self._session.datasource_name)
            connection = self.get_connection(tx)
            with connection.cursor() as cursor:
                insert_ids = []
                if values:
                    cursor.executemany(self._sql, values)

                    last_id = cursor.lastrowid
                    insert_num = cursor.rowcount
                    for i in range(insert_num):
                        insert_ids.append(last_id + i)
                else:
                    cursor.execute(self._sql)
                    insert_ids.append(cursor.lastrowid)

                if tx is None:
                    connection.commit()

                return insert_ids
        except (NotImplementedError, Exception):
            Logger.throw(LogType.DAO,f"执行SQL失败: {self._sql}")