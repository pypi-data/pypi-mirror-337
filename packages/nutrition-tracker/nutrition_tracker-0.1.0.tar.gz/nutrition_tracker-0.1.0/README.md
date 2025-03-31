# Nutrition Tracker

A Python library for tracking nutrition, meal logs, water intake, and weight.

## Installation

```bash
pip install nutrition_tracker

from nutrition_tracker import NutritionTracker

tracker = NutritionTracker()
tracker.log_meal("Apple", 95, 0.5, 25, 0.3)
print(tracker.get_meal_summary())


