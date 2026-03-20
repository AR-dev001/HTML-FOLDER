import cv2
import numpy as np
import matplotlib.pyplot as plt
def displayimage(title,image):
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:
        plt.imshow(image,cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def interactive_edge_detection(image_path):
    """Interactive thingy for edge detection"""
    image=cv2.imread(image_path)
    if image is None:
        print("Error:Image Not Found")
        return
    gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    displayimage("Original Grayscale image or something",gray_image)
    print("Select An Option:")
    print("1: Sobbel Edge Detection")
    print("2: Canny Edge Detection")
    print("3: Laplacian Edge Detection")
    print("4: Gaussian Smoothing")
    print("5: Median Filtering")
    print("6: Exit")

    while True:
        choice=input("Enter your choice 1-6: ")
        if choice == "1":
            # Sobel Edge Detection
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobelx.astype(np.uint8), sobely.astype(np.uint8))
            displayimage("Sobel Edge Detection", combined_sobel)

        elif choice == "2":
            # Canny Edge Detection
            print("Adjust thresholds for Canny (default: 100 and 200)")
            lower_thresh = int(input("Enter lower threshold: "))
            upper_thresh = int(input("Enter upper threshold: "))
            edges = cv2.Canny(gray_image, lower_thresh, upper_thresh)
            displayimage("Canny Edge Detection", edges)

        elif choice == "3":
            # Laplacian Edge Detection
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            displayimage("Laplacian Edge Detection", np.abs(laplacian).astype(np.uint8))
        
interactive_edge_detection('example.jpg')