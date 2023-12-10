import requests
import pandas as pd
from requests_html import HTML
import os
import datetime 
import sys

BASE_DIR = os.path.dirname(__file__)

url = "https://www.boxofficemojo.com/year/world/"

def parse_and_extract(url, name = "2023"):

    html_text = url_to_txt(url)

    if html_text == None: # where year entered doesnt exist yet
        return False
    # print(html_text)

    r_html = HTML(html=html_text)
    # table_class = "a-section imdb-scroll-table mojo-gutter imdb-scroll-table-styles"
    table_class = ".imdb-scroll-table" 
    # mojo-gutter imdb-scroll-table-styles"

    r_table = r_html.find(table_class)

    table_data = []
    header_names = []
    if len(r_table) != 1:
        return False

    # print(r_table[0].text)
    parsed_table = r_table[0]
    rows = parsed_table.find("tr")
    # print(rows)
    header_row = rows[0]
    header_cols = header_row.find("th")
    header_names = [x.text for x in header_cols]
    # table_data = []
    for row in rows[1:]:
        # print(row.text)
        cols = row.find("td")
        row_data = []
        for i, col in enumerate(cols):
            # print(i, col.text, "\n\n")
            row_data.append(col.text)
        
        table_data.append(row_data)
    

    pathname = os.path.join(BASE_DIR, "data")
    os.makedirs(pathname, exist_ok=True)
    filepath = os.path.join("data", f"{name}.csv")
    df = pd.DataFrame(table_data, columns=header_names)
    df.to_csv(filepath, index=False)
    
    return True 
        
    
    
    

    

    return

# grab html to local machine 
def url_to_txt(url, filename = "world.html"):

    r = requests.get(url)

    if r.status_code == 200:

        html_text = r.text
        with open(filename, "w") as file:
            file.write(html_text)
        
        return html_text
    
    return None


def run(start_year = None, years_ago = 3):

    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year

    assert isinstance(years_ago, int)
    assert isinstance(start_year, int)
    assert len(f"{start_year}") == 4 

    
    

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

    # print(start, count)
    run(start_year=start_yr, years_ago=years_back)