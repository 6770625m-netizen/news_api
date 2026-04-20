from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Faqat admin."""
    message = "Bu amal faqat admin uchun ruxsat etilgan."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class IsJournalist(BasePermission):
    """Faqat jurnalist."""
    message = "Bu amal faqat jurnalistlar uchun ruxsat etilgan."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_journalist
            and not request.user.is_currently_blocked
        )


class IsAdminOrJournalist(BasePermission):
    
    message = "Bu amal admin yoki jurnalistlar uchun ruxsat etilgan."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_admin:
            return True
        return request.user.is_journalist and not request.user.is_currently_blocked


class IsNotBlocked(BasePermission):
    
    message = "Sizning hisobingiz vaqtincha bloklangan."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return True  # Auth tekshiruvi boshqa permission tomonidan amalga oshiriladi
        return not request.user.is_currently_blocked
