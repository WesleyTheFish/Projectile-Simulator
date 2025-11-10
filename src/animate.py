import pygame
from sys import exit
from sim import *

def animate_sim():
    """animates data from simulation""" 
    sim_state = 0
    pygame.init()
    screen = pygame.display.set_mode((1000,700))
    pygame.display.set_caption("Simulator")
    clock = pygame.time.Clock()
    sim_font = pygame.font.SysFont("assets/font/josefinSons.ttf", 50)
    data_font = pygame.font.SysFont("comicsans", 20)

    # --------------------------------------------main screen[0]----------------------------------
    title_0 = sim_font.render("This is a Projectile Simulator", True, ("black"))
    title_0_rect = title_0.get_rect(midtop=(500,50))
    
    next_0 = sim_font.render("Press to create a simulation", True, ("black"))
    next_0_rect = next_0.get_rect(midtop=(500,500))

    # -------------------------------------------data entered screen[1]---------------------------
    text_color = "Black"

    # title
    title_1 = sim_font.render("Enter flight parameters", 1, text_color)
    title_1_rect = title_1.get_rect(midtop=(500,20))
    
    # continue button
    next_1 = data_font.render("Simulate", 1, text_color)
    next_1_rect = next_1.get_rect(bottomright=(950,650))

    # Help button
    help = sim_font.render("Help", 1, text_color)
    help_rect = help.get_rect(topleft=(820,50))

    # back button in help
    back = sim_font.render("Back", 1, text_color)
    back_rect = back.get_rect(topleft=(825,640))
    help_text = pygame.image.load("src/assets/images/help_text.png")

    pos = create_data_cat(type="pos", font=data_font, screen=screen)
    vel = create_data_cat(type="vel",font=data_font, screen=screen)
    angle = create_data_cat(type="angle",font=data_font, screen=screen)
    mass = create_data_cat(type="mass",font=data_font, screen=screen)
    target = create_data_cat(type="target",font=data_font, screen=screen)
    wind = Wind(font = data_font, screen = screen)
    pid = PID(font = data_font, screen = screen)

    # list of data categories
    data_list = [pos,vel,angle,mass,target]
    
    # --------------------------------------Simulation screen[2]--------------------------------
    sim_running = True
    font1 = pygame.font.SysFont("src/assets/font/josefinSons.ttf", 35)

    # Background
    background = pygame.image.load("src/assets/images/help_text.png")
    background = pygame.transform.scale(background, (1000, 700))
    dart = pygame.image.load("src/assets/images/dart.png")
    dart = pygame.transform.scale(dart, (100, 50))
    dart2 = pygame.transform.scale(dart, (55, 27.5))
    
    # Landed alert
    landed = sim_font.render("Landed!", 1, "black")
    landed_rect = landed.get_rect(midtop=(500,10))
    
    # continue button
    next_2 = font1.render("Press to Continue", 1, text_color)
    next_2_rect = next_2.get_rect(midtop=(500,60))

    # ----------------------------------------End screen[3]-------------------------------------
    title_3 = sim_font.render("Simulation Complete", 1, text_color)
    title_3_rect = title_3.get_rect(midtop=(500,50))
    next_3 = sim_font.render("Press to start new simulation", 1, text_color)
    next_3_rect = next_3.get_rect(midtop=(500,600))

    # Graphs button
    graph_font = pygame.font.SysFont("assets/font/josefinSons.ttf", 50)
    graph = graph_font.render("See Graphs", 1, text_color)
    graph_rect = graph.get_rect(midtop=(500,400))
    
    # ----------------------------------------Main Loop-----------------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                for data in data_list:
                    data.update_active(event.pos)
                wind.update_active(event.pos)
                pid.update_active(event.pos)
            if event.type == pygame.KEYDOWN:
                # puts input into boxes
                for data in data_list:
                    data.update_input(event)
                wind.update_input(event)
                pid.update_input(event)

        # intro screen
        if sim_state == 0:
            sim_state = screen1(screen=screen, title_0=title_0, title_0_rect=title_0_rect, next_0=next_0, next_0_rect=next_0_rect, sim_state=sim_state)
            sim_running = True
        # Data entered screen
        elif sim_state == 1:
            sim_state,sim,body = screen2(screen=screen, title_1=title_1, title_1_rect=title_1_rect, next_1=next_1, next_1_rect=next_1_rect, data_list=data_list, sim_state=sim_state, wind= wind, pid=pid, help=help, help_rect=help_rect, back=back,back_rect=back_rect,help_text=help_text)
        # Simulation screen  
        elif sim_state == 2:
            sim_state, sim_running = screen3(screen=screen, next_2=next_2, next_2_rect=next_2_rect, sim_state=sim_state,sim=sim,sim_running=sim_running, sim_font=font1, background=background, dart=dart, dart2=dart2, landed = landed, landed_rect = landed_rect)
        # end screen
        else:
            sim_state = screen4(screen=screen, title_3=title_3, title_3_rect=title_3_rect, next_3=next_3, next_3_rect=next_3_rect, sim_state=sim_state,sim = sim, body = body, data_font=data_font, graphs = graph, graph_rect = graph_rect)

        pygame.display.update()
        clock.tick(60)

def screen1(screen, title_0, title_0_rect, next_0, next_0_rect, sim_state):
    """intro screen"""

    screen.fill("#c0e8ec")
    screen.blit(title_0,title_0_rect)
    screen.blit(next_0,next_0_rect)

    # changes color of button on hover
    if next_0_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen,"lightskyblue3", next_0_rect)
        pygame.draw.rect(screen,"lightskyblue3", next_0_rect,6)
        screen.blit(next_0,next_0_rect)

    # changes screen on click
    if pygame.mouse.get_pressed()[0] and next_0_rect.collidepoint(pygame.mouse.get_pos()):
        return (sim_state + 1) % 4
    else:
        return sim_state
    
