import os
from loguru import logger
import numpy as np
import boto3
import torch
import json
import time

os.environ["AWS_ACCESS_KEY_ID"] = os.environ.get("AWS_ACCESS_KEY_ID", "test")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ.get("AWS_SECRET_ACCESS_KEY", "test")

s3_client = boto3.client("s3", endpoint_url="http://localhost.localstack.cloud:4566")
sqs_client = boto3.client(
    "sqs",
    endpoint_url="http://localhost:4566",
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
)
queue_url = sqs_client.get_queue_url(QueueName=os.environ.get("SQS_QUEUE_NAME", "raw-frame-queue"))[
    "QueueUrl"
]
logger.info(f"getting images from queue located at {queue_url}")

max_batch_inference_size = 5


def retreive_images(messages: list[dict]) -> tuple[list[dict], list[np.ndarray]]:
    parsed_bodies = []
    images = []
    for m in messages["Messages"]:
        msg = json.loads(m["Body"])
        parsed_bodies.append(msg)
        image = np.frombuffer(
            s3_client.get_object(Bucket=msg["s3_bucket"], Key=msg["s3_key"])["Body"].read(),
            dtype=int,
        )
        image.shape = (msg["height"], msg["width"], 3)
        images.append(image.astype(float))

    return parsed_bodies, images


if __name__ == "__main__":
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
    while True:
        messages = sqs_client.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=max_batch_inference_size
        )
        if messages.get("Messages", False):
            metadata, images = retreive_images(messages)
            results = model(images)
            logger.info("successful inference")
            sqs_client.delete_message_batch(
                QueueUrl=queue_url,
                Entries=[
                    {"ReceiptHandle": m["ReceiptHandle"], "Id": m["MessageId"]}
                    for m in messages["Messages"]
                ],
            )
            continue
        logger.info("queue empty")
        time.sleep(0.05)
