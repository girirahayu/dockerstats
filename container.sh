#!/bin/bash

#list=`docker stats --no-stream --format "{\"Name\":\"{{ .Name }}\",\"memory\":{\"usage / limit\":\"{{ .MemUsage }}\",\"percent\":\"{{ .MemPerc }}\"},\"cpu\":\"{{ .CPUPerc }}\"},"`
list=`docker stats --no-stream --format "{{ json . }},"`
#echo "["$list"]"
echo $list
#echo '{"data":['$list']}'

