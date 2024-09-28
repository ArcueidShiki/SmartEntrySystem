import requests

def store_data(temperature, label, image_path):
    url = 'http://127.0.0.1:5000/entry'
    data = {
        'temperature': temperature,
        'mask_status': label
    }
    files = {'image': ('captured_image.jpg', open(image_path, 'rb'))}

    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code == 201:
            print("Entry added successfully.")
        else:
            print(f"Failed to add entry: {response.text}")
    except Exception as e:
        print(f"Error in store_data: {e}")