def screen2(screen, title_1, title_1_rect, next_1, next_1_rect, data_list, sim_state,wind,pid,help,help_rect,back,back_rect,help_text):
    """data entered screen"""

    screen.fill("#c0e8ec")
    # draws title and continue button
    screen.blit(title_1,title_1_rect)
    screen.blit(next_1, next_1_rect)
    screen.blit(help,help_rect)

    # draws data categories
    for data in data_list:
        data.draw()
    wind.draw()
    pid.draw()

    # changes if pid's are custom or default
    if pygame.mouse.get_pressed()[0] and (pid.custom_button_rect.collidepoint(pygame.mouse.get_pos()) or pid.default_button_rect.collidepoint(pygame.mouse.get_pos())):
        if pid.button_delay + 250 < pygame.time.get_ticks():
            pid.default_active = not pid.default_active
            if pid.default_active:
                pid.pos_p = "15"
                pid.pos_i = "0.15"
                pid.pos_d = "5"
                pid.ang_p = "2"
                pid.ang_i = "0.001"
                pid.ang_d = "0.2"
            pid.button_delay = pygame.time.get_ticks()

    # Changes if wind is on or off
    if pygame.mouse.get_pressed()[0] and (wind.wind_on_button_rect.collidepoint(pygame.mouse.get_pos()) or wind.wind_off_button_rect.collidepoint(pygame.mouse.get_pos())):
        if wind.active_delay + 250 < pygame.time.get_ticks():
            wind.active = not wind.active
            wind.active_delay = pygame.time.get_ticks()
    
    # Changes if random wind is on or off
    if pygame.mouse.get_pressed()[0] and (wind.rand_wind_on_button_rect.collidepoint(pygame.mouse.get_pos()) or wind.rand_wind_off_button_rect.collidepoint(pygame.mouse.get_pos())):
        if wind.rand_active_delay + 250 < pygame.time.get_ticks():
            wind.rand_active = not wind.rand_active
            wind.rand_active_delay = pygame.time.get_ticks()

    # changes color of "simulate" button on hover
    if next_1_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen,"lightskyblue3", next_1_rect)
        pygame.draw.rect(screen,"lightskyblue3", next_1_rect,6)
        screen.blit(next_1,next_1_rect)

    # changes color of help button
    if help_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen,"lightskyblue3", help_rect)
        pygame.draw.rect(screen,"lightskyblue3", help_rect,6)
        screen.blit(help,help_rect)  

    # draws help menu
    if pygame.mouse.get_pressed()[0] and help_rect.collidepoint(pygame.mouse.get_pos()):
        draw_help(screen,back,back_rect,help_text)
        pygame.time.wait(100)

    # changes screen on click
    if pygame.mouse.get_pressed()[0] and next_1_rect.collidepoint(pygame.mouse.get_pos()):
        # checks if there was an error in the user input
        error = False
        error = pid.check_error()
        if not error: error = wind.check_error()
        for data in data_list:
            if data.check_input_error():
                error = True
                break

        # only continues if there is no error
        if not error:

            # get data from input boxes
            pos_data = [float(data_list[0].x_input), float(data_list[0].y_input), float(data_list[0].z_input)]
            vel_data =[float(data_list[1].x_input), float(data_list[1].y_input), float(data_list[1].z_input)]
            angle_data = float(data_list[2].x_input)
            mass_data = float(data_list[3].x_input)
            target_data = [float(data_list[4].x_input), float(data_list[4].y_input)]
            pos_pid = [float(pid.pos_p), float(pid.pos_i), float(pid.pos_d)]
            ang_pid = [float(pid.ang_p), float(pid.ang_i), float(pid.ang_d)]
            
            
            # 0=no wind   1 = Constant wind with no random     2 = constant wind with random
            if not wind.active:
                wind_data = (0,0,0)
            elif wind.rand_active:
                wind_data = (1,float(wind.x_input),float(wind.y_input))
            else:
                wind_data = (0,float(wind.x_input),float(wind.y_input))

        
            body = Body(mass=mass_data, position=pos_data, velocity=vel_data, drag=(0, 0, 0), target=target_data, angle = angle_data, pos_pid = pos_pid, ang_pid = ang_pid)
            sim = Simulator(body, wind = wind_data)
            sim.run()

            return (sim_state + 1) % 4, sim, body
        else:
            return sim_state, None, None
    else:
        return sim_state, None, None
        
