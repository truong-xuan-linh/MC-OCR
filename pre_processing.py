import argparse
from rotation_corrector import find_Longest_Box, calculate_Angle, rotate_Image, rotated_image_predict
from pre_vietocr import vietocr_predict_image
from text_detector import find_box
import cv2
import math
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--image_path', required=True, help='your image ')
  parser.add_argument('--gpu', required=True, help='turn on/off gpu ')
  #Rotate Image
  args = parser.parse_args()
  image_dir = args.image_path
  image = cv2.imread(image_dir)
  if rotated_image_predict(image) == 1:
    image = rotate_Image(image, 180) 
  boxes = find_box(image)
  pos_longest_box = find_Longest_Box(boxes)
  angle = calculate_Angle(pos_longest_box)*180/math.pi
  rotated_image = rotate_Image(image, angle)
  cv2.imwrite("./output/rotated_image/rotated_image.jpg", rotated_image)
  with open("./output/boxes/rotated_image.tsv", "w") as f:
      pass
  #Find boxes and trans
  rotated_image_path = "./output/rotated_image/rotated_image.jpg"
  boxes = find_box(rotated_image_path)
  image = cv2.imread(rotated_image_path)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  for box in boxes:
    A = box[0]
    B = box[1]
    C = box[2]
    D = box[3]
    y1 = int(min(A[1], B[1]))
    y2 = int(max(C[1], D[1]))
    x1 = int(min(A[0], D[0]))
    x2 = int(max(B[0], C[0]))
    cut_image = image[y1:y2, x1:x2]

    text = vietocr_predict_image(cut_image, args.gpu)
    line = ["1",str(x1), str(y1), str(x2), str(y1), str(x2), str(y2), str(x1), str(y2), text]
    line = ",".join(line)
    with open("./output/boxes/rotated_image.tsv", "a", encoding = "utf-8") as f:
      f.write(line+"\n")
if __name__ == '__main__':
    main()