#! /bin/bash

rm -rf ./dist
uv build
rm -rf ./*.egg-info
uv pip install dist/greed_spider-0.1.0-py3-none-any.whl
