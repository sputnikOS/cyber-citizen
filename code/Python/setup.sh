#!/bin/bash
# Bash Script for install sputnikOS tools
# Must run to install tool

clear
echo "

██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ███████╗██████╗
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██╔════╝██╔══██╗
██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     █████╗  ██████╔╝
██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██╔══╝  ██╔══██╗
██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗███████╗██║  ██║
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
";

sudo chmod +x uninstall

if [ "$PREFIX" = "/data/data/com.termux/files/usr" ]; then
    INSTALL_DIR="$PREFIX/usr/share/doc/sputnikOS"
    BIN_DIR="$PREFIX/bin/"
    BASH_PATH="$PREFIX/bin/bash"
    TERMUX=true

    pkg install -y git python2
elif [ "$(uname)" = "Darwin" ]; then
    INSTALL_DIR="/usr/local/sputnikOS"
    BIN_DIR="/usr/local/bin/"
    BASH_PATH="/bin/bash"
    TERMUX=false
else
    INSTALL_DIR="$HOME/.sputnikOS"
    BIN_DIR="/usr/local/bin/"
    BASH_PATH="/bin/bash"
    TERMUX=false

    sudo apt-get install -y git python3
fi

echo "[✔] Checking directories...";
if [ -d "$INSTALL_DIR" ]; then
    echo "[◉] A directory was found! Do you want to replace it? [Y/n]:" ;
    read -r mama
    if [ "$mama" = "y" ]; then
        if [ "$TERMUX" = true ]; then
            rm -rf "$INSTALL_DIR"
            rm "$BIN_DIR/sputnikOS*"
        else
            sudo rm -rf "$INSTALL_DIR"
            sudo rm "$BIN_DIR/sputnikOS*"
        fi
    else
        echo "[✘] If you want to install you must remove previous installations [✘] ";
        echo "[✘] Installation failed! [✘] ";
        exit
    fi
fi
echo "[✔] Cleaning up old directories...";


echo "[✔] Installing ...";
echo "";
git clone --depth=1 https://github.com/sputnikOS "$INSTALL_DIR";
echo "#!$BASH_PATH
python $INSTALL_DIR/start.py" "${1+"$@"}" > "$INSTALL_DIR/sputnikOS";
chmod +x "$INSTALL_DIR/sputnikOS";
if [ "$TERMUX" = true ]; then
    cp "$INSTALL_DIR/sputnikOS" "$BIN_DIR"
    cp "$INSTALL_DIR/sputnikOS.cfg" "$BIN_DIR"
else
    sudo cp "$INSTALL_DIR/sputnikOS" "$BIN_DIR"
    sudo cp "$INSTALL_DIR/sputnikOS.cfg" "$BIN_DIR"
fi
rm "$INSTALL_DIR/sputnikOS";


if [ -d "$INSTALL_DIR" ] ;
then
    echo "";
    echo "[✔] Tool installed successfully! [✔]";
    echo "";
    echo "[✔]====================================================================[✔]";
    echo "[✔]      All is done!! You can execute tool by typing sputnikOS !       [✔]";
    echo "[✔]====================================================================[✔]";
    echo "";
else
    echo "[✘] Installation failed! [✘] ";
    exit
fi
