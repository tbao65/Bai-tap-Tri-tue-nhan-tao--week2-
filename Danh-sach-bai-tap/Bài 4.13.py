import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

product_demand = ctrl.Antecedent(np.arange(0, 101, 1), 'product_demand')           
competitor_pressure = ctrl.Antecedent(np.arange(0, 101, 1), 'competitor_pressure') 
store_reputation = ctrl.Antecedent(np.arange(1.0, 5.1, 0.1), 'store_reputation')   
profit_margin = ctrl.Antecedent(np.arange(0, 101, 1), 'profit_margin')            
seasonal_demand = ctrl.Antecedent(np.arange(0, 101, 1), 'seasonal_demand')      
discount = ctrl.Consequent(np.arange(0, 71, 1), 'discount')                    

product_demand['low'] = fuzz.trimf(product_demand.universe, [0, 0, 40])
product_demand['medium'] = fuzz.trimf(product_demand.universe, [30, 50, 70])
product_demand['high'] = fuzz.trimf(product_demand.universe, [60, 80, 100])

competitor_pressure['low'] = fuzz.trimf(competitor_pressure.universe, [0, 0, 40])
competitor_pressure['medium'] = fuzz.trimf(competitor_pressure.universe, [30, 50, 70])
competitor_pressure['high'] = fuzz.trimf(competitor_pressure.universe, [60, 80, 100])

store_reputation['low'] = fuzz.trimf(store_reputation.universe, [1.0, 1.0, 4.0])
store_reputation['medium'] = fuzz.trimf(store_reputation.universe, [3.8, 4.25, 4.5])
store_reputation['high'] = fuzz.trimf(store_reputation.universe, [4.3, 4.6, 5.0])

profit_margin['low'] = fuzz.trimf(profit_margin.universe, [0, 0, 40])
profit_margin['medium'] = fuzz.trimf(profit_margin.universe, [30, 50, 70])
profit_margin['high'] = fuzz.trimf(profit_margin.universe, [60, 80, 100])

seasonal_demand['none'] = fuzz.trimf(seasonal_demand.universe, [0, 0, 35])
seasonal_demand['medium'] = fuzz.trimf(seasonal_demand.universe, [25, 50, 75])
seasonal_demand['high'] = fuzz.trimf(seasonal_demand.universe, [65, 85, 100])

discount['very_low'] = fuzz.trimf(discount.universe, [0, 2.5, 5])       
discount['low'] = fuzz.trimf(discount.universe, [5, 7.5, 10])       
discount['medium'] = fuzz.trimf(discount.universe, [10, 15, 20])         
discount['high'] = fuzz.trimf(discount.universe, [20, 30, 40])           
discount['very_high'] = fuzz.trimf(discount.universe, [40, 55, 70])  

rules = [
    ctrl.Rule(product_demand['high'] & competitor_pressure['low'] & profit_margin['low'], discount['very_low']),
    ctrl.Rule(product_demand['low'] & competitor_pressure['high'] & profit_margin['high'], discount['high']),
    ctrl.Rule(store_reputation['high'] & profit_margin['medium'] & seasonal_demand['high'], discount['medium']),
    ctrl.Rule(competitor_pressure['high'] & seasonal_demand['high'] & profit_margin['high'], discount['very_high']),
    ctrl.Rule(store_reputation['low'] & product_demand['medium'] & profit_margin['low'], discount['medium']),
    ctrl.Rule(product_demand['high'] & seasonal_demand['none'] & competitor_pressure['low'], discount['very_low']),
    ctrl.Rule(profit_margin['high'] & competitor_pressure['medium'] & seasonal_demand['medium'], discount['medium']),
    ctrl.Rule(product_demand['high'], discount['medium']),
    ctrl.Rule(competitor_pressure['high'], discount['high']),
    ctrl.Rule(seasonal_demand['high'], discount['high']),
    ctrl.Rule(store_reputation['medium'], discount['medium'])
]
shopee_ctrl = ctrl.ControlSystem(rules)


import tkinter as tk

root = tk.Tk()
root.title("Kế hoạch chiến lược bán hàng của Shopee")
root.geometry("500x300")

tk.Label(root, text="Product Demand").grid(row=0, column=0)
product_demand_var = tk.IntVar(value=80)
tk.Radiobutton(root, text="Low", variable=product_demand_var, value=20).grid(row=0, column=1)
tk.Radiobutton(root, text="Medium", variable=product_demand_var, value=50).grid(row=0, column=2)
tk.Radiobutton(root, text="High", variable=product_demand_var, value=80).grid(row=0, column=3)

tk.Label(root, text="Competitor Pressure").grid(row=1, column=0)
competitor_pressure_var = tk.IntVar(value=50)
tk.Radiobutton(root, text="Low", variable=competitor_pressure_var, value=20).grid(row=1, column=1)
tk.Radiobutton(root, text="Medium", variable=competitor_pressure_var, value=50).grid(row=1, column=2)
tk.Radiobutton(root, text="High", variable=competitor_pressure_var, value=80).grid(row=1, column=3)

tk.Label(root, text="Store Reputation (1.0 - 5.0)").grid(row=2, column=0)
reputation_entry = tk.Entry(root)
reputation_entry.insert(0, "4.2")
reputation_entry.grid(row=2, column=1)

tk.Label(root, text="Profit Margin").grid(row=3, column=0)
profit_margin_var = tk.IntVar(value=80)
tk.Radiobutton(root, text="Low", variable=profit_margin_var, value=20).grid(row=3, column=1)
tk.Radiobutton(root, text="Medium", variable=profit_margin_var, value=50).grid(row=3, column=2)
tk.Radiobutton(root, text="High", variable=profit_margin_var, value=80).grid(row=3, column=3)

tk.Label(root, text="Seasonal Demand").grid(row=4, column=0)
seasonal_demand_var = tk.IntVar(value=80)
tk.Radiobutton(root, text="None", variable=seasonal_demand_var, value=20).grid(row=4, column=1)
tk.Radiobutton(root, text="Medium", variable=seasonal_demand_var, value=50).grid(row=4, column=2)
tk.Radiobutton(root, text="High", variable=seasonal_demand_var, value=80).grid(row=4, column=3)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=4, pady=15)

def calculate():
    shopee_simulation = ctrl.ControlSystemSimulation(shopee_ctrl)
    shopee_simulation.input['product_demand'] = product_demand_var.get()
    shopee_simulation.input['competitor_pressure'] = competitor_pressure_var.get()
    shopee_simulation.input['store_reputation'] = float(reputation_entry.get())
    shopee_simulation.input['profit_margin'] = profit_margin_var.get()
    shopee_simulation.input['seasonal_demand'] = seasonal_demand_var.get()
    shopee_simulation.compute()
    discount_value = shopee_simulation.output.get('discount', 0)
    if discount_value < 7: level = "Very Low"
    elif discount_value < 15: level = "Low"
    elif discount_value < 25: level = "Medium"
    elif discount_value < 40: level = "High"
    else: level = "Very High"
    result_label.config(text=f"Suggested Discount: {discount_value:.2f}%, (Level of Discount: {level})")

tk.Button(root, text="Calculate", command=calculate).grid(row=6, column=0, columnspan=4, pady=10)
root.mainloop()