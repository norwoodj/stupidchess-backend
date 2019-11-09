#!/usr/bin/env python
from mongoengine import DoesNotExist

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 10


class MongoDao:
    def __init__(self, model_class):
        self.__model_class = model_class

    @staticmethod
    def __apply_paging(queryset, offset, limit):
        return queryset[offset:offset+limit]

    @staticmethod
    def __only_fields(queryset, only_fields):
        return queryset if only_fields is None else queryset.only(*only_fields)

    @staticmethod
    def __order_by(queryset, order_by_fields):
        return queryset if order_by_fields is None else queryset.order_by(*order_by_fields)

    @staticmethod
    def insert(obj):
        return obj.save()

    def insert_many(self, objs):
        self.__model_class.objects.insert(objs)
        return objs

    def query(self, query):
        return self.__model_class.objects(__raw__=query)

    def update(self, obj_id, updates):
        self.query({"_id": obj_id}).update(__raw__=updates)

    def update_matching(self, query, updates):
        self.query(query).update(__raw__=updates)

    def count(self, query):
        return len(self.query(query))

    def find(
        self,
        query,
        offset=DEFAULT_OFFSET,
        limit=DEFAULT_LIMIT,
        only_fields=None,
        order_by_fields=None,
    ):
        queryset = self.query(query)
        limited_fields = MongoDao.__only_fields(queryset, only_fields)
        page = MongoDao.__apply_paging(limited_fields, offset, limit)
        return self.__order_by(page, order_by_fields)

    def find_one(self, query, only_fields=None):
        queryset = MongoDao.__only_fields(self.__model_class.objects, only_fields)
        return queryset.get_or_404(__raw__=query)

    def find_one_or_none(self, query, only_fields=None):
        queryset = MongoDao.__only_fields(self.__model_class.objects, only_fields)

        try:
            return queryset.get(__raw__=query)
        except DoesNotExist:
            return None
