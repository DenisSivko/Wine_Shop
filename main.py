from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas as pd

excel_data_df = pd.read_excel('wine2.xlsx', na_values=['N/A', 'NA'],
                              keep_default_na=False)

data = excel_data_df.to_dict()
unique_category = []
minimal_category = []
minimal = max(data['Цена'].values())
minimal_price = min(data['Цена'].values())

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('templates/ListWine3.html')

if 'Категория' in data:
    template = env.get_template('templates/ListWine2.html')
    for i in range(len(data['Категория'])):
        if data['Категория'][i] not in unique_category:
            unique_category.append(data['Категория'][i])
    for category in unique_category:
        for i in range(len(data['Цена'])):
            if data['Категория'][i] == category:
                if data['Цена'][i] <= minimal:
                    minimal = data['Цена'][i]
        minimal_category.append(minimal)
        minimal = max(data['Цена'].values())

rendered_page = template.render(
    data=data,
    unique_category=unique_category,
    minimal_price=minimal_price,
    minimal_category=minimal_category,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
