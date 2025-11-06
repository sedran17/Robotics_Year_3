import numpy as np
import matplotlib.pyplot as plt

def part_a():

    #Constants
    x_0 = 100
    x_f = 0
    h = 20
    d = 200
    t_0 = 0


    r = 0 # Noise
    kp = 500 #feedback gain
    dt = 0.01 #timestep
    phi_i = np.arctan(h/(d-x_0)) #initial angle
    phi_f = np.arctan(h/(d-x_f)) #final angle
    phi = phi_i
    u_0 = -kp*(phi - phi_f)
    x_k = x_0
    t_k = t_0
    u_k = u_0

    #Varibles to store that calculated values that will be graphed
    t = []
    x = []

    while x_k > 2:
        #Update the state
        v_k = np.random.uniform(-r, r)
        x_k = x_k + u_k*dt + v_k
        t_k = t_k + dt
        print(x_k)

        #update the measurement
        w_k = np.random.uniform(-h*r/d**2, h*r/d**2) #Noise
        phi = np.arctan(h/(d-x_k)) + w_k
        u_k = -kp*(phi - phi_f)
        t.append(t_k)
        x.append(x_k)

    plt.plot(t, x, color="red", label="r=0")
    plt.xlabel("Time")          # x-axis label
    plt.ylabel("Position")         # y-axis label
    plt.title("Part A: Distance from Robot to Origin")  # graph title
    plt.legend()
    plt.show()
    return

if __name__ == "__main__":
    part_a()