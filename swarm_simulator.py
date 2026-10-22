import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- CONFIGURATION & ENVIRONMENT ---
NUM_BOIDS = 40          # Number of "cyber-birds" in the swarm
TARGET_NODE = np.array([50.0, 50.0])  # The enterprise infrastructure target
FIREWALL_RADIUS = 15.0  # Static defense boundary around the target

class CyberBoid:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)
        # Random initial velocity vector
        self.velocity = (np.random.rand(2) - 0.5) * 4.0
        self.max_speed = 3.0
        self.max_force = 0.2

    def update(self):
        # Limit speed to maintain realistic swarm physics
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed
        self.position += self.velocity

    def apply_behaviors(self, boids, target):
        """
        Applies Craig Reynolds' classic 3 rules of flocking behavior, 
        plus a specialized AI target attraction vector.
        """
        sep = self.separate(boids) * 1.5
        ali = self.align(boids) * 1.0
        coh = self.cohere(boids) * 1.0
        att = self.attract_to_target(target) * 2.0  # Hitchcock attraction force

        # Emergent velocity calculation
        self.velocity += sep + ali + coh + att

    def separate(self, boids):
        # Rule 1: Separation (Avoid crowding local swarm-mates)
        steering = np.zeros(2)
        desired_separation = 4.0
        count = 0
        for other in boids:
            d = np.linalg.norm(self.position - other.position)
            if (d > 0) and (d < desired_separation):
                diff = self.position - other.position
                diff /= d  # Weight by distance
                steering += diff
                count += 1
        if count > 0:
            steering /= count
        return steering

    def align(self, boids):
        # Rule 2: Alignment (Steer towards the average heading of neighbors)
        steering = np.zeros(2)
        neighbor_dist = 10.0
        count = 0
        for other in boids:
            d = np.linalg.norm(self.position - other.position)
            if (d > 0) and (d < neighbor_dist):
                steering += other.velocity
                count += 1
        if count > 0:
            steering /= count
            steering -= self.velocity
        return steering

    def cohere(self, boids):
        # Rule 3: Cohesion (Steer to move toward the average center of mass)
        steering = np.zeros(2)
        neighbor_dist = 10.0
        count = 0
        for other in boids:
            d = np.linalg.norm(self.position - other.position)
            if (d > 0) and (d < neighbor_dist):
                steering += other.position
                count += 1
        if count > 0:
            steering /= count
            desired = steering - self.position
            steering = desired - self.velocity
        return steering

    def attract_to_target(self, target):
        # Specialized rule: Swarm payload targeting critical infrastructure
        desired = target - self.position
        d = np.linalg.norm(desired)
        if d > 0:
            desired = (desired / d) * self.max_speed
            steering = desired - self.velocity
            return steering
        return np.zeros(2)

# --- INITIALIZATION ---
boids = [CyberBoid(np.random.rand() * 20.0, np.random.rand() * 20.0) for _ in range(NUM_BOIDS)]

# Setup the visualization canvas
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_title("Hack The Lore: Hitchcock AI Swarm Attack Simulation", fontsize=14, color='white')
fig.patch.set_facecolor('#121212')
ax.set_facecolor('#1e1e1e')

# Draw the target system and static firewall boundary
target_dot, = ax.plot(TARGET_NODE[0], TARGET_NODE[1], 'ro', markersize=12, label="Critical Infrastructure")
firewall_circle = plt.Circle(TARGET_NODE, FIREWALL_RADIUS, color='orange', fill=False, linestyle='--', label="Static Firewall")
ax.add_artist(firewall_circle)
boid_scatter = ax.scatter([], [], color='#00ffcc', s=15, label="Autonomous AI Malware Nodes")
ax.legend(loc="upper left")

def animate(frame):
    positions_x = []
    positions_y = []
    for boid in boids:
        boid.apply_behaviors(boids, TARGET_NODE)
        boid.update()
        
        # Check for edge wrapping/boundaries
        boid.position = np.clip(boid.position, 0, 100)
        
        positions_x.append(boid.position[0])
        positions_y.append(boid.position[1])
        
    boid_scatter.set_offsets(np.c_[positions_x, positions_y])
    return boid_scatter,

ani = FuncAnimation(fig, animate, frames=200, interval=50, blit=True)
plt.show()
