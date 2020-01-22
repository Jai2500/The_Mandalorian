# The Mandalorian Python Based Terminal Game
## Terminal Based Jetpack Joyride 

### Prologue
In this work, I've created a terminal game which is very similar to Jetpack Joyride in concept. 

### Philosophy
I could have easily gotten away by making the objects and the game engine to just suit this game, however, I decided to take the approach of building as general of a game engine which included a **shape agnostic physics engine** that not only registers 99.9% of all collisions but also follows the *Separating Axis Theorem (SAT)* to find out the *Minimum Push Vector* for each collision. <br>
The physics engine also includes a parameterised **gravity**, **drag forces** and also **radial forces for the magnets**. A huge amount of detail was paid to even implement terminal velocity for the player objects. A complete acceleration and velocity is also implemented<br> 
Moreover the object system was inspired from **Unreal Engine's Object Classification**. The classes were so defined to be as generalized as possible. <br>
Some *shortcuts* were taken and the generalization was sacrificied so as to ensure that the program ran smoothly on the terminal screen.  

### How to execute the game
1. Make sure that you have *Python 3.7.3+* and the required Python libraries. If you don't you may install them using:
```Python 
pip install -r requirements.txt
```
2. Navigate into the `game_files` folder and run the following command to start the game: 
```Python
python3 game.py
```
3. Make sure that you have your terminal with a size of atleast `31 x 171` to run the game. I would recommend a size of `46 x 171` as that was one used while development.

### Controls
* `W` : to move upwards using Jetpack
* `A` : to move left using Jetpack
* `D` : to move right using Jetpack
* `E` : to fire the bullet
* `G` : to spawn Mr.Cuddles for the player
* `space` : to activate the Player Shield


### Objects in the Game
* **Ground**: The ground is present below the player at all times throughout the game.
* **Solid Objects**: These are obstacles that are placed so as to slow down the player. It does not take away a life from the player. 
* **Firebeams**: These are obstacles that have been modified from *solid objects* to cause the player to lose life on impact.
* **Magnets**: These are obstacles that drag the player radially towards themselves. 
* **Coin**: A collectible that will increase the score of the player.
* **Speed Boost**: A collectible that will increase the game speed. 
* **Shield**: The player will be able to activate his shield which will provide him invincibility.
* **Player Bullets**: The player can shoot these which will destroy the obstacles (except the magnet) on impact. They also cause damage to the boss enemy.
* **Boss Enemy**: The boss enemy spawns near the end of the game and fires player tracking bullets to the player. The boss enemy will follow the player along the Y axis.
* **Player Dragon**: The player can spawn its own dragon which will cause the game to speed up and will provide shield after to the player.

### Additional Details:
* The game has a ```time``` system and the player has to complete the game within the time. 
* The game has *color* implemented using ```colorama``` and ```ANSI Sequences```. 
* The game does not use ```curses``` or any ```curses``` based libraries such as ```pygame```.


### Way forward:
1. Currently the terminal game only works for ```Linux Terminals```. Can work on to port it to the ```Windows Powershell```. 
2. Implement a procedurally random generation algorithm instead of a simple random generation system. 