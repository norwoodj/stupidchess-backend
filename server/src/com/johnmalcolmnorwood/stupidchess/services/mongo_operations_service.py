#!/usr/local/bin/python

class MongoOperationsService:
    """
    This class will wrap the methods exposed by the db models to do retrieval and update operations on the database
    """
    def __init__(
        self,
        model_cls,
        return_fields=None,
        exclude_fields=None,
    ):
        """
        :param model_cls: class of MongoEngine model object being returned
        :param return_fields: list<str> of names of fields to be returned in find queries
        :param exclude_fields: list<str> of names of fields to be excluded in find queries
        """
        self.__model_cls = model_cls
        self.__return_fields = return_fields
        self.__exclude_fields = exclude_fields

    def find(self, **kwargs):
        """
        Returns all objects that match the input criteria

        :param kwargs: keyword args that will be used to filter the list of items returned
        :return: The list of objects of the model class that match the criteria
        """
        result = self.__model_cls.objects(**kwargs)

        if self.__return_fields is not None:
            result = result.only(*self.__return_fields)

        if self.__exclude_fields is not None:
            result = result.exclude(*self.__exclude_fields)

        return result

    def find_one(self, **kwargs):
        """
        Returns only one object that should uniquely match the input criteria. Will return a 404 response if none exists,
        and will raise an exception if more than one object matches the criteria

        :param kwargs: keyword args that will be used to filter the list of items returned
        :return: The single object of the model class that matches the criteria
        """
        return self.find().get_or_404(**kwargs)

    def update(self, query, updates):
        """
        Updates any document that matches the input query dict with the input updates dict

        :param query: dict of criteria that is used to match documents
        :param updates: dict of updates that will be applied to the  matched documents
        :return: The result dict from Mongo
        """
        return self.__model_cls.objects(**query).update(**updates)

