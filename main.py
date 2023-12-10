import requests
import pandas as pd
from requests_html import HTML

url = "https://www.boxofficemojo.com/year/world/"

# grab html to local machine 
def url_to_txt(url, filename = "world.html"):

    r = requests.get(url)

    if r.status_code == 200:

        html_text = r.text
        with open(filename, "w") as file:
            file.write(html_text)
        
        return html_text
    
    return ""


if __name__ == "__main__":


    html_text = url_to_txt(url)
    # print(html_text)

    r_html = HTML(html=html_text)
    # table_class = "a-section imdb-scroll-table mojo-gutter imdb-scroll-table-styles"
    table_class = ".imdb-scroll-table" 
    # mojo-gutter imdb-scroll-table-styles"

    r_table = r_html.find(table_class)

    table_data = []
    header_names = []
    if len(r_table) == 1:

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
    
    print(header_names)
    # print(table_data)

    df = pd.DataFrame(table_data, columns=header_names)
    df.to_csv("movies.csv", index=False)

    
