import requests

def store_data(temperature, label, final_result, image_path):
    url = 'http://127.0.0.1:5000/entry'
    data = {
        'temperature': temperature,
        'mask_status': label,
        'final_result': final_result  # Ensure final_result is included
    }
    files = {'image': (image_path, open(image_path, 'rb'))}

    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code == 201:
            print("Entry added successfully.")
        else:
            print(f"Failed to add entry: {response.text}")
    except Exception as e:
        print(f"Error in store_data: {e}")

# Usage example
temperature = 35.5
mask_status = True  # Keep this as a boolean
final_result = True  # Keep this as a boolean
image_path = "static/images/captured_image.jpeg"

store_data(temperature, mask_status, final_result, image_path)