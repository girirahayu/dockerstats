#!/bin/bash

docker ps -a --format "{\"Size\":\"{{.Size}}\",\"ID\":\"{{.ID}}\"}" | grep $1
