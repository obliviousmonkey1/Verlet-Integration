import math
import pygame

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
angle = 0
speed = 0.1

pos = {
    "x" : 100,
    "y" : 100,
    "oldx" : 95,
    "oldy" : 95,
    "pinned" : False
    }
pos2 = {
    "x" : 200,
    "y" : 100,
    "oldx" : 200,
    "oldy" : 100,
    "pinned" : False
    }
pos3 = {
    "x" : 200,
    "y" : 200,
    "oldx" : 200,
    "oldy" : 100,
    "pinned" : False
    }
pos4 = {
    "x" : 100,
    "y" : 200,
    "oldx" : 100,
    "oldy" : 200,
    "pinned" : False
 
    }
pos5 = {
    "x" : 550,
    "y" : 100,
    "oldx" : 550,
    "oldy" : 200,
    "pinned" : True
 
    }
pos6 = {
    "x" : 400,
    "y" : 100,
    "oldx" : 400,
    "oldy" : 100,
    "pinned" : False
 
    }
pos7 = {
    "x" : 250,
    "y" : 100,
    "oldx" : 250,
    "oldy" : 100,
    "pinned" : False
 
    }



points.append(pos)
points.append(pos2)
points.append(pos3)
points.append(pos4)
points.append(pos5)
points.append(pos6)
points.append(pos7)


def distance(p0, p1):
    dx = p1["x"] - p0["x"]
    dy = p1["y"] - p0["y"]
    return math.sqrt(dx * dx + dy * dy)

# p0 = 1 , p1 = 2
sticks.append({

    1: points[0],
    2: points[1],
    "length": distance(points[0], points[1]),
    "hidden": False

    })
sticks.append({

    1: points[1],
    2: points[2],
    "length": distance(points[1], points[2]),
    "hidden": False

    })
sticks.append({

    1: points[2],
    2: points[3],
    "length": distance(points[2], points[3]),
    "hidden": False

    })
sticks.append({

    1: points[3],
    2: points[0],
    "length": distance(points[3], points[0]),
    "hidden": False

    })
sticks.append({

    1: points[3],
    2: points[1],
    "length": distance(points[3], points[1]),
    "hidden": True

    })
sticks.append({

    1: points[4],
    2: points[5],
    "length": distance(points[4], points[5]),
    "hidden": False

    })
sticks.append({

    1: points[5],
    2: points[6],
    "length": distance(points[5], points[6]),
    "hidden": False

    })
sticks.append({

    1: points[6],
    2: points[0],
    "length": distance(points[6], points[0]),
    "hidden": False

    })




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
    #renderPoints()
    renderSticks()
  
    pygame.display.update(update())
            
        

def updatePoints():
    for i in range(0, len(points)):
        p = points[i]
        if p["pinned"] == False:
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
        if p["pinned"] == False:
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
    for i in range(0, len(sticks)):
        s = sticks[i]
        dx = s[2]["x"]-  s[1]["x"]
        dy = s[2]["y"] - s[1]["y"]
        distance = math.sqrt(dx * dx + dy * dy)
        difference = s["length"] - distance
        # distance each point will have to move to put it in the right spot
        percent = difference / distance / 2
        offsetX = dx*percent
        offsetY = dy*percent

        if s[1]["pinned"] == False:
            s[1]["x"] -= offsetX
            s[1]["y"] -= offsetY
        if s[2]["pinned"] == False:
            s[2]["x"] += offsetX
            s[2]["y"] += offsetY

    

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
    for i in range(0, len(sticks)):
        s = sticks[i]

        if s["hidden"] != True:
            
            a = s[1]["x"] , s[1]["y"]
            b = s[2]["x"] , s[2]["y"]
            pygame.draw.line(screen, BLACK,a, b, 2)

        clock.tick(60)
        pygame.display.flip()
        

update()
    

