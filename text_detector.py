# -*- coding: utf-8 -*-
"""text_detector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QX24WFNX44EboYcoAsvztS5_uCDZ90S5
"""

from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies

ocr_model = PaddleOCR(lang='en')

def find_box(image):
  result = ocr_model.ocr(image)
  # Extracting detected components
  boxes = [res[0] for res in result] # 
  texts = [res[1][0] for res in result]
  scores = [res[1][1] for res in result]
  return boxes