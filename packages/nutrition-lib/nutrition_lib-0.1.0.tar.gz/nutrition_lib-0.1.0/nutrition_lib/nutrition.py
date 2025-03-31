from datetime import datetime

class NutritionTracker:
    def __init__(self):
        self.meal_log = []
        self.water_log = []
        self.weight_log = []

    def log_meal(self, food_name, calories, protein, carbs, fats):
        """Log a meal entry."""
        entry = {
            "food": food_name,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.meal_log.append(entry)
        return entry

    def log_water(self, amount_ml):
        """Log daily water intake."""
        entry = {"amount_ml": amount_ml, "date": datetime.now().strftime("%Y-%m-%d")}
        self.water_log.append(entry)
        return entry

    def log_weight(self, weight):
        """Log daily weight."""
        entry = {"weight": weight, "date": datetime.now().strftime("%Y-%m-%d")}
        self.weight_log.append(entry)
        return entry

    def get_meal_summary(self):
        """Summarize meal logs (calories breakdown)."""
        total_calories = sum(meal["calories"] for meal in self.meal_log)
        return {"total_meals": len(self.meal_log), "total_calories": total_calories}

    def get_water_summary(self):
        """Summarize water intake."""
        total_water = sum(entry["amount_ml"] for entry in self.water_log)
        return {"total_entries": len(self.water_log), "total_water_ml": total_water}

    def get_weight_progress(self):
        """Return weight logs sorted by date."""
        return sorted(self.weight_log, key=lambda x: x["date"], reverse=True)

# Example usage
if __name__ == "__main__":
    tracker = NutritionTracker()
    print(tracker.log_meal("Apple", 95, 0.5, 25, 0.3))
    print(tracker.log_water(500))
    print(tracker.log_weight(70))
