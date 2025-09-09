from django.contrib import admin

# Register your models here. 
from .models import FoodProcess, LoginRecord, FoodItem, Contact



@admin.register(FoodProcess)
class FoodProcessAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image", "video")
    search_fields = ("name", "description")
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time", "ip_address")
    search_fields = ("user__username", "ip_address")
    list_filter = ("login_time",)
    ordering = ("-login_time",)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image", "video")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_amount", "payment_completed", "created_at")
    list_filter = ("status", "payment_completed", "created_at")
    search_fields = ("user__username", "razorpay_order_id", "razorpay_payment_id")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "food_item", "quantity", "price")
    list_filter = ("order__status",)
    search_fields = ("order__user__username", "food_item__name")