import pico2d
class BaseObject:
    WIDTH, HEIGHT = 0, 0
    def __init__(self):
        print('do not create')
        self.x = 0
        self.y = 0
    def draw(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def getRect(self):
        return [[self.x - self.WIDTH//2, self.y - self.HEIGHT//2], [self.x + self.WIDTH//2, self.y + self.HEIGHT//2]]
    def drawRect(self):
        rect = self.getRect()
        pico2d.draw_rectangle(rect[0][0], rect[0][1], rect[1][0], rect[1][1])
    def inRect(self, x, y):
        r = self.getRect()
        if x >= r[0][0] and y >= r[0][1] and x <= r[1][0] and y <= r[1][1]:
            return True
        return False
        