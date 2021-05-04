from os import makedirs
from datetime import datetime, timedelta

import bs4
import requests
import cv2
from pony.orm import db_session
from models import Forecast


class WeatherMaker:

    def __init__(self, f_date):
        self.today_url = 'https://weather.com/ru-RU/weather/today/l/59.89,30.26'
        self.future_url = 'https://weather.com/ru-RU/weather/tenday/l/' \
                          '298feb763c42fafce0010cacb7672aec664e07112eb867199ef62b6d42024376'
        self.past_url = 'https://api.weather.com/v1/location/ULLI:9:RU/observations/historical.json?' \
                        'apiKey=6532d6454b8aa370768e63d6ba5a832e&units=e&startDate='
        self.f_date = f_date
        self.current_date = datetime.now()
        self.json_data = None
        self.past_data, self.future_data = [], []

    def today_parsing(self):
        html = requests.get(url=self.today_url).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        list_of_names = soup.find_all('div', {'class': 'WeatherDetailsListItem--label--3JSSI'})
        list_of_values = soup.find_all('div', {'class': 'WeatherDetailsListItem--wxData--23DP5'})
        forecast = soup.find_all('div', {'class': 'CurrentConditions--precipValue--RBVJT'})[0].text
        weather_data = {}
        for name, value in zip(list_of_names, list_of_values):
            weather_data[name.text] = value.text
        today_weather = {
            'дата': self.current_date.strftime('%d.%m.%Y'),
            'время': 'на сегодня',
            'температура': soup.find_all('span', {'class': 'TodayDetailsCard--feelsLikeTempValue--2aogo'})[0].text,
            'погода': soup.find_all('div', {'class': 'CurrentConditions--phraseValue--2xXSr'})[0].text,
            'ветер': weather_data['Ветер'][-7:],
            'влажность': weather_data['Влажность'],
            'давление': weather_data['Давление'][10:],
            'проноз': f'{str(forecast[:-11]) + str(forecast[-10:])}',
        }
        return today_weather

    def future_parsing(self):
        # прогноз составляется максимум на 14 дней
        html = requests.get(url=self.future_url).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        list_date = [datetime.strftime(self.current_date + timedelta(day), '%d.%m.%Y') for day in range(14)]
        list_weather = soup.find_all('span', {'class': 'DetailsSummary--extendedData--aaFeV'})
        list_high_temp = soup.find_all('span', {'class': 'DetailsSummary--highTempValue--3x6cL'})
        list_low_temp = soup.find_all('span', {'class': 'DetailsSummary--lowTempValue--1DlJK'})
        list_humidity = soup.find_all('div', {'class': 'DetailsSummary--precip--2ARnx'})
        list_wind = soup.find_all('span', {'class': 'Wind--windWrapper--1Va1P undefined'})
        list_data = zip(list_date, list_weather, list_high_temp, list_low_temp, list_wind, list_humidity)
        for date_out, weather_out, high_temp, low_temp, wind, humidity in list_data:
            if datetime.strptime(date_out, '%d.%m.%Y') == self.f_date:
                weather = {
                    'дата': date_out,
                    'время': '00:00',
                    'погода': weather_out.text,
                    'температура': f'{high_temp.text[:-1]}C/{low_temp.text[:-1]}C',
                    'ветер': wind.text,
                    'влажность': humidity.text[4:],
                    'давление': 'нет данных',
                    'прогноз': weather_out.text
                }
                self.future_data.append(weather)
        return self.future_data

    def get_url(self):
        date = datetime.strptime(self.f_date, "%d.%m.%Y")
        year, month, day = date.strftime('%Y.%m.%d').split('.')
        url = f'{self.past_url}{year}{month}{day}'
        return url

    def past_parsing(self):
        header = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json, text/plain, */*'
        }
        url = self.get_url()
        html = requests.get(url, headers=header).json()
        date = f'{url[-2:]}.{url[-4:-2]}.{url[-8:-4]}'
        c_time = datetime.strptime('00:00', '%H:%M')
        for data in html['observations']:
            weather = {
                'дата': date,
                'время': str(c_time.strftime('%H:%M')),
                'температура': f"{data['temp']}F",
                'погода': data['wx_phrase'],
                'давление': f"{data['pressure']} in",
                'влажность': f"{data['rh']}%",
                'ветер': f"{data['wdir_cardinal']} {data['wc']} mph",
                'прогноз': 'нет данных'
            }
            self.past_data.append(weather)
            c_time += timedelta(minutes=30)
        return self.past_data


class ImageMaker:

    def __init__(self, data):
        self.data = data
        self.image_cv2 = cv2.imread('Files/probe.jpg')
        self.weather_intents = {
            'snow': 'снег',
            'cloud': 'облачно',
            'smoke': 'облачно',
            'wintry': 'дожд',
            'rain': 'дожд',
            'drizzle': 'дожд',
            'fair': 'солнечно',
            'fog': 'туман',
            'mist': 'туман',
            'thunder': 'дожд',
            't - storm': 'дожд',
        }
        self.weather_path = {
            'облачно': 'cloud.jpg',
            'дожд': 'rain.jpg',
            'снег': 'snow.jpg',
            'солнечно': 'sun.jpg',
            'туман': 'fog.jpg',
            'молния': 'thunder.png'
        }
        self.path = 'Files/weather_img/'

    def viewImage(self, image, name_of_window='postcard'):
        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.imshow(name_of_window, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_path_draw(self):
        inc_text = self.data['погода'].lower()
        for item, value in self.weather_intents.items():
            if item in inc_text:
                return self.path + f'{self.weather_path[self.weather_intents[item]]}', self.weather_intents[item]
            elif value in inc_text:
                return self.path + self.weather_path[value], value

    def draw_postcard(self):
        path, color_path = self.get_path_draw()
        inc_weather = cv2.imread(path)
        postcard = self.image_cv2.copy()
        h = postcard.shape[0]
        x, y, c = 0, 30, 0
        for _ in range(128):
            colors = {
                'дожд': (255, c, c),
                'снег': (255, 128 + c, 128 + c),
                'солнечно': (c, 255, 255),
                'облачно': (128 + c, 128 + c, 128 + c),
                'туман': (128 + c, 128 + c, 128 + c)
            }
            color = colors[color_path]
            cv2.line(postcard, (x, 0), (x, h), color, 4)
            c += 2
            x += 4
        for item, value in self.data.items():
            cv2.putText(postcard, f'{item}: {value}', (20, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)
            y += 20

        rows, cols, channels = inc_weather.shape
        roi = postcard[0:rows, 0:cols]
        img2gray = cv2.cvtColor(inc_weather, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        img2_fg = cv2.bitwise_and(inc_weather, inc_weather, mask=mask)
        dst = cv2.add(img1_bg, img2_fg)
        postcard[0:100, 400:500] = dst
        return postcard

    def save_postcard(self):
        postcard = self.draw_postcard()
        filename = f"{self.data['дата']}.{self.data['время'].split(':')[0]}.{self.data['время'].split(':')[1]}"
        makedirs('postcards', exist_ok=True)
        cv2.imwrite(f'postcards/{filename}.jpg', postcard)


class DatabaseUpdater:

    def __init__(self):
        self.db = Forecast

    @db_session
    def write_data(self, data):
        for weather in data:
            Forecast(
                date=weather['дата'],
                time=weather['время'],
                temperature=weather['температура'],
                weather=weather['погода'],
                pressure=weather['давление'],
                humidity=weather['влажность'],
                wind=weather['ветер'],
                forecast=weather['прогноз']
            )

    def get_data(self, date):
        forecast = []
        w_date = datetime.strptime(date, "%d.%m.%Y")
        weather = self.db.select(Forecast).where(Forecast.date == datetime.strftime(w_date, "%d.%m.%Y")).get()
        forecast.append({
            'дата': weather.date,
            'время': weather.time,
            'температура': weather.temperature,
            'погода': weather.weather,
            'давление': weather.pressure,
            'влажность': weather.humidity,
            'ветер': weather.wind,
            'прогноз': weather.forecast
        })
        return forecast


class Manager:

    def __init__(self, f_date):
        self.f_date = f_date
        self.curr_date = datetime.now()
        self.db_upd = DatabaseUpdater()

    def check_date(self):
        if len(str(self.f_date)) != 10:
            return ValueError('Введено неверное значение')
        try:
            self.f_date = datetime.strptime(self.f_date, "%d.%m.%Y")
        except ValueError:
            return ValueError(f'{self.f_date} не соответствует формату "день.месяц.год"')
        if self.f_date > (datetime.now() + timedelta(14)):
            return NameError(f'Прогноз доступен только на ближайшие 14 дней, введите другую дату')
        else:
            return False

    def parse_forecast(self):
        weather = WeatherMaker(self.f_date)
        if self.f_date <= datetime.now():
            return weather.past_parsing()
        else:
            return weather.future_parsing()

    def write_data_to_db(self, data):
        self.db_upd.write_data(data)

    def get_data_from_db(self, date):
        if date is not None:
            return self.db_upd.get_data(date)

    def make_postcards(self, data):
        for forecast in data:
            image = ImageMaker(forecast)
            image.save_postcard()
