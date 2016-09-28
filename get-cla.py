from bs4 import BeautifulSoup
import dateutil.parser
import requests

html = requests.get('https://www.oasis-open.org/resources/open-repositories/cla/view-individual').text

# with open("oasis.html", 'w') as f:
#     f.write(html)

# with open("oasis.html") as f:
#     html = f.read()

soup = BeautifulSoup(html, "html.parser")

form = soup.find(id='oasis-cla-individual-page')
table = form.div.table

rows = [x for x in table.tbody.children if hasattr(x, 'tag') and x.name == 'tr']

for row in rows:
    list_items = list(row.td.ul.find_all('li'))

    username_li = list(list_items[1].children)
    if len(username_li) > 1:
        username = username_li[1]
    else:
        username = ""

    # Strip off last part if username is a URL
    username = username.split(r'/')[-1]

    start_li = list(list_items[4].children)
    if len(start_li) > 1:
        start = start_li[1]
        start = dateutil.parser.parse(start).isoformat()
    else:
        start = "???"


    end_li = list(list_items[5].children)
    if len(end_li) > 1:
        end = end_li[1]
        end = dateutil.parser.parse(end).isoformat()
    else:
        end = "present"

    print("{} ({} - {})".format(username, start, end))
