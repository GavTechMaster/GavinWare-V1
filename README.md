# GavinWare V1
A parody game of one of Nintendo/Intelligent System's popular games: WarioWare.
# Installation
## Windows
### If you don't have python installed:
1. Go to python.org, then select Downloads.
2. Select "get the standalone installer for Python 3.X.X" (for easier installation).
3. Open the installer and check the box "Add Python 3.X to PATH".
4. Click on "Install Now" and follow further default instructions.
### If you don't have the required dependencies:
1. Extract the GavinWare ZIP file.
2. Open terminal (or Powershell), FIND WHERE YOUR REQUIREMENTS DIRECTORY IS, then type these commands:
```bash
cd GavinWare
```
```bash
# Make sure you are inside the GavinWare folder or you are using an absolute path
pip install -r requirements.txt
```
4. If that doesn't work, just type this command to install them simultaneously:
```bash
pip install pygame-ce; pip install numpy
```
### Opening the file:
#### Option 1: File Explorer
1. Right click on the main.py file.
2. If you're on Windows 11 click Show more options > Open with > Python, otherwise if you're on Windows 10 click Open with > Python
#### Option 2: Command Line
1. Open terminal (or Powershell) then type these commands:
```bash
cd GavinWare
```
```bash
# Make sure you're inside the GavinWare folder or you are using an absolute path
python main.py
```
