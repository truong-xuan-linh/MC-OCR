import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
def main():
  with open("./output/output/rotated_image.txt", "r") as f:
    information = f.readlines()
  f.close()
  with open("./output/boxes/rotated_image.tsv", "r") as f:
    anno_boxes = f.readlines()
  boxes = []
  pre_texts = []
  image = cv2.imread("./output/rotated_image/rotated_image.jpg")
  h,w,c = image.shape
  scl = max(h//1000,1)
  colors = {"SELLER":(51, 51, 255),
            "TIMESTAMP":(0, 128, 96),
            "TOTAL_COST":(255, 0, 102),
            "ADDRESS":(153, 0, 255)}
  fontpath = "./fonts/Roboto-Black.ttf"
  for anno_box in anno_boxes:
    box = anno_box.split(",")
    boxes.append(box[1:9])
    pre_text = ",".join(box[9:])
    pre_texts.append(pre_text.replace("\n",""))
    
  for inf in information:
    texts = inf.split("\t")
    text = texts[1].replace("\n","")
    texttype = texts[0]
    try:
      index = pre_texts.index(text)
    except:
      continue
    box = boxes[index]
    boxes[index] = " "
    pre_texts[index] = " "
    image = cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[4]), int(box[5])), colors[texttype], scl)
    ## Use simsum.ttc to write Chinese.
    
    font = ImageFont.truetype(fontpath, 15*scl)
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    draw.text((int(box[0]), max(int(box[1])-10,0)),  text, font = font, fill = colors[texttype])
    image = np.array(img_pil)
  cv2.imwrite("./output/visualize/visualize_image.jpg", image)
    #cv2.putText(image, 'Fedex', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
if __name__ == '__main__':
    main()