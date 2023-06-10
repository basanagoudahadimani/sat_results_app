import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('sat_results.db')
c = conn.cursor()

# Create the SAT Results table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS sat_results
             (name TEXT PRIMARY KEY,
              address TEXT,
              city TEXT,
              country TEXT,
              pincode TEXT,
              sat_score INTEGER)''')

# Menu function to display options
def show_menu():
    print("SAT Results Application")
    print("1. Insert data")
    print("2. View all data")
    print("3. Get rank")
    print("4. Update score")
    print("5. Delete one record")
    print("0. Exit")

# Function to insert data
def insert_data():
    name = input("Enter name: ")
    address = input("Enter address: ")
    city = input("Enter city: ")
    country = input("Enter country: ")
    pincode = int(input("Enter pincode: "))
    sat_score = int(input("Enter SAT score: "))
    passed = "Pass" if sat_score > 30 else "Fail"
    
    c.execute("INSERT INTO sat_results VALUES (?, ?, ?, ?, ?, ?)",
              (name, address, city, country, pincode, sat_score))
    
    conn.commit()
    print("Data inserted successfully!")

# Function to view all data
def view_all_data():
    c.execute("SELECT * FROM sat_results")
    rows = c.fetchall()
    if rows:
        data = []
        for row in rows:
            record = {
                "name": row[0],
                "address": row[1],
                "city": row[2],
                "country": row[3],
                "pincode": row[4],
                "sat_score": row[5]
            }
            data.append(record)
        json_data = json.dumps(data, indent=4)
        print(json_data)
    else:
        print("No data available.")

# Function to get rank by name
def get_rank():
    name = input("Enter name: ")
    c.execute("SELECT COUNT(*) FROM sat_results WHERE sat_score > (SELECT sat_score FROM sat_results WHERE name = ?)", (name,))
    rank = c.fetchone()[0] + 1
    print(f"The rank of {name} is {rank}")

# Function to update score by name
def update_score():
    name = input("Enter name: ")
    sat_score = int(input("Enter new SAT score: "))
    passed = "Pass" if sat_score > 30 else "Fail"
    
    c.execute("UPDATE sat_results SET sat_score = ? WHERE name = ?", (sat_score, name))
    conn.commit()
    print("Score updated successfully!")

# Function to delete one record by name
def delete_record():
    name = input("Enter name: ")
    c.execute("DELETE FROM sat_results WHERE name = ?", (name,))
    conn.commit()
    print("Record deleted successfully!")

# Main application loop
while True:
    show_menu()
    choice = input("Enter your choice (0-5): ")

    if choice == '1':
        insert_data()
    elif choice == '2':
        view_all_data()
    elif choice == '3':
        get_rank()
    elif choice == '4':
        update_score()
    elif choice == '5':
        delete_record()
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")
   