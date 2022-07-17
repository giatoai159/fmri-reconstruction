# Tái tạo hình ảnh từ tín hiệu não người dựa trên mô hình mạng học sâu 

## Chuẩn bị dữ liệu:

* Dữ liệu thô: 
  - [BOLD5000 openneuro.org](https://openneuro.org/datasets/ds001499/versions/1.3.0)
  - [BOLD5000 figshare.com](https://figshare.com/articles/dataset/BOLD5000/6459449)
* Hoặc chỉ tải các ROIs và ảnh kích thích thị giác ở dưới đây và bỏ qua phần tiền xử lý dữ liệu thô: [BOLD5000 ROIs](https://ndownloader.figshare.com/files/12965447)
* Ảnh kích thích thị giác: [BOLD5000 stimuli](https://www.dropbox.com/s/5ie18t4rjjvsl47/BOLD5000_Stimuli.zip?dl=1)

### Các bước sơ bộ:

1. Cài đặt PYTHONPATH
```
export PYTHONPATH=$PYTHONPATH:[đường dẫn tới thư mục]/fmri-reconstruction/
```
2. Thay đổi thông số đường dẫn trong ```config/data_configs.py``` (chi tiết bên dưới).

3. Dữ liệu đã tiền xử lý ở [đây](https://drive.google.com/drive/folders/1yftoRrlOOb1INTxs2Jcq5bMKICI5VwQ5?usp=sharing). 
   Nếu đã tải file thì phải định ra các vị trí của từng file trong folder *BOLD5000*. 
   
    Thay đổi đường dẫn đến ảnh kích thích thị giác trong `BoldRoiDataloader`:
   ```python
    # TODO: thay đổi đường dẫn đến ảnh kích thích thị giác của mình.
    # Dữ liệu có liên quan đến fMRI sẽ được mặc định là nằm trong thư mục "/BOLD5000/"
    if self.root_path is not None and self.root_path not in self.dataset[idx]['image']:
        name = self.dataset[idx]['image'].split('BOLD5000')[0]
        self.dataset[idx]['image'] = self.dataset[idx]['image'].replace(name, self.root_path)
    ```

4. Nên chuẩn bị dữ liệu với cùng cấu trúc thư mục để có thể dễ dàng chạy chương trình. 
  
### Tiền xử lý

### Đọc tín hiệu BOLD

1. Chuẩn bị đường dẫn trong ```data_configs:```
```python
# đường dẫn tới tập dữ liệu user_path/[data_root], user_path sẽ được hỏi lúc chạy chương trình
data_root = 'datasets/'
```
1. Thay đổi đường dẫn tới fMRI và ảnh kích thích thị giác trong ```data_config:```
   
```python
    # Đường dẫn tới ảnh kích thích thị giác được show cho tình nguyện viên
    bold_stimuli_path = 'BOLD5000/BOLD5000_Stimuli/Scene_Stimuli/Presented_Stimuli/'
    # Đường dẫn tới tên các ảnh kích thích thị giác
    bold_labels_path = 'BOLD5000/BOLD5000_Stimuli/Image_Labels/'
    # Đường dẫn tới dữ liệu fMRI chưa tiền xử lý
    bold_session_path = 'BOLD5000/ds001499-download/'
    # Đường dẫn tới tập thông tin ảnh COCO
    coco_annotation_file = 'coco_2017/annotations/annotations_image_info_test2017/image_info_test2017.json'

```
2. Đường dẫn lưu file pickle (chứa đường dẫn tới dữ liệu tín hiệu BOLD và ảnh kích thích thị giác tương ứng)

```python
    # Đường dẫn tới dữ liệu đã tiền xử lý user_path/[save_path]
    save_path = 'BOLD5000/'
```
3. Chạy  ```bold_parser.py``` với các cờ:

```
   python3 data_preprocessing/bold_parser.py -i [input_path] -o [output_path] -l [log_path]
```
  Flags:
  * ``` -i [input_path]``` đường dẫn tới tập dữ liệu thô
  * ``` -o [output_path]``` đường dẫn lưu tập dữ liệu tiền xử lý
  * ``` -l [log_path]``` đường dẫn tới log
   
PS: ```input_path``` và ```output_path``` có thể giống nhau.

4. File pickle sẽ được lưu ở ```user_path/[save_path]```

5. Xem một file ví dụ: [bold500.pickle](https://drive.google.com/file/d/1L_a4pjeUUh8NlD2bgiSCpNAj5MviKzEJ/view?usp=sharing)


### Trích xuất ROIs (vùng trọng yếu)

Ở đây ta sẽ chạy ```data_preprocessing/roi_extraction.py```

1. Cài đặt đường dẫn tới file pickle trong *data_config*

```python
bold_pickle_file = 'BOLD5000/bold5000.pickle'
```

2. Chạy ```data_preprocessing/roi_extraction.py``` với các cờ tương tự trên và bỏ comment các hàm sau:

```python
    
    from  data_preprocessing.roi_extraction import  extract_roi, find_stimuli_path

    extract_roi(SAVE_PATH, ROI_PATH, save=save)
    find_stimuli_path(SAVE_PATH, ROI_PATH, save=save)
```

3. Các file pickle sẽ được lưu lại chứa dữ liệu ROIs tương ứng với ảnh kích thích thị giác. Cấu trúc thư mục sẽ như sau:
   
    ```python
            |-- BOLD5000
                |-- bold_roi
                    |-- CSI1
                        |--CSI1_roi_pad.pickle
                        |--CSI1_stimuli_paths.pickle 
                    |-- CSI2
                        |--CSI2_roi_pad.pickle
                        |--CSI2_stimuli_paths.pickle
                    |-- CSI3
                       |-- ...
                    |-- CSI4
                       |-- ...
    ```
   Xem [ví dụ](https://drive.google.com/drive/folders/1NPXDvj12O0pD2YCxHraprLtCrSPxnAhT?usp=sharing). 
   Có thể tải trực tiếp các dữ liệu này nhưng phải thay đổi các đường dẫn tương ứng.

### Đọc data

Ở đây ta sử dụng ```data_preprocessing/data_loader.py```

1. Hàm ``` concatenate_bold_data(data_dir)``` gộp các dữ liệu fMRI với nhau. 
   Ở đây ta cũng chia dữ liệu thành tập huấn luyện và tập kiểm tra.

```python

    import pickle
    from data_preprocessing.data_loader import concatenate_bold_data
    from sklearn.model_selection import train_test_split
    
    data_path = ... # đường dẫn tới BOLD5000/bold_roi/... 
    # Concatenate data for all subjects
    bold_dataset = concatenate_bold_data(data_path)
    # Split into training and validation sets
    train_data, valid_data = train_test_split(bold_dataset, test_size=0.2, random_state=12345)
    with open(os.path.join(SAVE_PATH, 'bold_train', 'bold_train_norm.pickle'), 'wb') as f:
        pickle.dump(train_data, f)
    with open(os.path.join(SAVE_PATH, 'bold_validation', 'bold_valid_norm.pickle'), 'wb') as f:
        pickle.dump(valid_data, f)
```
2.  Dữ liệu được lưu trong các thư mục:
   
   ```python
   train_data = 'BOLD5000/bold_train/bold_train_norm.pickle'
   valid_data = 'BOLD5000/bold_valid/bold_valid_norm.pickle'
   ```
   * Ví dụ [tập bold huấn luyện](https://drive.google.com/file/d/1FXth92p9gI1dGI8-c-P032psIB_VU6ZL/view?usp=sharing)
   * Ví dụ [tập bold kiểm tra](https://drive.google.com/file/d/1p7_i8M9tWc8B3wc6YzBtWhkzh2yjzJdk/view?usp=sharing)
   
3. Có thể sử dụng chia dữ liệu cố định, xem bên dưới.


### Chia dữ liệu cố định

Ở đây ta chuẩn bị chia dữ liệu cố định. 

Ta có thể tải về các file với list các ID ảnh kích thích thị giác:

* [Ảnh kích thích thị giác huấn luyện](https://drive.google.com/file/d/1COGYwtJvZnQlA23bKULsrmh_nosr6a8C/view?usp=sharing)
* [Ảnh kích thích thị giác kiểm tra](https://drive.google.com/file/d/1hBb79RQ64RnnQSiqy9Bb_6TTXnKgozLa/view?usp=sharing)

Các file trên gồm ID ảnh kích thích thị giác cho tập huấn luyện (90%) và tập kiểm tra (10%).

Nếu ta muốn chuẩn bị phân chia dữ liệu theo ý của mình, thực hiện như sau:

1. Chạy hàm ```train_test_stimuli_split```

```python
from  data_preprocessing.roi_extraction import train_test_stimuli_split

ratio = 0.1 # Tỉ lệ phân chia
train_test_stimuli_split(SAVE_PATH, ROI_PATH, ratio=ratio, save=save)
```
   
* ID ảnh kích thích thị giác tập huấn luyện sẽ được lưu trong file: ```stimuli_train.pickle``` tại SAVE_PATH
* ID ảnh kích thích thị giác tập kiểm tra sẽ được lưu trong file: ```stimuli_valid.pickle``` tại SAVE_PATH

Đường dẫn hiện tại:
```python
# stimuli split to fix train and validation sets
train_stimuli_split = 'BOLD5000/bold_roi/stimuli_train.pickle'
valid_stimuli_split = 'BOLD5000/bold_roi/stimuli_valid.pickle'
```

2. Tất cả dữ liệu fMRI đã gộp với ID ảnh kích thích thị giác cố định:

* [Tập huấn luyện](https://drive.google.com/file/d/1Zohf2I-ZHsY8f-NdLJl9oSmxfzylHVpS/view?usp=sharing)
* [Tập kiểm tra](https://drive.google.com/file/d/1nkJ9OwJ3kR1wDS2BBBQg1mnzbsG_S-Rn/view?usp=sharing)

Trong ```data_configs.py:```
```
# data split with/without fixed stimuli IDs
train: 'BOLD5000/bold_train/bold_train_all_fixed.pickle'
valid: 'BOLD5000/bold_valid/bold_valid_all_fixed.pickle'
```

3. Chỉ sử dụng dữ liệu của một tình nguyện viên

Trong ```data_configs.py:```
```
# data split with/without fixed stimuli IDs
train: 'BOLD5000/bold_train/bold_CSI3_pad.pickle'
valid: 'BOLD5000/bold_train/bold_CSI3_pad.pickle'
```

Để huấn luyện/đánh giá, viết như sau:

```python
from data_preprocessing.bold_loader import split_subject_data

train_data = split_subject_data(train_data, TRAIN_STIMULI)
valid_data = split_subject_data(train_data, VALID_STIMULI)
```

Tại đây ta đã thành công chuẩn bị dữ liệu cho huấn luyện.

