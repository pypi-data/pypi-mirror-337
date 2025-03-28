import boto3
import json

class SQSMessageSender:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        """
        Initialize the SQSMessageSender with AWS credentials and region.
        """
        self.sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def send_message(self, queue_name, message_body, message_group_id):
        """
        Send a message to the specified SQS queue.
        
        :param queue_name: Name of the SQS queue.
        :param message_body: The body of the message (dict).
        :param message_group_id: The MessageGroupId for FIFO queues.
        :return: Response from AWS SQS.
        """
        try:
            # Get queue URL
            queue_url = self.sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']

            # Send the message
            response = self.sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body),
                MessageGroupId=message_group_id,
            )
            print(f"Message sent to SQS. MessageId: {response['MessageId']}")
            return response
        except Exception as e:
            raise Exception(f"Error sending message to SQS: {str(e)}")
