from bs4 import BeautifulSoup
from random import choice
import requests
import csv


def write_csv(data):
    with open('stock_list.csv', 'a', newline='') as file:
        field_names = ['Название', 'Цена', 'Максимальная цена', 'Минимальная цена', 'Изменение',
                       'Время проверки', 'Ссылка']
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for i in range(len(data)):
            writer.writerow({'Название': data[i]['name'], 'Цена': data[i]['current price'],
                             'Максимальная цена': data[i]['max price'], 'Минимальная цена': data[i]['min price'],
                             'Изменение': data[i]['change'], 'Время проверки': data[i]['current_time'],
                             'Ссылка': data[i]['link']})


def get_html_stock(url, current_proxy):
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) '
                                'Gecko/20100101 Firefox/65.0'}
    response = requests.get(url, headers=user_agent, proxies=current_proxy).text
    return response


def get_stock_list(html_stock):
    url_stock ='https://ru.investing.com'
    soup = BeautifulSoup(html_stock, 'lxml')
    list = soup.find('tbody').find_all('tr')
    data = []
    for i in list:
        link = url_stock + i.find('a').get('href')
        name = i.find_all('td')[1].text
        price_max = i.find_all('td')[3].text
        price_min = i.find_all('td')[4].text
        price_cur = i.find_all('td')[2].text
        change = i.find_all('td')[5].text
        cur_time = i.find_all('td')[8].text
        dataRow = {'name': name, 'current price': price_cur, 'max price': price_max,
                     'min price': price_min, 'change': change, 'current_time': cur_time, 'link': link}
        data.append(dataRow)
    return data


def get_html(url):
    response = requests.get(url).text
    return response


def get_proxy_list(html):
    soup = BeautifulSoup(html, 'lxml')
    ip_table = soup.find('tbody').find_all('tr')
    proxy_list = []
    for i in ip_table:
        ip = i.find_all('td')
        if ip[6].text == 'no':
            proxy_list.append(ip[0].text + ':' + ip[1].text)
    return proxy_list


def main():
    url_proxy = 'https://free-proxy-list.net/'
    url_stock = 'https://ru.investing.com/equities'
    html = get_html(url_proxy)
    proxy_list = get_proxy_list(html)
    current_proxy = {'http': 'http://'+choice(proxy_list)}
    html_stock = get_html_stock(url_stock, current_proxy)
    data = get_stock_list(html_stock)
    with open('stock_list.csv', 'w+') as f:
        file = f.readline()
        print(file)
        if len(file) > 0:
            f.truncate()
    write_csv(data)


if __name__=="__main__":
    main()