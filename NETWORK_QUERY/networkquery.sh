# Created by Francisco Gutierez G.
# Unix Engineer MASTEC 2013
basenet=$1
echo "Checking network IP address between $basenet.1 and $basenet.255..."
echo ""
echo "Base typed:"
if echo "$basenet" | egrep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
then
    # Checking address format, including if each octect is valid (octect <= 255) 
    checkipformat="$(echo $basenet | awk -F'.' '$1 <=255 && $2 <= 255 && $3 <= 255')"
    if [ -z "$checkipformat" ]
    then
       echo "The base network format is invalid; octects must be <= 255"
    else
    # If format looks good and all octets are valid...   
       for i in $(seq 1 254);
       do
         check=`ping -w 3 -c 1 $basenet.$i | grep "time="`
         name=`nslookup $basenet.$i | grep "name" | awk '{ print $4 }'`
         if [ -z "$check" ]
         #if [ -z `ping -w 3 -c 1 $basenet.$i | grep "time="` ]
         then
            echo "$basenet.$i  $name" >> available.txt
         else
            echo "$basenet.$i  $name" >> used.txt
         fi
       done
       clear
       echo "To see used ip addresses please open used.txt file"
       echo ""
       echo "To see available ip addresses please open available.txt file"
    fi
else
    echo "The network range was invalid or misstyped, you must type the network base (first three octects) xxx.xxx.xxx"
    echo "Usage: sh networkquery.sh xxx.xxx.xxx  or ./networkquery.sh xxx.xxx.xxx"
    echo "The last octect evaluated inside the script as a range between 1-255" 
fi
