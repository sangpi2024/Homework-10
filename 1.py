import numpy as np
from scipy.optimize import minimize
from scipy.integrate import odeint

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)
m_car = 450  # Mass of the car (kg)
# Assuming a mass for the wheel (placeholder value, please replace with the actual mass)
m_wheel = 40  # Mass of the wheel (kg)

# Calculate minimum and maximum spring constants based on static compression
def calculate_spring_constants(m, min_compression, max_compression):
    k_min = m * g / max_compression
    k_max = m * g / min_compression
    return k_min, k_max

# Static compression values in meters
compression_suspension = (0.0762, 0.1524)  # 3" to 6"
compression_tire = (0.0381, 0.01905)       # 1.5" to 0.75"

# Calculating spring constants for suspension (k1) and tire (k2)
k1_min, k1_max = calculate_spring_constants(m_car, *compression_suspension)
k2_min, k2_max = calculate_spring_constants(m_wheel, *compression_tire)

# Equations of motion for the quarter car model
def quarter_car_model(Y, t, k1, c1, k2, v, ymag, tramp):
    x1, x1_dot, x2, x2_dot = Y
    if t < tramp:
        y = ymag * (t / tramp)
    else:
        y = ymag

    # Differential equations
    x1_ddot = (k1 * (x2 - x1) + c1 * (x2_dot - x1_dot)) / m_car
    x2_ddot = (-k1 * (x2 - x1) - c1 * (x2_dot - x1_dot) + k2 * (y - x2)) / m_wheel

    return [x1_dot, x1_ddot, x2_dot, x2_ddot]

# Initial conditions (assuming the car starts at rest at the datum level)
initial_conditions = [0, 0, 0, 0]


# Objective function for optimization
def objective_function(params, *args):
    k1, c1, k2 = params
    time_vector, ymag, tramp = args
    # Solve the ODE with current parameters
    results = odeint(quarter_car_model, initial_conditions, time_vector, args=(k1, c1, k2, v, ymag, tramp))

    # Calculate the sum of squared errors (SSE) with penalties for violating spring constant bounds
    sse = 0
    for i, t in enumerate(time_vector):
        x1 = results[i, 0]
        if t < tramp:
            yroad = ymag * (t / tramp)
        else:
            yroad = ymag
        sse += (x1 - yroad) ** 2

    # Penalties for spring constants outside the valid range
    if k1 < k1_min or k1 > k1_max:
        sse += 100
    if k2 < k2_min or k2 > k2_max:
        sse += 100

    # Assuming a reasonable acceleration limit (e.g., 2.0g), add penalties if exceeded
    accel = np.diff(results[:, 1]) / np.diff(time_vector)  # Approximate derivative
    accel_limit = 2.0 * g
    exceedances = accel[accel > accel_limit]
    sse += np.sum((exceedances - accel_limit) ** 2)

    return sse

# Optimization
def optimize_suspension(time_vector, ymag, tramp, initial_guess):
    result = minimize(
        objective_function,
        initial_guess,
        args=(time_vector, ymag, tramp),
        method='Nelder-Mead'
    )
    return result.x  # Returns the optimized parameters

# Time vector for the simulation
tmax = 3.0
t = np.linspace(0, tmax, 100)
# Ramp properties (specified in the GUI, here are placeholders)
v = 15  # Car speed in m/s
ymag = 0.1524  # Ramp height in meters (6 inches)
tramp = ymag / (np.tan(np.radians(45)) * v)  # Time to traverse the ramp

# Initial guess for the parameters
initial_guess = [k1_min, 1000, k2_min]  # Example values for k1, c1, k2

# Perform optimization
optimized_params = optimize_suspension(t, ymag, tramp, initial_guess)

# Output the optimized parameters
print(f"Optimized k1: {optimized_params[0]}")
print(f"Optimized c1: {optimized_params[1]}")
print(f"Optimized k2: {optimized_params[2]}")
