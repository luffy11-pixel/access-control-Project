from PIL import Image

def preprocess_image(image_path, threshold = 150):
    
        img = Image.open(image_path) #Load image 

        gray = img.convert("L") #Convert to grayscale

        binary = gray.point(lambda x: 255 if x > threshold else 0, mode= '1') #convert into binary

        return binary