## real-time-object-processing
This project lays out thoughts on how to go about a real-time object detection system using video streams.

### Current existing tooling
- If running in a cloud service, something like AWS's [kinesis video streams](https://aws.amazon.com/kinesis/video-streams/features/?nc=sn&loc=2) is probably a good choice for storage while adding in hooks for inference tools.
- Nvidia also has [DeepStream](https://developer.nvidia.com/deepstream-sdk) which was made for this purpose as well.


### This repo
This repo is set up to mock the below shown diagram using the following tools to help test a full system
setup:
- [fake rtsp stream](https://github.com/insight-platform/Fake-RTSP-Stream?tab=readme-ov-file)
- [localstack for mocking aws services](https://docs.localstack.cloud/overview/)

