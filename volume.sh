#!/bin/bash

docker inspect -f '{{ json .Mounts }}' $1