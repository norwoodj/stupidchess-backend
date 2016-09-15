#!/usr/local/bin/python


class Dictable:
    def to_dict(self, *keys):
        prefixes = set()
        result = {}

        for i, k in enumerate(keys):
            if k in prefixes:
                continue
            if '.' in k:
                prefix = k.split('.')[0]
                if prefix in prefixes:
                    continue

                v = getattr(self, prefix)
                if isinstance(v, Dictable):
                    prefixed_keys = filter(lambda key: k.startswith(prefix), keys[i:])
                    sub_keys = list(map(lambda key: k[len(prefix) + 1:], prefixed_keys))
                    result[prefix] = v.to_dict(*sub_keys)
                else:
                    result[prefix] = v

                prefixes.add(prefix)

            else:
                result[k] = getattr(self, k)

        return result
