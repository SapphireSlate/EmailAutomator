import os
import shutil

# Create media directory if it doesn't exist
os.makedirs('media/products', exist_ok=True)

# Save the images with descriptive names
image_mappings = {
    'treat1.jpg': 'path/to/fruity_pebbles_image',  # Replace with actual image path
    'cupcakes.jpg': 'path/to/purple_cupcakes_image',  # Replace with actual image path
    'jar.jpg': 'path/to/chocolate_jar_image'  # Replace with actual image path
}

for new_name, source_path in image_mappings.items():
    destination_path = os.path.join('media/products', new_name)
    try:
        shutil.copy2(source_path, destination_path)
        print(f"Saved {new_name}")
    except Exception as e:
        print(f"Error saving {new_name}: {str(e)}")

print("\nPlease place your product images in the media/products directory with these names:")
print("- treat1.jpg (Fruity Pebbles treat)")
print("- cupcakes.jpg (Purple cupcakes)")
print("- jar.jpg (Chocolate jar)") 