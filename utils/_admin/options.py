from django.contrib import admin


class ReadOnlyInlineModelAdmin(admin.TabularInline):
    extra = 0
    can_delete = False
    show_change_link = True

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def has_add_permission(self, request, obj):
        return False
