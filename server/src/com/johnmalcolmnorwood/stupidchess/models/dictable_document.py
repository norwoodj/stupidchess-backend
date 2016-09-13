#!/usr/local/bin/python


class DictableDocument:
    def to_dict(self, *keys):
        return {k: getattr(self, k) for k in keys}



