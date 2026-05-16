from os import system

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

distance = ctrl.Antecedent(np.arange(0, 51, 1), 'distance')        
traffic = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic')
demand = ctrl.Antecedent(np.arange(0, 101, 1), 'demand')          
weather = ctrl.Antecedent(np.arange(0, 11, 1), 'weather')          
rating = ctrl.Antecedent(np.arange(1.0, 5.1, 0.1), 'rating')        
punctuality = ctrl.Antecedent(np.arange(0, 101, 1), 'punctuality')   

price = ctrl.Consequent(np.arange(0, 101, 1), 'price')
reward = ctrl.Consequent(np.arange(0, 101, 1), 'reward')

distance['short'] = fuzz.trimf(distance.universe, [0, 0, 3])
distance['medium'] = fuzz.trimf(distance.universe, [2, 5, 8])
distance['long'] = fuzz.trimf(distance.universe, [6, 13, 20])
distance['very_long'] = fuzz.trimf(distance.universe, [15, 30, 50])

traffic['low'] = fuzz.trimf(traffic.universe, [0, 0, 30])
traffic['medium'] = fuzz.trimf(traffic.universe, [20, 50, 70])
traffic['high'] = fuzz.trimf(traffic.universe, [60, 80, 100])

demand['low'] = fuzz.trimf(demand.universe, [0, 0, 30])
demand['medium'] = fuzz.trimf(demand.universe, [20, 50, 70])
demand['high'] = fuzz.trimf(demand.universe, [60, 80, 100])

weather['good'] = fuzz.trimf(weather.universe, [0, 0, 4])
weather['moderate'] = fuzz.trimf(weather.universe, [3, 5, 7])
weather['bad'] = fuzz.trimf(weather.universe, [6, 8, 10])

rating['poor'] = fuzz.trimf(rating.universe, [1.0, 1.0, 2.5])
rating['average'] = fuzz.trimf(rating.universe, [2.0, 3.0, 4.0])
rating['good'] = fuzz.trimf(rating.universe, [3.5, 4.5, 5.0])

punctuality['late'] = fuzz.trimf(punctuality.universe, [0, 0, 50])
punctuality['on_time'] = fuzz.trimf(punctuality.universe, [40, 60, 80])
punctuality['early'] = fuzz.trimf(punctuality.universe, [70, 85, 100])

price['low'] = fuzz.trimf(price.universe, [0, 0, 30])
price['medium'] = fuzz.trimf(price.universe, [25, 50, 75])
price['high'] = fuzz.trimf(price.universe, [60, 75, 90])
price['very_high'] = fuzz.trimf(price.universe, [80, 90, 100])

reward['none'] = fuzz.trimf(reward.universe, [0, 0, 20])
reward['few'] = fuzz.trimf(reward.universe, [15, 40, 60])
reward['medium'] = fuzz.trimf(reward.universe, [50, 70, 85])
reward['high'] = fuzz.trimf(reward.universe, [75, 90, 100])

rules = [
    ctrl.Rule(distance['short'] & traffic['low'] & demand['low'], price['low']),
    ctrl.Rule(distance['short'] & traffic['medium'] & demand['high'], price['medium']),
    ctrl.Rule(distance['medium'] & traffic['high'] & demand['high'], price['high']),
    ctrl.Rule(distance['long'] & traffic['medium'] & weather['good'], price['medium']),
    ctrl.Rule(distance['long'] & traffic['high'] & weather['bad'], price['very_high']),
    ctrl.Rule(distance['very_long'] & traffic['high'] & demand['high'], price['very_high']),
    ctrl.Rule(distance['medium'] & traffic['low'] & demand['low'], price['medium']),
    ctrl.Rule(distance['short'] & traffic['high'] & weather['bad'], price['high']),
    ctrl.Rule(distance['very_long'] & weather['bad'], price['very_high']),
    ctrl.Rule(distance['medium'] & traffic['medium'] & weather['moderate'], price['medium']),

    ctrl.Rule(rating['good'] & punctuality['early'], reward['high']),
    ctrl.Rule(rating['average'] & punctuality['on_time'], reward['medium']),
    ctrl.Rule(rating['poor'] & punctuality['late'], reward['none']),
    ctrl.Rule(distance['long'] & traffic['high'] & punctuality['on_time'], reward['high']),
    ctrl.Rule(distance['medium'] & traffic['medium'] & rating['good'], reward['medium']),
    ctrl.Rule(rating['poor'] & punctuality['late'], reward['none']),
    ctrl.Rule(distance['very_long'] & weather['bad'] & rating['good'], reward['high']),
    ctrl.Rule(distance['short'] & rating['average'] & punctuality['on_time'], reward['few']),
    ctrl.Rule(distance['long'] & traffic['high'] & punctuality['late'], reward['few']),
    ctrl.Rule(distance['medium'] & weather['moderate'] & rating['good'], reward['medium'])
]
grab_control_system = ctrl.ControlSystem(rules)


import tkinter as tk
root = tk.Tk()
root.geometry("300x400")
root.title("Hệ thống giá tiền Grab-bike")

tk.Label(root, text="Distance (0-50km)").pack()
distance_entry = tk.Entry(root)
distance_entry.pack()

tk.Label(root, text="Traffic (0-100%)").pack()
traffic_entry = tk.Entry(root)
traffic_entry.pack()

tk.Label(root, text="Demand (0-100%)").pack()
demand_entry = tk.Entry(root)
demand_entry.pack()

tk.Label(root, text="Weather").pack()
weather_var = tk.IntVar()
tk.Radiobutton(root, text="Clear weather", variable=weather_var, value=2).pack()
tk.Radiobutton(root, text="Light rain", variable=weather_var, value=5).pack()
tk.Radiobutton(root, text="Heavy rain", variable=weather_var, value=9).pack()

tk.Label(root, text="Rating (1-5)").pack()
rating_entry = tk.Entry(root)
rating_entry.pack()

tk.Label(root, text="Punctuality (0-100%)").pack()
punctuality_entry = tk.Entry(root)
punctuality_entry.pack()

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

def calculate():
    grab_simulation = ctrl.ControlSystemSimulation(grab_control_system)
    grab_simulation.input['distance'] = float(distance_entry.get())
    grab_simulation.input['traffic'] = float(traffic_entry.get())
    grab_simulation.input['demand'] = float(demand_entry.get())
    grab_simulation.input['weather'] = weather_var.get()
    grab_simulation.input['rating'] = float(rating_entry.get())
    grab_simulation.input['punctuality'] = float(punctuality_entry.get())
    grab_simulation.compute()
    result_label.config(
        text=f"Price: {grab_simulation.output['price']:.2f}\nReward: {grab_simulation.output['reward']:.2f}"
    )

tk.Button(root, text="Calculate", command=calculate).pack(pady=10)
root.mainloop()