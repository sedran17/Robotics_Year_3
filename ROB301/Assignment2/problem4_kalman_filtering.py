import numpy as np
import matplotlib.pyplot as plt

def part_a():

    #Constants
    x_0 = 100.0
    x_f = 0.0
    h = 20.0
    d = 200.0
    t_0 = 0.0


    r = 0 # Noise
    kp = 500.0 #feedback gain
    dt = 0.001 #timestep
    phi_i = np.arctan(h/(d-x_0)) #initial angle
    phi_f = np.arctan(h/(d-x_f)) #final angle
    phi = phi_i
    u_0 = -kp*(phi - phi_f)
    x_k = x_0
    t_k = t_0
    u_k = u_0

    #Varibles to store the calculated values that will be graphed
    t = []
    x = []

    while x_k > 0.01:
        #update the measurement
        w_k = np.random.uniform(-h*r/d**2, h*r/d**2) #Noise
        phi = np.arctan(h/(d-x_k)) + w_k
        u_k = -kp*(phi - phi_f)
        t.append(t_k)
        x.append(x_k)
        #Update the state
        v_k = np.random.uniform(-r, r)
        x_k = x_k + u_k*dt + v_k
        t_k = t_k + dt
        print(x_k)

    plt.plot(t, x, color="red", label="r=0")
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title("Part A: Distance from Robot to Origin")
    plt.legend()
    plt.grid(True)
    plt.show()
    return

