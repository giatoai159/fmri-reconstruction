# Tái tạo hình ảnh từ tín hiệu não người dựa trên mô hình mạng học sâu

## Hướng dẫn cài đặt

### Các thư viện quan trọng

-   Python 3.6.11
-   PyTorch 1.4.0
-   Torchvision 0.5.0
-   Tensorboard 2.4.1
-   Numpy 1.19.2
-   Pandas 1.1.3
-   Matplotlib 3.3.2

Các thư viện sẽ nằm trong file `environment.yml`.

### Hướng dẫn cài đặt

Để có thể chạy chương trình, ta nên sử dụng một môi trường Python riêng biệt thông qua Anaconda hoặc Miniconda (trên Linux).

Chạy lệnh `conda env create -f environment.yml` để tạo môi trường từ file `environment.yml`

Trước khi chạy được chương trình, ta cần tải các tập dữ liệu cần thiết, BOLD5000 và COCO.

-   Dữ liệu BOLD5000 đã được tiền xử lý để mô hình khóa luận đọc được có thể được tải về ở [đây](https://drive.google.com/file/d/1YAySrNKqw_9LEb-uioxZYdIxzUoGZU5Q/view?usp=sharing).
-   Dữ liệu COCO có thể được tải về ở [đây](https://drive.google.com/file/d/1fxETpipfc0U1C1V8pJXgiEEEreND4hCY/view?usp=sharing)

Có thể xem thông tin chi tiết về chuẩn bị dữ liệu thô tại thư mục [data_preprocessing](data_preprocessing).

Các tập tin dữ liệu có thể được giải nén trong thư mục `datasets`.

## Cấu trúc thư mục

-   **configs**: chứa các tập tin chỉnh sửa thông số chương trình
-   **data_preprocessing**: chứa các script python tiền xử lý dữ liệu
-   **inference**: chứa script python đánh giá model
-   **models**: định dạng model
-   **train**: chứa script huấn luyện model

## Chỉnh sửa thông số:

-   `data_config.py:` Chỉnh sửa đường dẫn tới các tập tin.
-   `models_config.py:` Chỉnh sửa thông số kiến trúc mô hình.
-   `gan_config.py:` Chỉnh sửa thông số mô hình.
-   `inference_config.py:` Chỉnh sửa thông số đánh giá mô hình.

## Huấn luyện mô hình

Ta huấn luyện mô hình thông qua 3 bước đề cập ở khóa luận.

Một số thông số quan trọng cần chú ý ở giai đoạn huấn luyện trong `configs/gan_config.py`:

-   Thiết bị huấn luyện:
    `python device = 'cuda:0' # cuda hoặc cpu `

-   Tiếp tục huấn luyện từ tập huấn luyện dở trước đó:
    ```python
    pretrained_gan = None # e.g. 'gan_20210203-173210'
    load_epoch = 395
    evaluate = False
    ```
-   Kích thước ảnh và thông số không gian tiềm ẩn:

    ```python
    image_size = 100
    latent_dim = 128
    ```

-   Trung bình và độ lệch chuẩn ảnh:

    ```python
    mean = [0.5, 0.5, 0.5]
    std = [0.5, 0.5, 0.5]
    ```

#### Bước 1

Chạy lệnh `python3 train/train_vgan_stage1.py -i [input_path] -o [output_path] -l [log_path]`

Với các cờ:

-   ` -i [input_path]` đường dẫn tới tập dữ liệu.
-   ` -o [output_path]` đường dẫn tới nơi output.
-   ` -l [log_path]` đường dẫn tới log.

#### Bước 2

Chỉnh sửa thông số ở tập `configs/gan_config.py`

```python
# Trained model for stage II (model from stage I)
decoder_weights = ['gan_20210127-012348', 90]  # model, epoch
```

Chạy lệnh `python3 train/train_vgan_stage2.py -i [input_path] -o [output_path] -l [log_path]`

#### Stage III

Chỉnh sửa thông số ở tập `configs/gan_config.py`

```python
# Trained model for stage III (model from stage II)
cog_encoder_weights = ['gan_cog_2st_20210223-224153', 395]
```

Chạy lệnh `python3 train/train_vgan_stage3.py -i [input_path] -o [output_path] -l [log_path]`

## Đánh giá mô hình

Một số thông số quan trọng cần chú ý ở khi đánh giá mô hình trong `configs/inference_config.py`:

-   Dữ liệu cho việc đánh giá:

    ```python
    train_data = 'BOLD5000/bold_train/bold_CSI4_pad.pickle'
    valid_data = 'BOLD5000/bold_train/bold_CSI4_pad.pickle'
    ```

-   Đường dẫn tới tập model đã huấn luyện và số epoch:
    ```python
    folder_name = 'gan_cog_3st'
    pretrained_gan = 'gan_cog_3st_20210310-214859'
    load_epoch = 195
    ```
-   Một số thông số khác:
    ```python
    dataset = 'coco' # 'bold', 'coco'
    evaluate = True save = False # True: lưu ảnh
    save_to_folder = None # lưu vào thư mục nào đó
    file_to_save = 'results.csv' # lưu kết quả vào tập tin .csv
    ```

Chạy lệnh `python3 inference/inference_gan.py -i [input_path] -o [output_path] -l [log_path]`

Với các cờ:

-   ` -i [input_path]` đường dẫn tới tập dữ liệu.
-   ` -o [output_path]` đường dẫn tới nơi output.
-   ` -l [log_path]` đường dẫn tới log.

## Mô hình đã huấn luyện

Hiện khóa luận đã huấn luyện mô hình với kích thước ảnh 100x100 và không gian tiềm ẩn 128. Có thể tải về tại [đây](https://drive.google.com/drive/folders/19VgiWyhba94dgERLaPWVz2fQe0gbBi9o?usp=sharing).
