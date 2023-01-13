# This class creates an interface to accept new job boards from an upstream service that locates boards of interest

import csv
import requests
from googlesearch import search

class BoardHandler:
    
    def __init__(self, board_file):
        # CSV file storing companies and job board links
        self.board_file = board_file
        
        # Dictionary will be synced on construction & destruction
        self.board_dict = {}
        self.load_board_dict()
        
    def __del__(self):
        print("DBHandler object destroyed, changed synced to board_file.")
        self.save_board_file()
        
    def find_board_url(self, employer: str) -> str:
        for url in search(employer+" careers", num_results=1):
            return url
        
    def __str__(self) -> str:
        s = ''
        for k, v in self.board_dict.items():
            s += (k+'\t'+v+'\n')
        return(s)
    
    def is_url_up(self, url: str) -> bool:
        # Returns if a URL is down or up
        try:
            # Make a GET request to the URL
            response = requests.get(url, timeout=5)
            print("Response status code is ", response.status_code)
            # If the GET request returns a status code between 200 and 399, the URL is up
            if 200 <= response.status_code < 400:
                print(f"{url} is up")
                return True
            else:
                print(f"{url} is down")
                return False
        except requests.exceptions.RequestException as e:
            print(e)
            print(f"{url} is down")
            return False

    def add_board(self, employer: str, url: str) -> bool:
        self.board_dict[employer] = url
            
    def delete_board(self, employer: str) -> bool:
        del self.board_dict[employer]
    
    def load_board_dict(self):
        # Open the file
        
        try:
            with open(self.board_file, newline='',encoding='utf-8') as csv_file:
                # Create a CSV reader object
                reader = csv.DictReader(csv_file)
                # Iterate over the rows
                for row in reader:
                    # Assign the first column as the key and the second column as the value
                    self.board_dict[row[reader.fieldnames[0]]] = row[reader.fieldnames[1]]
        except Exception:
            # Create a new empty csv file
            open(board_file, 'w')
                
    def save_board_file(self):
        # Write dictionary to database (ideally on the diff)
        
        # Open the file
        with open(self.board_file, 'w', newline='', encoding='utf-8') as csv_file:
            # Create a CSV writer object
            writer = csv.writer(csv_file)
            # Write the data
            for key, value in self.board_dict.items():
                writer.writerow([key, value])