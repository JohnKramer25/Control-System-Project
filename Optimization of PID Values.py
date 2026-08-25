# Control system designed to regulate temperature of a reactor using the PID method


import numpy as np
import matplotlib.pyplot as plt
import statistics
import pandas as pd

# CONFIGURATION
SETPOINT = 50.0
Kp = 2.0     # Proportional (The base cooling)
Ki = 0.1     # Integral (The Memory - fixes offset)
Kd = 1.0     # Derivative (The Brakes - stops oscillation)
def run_reactor_sim(Kp, Ki, Kd=1, return_all_data=False):
        
        time_history = []
        pv_history=[]

        SETPOINT = 50.0
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

        # Error variable
        total_abs_error = 0

        # THE SIMULATION LOOP
        # Simulate 100 minutes
        for t in range(1, 200):

            # Get the Previous Temperature
            current_temp = history_temp[-1]
            # Simulation - a reactor generating heat requiring cooling
            # Disturbance: At t=80, the pump breaks and adds +1.0 degree heat per minute
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

            # UPDATE THE SYSTEM
            # New Temp = Old Temp + (Heat In) - (Heat Removed)
            new_temp = current_temp + heat_added - total_cooling_action

            #Update error, time histrory, and pv history
            total_abs_error += abs(error)
            pv_history.append(new_temp)
            time_history.append(t)

        if return_all_data:
             return total_abs_error, time_history, pv_history
        else:
            return total_abs_error

            
# Part 2: the Optimization

print("Running Optimization of Variables")
results = []

# test kp and ki
kp_test_range=np.linspace(.01,5,50)
ki_test_range=np.linspace(.01,.1,50)
score  = 0
for kp_test in kp_test_range:
     for ki_test in ki_test_range:
          score = 0
          for i in range(10):
            score += run_reactor_sim(kp_test, ki_test)
          results.append({'Kp': kp_test, 'Ki' : ki_test, 'Error' : score/10})
df = pd.DataFrame(results)
print(df.head())

# Part 3: graph these 'optimal values' for p and i
heatmap_data = df.pivot(index='Ki', columns='Kp', values='Error')
plt.figure(figsize=(10, 8))
# Use 'imshow' to create a heatmap
plt.imshow(heatmap_data, cmap='viridis_r', interpolation='bilinear', origin='lower',
           extent=[df['Kp'].min(), df['Kp'].max(), df['Ki'].min(), df['Ki'].max()],
           aspect='auto')

plt.colorbar(label='Total Error (Lower is Better)')
plt.xlabel('Proportional Gain (Kp)')
plt.ylabel('Integral Gain (Ki)')
plt.title('PID Tuning Optimization Map')

# Mark the best spot
best_run = df.loc[df['Error'].idxmin()]
plt.scatter(best_run['Kp'], best_run['Ki'], color='red', marker='x', s=100, label='Optimal Point')
plt.legend()

plt.show()

print(f"RECOMMENDATION: The optimal settings are Kp={best_run['Kp']:.2f} and Ki={best_run['Ki']:.2f}")

import numpy as np

baseline_iae = run_reactor_sim(1,0)
optimized_iae = run_reactor_sim(best_run['Kp'], best_run['Ki'])

# --- 1. Calculate Error Reduction (Accuracy) ---
# Formula: (Old Error - New Error) / Old Error
# Let's assume you used Integral Absolute Error (IAE)
improvement = abs((baseline_iae - optimized_iae) / baseline_iae) * 100

print(f"Optimization improved control accuracy by {improvement:.1f}%")

# --- 2. Calculate Standard Deviation (Consistency) ---
# "Consistency" in control theory is usually how much the value wiggles 
# once it's supposed to be steady.
# Take the last 50 data points (steady state)
optimized_error, time_data, pv_data = run_reactor_sim(best_run['Kp'], best_run['Ki'], return_all_data=True)
steady_state_data = pv_data[-50:] 
consistency_metric = np.std(steady_state_data)

print(f"Maintained process variable consistency within "
      f"+/- {consistency_metric:.4f} units at steady state.")
