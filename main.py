import pygame as pg
from PIL import Image,ImageFilter
from random import randrange
import os
from rich import print


class Window:
    
    def __init__(self,height: int,width: int) -> None:
        """Initialize a pygame window

        Args:
            height (int): [height of the window]
            width (int): [width of the window]
        """
        self.height=height
        self.width=width
        self.window=pg.display.set_mode((width,height))

    def clear(self,color: tuple = (0,0,0)) -> None:
        """Clear the pygame window with a color

        Args:
            color (tuple, optional): Color to fill the window with. Defaults to (0,0,0).
        """
        self.window.fill(color)

    def update(self) -> None:
        """Updates the pygame window
        """
        pg.display.flip()

    def show(self,image,pos: tuple) -> None:
        """Shows the image on the screen

        Args:
            image (image): image to show
            pos (tuple): coordinates of the image
        """
        self.window.blit(image,pos)
                
    def close(self) -> None:
        """Close the pygame window

        Raises:
            SystemExit: Closes the python program
        """
        pg.quit()
        raise SystemExit
    

class Cars:
    
    def __init__(self,color: str,column: int,y: int) -> None:
        """Initialize a car object

        Args:
            color (str): Color of the car (blue,brown,green,red,yellow)
            column (int): Column of the car (1,2,3)
            y (int): Starting y coordinate
        """
        self.color=color
        self.column=column
        self.image=pg.image.load(os.path.join('Assets','car_'+color+'.png'))
        self.y=y
        
    def show(self) -> None:
        """Show the car
        """
        screen.show(self.image,(width/4-100+150*(self.column-1),self.y))
        
    def move(self) -> None:
        """Moves the car slighly down
        """
        self.y+=0.8
        self.show()


class Buttons:
    
    def __init__(self,text: str = 'Test',pos: tuple = (0,0),size: tuple = (300,100),color: tuple = (255,255,255),alpha: int = 25):
        """Generate a button

        Args:
            text (str, optional): Text on the button. Defaults to 'Test'.
            pos (tuple, optional): coordinates of the button. Defaults to (0,0).
            size (tuple, optional): size of the button. Defaults to (300,100).
            color (tuple, optional): color of the button. Defaults to (255,255,255).
            alpha (int, optional): opacity of the button. Defaults to 25.
        """
        self.pos=pos
        box = pg.Surface(size)
        box.set_alpha(alpha)
        box.fill(color)
        myfont= pg.font.Font('Fonts\ARCADECLASSIC.TTF',int(size[1]*0.7))
        self.box=box
        self.string = myfont.render(text,False,(0,0,0)) 
        self.x1=width/2-self.box.get_rect().width/2
        self.size=size
        
    def show_box(self) -> None:
        """Show the box of the button
        """
        screen.show(self.box,(self.x1,self.pos[1]))
        
    def show_text(self) -> None:
        """Show the text of the button"""    
        screen.show(self.string,(width/2-self.string.get_rect().width/2,self.pos[1]+10))


colors=['blue','brown','green','red','yellow']
def get_car() -> object:
    """Function to generate car

    Returns:
        [object]: [random car]
    """
    return Cars(colors[randrange(0,5)],randrange(1,4),-150)


pg.font.init()
width = 500
height = 800
bg = pg.image.load(os.path.join('Assets','road.png'))
screen = Window(height,width)
pg.display.set_caption("Roadway Surfers")
pg.display.set_icon(pg.image.load('Assets\icon.png'))

car_event = pg.USEREVENT+1
pg.time.set_timer(car_event,1000)
car_list=[]

status=0
while True:
    
    if pg.event.get(pg.QUIT): screen.close()
    
    if status==0:
        
        screen.show(bg,(0,0))
        
        for e in pg.event.get():
            if e.type == car_event: car_list.append(get_car())
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    [car.show() for car in car_list]
                    pg.image.save(screen.window,'Assets\screenshot.jpg')
                    screenshot = Image.open('Assets\screenshot.jpg')
                    blur = screenshot.filter(ImageFilter.GaussianBlur(7))
                    blur.save('assets\\blurred.jpg')
                    blurred = pg.image.load('Assets\\blurred.jpg')
                    status=1        
        for car in car_list:
            car.move()
            if car.y > height: car_list.remove(car)
        
    if status==1:
        
        screen.show(blurred,(0,0))
        
        size=(250,100)
        b1=Buttons(text='RESUME',size=size,pos=(width/2-size[0]/2,height/2-size[1]/2-55))
        b2=Buttons(text='EXIT',size=size,pos=(width/2-size[0]/2,height/2-size[1]/2+55))
        b1.show_text()
        b2.show_text()
        
        mousex,mousey = pg.mouse.get_pos()
        if b1.x1<=mousex<=b1.x1+b1.size[0] and b1.pos[1]<=mousey<=b1.pos[1]+b1.size[1]:
            b1.show_box()
            for e in pg.event.get():
                if e.type == pg.MOUSEBUTTONDOWN: status=0
        elif b2.x1<=mousex<=b2.x1+b2.size[0] and b2.pos[1]<=mousey<=b2.pos[1]+b2.size[1]:
            b2.show_box()
            for e in pg.event.get():
                if e.type == pg.MOUSEBUTTONDOWN: screen.close()
        
    screen.update()
    