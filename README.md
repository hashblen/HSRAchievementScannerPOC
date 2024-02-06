# HSR Achievement Scanner POC
This is a quickly hacked together Achievement scanner for Honkai: Star Rail.
It uses a virtual controller to navigate through the menus, and is able to upload the
achievements to the best tracker for them around, [stardb.gg](https://stardb.gg).

## Installation
In you pip environment, you need to install `pywin32 vgamepad requests Levenshtein pytesseract`.
Vgamepad will probably ask you to install a driver for it to work. Follow the instructions.

Now go in main.py and change the global variables at the beginning according to you choices.

#### If you want to upload the achievements to stardb, do the following:
Go and retrieve your cookie from stardb (you need to be logged in).
For that, open the developer menu by pressing F12 in the tracker and go the network tab, then check and uncheck an achievement.
You now see an achievement at the bottom. Click on it and scroll down until you see `Cookie: _____`.
Copie the value in it following `id:`.
Copy that value and remember it.

## Running

### User Graphical interface

Run `gui.py`.

### Command-Line Interface

Run `main.py`. Command line arguments can be seen by doing `python main.py --help`.

DO NOT MOVE THE MOUSE OR TOUCH THE KEYBOARD WHILE IT IS RUNNING, AS HSR WILL GO BACK TO MOUSE+KEYBOARD MODE AND EVERYTHING WILL BREAK!

To stop the scanner while it is running, you just have to Alt+Tab.