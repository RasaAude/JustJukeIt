from workout_database import WorkoutDatabase


db = WorkoutDatabase()
workout_counts = db.count_workout_files()

for athlete_id, counts in workout_counts.items():
    print(f"Athlete {athlete_id}:")
    for workout_type, count in counts.items():
        print(f"  {workout_type}: {count} file(s)")