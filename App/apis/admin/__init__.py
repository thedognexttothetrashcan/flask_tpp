from flask_restful import Api

from App.apis.admin.user_apis import AdminUsersResource, AdminUserResource

admin_api = Api(prefix="/admin")


admin_api.add_resource(AdminUsersResource, "/users/")
admin_api.add_resource(AdminUserResource, "/users/<int:pk>/")