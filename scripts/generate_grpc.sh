#!/bin/sh
# Generate gRPC Python stubs
python -m grpc_tools.protoc -I=proto --python_out=services --grpc_python_out=services proto/trading.proto
