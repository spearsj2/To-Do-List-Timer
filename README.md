# To-Do-List-Timer (Python Final)

    The purpose of this repository is to use a mixture of Sqlite3, and Regex to create an active to-do list for keeping organized.
## Functions of the add_item.py script
    -h or --help - This allows users to ask for help from the script.
    --name [Clean kitchen] - This allows users to give their tasks a name.
    --description [Wash the dishes and take out the trash] - This allows the user to give their tasks a detailed description.
    --due [2024-04-24 00:00:00] - This allows the user to set a deadline for the timer.py script.

    The script also uses Regular Expression to check if any names or descriptions are the same and asks the user if they are sure they want to continue.

## Functions of the timer.py script
    *No arguments need to be passed into this script, only user inputs from within the script.*
    - The script tells the user the names, descriptions, and due dates of the tasks in the database.
    - Moves tasks with expired deadlines to the Completed_Tasks table, and removes them from the tasks table.
    - Tells the user if there are no active tasks that can be timed.

## Checklist

```md
- [x] This task is complete.
```

- [X] Argument -h command output.
- [X] Filled out the self-evaluation.
- [X] Filled out the self-reflection.

## Self-Evaluation

How many points out of 85 do you deserve on this assignment: `85`

I spent a lot of time testing this script, making it better, adding new features to make it look nicer and adding more functionality.

## Self-Reflection
<!-- What did you learn that you found interesting -->
I previously made a timer, so I used a lot of the same code from my previous project, but all I needed to change was the input of the deadline from the Sqlite3 db.
A lot of this project was just SQL code and making things look nice. I ran into a few issues but I sorted them out.

### How long it took you to finish this?
7 hours, give or take, and no, I didn't time myself making this timer. That would be silly.