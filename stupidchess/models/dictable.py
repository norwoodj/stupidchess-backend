#!/usr/local/bin/python
from collections import defaultdict


class Dictable:
    def to_dict(self, *keys, delimiter='.'):
        """
        Specify a list of keys to pull out of the Dictable object, and this will convert the object to a dictionary
        containing those fields. Allows for nested fields to be specified by passing dotted fields:

        obj.to_dict("name", "createTimestamp", "address.street", "friends.name")
        {
            "name": "John",
            "createTimestamp": "2017-09-17T23:23:23Z",
            "friends": [
                {"name": "Erin"},
                {"name": "Thomas"}
            ],
            "address": {
                "street": "East 7th Street"
            }
        }

        :param keys:
        :param delimiter:
        :return:
        """
        result = {}
        sub_keys = defaultdict(list)

        for k in keys:
            split_key = k.partition(delimiter)

            if len(split_key[2]) == 0:
                result[k] = getattr(self, k)
            else:
                sub_keys[split_key[0]].append(split_key[2])

        for prefix, sub_keys in sub_keys.items():
            prefix_object = getattr(self, prefix)
            prefix_object = self.__convert_prefix_object(
                prefix_object,
                sub_keys,
                delimiter,
            )

            if prefix_object is not None:
                result[prefix] = prefix_object

        return result

    def __convert_prefix_object(self, prefix_object, sub_keys, delimiter):
        if prefix_object is None:
            return None
        if isinstance(prefix_object, list):
            return [self.__convert_prefix_object(o, sub_keys, delimiter) for o in prefix_object]
        if isinstance(prefix_object, dict):
            return {k: prefix_object[k] for k in sub_keys}
        elif isinstance(prefix_object, Dictable):
            return prefix_object.to_dict(*sub_keys, delimiter=delimiter)
        else:
            return [self.__convert_prefix_object(o, sub_keys, delimiter) for o in prefix_object]
