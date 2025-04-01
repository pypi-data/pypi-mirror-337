import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def Practical_14():
    print("\n" + "="*50)
    print("AI IN ROBOTICS: PATH PLANNING SIMULATION")
    print("="*50 + "\n")
    
    # Enhanced Robot class with AI capabilities
    class Robot:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y
            self.path = [(x, y)]  # Track movement history
            self.sensors = {
                'front': 0,
                'left': 0,
                'right': 0
            }
            
        def move(self, dx, dy):
            """Move robot with basic collision avoidance"""
            new_x, new_y = self.x + dx, self.y + dy
            
            # Simple obstacle detection (simulated)
            if not self._detect_obstacle(new_x, new_y):
                self.x, self.y = new_x, new_y
                self.path.append((self.x, self.y))
                return True
            return False
            
        def _detect_obstacle(self, x, y):
            """Simulate sensor input (in real implementation would use sensor data)"""
            # Define some obstacle areas
            obstacles = [
                (2, 3), (2, 4), (3, 3), (3, 4),
                (5, 5), (5, 6), (6, 5), (6, 6)
            ]
            return (x, y) in obstacles
            
        def get_position(self):
            return self.x, self.y
            
        def sense_environment(self):
            """Simulate sensor readings"""
            self.sensors = {
                'front': np.random.uniform(0, 1),
                'left': np.random.uniform(0, 1),
                'right': np.random.uniform(0, 1)
            }
            return self.sensors
            
        def ai_decision(self):
            """Simple AI decision making"""
            sensors = self.sense_environment()
            
            # Basic obstacle avoidance logic
            if sensors['front'] < 0.3:
                if sensors['left'] > sensors['right']:
                    return self.move(0, 1)  # Move left
                else:
                    return self.move(0, -1)  # Move right
            else:
                return self.move(1, 0)  # Move forward

    # Initialize robot and environment
    robot = Robot()
    obstacles = [(2, 3), (2, 4), (3, 3), (3, 4), (5, 5), (5, 6), (6, 5), (6, 6)]
    target = (8, 8)
    
    print("Starting robotic simulation...")
    print(f"Initial Position: {robot.get_position()}")
    print(f"Target Position: {target}")
    
    # Simulate AI-powered movement
    steps = 20
    for _ in range(steps):
        if robot.get_position() == target:
            break
        robot.ai_decision()
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set up plot elements
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    ax.grid(True)
    ax.set_title('AI Robotics Simulation: Path Planning with Obstacle Avoidance')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    
    # Draw obstacles
    for obs in obstacles:
        ax.add_patch(plt.Rectangle(obs, 1, 1, color='red', alpha=0.5))
    
    # Draw target
    ax.add_patch(plt.Circle(target, 0.3, color='green', alpha=0.7))
    ax.text(target[0], target[1], 'Target', ha='center', va='center')
    
    # Initialize robot marker
    robot_marker, = ax.plot([], [], 'bo', markersize=12)
    path_line, = ax.plot([], [], 'b--', alpha=0.5)
    
    # Animation function
    def update(frame):
        if frame < len(robot.path):
            x, y = robot.path[frame]
            robot_marker.set_data(x, y)
            path_line.set_data([p[0] for p in robot.path[:frame+1]], 
                             [p[1] for p in robot.path[:frame+1]])
        return robot_marker, path_line
    
    # Create animation
    ani = FuncAnimation(fig, update, frames=len(robot.path)+5, 
                       interval=500, blit=True, repeat=False)
    
    plt.close()
    
    # Display results
    print("\nSimulation Results:")
    print(f"Final Position: {robot.get_position()}")
    print(f"Path Length: {len(robot.path)} steps")
    print(f"Obstacles Encountered: {sum(1 for pos in robot.path if pos in obstacles)}")
    
    print("\nKey AI Components Demonstrated:")
    print("- Sensor data processing")
    print("- Decision making under uncertainty")
    print("- Obstacle avoidance algorithms")
    print("- Path planning and optimization")
    
    return HTML(ani.to_jshtml())

# Call the function with:
# Practical_14()