def screen3(screen, next_2, next_2_rect, sim_state, sim, sim_running, sim_font, background, dart, dart2, landed, landed_rect):
    """simulation screen"""

    # screen: x = 700 y = 1000
    dart_x, dart_y, dart_z = sim.x_pos, sim.y_pos, sim.z_pos
    vel_x,vel_y,vel_z = sim.x_vel, sim.y_vel, sim.z_vel
    index = 0
    length = len(dart_x)
    
    while sim_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Blits the field and the dart
        screen.blit(background, (0,0))
        screen.blit(dart,(500 + (round(dart_x[index] * 8.5)), (340 + (round(dart_y[index] * -8.4)))))
        pygame.draw.rect(screen, "#c0e8ec", (0,625,1000,100))
        
        # Render flight data
        vel_label = sim_font.render("Velocity:", True, "black")
        x_vel = sim_font.render(str(round(vel_x[index])), True, "black")
        y_vel = sim_font.render(str(round(vel_y[index])), True, "black")
        z_vel = sim_font.render(str(round(vel_z[index])), True, "black")
        pos_label = sim_font.render("Position:", True, "black")
        x_pos = sim_font.render(str(round(dart_x[index])), True, "black")
        y_pos = sim_font.render(str(round(dart_y[index])), True, "black")
        z_pos = sim_font.render(str(round(dart_z[index])), True, "black")
        time_label = sim_font.render("Time:", True, "black")
        time = sim_font.render(str(round(sim.time[index],2)), True, "black")
        angle_label = sim_font.render("Angle:", True, "black")
        angle = sim_font.render(str(round(sim.angle[index],2)), True, "black")

        # Blit flight data
        screen.blit(pos_label, (50,650))
        screen.blit(x_pos, (175,650))
        screen.blit(y_pos, (225,650))
        screen.blit(z_pos, (275,650))
        screen.blit(vel_label, (350,650))
        screen.blit(x_vel, (475,650))
        screen.blit(y_vel, (525,650))
        screen.blit(z_vel, (575,650))
        screen.blit(time_label, (650,650))
        screen.blit(time, (730,650))
        screen.blit(angle_label, (815,650))
        screen.blit(angle, (900,650))

        # Blits z position picture
        pygame.draw.rect(screen, "#c0e8ec", (0,400,100,225),border_top_right_radius= 50)
        pygame.draw.rect(screen, "black", (10,620,80,5))
        pygame.draw.rect(screen, "black", (10,410,5,210))
        
        # draw horizontal dart
        height = 605-((dart_z[index]/dart_z[0]) * 200)
        screen.blit(dart2,(30, height))
        # pygame.draw.rect(screen, "black", (30,height, 50, 5) )
   
        pygame.time.wait(int(sim.time_step * 687.5))
        # Cycle time_step
        if index == length-1:
            sim_running = False
        else:
            index += 1
        pygame.display.update()

    # draws landed text and continue button
    pygame.draw.rect(screen, "#c0e8ec", (0,0,1000,100))
    screen.blit(landed, landed_rect)
    screen.blit(next_2, next_2_rect)
    
    # changes color of continue button on hover
    if next_2_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen,"lightskyblue3", next_2_rect)
        pygame.draw.rect(screen,"lightskyblue3", next_2_rect,6)
        screen.blit(next_2,next_2_rect)

    # changes screen on click
    if pygame.mouse.get_pressed()[0] and next_2_rect.collidepoint(pygame.mouse.get_pos()):
        return (sim_state + 1) % 4, sim_running
    else:
        return sim_state, sim_running

def screen4(screen, title_3, title_3_rect, next_3, next_3_rect, sim, body, data_font,sim_state, graphs, graph_rect):
    """end screen"""

    # get final error
    x_error = body.pos_error[0]
    y_error = body.pos_error[1]
    error_msg = data_font.render("Distance from target: x(m): {0:.2f}, y(m): {1:.2f}".format(x_error, y_error), 1, (0,0,0))
    error_rect = error_msg.get_rect(midtop=(500,100))

    screen.fill("#c0e8ec")
    screen.blit(title_3, title_3_rect)
    screen.blit(error_msg, error_rect)
    screen.blit(next_3, next_3_rect)
    screen.blit(graphs, graph_rect)

    # changes color of graph button on hover
    if graph_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen,"lightskyblue3", graph_rect)
        pygame.draw.rect(screen,"lightskyblue3", graph_rect,6)
        screen.blit(graphs, graph_rect)

    # creates graphs
    if pygame.mouse.get_pressed()[0] and graph_rect.collidepoint(pygame.mouse.get_pos()):
        graph(body,sim)
        
    # changes color of continue button on hover
    if next_3_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen,"lightskyblue3", next_3_rect)
        pygame.draw.rect(screen,"lightskyblue3", next_3_rect,6)
        screen.blit(next_3,next_3_rect)

    # changes screen on click
    if pygame.mouse.get_pressed()[0] and next_3_rect.collidepoint(pygame.mouse.get_pos()):
        return (sim_state + 1) % 4
    else:
        return sim_state

