#!/bin/bash
# Dveloped by Francisco Gutierrez

# This script will allow you to install y configure Kennetmon Utility to certify network bandwidth.

yum update -y kernel* openssh firewalld iptables 

# Disabling SeLinux
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

# Installing dependencies:
yum install -y iperf3 git epel-release 
yum install -y nodejs npm

# Running iperf collection (alternativelly, you can install iperf3 on clients and do the same)
# Be aware that firewall cannot be active in client side.
iperf3 -s -D
# Adding iperf3 collection routine at system startup
echo "iperf3 -s -D" >> /etc/rc.local

# Adding firewall rules:
firewall-cmd --permanent --zone=public --add-port=8080/tcp
firewall-cmd --reload
#systemctl disable firewalld

# Downloading and installing KentNetMon
cd /opt
git clone https://github.com/IceQubed/kentnetmon.git
cd /opt/kentnetmon && npm install && npm install forever -g

# Downgrade Mongoose
npm remove mongoose
npm install mongoose@4.10.8 --save

# Configuring KenNetMon
sed -i 's/USERNAME/iperfadm/g' database.js && sed -i 's/PASSWORD/mcciperf2021/g' database.js && sed -i 's/DATABASENAME/kentnetmon/g' database.js

# Adding mongo 3.4 repo
cat > /etc/yum.repos.d/mongo.repo << EOF
[mongodb-org-3.4]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7/mongodb-org/3.4/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.4.asc
EOF

# Installing mongo 3.4
yum -y install mongodb-org

# Starting and enabling mongodb
systemctl start mongod.service
systemctl enable mongod.service
systemctl status mongod.service

# Create mongo admin user
mongo admin --eval "db.createUser({user: 'mccadmin', pwd: 'mccmongoadm2021', roles: [{role: 'userAdminAnyDatabase', db: 'admin'}]})"

mongo <<EOF
use kentnetmon
db.createUser(
{
	user: "iperfadm",
	pwd: "mcciperf2021",
	roles:[{role: "readWrite" , db:"kentnetmon"}]})
EOF

# Enabling mongodb security:
sed -i 's/#security/security/g' /etc/mongod.conf
sed -i '/^security/a \ \ authorization: enabled' /etc/mongod.conf

# Mongodb kernel tuning
echo "mongod soft nproc 32000" >> /etc/security/limits.d/20-nproc.conf

# Starting and enabling mongodb
systemctl stop mongod.service
systemctl start mongod.service
systemctl status mongod.service

# Starting KentNetMon
forever start start.js


