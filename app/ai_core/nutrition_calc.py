def calculate_macros(age, weight, height, sex, activity, goal, target_change_kg=1.8):
    base_mult = {
        "sedentary": 25, "light": 28, "moderate": 32,
        "active": 36, "very_active": 40
    }.get(activity.lower(), 30)

    maintenance = base_mult * weight
    daily_adjust = (target_change_kg * 7700) / 30

    if goal == "weight_gain":
        calories = maintenance + daily_adjust
        p, c, f = 2.2, 4.5, 1.2
    elif goal == "weight_loss":
        calories = maintenance - daily_adjust
        p, c, f = 2.0, 2.5, 0.9
    else:
        calories = maintenance
        p, c, f = 1.8, 3.5, 1.0

    protein_g = weight * p
    carbs_g = weight * c
    fats_g = weight * f

    return {
        "goal": goal,
        "target_change_kg_month": round(target_change_kg, 2),
        "calories": round(calories, 2),
        "protein_g": round(protein_g, 2),
        "carbs_g": round(carbs_g, 2),
        "fats_g": round(fats_g, 2)
    }
