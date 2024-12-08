import http

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models


def main(request):
    template = 'main/index.html'
    items = catalog.models.Competition.objects.published()
    context = {
        'items': items,
    }
    return render(request, template, context)


def coffee(request):
    return HttpResponse('Я чайник', status=http.HTTPStatus.IM_A_TEAPOT)

def parse(request):
    import requests
    from bs4 import BeautifulSoup
    import datetime

    class RegionParser:  # парсер представителей регионов РФ
        def __init__(self):
            url = 'https://fsp-russia.com/region/regions/'
            self.json = dict()

            response = requests.get(url)

            soup = BeautifulSoup(response.text, 'lxml')
            accordion = soup.find('div', class_='accordion')
            region_blocks = accordion.find_all('div', class_='accordion-item')
            data = soup.find('div', class_='contacts_info').find_all('div', class_="contact_td")[1].find_all('p',
                                                                                                             class_='white_region')
            self.json['г. Москва'] = [{'region_name': data[0].text, 'director': data[1].text, 'email': data[2].text}]
            for block in region_blocks:
                key = block.find('h4').text
                self.json[key] = []
                regions = block.find_all('div', class_='contact_td')
                for region in regions:
                    data = region.find_all('p', class_='white_region')
                    self.json[key].append(
                        {'region_name': data[0].text, 'director': data[1].text, 'email': data[2].text})

    class CalendarParser:  # парсер календаря на ФСП
        def __init__(self, city=''):
            self.json = dict()

            for month in range(1, datetime.date.today().month + 1):
                year = datetime.date.today().year
                attr = f'?month={month}&year={year}&city={city}'
                url = f'https://fsp-russia.com/calendar/{attr}'

                response = requests.get(url)

                soup = BeautifulSoup(response.text, 'lxml')
                events = soup.find_all('div', class_='event-item-hover')
                for event in events:
                    date = event.find(class_='date').text.strip('\n')
                    try:
                        self.json[date]
                    except KeyError:
                        self.json[date] = []

                    location_block = event.find(class_='location')
                    location = None
                    if location_block:
                        location = location_block.text.strip('\n')

                    online_block = event.find(class_='online')
                    online = None
                    if online_block:
                        online = online_block.text.strip('\n')

                    arr = event.find_all(class_='info')
                    dis_par = [None, None]
                    if arr:
                        if len(arr) == 1:
                            dis_par[0] = arr[0].text.strip('\n')
                        elif len(arr) == 2:
                            dis_par[0] = arr[0].text.strip('\n')
                            dis_par[1] = arr[1].text.strip('\n')
                    self.json[date].append({'name': event.select('div.name')[0].text.strip('\n'),
                                            'online': online,
                                            'location': location,
                                            'discipline': dis_par[0],
                                            'participants': dis_par[1]
                                            })

    return HttpResponse('OK', status=http.HTTPStatus.OK)


__all__ = [
    'main',
    'coffee',
]
