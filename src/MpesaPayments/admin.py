from django.contrib import admin
from .models import Mpesa_api_Responses, Succesful_Room_payments, Unsuccesful_Room_payments 


class Response_admin(admin.ModelAdmin):
	list_display = ('MerchantRequestID','CheckoutRequestID', 'ResponseCode', 'ResponseDescription')
	list_display_links = ('MerchantRequestID','CheckoutRequestID', 'ResponseCode', 'ResponseDescription')
	search_fields = ('ResponseCode', 'MerchantRequestID')
admin.site.register(Mpesa_api_Responses, Response_admin)

class Success_admin(admin.ModelAdmin):
	list_display = ('MerchantRequestID', 'Amount', 'MpesaReceiptNumber', 'PhoneNumber', 
		'TransactionDate', 'Paying_user')
	list_display_links = ('MerchantRequestID', 'Amount', 'MpesaReceiptNumber', 'PhoneNumber', 
		'TransactionDate', 'Paying_user')
	search_fields = ('MerchantRequestID', 'MpesaReceiptNumber', 'PhoneNumber','TransactionDate')
admin.site.register(Succesful_Room_payments, Success_admin)

class Failed_admin(admin.ModelAdmin):
	list_display = ('MerchantRequestID', 'ResultCode', 'ResultDesc', 'Paying_user')
	list_display_links = ('MerchantRequestID', 'ResultCode', 'ResultDesc', 'Paying_user')
admin.site.register(Unsuccesful_Room_payments, Failed_admin)


