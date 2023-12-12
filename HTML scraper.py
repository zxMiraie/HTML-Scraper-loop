from bs4 import BeautifulSoup
import csv

try:
    file_path = input("Please enter the file path: ")
    filein = open(file_path, 'r')
    print("working")
except IOError:
    print("Error: File not found or unable to read file.")
    exit()

try:
    soup = BeautifulSoup(filein, 'html.parser')
except Exception as e:
    print("Error: Unable to parse HTML.")
    print(str(e))
    exit()

user_data = []

# Define the ids and corresponding statuses
ids_statuses = {
    'panel-user-registered': 'ACTIVE',
    'panel-user-unregistered': 'INACTIVE',
    'panel-user-archived': 'ARCHIVED'
}

# Loop through the ids and statuses
for id, status in ids_statuses.items():
    # Find all divs with the current id
    divs = soup.find_all(id=id)
    for div in divs:
        
        username_div = div.find(class_='col-md-10 col-xs-10')
        if username_div:
            username = username_div.text.strip()
        
        data_user_div = div.find(class_='data-user')
        if data_user_div:
            name_b = data_user_div.find("b", class_='ng-binding')
            if name_b:
                name = name_b.text.strip()
            email = data_user_div.find(class_='ng-binding').text.strip()
            email_span = data_user_div.find("span", class_='trimValue')
            if email_span:
                email = email_span.text.strip()
        role_div = div.find(class_= "labels-user")
        roles = []
        if role_div:
            role_finder = role_div.find_all(class_="label ng-binding label-success")
            for role in role_finder:
                roles.append(role.text.strip())
            
        
        
        user_data.append([username, status, name, email, roles])

try:
    with open('output.csv', 'w', newline='') as fileout:
        writer = csv.writer(fileout)
        writer.writerow(['Username', 'Status', 'Name', 'Email', 'Role'])
        writer.writerows(user_data)
        print("Done")
except IOError:
    print("Error: Unable to write to file.")