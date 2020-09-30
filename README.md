（1）安装zabbix-agent
（2）配置zabbix_agentd.conf:
在zabbix_agentd.d目录下添加一个配置文件，内容为：
UserParameter=discovery_apname,/usr/lib/zabbix/externalscripts/apdiscovery.py
UserParameter=ap.status[*],/usr/lib/zabbix/externalscripts/apstatus.py $1
UserParameter=ap.clients[*],/usr/lib/zabbix/externalscripts/apclient.py $1
（3）修改zabbix_agentd.conf，Timeout=30和UnsafeUserParameters=1
（4）配置zabbix页面，添加主机，方式选择agent，然后配置其自动发现、Item prototypes和触发器。
PS:LLD宏的格式{#宏变量名}，使用参数ap.status[{#APNAME}]
