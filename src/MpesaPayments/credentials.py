#required inbuilt python  libraries
import requests#making request to the daraja api 
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime # generate date and time and format time using strftime to string
import base64 #encode the password to base 64

####


"""
Requirements to initiate a LMP transaction
#Consumer key and consumer secret-generate access token
#test credentials -LNM business shortcode(or till number) and LNM passkey-create the password
#Access Token
#transaction parameters-password, timestamp, shortcode, account reference, phone number, amount


"""

#credentials
class MpesaC2bCredential:
    consumer_key = 'umGj1Sbkt7PEUqUkzh5OdPOM7tX31LpG'
    consumer_secret = 'HtnsIqz8hmJoCI0N'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'#url for generating access token

#generate access token which is used for authentication in the daraja api
class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)#change the text to json format
    validated_mpesa_access_token = mpesa_access_token['access_token'] #get the access token 

#generate password
class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    # Test_c2b_shortcode = "600344"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())#encoding the password to base 64 and remains in bits
    decode_password = online_password.decode('utf-8')#decode the password to utf-8 which is a string because safaricom expects a string