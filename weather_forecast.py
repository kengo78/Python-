#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests


city_name = 'Osaka'
app_id = '787a38a08af83e144b561c2ecaace7f5'
def get_weather():
    URL = "https://api.openweathermap.org/data/2.5/weather?q={0},jp&units=metric&lang=ja&appid={1}".format(city_name, app_id)
    response = requests.get(URL)
    data = response.json()
    weather = data["weather"][0]['description']
    max_temperature = data['main']['temp_max']
    min_temperature = data['main']['temp_min']
    diff_temp = max_temperature - min_temperature
    humidity = data['main']['humidity']
    context = {'天気':weather,'最高気温':str(max_temperature) + '度', '最低気温': str(min_temperature)+'度', "寒暖差": str(diff_temp) + "度", "湿度": str(humidity) + "%"}
    return context.items()

def send_line(msg):
    method = 'POSt'
    headers = {'Authorization','Bearer %s' % LINE_TOKEN}
    payload = {'message',msg}
    payload = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.parse.Request(
            url = LINE_NOTIFY_URL,data = payload,method = method,headers = headers)
    urllib.request.urlopen(req)
    
    
def main():
    weather_info_json = get_weather()
    for k,v in weather_info_json:
        print('{0}:{1}'.format(k,v))
    
if __name__ == '__main__':
    main()


# In[ ]:




