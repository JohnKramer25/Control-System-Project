# Simulates a reaction failure and different methods of triggering the alarm (EWMA (Exponentially Weignted Moving Average) vs Rolling Average)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Alarm condition
ALARM_THRESHOLD = 55

# Simulate 100 minutes of reactor time
time = np.arange(0, 100)

# Target temperature is 50
# The reactor holds steady at 50, but at minute 80, a cooling pump fails
true_temp = np.where(time < 80, 50, 50 + (time - 80) * 1.5)

# Added "Sensor Noise"
noise = np.random.normal(0, 1.5, size=len(time))

# The Final Reading (Signal + Noise)
sensor_readings = true_temp + noise

# Store in a DataFrame
df = pd.DataFrame({
    'Time_Min': time,
    'Temperature_C': sensor_readings
})



# Allow a rolling average to be calculated from the previous 5 pieces of temperature data
df['Smoothed_Temp'] = df['Temperature_C'].rolling(window=5).mean()

# Make alarm condition for the slower, average calculator
alarm_triggered_avg = df[df['Smoothed_Temp'] > ALARM_THRESHOLD]
#note: alarm_triggered_avg is a smaller dataframe composed of the smoothed_temp values that were above 55 degrees C, as well as the time and sensor readings (same applies for EWMA equvalent)

# Make alarm condition for the fast, EWMA calculator (exponentially weighted moving average)
alarm_triggered_EWMA = df[df['Temperature_C'].ewm(span=5).mean() > ALARM_THRESHOLD]


# What happens when temp is above 55?
if not alarm_triggered_avg.empty:
    first_alarm_time_avg = alarm_triggered_avg.iloc[0]['Time_Min']
    print(f"ALARM TRIGGERED at Minute: {first_alarm_time_avg} by rolling average")
    print("Action: EMERGENCY COOLING ACTIVATED.")
else:
    print('Status: Normal Operation')

if not alarm_triggered_EWMA.empty:
    first_alarm_time_EWMA = alarm_triggered_EWMA.iloc[0]['Time_Min']
    print(f"ALARM TRIGGERED at Minute: {first_alarm_time_EWMA} by EWMA")
    print("Action: EMERGENCY COOLING ACTIVATED.")

# Which system is better?
winner = ''
if (first_alarm_time_EWMA > first_alarm_time_avg):
    winner = 'Smoothed Signal'
elif (first_alarm_time_EWMA < first_alarm_time_avg):
    winner = 'EWMA Signal'
if winner != '':
    print(f'{winner} signaled the alarm faster')

# Graph it
plt.figure(figsize=(12, 6))
plt.plot(df['Time_Min'], df['Temperature_C'], color='grey', alpha=0.5, label='Raw Sensor Data')
plt.plot(df['Time_Min'], true_temp, color='red', linestyle='--', label='True Temperature (Hidden)')
plt.plot(df['Time_Min'], df['Smoothed_Temp'], color = 'blue', linewidth = 2, label = 'Smoothed Signal (Moving Average)')
plt.plot(df['Time_Min'], df['Temperature_C'].ewm(span=5).mean(), color = 'orange', label = 'EWMA Signal (Moving Average)')
plt.hlines(55, 0, 100, colors='black', label='Alarm Threshold (55C)')
plt.title('Reactor Temperature Sensor (With Noise)')
plt.xlabel('Time (min)')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.show()

