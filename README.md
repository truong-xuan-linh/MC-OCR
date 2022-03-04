# **Mobile-Captured Image Document Recognition for Vietnamese Receipts (MC-OCR)**
## **Giới thiệu**
MC-OCR là một cuộc thi trích xuất thông tin hóa đơn gồm 2 task:
* Task 1: Đánh giá chất lượng hóa đơn.
* Task 2: Trích xuất thông tin quan trọng trong hóa đơn như: Tên cửa hàng, địa chỉ, thời gian xuất hóa đơn, tổng tiền.

Trong quá trình cuộc thi thì mình đã không tham gia vì một số lí do. Tuy nhiên, sau khi cuộc thi kết thúc, vì dataset vẫn được public nên mình đã thử sức để lấy kinh nghiệm. Mọi người có thể xem thêm chi tiết cuộc thi tại đây : https://www.rivf2021-mc-ocr.vietnlp.com/
## **Task 1: Đánh giá chất lượng hóa đơn**
Trong task này, mình đơn giản chỉ sử dụng mô hình EfficientNetB4 để đánh giá chất lượng các hóa đơn. Và dưới đây là kết quả sau khi submit
<img src ="https://github.com/truong-xuan-linh/MC-OCR/blob/master/RMSE.png" width = "750"/>

## **Task 2: Rút trích thông tin hóa đơn**
Mình tập trung chủ yếu thời gian để thực hiện task này. Để thực hiện task này, mình đã trải qua các bước sau:
* Tìm vùng chứa chữ trong ảnh: Mình sử dụng mô hình **PaddleOCR** để có thể tìm được tất cả các box có chứa chữ trong ảnh và mình hoàn toàn sử dụng pretrain trong mô hình này 
* Xoay ảnh: Sau khi tìm được các vùng chứa chữ trong ảnh. Đầu tiên, mình dựa vào tọa độ của một box bất kì để xem bức ảnh đó có ngang hay không, nếu ngang thì mình quay 90 độ về dọc. Sau đó, mình sử dụng mô hình EfficientNetV2M và tự tạo dataset để có thể phân loại ảnh dọc và ảnh ngược để xoay ảnh ngược 180 độ về ảnh dọc. Sau đó sử dụng kiến thức toán học cơ bản để tình góc vector giữa box dài nhất để có thể xoay bức ảnh về dạng thẳng nhất có thể.
* Đọc văn bản: Để có thể đọc được thông tin trên các box đã nhận dạng, mình tự tạo dataset từ bộ dữ liệu ban tổ chức cung cấp, sau đó sử dụng mô hình **VietOCR** để train với bộ dữ liệu này. Mình train cả hai mô hình Seq2Seq và Transformer thì nhận thấy kết quả của hai mô hình là khá tương đương nhau, tuy nhiên về thời gian thì mô hình Seq2Seq có tốc độ xử lý nhanh hơn nên mình sử dụng mô hình này.
* Rút trích thông tin: Mình sử dụng những trường dữ liệu mà BTC cung cấp như SELLER, TAMSPAN, ADDRESS, TOTAL_COST và tự tạo dataset cho trường OTHER để có thể train với mô hình **PICK** 

Và dưới đây là kết quả task 2 sau khi mình submit:
<img src= "https://github.com/truong-xuan-linh/MC-OCR/blob/master/RMSE.png" width = "750" />

# **Kết quả**
Mọi người có thể sử dụng mô hình để test

**Clone git**
```
git clone https://github.com/truong-xuan-linh/MC-OCR.git
cd MC-OCR
```

**Tải pre-train của mình**
Tải về 2 pre-train mà mình train sau đó dán vào folder checkpoint

https://drive.google.com/drive/folders/1-tMsoLKT2sAtufG9UR4_hI33kg4kfgZM?usp=sharing 

**Cài đặt thư viện cần thiết**
```
pip install "paddleocr>=2.2"
python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```
```
pip install vietocr==0.3.6
pip install --upgrade gdown
```
```
pip install -r PICK-pytorch/requirements.txt
pip install torch==1.5.1+cu101 torchvision==0.6.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
```

**Xoay ảnh và tìm boxes**
```
python pre_processing.py --image_path /content/drive/MyDrive/MCOCR/20220303_232206.jpg {Đường dẫn ảnh} \
                          --gpu 1   
```

**Trích xuất thông tin**
```
python PICK-pytorch/test.py --checkpoint ./checkpoint/model_best.pth \
                --boxes_transcripts ./output/boxes \
                --images_path ./output/rotated_image --output_folder ./output/output \
                --gpu 0 --batch_size 1
```

**Visualize**
```
python visualize.py
```

Kết quả của các quá trình sẽ được lưu trong folder output

Dưới đây là một số ảnh kết quả sau khi trích xuất thông tin hóa đơn
![Screenshot 2022-03-04 110039](https://user-images.githubusercontent.com/79902816/156696999-d42ca555-1d48-4bcb-97a3-7086e2f27b40.png)
![Screenshot 2022-03-04 110454](https://user-images.githubusercontent.com/79902816/156697352-4ed7fdf7-5c88-4b11-8f26-5c948aeb77e3.png)

                
