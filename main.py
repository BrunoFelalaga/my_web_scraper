import requests

url = "https://www.boxofficemojo.com/year/world/"

# grab html to local machine
def url_to_file(url, filename = "world.html"):

    r = requests.get(url)

    if r.status_code == 200:

        html_text = r.text
        with open(filename, "w") as file:
            file.write(html_text)
        
        return html_text
    
    return ""

url_to_file(url)

