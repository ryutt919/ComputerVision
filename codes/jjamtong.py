import cv2
import numpy as np

shingeki_img = cv2.imread('./data/shingeki.jpeg')
contrast = 1.6
con_interval = 0.1
brightness = 0
bright_interval = 5
alpha = 0.5

if not shingeki_img is None :


    while True :
        transformed_img = contrast * shingeki_img + brightness
        transformed_img = np.clip(transformed_img, 0, 255).astype(np.uint8)
        blend = (alpha*shingeki_img + (1-alpha)*transformed_img).astype(np.uint8)
        merged_img = np.hstack((shingeki_img,transformed_img, blend))
        

        
        cv2.putText(merged_img,'] : brt,  \' : con', (10,30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,0), thickness=3)
        cv2.putText(merged_img,'] : brt,  \' : con', (10,30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,255,0) )
        cv2.imshow('trasnformed', merged_img)

        key = cv2.waitKey()
        if key == ord(']') :
            brightness+=bright_interval
        elif key == ord('[') :
            brightness -= bright_interval
        elif key == ord(';') :
            contrast -= con_interval
        elif key == ord('\'') :
            contrast += con_interval
        elif key == ord('\t') :
            contrast, brightness = 1.0,0
        elif key == 27 :
            cv2.destroyAllWindows()
            break
            

    