def create_data_cat(type, font, screen):
    """creates a data category"""

    text_color = "Black"
    left_margin = 50

    if type.__eq__("pos"):
        # starting position
        pos_label = font.render("Starting Position:", 1, text_color)
        pos_label_rect = pos_label.get_rect(topleft=(left_margin,100))
        
        x_pos_label = font.render("x(m):", 1, text_color)
        x_pos_label_rect = x_pos_label.get_rect(topleft=(pos_label_rect.right+20,100))
        input_pos_x_rect = pygame.Rect(x_pos_label_rect.right+10, 102.5, 75, 30)
        
        y_pos_label = font.render("y(m):", 1, text_color)
        y_pos_label_rect = y_pos_label.get_rect(topleft=(input_pos_x_rect.right+25,100))
        input_pos_y_rect = pygame.Rect(y_pos_label_rect.right+10, 102.5, 75, 30)
        
        z_pos_label = font.render("z(m):", 1,text_color)
        z_pos_label_rect = z_pos_label.get_rect(topleft=(input_pos_y_rect.right+25,100))
        input_pos_z_rect = pygame.Rect(z_pos_label_rect.right+10, 102.5, 75, 30)

        return Data_Cat( 
            screen=screen,
            font=font,
            label=pos_label, 
            label_rect = pos_label_rect, 
            x_label = x_pos_label, 
            x_label_rect = x_pos_label_rect, 
            y_label = y_pos_label, 
            y_label_rect = y_pos_label_rect, 
            z_label = z_pos_label, 
            z_label_rect = z_pos_label_rect, 
            x_input_rect = input_pos_x_rect, 
            y_input_rect = input_pos_y_rect, 
            z_input_rect = input_pos_z_rect,
            type=0)
    elif type.__eq__("vel"):
        # starting velocity
        vel_label = font.render("Starting Velocity:", 1, text_color)
        vel_label_rect = vel_label.get_rect(topleft=(left_margin,165))

        x_vel_label = font.render("x(m/s):", 1, text_color)
        x_vel_label_rect = x_vel_label.get_rect(topleft=(vel_label_rect.right+20,165))
        input_vel_x_rect = pygame.Rect(x_vel_label_rect.right+10, 165, 100, 30)
        
        y_vel_label = font.render("y(m/s):", 1, text_color)
        y_vel_label_rect = y_vel_label.get_rect(topleft=(input_vel_x_rect.right+10,165))
        input_vel_y_rect = pygame.Rect(y_vel_label_rect.right+10, 165, 100, 30)
        
        z_vel_label = font.render("z(m/s):", 1, text_color)
        z_vel_label_rect = z_vel_label.get_rect(topleft=(input_vel_y_rect.right+10,165))
        input_vel_z_rect = pygame.Rect(z_vel_label_rect.right+10, 165, 100, 30)
        
        return Data_Cat(
            screen=screen,
            font=font,
            label=vel_label, 
            label_rect = vel_label_rect, 
            x_label = x_vel_label, 
            x_label_rect = x_vel_label_rect, 
            y_label = y_vel_label, 
            y_label_rect = y_vel_label_rect, 
            z_label = z_vel_label, 
            z_label_rect = z_vel_label_rect, 
            x_input_rect = input_vel_x_rect, 
            y_input_rect = input_vel_y_rect, 
            z_input_rect = input_vel_z_rect,
            type=0)
    elif type.__eq__("angle"):

        # starting angle
        angle_label = font.render("Starting Angle(degrees):", 1, text_color)
        angle_label_rect = angle_label.get_rect(topleft=(50,225))
        input_angle_rect = pygame.Rect(angle_label_rect.right+10, 225, 200, 30)

        return Data_Cat(
            screen=screen,
            font=font,
            label=angle_label, 
            label_rect = angle_label_rect, 
            x_input_rect = input_angle_rect,
            type=1)
    elif type.__eq__("mass"):
        # starting mass
        mass_label = font.render("Starting Mass(kg):", 1, text_color)
        mass_label_rect = mass_label.get_rect(topleft=(50,285))
        input_mass_rect = pygame.Rect(mass_label_rect.right+10, 285, 200, 30)

        return Data_Cat(
            screen=screen,
            font=font,
            label=mass_label, label_rect=mass_label_rect, 
            x_input_rect=input_mass_rect,
            type=1)
    elif type.__eq__("target"):
        # target
        target_label = font.render("Target:", 1, text_color)
        target_label_rect = target_label.get_rect(topleft=(left_margin,590))
        
        x_target_label = font.render("x(m):", 1, text_color)
        x_target_label_rect = x_target_label.get_rect(topleft=(left_margin,target_label_rect.bottom+10))
        input_target_x_rect = pygame.Rect(x_target_label_rect.right + 10, target_label_rect.bottom+10, 50, 30)
        
        y_target_label = font.render("y(m):", 1, text_color)
        y_target_label_rect = y_target_label.get_rect(topleft=(input_target_x_rect.right+50,target_label_rect.bottom+10))
        input_target_y_rect = pygame.Rect(y_target_label_rect.right + 10, target_label_rect.bottom+10, 50, 30)
        
        return Data_Cat(
            screen=screen,
            font=font,
            label=target_label, 
            label_rect = target_label_rect, 
            x_label = x_target_label, 
            x_label_rect = x_target_label_rect, 
            y_label = y_target_label, 
            y_label_rect = y_target_label_rect, 
            x_input_rect = input_target_x_rect, 
            y_input_rect = input_target_y_rect,
            type = 2)
    
def draw_help(screen, back,back_rect,help_text):
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill("#c0e8ec")
        screen.blit(back,back_rect)
        screen.blit(help_text,(22,15))

        # changes color of back button
        if back_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen,"lightskyblue3", back_rect)
            pygame.draw.rect(screen,"lightskyblue3", back_rect,6)
            screen.blit(back,back_rect)
        
        # goes back to data screen
        if pygame.mouse.get_pressed()[0] and back_rect.collidepoint(pygame.mouse.get_pos()):
            done = True

        pygame.display.update()
