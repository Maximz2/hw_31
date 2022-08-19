from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import Ad, Selection
from users.models import User


class AdEditPermission(BasePermission):
    """
    Разрешение на редактирование объявления только для владельца объявления, админа или модератора.
    """
    message = "Only owner or admin(moderator) can edit ads"

    def has_permission(self, request, view):
        if request.user.role in [User.MODERATOR, User.ADMIN]:
            return True

        try:
            ad = Ad.objects.get(pk=view.kwargs['pk'])
        except Ad.DoesNotExist:
            raise Http404

        if ad.author_id == request.user.id:
            return True
        return False


class SelectionEditPermission(BasePermission):
    """
    Разрешение на редактирование подборки объявлений только для её владельца
    """
    message = "You can only edit your own selections"

    def has_permission(self, request, view):
        try:
            selection = Selection.objects.get(pk=view.kwargs['pk'])
        except Selection.DoesNotExist:
            raise Http404

        if selection.owner_id == request.user.id:
            return True
        return False
