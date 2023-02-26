# from math import copysign
import math
from matplotlib import pyplot as plt

class Body:
    """Class for a projectile with mass, radius, position, velocity, angle, angular velocity, drag, target, xy_force, and angle_force"""

    # Constructor
    def __init__(self, mass = 1, radius = .05, position = [0, 0, 122], velocity = [0, 0, 0], angle = 0, ang_velocity = 0, drag = (0,0,0), target = (0,0), xy_force = [0,0], angle_force = 0):
        self.mass = mass
        self.radius = radius
        self.drag = drag
        self.target = target
        self.target_final_vel = [0,0]
        self.controller = Controller(self)

        self.position = position
        self.velocity = velocity
        self.angle = angle
        self.ang_velocity = ang_velocity

        
        
        self.pos_error = [0,0]
        self.ang_error = 0
        self.vel_error = [0,0]
        self.xy_force = xy_force
        self.angle_force = angle_force
    
    
    def step(self, net_accel, time_step = 0.01):
        """Integrates xyz accelerations to corresponding velocity and position of projectile"""
        for i in range(3):
            self.velocity[i] += net_accel[i] * time_step
            self.position[i] += self.velocity[i] * time_step

        # integrates to find new angle and angular velocity
        self.ang_velocity += net_accel[3] * time_step
        self.angle += self.ang_velocity * time_step
        self.angle = self.angle % 360
        if self.angle < 0:
            self.angle += 360
        
    """updates position, velocity, and angle errors"""
    def update_pos_error(self):
        self.pos_error = [curr-target for curr, target in zip(self.position, self.target)]
    
    def update_vel_error(self):
        self.vel_error = [velocity-target for velocity, target in zip(self.velocity, self.target_final_vel)]
        
    def update_angle_error(self):
        self.ang_error = (450 - 180/math.pi*(math.atan2(-self.pos_error[1],-self.pos_error[0]))) % 360 - self.angle 
        if self.ang_error > 180:
            self.ang_error -= 360
    
    """formats terminal output"""
    def pos_report(self):
        return f"pos({self.position[0]:0.2f}, {self.position[1]:0.2f}, {self.position[2]:0.2f})"

    def vel_report(self):
        return f"vel({self.velocity[0]:0.2f}, {self.velocity[1]:0.2f}, {self.velocity[2]:0.2f})"
    
    def ang_report(self):
        return f"angle({self.angle:0.2f})"
    
    def ang_vel_report(self):
        return f"ang_vel({self.ang_vel:0.2f})"
    
    def pos_error_report(self):
        return f"pos_error({self.pos_error[0]:0.2f}, {self.pos_error[1]:0.2f})"

    def vel_error_report(self):
        return f"vel_error({self.vel_error:0.2f})"

    def ang_error_report(self):
        return f"ang_error({self.ang_error:0.2f})"


class Controller:
    
    # Constructor
    def __init__(self, body:Body):
        self.body = body
        self.force_limit = 10
        self.angle_force_lim = 5
        
        self.p = 100
        self.i = .05
        self.d = 20

        self.ang_p = .01
        self.ang_i = .05
        self.ang_d = 5


    def correct_xy(self, integral_x, integral_y):
        """pass all of its parameters to a PID controller and it will tell me what force to apply to the projectile"""
        force_x = 0
        force_y = 0

        # x axis
        force_x = self.body.pos_error[0] * -self.p
        force_x += self.body.velocity[0] * -self.d
        force_x += integral_x * -self.i

        # y axis
        force_y = self.body.pos_error[1] * -self.p
        force_y += self.body.velocity[1] * -self.d
        force_y += integral_y * -self.i

        # limit force
        if force_x > self.force_limit:
            force_x = self.force_limit
        elif force_x < -self.force_limit:
            force_x = -self.force_limit

        if force_y > self.force_limit:
            force_y = self.force_limit
        elif force_y < -self.force_limit:
            force_y = -self.force_limit


        self.body.xy_force = [force_x, force_y]


    def correct_angle(self, integral_ang):
        

        # x axis
        ang_force = self.body.ang_error * -self.p
        ang_force += self.body.ang_velocity * -self.d
        ang_force += integral_ang * -self.i

        
        # limit force
        if ang_force > self.angle_force_lim:
            ang_force = self.angle_force_lim
        elif ang_force < -self.angle_force_lim:
            ang_force = -self.angle_force_lim


        self.body.angle_force = ang_force

           
