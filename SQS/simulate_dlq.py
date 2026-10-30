import json
import time

from aws_client import AWSClient

SOURCE_QUEUE_URL = "https://sqs.ap-southeast-1.amazonaws.com/141681050375/Testing"
DLQ_NAME = "Testing-DLQ"
MAX_RECEIVE_COUNT = 2
VISIBILITY_TIMEOUT = 5


class DLQSimulator:
    def __init__(self):
        self.client = AWSClient().get_client('sqs')

    def setup(self):
        dlq_url = self.client.create_queue(QueueName=DLQ_NAME)["QueueUrl"]
        dlq_arn = self.client.get_queue_attributes(
            QueueUrl=dlq_url, AttributeNames=["QueueArn"]
        )["Attributes"]["QueueArn"]

        self.client.set_queue_attributes(
            QueueUrl=SOURCE_QUEUE_URL,
            Attributes={
                "RedrivePolicy": json.dumps({
                    "deadLetterTargetArn": dlq_arn,
                    "maxReceiveCount": MAX_RECEIVE_COUNT
                }),
                "VisibilityTimeout": str(VISIBILITY_TIMEOUT)
            }
        )
        print(f"DLQ ready: {dlq_url}")
        print(f"Redrive policy set on source queue, maxReceiveCount={MAX_RECEIVE_COUNT}")
        return dlq_url

    def produce(self, payload):
        self.client.send_message(
            QueueUrl=SOURCE_QUEUE_URL,
            MessageBody=json.dumps(payload)
        )
        print(f"Sent: {payload}")

    def check_dlq(self, dlq_url):
        res = self.client.receive_message(
            QueueUrl=dlq_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )
        messages = res.get("Messages", [])
        if messages:
            print(f"Found in DLQ: {messages[0]['Body']}")
        else:
            print("DLQ empty — message hasn't landed yet, try again shortly")


if __name__ == "__main__":
    sim = DLQSimulator()
    dlq_url = sim.setup()
    sim.produce({"test": "poison message"})

    for round_num in range(1, MAX_RECEIVE_COUNT + 2):
        print(f"\n--- round {round_num} ---")
        res = sim.client.receive_message(
            QueueUrl=SOURCE_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5,
            AttributeNames=["ApproximateReceiveCount"]
        )
        messages = res.get("Messages", [])
        if not messages:
            print("Source queue empty — message likely moved to DLQ")
            break
        msg = messages[0]
        print(f"received body={msg['Body']} receive_count={msg['Attributes']['ApproximateReceiveCount']} — NOT deleting")
        print(f"waiting {VISIBILITY_TIMEOUT + 1}s for visibility timeout...")
        time.sleep(VISIBILITY_TIMEOUT + 1)

    print("\n--- checking DLQ ---")
    time.sleep(2)
    sim.check_dlq(dlq_url)
