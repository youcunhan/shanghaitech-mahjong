#!/bin/bash

while true; do
  bash bin/unidbg-fetch-qsign --basePath=txlib/8.9.63
  echo "签名服务异常终止, 将在 3 秒后重新启动"
  sleep 3
done