import requests
from bs4 import BeautifulSoup
import argparse

# выделяет домен сайта
def get_domain(url):
    tmp = url.split('//')
    domain = tmp[1].split('/')[0]
    return domain

# получает ссылки с сайта
def get_link(url):
    html = requests.get(url)
    if html.status_code != 200:
        return html.status_code
    bs = BeautifulSoup(html.text, 'html.parser')
    link_a = bs.find_all('a', href=True)
    return link_a


# парсит ссылки с сайта
def parse_link(url):
    tmp_urls = []
    link_a = get_link(url)
    if str(link_a).isdigit():
        print(f'Что-то пошло не так. Код ошибки: {link_a}')
    else:
        for i in link_a:
            if 'http' in i['href'] and i['href'].find('http') == 0:
                if get_domain(i['href']) != get_domain(url):
                    tmp_urls.append(i['href'])
                    link_b = get_link(i['href'])
                    for j in link_b:
                        if j['href'].find('http') == 0 and 'http' in j['href']:
                            if get_domain(j['href']) != get_domain(i['href']):
                                tmp_urls.append(j['href'])
    return tmp_urls

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Парсер ссылок на сайте.')
    parser.add_argument("-a", dest="url", default='https://xakep.ru/', type=str, help='Введите полный адрес сайта.')
    parser.add_argument('-o', dest="save", default="termninal", type=str, help='Для сохранение в файл используейте аргумент: file')
    args = parser.parse_args()
    urls = parse_link(args.url)
    if args.save == 'termninal':
        urls_set = set(urls)
        for i in urls_set:
            print(i)
    else:
        with open('urls.txt', 'w') as file:
            urls_set = set(urls)
            file.write('\n'.join(urls_set))
