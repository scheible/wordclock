from application.application import *
from shared.ledBinding import *
import time, random

class ApplicationSnake(Application):
    
    def applicationInit(self):
        
        jsonConfig = super().getJsonConfig()
        jsonWs2812b = super().getWs2812bJson()
        self.__oldBrightness = jsonConfig["brightness"]
        self.__ledBinding = LedBinding(jsonWs2812b, 220, 150)
        self.__ledBinding.clear()
        self.__ledMatrix = LEDMatrix(self.__ledBinding)
        self.__snake = SnakeGame(self.__ledMatrix)
        
    def applicationTask(self, jsonConfig, isUpdateJson):   
        
        if (isUpdateJson):
            self.__snake.changeDirection(jsonConfig['direction'])
            print("new direction", jsonConfig['direction'])

        self.__snake.tick()
        self.__snake.render()

        time.sleep(0.3)


        


# The LEDMatrix is an abstraction from the LEDBinding. The LEDBinding
# can control single LEDs, but does not know how the LEDs are positioned
# in the clock. The LEDMatrix takes x/y coordinates and shows converts
# them into the index on the strip
class LEDMatrix():

    def __init__(self, ledBinding):
        self.__ledBinding = ledBinding
        self.__xMax = 10    # starting with 0
        self.__yMax = 9

    def clear(self):
        self.__ledBinding.clear()

    def setRGB(self, x, y, r, g, b):

        if (x < 0 or x > self.__xMax or y < 0 or y > self.__yMax):
            raise Exception("index out of LEDMatrix bounds")

        # x starts on the right side of the clock, but the interface
        # references the left side as the origin
        x = self.__xMax - x
        # how many full rows are before the row that we are targeting?
        # -> x rows. Each of these rows has yMax*2 LEDs
        index = x * (self.__yMax+1) * 2
        # y depends if we are in an even row that starts from the bottom
        # or if we are in an odd row that starts from the top
        if (x % 2 == 0):
            index += y*2
        else:
            index += (self.__yMax - y)*2

        self.__ledBinding.setLedRGB(index, r, g, b)
        self.__ledBinding.setLedRGB(index+1, r, g, b)
    
    def show(self):
        self.__ledBinding.show()


class SnakeGame():

    def __init__(self, ledMatrix):
        self.__ledMatrix = ledMatrix
        self.__snake = Snake(5,5)
        self.__tickCounter = 0
        self.__food = Food()
        self.__food.place(self.__snake)

    def tick(self):
        self.__tickCounter += 1
        self.__snake.move()

        if (self.__food.collisionWithSnake(self.__snake)):
            self.__snake.eat()
            self.__food.place(self.__snake)     

    def changeDirection(self, direction):
       self.__snake.changeDirection(direction)

    def render(self):
        self.__ledMatrix.clear()
        self.__snake.render(self.__ledMatrix)
        self.__food.render(self.__ledMatrix)
        self.__ledMatrix.show()

class Food():

    def __init__(self):
        pass

    def place(self, snake):
        while True:
            self._x = random.randint(0,10)
            self._y = random.randint(0,9)

            if (not snake.checkCollision(self._x, self._y)):
                break

    def getX(self):
        return self._x 

    def getY(self):
        return self._y

    def render(self, ledMatrix):
        if (self._x >= 0 and self._y >= 0):
            ledMatrix.setRGB(self._x, self._y, 0, 150, 0)

    def collisionWithSnake(self, snake):
        return self.collision(snake.getX(), snake.getY())

    def collision(self, x, y):
        return (self._x == x and self._y == y)


class SnakeLink():

    def __init__(self):
        self._x = -1
        self._y = -1
        self._prevLink = None

    def render(self, ledMatrix):
        if (self._x >= 0 and self._y >= 0):
            ledMatrix.setRGB(self._x, self._y, 150, 0, 0)
        
        if (self._prevLink != None):
            self._prevLink.render(ledMatrix)

    def kill(self):
        if (self._prevLink != None):
            self._prevLink.kill()
            del self._prevLink
            self._prevLink = None

    def eat(self):
        #if __prevLink == None then we are the
        #last link, in this case add to this
        #if we are not the last link, pass it
        #on until the last link will add the new
        #link
        if (self._prevLink == None):
            self._prevLink = SnakeLink()
        else:
            self._prevLink.eat()

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def move(self, x, y):
        # first move the previous link to the position of this
        # link. Then move this link to the new position
        if (self._prevLink != None):
            self._prevLink.move(self._x, self._y)

        self._x = x 
        self._y = y

    def collisionDownTheLine(self, x, y):
        # checks if this link or any link behind it
        # collides with x and y
        if (self._x == x and self._y == y):
            return True
        else:
            if (self._prevLink != None):
                return self._prevLink.collisionDownTheLine(x,y)
            else:
                return False


class Snake(SnakeLink):

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._prevLink = None
        self.changeDirection(3)

    def move(self):
        if (self._prevLink != None):
            self._prevLink.move(self._x, self._y)

        self._x += self._xDir
        self._y += self._yDir

        if self._x > 10:
            self._x = 0
        if self._x < 0:
            self._x = 10
        if self._y > 9:
            self._y = 0 
        if self._y < 0:
            self._y = 9

        if self.checkSelfCollision():
            print("kill snake!!")
            self._prevLink.kill()

    def changeDirection(self, direction):
        # dir 0 -> up
        # dir 1 -> down
        # dir 2 -> left
        # dir 3 -> right
        if (direction == 0):
            self._xDir = 0
            self._yDir = 1
        elif (direction == 1):
            self._xDir = 0
            self._yDir = -1
        elif (direction == 2):
            self._xDir = -1
            self._yDir = 0
        elif (direction == 3):
            self._xDir = 1
            self._yDir = 0

    def checkSelfCollision(self):
        return self.checkCollision(self._x, self._y)

    def checkCollision(self, x, y):
        if (self._prevLink != None):
            return (self._prevLink.collisionDownTheLine(x, y))
        else:
            return False
