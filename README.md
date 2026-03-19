# GavinWare V1
A parody game of one of Nintendo/Intelligent System's popular games: WarioWare.
(sorry if the installation tutorial is insulting other GitHub user's intelligence, but this will also be shared to my friends who are non GitHub users)
# Installation
## Windows
### Option 1: Terminal (If you have Git installed)
1. Open terminal (or Powershell), then go to a directory of your choosing.
2. Type the command:
```bash
git clone https://github.com/GavTechMaster/GavinWare-V1.git
```
### Option 2: File Explorer (If you don't have Git installed)
1. Download ZIP from GitHub
![Download ZIP GitHub](./download_zip.png)
2. Extract it within your Downloads (or the directory you installed it in).
### Opening the file:
#### Option 1: File Explorer
1. Right click on the main.py file, then Open with > Python (or Open with > Choose another app > Python)
![File Explorer main.py](./file_explore_open.png)
#### Option 2: Terminal
1. Open terminal (or Powershell) then type these commands:
```bash
# Make sure this is relative to you in CLI or make it an absolute path
cd GavinWare
```
```bash
# Make sure you're inside the GavinWare directory or you are using an absolute path
python main.py
```
### If you don't have python installed:
1. Go to python.org, then go to Downloads > "Or get the standalone installer for Python 3.X.X"
![Python.org Install](./python_install_windows.png)
### If you don't have the required dependencies:
1. Open terminal (or Powershell), FIND WHERE YOUR REQUIREMENTS DIRECTORY IS, then type these commands:
```bash
# Make sure this is relative to you in CLI or make it an absolute path
cd GavinWare
```
```bash
# Make sure you are inside the GavinWare directory or you are using an absolute path
pip install -r requirements.txt
```
2. If that doesn't work, just type this command to install them simultaneously:
```bash
pip install pygame-ce; pip install numpy
```
## MacOS
### Option 1: Terminal (If you have Git installed)
1. Open terminal, then go to a directory of your choosing.
2. Type the command:
```bash
git clone https://github.com/GavTechMaster/GavinWare-V1.git
```
### Option 2: Finder (If you don't have Git installed)
1. Download ZIP from GitHub
![Download ZIP GitHub](./download_zip.png)
2. Extract it within your Downloads (or the directory you installed it in).
### Opening the file:
#### Option 1: Finder
1. Double click on the main.py file, then open with Python.
#### Option 2: Terminal
1. Open terminal, then type these commands:
```bash
# Make sure this is relative to you in CLI or make it an absolute path
cd GavinWare
```
```bash
# Make sure you're inside the GavinWare directory or you are using an absolute path
python3 main.py
```
### If you don't have python installed:
1. Go to python.org, then go to Downloads > "Download for macOS Python 3.X.X"
![Python.org Install](./python_install_macos.png)
### If you don't have the required dependencies:
1. Open terminal, FIND WHERE YOUR REQUIREMENTS DIRECTORY IS, then type these commands:
```bash
# Make sure this is relative to you in CLI or make it an absolute path
cd GavinWare
```
```bash
# Make sure you are inside the GavinWare directory or you are using an absolute path
pip3 install -r requirements.txt
```
2. If that doesn't work, just type this command to install them simultaneously:
```bash
pip3 install pygame-ce; pip3 install numpy
```
## Linux
### Terminal
1. Install git:
```bash
sudo apt update && sudo apt install git
```
2. Type this command to clone this respitory to you computer:
```bash
git clone https://github.com/GavTechMaster/GavinWare-V1.git
```
3. Go inside the GavinWare directory and add executable permissions to the main.py file:
```bash
sudo chmod u+x main.py
```
4. Run the python file:
```bash
python3 main.py
```
### If you don't have python installed:
Type the commands:
```bash
sudo apt update
```
```bash
sudo apt install python3
```
### If you don't have the required dependencies:
1. Open terminal, FIND WHERE YOUR REQUIREMENTS DIRECTORY IS, then type these commands:
```bash
# Make sure this is relative to you in CLI or make it an absolute path
cd GavinWare
```
```bash
# Make sure you are inside the GavinWare directory or you are using an absolute path
pip3 install -r requirements.txt
```
2. If that doesn't work, just type this command to install them simultaneously:
```bash
pip3 install pygame-ce; pip3 install numpy
```
