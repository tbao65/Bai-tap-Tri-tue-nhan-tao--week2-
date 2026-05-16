import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

rating = ctrl.Antecedent(np.arange(1.0, 5.1, 0.1), 'rating')                
sales = ctrl.Antecedent(np.arange(0, 101, 1), 'sales')         
profit = ctrl.Antecedent(np.arange(0, 101, 1), 'profit')       
seasonal_event = ctrl.Antecedent(np.arange(0, 101, 1), 'seasonal_event')  
competitor_discount = ctrl.Antecedent(np.arange(0, 101, 1), 'competitor_discount') 
discount = ctrl.Consequent(np.arange(0, 71, 1), 'discount')              

rating['low'] = fuzz.trimf(rating.universe, [1.0, 1.0, 4.0])
rating['medium'] = fuzz.trimf(rating.universe, [4.0, 4.25, 4.5])
rating['high'] = fuzz.trimf(rating.universe, [4.5, 4.7, 5.0])

sales['low'] = fuzz.trimf(sales.universe, [0, 0, 40])
sales['medium'] = fuzz.trimf(sales.universe, [30, 50, 70])
sales['high'] = fuzz.trimf(sales.universe, [60, 80, 100])

profit['low'] = fuzz.trimf(profit.universe, [0, 0, 40])
profit['medium'] = fuzz.trimf(profit.universe, [30, 50, 70])
profit['high'] = fuzz.trimf(profit.universe, [60, 80, 100])

competitor_discount['low'] = fuzz.trimf(competitor_discount.universe, [0, 0, 40])
competitor_discount['medium'] = fuzz.trimf(competitor_discount.universe, [30, 50, 70])
competitor_discount['high'] = fuzz.trimf(competitor_discount.universe, [60, 80, 100])

seasonal_event['none'] = fuzz.trimf(seasonal_event.universe, [0, 0, 35])
seasonal_event['medium'] = fuzz.trimf(seasonal_event.universe, [25, 50, 75])
seasonal_event['high'] = fuzz.trimf(seasonal_event.universe, [65, 85, 100])

discount['very_low'] = fuzz.trimf(discount.universe, [0, 2.5, 5])        
discount['low'] = fuzz.trimf(discount.universe, [5, 7.5, 10])          
discount['medium'] = fuzz.trimf(discount.universe, [10, 15, 20])        
discount['high'] = fuzz.trimf(discount.universe, [20, 30, 40])          
discount['very_high'] = fuzz.trimf(discount.universe, [40, 55, 70])  

rules = [
    ctrl.Rule(rating['high'] & sales['high'] & profit['high'], discount['very_low']),
    ctrl.Rule(rating['low'] & sales['low'] & profit['high'], discount['high']),
    ctrl.Rule(seasonal_event['high'] & competitor_discount['high'], discount['very_high']),
    ctrl.Rule(rating['medium'] & sales['medium'] & profit['medium'], discount['medium']),
    ctrl.Rule(competitor_discount['low'] & profit['low'] & sales['high'], discount['very_low']),
    ctrl.Rule(rating['low'] & seasonal_event['none'], discount['medium']),
    ctrl.Rule(sales['low'] & profit['low'], discount['very_high'])
]
shopee_control_system = ctrl.ControlSystem(rules)


import tkinter as tk

root = tk.Tk()
root.title("Hệ thống tính toán chiết khấu cho Shopee")
root.geometry("550x300")

tk.Label(root, text="Rating (1.0 - 5.0)").grid(row=0, column=0)
rating_entry = tk.Entry(root)
rating_entry.insert(0, "4.3")
rating_entry.grid(row=0, column=1)

tk.Label(root, text="Sales").grid(row=1, column=0)
sales_var = tk.IntVar(value=50)
tk.Radiobutton(root, text="Low", variable=sales_var, value=10).grid(row=1, column=1)
tk.Radiobutton(root, text="Medium", variable=sales_var, value=50).grid(row=1, column=2)
tk.Radiobutton(root, text="High", variable=sales_var, value=80).grid(row=1, column=3)

tk.Label(root, text="Profit").grid(row=2, column=0)
profit_var = tk.IntVar(value=10)
tk.Radiobutton(root, text="Low", variable=profit_var, value=10).grid(row=2, column=1)
tk.Radiobutton(root, text="Medium", variable=profit_var, value=50).grid(row=2, column=2)
tk.Radiobutton(root, text="High", variable=profit_var, value=80).grid(row=2, column=3)

tk.Label(root, text="Seasonal Event").grid(row=3, column=0)
seasonal_var = tk.IntVar(value=80)
tk.Radiobutton(root, text="None", variable=seasonal_var, value=10).grid(row=3, column=1)
tk.Radiobutton(root, text="Moderate", variable=seasonal_var, value=50).grid(row=3, column=2)
tk.Radiobutton(root, text="High", variable=seasonal_var, value=80).grid(row=3, column=3)

tk.Label(root, text="Competitor Discount").grid(row=4, column=0)
competitor_discount_var = tk.IntVar(value=80)
tk.Radiobutton(root, text="Low", variable=competitor_discount_var, value=10).grid(row=4, column=1)
tk.Radiobutton(root, text="Medium", variable=competitor_discount_var, value=50).grid(row=4, column=2)
tk.Radiobutton(root, text="High", variable=competitor_discount_var, value=80).grid(row=4, column=3)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=4, pady=15)

def calculate():
    shopee_simulation = ctrl.ControlSystemSimulation(shopee_control_system)    
    shopee_simulation.input['rating'] = float(rating_entry.get())
    shopee_simulation.input['sales'] = float(sales_var.get())
    shopee_simulation.input['profit'] = float(profit_var.get())
    shopee_simulation.input['seasonal_event'] = seasonal_var.get()
    shopee_simulation.input['competitor_discount'] = float(competitor_discount_var.get())
    shopee_simulation.compute()
    discount_value = shopee_simulation.output.get('discount', 0)
    result_label.config(
        text=f"Suggested Discount: {discount_value:.2f}%"
    )

tk.Button(root, text="Calculate", command=calculate).grid(row=6, column=0, columnspan=4, pady=10)
root.mainloop()

             
