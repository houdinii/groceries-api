from sqlalchemy import asc, desc, func
from sqlalchemy.sql import label
from models import Item, Offer

import requests
import requests_cache
from requests_cache import CachedSession
import json
from types import SimpleNamespace

OMIT_LIST = {'images', 'offers', 'user_data'}

requests_cache.install_cache('search_cache', backend='sqlite', expire_after=604800)


class Inline(object):
    """An empty object to create new objects inline dynamically"""
    pass


def upcitemedb_upc_request(upc, api='https://api.upcitemdb.com/prod/trial/lookup', headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip,deflate'
        }
    if upc is None:
        return
    try:
        url = f'{api}?upc={upc}'
        resp = requests.get(url, headers=headers)
    except Exception as e:
        print(f'Exception: {e}')
        return search_error(e)
    return resp


def create_search_object_from_response(upc_response):
    try:
        upc_search = json.loads(upc_response.text, object_hook=lambda d: SimpleNamespace(**d))
    except Exception as e:
        print(f'Exception: {e}')
        return search_error(e)
    return upc_search


def upc_query(upc, api='https://api.upcitemdb.com/prod/trial/lookup', headers=None):
    try:
        response = upcitemedb_upc_request(upc, api, headers)
        item = create_search_object_from_response(response)
    except Exception as e:
        print(f'Exception: {e}')
        return search_error(e)
    return item


def search_error(e):
    e_object = Inline()
    e_object.code = 'ERROR'
    e_object.reason = e
    return e_object


def object_or_empty(input_obj, attribute, obj_type):
    if hasattr(input_obj, attribute):
        try:
            return obj_type(getattr(input_obj, attribute))
        except ValueError as e:
            if obj_type == int or obj_type == float:
                return obj_type(0)
            else:
                return ""
    else:
        return ""
