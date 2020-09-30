#!/usr/bin/env python3

import paramiko
import time
import sys

if len(sys.argv)<2 :
    print("Nothing!! Something Wrong!")
else:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 建立连接
    ssh.connect(hostname='10.119.15.245', port=22, username='hrb_adm', password='hrb@ldjt.adm.liu', timeout=5)
    client = ssh.invoke_shell(width=80, height=80)
    time.sleep(0.5)
    buff = ''
    buff = str(client.recv(65535), 'utf-8').strip()
    buff = ''
    client.send('display wlan ap name ' + sys.argv[1] + ' \n')
    time.sleep(1)
    # 获取数据
    while not buff.endswith('>'):
        if -1 != buff.strip().find('---- More ----'):
            buff = buff.replace('---- More ----', '')
            client.send(' ')
        time.sleep(1)
        buff += str(client.recv(65535), 'utf-8').strip()

    ap_list = buff.split('\n')
    ap_status = ''
    ap_names = []

    # 去除无用的表头
    go_on = True
    for i in ap_list:
        if go_on and not i.startswith('AP name'):
            continue
        elif i.startswith('AP name'):
            go_on = False
            continue
        ap_status = i.split()[2].strip()
        break

    print(ap_status)
