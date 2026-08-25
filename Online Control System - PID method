# Control system designed to regulate temperature of a reactor using the PID method


import numpy as np
import matplotlib.pyplot as plt
import statistics

# CONFIGURATION
SETPOINT = 50.0
Kp = 2.0     # Proportional (The base cooling)
Ki = 0.1     # Integral (The Memory - fixes offset)
Kd = 1.0     # Derivative (The Brakes - stops oscillation)

# Set up a filtered signal in order to use D term of PID
filtered_temp = 50
alpha = 0.2

# Storage lists to keep track of history
history_temp = [50.0]  # Start at 50 degrees
history_time = [0]
history_valve = [0.5]  # 0.5% valve opening to start - same as cooling power
# PID Variables
integral_sum = 0
previous_error = 0

# THE SIMULATION LOOP
# Simulate 100 minutes
for t in range(1, 100):

    # Get the Previous Temperature
    current_temp = history_temp[-1]
    # PHYSICS SIMULATION - a reactor generating heat requiring cooling
    # Disturbance: At t=80, the pump breaks and adds 1.0 degree heat per minute
    current_valve_pos = history_valve[-1]
    if t >= 0:
        heat_added = 0.5
    if t >= 50:
        heat_added = 2.0  # The runaway reaction heat
        
    # MEASUREMENT (The Sensor)
    # Add random noise
    raw_sensor_reading = current_temp + np.random.normal(0, 0.4)

    # Filter the reading
    filtered_sensor_reading = (raw_sensor_reading * alpha) + (1-alpha) * filtered_temp

    # Save state for next loop
    filtered_temp = filtered_sensor_reading
    
    # THE CONTROLLER:
    # Calculate Error
    error = filtered_sensor_reading - SETPOINT
    # Integral calculation
    integral_sum += error

    # PID Variables
    P = Kp * error
    I = Ki * integral_sum
    slope = error - previous_error
    D = Kd * slope

    # Set Previous Error
    previous_error = error

    # Calculate proper cooling measures
    base_valve = 0.5
    pid_adjustment = P + I + D
    total_cooling_action = base_valve + pid_adjustment

    # Restrict cooling action to decrease wear on cooling pump
    # MCC = Maximum Cooling Change - determined while considering the worse case scenarios
    MCC = 4
    if total_cooling_action < 0:
        total_cooling_action = 0
    if total_cooling_action > MCC:
        total_cooling_action = MCC

    # UPDATE THE SYSTEM
    # New Temp = Old Temp + (Heat In) - (Heat Removed)
    new_temp = current_temp + heat_added - total_cooling_action

    # Save Data for Plotting
    history_temp.append(new_temp)
    history_time.append(t)
    history_valve.append(total_cooling_action)

# GRAPHING THE DATA
plt.figure(figsize=(10, 8))

# Plot 1: Temperature vs Time
plt.subplot(2, 1, 1) # Top graph
plt.plot(history_time, history_temp, color='blue', label='Controlled Temp')
plt.hlines(SETPOINT, 0, 100, colors='green', linestyles='--', label='Target (50°C)')
plt.hlines(55, 0, 100, colors='red', linestyles='--', label='Alarm Limit')
plt.title(f'P-Controller Performance (Kp={Kp})')
plt.ylabel('Temperature (°C)')
plt.xlabel('Time (Minutes)')
plt.legend()
plt.grid(True)

# Plot 2: Valve Action vs Time
plt.subplot(2, 1, 2) # Bottom graph
plt.plot(history_time, history_valve, color='orange', label='Cooling Valve Action')
plt.ylabel('Cooling Power')
plt.xlabel('Time (Minutes)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
