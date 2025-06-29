#!/bin/sh

################################################################################
# ----------------------------- HELPER FUNCTIONS ----------------------------- #
################################################################################

readvalue() {
    read -r -p "$1 ($2): " reply
    if [ -n "$reply" ]; then echo "$reply"
    else echo "$2";
    fi
}

readyn() {
    read -r -p "$1 [Yn]: " reply
    if [ -z "$reply" -o "$reply" = "y" ]; then echo 0
    else echo 1
    fi
}


################################################################################
# ---------------------------- PLATFORM DEFAULTS ----------------------------- #
################################################################################

os=`uname -o`
if [ "$os" = "GNU/Linux" ]; then
    echo "Running under Linux ($os)"
    git="git"
    python="python3"
    path="$HOME/.local/opt/furet"
    entryPath="$HOME/.local/share/applications/furet.desktop"
else
    echo "Running under Windows ($os)"
    git="git"
    python="python"
    path="$(realpath "$LOCALAPPDATA")/Programs/Furet"
    entryPath="$(realpath "$APPDATA")/Microsoft/Windows/Start Menu/Programs/Furet.lnk"
fi


################################################################################
# ------------------------------ CONFIGURATION ------------------------------- #
################################################################################
echo ""
echo "Configuration of the installation"

# git 
git=`readvalue "Path to git binary" $git`
gitVersion=`$git --version`
if [ $? -ne 0 ]; then
    echo "$git returned an error"
    echo "Exiting"
    exit 1
fi
gitVersion=`echo "$gitVersion" | sed -nr "s/^git version ([0-9]+\.[0-9]+\.[0-9]+)/\1/p"`
if [ -z "$gitVersion" ]; then
    echo "$git is not a git binary"
    echo "Exiting"
    exit 1
fi
echo "Using git $gitVersion ($git)"

# python
python=`readvalue "Path to python binary >=3.11 <3.13" $python`
pythonVersion=`$python --version`
if [ $? -ne 0 ]; then
    echo "$python returned an error"
    echo "Exiting"
    exit 1
fi
pythonVersion=`echo "$pythonVersion" | sed -nr "s/^Python ([0-9]+\.[0-9]+\.[0-9]+)$/\1/p"`
if [ -z "$pythonVersion" ]; then
    echo "$python is not a python binary"
    echo "Exiting"
    exit 1
fi
echo "3.11 $pythonVersion 3.13" | tr " " "\\n" | sort -V -C
if [ $? -ne 0 -o "$pythonVersion" = "3.13" ]; then
    echo "python version must be >=3.11 <3.13 ($python is $pythonVersion)"
    echo "Exiting"
    exit 1
fi
echo "Using python $pythonVersion ($python)"

# Installation path
path=`readvalue "Installation directory" $path`
path=`realpath $path`
if [ $? -ne 0 -o -e "$path" ]; then
    echo "\"$path\" already exists. Remove it first to install furet"
    echo "Exiting"
    exit 1
fi
echo "Using install directory \"$path\""

# Desktop entry
addEntry=`readyn "Add a desktop entry"`
if [ "$addEntry" -eq 0 -a -e "$entryPath" ]; then
    echo "\"$entryPath\" already exists. Remove it first to install furet on do not add a desktop entry"
    echo "Exiting"
    exit 1
fi


################################################################################
# ---------------------------- VALIDATING CONFIG ----------------------------- #
################################################################################
echo ""
echo "Furet will be installed at \"$path\" with git $gitVersion ($git) and python $pythonVersion ($python)"
if [ "$addEntry" -eq 0 ]; then
    echo "Desktop entry \"Furet\" will be added (\"$entryPath\")"
else 
    echo "No desktop entry will be added"
fi

install=`readyn "Proceed with installation"`
if [ "$install" -ne 0 ]; then
    echo "Installation Cancelled"
    exit 0
fi


################################################################################
# ------------------------------- INSTALLATION ------------------------------- #
################################################################################
echo ""
echo "Installing furet..."

remote="https://github.com/Hexoplanete/Projet-Furet.git"
echo "Cloning the latest tag of \"$remote\" to \"$path\"..."
version=`$git ls-remote --refs --tags --sort="v:refname" $remote | tail -n 1 | sed 's/.*\///'`
if [ $? -ne 0 -o -z "$version" ]; then
    echo "Failed to fetch the latest tag"
    echo "Exiting"
    exit 0
fi
echo "Latest tag is $version"
$git clone --depth 1 --branch $version --single-branch $remote "$path"
if [ $? -ne 0 ]; then
    echo "Failed to clone repository"
    echo "Exiting"
    exit 0
fi

cd "$path"
echo "Setting up environment (\"./scripts/setup.bash\")..."
bash ./scripts/setup.bash $python
if [ $? -ne 0 ]; then
    echo "Failed to setup environment"
    echo "Exiting"
    exit 0
fi

if [ "$addEntry" -eq 0 ]; then
    echo "Adding desktop entry..."
    if [ "$os" = "GNU/Linux" ]; then
        echo "[Desktop Entry]
Name=Furet
Comment=Fouille Universelle de Recueils pour Entreposage et Traitement
GenericName=Gestionnaire d'arrêtés
Exec=\"$path/bin/furet\"
Icon=$path/assets/furet-logo.ico
Type=Application
StartupNotify=false
Categories=Office;
Keywords=furet;" > $entryPath
    else
        powershell "\$ShortcutFile = \"$entryPath\"
\$WScriptShell = New-Object -ComObject WScript.Shell
\$Shortcut = \$WScriptShell.CreateShortcut(\$ShortcutFile)
\$Shortcut.TargetPath = \"powershell\"
\$Shortcut.Arguments = \"-ExecutionPolicy Bypass \"\"$(cygpath -w "$path/bin/furet.ps1")\"\"\"
\$shortcut.IconLocation = \"$(cygpath -w "$path/assets/furet-logo.ico")\"
\$Shortcut.Save()"
    fi
fi


################################################################################
# -------------------------------- LAUNCHING --------------------------------- #
################################################################################
echo ""
echo "Installation complete!"

if [ "$os" = "GNU/Linux" ]; then command="$path/bin/furet"
else command="powershell -ExecutionPolicy Bypass \"$(cygpath -w "$path/bin/furet.ps1")\""
fi

echo "You can now launch Furet with the following command: \"$command\""
if [ "$addEntry" -eq 0 ]; then echo "or from your application launcher directly under the name \"Furet\""; fi