class Data_Cat:
    def __init__(self, font, screen, label, label_rect, x_input_rect, x_label = None, x_label_rect = None, y_label = None, y_label_rect= None, y_input_rect= None, z_label = None, z_label_rect = None, z_input_rect = None, type = None):
        self.screen = screen
        self.font = font
        self.label = label
        self.label_rect = label_rect

        self.x_input_rect = x_input_rect
        self.y_input_rect = y_input_rect
        self.z_input_rect = z_input_rect
        self.x_input = ""
        self.y_input = ""
        self.z_input = ""

        self.x_label = x_label
        self.y_label = y_label
        self.z_label = z_label
        self.x_label_rect = x_label_rect
        self.y_label_rect = y_label_rect
        self.z_label_rect = z_label_rect

        self.x_active = False
        self.y_active = False
        self.z_active = False
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('black')
        
        # 0 = xyz input
        # 1 = single value input
        # 2 = xy input
        self.type = type
        
    def update_active(self, event_pos):
        # 0 = xyz input
        if self.type == 0:
            if self.x_input_rect.collidepoint(event_pos):
                self.x_active = True
                self.y_active = False
                self.z_active = False
            elif self.y_input_rect.collidepoint(event_pos):
                self.x_active = False
                self.y_active = True
                self.z_active = False
            elif self.z_input_rect.collidepoint(event_pos):
                self.x_active = False
                self.y_active = False
                self.z_active = True
            else:
                self.x_active = False
                self.y_active = False
                self.z_active = False
        # 1 = single value input
        elif self.type == 1:
            if self.x_input_rect.collidepoint(event_pos):
                self.x_active = True
            else:
                self.x_active = False
        # 2 = xy input
        elif self.type == 2:
            if self.x_input_rect.collidepoint(event_pos):
                self.x_active = True
                self.y_active = False
            elif self.y_input_rect.collidepoint(event_pos):
                self.x_active = False
                self.y_active = True
            else:
                self.x_active = False
                self.y_active = False

    def update_input(self, event):
        if self.x_active:
            if event.key == pygame.K_BACKSPACE:
                self.x_input = self.x_input[:-1]
            else:
                self.x_input += event.unicode
        elif self.y_active:
            if event.key == pygame.K_BACKSPACE:
                self.y_input = self.y_input[:-1]
            else:
                self.y_input += event.unicode
        elif self.z_active:
            if event.key == pygame.K_BACKSPACE:
                self.z_input = self.z_input[:-1]
            else:
                self.z_input += event.unicode

    def draw(self):
        """Draws the input box and the text that has been entered so far."""

        # draws label
        self.screen.blit(self.label, self.label_rect)
        
        # 0 = xyz input
        if self.type == 0:

            # designates colors of boxes
            x_color = self.color_active if self.x_active else self.color_inactive
            y_color = self.color_active if self.y_active else self.color_inactive
            z_color = self.color_active if self.z_active else self.color_inactive

            # Render the current text.
            x_txt_surface = self.font.render(self.x_input, True, x_color)
            y_txt_surface = self.font.render(self.y_input, True, y_color)
            z_txt_surface = self.font.render(self.z_input, True, z_color)
            
            # Resize the xyz boxes if the text is too long.
            x_width = max(75, x_txt_surface.get_width()+10)
            self.x_input_rect.w = x_width
            y_width = max(75, y_txt_surface.get_width()+10)
            self.y_input_rect.w = y_width
            z_width = max(75, z_txt_surface.get_width()+10)
            self.z_input_rect.w = z_width

            # Blit the Labels
            self.screen.blit(self.x_label, self.x_label_rect)
            self.screen.blit(self.y_label, self.y_label_rect)
            self.screen.blit(self.z_label, self.z_label_rect)

            # Blit the text.
            self.screen.blit(x_txt_surface, (self.x_input_rect.x+5, self.x_input_rect.y))
            self.screen.blit(y_txt_surface, (self.y_input_rect.x+5, self.y_input_rect.y))
            self.screen.blit(z_txt_surface, (self.z_input_rect.x+5, self.z_input_rect.y))
            
            # Blit the xyz input_box rect.
            pygame.draw.rect(self.screen, x_color, self.x_input_rect, 2)
            pygame.draw.rect(self.screen, y_color, self.y_input_rect, 2)
            pygame.draw.rect(self.screen, z_color, self.z_input_rect, 2)
        # 1 = single value input
        elif self.type == 1:

            # designates color of the box
            color = self.color_active if self.x_active else self.color_inactive
           
            # Render the current text.
            txt_surface = self.font.render(self.x_input, True, color)

            # Resize the xyz boxes if the text is too long.
            width = max(75, txt_surface.get_width()+10)
            self.x_input_rect.w = width

            # Blit the text.
            self.screen.blit(txt_surface, (self.x_input_rect.x+5, self.x_input_rect.y))

            # Blit the xyz input_box rect.
            pygame.draw.rect(self.screen, color, self.x_input_rect, 2)
        # 2 = xy input
        elif self.type == 2:
            # designates colors of boxes
            x_color = self.color_active if self.x_active else self.color_inactive
            y_color = self.color_active if self.y_active else self.color_inactive

            # Render the current text.
            x_txt_surface = self.font.render(self.x_input, True, x_color)
            y_txt_surface = self.font.render(self.y_input, True, y_color)
            
            # Resize the xyz boxes if the text is too long.
            x_width = max(75, x_txt_surface.get_width()+10)
            self.x_input_rect.w = x_width
            y_width = max(75, y_txt_surface.get_width()+10)
            self.y_input_rect.w = y_width

            # Blit the Labels
            self.screen.blit(self.x_label, self.x_label_rect)
            self.screen.blit(self.y_label, self.y_label_rect)

            # Blit the text.
            self.screen.blit(x_txt_surface, (self.x_input_rect.x+5, self.x_input_rect.y))
            self.screen.blit(y_txt_surface, (self.y_input_rect.x+5, self.y_input_rect.y))

            # Blit the xyz input_box rect.
            pygame.draw.rect(self.screen, x_color, self.x_input_rect, 2)
            pygame.draw.rect(self.screen, y_color, self.y_input_rect, 2)

    def check_input_error(self):
        error = False

        x = self.x_input.replace(".","")
        x = x.replace("-","")

        if not self.y_input == None:
            y = self.y_input.replace(".","")
            y = y.replace("-","")

        if not self.z_input == None:
            z = self.z_input.replace(".","")
            z = z.replace("-","")
            
        if self.type == 0:
            error = not x.isdigit() or not y.isdigit() or not z.isdigit()
        elif self.type == 1:
            error = not x.isdigit()
        elif self.type == 2:
            error = not x.isdigit() or not y.isdigit()

        return error    
