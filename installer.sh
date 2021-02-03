#!/bin/sh

# Shell script to install odrive Sync Agent and odrive-x

# Enables Universe repository and updates the system

echo "Get update"
sudo add-apt-repository universe && sudo apt-get update

# installs pip3

echo "Installing pip3"
sudo apt install python3-pip -y

# installs PyQt5, PyQtWebEngine

echo "Installing PyQt5"
pip3 install PyQt5
echo "Installing PyQtWebEngine"
pip3 install PyQtWebEngine

# installs curl

echo "Installing curl"
sudo apt install curl

# download odrive sync agent

ODRIVE_SYNC_AGENT_PATH="$HOME/.local/bin"
echo "Get odrive Sync Agent"
curl -L "https://dl.odrive.com/odrive-py" --create-dirs -o "$ODRIVE_SYNC_AGENT_PATH/odrive.py"
curl -L "https://dl.odrive.com/odriveagent-lnx-64" | tar -xvzf- -C "$ODRIVE_SYNC_AGENT_PATH/"

# make the odrive sync agent files executable

echo "Setting up odrive Sync Agent"
cd .local/bin/
chmod +x *
cd $HOME

# download odrive-x

echo "Get odrive-x"
wget https://github.com/absdarekar/odrive-x/archive/master.zip
echo "Unpacking odrive-x"
unzip master.zip -d $HOME
mv $HOME/odrive-x-master/ $HOME/odrive-x/
rm master.zip

# make .desktop file of odrive-x

echo "Setting up odrive-x"
ODRIVEX_DESKTOP_LAUNCHER_PATH="$HOME/.local/share/applications"
echo "[Desktop Entry]" >> $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop
echo "Version=1.0" >> $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop
echo "Type=Application" >> $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop
echo "Terminal=false" >> $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop
echo "Name[en_IN]=odrive-x" >> $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop
echo "Exec=python3 $HOME/odrive-x/bin/Odrivex.py" >> $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop
echo "Name=odrive-x" >> $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop
echo "Icon=$HOME/odrive-x/icon/odrive.png" >> $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop

chmod 777 $ODRIVEX_DESKTOP_LAUNCHER_PATH/odrivex.desktop

echo "Done"
