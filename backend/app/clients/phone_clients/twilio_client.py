# app/clients/phone_clients/twilio_client.py

from twilio.rest import Client


class TwilioClient:
    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        from_number: str,
    ) -> None:
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def create_call(
        self,
        to_number: str,
        webhook_url: str,
    ):
        """
        Start an outbound phone call.
        Twilio will call webhook_url when the callee answers.
        """
        return self.client.calls.create(
            to=to_number,
            from_=self.from_number,
            url=webhook_url,
            method="POST",
        )

    def create_call_with_machine_detection(
        self,
        to_number: str,
        webhook_url: str,
    ):
        """
        Start outbound call with answering machine detection.
        /call/out will receive AnsweredBy in the webhook form.
        """
        return self.client.calls.create(
            to=to_number,
            from_=self.from_number,
            url=webhook_url,
            method="POST",
            machine_detection="Enable",
        )

    def send_sms(
        self,
        to_number: str,
        body: str,
    ):
        return self.client.messages.create(
            to=to_number,
            from_=self.from_number,
            body=body,
        )