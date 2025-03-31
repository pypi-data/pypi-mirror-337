# nutrition_lib/__init__.py
from .nutrition import get_nutrition, NutritionError
from .meals import Meal, log_meal, summarize_meals
from .water import WaterIntake, log_water, calculate_water_progress
from .weight import WeightLog, log_weight, summarize_weight
from .utilities import format_chart_data

__version__ = "0.1.0"



from .nutrition import NutritionTracker
