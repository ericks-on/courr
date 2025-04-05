import base64
import json
import logging
import uuid
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mpesa_flask_logger')
# Configure logging




# Config class to replace Django settings
class Config:
    # M-Pesa API configuration
    MPESA_BUSINESS_SHORTCODE = "174379"
    MPESA_CONSUMER_KEY = "9cBsJ56OY0wdfu7upfvrscnVL4H1OYtT3mDlLrwGYKUafrep"
    MPESA_CONSUMER_SECRET = "H4xvqfVYRm6oFRhdZ8wcUoDdpVmKTuz1jpIrFCVaAsaH29GigydZhPTqULe4t4GX"
    MPESA_AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    MPESA_STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    MPESA_C2B_REGISTER_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    MPESA_TRANSACTION_STATUS_URL = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
    MPESA_REVERSAL_URL = "https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request"
    MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    MPESA_EXPRESS_CALLBACK_URL = "https://cbctrack.com/api/mpesa/stk-callback"
    MPESA_REQUEST_TIMEOUT = 10
    MPESA_CACHE_DURATION = 300  

# Load config
config = Config()

# Custom exceptions
class MpesaAuthenticationError(Exception):
    """M-Pesa API authentication error."""
    pass

class MpesaPaymentError(Exception):
    """Exception raised for payment-related errors."""
    pass

class MpesaStatusError(Exception):
    """Exception raised for transaction status query errors."""
    pass




class PhoneValidationError(BadRequest):
    """Exception raised for phone validation errors."""
    pass

