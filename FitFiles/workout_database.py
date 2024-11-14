import pandas as pd
import os
from fitparse import FitFile
import gzip
import shutil

class WorkoutDatabase:
    def __init__(self, database_dir='workout_database'):
        self.database_dir = database_dir
        self.workouts = {}
        self.load_database()

    def load_database(self):
        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)
        for athlete_id in os.listdir(self.database_dir):
            athlete_dir = os.path.join(self.database_dir, athlete_id)
            if os.path.isdir(athlete_dir):
                self.workouts[athlete_id] = {}
                for workout_file in os.listdir(athlete_dir):
                    if workout_file.endswith('.parquet'):
                        workout_type = workout_file[:-8]  # Remove '.parquet'
                        file_path = os.path.join(athlete_dir, workout_file)
                        self.workouts[athlete_id][workout_type] = pd.read_parquet(file_path)

    def save_workout(self, athlete_id, workout_type, df):
        athlete_dir = os.path.join(self.database_dir, athlete_id)
        if not os.path.exists(athlete_dir):
            os.makedirs(athlete_dir)
        file_path = os.path.join(athlete_dir, f"{workout_type}.parquet")
        df.to_parquet(file_path)

    def add_workout(self, athlete_id, workout_type, fit_file_path):
        
        if fit_file_path.endswith('.fit.gz'):
            # Create a temporary .fit file to store the unzipped contents
            temp_fit_path = fit_file_path.replace('.fit.gz', '.fit')
            
            # Unzip the .fit.gz file
            with gzip.open(fit_file_path, 'rb') as f_in:
                with open(temp_fit_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Use the temporary .fit file for processing
            fit_file_path = temp_fit_path        
        # Load and process the FIT file
        fitfile = FitFile(fit_file_path)
        records = []
        for record in fitfile.get_messages('record'):
            records.append(record.get_values())

        new_df = pd.DataFrame(records)
        new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
        new_df.set_index('timestamp', inplace=True)
        new_df['Athlete ID'] = athlete_id

        # Add the workout to the database
        if athlete_id not in self.workouts:
            self.workouts[athlete_id] = {}
        
        if workout_type in self.workouts[athlete_id]:
            # Append new workout data to existing dataframe
            combined_df = pd.concat([self.workouts[athlete_id][workout_type], new_df])
            # Remove duplicates based on index (timestamp) and all columns
            combined_df = combined_df.loc[~combined_df.index.duplicated(keep='first')]
            # Sort the combined dataframe by timestamp
            combined_df.sort_index(inplace=True)
            self.workouts[athlete_id][workout_type] = combined_df
        else:
            # Create new dataframe for this workout type
            self.workouts[athlete_id][workout_type] = new_df

        # Save the updated workout data to a Parquet file
        self.save_workout(athlete_id, workout_type, self.workouts[athlete_id][workout_type])

    def get_workout(self, athlete_id, workout_type):
        return self.workouts.get(athlete_id, {}).get(workout_type)

    def get_all_workouts(self, athlete_id):
        return self.workouts.get(athlete_id, {})

    def list_athletes(self):
        return list(self.workouts.keys())

    def list_workouts(self, athlete_id):
        return list(self.workouts.get(athlete_id, {}).keys())
    
    def get_workout_dates(self, athlete_id, workout_type):
        workout_df = self.get_workout(athlete_id, workout_type)
        if workout_df is not None:
            return sorted(set((date.year, date.month, date.day) for date in workout_df.index.date))
        return []

    def get_workout_by_date(self, athlete_id, workout_type, date):
        workout_df = self.get_workout(athlete_id, workout_type)
        if workout_df is not None:
            if isinstance(date, tuple) and len(date) == 3:
                year, month, day = date
                start_of_day = pd.Timestamp(year=year, month=month, day=day)
            else:
                start_of_day = pd.Timestamp(date)
            
            end_of_day = start_of_day + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
            return workout_df.loc[start_of_day:end_of_day]
        return None

