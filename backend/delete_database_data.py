from app import app, db  # Import the existing db instance from your Flask app

# Define the Entry model if it's not in a separate module
class Entry(db.Model):
    __tablename__ = 'entry'
    __table_args__ = {'extend_existing': True}  # Allow reuse of the existing table

    id = db.Column(db.Integer, primary_key=True)
    # Add other fields of the Entry model here, e.g., name, timestamp, etc.

# Function to delete entries from the database
def delete_entries(start_id, end_id):
    # Query to delete entries within the specified ID range
    entries_to_delete = Entry.query.filter(Entry.id >= start_id, Entry.id <= end_id).all()
    
    # Check if there are entries to delete
    if entries_to_delete:
        for entry in entries_to_delete:
            db.session.delete(entry)
        db.session.commit()  # Commit the changes to the database
        print(f"Deleted {len(entries_to_delete)} entries from ID {start_id} to {end_id}.")
    else:
        print("No entries found in the specified range.")

if __name__ == '__main__':
    # Set up the app context
    with app.app_context():
        delete_entries(10, 73)  # Call the function to delete entries