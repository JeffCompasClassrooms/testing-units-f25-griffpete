# Spaceship Navigation System
# Created by: Claude (Anthropic AI Assistant)
# A comprehensive navigation system for spaceship movement and positioning

import math
from typing import Tuple, List, Optional, Dict
from enum import Enum

class NavigationMode(Enum):
    MANUAL = "manual"
    AUTOPILOT = "autopilot"
    EMERGENCY = "emergency"

class SpaceshipNavigation:
    """
    A comprehensive spaceship navigation system that handles positioning,
    movement, fuel management, and navigation calculations in 3D space.
    """

    def __init__(self, initial_x: float = 0.0, initial_y: float = 0.0, initial_z: float = 0.0):
        # Position coordinates (in space units)
        self.x = float(initial_x)
        self.y = float(initial_y)
        self.z = float(initial_z)

        # Velocity components (units per time)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_z = 0.0

        # Navigation state
        self.fuel_level = 1000.0  # Starting fuel
        self.max_fuel = 1000.0
        self.fuel_consumption_rate = 1.0  # fuel per unit distance
        self.max_speed = 100.0  # maximum velocity in any direction

        # Navigation mode and status
        self.navigation_mode = NavigationMode.MANUAL
        self.is_engine_active = False
        self.navigation_locked = False

        # Waypoint system
        self.waypoints: List[Tuple[float, float, float]] = []
        self.current_waypoint_index = 0

        # Navigation history
        self.position_history: List[Tuple[float, float, float]] = [(self.x, self.y, self.z)]
        self.max_history_size = 100

    def get_position(self) -> Tuple[float, float, float]:
        """Return current position as (x, y, z) tuple."""
        return (self.x, self.y, self.z)

    def get_velocity(self) -> Tuple[float, float, float]:
        """Return current velocity as (vx, vy, vz) tuple."""
        return (self.velocity_x, self.velocity_y, self.velocity_z)

    def set_position(self, x: float, y: float, z: float) -> bool:
        """
        Set spaceship position directly.
        Returns False if navigation is locked.
        """
        if self.navigation_locked:
            return False

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self._add_to_history()
        return True

    def move(self, dx: float, dy: float, dz: float) -> bool:
        """
        Move spaceship by relative amounts.
        Returns False if insufficient fuel or navigation locked.
        """
        if self.navigation_locked:
            return False

        # Calculate distance
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        if distance == 0:
            return True

        # Check fuel
        fuel_needed = distance * self.fuel_consumption_rate
        if fuel_needed > self.fuel_level:
            return False

        # Update position
        self.x += dx
        self.y += dy
        self.z += dz

        # Consume fuel
        self.fuel_level -= fuel_needed
        self._add_to_history()

        return True

    def set_velocity(self, vx: float, vy: float, vz: float) -> bool:
        """
        Set velocity components.
        Returns False if any component exceeds max_speed or navigation locked.
        """
        if self.navigation_locked:
            return False

        # Check speed limits
        if abs(vx) > self.max_speed or abs(vy) > self.max_speed or abs(vz) > self.max_speed:
            return False

        self.velocity_x = float(vx)
        self.velocity_y = float(vy)
        self.velocity_z = float(vz)

        return True

    def accelerate(self, ax: float, ay: float, az: float, time_delta: float) -> bool:
        """
        Apply acceleration for given time period.
        Returns False if resulting velocity exceeds limits or insufficient fuel.
        """
        if self.navigation_locked or time_delta <= 0:
            return False

        # Calculate new velocity
        new_vx = self.velocity_x + ax * time_delta
        new_vy = self.velocity_y + ay * time_delta
        new_vz = self.velocity_z + az * time_delta

        # Check speed limits
        if abs(new_vx) > self.max_speed or abs(new_vy) > self.max_speed or abs(new_vz) > self.max_speed:
            return False

        # Calculate fuel for acceleration (acceleration requires more fuel)
        acceleration_magnitude = math.sqrt(ax*ax + ay*ay + az*az)
        fuel_needed = acceleration_magnitude * time_delta * 2.0  # 2x fuel rate for acceleration

        if fuel_needed > self.fuel_level:
            return False

        # Apply changes
        self.velocity_x = new_vx
        self.velocity_y = new_vy
        self.velocity_z = new_vz
        self.fuel_level -= fuel_needed

        return True

    def navigate_time_step(self, time_delta: float) -> bool:
        """
        Update position based on current velocity over time period.
        Returns False if navigation locked or insufficient fuel for movement.
        """
        if self.navigation_locked or time_delta <= 0:
            return False

        # Calculate movement
        dx = self.velocity_x * time_delta
        dy = self.velocity_y * time_delta
        dz = self.velocity_z * time_delta

        # Use move method which handles fuel consumption
        return self.move(dx, dy, dz)

    def calculate_distance_to(self, target_x: float, target_y: float, target_z: float) -> float:
        """Calculate distance to target coordinates."""
        dx = target_x - self.x
        dy = target_y - self.y
        dz = target_z - self.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def calculate_heading_to(self, target_x: float, target_y: float, target_z: float) -> Tuple[float, float]:
        """
        Calculate heading angles to target.
        Returns (azimuth, elevation) in radians.
        Azimuth: angle in XY plane from positive X axis
        Elevation: angle from XY plane toward Z axis
        """
        dx = target_x - self.x
        dy = target_y - self.y
        dz = target_z - self.z

        # Calculate azimuth (angle in XY plane)
        azimuth = math.atan2(dy, dx)

        # Calculate elevation (angle from XY plane to target)
        xy_distance = math.sqrt(dx*dx + dy*dy)
        if xy_distance == 0 and dz == 0:
            elevation = 0.0  # No movement needed
        else:
            elevation = math.atan2(dz, xy_distance)

        return (azimuth, elevation)

    def navigate_to_target(self, target_x: float, target_y: float, target_z: float,
                          max_speed: Optional[float] = None) -> bool:
        """
        Set velocity to move toward target at specified speed.
        Returns False if insufficient fuel or navigation locked.
        """
        if self.navigation_locked:
            return False

        # Calculate direction
        distance = self.calculate_distance_to(target_x, target_y, target_z)
        if distance == 0:
            return self.set_velocity(0, 0, 0)

        # Use provided max_speed or default
        speed = max_speed if max_speed is not None else self.max_speed
        speed = min(speed, self.max_speed)  # Don't exceed ship's max speed

        # Calculate unit direction vector
        dx = target_x - self.x
        dy = target_y - self.y
        dz = target_z - self.z

        # Normalize and scale by speed
        vx = (dx / distance) * speed
        vy = (dy / distance) * speed
        vz = (dz / distance) * speed

        return self.set_velocity(vx, vy, vz)

    def add_waypoint(self, x: float, y: float, z: float) -> bool:
        """Add waypoint to navigation route."""
        if self.navigation_locked:
            return False

        self.waypoints.append((float(x), float(y), float(z)))
        return True

    def clear_waypoints(self) -> bool:
        """Clear all waypoints."""
        if self.navigation_locked:
            return False

        self.waypoints.clear()
        self.current_waypoint_index = 0
        return True

    def get_next_waypoint(self) -> Optional[Tuple[float, float, float]]:
        """Get next waypoint in route, or None if no waypoints remain."""
        if self.current_waypoint_index >= len(self.waypoints):
            return None
        return self.waypoints[self.current_waypoint_index]

    def advance_to_next_waypoint(self) -> bool:
        """
        Advance to next waypoint in route.
        Returns False if no more waypoints or navigation locked.
        """
        if self.navigation_locked:
            return False

        if self.current_waypoint_index >= len(self.waypoints):
            return False

        self.current_waypoint_index += 1
        return True

    def navigate_waypoint_route(self, waypoint_threshold: float = 5.0) -> bool:
        """
        Navigate to next waypoint, auto-advancing when close enough.
        Returns False if no waypoints or navigation locked.
        """
        next_waypoint = self.get_next_waypoint()
        if next_waypoint is None:
            return False

        target_x, target_y, target_z = next_waypoint
        distance = self.calculate_distance_to(target_x, target_y, target_z)

        # If close enough to waypoint, advance to next
        if distance <= waypoint_threshold:
            return self.advance_to_next_waypoint()

        # Navigate toward current waypoint
        return self.navigate_to_target(target_x, target_y, target_z)

    def refuel(self, fuel_amount: float) -> float:
        """
        Add fuel to spaceship.
        Returns actual amount of fuel added (limited by tank capacity).
        """
        if fuel_amount <= 0:
            return 0.0

        available_capacity = self.max_fuel - self.fuel_level
        actual_fuel_added = min(fuel_amount, available_capacity)
        self.fuel_level += actual_fuel_added

        return actual_fuel_added

    def get_fuel_percentage(self) -> float:
        """Return fuel level as percentage of maximum."""
        return (self.fuel_level / self.max_fuel) * 100.0

    def estimate_fuel_for_distance(self, distance: float) -> float:
        """Estimate fuel needed to travel given distance."""
        return distance * self.fuel_consumption_rate

    def can_reach_target(self, target_x: float, target_y: float, target_z: float) -> bool:
        """Check if spaceship has enough fuel to reach target."""
        distance = self.calculate_distance_to(target_x, target_y, target_z)
        fuel_needed = self.estimate_fuel_for_distance(distance)
        return fuel_needed <= self.fuel_level

    def set_navigation_mode(self, mode: NavigationMode) -> bool:
        """Set navigation mode."""
        if self.navigation_locked and mode != NavigationMode.EMERGENCY:
            return False

        self.navigation_mode = mode
        return True

    def lock_navigation(self, locked: bool) -> bool:
        """
        Lock or unlock navigation controls.
        Can always unlock, but locking requires manual mode.
        """
        if locked and self.navigation_mode != NavigationMode.MANUAL:
            return False

        self.navigation_locked = locked
        return True

    def emergency_stop(self) -> bool:
        """Emergency stop - set velocity to zero and enter emergency mode."""
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_z = 0.0
        self.navigation_mode = NavigationMode.EMERGENCY
        self.navigation_locked = False  # Emergency mode overrides lock
        return True

    def get_navigation_status(self) -> Dict:
        """Get comprehensive navigation status."""
        return {
            'position': self.get_position(),
            'velocity': self.get_velocity(),
            'fuel_level': self.fuel_level,
            'fuel_percentage': self.get_fuel_percentage(),
            'navigation_mode': self.navigation_mode.value,
            'navigation_locked': self.navigation_locked,
            'is_engine_active': self.is_engine_active,
            'waypoints_remaining': len(self.waypoints) - self.current_waypoint_index,
            'total_distance_traveled': len(self.position_history)
        }

    def _add_to_history(self):
        """Add current position to history, maintaining size limit."""
        self.position_history.append((self.x, self.y, self.z))
        if len(self.position_history) > self.max_history_size:
            self.position_history.pop(0)
