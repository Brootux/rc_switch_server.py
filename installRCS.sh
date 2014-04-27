#!/bin/bash
# Install script for rc_switch

if [ ! $(id -u) -eq "0" ]
then
    echo
    echo "You have to run this script as root (sudo)!"
    echo
    exit 1
fi


echo
echo "###################################################################"
echo "# Update of apt-get"
echo "###################################################################"
echo
apt-get update


echo
echo "###################################################################"
echo "# Setup of apt-get packages"
echo "###################################################################"
echo
apt-get -y install git-core python-dev python-setuptools


echo
echo "###################################################################"
echo "# Installing WiringPi into /etc/local/src/wiringPi"
echo "###################################################################"
echo
cd /usr/local/src
git clone git://git.drogon.net/wiringPi
cd wiringPi
sudo ./build
cd ..


echo 
echo "###################################################################"
echo "# Installing WiringPi-Python into /etc/local/src/WiringPi-Python"
echo "###################################################################"
echo
git clone https://github.com/WiringPi/WiringPi-Python.git
cd WiringPi-Python
git submodule update --init
python setup.py install


echo 
echo "###################################################################"
echo "# Installing RC-Switch for console into /usr/local/"
echo "###################################################################"
echo
chmod 755 rc_switch_console/*
cp rc_switch_console/* /usr/local/


echo 
echo "###################################################################"
echo "# Installing RC-Switch-Server into /usr/local/rc_switch_server"
echo "###################################################################"
echo
cp rc_switch_server/rc_switch_server /etc/init.d/
cp -R rc_switch_server/ /usr/local/
/usr/local/bin/gpio export 23 out
service rc_switch_server start


echo "###################################################################"
echo "# Default wire setup:"
echo "#"
echo "#   RPI             Transmitter"
echo "#  x x"
echo "#  x o -5V ------------- VCC"
echo "#  x o -GND ------------ GND"
echo "#  x x"
echo "#  x x"
echo "#  x x"
echo "#  x x"
echo "#  x o -GPIO23 --------- DATA"
echo "#  ..."
echo "###################################################################"
echo
echo "###################################################################"
echo "# The following new commands are now ready for use:"
echo "#     - rc_switch.py"
echo "#         Use this command to conrol your rc-switches via console"
echo "#     - rc_switch_server.py"
echo "#         This is installed as a deamon, you can conrol the"
echo "#         behaviour of this deamon via"
echo "#             sudo service rc_switch_server start|stop|restart"
echo "###################################################################"
echo
echo "###################################################################"
echo "# What you now have to do manually:"
echo "#"
echo "# > sudo vi /etc/rc.local"
echo "#    add BEFORE ->exit 0<- the line"
echo "#    ->sudo -u pi /usr/local/bin/gpio export 23 out<-"
echo "#"
echo "#    !!!maybe you should use another user or gpio port !!!"
echo "#       (see Default wire setup)"
echo "#"
echo "# > sudo shutdown -r now"
echo "#"
echo "###################################################################"
