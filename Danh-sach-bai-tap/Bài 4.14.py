import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

order_density = ctrl.Antecedent(np.arange(0, 101, 1), 'order_density')            
delivery_urgency = ctrl.Antecedent(np.arange(0, 101, 1), 'delivery_urgency')      
driver_load = ctrl.Antecedent(np.arange(0, 101, 1), 'driver_load')             
traffic_conditions = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_conditions')   
profit_per_delivery = ctrl.Antecedent(np.arange(0, 101, 1), 'profit_per_delivery') 
orders_to_combine = ctrl.Consequent(np.arange(0, 11, 1), 'orders_to_combine')      
delivery_priority = ctrl.Consequent(np.arange(0, 101, 1), 'delivery_priority')

order_density['low'] = fuzz.trimf(order_density.universe, [0, 0, 45])
order_density['medium'] = fuzz.trimf(order_density.universe, [35, 50, 65])
order_density['high'] = fuzz.trimf(order_density.universe, [55, 75, 100])

delivery_urgency['low'] = fuzz.trimf(delivery_urgency.universe, [0, 0, 45])
delivery_urgency['medium'] = fuzz.trimf(delivery_urgency.universe, [35, 50, 65])
delivery_urgency['high'] = fuzz.trimf(delivery_urgency.universe, [55, 75, 100])

driver_load['low'] = fuzz.trimf(driver_load.universe, [0, 0, 45])
driver_load['medium'] = fuzz.trimf(driver_load.universe, [35, 50, 65])
driver_load['high'] = fuzz.trimf(driver_load.universe, [55, 75, 100])

traffic_conditions['low'] = fuzz.trimf(traffic_conditions.universe, [0, 0, 45])
traffic_conditions['medium'] = fuzz.trimf(traffic_conditions.universe, [35, 50, 65])
traffic_conditions['high'] = fuzz.trimf(traffic_conditions.universe, [55, 75, 100])

profit_per_delivery['low'] = fuzz.trimf(profit_per_delivery.universe, [0, 0, 45])
profit_per_delivery['medium'] = fuzz.trimf(profit_per_delivery.universe, [35, 50, 65])
profit_per_delivery['high'] = fuzz.trimf(profit_per_delivery.universe, [55, 75, 100])

orders_to_combine['few'] = fuzz.trimf(orders_to_combine.universe, [0, 0, 4])      
orders_to_combine['some'] = fuzz.trimf(orders_to_combine.universe, [3, 5, 7])       
orders_to_combine['many'] = fuzz.trimf(orders_to_combine.universe, [6, 8, 10])  

delivery_priority['low'] = fuzz.trimf(delivery_priority.universe, [0, 0, 45])
delivery_priority['medium'] = fuzz.trimf(delivery_priority.universe, [35, 50, 65])
delivery_priority['high'] = fuzz.trimf(delivery_priority.universe, [55, 75, 100])

rules = [
    ctrl.Rule(order_density['high'] & driver_load['low'] & traffic_conditions['low'], orders_to_combine['many']),
    ctrl.Rule(order_density['medium'] & traffic_conditions['high'] & delivery_urgency['medium'], orders_to_combine['some']),
    ctrl.Rule(driver_load['high'] & order_density['high'] & profit_per_delivery['medium'], orders_to_combine['some']),
    ctrl.Rule(order_density['low'] & delivery_urgency['high'] & traffic_conditions['medium'], orders_to_combine['some']),
    ctrl.Rule(profit_per_delivery['high'] & delivery_urgency['high'] & traffic_conditions['high'], orders_to_combine['some']),
    ctrl.Rule(delivery_urgency['high'] & profit_per_delivery['high'], delivery_priority['high']),
    ctrl.Rule(delivery_urgency['medium'] & traffic_conditions['medium'], delivery_priority['medium']),
    ctrl.Rule(delivery_urgency['low'] & order_density['high'] & profit_per_delivery['low'], delivery_priority['low']),
    ctrl.Rule(order_density['high'] & driver_load['low'], orders_to_combine['many']),
    ctrl.Rule(order_density['medium'] & driver_load['low'], orders_to_combine['some']),
    ctrl.Rule(delivery_urgency['medium'], delivery_priority['medium']),
    ctrl.Rule(delivery_urgency['high'], delivery_priority['high']),
    ctrl.Rule(traffic_conditions['high'], delivery_priority['high'])
]
logistics_ctrl = ctrl.ControlSystem(rules)


import tkinter as tk

root = tk.Tk()
root.title("Tối ưu hóa kế hoạch giao hàng cho tài xế")
root.geometry("400x300")

tk.Label(root, text="Order Density").grid(row=0, column=0)
order_density_var = tk.IntVar(value=80)
tk.Radiobutton(root, text="Low", variable=order_density_var, value=20).grid(row=0, column=1)
tk.Radiobutton(root, text="Medium", variable=order_density_var, value=50).grid(row=0, column=2)
tk.Radiobutton(root, text="High", variable=order_density_var, value=80).grid(row=0, column=3)

tk.Label(root, text="Delivery Urgency").grid(row=1, column=0)
delivery_urgency_var = tk.IntVar(value=50)
tk.Radiobutton(root, text="Low", variable=delivery_urgency_var, value=20).grid(row=1, column=1)
tk.Radiobutton(root, text="Medium", variable=delivery_urgency_var, value=50).grid(row=1, column=2)
tk.Radiobutton(root, text="High", variable=delivery_urgency_var, value=80).grid(row=1, column=3)

tk.Label(root, text="Driver's Current Load").grid(row=2, column=0)
driver_load_var = tk.IntVar(value=20)
tk.Radiobutton(root, text="Low", variable=driver_load_var, value=20).grid(row=2, column=1)
tk.Radiobutton(root, text="Medium", variable=driver_load_var, value=50).grid(row=2, column=2)
tk.Radiobutton(root, text="High", variable=driver_load_var, value=80).grid(row=2, column=3)

tk.Label(root, text="Traffic Conditions").grid(row=3, column=0)
traffic_conditions_var = tk.IntVar(value=50)
tk.Radiobutton(root, text="Low", variable=traffic_conditions_var, value=20).grid(row=3, column=1)
tk.Radiobutton(root, text="Medium", variable=traffic_conditions_var, value=50).grid(row=3, column=2)
tk.Radiobutton(root, text="High", variable=traffic_conditions_var, value=80).grid(row=3, column=3)

tk.Label(root, text="Profit Per Delivery").grid(row=4, column=0)
profit_per_delivery_var = tk.IntVar(value=50)
tk.Radiobutton(root, text="Low", variable=profit_per_delivery_var, value=20).grid(row=4, column=1)
tk.Radiobutton(root, text="Medium", variable=profit_per_delivery_var, value=50).grid(row=4, column=2)
tk.Radiobutton(root, text="High", variable=profit_per_delivery_var, value=80).grid(row=4, column=3)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=4, pady=15)

def calculate():
    logistics_simulation = ctrl.ControlSystemSimulation(logistics_ctrl)
    logistics_simulation.input['order_density'] = order_density_var.get()
    logistics_simulation.input['delivery_urgency'] = delivery_urgency_var.get()
    logistics_simulation.input['driver_load'] = driver_load_var.get()
    logistics_simulation.input['traffic_conditions'] = traffic_conditions_var.get()
    logistics_simulation.input['profit_per_delivery'] = profit_per_delivery_var.get()
    logistics_simulation.compute()
    orders_value = logistics_simulation.output.get('orders_to_combine', 0)
    priority_value = logistics_simulation.output.get('delivery_priority', 0)

    if orders_value < 3: orders_level = "Few Orders"
    elif orders_value < 6: orders_level = "Some Orders"
    else: orders_level = "Many Orders"
    if priority_value < 35: priority_level = "Low Priority"
    elif priority_value < 65: priority_level = "Medium Priority"
    else: priority_level = "High Priority"
    result_label.config(
        text=
        f"Orders to Combine: {orders_value:.2f} ({orders_level})\n"
        f"Delivery Priority: {priority_value:.2f} ({priority_level})"
    )

tk.Button(root, text="Calculate", command=calculate).grid(row=6, column=0, columnspan=4, pady=10)
root.mainloop()