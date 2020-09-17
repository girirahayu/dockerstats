#!/bin/bash

docker ps -a --filter "id=$1" --format "{\"Size\":\"{{.Size}}\"}"
