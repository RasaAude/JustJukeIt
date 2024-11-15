import drive_api
from workout_database import WorkoutDatabase
import os
import glob

def main():
    

    # Get the Drive service
    service = drive_api.get_drive_service()
    
    # Initialize your workout database
    db = WorkoutDatabase()  # Make sure this is properly initialized
    
    # Update the workout database
    drive_api.update_workout_database(service, db)
    # Clear .fit and .fit.gz files from the current directory
    clear_fit_files()

def clear_fit_files():
    # Get a list of all .fit and .fit.gz files in the current directory
    fit_files = glob.glob('*.fit') + glob.glob('*.fit.gz')
    
    # Remove each file
    for file in fit_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {str(e)}")

if __name__ == '__main__':
    main()

