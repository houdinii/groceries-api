import json
from datetime import date, time

from flask import request, Response
from flask_restful import Resource
from sqlalchemy import exists, and_

from models import Item, Offer, Error, Inventory
from models import db
from operations import upc_query
from schema import item_schema, items_schema, offer_schema, inventory_schema, inventories_schema


class ItemListResource(Resource):
    def get(self):
        items = Item.query.all()
        return items_schema.dump(items)


class ItemResource(Resource):
    def post(self):
        new_item = Item(
            ean=request.json['ean'],
            title=request.json['title'],
            upc=request.json['upc'],
            gtin=request.json['gtin'],
            elid=request.json['elid'],
            description=request.json['description'],
            brand=request.json['brand'],
            model=request.json['model'],
            color=request.json['color'],
            size=request.json['size'],
            dimension=request.json['dimension'],
            weight=request.json['weight'],
            category=request.json['category'],
            currency=request.json['currency'],
            lowest_recorded_price=request.json['lowest_recorded_price'],
            highest_recorded_price=request.json['highest_recorded_price'],
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
        return item_schema.dump(new_item)


class OfferResource(Resource):
    def post(self):
        new_offer = Offer(
            item_id=request.json['item_id'],
            upc=request.json['upc'],
            merchant=request.json['merchant'],
            domain=request.json['domain'],
            title=request.json['title'],
            currency=request.json['currency'],
            list_price=request.json['list_price'],
            price=request.json['price'],
            shipping=request.json['shipping'],
            condition=request.json['condition'],
            availability=request.json['availability'],
            link=request.json['link'],
            updated_t=request.json['updated_t'],
        )

        existing_record = db.session.query(Offer).filter_by(upc=new_offer.upc).filter_by(merchant=new_offer.merchant)
        exists_bool = db.session.query(exists().where(Offer.upc == new_offer.upc).where(Offer.merchant == new_offer.merchant)).scalar()
        if exists_bool:
            db.session.query(Offer).filter(Offer.upc == new_offer.upc and Offer.merchant == new_offer.merchant).update({
                "item_id": new_offer.item_id,
                "upc": new_offer.upc,
                "merchant": new_offer.merchant,
                "domain": new_offer.domain,
                "title": new_offer.title,
                "currency": new_offer.currency,
                "list_price": new_offer.list_price,
                "price": new_offer.price,
                "shipping": new_offer.shipping,
                "condition": new_offer.condition,
                "availability": new_offer.availability,
                "link": new_offer.link,
                "updated_t": new_offer.updated_t,
            })
        else:
            db.session.add(new_offer)
        db.session.commit()
        return offer_schema.dump(new_offer)


class UpcResource(Resource):
    def get(self, upc_number):
        upc = upc_query(upc_number)
        upc_json = json.dumps(upc.__dict__, default=serialize)
        upc_response = Response(
            response=upc_json,
            status=200,
            mimetype="application/json"
        )
        add_upc_to_db(upc)
        return upc_response


class InventoryListResources(Resource):
    def get(self):
        inventory = Inventory.query.all()
        return inventories_schema.dump(inventory)


class InventoryListResource(Resource):
    def get(self, upc_number):
        inventory = Inventory.query.where(upc_number == Inventory.upc).first()
        return inventory_schema.dump(inventory)


class InventoryResource(Resource):
    def post(self):
        new_inventory = Inventory(
            item_id=request.json['item_id'],
            upc=request.json['upc'],
            title=request.json['title'],
            description=request.json['description'],
            onhand=request.json['onhand'],
            minimum=request.json['minimum'],
            unit=request.json['unit'],
            priority=request.json['priority'],
        )
        existing_record = db.session.query(Inventory).filter_by(upc=new_inventory.upc).first()
        exists_bool = db.session.query(exists().where(Inventory.upc == new_inventory.upc).where(Offer.merchant == new_offer.merchant)).scalar()
        if exists_bool:
            db.session.query(Inventory).filter(Inventory.upc == new_inventory.upc).update({
                "item_id": new_inventory.item_id,
                "upc": new_inventory.upc,
                "title": new_inventory.title,
                "description": new_inventory.description,
                "onhand": new_inventory.onhand,
                "minimum": new_inventory.minimum,
                "unit": new_inventory.unit,
                "priority": new_inventory.priority,
            })
        else:
            db.session.add(new_inventory)
        db.session.commit()
        return inventory_schema.dump(new_inventory)


def add_upc_to_db(upc):
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
        db.session.commit()
    return True


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
