import pygame
from pygame.locals import *
from copy import deepcopy
from math import sqrt, sin, cos, atan2
from random import random
from bodies import StaticBody, DynamicBody
from vector import Vector
from config import Configuration
import file_handler as fh

help = """
---- HELP MENU ----
Welcome to the gravity simulator! Here is a list of commands/features.

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
"""

def input_int(txt, help = "Enter the desired size of your window in pixels.", max = 10000):
    i = input(txt)
    try:
        i = int(i)
        if i < 0 or i > max:
            print("Invalid input!")
            return input_int(txt, help, max)
        return i
    except:
        if i in ["quit", "exit", "q"]:
            exit()
        elif i == "help":
            print(help)
        else:
            print("Invalid input!")
        return input_int(txt, help, max)

def save_config():
    global history
    global static_bodies
    global dynamic_bodies
    global size
    global buffer
    global sim_mode
    global cmass
    global time_step
    global g_const
    global wall
    global gravity
    global tracing
    history.append(Configuration(deepcopy(static_bodies), deepcopy(dynamic_bodies[:]), [size, buffer, sim_mode, cmass, time_step, g_const, wall, gravity, tracing]))

def load_config(config):
    global static_bodies
    global dynamic_bodies
    global screen
    global size
    global buffer
    global sim_mode
    global cmass
    global time_step
    global g_const
    global wall
    global gravity
    global tracing
    contents = config.unpack()
    static_bodies = contents[0][:]
    dynamic_bodies = contents[1][:]
    size, buffer, sim_mode, cmass, time_step, g_const, wall, gravity, tracing = contents[2]
    screen = pygame.display.set_mode((size, size))

def save_file():
    global history
    global cfile
    if cfile == "":
        save = input("Save current simulation? (Press enter to delete current simulation)\nFile name: ").lower()
        if save not in ["", "n", "no", "cancel"]:
            fh.fwrite(history, save)
            cfile = save
            print('"'+save+'" saved')
    else:
        save = input("Save current simulation? (Press enter to save changes)\n").lower()
        if save in ["new", "y", "yes"]:
            save = input("File name: ")
        if save not in ["", "n", "no"]:
            fh.fwrite(history, save)
            print('"'+save+'" saved')

def on_click():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()

