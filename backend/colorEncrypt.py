import sys
import cv2
import os
import numpy as np

# Function to encrypt an image with a specified key
def encrypt_image(img, key):
    img_height, img_width, _ = img.shape
    encrypted_image = np.zeros((img_height, img_width), dtype=np.uint8)

    for i in range(img_height):
        for j in range(img_width):
            decimal_number_R = img[i, j, 0]
            binary_R = bin(decimal_number_R)[2:]    #轉二進制
            decimal_number_G = img[i, j, 1]
            binary_G = bin(decimal_number_G)[2:]    #轉二進制
            decimal_number_B = img[i, j, 2]
            binary_B = bin(decimal_number_B)[2:]    #轉二進制

            #將每個二進制調整至8位元，以便後續分配位置
            r=len(binary_R)
            g=len(binary_G)
            b=len(binary_B)

            while r<=7:
                binary_R='0'+binary_R
                r=len(binary_R)

            while g<=7:
                binary_G='0'+binary_G
                g=len(binary_G)

            while b<=7:
                binary_B='0'+binary_B
                b=len(binary_B)

            binary_R=binary_R[:7]
            binary_B=binary_B[:7]
            binary_G=binary_G[:7]

            if binary_R<bin(123):
                R=bin(decimal_number_R)[-1]+binary_R   #係數a 放R
            else:
                R="0"+binary_R

            if binary_G<bin(123):
                G=bin(decimal_number_G)[-1]+binary_G   #係數b 放G
            else:
                G="0"+binary_G

            if binary_B<bin(123):
                B=bin(decimal_number_B)[-1]+binary_B   #係數c 放B
            else:
                B="0"+binary_B

            decimal_R = int(binary_R, 2)
            decimal_G = int(binary_G, 2)
            decimal_B = int(binary_B, 2)

            result = (decimal_R * (key**2) + decimal_G * key + decimal_B) % 251
            encrypted_image[i, j] = result

    return encrypted_image

print("Color Encryption Started")

# Check if the correct number of command line arguments is provided
if len(sys.argv) < 2:
    print("Usage: python colorEncrypt.py <numberOfKeysToUse>")
    sys.exit(1)

# Parse the command line argument
num_keys_to_use = int(sys.argv[1])

# Get a list of all image files in the "color_selected" folder
selected_img_folder = 'color_selected'
selected_img_files = [f for f in os.listdir(selected_img_folder) if f.endswith('.png')]

# Iterate through each image file in the "color_selected" folder
for selected_img_file in selected_img_files:
    file_path = os.path.join(selected_img_folder, selected_img_file)

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the original image
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if img is None:
            print(f"Error: Unable to load image '{file_path}'")
            exit(1)

        print(f"Image loaded: {file_path}")
        image_name = os.path.splitext(selected_img_file)[0]

        # Load encryption keys from the corresponding "keys.txt" file
        keys_folder = 'keys'
        keys_file_path = os.path.join(keys_folder, f'{image_name}.txt')

        if os.path.exists(keys_file_path):
             with open(keys_file_path, 'r') as keys_file:
                    encryption_keys = [int(line.strip()) for line in keys_file][:num_keys_to_use]
        else:
            print(f"Error: The file '{keys_file_path}' does not exist.")
            exit(1)

        # Create a folder named "color_encrypted" if it doesn't exist
        output_folder = 'color_encrypted'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        else:
            # Remove existing files in the "color_encrypted" folder
            for filename in os.listdir(output_folder):
                file_path_to_remove = os.path.join(output_folder, filename)
                os.remove(file_path_to_remove)
            print("Previous files in 'color_encrypted' folder cleared.")

        # Encrypt the image with each key and save the result
        for i, key in enumerate(encryption_keys):
            encrypted_img = encrypt_image(img, key)
            if encrypted_img is None:
                    print("Error: Encryption process failed.")
                    exit(1)
            output_path = os.path.join(output_folder, f'encrypted_{image_name}_{i+1}.png')
            cv2.imwrite(output_path, encrypted_img)
            print(f"Encrypted image saved to: {output_path}")
    else:
        print(f"Error: The file '{file_path}' does not exist.")
