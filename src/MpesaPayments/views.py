from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import random
import datetime
import requests 
import json
from django.contrib import messages
from .models import *
from user_account.models import myUser
from nyumba.models import *



#import the credential we created
from . credentials import MpesaAccessToken, LipanaMpesaPpassword


@login_required
def bookingAndpayment(request):
    if request.method == 'POST':
        #t_id = request.POST['tenant']
        booking_user = request.user
        room_id = request.POST['roomId']
        booked_room = Room.objects.get(id=room_id)
        booked_plot = booked_room.room_plot
        #landlords_response = 1
        # payment_status = False
        #disabled_status = False
        #merchantrequestid = "12345"
        #active_status =True
        book_time = datetime.datetime.now() 
        check_in_date = request.POST['s_date']
        stay_time = request.POST['s_time']
        check_out_date = request.POST['e_date']
        t_amount = request.POST['amount']
        p_number = request.POST['phone_number']
        
        #make api call
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": t_amount,
            "PartyA": p_number,  # replace with your phone number to get stk push
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": p_number, # replace with your phone number to get stk push
            "CallBackURL": "https://calm-robin-99.loca.lt/MpesaPayments/callback",
            "AccountReference": "lewis and associates",
            "TransactionDesc": "paying for rental deposit"
        }

        response = requests.post(api_url, json=request, headers=headers)#initiate the payment with post method
        response_data = response.json()
        print(response_data)
        if response_data:
            Merchant_RequestID = response_data["MerchantRequestID"] 
            Checkout_RequestID = response_data["CheckoutRequestID"]
            Response_Code = response_data["ResponseCode"]
            Response_Description = response_data["ResponseDescription"]
            Customer_Message = response_data["CustomerMessage"]

            saving_response = Mpesa_api_Responses(
                MerchantRequestID = Merchant_RequestID, 
                CheckoutRequestID = Checkout_RequestID ,
                ResponseCode = Response_Code, 
                ResponseDescription = Response_Description, 
                CustomerMessage = Customer_Message ,
                the_user = booking_user,

                )
            saving_response.save() 
        
        
            if Response_Code == '0':
                new_re=Room_application(booking_user=booking_user, booked_room=booked_room, booked_plot=booked_plot, merchantrequestid=Merchant_RequestID, 
                book_time=book_time, check_in_date=check_in_date,stay_time=stay_time,check_out_date=check_out_date )
                try:
                    booked_room.room_status=True
                    booked_room.save()  
                    new_re.save()
                    #messages.add_message(request, messages.SUCCESS, 'application succesful.')
                    #messages.success(request, "rental application send succesfully")
                    return redirect("nyumba:myapplications")
                except:
                    #messages.add_message(request, messages.WARNING, 'application succesful.')
                    #messages.add_message(request, "the applicaiton process failed, try again")
                    return redirect("nyumba:explore_rentals")
         
        else:
            messages.danger(request, "application failed")
            return redirect("nyumba:explore_rentals")
     
    return render(request, 'nyumba/tenant/explore_rentals.html')


#view for saving the Daraja api response to the database and activating a booking 
@csrf_exempt
def call_back(request):
    s=datetime.datetime.now()
    random.seed(s)
    ran_number = random.randrange(10000,100000, 3)
    ran_number = str(ran_number)
    receiptNo = ("##" + ran_number)
    print (ran_number)
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    print(mpesa_body)
    print(mpesa_payment)
    
    Merchant_RequestID = mpesa_payment['Body']['stkCallback']['MerchantRequestID']
    api_response=Mpesa_api_Responses.objects.get(MerchantRequestID=Merchant_RequestID)
    paying_user = api_response.the_user
    paid_booking=Room_application.objects.get(merchantrequestid=Merchant_RequestID)#get the booking 
    Checkout_RequestID=mpesa_payment['Body']['stkCallback']['CheckoutRequestID']
    Result_Code=mpesa_payment['Body']['stkCallback']['ResultCode']
    if Result_Code == 0:
        Result_Desc = mpesa_payment['Body']['stkCallback']['ResultDesc']
        Amount = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        Mpesa_ReceiptNumber = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        #Balance = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][2]['Value']
        Transaction_Date = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        str_transaction_date = str(Transaction_Date)
        transaction_datetime = datetime.datetime.strptime(str_transaction_date,"%Y%m%d%H%M%S")
        Phone_Number = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        payment = Succesful_Room_payments(
            MerchantRequestID = Merchant_RequestID,
            CheckoutRequestID = Checkout_RequestID,
            ResultCode = Result_Code,
            Amount = Amount,
            ResultDesc = Result_Desc,
            MpesaReceiptNumber = Mpesa_ReceiptNumber,
            #Balance = Balance,
            TransactionDate = transaction_datetime,
            PhoneNumber = Phone_Number,
            Paying_user = paying_user,
            Paid_booking = paid_booking,
        )
        payment.save()
        paid_booking.payment_status = True#change the boolean field in our booking table to true
        paid_booking.Receipt_Number = receiptNo
        paid_booking.save()
        

    else:
        Result_Desc = mpesa_payment['Body']['stkCallback']['ResultDesc']
        unsuccesful_payment = Unsuccesful_Room_payments(
            MerchantRequestID = Merchant_RequestID,
            CheckoutRequestID = Checkout_RequestID,
            ResultCode = Result_Code,
            ResultDesc = Result_Desc,
            Paying_user = paying_user,
            Paid_booking = paid_booking,
            )
        unsuccesful_payment.save()
        paid_booking.disable_status = True #disable the booking due to unsuccessful payment
        paid_booking.save()
        

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))#return a json response to daraja that response has been accepted
     

    
