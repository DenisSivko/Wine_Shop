import argparse
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?',
                        default='wine', type=str)
    args = parser.parse_args()

    excel_data_df = pandas.read_excel(
        f'{args.file}.xlsx',
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )
    wines = excel_data_df.to_dict(orient='records')

    groups_wines = defaultdict(list)
    for wine in wines:
        groups_wines[wine['Категория']].append(wine)
    groups_wines = sorted(groups_wines.items())

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        assortment=groups_wines
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
