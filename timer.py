import os
import sqlite3
import datetime
import time
import argparse

def clear_screen():
    os.system('cls') # Clear the screen to make it look nice? idk. Why not.

def format_time_amount(amount, unit): # Formatting time to only include non-zero values.
    if amount == 0:
        return ''
    elif amount == 1:
        return f"{amount} {unit}"
    else:
        return f"{amount} {unit}s"

def create_table(): # Create the Tasks table if it doesn't exist already.
    try:
        conn = sqlite3.connect('list.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Name TEXT,
                            Description TEXT,
                            Due TEXT,
                            Complete BOOL
                        )''')
        
        # Create the Completed_Tasks table if it doesn't exist yet (probably not).
        cursor.execute('''CREATE TABLE IF NOT EXISTS Completed_Tasks (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Name TEXT,
                            Description TEXT,
                            Due TEXT,
                            Complete BOOL
                        )''')
        conn.commit()
    except sqlite3.Error as e:
        print("Error creating table:", e)
    finally:
        conn.close()

def start_timer(task_id, due_datetime): # Start the timer for the given task.
    while True:
        clear_screen() # Clear the screen
        current_datetime = datetime.datetime.now()
        time_left = due_datetime - current_datetime
        days = time_left.days # Convert time to formatted time from above like the format_time_amount function.
        years, remainder = divmod(days, 365)
        months, days = divmod(remainder, 30)
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_left_str = ', '.join(
            filter(None, [ # Only include non-zero values, also fixes grammar from 1 years to 1 year and so on.
                format_time_amount(years, 'year'),
                format_time_amount(months, 'month'),
                format_time_amount(days, 'day'),
                format_time_amount(hours, 'hour'),
                format_time_amount(minutes, 'minute'),
                format_time_amount(seconds, 'second')
            ])
        )

        if time_left.total_seconds() <= 0:  # Check every second to see if any tasks are expired.
            move_to_completed(task_id)  # Move task to Completed_Tasks table

            try:
                conn = sqlite3.connect('list.db')
                cursor = conn.cursor()

                # Update Complete column to True for the task being moved in Tasks table
                cursor.execute('''UPDATE Tasks SET Complete = ? WHERE ID = ?''', (True, task_id))

                # Update Complete column to True for the task being moved in Completed_Tasks table
                cursor.execute('''UPDATE Completed_Tasks SET Complete = ? WHERE ID = ?''', (True, task_id))

                conn.commit()
            except sqlite3.Error as e:
                print("Error updating Complete column:", e)
            finally:
                conn.close()

            break

        print(f"Time left for task {task_id}: {time_left_str}") # Actually print the time left.
        time.sleep(1) # Wait 1 second before printing again.

def move_to_completed(task_id):
    try:
        conn = sqlite3.connect('list.db')
        cursor = conn.cursor()

        # Get task details
        cursor.execute('''SELECT * FROM Tasks WHERE ID = ?''', (task_id,))
        task_details = cursor.fetchone()

        # Move task to Completed_Tasks table with Complete value of True
        cursor.execute('''INSERT INTO Completed_Tasks (Name, Description, Due, Complete)
                          VALUES (?, ?, ?, ?)''', (task_details[1], task_details[2], task_details[3], True))
        conn.commit()

        # Delete task from Tasks table
        cursor.execute('''DELETE FROM Tasks WHERE ID = ?''', (task_id,))
        conn.commit()

        print(f"Task {task_id} has expired and moved to added to your Completed Tasks.")
    except sqlite3.Error as e:
        print("Error moving task to Completed_Tasks:", e)
    finally:
        conn.close()
        
def list_tasks(cursor):
    cursor.execute('''SELECT ID, Name, Description, Due FROM Tasks WHERE NOT Complete''')
    tasks = cursor.fetchall() # Get all tasks from db.

    print("Tasks:")
    for task in tasks: # Print all task details for user to choose from in case they forgot.
        task_id, name, description, due_date = task
        print(f"{task_id}. Name: {name}, Description: {description}, Due: {due_date}")

def select_task(): # Allow user to choose which task they want to worry about.
    task_id = input("Enter the ID of the task you want to start the timer for: ")
    return int(task_id.strip())

def main():
    try:
        conn = sqlite3.connect('list.db')
        cursor = conn.cursor()

        create_table() # Function from above to create table if it doesn't exist yet.

        cursor.execute('''SELECT COUNT(*) FROM Tasks WHERE NOT Complete''')
        num_tasks = cursor.fetchone()[0] # Count the number of tasks available to be timed.

        if num_tasks == 0: # Tell the user to create a task if there are none to time.
            print("There are no tasks in the list. Please create a task using the add_item.py script.")
            return

        list_tasks(cursor)
        selected_task = select_task() # Pass the user input into the script to start the timer.

        cursor.execute('''SELECT Due FROM Tasks WHERE ID = ?''', (selected_task,))
        due_date = cursor.fetchone()[0]
        due_datetime = datetime.datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        start_timer(selected_task, due_datetime)

        cursor.close()
        conn.close()

    except sqlite3.Error as e:
        print("Error starting timer:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start timer for a task")
    args = parser.parse_args()
    
    main() # Best way to start a script.