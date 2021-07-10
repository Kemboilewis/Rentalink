from django.contrib import admin
from .models import Plot, Room, Room_application, Maintenance, Store, Store_unit, Store_applications


class Plot_admin(admin.ModelAdmin):
	list_display = ('plot_owner','property_name', 'location', 'property_type', 'date_created')
	list_display_links = ('plot_owner','property_name', 'location', 'property_type')
	search_fields = ('property_name', 'plot_owner')
admin.site.register(Plot, Plot_admin)

class Room_admin(admin.ModelAdmin):
	list_display = ('room_name','room_plot', 'room_tenant', 'room_status')
	list_display_links = ('room_name','room_plot', 'room_tenant', 'room_status')
	search_fields = ('room_name', 'room_plot','room_tenant')
admin.site.register(Room, Room_admin)

class Room_application_admin(admin.ModelAdmin):
	list_display = ('booking_user','booked_room', 'landlords_response', 'payment_status')
	list_display_links = ('booking_user','booked_room', 'landlords_response', 'payment_status')
	search_fields = ('booking_user','booked_room')
admin.site.register(Room_application, Room_application_admin)

class Maintenance_admin(admin.ModelAdmin):
	list_display = ('applying_user','plot', 'room', 'subject')
	list_display_links = ('applying_user','plot', 'room', 'subject')
	search_fields = ('applying_user','plot', 'room')
admin.site.register(Maintenance, Maintenance_admin)

class Store_admin(admin.ModelAdmin):
	list_display = ('store_owner','store_name', 'store_location', 'store_capacity')
	list_display_links = ('store_owner','store_name', 'store_location', 'store_capacity')
	search_fields = ('store_owner','store_name', 'store_location')
admin.site.register(Store, Store_admin)

class Store_unit_admin(admin.ModelAdmin):
	list_display = ('unit_name','unit_store', 'user_mzigo', 'unit_number', 'unit_status', 'date_created')
	list_display_links = ('unit_name','unit_store', 'user_mzigo', 'unit_number')
	search_fields = ('unit_name','unit_store', 'user_mzigo')
admin.site.register(Store_unit, Store_unit_admin)

class Store_applications_admin(admin.ModelAdmin):
	list_display = ('applied_unit','applying_user', 'payment_status', 'applied_store', 'owner_response', 'starting_date')
	list_display_links = ('applied_unit','applying_user', 'payment_status', 'applied_store', 'owner_response', 'starting_date')
	search_fields = ('applied_unit','applying_user','starting_date')
admin.site.register(Store_applications, Store_applications_admin)