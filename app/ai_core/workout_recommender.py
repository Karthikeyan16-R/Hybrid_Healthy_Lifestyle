import pandas as pd
import random

class WorkoutRecommender:

    def __init__(self, path="/mnt/data/exercises.csv"):
        self.df = pd.read_csv(path)
        self.df['secondaryMuscles'] = self.df[[c for c in self.df.columns if "secondaryMuscles" in c]].values.tolist()

    # SPLIT SELECTOR
    def get_split(self, days):
        if days == 3:
            return ["full_body"] * 3
        if days == 4:
            return ["upper", "lower", "upper", "lower"]
        if days == 5:
            return ["push", "pull", "legs", "upper", "full_body"]
        if days == 6:
            return ["push", "pull", "legs", "push", "pull", "legs"]
        return ["full_body"]

    # SET-REP logic
    def set_rep_scheme(self, level, goal):
        if level == "beginner":
            return 3, "10-12"
        if level == "intermediate":
            return 4, "8-12"
        return 5, "6-10"

    # SELECT EXERCISES FROM DATASET
    def get_exercises(self, split, count):
        df = self.df.copy()

        if split == "push":
            df = df[df['target'].isin(["chest","shoulders","triceps"])]
        elif split == "pull":
            df = df[df['target'].isin(["back","biceps"])]
        elif split == "legs":
            df = df[df['target'].isin(["quads","hamstrings","glutes","calves"])]
        elif split == "upper":
            df = df[df['bodyPart'].isin(["chest","back","shoulders","arms"])]
        elif split == "lower":
            df = df[df['bodyPart'].isin(["upper legs","lower legs"])]
        else:
            df = df  # full body = entire dataset

        return df.sample(count).to_dict(orient="records")

    # MAIN WORKOUT BUILDER
    def build_workout(self, user):
        days = user["days_per_week"]
        split = self.get_split(days)
        daily_count = 6 if user["daily_workout_time"] >= 40 else 4

        sets, reps = self.set_rep_scheme(user["activity_level"], user["goal"])

        plan = []

        for i, day_type in enumerate(split):
            exercises = self.get_exercises(day_type, daily_count)
            for ex in exercises:
                ex["sets"] = sets
                ex["reps"] = reps

            plan.append({
                "day": i + 1,
                "split_type": day_type,
                "exercises": exercises
            })

        return {
            "goal": user["goal"],
            "days": days,
            "plan": plan
        }
