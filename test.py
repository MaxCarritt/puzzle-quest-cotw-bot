import os
import cv2
import time

def getTemplateImages():
    template_folder = 'template_images/'
    file_list = os.listdir(template_folder)
    icon_templates = {}

    for image in file_list:
        template_path = os.path.join(template_folder, image)
        print(template_path)
        
        template_image = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template_image is not None:
            icon_templates[image] = template_image
            cv2.imshow("Template Image", template_image)
            cv2.waitKey(0)  # Wait indefinitely for a key event
        else:
            print(f"Error loading {image}")
    
    cv2.destroyAllWindows()  # Close all OpenCV windows after loop ends
    return icon_templates

if __name__ == "__main__":
    templates = getTemplateImages()
    # Process or use the loaded templates as needed