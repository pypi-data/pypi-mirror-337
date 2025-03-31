import boto3
import botocore.exceptions

class SNSService:
    def __init__(self, region_name="us-east-1", topic_arn=None):
        """Initialize SNS Client."""
        self.sns_client = boto3.client("sns", region_name=region_name)
        self.topic_arn = topic_arn

        if not topic_arn:
            raise ValueError("❌ SNS Topic ARN is required.")

    def send_notification(self, subject, message):
        """Send an SNS notification to the topic."""
        try:
            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Message=message,
                Subject=subject,
            )
            print(f"✅ Notification sent successfully: {response['MessageId']}")
            return response
        except botocore.exceptions.BotoCoreError as e:
            print(f"❌ BotoCore Error sending SNS notification: {e}")
        except botocore.exceptions.ClientError as e:
            print(f"❌ Client Error sending SNS notification: {e}")
        except Exception as e:
            print(f"❌ Unexpected error sending SNS notification: {e}")
        return None

    def subscribe(self, endpoint, protocol="email"):
        """Subscribe an endpoint (email, SMS, HTTP/S) to the SNS topic."""
        try:
            response = self.sns_client.subscribe(
                TopicArn=self.topic_arn,
                Protocol=protocol,
                Endpoint=endpoint
            )
            print(f"✅ Subscription request sent to {endpoint} via {protocol}.")
            return response
        except botocore.exceptions.BotoCoreError as e:
            print(f"❌ BotoCore Error subscribing endpoint: {e}")
        except botocore.exceptions.ClientError as e:
            print(f"❌ Client Error subscribing endpoint: {e}")
        except Exception as e:
            print(f"❌ Unexpected error subscribing endpoint: {e}")
        return None
