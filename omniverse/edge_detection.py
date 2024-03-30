import cv2
import sys
import os

def detect_edges(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Could not read the image.")
        sys.exit()

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detector
    edges = cv2.Canny(gray, threshold1=50, threshold2=200)

    # Construct the output filename by adding '_edge' before the file extension
    base, ext = os.path.splitext(image_path)
    output_path = f"{base}_edge{ext}"


    # Save the edges image
    cv2.imwrite(output_path, edges)

    # Optionally, display the edges image
    cv2.imshow('Edges', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        detect_edges(sys.argv[1])
    else:
        print("Please provide an image path.")