def part_c(r: int):
    #Constants
    x_0 = 100.0
    x_f = 0.0
    h = 20.0
    d = 200.0
    t_0 = 0.0
    P_c = 1.0 #predicted covariance matrix

    kp = 500.0 #feedback gain
    dt = 1.0 #timestep
    n = 50 # number timesteps
    x_k_t = x_0
    x_k = x_0
    t_k = t_0
    A_k = 1.0 #calculated in part b
    B_k = dt #calculated in part b
    W_k = 1.0 #noise matrix
    V_k = 1.0 #measurement noise matrix


    #Noise variances
    var_v = (r**2)/3
    var_w = ((h**2)*(r**2))/(3*(d**4))

    #Varibles to store the calculated values that will be graphed
    x_true = []
    x = []
    t = []

    while t_k < n:
        t_k = t_k + dt
        t.append(t_k)
        #True System
        #Measurement
        w_k = np.random.uniform(-h*r/d**2, h*r/d**2)
        phi = np.arctan2(h, d - x_k_t) + w_k

        #Control
        u_k = -kp * (h / d**2) * x_k

        #Motion
        v_k = np.random.uniform(-r, r)
        x_k_t = x_k_t+u_k*dt + v_k

        #EKF
        x_p = x_k+u_k*B_k #predicted x
        P_p = A_k * P_c * A_k + V_k * var_v * V_k # predicted covariance

        D_k = h / ((d - x_p)**2 + h**2)
        phi_p = np.arctan2(h, d - x_p)
        innovation = phi - phi_p
        S_k = D_k * P_p * D_k + W_k * var_w

        #Updates
        K_k = P_p * D_k / S_k
        x_k = x_p + K_k * innovation
        P_c = P_p - K_k * D_k* P_p

        #Store to be graphed
        x_true.append(x_k_t)
        x.append(x_k)

    plt.plot(t, x_true, color="red", label="True position")
    title = "EKF Control Simulation (r = " + str(r) + ")"
    plt.plot(t, x, color="blue", label="EKF position")
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def part_di():
    #Constants
    x_0 = 100.0
    x_f = 0.0
    h = 20.0
    d = 200.0
    t_0 = 0.0
    P_c = 1.0 #predicted covariance matrix

    r = 0
    kp = 500.0 #feedback gain
    dt = 1.0 #timestep
    n = 50 # number timesteps
    x_k_t = x_0
    x_k = x_0
    t_k = t_0
    A_k = 1.0 #calculated in part b
    B_k = dt #calculated in part b
    W_k = 1.0 #noise matrix
    V_k = 1.0 #measurement noise matrix


    #Noise variances
    var_v = (r**2)/3
    var_w = ((h**2)*(r**2))/(3*(d**4))

    #Varibles to store the calculated values that will be graphed
    x_true = [x_0]
    x = [x_0]
    t = [t_0]

    while t_k < n:
        t_k = t_k + dt
        t.append(t_k)
        #True System
        #Measurement
        w_k = np.random.uniform(-h*r/d**2, h*r/d**2)
        phi = np.arctan2(h, d - x_k_t)

        #Control
        u_k = -kp * (h / d**2) * x_k

        #Motion
        v_k = np.random.uniform(-r, r)
        x_k_t = x_k_t+u_k*dt + v_k

        #EKF
        x_p = x_k+u_k*B_k #predicted x
        P_p = A_k * P_c * A_k + V_k * var_v * V_k # predicted covariance

        D_k = h / ((d - x_p)**2 + h**2)
        phi_p = np.arctan2(h, d - x_p)
        innovation = phi - phi_p
        S_k = D_k * P_p * D_k + W_k * var_w

        #Updates
        K_k = P_p * D_k / S_k
        x_k = x_p + K_k * innovation
        P_c = P_p - K_k * D_k* P_p

        #Store to be graphed
        x_true.append(x_k_t)
        x.append(x_k)

    plt.plot(t, x_true, color="red", label="True position")
    title = "EKF Control Simulation (r = " + str(r) + ")"
    plt.plot(t, x, color="blue", label="EKF position")
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def part_dii_iii(true_pos:bool, r:int):
    #Constants
    x_0 = 100.0
    x_f = 0.0
    h = 20.0
    d = 200.0
    t_0 = 0.0
    P_c = 1.0 #predicted covariance matrix

    kp = 500.0 #feedback gain
    dt = 1.0 #timestep
    n = 50 # number timesteps
    x_k_t = x_0
    x_k = x_0
    t_k = t_0
    A_k = 1.0 #calculated in part b
    B_k = dt #calculated in part b
    W_k = 1.0 #noise matrix
    V_k = 1.0 #measurement noise matrix


    #Noise variances
    var_v = (r**2)/3
    var_w = ((h**2)*(r**2))/(3*(d**4))

    #Varibles to store the calculated values that will be graphed
    x_true = [x_0]
    x = [x_0]
    t = [t_k]

    while t_k < n:
        t_k = t_k + dt
        t.append(t_k)
        #True System
        #Measurement
        w_k = np.random.uniform(-h*r/d**2, h*r/d**2)
        phi = np.arctan2(h, d - x_k_t)

        #Control
        u_k = -kp * (h / d**2) * x_k

        #Motion
        v_k = np.random.uniform(-r, r)
        x_k_t = x_k_t+u_k*dt + v_k

        #EKF
        x_p = x_k+u_k*B_k #predicted x
        P_p = A_k * P_c * A_k + V_k * var_v * V_k # predicted covariance

        D_k = h / ((d - x_p)**2 + h**2)
        phi_p = np.arctan2(h, d - x_p)
        innovation = phi - phi_p
        S_k = D_k * P_p * D_k + W_k * var_w

        #Updates
        K_k = P_p * D_k / S_k
        x_k = x_p + K_k * innovation
        P_c = P_p - K_k * D_k* P_p

        #Store to be graphed
        x_true.append(x_k_t)
        x.append(x_k)

    if true_pos:
        plt.plot(t, x_true, color="red", label="True position")
        title = "EKF True Position (r = " + str(r) + ")"
    else:
        plt.plot(t, x, color="blue", label="EKF position")
        title = "EKF Position (r = " + str(r) + ")"
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def part_ei():
    #Constants
    x_0 = 100.0
    x_f = 0.0
    h = 20.0
    d = 200.0
    t_0 = 0.0
    P_c = 1.0 #predicted covariance matrix

    r = 0
    kp = 500.0 #feedback gain
    dt = 1.0 #timestep
    n = 50 # number timesteps
    x_k_t = x_0
    x_k = x_0
    t_k = t_0
    A_k = 1.0 #calculated in part b
    B_k = dt #calculated in part b
    W_k = 1.0 #noise matrix
    V_k = 1.0 #measurement noise matrix


    #Noise variances
    var_v = (r**2)/3
    var_w = ((h**2)*(r**2))/(3*(d**4))

    #Varibles to store the calculated values that will be graphed
    x_true = [x_0]
    x = [x_0]
    t = [t_k]

    while t_k < n:
        t_k = t_k + dt
        t.append(t_k)
        #True System
        #Measurement
        w_k = np.random.uniform(-h*r/d**2, h*r/d**2)
        phi = np.arctan2(h, d - x_k_t)

        #Control
        u_k = -kp * (h / d**2) * x_k

        #Motion
        v_k = np.random.uniform(-r, r)
        x_k_t = x_k_t+u_k*dt + v_k

        #EKF
        x_p = x_k+u_k*B_k #predicted x
        P_p = A_k * P_c * A_k + V_k * var_v * V_k # predicted covariance

        D_k = h / ((d - x_p)**2 + h**2)
        phi_p = np.arctan2(h, d - x_p)
        innovation = phi - phi_p
        S_k = D_k * P_p * D_k + W_k * var_w

        #Updates
        K_k = P_p * D_k / S_k
        x_k = x_p + K_k * innovation
        P_c = P_p - K_k * D_k* P_p

        #Store to be graphed
        x_true.append(x_k_t)
        x.append(x_k)

    plt.plot(t, x_true, color="red", label="True position")
    title = "Baseline Noiseless Position (r = " + str(r) + ")"
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def part_eii_iii(true_pos:bool, r:int):
    #Constants
    x_0 = 100.0
    x_f = 0.0
    h = 20.0
    d = 200.0
    t_0 = 0.0
    P_c = 1.0 #predicted covariance matrix

    kp = 500.0 #feedback gain
    dt = 1.0 #timestep
    n = 50 # number timesteps
    x_k_t = x_0
    x_k = x_0
    t_k = t_0
    A_k = 1.0 #calculated in part b
    B_k = dt #calculated in part b
    W_k = 1.0 #noise matrix
    V_k = 1.0 #measurement noise matrix


    #Noise variances
    var_v = (r**2)/3
    var_w = ((h**2)*(r**2))/(3*(d**4))

    #Varibles to store the calculated values that will be graphed
    x_true = [x_0]
    x = [x_0]
    t = [t_k]

    while t_k < n:
        t_k = t_k + dt
        t.append(t_k)
        #True System
        #Measurement
        w_k = np.random.uniform(-h*r/d**2, h*r/d**2)
        phi = np.arctan2(h, d - x_k_t)

        #Control
        u_k = -kp * (h / d**2) * x_k

        #Motion
        v_k = np.random.uniform(-r, r)
        x_k_t = x_k_t+u_k*dt + v_k

        #EKF
        x_p = x_k+u_k*B_k #predicted x
        P_p = A_k * P_c * A_k + V_k * var_v * V_k # predicted covariance

        D_k = h / ((d - x_p)**2 + h**2)
        phi_p = np.arctan2(h, d - x_p)
        innovation = phi - phi_p
        S_k = D_k * P_p * D_k + W_k * var_w

        #Updates
        K_k = P_p * D_k / S_k
        x_k = x_p + K_k * innovation
        P_c = P_p - K_k * D_k* P_p

        #Store to be graphed
        x_true.append(x_k_t)
        x.append(x_k)

    if true_pos:
        plt.plot(t, x_true, color="red", label="True position")
        title = "Noise in Measurements and Motion Disabled EKF True Position (r = " + str(r) + ")"
    else:
        plt.plot(t, x, color="blue", label="EKF position")
        title = "Noise in Measurements and Motion Disabled EKF Position (r = " + str(r) + ")"
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    #part_a()
    #part_di()
    '''part_dii_iii(True, 1)
    part_dii_iii(True, 2.5)
    part_dii_iii(True, 10)

    part_dii_iii(False, 1)
    part_dii_iii(False, 2.5)
    part_dii_iii(False, 10)'''

    #part_ei()
    part_eii_iii(True, 1)
    part_eii_iii(True, 2.5)
    part_eii_iii(True, 10)

    part_eii_iii(False, 1)
    part_eii_iii(False, 2.5)
    part_eii_iii(False, 10)
