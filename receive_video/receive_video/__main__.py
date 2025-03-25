import av
import os
import time
from loguru import logger
import boto3
import io
import json
import numpy as np

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
logger.info(f"putting images in queue located at {queue_url}")

if __name__ == "__main__":
    streaming_source = os.environ.get("STREAMING_SOURCE", None)
    if streaming_source is None:
        logger.error("No valid STREAMING_SOURCE specified.")
        exit(1)
    logger = logger.bind(streaming_source=streaming_source)
    logger.info(f"reading from streaming source {streaming_source}")
    destination_bucket = "raw-data"

    with av.open(streaming_source) as container:
        stream_start_time = time.time()  # to make a useful time out of the stream time

        for frame in container.decode(video=0):
            frame_time = frame.pts * frame.time_base
            absolute_timestamp = stream_start_time + frame_time
            frame_image: np.ndarray = frame.to_ndarray(format="bgr24").astype(int)
            h, w, c = frame_image.shape
            # logger.info(f"Server-Side Timestamp: {absolute_timestamp}")
            key = f"{streaming_source}/{absolute_timestamp}"
            s3_client.upload_fileobj(
                Fileobj=io.BytesIO(frame_image.tobytes()), Bucket=destination_bucket, Key=key
            )
            sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(
                    {
                        "source": streaming_source,
                        "timestamp": absolute_timestamp,
                        "s3_bucket": destination_bucket,
                        "s3_key": key,
                        "width": w,
                        "height": h,
                    }
                ),
            )
