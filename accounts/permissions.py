from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        obj_dict = obj.__dict__
        user = None
        if 'owner_id' in obj_dict:
            user = obj.owner
        elif 'user_id' in obj_dict:
            user = obj.user
        elif 'customer_id' in obj_dict:
            user = obj.customer

        if user:
            return user == request.user
        else:
            return False