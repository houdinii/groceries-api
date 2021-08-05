import json
from datetime import date, time

from flask import request, Response
from flask_restful import Resource
from sqlalchemy import exists, and_

from models import Item, Offer, Error, Inventory
from models import db
from operations import upc_query
from schema import item_schema, items_schema, offer_schema, inventory_schema, inventories_schema
from operations import add_upc_to_db, serialize, jExtract


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
        add_upc_to_db(upc, db)
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
