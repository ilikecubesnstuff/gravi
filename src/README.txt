Welcome to the gravity simulator! This is a simulator written in the Python programming language. In order to run this simulation, you need to have Python installed as well as the Pygame module.

Install Python here: https://www.python.org/downloads/
Install Pygame here: https://www.pygame.org/download.shtml

To open the simulation, run the main.py file in this directory. Here is a list of commands/features.

-- MOUSE CONTROLS --
Left click + drag
    Add dynamic (moving) body.
Right click
    Add static (non-moving) body.
Scroll
    Change the mass of the objects being added.

-- BASIC --
H - Prints this menu.
I - Prints information about the current simulation frame.
Y - Prints the history of previous actions.
1 - Changes simulation mode to 1 (No collisions/combining objects).
2 - Changes simulation mode to 2 (Touching objects combine).
D - Adds random dynamic body to the simulation.
7 - Halts all dynamic bodies (sets velocity = [0, 0]).
8 - Deletes all static bodies.
9 - Deletes all dynamic bodies.
0 - Deletes all bodies.
G - Toggle gravity.
W - Toggle wall along the edges of the simulation window.
T - Toggle tracing (showing object paths).
R - Refresh (fill window with black, used with tracing).
S - Save screenshot of current simulation frame.
Q - Quit program.

-- FILES --
Z - Save current simulation.
N - Create new simulation.
O - Open existing simulation.
Q - Save simulation on quit.

-- ADVANCED --
P   - Resize window. (Default: 500px)
-/+ - Increase/decrease time step for Euler's method. (Default: 1.0)
[/] - Increase/decrease force of gravity between masses. (Default: 1.2)
</> - Increase/decrease buffer size. (The buffer is the length around simulation window in which objects can stay. Going beyond the buffer removes objects from the simulation. Default: 2000px)
