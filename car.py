from refueling import Refueling


class Car:
    def __init__(self, tank_capacity: float, kilometers_per_liter: float, spent_money: float):
        self.tank_capacity = tank_capacity
        self.kilometers_per_liter = kilometers_per_liter
        self.spent_money = spent_money
        self.liters_per_tank_capacity = tank_capacity

    def fuel(self, refueling: Refueling):
        self.spent_money += (self.tank_capacity - self.liters_per_tank_capacity) * refueling.cost_in_liter + 20
        self.liters_per_tank_capacity = self.tank_capacity

    def drive_kilometres(self, km):
        self.liters_per_tank_capacity -= km / self.kilometers_per_liter

    def check_cost_fuel(self, ref: Refueling, km):
        return (self.tank_capacity - (
                    self.liters_per_tank_capacity - km / self.kilometers_per_liter)) * ref.cost_in_liter + 20

    def check_opportunity_to_get_there(self, km):
        return self.liters_per_tank_capacity - km / self.kilometers_per_liter >= 0

    def check_liters_per_tank_capacity(self, km):
        return self.liters_per_tank_capacity - km / self.kilometers_per_liter

    def check_drive_kilometres(self, km):
        return self.liters_per_tank_capacity * self.kilometers_per_liter >= km
