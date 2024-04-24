import sqlite3
import argparse

# Example arguents: --name "Submit this assignment" --description "Finish this project and submit the GitHub URL" --due "2024-04-24 00:00:00"

def create_table(): # Create the list.db file and create the Tasks table if it doesn't exist yet.
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
        conn.commit()
    except sqlite3.Error as e:
        print("Error creating table:", e)
    finally:
        conn.close()

def check_duplicate_task(name, description): # Function to include regex, for checking if there are duplicate names or descriptions.
    try:
        conn = sqlite3.connect('list.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Tasks WHERE Name = ? OR Description = ?''', (name, description))
        existing_tasks = cursor.fetchone()
        if existing_tasks:
            return existing_tasks
        else:
            return None
    except sqlite3.Error as e:
        print("Error checking for duplicate task:", e)
    finally:
        conn.close()

def add_item(name, description, due): # Function for adding items to the Tasks table.
    try:
        conn = sqlite3.connect('list.db')
        cursor = conn.cursor()
        
        # Check for duplicate task
        duplicate_task = check_duplicate_task(name, description) # call the check_duplicate_tasks function to tell the user.
        if duplicate_task:
            print("A task with the same name or description already exists:")
            print(f"Name: {duplicate_task[1]}, Description: {duplicate_task[2]}")
            rename = input("Do you want to rename the task? (yes/no): ")
            if rename.lower() == 'yes': # Ask the user if they want to continue or remake the task with a new name or description.
                new_name = input("Enter the new name: ")
                new_description = input("Enter the new description: ")
                cursor.execute('''UPDATE Tasks SET Name = ?, Description = ? WHERE ID = ?''',
                               (new_name, new_description, duplicate_task[0]))
                conn.commit()
                print("Task renamed successfully.") # :D
                return
            else:
                print("Task not added.") # D:
                return
        
        cursor.execute('''INSERT INTO Tasks (Name, Description, Due, Complete)
                          VALUES (?, ?, ?, ?)''',
                       (name, description, due, False))
        conn.commit()
        print("Task added successfully.")
    except sqlite3.Error as e:
        print("Error adding task:", e)
    finally:
        conn.close()

if __name__ == "__main__": # Init for getting arguments from the user.
    parser = argparse.ArgumentParser(description="Add a task to the to-do list")
    parser.add_argument("--name", required=True, help="Name of the task")
    parser.add_argument("--description", required=True, help="Description of the task")
    parser.add_argument("--due", required=True, help="Due date and time (format: YYYY-MM-DD HH:MM:SS)")
    args = parser.parse_args()
    
    create_table() # Create table if not exists from above.
    add_item(args.name, args.description, args.due) # Add items from args to values to be stored in db.
