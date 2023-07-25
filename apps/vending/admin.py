from django.contrib import admin
from apps.vending.models import Product, Client, VendingMachineSlot


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at", "updated_at"]
    ordering = ["-created_at"]


class ClientAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "credit"]


class VendingMachineSlotAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "row", "column"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(VendingMachineSlot, VendingMachineSlotAdmin)