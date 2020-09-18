
#info@girirahayu.com

import subprocess
import json
import csv
import sys
import datetime
import os
import socket

d = datetime.datetime.today()
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if os.path.isdir(ip_address) is False:
    os.makedirs(ip_address, 0o777, True)

def command(string):
    proc = subprocess.Popen([string], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out.decode().replace('\n','')

def Convert(string): 
    li = list(string.split(", ")) 
    return li 

awk = """ awk 'NR>1 {$1=$1","; print $1}' """
getNamespace = "kubectl get namespace | " + awk
strNamespace = command(getNamespace)
strNamespace = strNamespace[:-1].split(",")


for n in range(0, len(strNamespace)):

    awk_getDocker = """ awk 'NR>1 {$1=$1","; print $1}' """
    getPods = "kubectl get pods -n "+ strNamespace[n] +" | " + awk_getDocker 
    getPods = command(getPods)
    
    if getPods != "":
        getPods = getPods[:-1].split(",")
    
        for p in range(0, len(getPods)):
            # print(getPods[p])

            #filter = """ '{{ json .}}' """
            #cmd = "docker stats --no-stream --format "+filter+" | grep "+getPods[p]
            data = command('../container.sh '+getPods[p])
            data = data.strip(",")
            
            if data != "":
                dj = Convert(data)
                
                row = [["Namespace:",strNamespace[n]],["No","BlockIO","CPUPerc","Container","ID","MemPerc","MemUsage","Name","NetIO","TotalFileSize"]]
                volrow = [[],["volume:"],["#","ContainerName","Type","Source","Destination","VolumeSize"]]
       
                for x in range(0, len(dj)):
                    parsed_json = (json.loads(dj[x]))
                    
                    getSize = command('../size.sh '+ parsed_json['ID'])
                    sizeJson = json.loads([getSize][0])
                    #print(sizeList['Size'])

                    row_list = [x, parsed_json['BlockIO'], parsed_json['CPUPerc'], parsed_json['Container'], parsed_json['ID'],parsed_json['MemPerc'],parsed_json['MemUsage'],parsed_json['Name'],parsed_json['NetIO'],sizeJson['Size']]    
                    row.append(row_list)

                    getVolume = command('../volume.sh '+ parsed_json['ID'])
                    volumeJson = json.loads(getVolume)

                    for v in range(0, len(volumeJson)):
                        #print(volumeJson[v]["Source"])
                        cmd = "du -sh " + volumeJson[v]["Source"] + """ | awk '{print $1}'"""
                        volsize = command(cmd)
                        vol_list = [" ",parsed_json['Name'],volumeJson[v]["Type"],volumeJson[v]["Source"],volumeJson[v]["Destination"],volsize]
                        volrow.append(vol_list)
                    

                with open(ip_address+'/'+strNamespace[n]+'-'+d.strftime("%d-%b-%Y")+'.csv', 'w', newline='') as file:
                    writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
                    writer.writerows(row)
                with open(ip_address+'/'+strNamespace[n]+'-'+d.strftime("%d-%b-%Y")+'.csv', 'a+', newline='') as file:
                    writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
                    writer.writerows(volrow)


#compress
compress = "tar czvf "+ip_address+".tar.gz "+ip_address+"/"
command(compress)

#upload to s3
upload = "s3cmd put "+ip_address+".tar.gz s3://devops/resource/ --no-check-certificate --acl-public"
command(upload)