from flask_marshmallow import Marshmallow

from models import Item, Offer, Error, Inventory

ma = Marshmallow()


class ItemSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "timestamp",
            "ean",
            "title",
            "upc",
            "gtin",
            "elid",
            "description",
            "brand",
            "model",
            "color",
            "size",
            "dimension",
            "weight",
            "category",
            "currency",
            "lowest_recorded_price",
            "highest_recorded_price",
            "offers"
        )
        model = Item


class OfferSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "item_id",
            "merchant",
            "domain",
            "title",
            "currency",
            "list_price",
            "price",
            "shipping",
            "condition",
            "availability",
            "link",
            "updated_t"
        )
        model = Offer


class ErrorSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "search_url",
            "upc",
            "timestamp",
            "code",
            "message",
        )
        model = Error


class InventorySchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "item_id",
            "upc",
            "title",
            "description",
            "onhand",
            "minimum",
            "unit",
            "priority",
        )
        model = Inventory


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
offer_schema = OfferSchema()
offers_schema = OfferSchema(many=True)
error_schema = ErrorSchema()
errors_schema = ErrorSchema(many=True)
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
