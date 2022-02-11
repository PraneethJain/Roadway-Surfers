import pygame as pg
from PIL import Image,ImageFilter
from random import randrange
import os


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
        self.image=pg.image.load(os.path.join('Assets','car_'+color+'.png')).convert_alpha()
        self.x=width/4-100+150*(self.column-1)
        self.y=y
        self.height=self.image.get_height()
        self.width=self.image.get_width()
        self.rect=self.image.get_rect()
        self.mask=pg.mask.from_surface(self.image)
        
    def show(self) -> None:
        """Show the car
        """
        screen.show(self.image,(self.x,self.y))
        
    def move(self,speed) -> None:
        """Moves the car slighly down
        """
        self.y+=speed
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


class Player:
    
    def __init__(self,) -> None:
        """Initialize a player
        """
        self.image=pg.image.load('Assets\slime_red.png').convert_alpha()
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.x,self.y=width/2-self.width/2,height-self.height-50
        self.rect=self.image.get_rect()
        self.mask=pg.mask.from_surface(self.image)
        
    def show(self) -> None:
        """Show the player at its position
        """
        screen.show(self.image,(self.x,self.y))
        
    def move(self,x,y, show: bool = True) -> None:
        """Move the player

        Args:
            pos (tuple): coordinates to move to
            show (bool, optional): Whether to show the moved player. Defaults to True.
        """
        self.x=x
        self.y=y
        if show:
            self.show()


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
player = Player()
dx,dy=0,0
score=0

my_font=pg.font.Font("Fonts\ARCADECLASSIC.TTF",50)
big_font=pg.font.Font("Fonts\ARCADECLASSIC.TTF",100)
game_over=big_font.render('GAME OVER',False,(0,0,0))

while True:
    
    if pg.event.get(pg.QUIT): screen.close()
    
    if status==0:
        
        screen.show(bg,(0,0))
        screen_text = my_font.render(str(score),0,(0,0,0))
        screen.show(screen_text,(10,10))
        for e in pg.event.get():
            if e.type == car_event: car_list.append(get_car()); score+=1
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    [car.show() for car in car_list]
                    player.show()
                    pg.image.save(screen.window,'Assets\screenshot.jpg')
                    screenshot = Image.open('Assets\screenshot.jpg')
                    blur = screenshot.filter(ImageFilter.GaussianBlur(7))
                    blur.save('assets\\blurred.jpg')
                    blurred = pg.image.load('Assets\\blurred.jpg')
                    status=1
                
                if e.key == pg.K_LEFT: dx=-1
                if e.key == pg.K_RIGHT: dx=1
                if e.key == pg.K_UP: dy=-1
                if e.key == pg.K_DOWN: dy=1
            
            if e.type == pg.KEYUP:
                if e.key == pg.K_LEFT or e.key == pg.K_RIGHT: dx=0
                if e.key == pg.K_UP or e.key == pg.K_DOWN: dy=0
        
        if player.x<-player.width and dx==-1: player.x=width
        if player.x>width+player.width and dx==1: player.x=-player.width
        if player.y<0: player.y=0
        if player.y>height-player.height: player.y=height-player.height
        
        player.move(player.x+dx,player.y+dy)
        
        for car in car_list:
            car.move(1)
            if car.y > height: car_list.remove(car)
            if car.x-player.width<player.x<car.x+car.width and car.y-player.height<player.y<car.y+car.height:   
                [car.show() for car in car_list]
                player.show()
                pg.image.save(screen.window,'Assets\screenshot.jpg')
                screenshot = Image.open('Assets\screenshot.jpg')
                blur = screenshot.filter(ImageFilter.GaussianBlur(7))
                blur.save('assets\\blurred.jpg')
                blurred = pg.image.load('Assets\\blurred.jpg')
                score_text=my_font.render(f'Score is  {score}',False,(0,0,0))
                restart=my_font.render(f'Enter  to  restart',False,(0,0,0))
                status=2
    
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
    
    if status==2:
        screen.show(blurred,(0,0))
        screen.show(game_over,(width/2-game_over.get_width()/2,height/2-game_over.get_height()))
        screen.show(score_text,(width/2-score_text.get_width()/2,height/2-score_text.get_height()/2+20))
        screen.show(restart,(width/2-restart.get_width()/2,height-restart.get_height()-20))
        for event in pg.event.get():
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_RETURN:
                    car_list=[]
                    player=Player()
                    dx,dy,score=0,0,0
                    status=0
    screen.update()
    