from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.gridlayout import GridLayout

from math import sqrt

class VirtualJoystick(Widget):

    stickpos = [0,0]
    
    def __init__(self, **kwargs):
        super(VirtualJoystick, self).__init__(**kwargs)

        self.size_hint = [None,None]
        self.bind(pos=self.redraw)
        self.bind(size=self.redraw)
        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Rectangle(pos=self.pos, size=self.size,
                      source = 'joy_bg.png')

            Rectangle(pos=[(i/4*j)+z+i/4 for i,j,z in
                           zip(self.size, self.stickpos, self.pos)],
                      size=[i/2 for i in self.size],
                      source = 'joy_fg.png')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            position = []
            position.append(((touch.x - self.x)/self.width-0.5)*4)
            position.append(((touch.y - self.y)/self.height-0.5)*4)

            mag = sqrt(sum([x**2 for x in position]))

            if mag > 1:
                self.stickpos = [(x/mag) for x in position]
            else:
                self.stickpos = [x for x in position]
            
            self.redraw()

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.stickpos = [0,0]
            self.redraw()
            
class TestApp(App):
    def build(self):
        layout = GridLayout(rows=2, cols=2)
        layout.add_widget(VirtualJoystick())
        layout.add_widget(VirtualJoystick())
        layout.add_widget(VirtualJoystick())
        layout.add_widget(VirtualJoystick())
        return layout

if __name__ == '__main__':
    TestApp().run()
