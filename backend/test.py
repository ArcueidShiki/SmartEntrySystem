import requests

url = 'http://127.0.0.1:5000/entry'
data = {
    'temperature': '36.6',
    'mask_status': 'true'
}
files = {'image': ('test_image.png', open('/Users/edward/Desktop/cits5506Iot/project/SmartEntrySystem/backend/static/images/image.jpeg', 'rb'))}

response = requests.post(url, data=data, files=files)
print(response.json())