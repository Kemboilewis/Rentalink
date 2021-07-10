from django.db import models
from nyumba.models import *
from user_account.models import *

#model for storing mpesa responses
class Mpesa_api_Responses(models.Model):
    MerchantRequestID = models.CharField(max_length=50)
    CheckoutRequestID = models.CharField(max_length=50)
    ResponseCode = models.IntegerField()
    ResponseDescription = models.TextField()
    CustomerMessage = models.TextField()
    the_user = models.ForeignKey(myUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Mpesa Response'
        verbose_name_plural = 'Mpesa Responses'

    def __str__(self):
        return self.MerchantRequestID+' '+self.ResponseDescription
        

#model for succesful mpesa payments
class Succesful_Room_payments(models.Model):
    MerchantRequestID = models.CharField(max_length=200)
    CheckoutRequestID = models.CharField(max_length=200)
    ResultCode = models.IntegerField()
    ResultDesc = models.TextField()
    Amount = models.DecimalField(decimal_places=3, max_digits=13)
    MpesaReceiptNumber = models.CharField(max_length=200)
    Balance = models.DecimalField(decimal_places=3,max_digits=13, blank=True, null=True)
    TransactionDate = models.DateTimeField()
    PhoneNumber = models.CharField(max_length=50)
    Paying_user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    Paid_booking = models.ForeignKey(Room_application,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Succesful Room Payment'
        verbose_name_plural = 'Succesful Room Payments'

    def __str__(self):
        return self.MerchantRequestID
        

#model for unsuccesful mpesa payments
class Unsuccesful_Room_payments(models.Model):
    MerchantRequestID = models.CharField(max_length=50)
    CheckoutRequestID = models.CharField(max_length=50)
    ResultCode = models.IntegerField()
    ResultDesc = models.TextField()
    Paying_user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    Paid_booking = models.ForeignKey(Room_application,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'unsuccesful Room transaction'
        verbose_name_plural = 'unsuccesful Room transactions'

    def __str__(self):
        return self.MerchantRequestID

     