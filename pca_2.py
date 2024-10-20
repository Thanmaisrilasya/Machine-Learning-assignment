# -*- coding: utf-8 -*-
"""PCA_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kWUUG9I9bqldIWzsBakzvp_a0-TJMUIe
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = "Ml_image.jpg"
img = Image.open(image_path).convert('L')  # Convert to grayscale

# Resize the image to 256x256 for uniformity
img_resized = img.resize((256, 256))

# Convert the image to a numpy array
img_array = np.array(img_resized)

# Display the original image
plt.figure(figsize=(4, 4))
plt.imshow(img_array, cmap='gray')
plt.title("Original Image")
plt.axis('off')
plt.show()

from sklearn.decomposition import PCA

# Function to apply PCA and reconstruct the image
def pca_image_reconstruction(image, n_components):
    # Reshape image to 2D array (flattened image matrix)
    img_flat = image.reshape(-1, 256)

    # Apply PCA
    pca = PCA(n_components=n_components)
    img_transformed = pca.fit_transform(img_flat)

    # Reconstruct the image
    img_reconstructed = pca.inverse_transform(img_transformed)

    # Reshape back to the original image dimensions
    return img_reconstructed.reshape(256, 256)

# Reconstruct the image with 5 principal components
reconstructed_5PC = pca_image_reconstruction(img_array, 5)

# Display the reconstructed image with 5 PCs
plt.figure(figsize=(4, 4))
plt.imshow(reconstructed_5PC, cmap='gray')
plt.title("5 Principal Components")
plt.axis('off')
plt.show()

# Reconstruct the images with 20 and 50 principal components
reconstructed_20PC = pca_image_reconstruction(img_array, 20)
reconstructed_50PC = pca_image_reconstruction(img_array, 50)

# Display the reconstructed image with 20 PCs
plt.figure(figsize=(4, 4))
plt.imshow(reconstructed_20PC, cmap='gray')
plt.title("20 Principal Components")
plt.axis('off')
plt.show()

# Display the reconstructed image with 50 PCs
plt.figure(figsize=(4, 4))
plt.imshow(reconstructed_50PC, cmap='gray')
plt.title("50 Principal Components")
plt.axis('off')
plt.show()

# Reconstruct the image with 100 principal components
reconstructed_100PC = pca_image_reconstruction(img_array, 100)

# Plot original and all reconstructed images
components = [5, 20, 50, 100]
reconstructed_images = [reconstructed_5PC, reconstructed_20PC, reconstructed_50PC, reconstructed_100PC]

plt.figure(figsize=(10, 6))

# Original image
plt.subplot(1, 5, 1)
plt.imshow(img_array, cmap='gray')
plt.title("Original")
plt.axis('off')

# Reconstructed images
for i, rec_img in enumerate(reconstructed_images):
    plt.subplot(1, 5, i + 2)
    plt.imshow(rec_img, cmap='gray')
    plt.title(f'{components[i]} PCs')
    plt.axis('off')

plt.tight_layout()
plt.show()