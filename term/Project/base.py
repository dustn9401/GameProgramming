import pico2d
class BaseObject:
    def __init__(self):
        print('do not create')
        self.x = 0
        self.y = 0
        self.WIDTH = 0
        self.HEIGHT = 0
    def draw(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def getRect(self):
        return [[self.x - self.WIDTH//2, self.y - self.HEIGHT//2], [self.x + self.WIDTH//2, self.y + self.HEIGHT//2]]
    def drawRect(self):
        rect = self.getRect()
        pico2d.draw_rectangle(rect[0][0], rect[0][1], rect[1][0], rect[1][1])