from workout_database import WorkoutDatabase

# Create an instance of WorkoutDatabase
workout_db = WorkoutDatabase()
#Mrin, ravi, gokey, haboosh, alptug, finn, sub, williams,wilson
# Add workouts
workout_db.add_workout('al4574', '40_Min', '92365581.fit')
workout_db.add_workout('sja2180', '40_Min', '92365588.fit')
workout_db.add_workout('ona2107', '40_Min', '92365590.fit')
workout_db.add_workout('jrb2299', '40_Min', '92365582.fit')
workout_db.add_workout('ab5927', '40_Min', '92365580.fit')
workout_db.add_workout('ocb2111', '40_Min', '92365598.fit')
workout_db.add_workout('jpd2208', '40_Min', '92365631.fit')
workout_db.add_workout('suf2102', '40_Min', '92363511.fit')
workout_db.add_workout('ocg2108', '40_Min', '92365587.fit')
workout_db.add_workout('akj2147', '40_Min', '92365891.fit')
workout_db.add_workout('ehl2158', '40_Min', '92365860.fit')
workout_db.add_workout('ekm2164', '40_Min', '92365579.fit')
workout_db.add_workout('jem2349', '40_Min', '92424534.fit')
workout_db.add_workout('bip2106', '40_Min', '92365594.fit')
workout_db.add_workout('nsr2144', '40_Min', '92365595.fit')
workout_db.add_workout('dls2230', '40_Min', '92365585.fit')
workout_db.add_workout('bes2178', '40_Min', '92365593.fit')
workout_db.add_workout('spt2120', '40_Min', '92365583.fit')
workout_db.add_workout('av3099', '40_Min', '92366321.fit')
workout_db.add_workout('agw2135', '40_Min', '92365589.fit')
workout_db.add_workout('pjw2145', '40_Min', '92438271.fit')
workout_db.add_workout('jhw2175', '40_Min', '92365586.fit')


# You can add more workouts of the same type on different dates
# workout_db.add_workout('al4574', '40_Min', 'another_40_min_workout.fit')

# Retrieve workouts
#print(workout_db.get_workout('sja2180', '40_Min'))
#all_al4574_workouts = workout_db.get_all_workouts('al4574')

unis = [
    'al4574', 'sja2180', 'ona2107', 'jrb2299', 'ab5927', 'ocb2111', 'jpd2208',
    'suf2102', 'ocg2108', 'akj2147', 'ehl2158', 'ekm2164', 'jem2349', 'bip2106',
    'nsr2144', 'dls2230', 'bes2178', 'spt2120', 'av3099', 'agw2135', 'pjw2145', 'jhw2175'
]

# Loop through each code and print the workout
for uni in unis:
    print(f"Workout for {uni}:")
    print(workout_db.get_workout(uni, '40_Min'))
    print()  # Add a blank line for better readability

# List athletes and workouts
print(workout_db.list_workouts('al4574'))

dates = workout_db.get_workout_dates('al4574', '40_Min')
print("Dates for al4574's 40_Min workouts:", dates)

# Get a specific workout instance by date
if dates:
    specific_workout = workout_db.get_workout_by_date('al4574', '40_Min', dates[0])
    print(f"Workout data for al4574's 40_Min workout on {dates[0]}:")
    print(specific_workout)