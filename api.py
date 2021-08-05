from flask_restful import Api

from resources import ItemResource, ItemListResource, OfferResource, UpcResource, InventoryResource, InventoryListResources, InventoryListResource

api = Api()

api.add_resource(ItemListResource, '/items')
api.add_resource(ItemResource, '/item')
api.add_resource(OfferResource, '/offer')
api.add_resource(UpcResource, '/upc/<string:upc_number>')
api.add_resource(InventoryResource, '/inventory')
api.add_resource(InventoryListResources, '/inventory/list')
api.add_resource(InventoryListResource, '/inventory/list/<string:upc_number>')
