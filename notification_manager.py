import datetime
import dotenv
import os
from twilio.rest import Client


dotenv.load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
print(ACCOUNT_SID)
print(AUTH_TOKEN)

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    @staticmethod
    def send_message(flight_data, message_to):
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        # account_sid = 'ACc14250c38b6af8edb3a1fa26f7c75314'
        # auth_token = '89d9b32764d424c47f43e5e81dbf6ea9'
        # client = Client(account_sid, auth_token)

        message_text = f"Low Price alert! Only €{flight_data['price']} to fly from "\
                       f"{flight_data['flyFrom']}-{flight_data['cityFrom']} "\
                       f"to {flight_data['flyTo']}-{flight_data['cityTo']}, from "\
                       f"{flight_data['utc_arrival'][:10]} to {flight_data['utc_departure'][:10]}. "\
                       f"{flight_data['deep_link']}"

        message = client.messages.create(
            body=message_text,
            from_='+14099787901',

            to='+491732714068'
        )

        print(message.sid)
