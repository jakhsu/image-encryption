import cv2
import os
import numpy as np

# Function to decrypt an image with a specified key
def decrypt_image(encrypted_img, key):
    img_height, img_width = encrypted_img.shape
    decrypted_image = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    for i in range(img_height):
        for j in range(img_width):
            result = encrypted_img[i, j]

            # Reverse the polynomial equation and extract binary values
            binary_R = result % 2
            binary_G = (result // 2) % 2
            binary_B = (result // 4) % 2

            # Reverse the padding and concatenate the last bit
            binary_R = bin(123)[2:] + str(binary_R)
            binary_G = bin(123)[2:] + str(binary_G)
            binary_B = bin(123)[2:] + str(binary_B)

            # Convert binary to decimal
            decimal_R = int(binary_R, 2)
            decimal_G = int(binary_G, 2)
            decimal_B = int(binary_B, 2)

            # Update the decrypted image
            decrypted_image[i, j, 0] = decimal_R
            decrypted_image[i, j, 1] = decimal_G
            decrypted_image[i, j, 2] = decimal_B

    return decrypted_image


def modinv(a, m):
    # Modular multiplicative inverse using Extended Euclidean Algorithm
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Encrypted images folder
encrypted_folder = 'color_encrypted'

# Create a folder named "color_decrypted" if it doesn't exist
output_folder = 'color_decrypted'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
else:
    # Remove existing files in the "color_decrypted" folder
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        os.remove(file_path)
    print("Previous files in 'color_decrypted' folder cleared.")

# Load decryption keys from the "keys" folder
keys_folder = 'keys'
keys_file_path = os.path.join(keys_folder, 'keys.txt')

if os.path.exists(keys_file_path):
    with open(keys_file_path, 'r') as keys_file:
        decryption_keys = [int(line.strip()) for line in keys_file]
else:
    print(f"Error: The file '{keys_file_path}' does not exist.")
    exit()

# Decrypt each image in the "color_encrypted" folder using the corresponding key
for i, filename in enumerate(os.listdir(encrypted_folder)):
    file_path = os.path.join(encrypted_folder, filename)

    # Read the encrypted image
    encrypted_img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    # Decrypt the image with the corresponding key
    key = decryption_keys[i]
    decrypted_img = decrypt_image(encrypted_img, key)

    # Convert the image to the correct data type (uint8)
    decrypted_img = decrypted_img.astype(np.uint8)

    # Remove the "encrypted_" prefix and replace with "decrypted_"
    output_filename = filename.replace("encrypted_", "decrypted_")
    output_path = os.path.join(output_folder, output_filename)

    # Save the decrypted image to the "color_decrypted" folder
    cv2.imwrite(output_path, decrypted_img)

    print(f"Decrypted image saved to: {output_path}")
