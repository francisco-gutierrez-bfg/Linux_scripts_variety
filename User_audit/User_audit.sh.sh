#!/bin/sh

for i in `cat /etc/passwd | sort | cut -f1,1 -d:`
 do
 user=$i;
 passwd -S $user | grep LK | awk '{print $1}' >> locked;
 passwd -S $user | grep NP | awk '{print $1}' >> nopass;
done
clear

for j in `cat locked`
 do
 groups $j >> locked_group
done
rm -rf locked

echo "Locked Users" > users_report
echo "" >> users_report
echo "User : Group" >> users_report
echo "" >> users_report

sort -k 2 locked_group >> ordenado_bloqueados
cat ordenado_bloqueados >> users_report
rm -rf locked_group ordenado_bloqueados

for k in `cat nopass`
 do
 groups $k >> passwordless_group
done
rm -rf nopass

echo "" >> users_report
echo "Passwordless users" >> users_report
echo "" >> users_report
echo "User : Group" >> users_report
echo "" >> users_report

sort -k 2 passwordless_group >> nopass_sorted
cat nopass_sorted >> users_report
rm -rf passwordless_group nopass_sorted

clear
echo "Generating report to users_report files..."
sleep 2
clear
more users_report
