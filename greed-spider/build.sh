#! /bin/bash

clean() {
    rm -rf ./dist
    rm -rf ./*.egg-info
}

clean
uv build
uv pip install dist/*.whl
clean
