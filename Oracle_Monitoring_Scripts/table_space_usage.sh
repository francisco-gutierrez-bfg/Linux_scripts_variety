#!/bin/sh
clear
#echo ""
echo ""
echo "TABLESPACES USAGE"
sqlplus sys/<password>@<instance> as sysdba << EOF | grep -v "SQL\|rows\|Oracle\|Connected" | sed s'/TABLESPACE_NAME/TABLESPACE NAME/g' |sed s'/USED (M/USAGE M/g'|sed s'/FREE (MB/FREE MB/g'|sed s'/TOTAL (M/TOTAL MB/g'|sed s'/PER_FR/\%FREE/g'| sed '1d' |sed '2d' | sed '3d'

set feed off
set linesize 100
set pagesize 200
spool tablespace.alert
SELECT F.TABLESPACE_NAME,
TO_CHAR ((T.TOTAL_SPACE - F.FREE_SPACE),'999,999') "USED (MB)",
TO_CHAR (F.FREE_SPACE, '999,999') "FREE (MB)",
TO_CHAR (T.TOTAL_SPACE, '999,999') "TOTAL (MB)",
TO_CHAR ((ROUND ((F.FREE_SPACE/T.TOTAL_SPACE)*100)),'999')||' %' PER_FREE
FROM   (
SELECT       TABLESPACE_NAME,
ROUND (SUM (BLOCKS*(SELECT VALUE/1024
FROM V\$PARAMETER
WHERE NAME = 'db_block_size')/1024)
) FREE_SPACE
FROM DBA_FREE_SPACE
GROUP BY TABLESPACE_NAME
) F,
(
SELECT TABLESPACE_NAME,
ROUND (SUM (BYTES/1048576)) TOTAL_SPACE
FROM DBA_DATA_FILES
GROUP BY TABLESPACE_NAME
) T
WHERE F.TABLESPACE_NAME = T.TABLESPACE_NAME
AND (ROUND ((F.FREE_SPACE/T.TOTAL_SPACE)*100)) < 10;
spool off
exit;
END;
EOF
rm -rf tablespace.alert
echo ""
#if [ `cat tablespace.alert|wc -l` -gt 0 ]
#then
#cat tablespace.alert -l tablespace.alert > tablespace.tmp
#mailx -s "TABLESPACE ALERT for ${2}" $DBALIST < tablespace.tmp
#fi
