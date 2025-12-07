import time

class TrafficLightController:
    def __init__(self, north, south, east, west):
        self.north = north
        self.south = south
        self.east = east
        self.west = west

        self.last_change = time.time()
        self.green_duration = 5
        self.yellow_duration = 2
        self.current_phase = "NS"  # North-South green, East-West red

        # Initialize lights
        self.north.change_color("green")
        self.south.change_color("green")
        self.east.change_color("red")
        self.west.change_color("red")

    def update(self):
        current_time = time.time()
        elapsed = current_time - self.last_change

        if self.current_phase == "NS":
            # North-South green
            if elapsed >= self.green_duration:
                self.north.change_color("yellow")
                self.south.change_color("yellow")
                self.current_phase = "NS_YELLOW"
                self.last_change = current_time

        elif self.current_phase == "NS_YELLOW":
            if elapsed >= self.yellow_duration:
                self.north.change_color("red")
                self.south.change_color("red")
                self.east.change_color("green")
                self.west.change_color("green")
                self.current_phase = "EW"
                self.last_change = current_time

        elif self.current_phase == "EW":
            # East-West green
            if elapsed >= self.green_duration:
                self.east.change_color("yellow")
                self.west.change_color("yellow")
                self.current_phase = "EW_YELLOW"
                self.last_change = current_time

        elif self.current_phase == "EW_YELLOW":
            if elapsed >= self.yellow_duration:
                self.east.change_color("red")
                self.west.change_color("red")
                self.north.change_color("green")
                self.south.change_color("green")
                self.current_phase = "NS"
                self.last_change = current_time