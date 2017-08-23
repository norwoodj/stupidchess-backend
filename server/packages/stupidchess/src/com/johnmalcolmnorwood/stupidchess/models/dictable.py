#!/usr/local/bin/python
from collections import defaultdict


class Dictable:
    def to_dict(self, *keys, delimiter='.'):
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
