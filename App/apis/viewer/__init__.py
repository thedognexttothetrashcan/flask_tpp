from flask_restful import Api

from App.apis.viewer.order_api import SeatOrdersResource
from App.apis.viewer.seat_api import SeatResource
from App.apis.viewer.ticket_api import TicketsResource
from App.apis.viewer.user_api import ViewerUsersResource

viewer_api = Api(prefix="/viewer")

viewer_api.add_resource(ViewerUsersResource, "/users/")

viewer_api.add_resource(SeatResource, "/seats/<int:pk>/")

viewer_api.add_resource(SeatOrdersResource, "/seatorders/")

viewer_api.add_resource(TicketsResource, "/tickets/")