class Simulator:

    # Constructor
    def __init__(self, body:Body, wind_accel = (0,0), time_step = 0.01):
        self.body = body
        self.time_step = time_step
        self.step_count = 0
        self.wind = wind_accel

         # lists to store data for graphing
        self.x_pos = []
        self.x_time = []
        self.y_pos = []
        self.z_pos = []
        self.x_vel = []
        self.y_vel = []
        self.z_vel = []
        self.x_accel = []
        self.y_accel = []
        self.z_accel = []
        self.angle = []

    # Runs simulation until projectile reaches ground
    def run(self):
        integral_x = 0
        integral_y = 0
        integral_ang = 0

        while self.body.position[2] > 0:
            self.body.step(net_accel(self.body, self))
            self.step_count +=1

            self.body.update_pos_error()
            self.body.update_vel_error()
            self.body.update_angle_error()
            
            # update controller every 5 steps
            if self.step_count % 5 == 0:
                self.body.controller.correct_angle(integral_ang)
                self.body.controller.correct_xy(integral_x, integral_y)


            # Sets integrals for PID loops
            if self.body.pos_error[0] < 1:
                integral_x += self.body.pos_error[0]
            else:
                integral_x = 0

            if self.body.pos_error[1] < 1:
                integral_y += self.body.pos_error[1]
            else:
                integral_y = 0

            if self.body.ang_error < 1:
                integral_ang += self.body.ang_error
            else:
                integral_ang = 0


            # append data to lists for plotting
            self.x_pos.append(self.body.position[0]) 
            self.x_time.append(self.time_step*self.step_count)
            self.y_pos.append(self.body.position[1])
            self.z_pos.append(self.body.position[2])
            self.x_vel.append(self.body.velocity[0])
            self.y_vel.append(self.body.velocity[1])
            self.z_vel.append(self.body.velocity[2])
            self.x_accel.append(1)  #implement
            self.y_accel.append(1)  #implement
            self.z_accel.append(9.81)
            self.angle.append(self.body.angle)

            print(
                f"time: {self.step_count*self.time_step:0.3f}, {self.body.pos_report()}, {self.body.vel_report()}, {self.body.ang_report()}, {self.body.pos_error_report()}, {self.body.ang_error_report()}"
            )


"""Calculates net acceleration of projectile"""
def net_accel(body:Body, sim:Simulator):
    # define gravity and moment of inertia constants
    gravity = -9.81
    body_moi = 1/2 * body.mass * (body.radius ** 2)


    x_accel = body.drag[0] * ((body.velocity[0]) ** 2) + sim.wind[0] + body.xy_force[0]
    y_accel = body.drag[1] * ((body.velocity[1]) ** 2) + sim.wind[1] + body.xy_force[1]
    z_accel = gravity * body.mass + body.drag[2] * ((body.velocity[2]) ** 2)
    torque = body.angle_force


    return x_accel/body.mass, y_accel/body.mass, z_accel/body.mass, torque/body_moi


"""builds projectile and simulator"""
def run_skydiver_simulation():
    """Run 60kg skydiver simulation from 1000m (units = Metric)"""
    body = Body(mass=1, position=[0, 0, 122], velocity=[0, 0, 0], drag=(0, 0, 0), target=(7,15), angle = 0)
    sim = Simulator(body, wind_accel = (0,0))
    sim.run()
    graph(sim, body)


def graph(sim:Simulator, body:Body):
    # create a figure with three subplots
    fig, axs = plt.subplots(4, 1, figsize=(8, 12), sharex=True)

    # plot position data
    axs[0].plot(sim.x_time, sim.x_pos, label='x')
    axs[0].plot(sim.x_time, sim.y_pos, label='y')
    axs[0].axhline(body.target[0], color='r', linestyle='--', linewidth=1)
    axs[0].axhline(body.target[1], color='r', linestyle='--',linewidth=1)
    #axs[0].plot(sim.x_time, sim.z_pos, label='z')
    axs[0].set_ylabel('Position (m)')
    axs[0].legend()

    # plot velocity data
    axs[1].plot(sim.x_time, sim.x_vel, label='x')
    axs[1].plot(sim.x_time, sim.y_vel, label='y')
    axs[1].plot(sim.x_time, sim.z_vel, label='z')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].legend()

    # plot acceleration data
    axs[2].plot(sim.x_time, sim.x_accel, label='x')
    axs[2].plot(sim.x_time, sim.y_accel, label='y')
    # axs[2].plot(sim.x_time, sim.z_accel, label='z')
    axs[2].set_ylabel('Acceleration (m/s^2)')
    axs[2].set_xlabel('Time (s)')
    axs[2].legend()
    
    # angle error
    axs[3].plot(sim.x_time, sim.angle)
    axs[3].axhline(0, color='r', linestyle='--', linewidth=1)
    axs[3].set_xlabel('Time (s)')
    axs[3].set_ylabel('Angle (deg)')


    # add a title to the figure
    fig.suptitle('Position, Velocity, and Acceleration vs. Time')


    fig2, axs2 = plt.subplots(1, 1, figsize=(8, 12), sharex=True)
    
    # 3d position plot
    axs2 = plt.axes(projection='3d')
    axs2.plot(sim.x_pos, sim.y_pos, sim.z_pos, 'red')

    plt.show()

run_skydiver_simulation()