class MpesaClient:
    """Enhanced M-Pesa API client with admin operations support."""
    
    def __init__(self):
        self.config = {
            'business_shortcode': config.MPESA_BUSINESS_SHORTCODE,
            'consumer_key': config.MPESA_CONSUMER_KEY,
            'consumer_secret': config.MPESA_CONSUMER_SECRET,
            'access_token_url': config.MPESA_AUTH_URL,
            'stk_push_url': config.MPESA_STK_PUSH_URL,
            'transaction_status_url': config.MPESA_TRANSACTION_STATUS_URL,
            'passkey': config.MPESA_PASSKEY,
            'callback_url': config.MPESA_EXPRESS_CALLBACK_URL
        }
        self._access_token = None
        self._token_expires_at = None
    
    def _validate_phone_number(self, phone_number):
        """Validate and standardize phone number."""
        try:
            # Assumes phonenumbers library is used
            from phonenumbers import (PhoneNumberFormat, format_number,
                                      is_valid_number, parse)
            parsed_number = parse(phone_number, 'KE')
            
            if not is_valid_number(parsed_number):
                raise PhoneValidationError("Invalid phone number")
            
            # Convert to E.164 format (international format)
            return format_number(parsed_number, PhoneNumberFormat.E164)
        except Exception as e:
            logger.error(f"Phone number validation error: {e}")
            raise PhoneValidationError("Invalid phone number format")
    
    def _get_access_token(self):
        current_time = datetime.now()
        
        if (self._access_token and self._token_expires_at and 
            current_time < self._token_expires_at - timedelta(seconds=config.MPESA_CACHE_DURATION)):
            return self._access_token
        
        try:
            auth = base64.b64encode(
                f"{self.config['consumer_key']}:{self.config['consumer_secret']}".encode()
            ).decode()
            
            headers = {'Authorization': f'Basic {auth}'}
            
            response = requests.get(
                self.config['access_token_url'], 
                headers=headers, 
                timeout=config.MPESA_REQUEST_TIMEOUT
            )
            
            # Add more detailed error logging
            if response.status_code != 200:
                logger.error(f"Token request failed. Status: {response.status_code}, Body: {response.text}")
                raise MpesaAuthenticationError(f"Token request failed with status {response.status_code}")
            
            token_data = response.json()
            logger.info("Token response received successfully")
            
            self._access_token = token_data['access_token']
            self._token_expires_at = current_time + timedelta(hours=1)
            
            return self._access_token
        
        except requests.RequestException as e:
            logger.error(f"M-Pesa token retrieval failed. Error: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Response content: {e.response.text}")
                logger.error(f"Response headers: {e.response.headers}")
            raise MpesaAuthenticationError("Failed to obtain M-Pesa access token")
    
    def initiate_stk_push(self, phone_number, amount, reference):
        """
        Initiate STK push with enhanced debugging and error handling.
        """
        try:
            # Validate inputs
            validated_phone = self._validate_phone_number(phone_number)
            validated_phone = validated_phone.lstrip('+')
            logger.info(f"validated phone: {validated_phone}")
            
            if amount <= 0:
                raise BadRequest("Amount must be positive")
            
            # Get access token
            access_token = self._get_access_token()
            
            # Generate password
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password_str = f"{self.config['business_shortcode']}{self.config['passkey']}{timestamp}"
            password = base64.b64encode(password_str.encode()).decode()
            
            # Construct payload 
            payload = json.dumps({
                'BusinessShortCode': self.config['business_shortcode'],
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerBuyGoodsOnline',
                'Amount': str(int(amount)), 
                'PartyA': validated_phone,
                'PartyB': self.config['business_shortcode'],
                'PhoneNumber': validated_phone, 
                'CallBackURL': self.config['callback_url'],
                'AccountReference': reference[:12], 
                'TransactionDesc': f'Subscription Payment {reference}'
            })
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            try:
                response = requests.post(
                    self.config['stk_push_url'],
                    headers=headers,
                    data=payload,
                    timeout=10  
                )
                
                response_data = response.json()
                
                if response_data.get('ResponseCode') == '0':
                    return {
                        'success': True,
                        'merchant_request_id': response_data['MerchantRequestID'],
                        'checkout_request_id': response_data['CheckoutRequestID'],
                        'customer_message': response_data['CustomerMessage']
                    }
                else:
                    error_msg = response_data.get('ResponseDescription', 'Unknown error')
                    logger.error(f"STK Push failed: {response_data}")
                    raise MpesaPaymentError(f"Payment initiation failed: {error_msg} {response_data}")
            
            except requests.RequestException as e:
                logger.error(f"STK Push API Error: {e}")
                logger.error(f"Response Content: {e.response.text if hasattr(e, 'response') else 'No response'}")
                raise MpesaPaymentError(f"Failed to initiate M-Pesa payment")
        
        except (PhoneValidationError, BadRequest, MpesaAuthenticationError) as e:
            logger.error(f"STK Push Validation Error: {e}")
            raise MpesaPaymentError(str(e))

    def query_transaction_status(self, transaction_id, identifier_type='1'):
        """
        Query the status of a transaction.
        
        Args:
            transaction_id: M-Pesa Receipt Number to query
            identifier_type: Type of identifier (1 for M-Pesa Transaction ID)
        """
        try:
            access_token = self._get_access_token()
            
            # Generate unique query ID
            query_id = str(uuid.uuid4())
            
            # Create payload
            payload = json.dumps({
                'Initiator': self.config['initiator_name'],
                'SecurityCredential': self.config['security_credential'],
                'CommandID': 'TransactionStatusQuery',
                'TransactionID': transaction_id,
                'PartyA': self.config['business_shortcode'],
                'IdentifierType': identifier_type,
                'ResultURL': f"{self.config['callback_url']}/status/result",
                'QueueTimeOutURL': f"{self.config['callback_url']}/status/timeout",
                'Remarks': f"Transaction status query {query_id}",
                'Occasion': ''
            })
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            response = requests.post(
                self.config['transaction_status_url'],
                headers=headers,
                data=payload,
                timeout=10
            )
            
            logger.info(f"Transaction status query response: {response.text}")
            
            response_data = response.json()
            
            if response_data.get('ResponseCode') == '0':
                logger.info(f"Transaction status query initiated: {transaction_id}")
                return {
                    'success': True,
                    'conversation_id': response_data.get('ConversationID', ''),
                    'originator_conversation_id': response_data.get('OriginatorConversationID', ''),
                    'response_description': response_data.get('ResponseDescription', '')
                }
            else:
                error_msg = response_data.get('ResponseDescription', 'Unknown error')
                logger.error(f"Transaction status query failed: {error_msg}")
                raise MpesaStatusError(f"Transaction status query failed: {error_msg}")
                
        except requests.RequestException as e:
            logger.error(f"Transaction Status API Error: {e} {e.response.text if hasattr(e, 'response') else 'No response'}")
            raise MpesaStatusError(f"Failed to query transaction status: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error in transaction status query: {e} {e.response.text if hasattr(e, 'response') else 'No response'}")
            raise MpesaStatusError(f"Unexpected error: {str(e)}")
    



