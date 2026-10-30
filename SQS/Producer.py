from aws_client import AWSClient
import json

class Producer:
    def add_event(self , payload):
        client = AWSClient().get_client('sqs')
        # print(client.get_queue_url(QueueName = "Testing"))
        res = client.send_message(
            QueueUrl = "https://sqs.ap-southeast-1.amazonaws.com/141681050375/Testing",
            MessageBody = json.dumps(payload)
        )

        print(res)

if __name__ == "__main__":
    p = Producer()
    p.add_event({"test": "FK U "})