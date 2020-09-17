
#info@girirahayu.com

import subprocess
import json
import csv
import sys
import datetime

d = datetime.datetime.today()

def command(string):
    proc = subprocess.Popen([string], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out.decode().replace('\n','')

def Convert(string): 
    li = list(string.split(", ")) 
    return li 

def read_config(json_node, string):
    with open('config.json') as json_data:
        if string is None:
            d = json.load(json_data)
            return d[json_node]
        else:
            d = json.load(json_data)
            return d[json_node][string]


stack = read_config('stack_name',None)

for n in range(0, len(stack)):

    data = command('./container.sh '+stack[n]).strip(",")
    
    if data != "":
        dj = Convert(data)

        row = [["Stack:",stack[n]],["No","BlockIO","CPUPerc","Container","ID","MemPerc","MemUsage","Name","NetIO","TotalFileSize"]]
        volrow = [["volume:"],["No","ContainerName","Type","Source","Destination","VolumeSize"]]
       
        for x in range(0, len(dj)):
            parsed_json = (json.loads(dj[x]))
            
            getSize = command('./size.sh '+ parsed_json['ID'])
            sizeJson = json.loads([getSize][0])
            #print(sizeList['Size'])

            row_list = [x, parsed_json['BlockIO'], parsed_json['CPUPerc'], parsed_json['Container'], parsed_json['ID'],parsed_json['MemPerc'],parsed_json['MemUsage'],parsed_json['Name'],parsed_json['NetIO'],sizeJson['Size']]    
            row.append(row_list)

            getVolume = command('./volume.sh '+ parsed_json['ID'])
            volumeJson = json.loads(getVolume)

            for v in range(0, len(volumeJson)):
                #print(volumeJson[v]["Source"])
                cmd = "du -sh " + volumeJson[v]["Source"] + """ | awk '{print $1}'"""
                volsize = command(cmd)
                vol_list = [v,parsed_json['Name'],volumeJson[v]["Type"],volumeJson[v]["Source"],volumeJson[v]["Destination"],volsize]
                volrow.append(vol_list)
            

        with open(stack[n]+'-'+d.strftime("%d-%b-%Y")+'.csv', 'w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
            writer.writerows(row)
        with open(stack[n]+'-'+d.strftime("%d-%b-%Y")+'.csv', 'a+', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
            writer.writerows(volrow)