class Wind:
    def __init__(self, screen, font):
        self.screen = screen
        self.text_color = "Black"
        self.left_margin = 50
        self.font = font
        self.active = False
        self.active_delay = 0
        self.rand_active = False
        self.rand_active_delay = 0
        self.x_input = ""
        self.y_input = ""
        self.x_active = False
        self.y_active = False
        
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('black')
        self.on_button = font.render("On", 1, self.text_color)
        self.off_button = font.render("Off", 1, self.text_color)

        # starting wind
        self.wind_label = font.render("Wind:", 1, self.text_color)
        self.wind_label_rect = self.wind_label.get_rect(topleft=(50,350))

        # on/off button
        self.wind_on_button_rect = self.on_button.get_rect(topleft=(150,350))
        self.wind_off_button_rect = self.off_button.get_rect(topleft=(150,350))

        # constant wind
        self.constant_wind = font.render("Constant Wind:", 1, self.text_color)
        self.constant_wind_rect = self.constant_wind.get_rect(topleft=(50,400))

        self.x_wind_label = font.render("x(m/s):", 1, self.text_color)
        self.x_wind_label_rect = self.x_wind_label.get_rect(topleft=(210,400))
        self.input_wind_x_rect = pygame.Rect(300, 400, 75, 30)
        
        self.y_wind_label = font.render("y(m/s):", 1, self.text_color)
        self.y_wind_label_rect = self.y_wind_label.get_rect(topleft=(210,440))
        self.input_wind_y_rect = pygame.Rect(300, 440, 75, 30)

        # Random wind
        self.rand_wind = font.render("Random Wind:", 1, self.text_color)
        self.rand_wind_rect = self.rand_wind.get_rect(topleft=(50,500))
        self.rand_wind_on_button_rect = self.on_button.get_rect(topleft=(220,500))
        self.rand_wind_off_button_rect = self.off_button.get_rect(topleft=(220,500))
    
    def draw(self):

        self.screen.blit(self.wind_label,self.wind_label_rect)
    
        if self.active:

            # changes color of "wind" button on hover
            if self.wind_on_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen,"lightskyblue3", self.wind_on_button_rect)
                pygame.draw.rect(self.screen,"lightskyblue3", self.wind_on_button_rect,6)
            self.screen.blit(self.on_button,self.wind_on_button_rect)

            # Blit Random wind button
            if not self.rand_active:
                if self.rand_wind_off_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen,"lightskyblue3", self.rand_wind_off_button_rect)
                    pygame.draw.rect(self.screen,"lightskyblue3", self.rand_wind_off_button_rect,6)
                self.screen.blit(self.off_button,self.rand_wind_off_button_rect)
            else:
                if self.rand_wind_on_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen,"lightskyblue3", self.rand_wind_on_button_rect)
                    pygame.draw.rect(self.screen,"lightskyblue3", self.rand_wind_on_button_rect,6)
                self.screen.blit(self.on_button,self.rand_wind_on_button_rect)
            
            # Blit the Labels
            self.screen.blit(self.constant_wind, self.constant_wind_rect)
            self.screen.blit(self.rand_wind, self.rand_wind_rect)
            
            # designates colors of boxes
            x_color = self.color_active if self.x_active else self.color_inactive
            y_color = self.color_active if self.y_active else self.color_inactive

            # Render the current text.
            x_txt_surface = self.font.render(self.x_input, True, x_color)
            y_txt_surface = self.font.render(self.y_input, True, y_color)
            
            # Blit the text.
            self.screen.blit(x_txt_surface, (self.input_wind_x_rect.x+5, self.input_wind_x_rect.y))
            self.screen.blit(y_txt_surface, (self.input_wind_y_rect.x+5, self.input_wind_y_rect.y))

            # Blit X/Y Labels
            self.screen.blit(self.x_wind_label, self.x_wind_label_rect)
            self.screen.blit(self.y_wind_label, self.y_wind_label_rect)

            # Resize the xyz boxes if the text is too long.
            x_width = max(75, x_txt_surface.get_width()+10)
            self.input_wind_x_rect.w = x_width
            y_width = max(75, y_txt_surface.get_width()+10)
            self.input_wind_y_rect.w = y_width

            # Blit the xyz input_box rect.
            pygame.draw.rect(self.screen, x_color, self.input_wind_x_rect, 2)
            pygame.draw.rect(self.screen, y_color, self.input_wind_y_rect, 2)
        else:
            # changes color of "wind" button on hover
            if self.wind_off_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen,"lightskyblue3", self.wind_off_button_rect)
                pygame.draw.rect(self.screen,"lightskyblue3", self.wind_off_button_rect,6)
            self.screen.blit(self.off_button,self.wind_off_button_rect)
        
    def update_active(self, event_pos):
        if self.input_wind_x_rect.collidepoint(event_pos):
            self.x_active = True
            self.y_active = False
        elif self.input_wind_y_rect.collidepoint(event_pos):
            self.x_active = False
            self.y_active = True
        else:
            self.x_active = False
            self.y_active = False

    def check_error(self):
        if self.active:
            x = self.x_input.replace(".","")
            y = self.y_input.replace(".","")
            x = x.replace("-","")
            y = y.replace("-","")

        error = self.active and (not x.isdigit() or not y.isdigit())
        return error    

    def update_input(self, event):
        if self.x_active:
            if event.key == pygame.K_BACKSPACE:
                self.x_input = self.x_input[:-1]
            else:
                self.x_input += event.unicode
        elif self.y_active:
            if event.key == pygame.K_BACKSPACE:
                self.y_input = self.y_input[:-1]
            else:
                self.y_input += event.unicode
