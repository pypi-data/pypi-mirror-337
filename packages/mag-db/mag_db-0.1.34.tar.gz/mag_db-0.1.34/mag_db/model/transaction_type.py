from mag_tools.model.base_enum import BaseEnum


class TransactionType(BaseEnum):
    REQUIRED = ("Required", "自动加入已开启事务,没有则自动创建新的事务")
    REQUIRED_NEW = ("RequiredNew", "自动创建新事务")