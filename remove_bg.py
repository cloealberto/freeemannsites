from PIL import Image
import numpy as np
import os

path = 'c:/Users/cloea/OneDrive/Desktop/antigravity/landing-page/logo.jpg'
out_path = 'c:/Users/cloea/OneDrive/Desktop/antigravity/landing-page/logo-transparent.png'

def remove_background():
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
        
    img = Image.open(path).convert('RGBA')
    data = np.array(img)
    
    # Define the reference background color from the top-left corner
    bg_color = data[0, 0, :3].astype(np.int32)
    
    # Calculate color distance to background
    diff = data[:, :, :3].astype(np.int32) - bg_color
    dist = np.linalg.norm(diff, axis=2)
    
    # Create an alpha mask based on distance threshold
    # To avoid jagged edges, we can create a soft threshold (anti-aliasing)
    lower_threshold = 40
    upper_threshold = 80
    
    # Completely transparent where distance < lower_threshold
    alpha = np.ones(dist.shape, dtype=np.float32) * 255
    alpha[dist < lower_threshold] = 0
    
    # Blend alpha where distance is between lower and upper threshold
    mask = (dist >= lower_threshold) & (dist < upper_threshold)
    alpha[mask] = (dist[mask] - lower_threshold) / (upper_threshold - lower_threshold) * 255
    
    data[:, :, 3] = alpha.astype(np.uint8)
    
    Image.fromarray(data).save(out_path)
    print(f"Saved transparent logo to {out_path}")

if __name__ == '__main__':
    remove_background()
