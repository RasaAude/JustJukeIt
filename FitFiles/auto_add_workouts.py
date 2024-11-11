import drive_api
from workout_database import WorkoutDatabase

def main():

    # Get the Drive service
    service = drive_api.get_drive_service()
    
    # Initialize your workout database
    db = WorkoutDatabase()  # Make sure this is properly initialized
    
    # Update the workout database
    drive_api.update_workout_database(service, db)

if __name__ == '__main__':
    main()

