--algorithm ethash --pool us-south01.miningrigrentals.com:3344 --wallet YOUR_WALLET --password x

python africrypt_node.py

mkdir build && cd build
cmake africryptchain
make

pip install ecdsa flask

git clone https://github.com/Web4application/AfriCryptChain.git
cd AfriCryptChain

sudo su
mkdir /opt/zano-2-1-7-411
mkdir /opt/zano-bin
cd /opt/zano-2-1-7-411
wget "https://build.zano.org/builds/zano-linux-x64-release-v2.1.7.411[29d02c1].AppImage"
mv zano-linux-x64-release-v2.1.7.411\[29d02c1\].AppImage zano-linux-x64-release-v2.1.7.411\[29d02c1\].7z
7z x zano-linux-x64-release-v2.1.7.411\[29d02c1\].7z
cp /opt/zano-2-1-7-411/usr/bin/* /opt/zano-bin

useradd -M mmbot
usermod -L mmbot
sudo mkdir /opt/mmbot/
sudo cp target/TradeBot-1.0.jar /opt/mmbot/
cp mmbot.service /etc/systemd/system/mmbot.service
systemctl enable mmbot
systemctl start mmbot

sudo apt-get install openjdk-17-jdk maven
mvn clean install
java -jar target/TradeBot-1.0.jar

sudo python3 createKey.py tradebot.example.com /etc/mmbot/keys/

nano /etc/mmbot/config.yaml


rpcDaemonAddr: "127.0.0.1"
rpcDaemonPort: 11211
rpcWalletAddr: "127.0.0.1"
rpcWalletPort: 11221
rpcWalletAddrRefill: "127.0.0.1"
rpcWalletPortRefill: 11217
rpcWalletAddrAudit: "127.0.0.1"
rpcWalletPortAudit: 11219

dbPassword: <change this>

coinexApiKey: <change this >

sudo cp config.yaml /etc/mmbot
sudo mysql < marketmaker.sql marketmaker

apt-get install mariadb-server mariadb-client
sudo mysql
CREATE DATABASE marketmaker DEFAULT CHARACTER SET utf8;
CREATE USER 'marketmaker'@'localhost' IDENTIFIED by 'YOUR_PASSWORD_HERE';
CREATE USER 'marketmaker'@'127.0.0.1' IDENTIFIED by 'YOUR_PASSWORD_HERE';
GRANT ALL ON marketmaker.* TO 'marketmaker'@'localhost';
GRANT ALL ON marketmaker.* TO 'marketmaker'@'127.0.0.1';
FLUSH PRIVILEGES;
