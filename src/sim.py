import math
from matplotlib import pyplot as plt

class Body:
    """Class for a projectile with mass, radius, position, velocity, angle, angular velocity, drag, target, xy_force, and angle_force"""

    def __init__(self, mass = 1, radius = .05, position = (0, 0, 122), velocity = (0, 0, 0), angle = 0, angle_vel = 0, drag = (0,0,0), target = (0,0), xy_force = (0,0), angle_force = 0):
        # constants
        self.mass = mass
        self.radius = radius
        self.drag = drag
        self.target = target
        self.target_vel = (0,0)
        self.target_angle_vel = 0
        self.controller = Controller(self)

        # state variables
        self.position = list(position)
        self.velocity = list(velocity)
        self.angle = angle
        self.angle_vel = angle_vel

        # error variables
        self.pos_error = [0,0]
        self.vel_error = [0,0]
        self.ang_error = 0
        self.ang_vel_error = 0
        

        # force variables
        self.xy_force = list(xy_force)
        self.angle_force = angle_force
    
    
    def step(self, net_accel, time_step = 0.01):
        """Integrates xyz/angular accelerations to corresponding velocity and position of projectile"""
        
        # integrates to find new position and velocity
        for i in range(3):
            self.velocity[i] += net_accel[i] * time_step
            self.position[i] += self.velocity[i] * time_step

        # integrates to find new angle and angular velocity
        self.angle_vel += net_accel[3] * time_step
        self.angle += self.angle_vel * time_step
        self.angle = self.angle % 360
        if self.angle < 0:
            self.angle += 360
        
    """updates position, velocity, and angle errors"""
    def update_pos_error(self):
        self.pos_error = [curr-target for curr, target in zip(self.position, self.target)]
    
    def update_vel_error(self):
        self.vel_error = [velocity-target for velocity, target in zip(self.velocity, self.target_vel)]
        
    def update_angle_error(self):
        self.ang_error =  self.angle
        if self.ang_error > 180:
            self.ang_error -= 360

    def update_ang_vel_error(self):
        self.ang_vel_error = self.angle_vel - self.target_angle_vel
    
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
    """Class for a PID controller with a body, force limit, and PID constants"""
    def __init__(self, body:Body):
        self.body = body
        self.force_lim = 50
        self.angle_force_lim = 10
        
        # xy PID constants
        self.p = 15
        self.i = .15
        self.d = 5

        # angle PID constants
        self.ang_p = 2
        self.ang_i = .001
        self.ang_d = .2


    def correct_xy(self, integral_x, integral_y):
        """Calculates xy force to apply to body"""

        # x axis
        force_x = self.body.pos_error[0] * -self.p
        force_x += self.body.velocity[0] * -self.d
        force_x += integral_x * -self.i

        # y axis
        force_y = self.body.pos_error[1] * -self.p
        force_y += self.body.velocity[1] * -self.d
        force_y += integral_y * -self.i

        # limit force
        if force_x > self.force_lim:
            force_x = self.force_lim
        elif force_x < -self.force_lim:
            force_x = -self.force_lim

        if force_y > self.force_lim:
            force_y = self.force_lim
        elif force_y < -self.force_lim:
            force_y = -self.force_lim


        self.body.xy_force = [force_x, force_y]


    def correct_angle(self, integral_ang):
        """Calculates angular force to apply to body"""
        
        # angular force
        ang_force = self.body.ang_error * -self.ang_p
        ang_force += self.body.ang_vel_error * -self.ang_d
        ang_force += integral_ang * -self.ang_i

        # limit force
        if ang_force > self.angle_force_lim:
            ang_force = self.angle_force_lim
        elif ang_force < -self.angle_force_lim:
            ang_force = -self.angle_force_lim


        self.body.angle_force = ang_force

           
