from flask_restful import Api

from resources import ItemResource, ItemListResource, OfferResource, UpcResource

api = Api()

api.add_resource(ItemListResource, '/items')
api.add_resource(ItemResource, '/item')
api.add_resource(OfferResource, '/offer')
api.add_resource(UpcResource, '/upc/<string:upc_number>')
