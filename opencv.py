import cv2
import os
image_path = r"C:\Users\HP\Desktop\I OpenCV At The Close\OpenCV\example.jpg"
if not os.path.exists(image_path):
    print("Error: File does not exist at the specified path.")
    exit()
image = cv2.imread(image_path)
if image is None:
    print("Error: Failed to load image. Check file integrity.")
    exit()
cv2.namedWindow('Loaded img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Loaded img', 800, 500)
cv2.imshow('Loaded img', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(f"Img Dimensions: {image.shape}")