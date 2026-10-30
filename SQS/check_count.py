from aws_client import AWSClient


class QueueCount:
    QUEUE_URL = "https://sqs.ap-southeast-1.amazonaws.com/141681050375/Testing"

    def get_count(self):
        client = AWSClient().get_client('sqs')
        res = client.get_queue_attributes(
            QueueUrl=self.QUEUE_URL,
            AttributeNames=["ApproximateNumberOfMessages"]
        )
        return res["Attributes"]["ApproximateNumberOfMessages"]


if __name__ == "__main__":
    q = QueueCount()
    print(q.get_count())