class PID:
    def __init__(self, font, screen):
        self.screen = screen
        self.text_color = "Black"
        self.font = font
        self.default_active = True
        self.button_delay = 0
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('black')

        # position pid valses
        self.pos_p = "15"
        self.pos_i = "0.15"
        self.pos_d = "5"
        self.pos_p_active = False
        self.pos_i_active = False
        self.pos_d_active = False

        # angle pid values pos_pid = (15, .15, 5), ang_pid = (2, .001, .2)
        self.ang_p = "2"
        self.ang_i = "0.001"
        self.ang_d = "0.2"
        self.ang_p_active = False
        self.ang_i_active = False
        self.ang_d_active = False
        
        # main pid label
        self.pid_label = font.render("PID's:", 1, self.text_color)
        self.pid_label_rect = self.pid_label.get_rect(midtop=(625,250))

        # custom/default button
        self.default_button = font.render("Default", 1, self.text_color)
        self.custom_button = font.render("Custom", 1, self.text_color)
        self.default_button_rect = self.default_button.get_rect(topleft=(self.pid_label_rect.right + 25,250))
        self.custom_button_rect = self.custom_button.get_rect(topleft=(self.pid_label_rect.right + 25,250))
       
        # Positional PID
        self.position_pid = font.render("Positional PID's:", 1, self.text_color)
        self.position_pid_rect = self.position_pid.get_rect(topleft=(400,300))

        self.pos_p_label = font.render("P:", 1, self.text_color)
        self.pos_p_label_rect = self.pos_p_label.get_rect(topleft=(self.position_pid_rect.right+20,300))
        self.input_pos_p_rect = pygame.Rect(self.pos_p_label_rect.right + 10, 300, 75, 30)
        
        self.pos_i_label = font.render("I:", 1, self.text_color)
        self.pos_i_label_rect = self.pos_i_label.get_rect(topleft=(self.input_pos_p_rect.right + 25,300))
        self.input_pos_i_rect = pygame.Rect(self.pos_i_label_rect.right + 10, 300, 75, 30)

        self.pos_d_label = font.render("D:", 1, self.text_color)
        self.pos_d_label_rect = self.pos_d_label.get_rect(topleft=(self.input_pos_i_rect.right + 25,300))
        self.input_pos_d_rect = pygame.Rect(self.pos_d_label_rect.right + 10, 300, 75, 30)

        # Angular PID
        self.angular_pid = font.render("Angular PID's:", 1, self.text_color)
        self.angular_pid_rect = self.angular_pid.get_rect(topleft=(400,350))

        self.ang_p_label = font.render("P:", 1, self.text_color)
        self.ang_p_label_rect = self.ang_p_label.get_rect(topleft=(self.angular_pid_rect.right+20,350))
        self.input_ang_p_rect = pygame.Rect(self.ang_p_label_rect.right + 10, 350, 75, 30)

        self.ang_i_label = font.render("I:", 1, self.text_color)
        self.ang_i_label_rect = self.ang_i_label.get_rect(topleft=(self.input_ang_p_rect.right + 25,350))
        self.input_ang_i_rect = pygame.Rect(self.ang_i_label_rect.right + 10, 350, 75, 30)

        self.ang_d_label = font.render("D:", 1, self.text_color)
        self.ang_d_label_rect = self.ang_d_label.get_rect(topleft=(self.input_ang_i_rect.right + 25,350))
        self.input_ang_d_rect = pygame.Rect(self.ang_d_label_rect.right + 10, 350, 75, 30)

    def draw(self):

        # blit main PID label and Custom/Default button
        self.screen.blit(self.pid_label,self.pid_label_rect)
        if self.default_active:
            if self.default_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen,"lightskyblue3", self.default_button_rect)
                pygame.draw.rect(self.screen,"lightskyblue3", self.default_button_rect,6)
            self.screen.blit(self.default_button,self.default_button_rect)
        else:
            if self.custom_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen,"lightskyblue3", self.custom_button_rect)
                pygame.draw.rect(self.screen,"lightskyblue3", self.custom_button_rect,6)
            self.screen.blit(self.custom_button,self.custom_button_rect)

        # designates colors of boxes
        pos_p_color = self.color_active if self.pos_p_active and not self.default_active else self.color_inactive
        pos_i_color = self.color_active if self.pos_i_active and not self.default_active else self.color_inactive
        pos_d_color = self.color_active if self.pos_d_active and not self.default_active else self.color_inactive
        ang_p_color = self.color_active if self.ang_p_active and not self.default_active else self.color_inactive
        ang_i_color = self.color_active if self.ang_i_active and not self.default_active else self.color_inactive
        ang_d_color = self.color_active if self.ang_d_active and not self.default_active else self.color_inactive
        
        # Render the current pid input text.
        pos_p_txt_surface = self.font.render(self.pos_p, True, pos_p_color)
        pos_i_txt_surface = self.font.render(self.pos_i, True, pos_i_color)
        pos_d_txt_surface = self.font.render(self.pos_d, True, pos_d_color)
        ang_p_txt_surface = self.font.render(self.ang_p, True, ang_p_color)
        ang_i_txt_surface = self.font.render(self.ang_i, True, ang_i_color)
        ang_d_txt_surface = self.font.render(self.ang_d, True, ang_d_color)
        
        # Blit the text.
        self.screen.blit(pos_p_txt_surface,(self.pos_p_label_rect.x+33, self.pos_p_label_rect.y+2.5))
        self.screen.blit(pos_i_txt_surface,(self.pos_i_label_rect.x+33, self.pos_i_label_rect.y+2.5))
        self.screen.blit(pos_d_txt_surface,(self.pos_d_label_rect.x+33, self.pos_d_label_rect.y+2.5))
        self.screen.blit(ang_p_txt_surface,(self.ang_p_label_rect.x+33, self.ang_p_label_rect.y+2.5))
        self.screen.blit(ang_i_txt_surface,(self.ang_i_label_rect.x+33, self.ang_i_label_rect.y+2.5))
        self.screen.blit(ang_d_txt_surface,(self.ang_d_label_rect.x+33, self.ang_d_label_rect.y+2.5))
        
        # Resize the xyz boxes if the text is too long.
        pod_p_width = max(75, pos_p_txt_surface.get_width()+10)
        self.input_pos_p_rect.w = pod_p_width
        pos_i_width = max(75, pos_i_txt_surface.get_width()+10)
        self.input_pos_i_rect.w = pos_i_width
        pos_d_width = max(75, pos_d_txt_surface.get_width()+10)
        self.input_pos_d_rect.w = pos_d_width
        ang_p_width = max(75, ang_p_txt_surface.get_width()+10)
        self.input_ang_p_rect.w = ang_p_width
        ang_i_width = max(75, ang_i_txt_surface.get_width()+10)
        self.input_ang_i_rect.w = ang_i_width
        ang_d_width = max(75, ang_d_txt_surface.get_width()+10)
        self.input_ang_d_rect.w = ang_d_width
        
        # Blit the PID input_box rect.
        pygame.draw.rect(self.screen, pos_p_color, self.input_pos_p_rect, 2)
        pygame.draw.rect(self.screen, pos_i_color, self.input_pos_i_rect, 2)
        pygame.draw.rect(self.screen, pos_d_color, self.input_pos_d_rect, 2)
        pygame.draw.rect(self.screen, ang_p_color, self.input_ang_p_rect, 2)
        pygame.draw.rect(self.screen, ang_i_color, self.input_ang_i_rect, 2)
        pygame.draw.rect(self.screen, ang_d_color, self.input_ang_d_rect, 2)

        # blit positional PID
        self.screen.blit(self.position_pid, self.position_pid_rect)
        self.screen.blit(self.pos_p_label, self.pos_p_label_rect)
        self.screen.blit(self.pos_i_label, self.pos_i_label_rect)
        self.screen.blit(self.pos_d_label, self.pos_d_label_rect)

        # blit angular PID
        self.screen.blit(self.angular_pid, self.angular_pid_rect)
        self.screen.blit(self.ang_p_label, self.ang_p_label_rect)
        self.screen.blit(self.ang_i_label, self.ang_i_label_rect)
        self.screen.blit(self.ang_d_label, self.ang_d_label_rect)
    
    def update_active(self, event_pos):
        if self.input_pos_p_rect.collidepoint(event_pos):
            self.pos_p_active = True
            self.pos_i_active = False
            self.pos_d_active = False
            self.ang_p_active = False
            self.ang_i_active = False
            self.ang_d_active = False
        elif self.input_pos_i_rect.collidepoint(event_pos):
            self.pos_p_active = False
            self.pos_i_active = True
            self.pos_d_active = False
            self.ang_p_active = False
            self.ang_i_active = False
            self.ang_d_active = False
        elif self.input_pos_d_rect.collidepoint(event_pos):
            self.pos_p_active = False
            self.pos_i_active = False
            self.pos_d_active = True
            self.ang_p_active = False
            self.ang_i_active = False
            self.ang_d_active = False
        elif self.input_ang_p_rect.collidepoint(event_pos):
            self.pos_p_active = False
            self.pos_i_active = False
            self.pos_d_active = False
            self.ang_p_active = True
            self.ang_i_active = False
            self.ang_d_active = False
        elif self.input_ang_i_rect.collidepoint(event_pos):
            self.pos_p_active = False
            self.pos_i_active = False
            self.pos_d_active = False
            self.ang_p_active = False
            self.ang_i_active = True
            self.ang_d_active = False
        elif self.input_ang_d_rect.collidepoint(event_pos):
            self.pos_p_active = False
            self.pos_i_active = False
            self.pos_d_active = False
            self.ang_p_active = False
            self.ang_i_active = False
            self.ang_d_active = True
        else:
            self.pos_p_active = False
            self.pos_i_active = False
            self.pos_d_active = False
            self.ang_p_active = False
            self.ang_i_active = False
            self.ang_d_active = False
    
    def check_error(self):
        if not self.default_active:
            pos_p = self.pos_p.replace(".","")
            pos_i = self.pos_i.replace(".","")
            pos_d = self.pos_d.replace(".","")
            ang_p = self.ang_p.replace(".","")
            ang_i = self.ang_i.replace(".","")
            ang_d = self.ang_d.replace(".","")
            pos_p = pos_p.replace("-","")
            pos_i = pos_i.replace("-","")
            pos_d = pos_d.replace("-","")
            ang_p = ang_p.replace("-","")
            ang_i = ang_i.replace("-","")
            ang_d = ang_d.replace("-","")

        error = not self.default_active and (not pos_p.isdigit() or not pos_i.isdigit() or not pos_d.isdigit() or not ang_p.isdigit() or not ang_i.isdigit() or not ang_d.isdigit())
        return error
    
    def update_input(self, event):
        if not self.default_active:
            if self.pos_p_active:
                if event.key == pygame.K_BACKSPACE:
                    self.pos_p = self.pos_p[:-1]
                else:
                    self.pos_p += event.unicode
            elif self.pos_i_active:
                if event.key == pygame.K_BACKSPACE:
                    self.pos_i = self.pos_i[:-1]
                else:
                    self.pos_i += event.unicode
            elif self.pos_d_active:
                if event.key == pygame.K_BACKSPACE:
                    self.pos_d = self.pos_d[:-1]
                else:
                    self.pos_d += event.unicode
            elif self.ang_p_active:
                if event.key == pygame.K_BACKSPACE:
                    self.ang_p = self.ang_p[:-1]
                else:
                    self.ang_p += event.unicode
            elif self.ang_i_active:
                if event.key == pygame.K_BACKSPACE:
                    self.ang_i = self.ang_i[:-1]
                else:
                    self.ang_i += event.unicode
            elif self.ang_d_active:
                if event.key == pygame.K_BACKSPACE:
                    self.ang_d = self.ang_d[:-1]
                else:
                    self.ang_d += event.unicode