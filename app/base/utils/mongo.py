"""
pymongo的api封装
"""

from app.base import mydb


class Mongo:
    def __init__(self, collection=None):
        self.collection = collection

    def get_last_one(self, condition=None):
        d = mydb[self.collection].find_one(condition, sort=[("_id", -1,)])
        return d or {}

    def get_first_one(self, condition=None):
        d = mydb[self.collection].find_one(condition)
        return d or {}

    def get_select_one(self, condition=None, **kwargs):
        return mydb[self.collection].find_one(condition, **kwargs)

    def get_select_data(self, condition=None, **kwargs):
        return mydb[self.collection].find(condition, **kwargs)

    def get_select_count(self, condition=None, **kwargs):
        return mydb[self.collection].find(condition, **kwargs).count()

    def get_distinct_data(self, key, filter_d=None, **kwargs):
        return mydb[self.collection].distinct(key, filter_d, **kwargs)

    def query_by_page(self, condition=None, page_size=10, page_num=1, **kwargs):
        return mydb[self.collection].find(condition, **kwargs).limit(page_size).skip(page_size * (page_num - 1))

    def insert_one(self, data):
        if data:
            return mydb[self.collection].insert_one(data)

    def insert_many(self, data_list):
        if data_list:
            return mydb[self.collection].insert_many(data_list)

    def update_one(self, condition, value, **kwargs):
        return mydb[self.collection].update_one(condition, value, **kwargs)

    def bulk_op(self, op_lst):
        mydb[self.collection].bulk_op(op_lst)

    def del_all(self, condition=None):
        return mydb[self.collection].delete_many(condition)

    def update_many(self, condition, value, **kwargs):
        return mydb[self.collection].update_many(condition, value, **kwargs)

