import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table

def Practical_6():
    # Initialize parameters
    state_size = 5
    action_size = 2
    Q_table = np.zeros((state_size, action_size))
    
    # Hyperparameters
    alpha = 0.1  # Learning rate
    gamma = 0.9  # Discount factor
    
    # Example transition
    state = 2
    action = 1
    reward = 10
    next_state = 3
    
    print("Initial Q-table:")
    print(Q_table)
    print("\nUpdating Q-table for:")
    print(f"State: {state}, Action: {action}, Reward: {reward}, Next State: {next_state}\n")
    
    # Q-learning update
    old_value = Q_table[state, action]
    Q_table[state, action] = old_value + alpha * (reward + gamma * np.max(Q_table[next_state]) - old_value)
    
    print("Updated Q-table:")
    print(Q_table)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_axis_off()
    
    # Create table
    tb = Table(ax, bbox=[0, 0, 1, 1])
    
    # Add cells
    width, height = 1.0 / (action_size + 1), 1.0 / (state_size + 1)
    
    # Add headers
    tb.add_cell(0, 0, width, height, text="State", loc='center')
    for a in range(action_size):
        tb.add_cell(0, a+1, width, height, text=f"Action {a}", loc='center')
    
    # Add Q-values
    for s in range(state_size):
        tb.add_cell(s+1, 0, width, height, text=f"State {s}", loc='center')
        for a in range(action_size):
            value = Q_table[s, a]
            color = 'lightgreen' if s == state and a == action else 'white'
            tb.add_cell(s+1, a+1, width, height, text=f"{value:.2f}", 
                       loc='center', facecolor=color)
    
    ax.add_table(tb)
    
    # Add title and explanation
    plt.suptitle("Q-table After Update", y=0.85)
    plt.figtext(0.5, 0.7, 
                f"Updated cell (State {state}, Action {action}) highlighted in green\n"
                f"Old value: {old_value:.2f} → New value: {Q_table[state, action]:.2f}",
                ha='center')
    
    plt.show()
    
    # Print learning details
    print("\nLearning Details:")
    print(f"Learning rate (alpha): {alpha}")
    print(f"Discount factor (gamma): {gamma}")
    print(f"Update rule: Q(s,a) = Q(s,a) + α * (r + γ * max_a' Q(s',a') - Q(s,a))")

# Call the function with:
# Practical_6()