from pyb import SPI, Pin, UART, LED, delay, Timer
from random import choice

# Adresse accelerometre
WHO_AM_I = 0x0F
CTRL_REG4 = 0x20
OUT_X = 0x29
OUT_y = 0x20

# Définition des paramètres de base
CS = Pin("PE3", Pin.OUT_PP)
SPI_1 = SPI(
    1,  # PA5, PA6, PA7
    SPI.MASTER,
    baudrate=50000,
    polarity=0,
    phase=0,
    firstbit=SPI.MSB,
    crc=None,
)

uart = UART(2, 115200)
push_button = pyb.Pin("PA0", pyb.Pin.IN, Pin.PULL_DOWN)

# définition variable de base
clock_timer = 0

Left_Value = 0
Right_Value = 205
Max_Value_move = 52
Top_Value = 0
Bottom_Value = 62

default_velocity = 1
velocity = 1

default_value_max_proj = 6
value_max_proj = 6

score = 0
default_score = 0

game_time = 0
default_playing_game = 0

value_spawn_x = 30
value_spawn_y = 50


proj_group = []
invaders = []
projectil_invaders_g = []


def wait_pin_change(pin, status_hope):
    active = 0
    while active < 50:
        if pin.value() == status_hope:
            active += 1
        else:
            active = 0
        delay(1)


def clear_screen():
    uart.write("\x1b[2J \x1b[ ?25l")


def move(x, y):
    uart.write("\x1b[{};{}H".format(x, y))


def read_reg(addr):
    CS.low()
    SPI_1.send(addr | 0x80)
    tab_values = SPI_1.recv(1)
    CS.high()
    return tab_values[0]


def write_reg(addr, value):
    CS.low()
    SPI_1.send(addr | 0x00)
    SPI_1.send(value)
    CS.high()


def convert_value(high, low):
    value = (high << 8) | low
    if value & (1 << 15):
        # negative number
        value = value - (1 << 16)
    return value


def read_acceleration(base_addr):
    low = read_reg(base_addr)
    high = read_reg(base_addr + 1)
    return convert_value(high, low)


class Racket:
    def __int__(self, x, y, skin):
        self.x = x
        self.y = y
        self.skin = skin
        self.status = 0

    def erase(self):
        move(self.x, self.y)
        uart.write('  ' * len(self.skin))

    def move_right(self):
        self.erase()
        if self.y < (Right_Value - len(self.skin) - 5):
            self.y += 1 + velocity
        move(self.x, self.y)
        uart.write(self.skin)
        delay(100)

    def move_left(self):
        self.erase()
        if self.y > (Left_Value + 2):
            self.y -= velocity
        move(self.x, self.y)
        uart.write(self.skin)
        delay(100)


racket = Racket(x=value_spawn_x, y=value_spawn_y, skin="|oOo|")
write_reg(CTRL_REG4, 0x77)


class Projectil:

    def __init__(self, x, y, skin):
        self.x = x
        self.y = y
        self.skin = skin
        self.status = 0

    def erase(self):
        move(self.x, self.y)
        uart.write('  ' * len(self.skin))

    def move(self):
        self.erase()
        self.collide()
        if self.status == 0:
            if self.x > (Top_Value + 3):
                self.x -= 2
                move(self.x, self.y)
                uart.write(self.skin)

            else:
                proj_group.remove(self)
        else:
            proj_group.remove(self)

        delay(1)

    def collide(self):
        global score
        for enemies in invaders[:]:
            if enemies.x <= self.x < enemies.x + 2 and enemies.y <= self.y < enemies.y + len(enemies.skin):
                enemies.erase()
                invaders.remove(enemies)
                self.status = 1
                score += (600 - (velocity * 100))


