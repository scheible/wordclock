from application.application import *
from shared.ledBinding import *
import time

class ApplicationSnake(Application):
    
    def applicationInit(self):
        
        jsonConfig = super().getJsonConfig()
        jsonWs2812b = super().getWs2812bJson()
        self.__oldBrightness = jsonConfig["brightness"]
        self.__ledBinding = LedBinding(jsonWs2812b, 220, 150)
        self.__ledBinding.clear()
        self.__ledMatrix = LEDMatrix(self.__ledBinding)
        self.__snake = Snake(self.__ledMatrix)
        
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
    
    def show(self):
        self.__ledBinding.show()


class Snake():

    def __init__(self, ledMatrix):
        self.__ledMatrix = ledMatrix
        self.__posX = 2
        self.__posY = 5
        self.__xDir = 0
        self.__yDir = 0

    def tick(self):
        self.__posX += self.__xDir
        self.__posY += self.__yDir

        if (self.__posX > 10):
            self.__posX = 0
        if (self.__posX < 0):
            self.__posX = 10
        if (self.__posY > 9):
            self.__posY = 0
        if (self.__posY < 0):
            self.__posY = 9

    def changeDirection(self, direction):
        # dir 0 -> up
        # dir 1 -> down
        # dir 2 -> left
        # dir 3 -> right
        if (direction == 0):
            self.__xDir = 0
            self.__yDir = 1
        elif (direction == 1):
            self.__xDir = 0
            self.__yDir = -1
        elif (direction == 2):
            self.__xDir = -1
            self.__yDir = 0
        elif (direction == 3):
            self.__xDir = 1
            self.__yDir = 0

    def render(self):
        self.__ledMatrix.clear()
        self.__ledMatrix.setRGB(self.__posX, self.__posY, 255, 0, 0)
        self.__ledMatrix.show()

