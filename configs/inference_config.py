"""___________________Config for inference_________________________________"""

train_data = 'BOLD5000/bold_train/bold_CSI4_pad.pickle'
valid_data = 'BOLD5000/bold_train/bold_CSI4_pad.pickle'

"""_______________Dual-VAE/GAN____________________"""

dataset = 'bold'       # 'bold' or 'coco'
mode = 'vae-gan'

folder_name = 'gan_cog_3st'
pretrained_gan = 'gan_cog_3st_20220624-222648'
load_epoch = 200


"""___________________________Inference parameters_____________________________"""

evaluate = True       # True if you want to evaluate
save = True         # True to save images
save_to_folder = None  # specify folder name if you want to save in specific directory
file_to_save = 'results.csv'   # save .csv file with results

image_crop = 375
image_size = 100
latent_dim = 128

batch_size = 64
num_workers = 4
recon_level = 3

device = 'cuda:0'
device2 = 'cuda:3'
device3 = 'cuda:5'

save_images = 5
mean = [0.5, 0.5, 0.5]
std = [0.5, 0.5, 0.5]
