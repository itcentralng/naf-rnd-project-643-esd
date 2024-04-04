import os

import africastalking

class SMS:
    def __init__(self):
        SMS_USERNAME="nefveh"
        SMS_API_KEY="4954ebaacdea0ea479258705e728660db03aed503544edd06bd229aa06df92d9"
        # Set your app credentials
        self.username = SMS_USERNAME
        self.api_key = SMS_API_KEY
        
        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)
        
        # Get the SMS service
        self.sms = africastalking.SMS
    
    def send(self, recipient, message):
        # Set your shortCode or senderId
        # sender = os.environ.get("SMS_ID")
        try:
            # print(recipient, message, sender)
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, [recipient])
            print (response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))