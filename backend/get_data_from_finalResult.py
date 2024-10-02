# import os
# from PIL import Image
# import pytesseract
# import requests

# # Set the path to the Tesseract executable if it's not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # Update this path as needed

# def extract_mask_status(image_path):
#     # Open the image using Pillow
#     image = Image.open(image_path)

#     # Use pytesseract to extract text from the image
#     extracted_text = pytesseract.image_to_string(image)

#     # Print the extracted text for verification
#     print("Extracted Text:")
#     print(extracted_text)

#     # Search for the mask_status and final_result in the extracted text
#     mask_status = None
#     final_result = None
#     for line in extracted_text.splitlines():
#         if "mask" in line.lower():  # Adjust this to match how mask status is formatted in your image
#             mask_status = line.strip()  # Store the found mask status
#             break
#     for line in extracted_text.splitlines():
#         if "Open" in line.lower():  # Adjust this to match how mask status is formatted in your image
#             final_result = line.strip()  # Store the found mask status
#             break

#     # Return the mask status if found, else return a default value
#     if mask_status == "Mask: No Mask":
#         return False
#     else:
#         return True
    
#     if final_result == "Final Result: Open the door":
#         return True
#     else:
#         return False

# def store_data(temperature, image_path):
#     # Call extract_mask_status to get the mask status
#     mask_status = extract_mask_status(image_path)
#     print(mask_status)
#     print(type(mask_status))
#     print(mask_status)
#     print(type(mask_status))
#     url = 'http://127.0.0.1:5000/entry'
#     data = {
#         'temperature': temperature,
#         'mask_status': mask_status  # Use the extracted mask status
#     }
#     image_name = os.path.basename(image_path)
#     files = {'image': (image_name, open(image_path, 'rb'))}
#     try:
#         response = requests.post(url, data=data, files=files)
#         if response.status_code == 201:
#             print("Entry added successfully.")
#         else:
#             print(f"Failed to add entry: {response.text}")
#     except Exception as e:
#         print(f"Error in store_data: {e}")

# # Example usage
# # image_path = 'path/to/your/image.png'  # Replace with your actual image path
# # temperature = 25.0  # Replace with the actual temperature you want to store
# # store_data(temperature, image_path)


import os
import re
from PIL import Image
import pytesseract
import requests

# Set the path to the Tesseract executable if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # Update this path as needed

def extract_mask_status(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image)

    # Print the extracted text for verification
    print("Extracted Text:")
    print(extracted_text)

    # Initialize variables
    mask_status = None
    final_result = None

    # Search for the mask_status and final_result in the extracted text
    for line in extracted_text.splitlines():
        if "mask" in line.lower():  # Adjust this to match how mask status is formatted in your image
            mask_status = line.strip()  # Store the found mask status
        if "open" in line.lower():  # Adjust this to match how final result is formatted in your image
            final_result = line.strip()  # Store the found final result
        if "temperature" in line.lower():
            temperature = line.strip()
            match = re.search(r"[-+]?\d*\.\d+|\d+", temperature)
            if match:
                temperature = float(match.group())

    # Process the extracted information
    if mask_status == "Mask: No Mask":
        mask_status = False
    else:
        mask_status = True
    
    if final_result == "Final Result: Open the door":
        final_result = True
    else:
        final_result = False

    # Return both mask_status and final_result
    return temperature, mask_status, final_result

def store_data(image_path):
    # Call extract_mask_status to get the mask status and final result
    temperature, mask_status, final_result = extract_mask_status(image_path)

    print("Mask Status:", mask_status)
    print("Final Result:", final_result)
    print("Type of Final Result:", type(final_result))

    url = 'http://127.0.0.1:5000/entry'
    data = {
        'temperature': temperature,
        'mask_status': mask_status,  # Use the extracted mask status
        'final_result': final_result  # Include the final result in the data
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

# Example usage
# image_path = 'path/to/your/image.png'  # Replace with your actual image path
# temperature = 25.0  # Replace with the actual temperature you want to store
# store_data(temperature, image_path)