def on_pause():
    global cfile
    global screen
    global size
    global buffer
    global history
    global static_bodies
    global dynamic_bodies
    global sim_mode
    global cmass
    global time_step
    global g_const
    global wall
    global gravity
    global tracing
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    save_config()
                    new_body = StaticBody(cmass, on_click())
                    static_bodies.append(new_body)
                    print("Static body added:", str(new_body))
                    pygame.draw.circle(screen, (255,255,255), round(new_body.pos).list(), new_body.radius)
                    pygame.display.flip()
                if event.button == 1:
                    save_config()
                    initial = pygame.mouse.get_pos()
                    final = on_click()
                    new_body = DynamicBody(cmass, initial, [(final[0]-initial[0])/300, (final[1]-initial[1])/300])
                    dynamic_bodies.append(new_body)
                    print("Dynamic body added:", str(new_body))
                    pygame.draw.circle(screen, (255,255,255), round(new_body.pos).list(), new_body.radius)
                    pygame.display.flip()
                if event.button == 5:
                    if cmass >= 0.4:
                        cmass -= 0.2
                    print("Current mass:",cmass)
                if event.button == 4:
                    cmass += 0.2
                    print("Current mass:",cmass)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Unpaused")
                    return
                save_config()
                if event.key == pygame.K_1:
                    sim_mode = 1
                    print("Simulation mode: 1 (No collisions)")
                if event.key == pygame.K_2:
                    sim_mode = 2
                    print("Simulation mode: 2 (Combining objects)")
                if event.key == pygame.K_7:
                    for body in dynamic_bodies:
                        body.vel = Vector([0, 0])
                    print("All dynamic bodies stopped")
                if event.key == pygame.K_8:
                    static_bodies = []
                    print("Static bodies cleared")
                if event.key == pygame.K_9:
                    dynamic_bodies = []
                    print("Dynamic bodies cleared")
                if event.key == pygame.K_0:
                    static_bodies = []
                    dynamic_bodies = []
                    print("All bodies cleared")

                if event.key == pygame.K_EQUALS:
                    time_step *= 2
                    print("Time step:", time_step)
                if event.key == pygame.K_MINUS:
                    time_step /= 2
                    print("Time step:", time_step)
                if event.key == pygame.K_RIGHTBRACKET:
                    g_const *= 1.2
                    print("Gravitational Constant:", g_const)
                if event.key == pygame.K_LEFTBRACKET:
                    g_const /= 1.2
                    print("Gravitational Constant:", g_const)
                if event.key == pygame.K_COMMA:
                    if buffer >= 100:
                        buffer -= 100
                    print("Buffer:", buffer)
                if event.key == pygame.K_PERIOD:
                    buffer += 100
                    print("Buffer:", buffer)

                if event.key == pygame.K_d:
                    dynamic_bodies.append(DynamicBody(cmass, [size/4+random()*size/2, size/4+random()*size/2], [(random()*size-size/2)/800, (random()*size - size/2)/800]))
                if event.key == pygame.K_g:
                    gravity = not gravity
                    print("Gravity:", gravity)
                if event.key == pygame.K_y:
                    print("--- HISTORY ---")
                    for i in range(len(history)):
                        print(i+1, "::", history[i])
                if event.key == pygame.K_h:
                    print(help)
                if event.key == pygame.K_i:
                    print("--- INFORMATION MENU ---")
                    print("Display size:", size)
                    print("Buffer:", buffer)
                    print("Simulation mode:", sim_mode)
                    print("Current mass:", cmass)
                    print("Time step:", time_step)
                    print("Gravitational Constant:", g_const)
                    print("Wall:", wall)
                    print("Gravity:", gravity)
                    print("Tracing:", tracing)
                    print("Static bodies:")
                    for body in static_bodies:
                        print("\t", body.mass, body.pos)
                    print("Dynamic bodies:")
                    for body in dynamic_bodies:
                        print("\t", body.mass, body.pos, body.vel, body.acc)
                if event.key == pygame.K_n:
                    print("NEW SIMULATION")
                    save_file()

                    static_bodies = []
                    dynamic_bodies = []
                    cmass = 3
                    time_step = 1
                    g_const = 2.0
                    sim_mode = 1
                    wall = True
                    gravity = True
                    tracing = False
                    print("New simulation created")
                    return
                if event.key == pygame.K_o:
                    print("--- OPENING SIMULATION ---")
                    save_file()
                    files = fh.fdir()
                    for i in range(len(files)):
                        print(i, files[i])
                    choice = input_int("File index (number): ",
                                       "Enter the index (number on the left) of your desired file from the list above.",
                                       len(files))
                    cfile = files[choice]
                    history = fh.fread(cfile)
                    if len(history) > 0:
                        load_config(history.pop())
                    else:
                        static_bodies = []
                        dynamic_bodies = []

                        cmass = 3
                        time_step = 1
                        g_const = 2.0
                        sim_mode = 1
                        wall = True
                        gravity = True
                        tracing = False
                    print("Simulation", cfile, "loaded")
                    return
                if event.key == pygame.K_p:
                    size = input_int("Resize window: ")
                    screen = pygame.display.set_mode((size, size))
                    print("Window resized")
                if event.key == pygame.K_q:
                    confirm = input("Are you sure you want to quit?\n")
                    if confirm not in ["y", "yes", "exit", "quit", "q"]:
                        continue
                    save_file()
                    exit()
                if event.key == pygame.K_s:
                    sname = input("Screenshot name: ")
                    pygame.image.save(screen, "screenshots/"+sname+".jpeg")
                    print(sname, "saved")
                if event.key == pygame.K_t:
                    tracing = not tracing
                    print("Tracing:", tracing)
                if event.key == pygame.K_w:
                    wall = not wall
                    print("Wall:", wall)
                if event.key == pygame.K_z:
                    save_file()

cfile = ""
size = 500
buffer = 2000
pygame.init()
screen = pygame.display.set_mode((size, size))

history = []
static_bodies = []
dynamic_bodies = []

