#!/bin/bash

docker run --rm \
    -u $(id -u):$(id -g) \
    -e BIN=llydnu-lambda \
    -v ${PWD}:/code \
    -v ${HOME}/.cargo/registry:/cargo/registry \
    -v ${HOME}/.cargo/git:/cargo/git \
    softprops/lambda-rust

