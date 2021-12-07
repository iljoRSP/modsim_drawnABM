import threading
import time
import random
import numpy as np
import tkinter as tk

s_print_lock = threading.Lock()
def s_print(*a, **b): # Thread-safe printing
    if not LOG: return
    if SAFEPRINT:
        with s_print_lock:
            print(*a, **b)
    else: print(*a, **b)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


class Agent(threading.Thread):
    def __init__(self, name, power, initpos, canvas: tk.Canvas):
        threading.Thread.__init__(self)
        self.name = name
        self.power = power
        self.pos = initpos
        self.canvas = canvas

        self.lock = threading.Lock()

        self.color = self.__pickColor()
        self.image = canvas.create_oval(self.posToBounds(), fill = self.color)

        self.track = False
        s_print('Agent {0} created with power {1} at {2}'.format(self.name, self.power, self.pos))
        
    def run(self):
        s_print('Agent {0} started.'.format(self.name))

        while True:
            # calculate movement vector and go to new position
            self.__adjustPos()
            time.sleep(framerate)

            if EXITSIM: break

    def posToBounds(self):
        return (self.pos[0] - circleDiameter / 2,
                self.pos[1] - circleDiameter / 2,
                self.pos[0] + circleDiameter / 2, 
                self.pos[1] + circleDiameter / 2,
               )

    def __adjustPos(self):
        finaldir = np.array((0,0))
        
        # make vector towards stronger agents
        for ag in agents:
            if ag.name == self.name:
                continue
            
            with ag.lock:
                if not rules[r](ag, self): continue
                adir = (ag.pos - self.pos) * (1.5 ** ag.power)
            
            finaldir = finaldir + adir

        finaldir = normalize(finaldir) * speed
        self.pos += finaldir

        if np.linalg.norm(finaldir): # if is moving, log
            s_print('Agent {} of p{} moved with <{:.2f}, {:.2f}> to ({:.2f}, {:.2f})'.format(self.name, self.power, *finaldir, *self.pos))
            

    def __pickColor(self):
        match = {
            0: '#FBBA72',
            1: '#CA5310',
            2: '#BB4D00',
            3: '#8F250C',
            4: '#691E06',
            5: '#361003'
        }

        return match.get(self.power)


# SIM PARAMS

WIDTH = 1200
HEIGHT = 700
circleDiameter = 10
framerate = 1 / 30  # 1/30 = 30 fps - has a hard cap based on time taken to calculate vector per frame
simTime = 40 / framerate  # approximate for 40 seconds real-time

numAgents = 40
numTracked = 0  # number of agents to trace the patch made

speed = 1  # high speeds can cause jittering

# choose what rule to follow for movement of agents
rules = {
    "classic": lambda ag, self: ag.power >= self.power,     # move towards stronger or equal agents
    "stronger": lambda ag, self: ag.power > self.power,     # move towards stronger agents
    "1above": lambda ag, self: ag.power == self.power + 1,  # move towards agents exactly 1 stronger than self
    "equal": lambda ag, self: True,                         # move towards all agents
}
r = "1above"


LOG = False  # log in console
SAFEPRINT = True  # safe printing slows down threads and can cause jittering
                   # LOG must be TRUE for this to have effect

EXITSIM = False
t = 0

# CREATE CANVAS

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

def stopSim():
    global t, simTime
    t = simTime
    print("Simulation halted early.")

tk.Button(root, command = stopSim, text = "Stop Simulation").pack()


# SIM STARTS

agents = [Agent(i, random.randint(0, 5), np.array([np.random.rand() * WIDTH, np.random.rand() * HEIGHT]), canvas) for i in range(numAgents)]
print(sorted([a.power for a in agents]), sep = ' ')
for a in agents[:numTracked]: a.track = True

for a in agents:
    a.start()

while not EXITSIM:
    for a in agents:
        # draw agent at its position
        canvas.coords(a.image, a.posToBounds())

        # track agent
        if a.track and not t % (5 / speed): 
            x1, y1 = (a.pos[0] - 1), (a.pos[1] - 1)
            x2, y2 = (a.pos[0] + 1), (a.pos[1] + 1)
            canvas.create_oval(x1, y1, x2, y2, outline = a.color)
            
    root.update()

    time.sleep(framerate)
    t += 1
    EXITSIM = t >= simTime


# SIM ENDS

for a in agents:
    a.join()

canvas.create_text(WIDTH / 2, HEIGHT / 2, anchor=tk.CENTER, text="SIMULATION HAS ENDED")
root.mainloop()





