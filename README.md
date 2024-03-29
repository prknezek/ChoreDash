# ChoreDash

Developed by Hungry Games: <br>
Payton Knezek, 
Hemanth Mukesh, 
Adnan Yusuf<br>

## Overview
ChoreDash is a 2D game developed in Python using the pygame library for the Capsher 2023 ACC Coding Challenge. It's a simple game where the player attempts to finish all of the tasks assigned to them within the time limit.

While taking a nice peaceful nap, you get a text message from your mom. Without even looking at your phone, you realize what you have done...

**YOU FORGOT TO DO THE CHORES!**
<br>
**HURRY UP AND GET THEM DONE BEFORE YOUR MOM GETS HOME!**

## How to Play

### General Gameplay
Run around and complete the tasks that are listed on the fridge within the time limit. The timer can be accessed from the phone. You will receive a score at the end with the option to try again.
<br>
Try to finish all the tasks within the time limit, and then try to do it as fast as possible!

Movement: WASD | W ⬆️, A ⬅️, S⬇️, D⬅➡️
<br>
Interact: E
<br>
Phone: Tab
<br>
Pause: Escape

### Dishwashing Mini-Game
The dirty dishes are chasing you!<br>
Have them touch the sponge to get them washed.<br>
Be careful, you only have three lives!<br>

Use the arrow keys to move the sponge!

## Design
### main.py
The main.py file holds the main game loop. The Game class is located here, which is the main class that runs the game. Here, all objects are initialized, and their respective run/update commands are called when necessary. Functions related to overall game flow are located here, such as loading screens, pause and retry mechanics, etc.
<br>
### player.py
The player.py file handles the input, collisions, and events that the main player experiences throughout the game.
### intro.py
The intro.py file is responsible for playing the intro at the beginning of the game.
### pause.py and ending.py
These two files are responsible for the pause and end screen games, and allow for retrying the game. Retrying is done by running the __init__ function in main again, re-initializing everything. The final score is calculated in ending.py and displayed to the player.
### level.py
The level.py file controls the map and the various sprites in the game. By far the longest and most complicated file.
### sprites.py
The sprites.py file includes all the sprites that are used in the game and their respective class. Inheritance is used heavily here.
### todolist.py
The todolist.py file is responsible for drawing the todolist on the topright of the screen when the player approaches the fridge.
### phone.py
The phone.py file is responsible for drawing the phone when opened and the tab-hint image when closed. This also holds the code for the timer, which is also displayed on the phone.
### clean_minigame.py
The clean_minigame.py plays the minigame when you interact with the dishes.
### overlay.py
The overlay.py displays the broom when it is equipped by the player. It is displayed on the bottom left of the screen.
### support.py
The support.py is an auxiliary file for locating and animating assets.
### config.py
The config.py file holds many important configurations required for the game, such as screen height and width, layers, and sprites that require time.
### camera_group.py
The camera_group.py is responsible for the illusion of a camera following the player.
