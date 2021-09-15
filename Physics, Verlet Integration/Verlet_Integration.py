import math
import pygame
import json

pygame.init()

WHITE=(255,255,255)
BLACK=(0,0,0)

width = 1920
height = 1080


clock = pygame.time.Clock()


points : int = []
sticks = []
bounce = 0.9
gravity = 0.5
friction = 0.999

model = "Model2.json"

angle = 0
speed = 0.1

def distance(p0, p1):
    dx = p1["x"] - p0["x"]
    dy = p1["y"] - p0["y"]
    return math.sqrt(dx * dx + dy * dy)


def loadModel(model_data):
    for i in range(0, len(model_data["points"])):
        points.append(model_data["points"][i])
 
    for i in range(0, len(model_data["sticks"])):
        s = model_data["sticks"][i]
        s["1"] = points[s["1"]]
        s["2"] = points[s["2"]]
        s["length"] = distance(s["1"], s["2"])
        sticks.append(s)


with open(f'D:\Python\Physics, Verlet Integration\Models\{model}' , "r") as f:
    model_data = json.load(f)

loadModel(model_data)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Verlet Integration')
screen.fill(WHITE)

# use a while loop or recursive call to update the game 
def update():
    #angle = 0
    #points[4]["x"] = 500 + math.cos(angle) * 50
    #angle += speed
    updatePoints()
    for i in range(0, 3):
        updateSticks()
        constrainPoints()
    screen.fill(WHITE)
    renderPoints()
    renderSticks()
  
    pygame.display.update(update())
            
        

def updatePoints():
    for i in range(0, len(points)):
        p = points[i]
        if p["pinned"] == 0:
            vx = (p["x"] - p["oldx"]) * friction
            vy = (p["y"] - p["oldy"]) * friction

            p["oldx"] = p["x"]
            p["oldy"] = p["y"]
            p["x"] += vx
            p["y"] += vy
            p["y"] += gravity

def constrainPoints():
    for i in range(0, len(points)):
        p = points[i]
        """
            How it works 
        If the x position gets bigger than the width of the screen we set x to be the
        width of the screen and then we basically flip the oldx value so that we get a
        change of volocity onto the screen.
        """
        if p["pinned"] == 0:
            vx = (p["x"] - p["oldx"]) * friction
            vy = (p["y"] - p["oldy"]) * friction

            if p["x"] > width:
                p["x"] = width
                p["oldx"] = p["x"] + vx * bounce

            elif p["x"] < 0:
                p["x"] = 0
                p["oldx"] = p["x"] + vx * bounce

            if p["y"] > height:
                p["y"] = height
                p["oldy"] = p["y"] + vy * bounce

            elif p["y"] < 0:
                p["y"] = 0
                p["oldy"] = p["y"] + vy * bounce

def updateSticks():
    if len(sticks) == 0:
        pass
    elif len(sticks) > 0 :
        for i in range(0, len(sticks)):
            s = sticks[i]
            dx = s["2"]["x"]-  s["1"]["x"]
            dy = s["2"]["y"] - s["1"]["y"]
            distance = math.sqrt(dx * dx + dy * dy)
            difference = s["length"] - distance
            # distance each point will have to move to put it in the right spot
            percent = difference / distance / 2
            offsetX = dx*percent
            offsetY = dy*percent

            if s["1"]["pinned"] == False:
                s["1"]["x"] -= offsetX
                s["1"]["y"] -= offsetY
            if s["2"]["pinned"] == False:
                s["2"]["x"] += offsetX
                s["2"]["y"] += offsetY

    

def renderPoints():
    screen.fill(WHITE)
    for i in range(0, len(points)):
        p = points[i]
        # want to draw a full circle obiviously a full circle is 2PI
        """
            what we want

        arc(screen, colour, [x, y, size, r], SA, EA)

        x, y = arc's center
        E = radius
        SA, EA = start and end angle i.e 0, 2PI would be a full circle
        """
        pygame.draw.arc(screen,BLACK,[p["x"],p["y"],10,10],0, math.pi * 2)
        #print(p["x"], p["y"], 5, 0, math.pi * 2)

        clock.tick(60)
        pygame.display.flip()

def renderSticks():
    print(len(sticks))
    if len(sticks) == 0:
        pass
    elif len(sticks) > 0 :
        for i in range(0, len(sticks)):
            s = sticks[i]

            if s["hidden"] == 0:
                
                a = s["1"]["x"] , s["1"]["y"]
                b = s["2"]["x"] , s["2"]["y"]
                pygame.draw.line(screen, BLACK,a, b, 2)

            clock.tick(60)
            pygame.display.flip()
        

update()

