# Based on instructions at
# https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

sudo apt update
sudo apt upgrade
sudo apt install mysql-server
# sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';"
# sudo mysql_secure_installation
# mysql -u root -p -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;"
sudo mysql -e "CREATE USER 'craapp'@'localhost' IDENTIFIED BY 'DBPa55w0rd';GRANT ALL PRIVILEGES ON *.* TO 'craapp'@'localhost' WITH GRANT OPTION;FLUSH PRIVILEGES;"
# mysql -u craapp -p -e "CREATE DATABASE cra;"
sudo mysql -e "CREATE DATABASE cra;"

sudo apt install python3-pip

pip install -r requirements.txt
