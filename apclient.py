#!/usr/bin/env python3

import paramiko
import time
import sys
import json

if len(sys.argv) < 2:
    print("Nothing!! Something Wrong!")
else:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 建立连接
    ssh.connect(hostname='10.119.15.245', port=22, username='hrb_adm', password='hrb@ldjt.adm.liu', timeout=5)
    client = ssh.invoke_shell(width=80, height=80)
    time.sleep(0.5)
    buff = str(client.recv(65535), 'utf-8').strip()
    buff = ''
    client.send('display wlan client ap ' + sys.argv[1] + ' \n')
    time.sleep(1)
    # 获取数据
    while not buff.endswith('>'):
        if -1 != buff.strip().find('---- More ----'):
            buff = buff.replace('---- More ----', '')
            client.send(' ')
        time.sleep(1)
        buff += str(client.recv(65535), 'utf-8').strip()

    if '' == buff.strip():
        print(json.dumps('Nothing', sort_keys=True, indent=4, separators=(',', ':')))
    else:
        ap_list = buff.split('\n')
        ap_client_mac = ''
        ap_client_ip = ''
        ap_clients = []

        # 去除无用的表头
        go_on = True
        for i in ap_list:
            if go_on and not i.startswith('MAC address'):
                continue
            elif i.startswith('MAC address'):
                go_on = False
                continue
            elif i.startswith('<') and i.endswith('>'):
                break

            ap_client_mac = i.split()[0].strip()
            ap_client_ip = i.split()[4].strip()
            ap_clients.append({'{#CLIENT_MAC}': ap_client_mac,
                               '{#CLIENT_IP}': ap_client_ip
                               })
        print(json.dumps(ap_clients, sort_keys=True, indent=4, separators=(',', ':')))
