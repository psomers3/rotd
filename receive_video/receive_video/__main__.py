import av
import os
import time
from loguru import logger
import boto3
import io

s3_client = boto3.client("s3", endpoint_url="http://localhost.localstack.cloud:4566")


if __name__ == "__main__":
    streaming_source = os.environ.get("STREAMING_SOURCE", None)
    if streaming_source is None:
        logger.error("No valid STREAMING_SOURCE specified.")
        exit(1)
    logger = logger.bind(streaming_source=streaming_source)
    logger.info(f"reading from streaming source {streaming_source}")
    
    with av.open(streaming_source) as container:
        # Record the stream start time as wall-clock time
        stream_start_time = time.time()
        
        for frame in container.decode(video=0):  # 'video=0' means the first video stream
            frame_time = frame.pts * frame.time_base
            absolute_timestamp = stream_start_time + frame_time
            frame_image = frame.to_ndarray(format="bgr24")
            logger.info(f"Server-Side Timestamp: {absolute_timestamp}")
            s3_client.upload_fileobj(Fileobj=io.BytesIO(frame_image.tobytes()), Bucket="raw-data", Key=f"{streaming_source}/{absolute_timestamp}")