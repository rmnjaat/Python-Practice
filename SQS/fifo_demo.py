import json
import uuid
import threading

from aws_client import AWSClient

FIFO_QUEUE_NAME = "Testing.fifo"
GROUPS = ["group-A", "group-B", "group-C"]
MESSAGES_PER_GROUP = 5
WORKER_COUNT = 3
IDLE_ROUNDS_BEFORE_STOP = 2


def setup_fifo():
    client = AWSClient().get_client('sqs')
    res = client.create_queue(
        QueueName=FIFO_QUEUE_NAME,
        Attributes={
            "FifoQueue": "true",
            "ContentBasedDeduplication": "true"
        }
    )
    print(f"FIFO queue ready: {res['QueueUrl']}")
    return res["QueueUrl"]


def produce_grouped(queue_url):
    client = AWSClient().get_client('sqs')
    for group_id in GROUPS:
        for seq in range(1, MESSAGES_PER_GROUP + 1):
            client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps({"group": group_id, "seq": seq}),
                MessageGroupId=group_id,
                MessageDeduplicationId=str(uuid.uuid4())
            )
            print(f"sent group={group_id} seq={seq}")


def worker(worker_id, queue_url):
    client = AWSClient().get_client('sqs')
    idle_rounds = 0

    while idle_rounds < IDLE_ROUNDS_BEFORE_STOP:
        res = client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5,
            AttributeNames=["MessageGroupId"]
        )
        messages = res.get("Messages", [])
        if not messages:
            idle_rounds += 1
            continue

        idle_rounds = 0
        msg = messages[0]
        body = json.loads(msg["Body"])
        group_id = msg["Attributes"]["MessageGroupId"]
        print(f"[worker-{worker_id}] processing group={group_id} body={body}")

        client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg["ReceiptHandle"]
        )

    print(f"[worker-{worker_id}] idle, stopping")


if __name__ == "__main__":
    queue_url = setup_fifo()
    produce_grouped(queue_url)

    threads = [
        threading.Thread(target=worker, args=(i, queue_url))
        for i in range(1, WORKER_COUNT + 1)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("all workers done")
