#!/usr/bin/env python3

import paramiko
import time
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 建立连接
ssh.connect(hostname='10.119.15.245', port=22, username='hrb_adm', password='hrb@ldjt.adm.liu', timeout=5)
client = ssh.invoke_shell(width=80, height=80)
time.sleep(0.5)
buff = ''
buff = str(client.recv(65535), 'utf-8').strip()
buff = ''
client.send('display wlan ap all\n')
time.sleep(1)
# 获取数据
while not buff.endswith('>'):
    if -1 != buff.strip().find('---- More ----'):
        buff = buff.replace('---- More ----', '')
        client.send(' ')
    time.sleep(1)
    buff += str(client.recv(65535), 'utf-8').strip()

ap_list = buff.split('\n')
ap_name = ''
ap_names = []

# 去除无用的表头
go_on = True
for i in ap_list:
    if go_on and not i.startswith('AP name'):
        continue
    elif i.startswith('AP name'):
        go_on = False
        continue
    ap_name = i.split(' ')[0].strip()
    if '' == ap_name or ap_name.endswith('>'):
        continue
    else:
        ap_names.append({'{#APNAME}': ap_name})

#print(json.dumps({'data': ap_names}, sort_keys=True, indent=4, separators=(',', ':')))
print(json.dumps(ap_names, sort_keys=True, indent=4, separators=(',', ':')))


ssh.close()
