import json
from datetime import date, time
from types import SimpleNamespace

import requests
import requests_cache
from sqlalchemy import exists

from models import Item, Offer, Inventory

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


def add_upc_to_db(upc, db):
    # Create Item object
    # Create Offer objects
    # Add or update them
    new_item = Item(
        ean=jExtract(upc.items[0], 'ean'),
        title=jExtract(upc.items[0], 'title'),
        upc=jExtract(upc.items[0], 'upc'),
        gtin=jExtract(upc.items[0], 'gtin'),
        elid=jExtract(upc.items[0], 'elid'),
        description=jExtract(upc.items[0], 'description'),
        brand=jExtract(upc.items[0], 'brand'),
        model=jExtract(upc.items[0], 'model'),
        color=jExtract(upc.items[0], 'color'),
        size=jExtract(upc.items[0], 'size'),
        dimension=jExtract(upc.items[0], 'dimension'),
        weight=jExtract(upc.items[0], 'weight'),
        category=jExtract(upc.items[0], 'category'),
        currency=jExtract(upc.items[0], 'currency'),
        lowest_recorded_price=jExtract(upc.items[0], 'lowest_recorded_price'),
        highest_recorded_price=jExtract(upc.items[0], 'highest_recorded_price'),
    )

    existing_record = db.session.query(Item).filter_by(upc=new_item.upc)
    exists_bool = db.session.query(exists().where(Item.upc == new_item.upc)).scalar()
    if exists_bool:
        db.session.query(Item).filter(Item.upc == new_item.upc).update({
            "ean": new_item.ean,
            "title": new_item.title,
            "upc": new_item.upc,
            "gtin": new_item.gtin,
            "elid": new_item.elid,
            "description": new_item.description,
            "brand": new_item.brand,
            "model": new_item.model,
            "color": new_item.color,
            "size": new_item.size,
            "dimension": new_item.dimension,
            "weight": new_item.weight,
            "category": new_item.category,
            "currency": new_item.currency,
            "lowest_recorded_price": new_item.lowest_recorded_price,
            "highest_recorded_price": new_item.highest_recorded_price
        })
    else:
        db.session.add(new_item)
    db.session.commit()
    new_item_id = db.session.query(Item).filter_by(upc=new_item.upc).first().id
    offers = []
    for each in upc.items[0].offers:
        new_offer = Offer(
            item_id=new_item_id,
            upc=jExtract(each, 'upc'),
            merchant=jExtract(each, 'merchant'),
            domain=jExtract(each, 'domain'),
            title=jExtract(each, 'title'),
            currency=jExtract(each, 'currency'),
            list_price=jExtract(each, 'list_price'),
            price=jExtract(each, 'price'),
            shipping=jExtract(each, 'shipping'),
            condition=jExtract(each, 'condition'),
            availability=jExtract(each, 'availability'),
            link=jExtract(each, 'link'),
            updated_t=jExtract(each, 'updated_t'),
        )
        existing_record = db.session.query(Offer).filter_by(upc=new_offer.upc).filter(
            Offer.merchant.contains(new_offer.merchant)).first()
        if existing_record is None:
            existing_record_domain = {"domain": "DSFLKJSDFLKDSJFSDLKJFSDLKFJSDFLKJSDLFKJSDLKFJSLDKFJ"}
        else:
            existing_record_domain = str(existing_record.domain)
        if str(existing_record_domain) == str(new_offer.domain):
            existing_record.item_id = new_offer.item_id
            existing_record.upc = new_offer.upc
            existing_record.merchant = new_offer.merchant
            existing_record.title = new_offer.title
            existing_record.currency = new_offer.currency
            existing_record.list_price = new_offer.list_price
            existing_record.price = new_offer.price
            existing_record.shipping = new_offer.shipping
            existing_record.condition = new_offer.condition
            existing_record.availability = new_offer.availability
            existing_record.link = new_offer.link
            existing_record.updated_t = new_offer.updated_t
        else:
            db.session.add(new_offer)
        offers.append(new_offer)
        db.session.commit()
    return [new_item, offers]


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


def jExtract(obj, key):
    float_list = [
        "lowest_recorded_price",
        "highest_recorded_price",
        "list_price",
        "price",
    ]
    try:
        attrib = getattr(obj, key)
        if attrib == '' and key in float_list:
            return 0
        return attrib
    except(KeyError, AttributeError):
        if key in float_list:
            return 0
        else:
            return ''


def add_or_update_inventory_item(inventory_item, db):
    existing_record = db.session.query(Inventory).filter_by(upc=inventory_item.upc)
    exists_bool = db.session.query(exists().where(Inventory.upc == inventory_item.upc)).scalar()
    if exists_bool:
        db.session.query(Inventory).filter(Inventory.upc == inventory_item.upc).update({
            "item_id": inventory_item.item_id,
            "upc": inventory_item.upc,
            "title": inventory_item.title,
            "description": inventory_item.description,
            "onhand": inventory_item.onhand,
            "minimum": inventory_item.minimum,
            "unit": inventory_item.unit,
            "priority": inventory_item.priority
        })
    else:
        db.session.add(inventory_item)
    db.session.commit()
    return inventory_item
