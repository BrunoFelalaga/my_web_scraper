import requests
import pandas as pd
from requests_html import HTML
import os
import datetime 
import sys


BASE_DIR = os.path.dirname(__file__)

url = "https://www.boxofficemojo.com/year/world/"

def parse_and_extract(url, name = "2023"):

    # get html text from url
    html_text = url_to_txt(url)

    # Check if the provided year doesn't exist yet in the HTML content
    if html_text == None: # where year entered doesnt exist yet
        return False
    
    # Parse the HTML content using requests-html library
    r_html = HTML(html=html_text) # using requests html to parse

    # CSS class for the table
    table_class = ".imdb-scroll-table"
    # table_class = "a-section imdb-scroll-table mojo-gutter imdb-scroll-table-styles"
    # mojo-gutter imdb-scroll-table-styles"


    # Retrieve the table based on the provided CSS class
    r_table = r_html.find(table_class)

    table_data = []
    header_names = []

    # Check for the existence of a single table
    if len(r_table) != 1:
        return False

    # Parse the table for its rows and header columns
    parsed_table = r_table[0]
    rows = parsed_table.find("tr") # search rows 
    header_row = rows[0]
    header_cols = header_row.find("th")
    header_names = [x.text for x in header_cols]


    # Extract data from each row of the table
    for row in rows[1:]:
        
        cols = row.find("td")
        row_data = []
        for i, col in enumerate(cols):
            # print(i, col.text, "\n\n")
            row_data.append(col.text)
        
        table_data.append(row_data)
    
    # Create a CSV file with the extracted data
    pathname = os.path.join(BASE_DIR, "data")
    os.makedirs(pathname, exist_ok=True)
    filepath = os.path.join("data", f"{name}.csv")
    df = pd.DataFrame(table_data, columns=header_names)
    df.to_csv(filepath, index=False)
    
    return True 
        
    
# grab html to local machine 
def url_to_txt(url, filename = "world.html"):

    r = requests.get(url)

    # Check if the request was successful (status code 200)
    if r.status_code == 200:

        html_text = r.text

        # Write the HTML content to a file with the given filename
        with open(filename, "w") as file:
            file.write(html_text)
        
        return html_text
    
    return None


def run(start_year = None, years_ago = 3):

    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year

    # Check if start_year and years_ago are of the correct type and format
    assert isinstance(years_ago, int)
    assert isinstance(start_year, int)
    assert len(f"{start_year}") == 4 

    # Loop through each year within the range of years_ago
    for i in range(0, years_ago+1):

        url = f"https://www.boxofficemojo.com/year/world/{start_year}/"
        finished = parse_and_extract(url,name=start_year )
        
        if finished: # T/F

            print(f"Finished {start_year}")
        else:
            print(f"{start_year} not found")

        start_year -= 1

    return 

if __name__ == "__main__":

    # url = "https://www.boxofficemojo.com/year/world/"
    # start, count = sys.argv[1], sys.argv[2]
    try:
        start_yr = int(sys.argv[1])
    except:
        start_yr = None
    
    try:
        years_back = int(sys.argv[2])
    
    except:
        years_back = 0 # just cur year

    
    run(start_year=start_yr, years_ago=years_back)