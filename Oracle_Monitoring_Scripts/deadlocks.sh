###################################################################
## deadlock_alert.sh ##
###################################################################
#!/bin/ksh
sqlplus sys/<password>@<instance> as sysdba <<EOF | grep -v "SQL"
set feed off
set heading off
spool deadlock.alert
SELECT   SID, DECODE(BLOCK, 0, 'NO', 'YES' ) BLOCKER,
DECODE(REQUEST, 0, 'NO','YES' ) WAITER
FROM     V\$LOCK
WHERE    REQUEST > 0 OR BLOCK > 0
ORDER BY block DESC;
spool off
exit
EOF
rm -rf deadlock.alert
#if [ `cat deadlock.alert|wc -l` -gt 0 ]
#then
#mailx -s "DEADLOCK ALERT for ${2}" $DBALIST < deadlock.alert
#fi
