#!/usr/local/bin/python
from flask import request, redirect, url_for

NEXT_QUERY_PARAM_PREFIX = "_next_"


def redirect_to_next(default_endpoint):
    next_endpoint = request.args.get("next")

    if next_endpoint is None:
        return redirect(url_for(default_endpoint))

    next_args = {
        k.replace(NEXT_QUERY_PARAM_PREFIX, ""): v for k, v in request.args.items() if NEXT_QUERY_PARAM_PREFIX in k
    }

    return redirect(url_for(next_endpoint, **next_args))
