
from aws_client import AWSClient

class Consumer:
    QUEUE_URL = "https://sqs.ap-southeast-1.amazonaws.com/141681050375/Testing"

    def get_message(self, count):
        client = AWSClient().get_client('sqs')
        res = client.receive_message(
            QueueUrl=self.QUEUE_URL,
            MaxNumberOfMessages=count,
            WaitTimeSeconds=10
        )

        messages = res.get("Messages", [])
        for msg in messages:
            print(msg["Body"])
            client.delete_message(
                QueueUrl=self.QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )


if __name__ == "__main__":
    c= Consumer()
    c.get_message( 1)