def new_projectil():
    proj_group.append(Projectil(x=(racket.x + 1), y=(racket.y + (len(racket.skin) // 2)), skin="°"))


class Invaders:
    def __init__(self, x, y, skin):
        self.x = x
        self.y = y
        self.skin = skin
        self.status_shoot = 0

    def erase(self):
        move(self.x, self.y)
        uart.write('  ' * len(self.skin))

    def move_left(self):
        self.erase()
        if self.y > (Left_Value + 2):
            self.y -= 1 + (velocity // 2)
        move(self.x, self.y)
        uart.write(self.skin)

    def move_right(self):
        self.erase()
        if self.y < (Right_Value - len(self.skin) - 5):
            self.y += 1 + (velocity // 2)
        move(self.x, self.y)
        uart.write(self.skin)

    def move_forward(self):
        self.erase()
        if self.x < (Max_Value_move - velocity):
            self.x += 1
        move(self.x, self.y)
        uart.write(self.skin)

    def standby(self):
        self.erase()
        move(self.x, self.y)
        uart.write(self.skin)

    def shoot(self):
        if self.status_shoot <= 10:
            projectil_invaders_g.append(
                Projectil_invaders(
                    x=self.x + 1,
                    y=self.y + (len(self.skin) // 2),
                )
            )
            self.status_shoot += 1


class Projectil_invaders:

    def __init__(self, x, y, ):
        self.x = x
        self.y = y
        self.skin = "*"
        self.status = 0

    def erase(self):
        move(self.x, self.y)
        uart.write('  ' * len(self.skin))

    def move(self):
        global game
        self.erase()
        self.collide()
        if self.status == 0:
            if self.x < (Bottom_Value - velocity - 1):
                self.x += 1 + (velocity // 2)
                move(self.x, self.y)
                uart.write(self.skin)
            else:
                projectil_invaders_g.remove(self)
        delay(1)

    def collide(self):
        if racket.x <= self.x < racket.x + 2 and racket.y <= self.y < racket.y + len(racket.skin):
            self.status = 1
            racket.status = 1


def clock(timer):
    global clock_timer
    clock_timer += 1


def velocity_up(timer):
    global value_max_proj, velocity
    if velocity < 5:
        velocity += 1

    if value_max_proj > 1:
        value_max_proj -= 1


def game_time_up(timer):
    global game_time
    game_time += 1


def counter_end():
    move(18, 25)
    text = "Try again : "
    uart.write(text)
    for i in range(60, 30, -1):
        value_counter = "{} | ".format(i)
        uart.write(value_counter)
        if push_button.value() == 1:
            break
        delay(1000)
    move(21, (25 + len(text)))
    for i in range(30, -1, -1):
        value_counter = "{} | ".format(i)
        uart.write(value_counter)
        if push_button.value() == 1:
            break
        delay(1000)


def borders():
    for Value_x in range(int(Top_Value), int(Bottom_Value)):
        move(Value_x, Left_Value)
        uart.write("|")
        move(Value_x, Right_Value)
        uart.write("|")

    for Value_y in range(int(Left_Value), int(Right_Value)):
        move(Top_Value, Value_y)
        uart.write("-")
        move(Bottom_Value, Value_y)
        uart.write("-")


def logo():
    logo_game = r"""███████╗██████╗  █████╗  ██████╗███████╗    ██╗███╗   ██╗██╗   ██╗ █████╗ ██████╗ ███████╗██████╗ ███████╗
██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ██║████╗  ██║██║   ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝
███████╗██████╔╝███████║██║     █████╗      ██║██╔██╗ ██║██║   ██║███████║██║  ██║█████╗  ██████╔╝███████╗
╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝      ██║██║╚██╗██║╚██╗ ██╔╝██╔══██║██║  ██║██╔══╝  ██╔══██╗╚════██║
███████║██║     ██║  ██║╚██████╗███████╗    ██║██║ ╚████║ ╚████╔╝ ██║  ██║██████╔╝███████╗██║  ██║███████║
╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝"""
    tab_logo = logo.splitlines()
    width = len(tab_logo[7])
    a = 1
    b = int((Right_Value - width) / 2)
    for i in tab_logo:
        move((2 + a), b)
        uart.write(i)
        a += 1


def logo_victory():
    logo_vict = r"""██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗    ██╗
██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝    ██║
██║   ██║██║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝     ██║
╚██╗ ██╔╝██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝      ╚═╝
 ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║       ██╗
  ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚═╝"""
    tab_logo = logo.splitlines()
    width= len(tab_logo[6])
    a = 1
    b = int((Right_Value - width) / 2)
    for i in tab_logo:
        move((43 + a), b)
        uart.write(i)
        a += 1


def logo_game_over():
    logo_over = r""" ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗              
██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗             
██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝             
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗             
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║    ██╗██╗██╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚═╝╚═╝╚═╝"""
    tab_logo = logo.splitlines()
    width = len(tab_logo[6])
    a = 1
    b = int((Right_Value - width) / 2)
    for i in tab_logo:
        move((43 + a), b)
        uart.write(i)
        a += 1


def game_home():
    global game, game_time, default_playing_game
    clear_screen()
    borders()
    logo()
    game_info()
    game_reset()
    game_time = default_playing_game

    while True:
            if push_button.value() == 1:
                move(17, 60)
                uart.write("Le jeux se lance dans : ")
                for i in range(10, -1, -1):
                    value_counter = "{} | ".format(i)
                    uart.write(value_counter)
                    delay(1000)
                game = "Level 1"
                break


def game_info():
    move((Right_Value + 10), (Top_Value + 10))
    info_game = "Temps de Jeux = {} | Score = {} | Invaders = {} ".format(
        game,
        game_time,
        score,
        len(Invaders),
    )
    uart.write(info_game)


def game_reset():
    global invaders, proj_group, projectil_invaders_g, default_velocity, \
        velocity, default_value_max_proj, value_max_proj

    for enemies in invaders[:]:
        enemies.erase()
    invaders = []
    for proj in proj_group[:]:
        proj.erase()
    proj_group = []
    proj_spaceship_group = []

    velocity = default_velocity
    value_max_proj = default_value_max_proj


def victory():
    global game
    clear_screen()
    game_info()
    borders()
    logo_victory()

    while True:
        if push_button.value() == 1:
            move(18, 60)
            uart.write("Retour au menu principal : ")
            for i in range(5, -1, -1):
                value_counter = "{} | ".format(i)
                uart.write(value_counter)
                delay(1000)
            game = "HOME"
            break


def game_over():
    global game
    clear_screen()
    game_info()
    borders()
    logo_game_over()

    while True:
        if push_button.value() == 1:
            move(18, 60)
            uart.write("Retour au menu principal : ")
            for i in range(5, -1, -1):
                value_counter = "{} | ".format(i)
                uart.write(value_counter)
                delay(1000)
            game = "HOME"
            break


racket = Racket(x=value_spawn_x, y=value_spawn_y, skin="|oOo|")
addr_ctrl_reg1 = 0x20
write_reg(CTRL_REG4, 0x77)

game = "HOME"