class Simulator:
    """class that simulates a projectile in 3D space"""

    def __init__(self, body:Body, wind_accel = (0,0), time_step = 0.01):
        # constants
        self.body = body
        self.time_step = time_step
        self.step_count = 0
        self.wind = wind_accel

        # lists to store data for graphing
        self.time = []

        self.x_pos = []
        self.y_pos = []
        self.z_pos = []

        self.x_vel = []
        self.y_vel = []
        self.z_vel = []
        
        self.x_accel = []
        self.y_accel = []
        self.z_accel = []

        self.angle = []
        self.angle_vel = []
        self.angle_accel = []


    def run(self):
        """Runs simulation until body reaches ground"""

        integral_x = 0
        integral_y = 0
        integral_ang = 0

        while self.body.position[2] > 0:
            body_accel = net_accel(self.body, self)
            self.body.step(body_accel)
            self.step_count +=1

            # update errors
            self.body.update_pos_error()
            self.body.update_vel_error()
            self.body.update_angle_error()
            self.body.update_ang_vel_error()
            
            # update controller every 5 steps
            if self.step_count % 1 == 0:
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
            self.time.append(self.time_step*self.step_count)

            self.x_pos.append(self.body.position[0])
            self.y_pos.append(self.body.position[1])
            self.z_pos.append(self.body.position[2])
            
            self.x_vel.append(self.body.velocity[0])
            self.y_vel.append(self.body.velocity[1])
            self.z_vel.append(self.body.velocity[2])

            self.x_accel.append(body_accel[0])
            self.y_accel.append(body_accel[1])
            self.z_accel.append(body_accel[2])

            self.angle.append(self.body.angle)
            self.angle_vel.append(self.body.angle_vel)
            self.angle_accel.append(body_accel[3])

            print(
                f"time: {self.step_count*self.time_step:0.3f}, {self.body.pos_report()}, {self.body.vel_report()}, {self.body.ang_report()}, {self.body.pos_error_report()}, {self.body.ang_error_report()}"
            )



def net_accel(body:Body, sim:Simulator):
    """Calculates net acceleration of projectile"""

    # define constants
    gravity = -9.81
    body_moi = 1/2 * body.mass * (body.radius ** 2)
    convert = 180/math.pi


    x_accel = body.drag[0] * ((body.velocity[0]) ** 2) + sim.wind[0] + body.xy_force[0] *  math.cos(body.angle/convert) + body.xy_force[1] *  math.sin(body.angle/convert)
    y_accel = body.drag[1] * ((body.velocity[1]) ** 2) + sim.wind[1] + body.xy_force[1] *  math.cos(body.angle/convert) + body.xy_force[0] *  math.sin(body.angle/convert)
    z_accel = gravity * body.mass + body.drag[2] * ((body.velocity[2]) ** 2)
    torque = body.angle_force


    return x_accel/body.mass, y_accel/body.mass, z_accel/body.mass, torque/body_moi



def run_skydiver_simulation():
    """builds projectile and simulator and runs simulation"""

    body = Body(mass=1, position=[0, 0, 122], velocity=[0, 0, 0], drag=(0, 0, 0), target=(-7,-15), angle = 181)
    sim = Simulator(body, wind_accel = (0,0))
    sim.run()
    graph(sim, body)


def graph(sim:Simulator, body:Body):
    """graphs data from simulation"""

    # create a figure with three subplots
    fig, axs = plt.subplots(4, 1, figsize=(8, 12), sharex=True)
    axs2 = plt.subplots(1, 1, figsize=(8, 12), sharex=True)

    # plot position data
    axs[0].plot(sim.time, sim.x_pos, label='x')
    axs[0].plot(sim.time, sim.y_pos, label='y')
    axs[0].axhline(body.target[0], color='r', linestyle='--', linewidth=1)
    axs[0].axhline(body.target[1], color='r', linestyle='--',linewidth=1)
    axs[0].set_ylabel('Position (m)')
    axs[0].legend()

    # plot velocity data
    axs[1].plot(sim.time, sim.x_vel, label='x')
    axs[1].plot(sim.time, sim.y_vel, label='y')
    axs[1].plot(sim.time, sim.z_vel, label='z')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].legend()

    # plot acceleration data(z not plotted)
    axs[2].plot(sim.time, sim.x_accel, label='x')
    axs[2].plot(sim.time, sim.y_accel, label='y')

    axs[2].set_ylabel('Acceleration (m/s^2)')
    axs[2].set_xlabel('Time (s)')
    axs[2].legend()
    
    # angle error
    axs[3].plot(sim.time, sim.angle)
    axs[3].axhline(0, color='r', linestyle='--', linewidth=1)
    axs[3].set_xlabel('Time (s)')
    axs[3].set_ylabel('Angle (deg)')


    # add a title to the figure
    fig.suptitle('Position, Velocity, Angle, and Acceleration vs. Time')
    
    # 3d position plot
    axs2 = plt.axes(projection='3d')
    axs2.plot(sim.x_pos, sim.y_pos, sim.z_pos, 'red')

    plt.show()

if __name__ == "__main__":
    run_skydiver_simulation()