cmass = 3.0
time_step = 1.0
g_const = 1.2
sim_mode = 1
wall = True
gravity = True
tracing = False
while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                save_config()
                static_bodies.append(StaticBody(cmass, on_click()))
                print("Static body added:", str(static_bodies[-1]))
            if event.button == 1:
                save_config()
                initial = pygame.mouse.get_pos()
                final = on_click()
                dynamic_bodies.append(DynamicBody(cmass, initial, [(final[0]-initial[0])/300, (final[1]-initial[1])/300]))
                print("Dynamic body added:", str(dynamic_bodies[-1]))
            if event.button == 5:
                if cmass >= 0.4:
                    cmass -= 0.2
                print("Current mass:",cmass)
            if event.button == 4:
                cmass += 0.2
                print("Current mass:",cmass)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                if len(history) > 0:
                    load_config(history.pop())
                    print("Undo")
                    continue
            if event.key == pygame.K_SPACE:
                print("Paused")
                on_pause()
            save_config()
            if event.key == pygame.K_1:
                sim_mode = 1
                print("Simulation mode: 1 (No collisions)")
            if event.key == pygame.K_2:
                sim_mode = 2
                print("Simulation mode: 2 (Combining objects)")
            if event.key == pygame.K_7:
                for body in dynamic_bodies:
                    body.vel = Vector([0, 0])
                print("All dynamic bodies stopped")
            if event.key == pygame.K_8:
                static_bodies = []
                print("Static bodies cleared")
            if event.key == pygame.K_9:
                dynamic_bodies = []
                print("Dynamic bodies cleared")
            if event.key == pygame.K_0:
                static_bodies = []
                dynamic_bodies = []
                print("All bodies cleared")

            if event.key == pygame.K_EQUALS:
                time_step *= 2
                print("Time step:", time_step)
            if event.key == pygame.K_MINUS:
                time_step /= 2
                print("Time step:", time_step)
            if event.key == pygame.K_RIGHTBRACKET:
                g_const *= 1.2
                print("Gravitational Constant:", g_const)
            if event.key == pygame.K_LEFTBRACKET:
                g_const /= 1.2
                print("Gravitational Constant:", g_const)
            if event.key == pygame.K_COMMA:
                if buffer >= 100:
                    buffer -= 100
                print("Buffer:", buffer)
            if event.key == pygame.K_PERIOD:
                buffer += 100
                print("Buffer:", buffer)

            if event.key == pygame.K_d:
                dynamic_bodies.append(DynamicBody(cmass, [size/4+random()*size/2, size/4+random()*size/2], [(random()*size-size/2)/800, (random()*size - size/2)/800]))
            if event.key == pygame.K_g:
                gravity = not gravity
                print("Gravity:", gravity)
            if event.key == pygame.K_y:
                print("--- HISTORY ---")
                for i in range(len(history)):
                    print(i+1, "::", history[i])
            if event.key == pygame.K_h:
                print(help)
            if event.key == pygame.K_i:
                print("--- INFORMATION MENU ---")
                print("Display size:", size)
                print("Buffer:", buffer)
                print("Simulation mode:", sim_mode)
                print("Current mass:", cmass)
                print("Time step:", time_step)
                print("Gravitational Constant:", g_const)
                print("Wall:", wall)
                print("Gravity:", gravity)
                print("Tracing:", tracing)
                print("Static bodies:")
                for body in static_bodies:
                    print("\t", body.mass, body.pos)
                print("Dynamic bodies:")
                for body in dynamic_bodies:
                    print("\t", body.mass, body.pos, body.vel, body.acc)
            if event.key == pygame.K_n:
                save_file()
                static_bodies = []
                dynamic_bodies = []
                cmass = 3
                time_step = 1
                g_const = 2.0
                sim_mode = 1
                wall = True
                gravity = True
                tracing = False
                print("New simulation created")
            if event.key == pygame.K_o:
                if cfile != "":
                    save_file()
                files = fh.fdir()
                for i in range(len(files)):
                    print(i, files[i])
                choice = input_int("File index (number): ", len(files))
                cfile = files[choice]
                history = fh.fread(cfile)
                if len(history) > 0:
                    load_config(history.pop())
                else:
                    static_bodies = []
                    dynamic_bodies = []
                    cmass = 3
                    time_step = 1
                    g_const = 2.0
                    sim_mode = 1
                    wall = True
                    gravity = True
                    tracing = False
                print("Simulation", cfile, "loaded")
            if event.key == pygame.K_p:
                size = input_int("Resize window: ")
                screen = pygame.display.set_mode((size, size))
                print("Window resized")
            if event.key == pygame.K_q:
                confirm = input("Are you sure you want to quit?\n")
                if confirm not in ["y", "yes", "exit", "quit", "q"]:
                    continue
                save_file()
                exit()
            if event.key == pygame.K_r:
                screen.fill((0,0,0))
                print("Screen refreshed")
            if event.key == pygame.K_s:
                sname = input("Screenshot name: ")
                pygame.image.save(screen, "screenshots/"+sname+".jpeg")
                print(sname, "saved")
            if event.key == pygame.K_t:
                tracing = not tracing
                print("Tracing:", tracing)
            if event.key == pygame.K_w:
                wall = not wall
                print("Wall:", wall)
            if event.key == pygame.K_z:
                save_file()

    if not tracing:
        screen.fill((0,0,0))
    for body in dynamic_bodies:
        body.acc = Vector([0, 0])
        for other in dynamic_bodies+static_bodies:
            d = body.dist(other)
            if d == 0:
                continue
            elif d < body.radius + other.radius:
                if sim_mode == 1:
                    continue
                elif sim_mode == 2:
                    other.increase_mass(body.mass)
                    other.pos = (body.pos*body.mass+other.pos*other.mass)/(body.mass+other.mass)
                    if other in dynamic_bodies:
                        other.vel = (body.vel*body.mass+other.vel*other.mass)/(body.mass+other.mass)
                    dynamic_bodies.remove(body)
                    continue
            else:
                dvec = other.pos - body.pos
                mag = g_const*other.mass/d**2
                arg = atan2(dvec.x, dvec.y)
                body.acc += Vector([mag*sin(arg), mag*cos(arg)])
        if body.pos.x < -buffer or body.pos.x > size+buffer or body.pos.y < -buffer or body.pos.y > size+buffer:
            dynamic_bodies.remove(body)
            print("Body out of range")
        if wall:
            if body.pos.x < 0 or body.pos.x > size:
                body.vel.x = -body.vel.x
            if body.pos.y < 0 or body.pos.y > size:
                body.vel.y = -body.vel.y
        if gravity:
            body.vel += body.acc * time_step
        body.pos += body.vel * time_step
        pygame.draw.circle(screen, (255,255,255), round(body.pos).list(), body.radius)
    for body in static_bodies:
        pygame.draw.circle(screen, (255,255,255), round(body.pos).list(), body.radius)
    pygame.display.flip()
