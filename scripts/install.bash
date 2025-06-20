#!/bin/bash

readValue() {
    read -r -p "$1 ($2): " reply
    if [[ ! -z "$reply" ]] then echo "$reply"
    else echo "$2"; fi
}

SOURCE_DIR="$(dirname "$(realpath "$0")")"


################################################################################
# ------------------------------ CONFIGURATION ------------------------------- #
################################################################################
echo "Configuring of the installation..."

# git 
git=`readValue "Path to git binary" "git"`
gitVersion=`$git --version`
gitTest=$?
if [[ $gitTest != 0 ]] then
    echo "$git returned an error"
    echo Exiting
    exit 1
fi
gitRegex="git version ([0-9]+\.[0-9]+\.[0-9]+)"
if [[ ! $gitVersion =~ $gitRegex ]] then
    echo "$git is not a git binary"
    echo Exiting
    exit 1
fi
gitVersion=${BASH_REMATCH[1]}
echo "Using git $gitVersion ($git)"

# python
python=`readValue "Path to python binary >=3.9 <3.13" "python3"`
pythonVersion=`$python --version`
pythonTest=$?
if [[ $pythonTest != 0 ]] then
    echo "$python returned an error"
    echo Exiting
    exit 1
fi
pythonRegex="Python ([0-9]+\.[0-9]+\.[0-9]+)"
if [[ ! $pythonVersion =~ $pythonRegex ]] then
    echo "$python is not a python binary"
    echo Exiting
    exit 1
fi
pythonVersion=${BASH_REMATCH[1]}
echo -e "3.9 $pythonVersion 3.13" | tr " " "\\n" | sort -V -C -t " "
pythonVersionTest=$?
if [[ $pythonVersion == "3.13" || $pythonVersionTest != 0 ]] then
    echo "python version must be >=3.9 <3.13 ($python is $pythonVersion)"
    echo Exiting
    exit 1
fi
echo "Using python ${pythonVersion} ($python)"


# Installation path
path=`readValue "Installation directory" "~/.local/opt/furet"`
path=`realpath ${path/#\~/$HOME}`
if [[ -d "$path" ]] then
    echo "\"$path\" already exists. Remove it first to install furet"
    echo Exiting
    exit 1
fi
echo "Using install directory \"$path\""

# Desktop entry
read -r -p "Add a desktop entry [Yn]: " reply
if [[ -z "$reply" || $reply == "y" ]] then
    desktopEntry="$HOME/.local/share/applications/furet.desktop"
    echo "Desktop entry Furet will be added (\"$desktopEntry\")"
fi


################################################################################
# ---------------------------- VALIDATING CONFIG ----------------------------- #
################################################################################
echo -e "\nFuret will be install at \"$path\" with git $gitVersion ($git) and python $pythonVersion ($python)"

read -r -p "Proceed with installation [Yn]: " reply
if [[ ! -z "$reply" && $reply != "y" ]] then
    echo "Installation Cancelled"
    exit 0
fi


################################################################################
# ------------------------------- INSTALLATION ------------------------------- #
################################################################################
echo -e "\nInstalling furet..."

# TODO clone tag branch only
remote=https://github.com/Hexoplanete/Projet-Furet.git
echo "Cloning the latest tag of \"$remote\" to \"$path\"..."
version=`$git ls-remote --refs --tags --sort="v:refname" $remote | tail -n 1 | sed 's/.*\///'`
echo "Latest tag is $version"
$git clone --depth 1 --branch $version --single-branch $remote "$path"
gitClone=$?
if [[ $gitClone != 0 ]] then
    echo "Failed to clone repository"
    echo Exiting
    exit 0
fi

echo "Creating virtual environment..."
cd "$path"
$python -m venv .venv
$venv=$?
if [[ $venv != 0 ]] then
    echo "Failed to create virtual environment"
    echo Exiting
    exit 0
fi

echo "Installing dependencies..."
source .venv/bin/activate
pip install uv && uv sync
$dependencies=$?
if [[ $dependencies != 0 ]] then
    echo "Failed to install dependencies"
    echo Exiting
    exit 0
fi

if [[ ! -z $desktopEntry ]] then
    echo "Adding desktop entry..."
    echo "[Desktop Entry]
Name=Furet
Comment=Fouille Universelle de Recueils pour Entreposage et Traitement
GenericName=Gestionnaire d'arrêtés
Exec=\"$path/bin/furet\"
Icon=$path/assets/furet-logo.ico
Type=Application
StartupNotify=false
Categories=Office;
Keywords=furet;" > $desktopEntry
fi


################################################################################
# -------------------------------- LAUNCHING --------------------------------- #
################################################################################
echo -e "\nInstallation complete!"

echo "You can now launch Furet with the following command: 'bash -c \"cd \\\"$path\\\" && source .venv/bin/activate && python -m furet\"'"
if [[ ! -z $desktopEntry ]] then echo "or from your application launcher directly under the name \"Furet\""; fi