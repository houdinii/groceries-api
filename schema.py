from flask_marshmallow import Marshmallow

from models import Item, Offer, Error

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

        )
        model = Error


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
offer_schema = OfferSchema()
offers_schema = OfferSchema(many=True)
error_schema = ErrorSchema()
errors_schema = ErrorSchema(many=True)
