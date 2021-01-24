import random
import requests
from get_wind_direction import get_wind_direction

# список фото из которых случайным образом будет выбираться одно
link_img = ['image0.jpg', 'image1.jpg', 'image2']
link_img = random.choice(link_img)

# appid нужно получить на https://home.openweathermap.org/users/sign_up
appid = "bcf8d1e32a6b7ffd72a5995f90c91012"
# id города список здесь: http://bulk.openweathermap.org/sample/city.list.json.gz
city_id = 554234

# получаем погоду
try:
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()

    x = data['main']['pressure'] * 0.75006375541921  # конверируем давление в мм р.с.
    deg = data['wind']['deg']  # получаем направление ветра в градусах

except Exception as e:
    print("Exception (weather):", e)
    pass

# функция определения направления ветра 
get_wind_direction(deg)

# формируем сообщение
msg = (f'''
    В Калининграде {data['weather'][0]['description']}
    Температура: {data['main']['temp']}°, ощущается как {round(data['main']['feels_like'])}°
    Ветер {get_wind_direction(deg)} {data['wind']['speed']} м.с
    Давление: {round(x)} мм р.с
    Влажность: {data['main']['humidity']}%
    Облачность: {data['clouds']['all']}%
    '''
       )

#Авторизация в ВК

# vk token
token = '3cce9a0b24e3f45g5656575757529b66d0c12589a40927bccb8bfbf556hrb5d7aeb28b613e'

g_id = '45566719'  # id сообщества или страницы
g_id_post = '-45566719' # этот же id с минусом
V = '5.103' # версия API

# запрос к серверу vk, чтобы получить ссылку на загрузку картинки
r = requests.get('https://api.vk.com/method/photos.getWallUploadServer',
                 params={'access_token': token, 'v': V, 'group_id': g_id})
data = r.json()

# загружаем фото
server = requests.post(data['response']['upload_url'], files={'photo': open(link_img, "rb")})
ser = server.json()

# сохраняем фото на сервере
load = requests.get('https://api.vk.com/method/photos.saveWallPhoto',
                    params={'access_token': token,
                            'v': V,
                            'group_id': g_id,
                            'server': ser['server'],
                            'photo': ser['photo'],
                            'hash': ser['hash']})

save = load.json()

# формирование имени фото
photo_id = (f'''photo{save['response'][0]['owner_id']}_{save['response'][0]['id']}''')


# отправка поста
post = requests.get('https://api.vk.com/method/wall.post',
                    params={'access_token': token, 'v': V, 'from_group': 1, 'owner_id': g_id_post, 'message': msg,
                            'attachments': photo_id})

print(post.content)
