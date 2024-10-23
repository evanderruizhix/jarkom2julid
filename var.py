import csv
ipp = "10.10.11.49"
password = "koplak"
username = ["Fav"]

# Function to read existing usernames from a CSV file
def read_usernames(file_name):
    usernames = []
    try:
        with open(file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            usernames = [row[0] for row in reader]  # Assuming usernames are in the first column
    except FileNotFoundError:
        # If the file doesn't exist, we just return an empty list
        print(f"{file_name} not found, starting with an empty list.")
    return usernames

# Function to write new username to the CSV file
def write_username(file_name, new_username):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_username])  # Writing the new username to the file

def delete_username(file_name, username):
    usernames = read_usernames(file_name)
    usernames = [user for user in usernames if user != username]  # Exclude the username
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for user in usernames:
            writer.writerow([user]) 