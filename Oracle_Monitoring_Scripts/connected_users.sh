#!/bin/sh
clear
#echo ""
echo ""
echo "ACTIVE SESSIONS AND STATUS"
sqlplus sys/<password>@<instance> as sysdba << EOF | grep -v "SQL\|rows\|Oracle\|Connected" | sed s'/STATUS/SESSION STATUS/g' | sed s'/ACTIVE/ACTIVE SESSIONS/'g | sed s'/INACTIVE/INACTIVE SESSIONS/g' | sed '1d' |sed '2d' | sed '3d'
select
       substr(a.spid,1,9) pid,
       substr(b.sid,1,5) sid,
       substr(b.serial#,1,5) ser#,
       substr(b.machine,1,6) box,
       substr(b.username,1,10) username,
--       b.server,
       substr(b.osuser,1,8) os_user,
       substr(b.program,1,30) program
from v\$session b, v\$process a
where
b.paddr = a.addr
and type='USER'
order by spid; 
select status, count(1) as "CONNECTION COUNT" from V\$SESSION group by status;
exit;
END;
EOF
