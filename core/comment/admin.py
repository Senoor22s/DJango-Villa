from django.contrib import admin
from .models import Comment, Contact
from django.contrib import admin


class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ("name", "email", "created_date")
    list_filter = ("email",)
    search_fields = ["name", "message"]


class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ("name", "post", "approved", "created_date")
    list_filter = ("post", "approved")
    search_fields = ["name", "post"]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Contact, ContactAdmin)
