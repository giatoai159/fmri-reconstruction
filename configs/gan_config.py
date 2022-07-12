"""____________________Config for Dual-VAE/GAN training___________________________"""

pretrained_gan = None
load_epoch = 335
evaluate = False

image_crop = 375
image_size = 100
latent_dim = 512

device = 'cuda:0'  # cuda or cpu
device2 = 'cuda:3'
device3 = 'cuda:5'

patience = 0   # for early stopping, 0 = deactivate early stopping
data_split = 0.2
batch_size = 100
learning_rate = 0.0001
weight_decay = 1e-7
n_epochs = 400
num_workers = 4
step_size = 30  # for scheduler
gamma = 0.1     # for scheduler
recon_level = 3
lambda_mse = 1e-6
decay_lr = 0.98
decay_margin = 1
decay_mse = 1
decay_equilibrium = 1
margin = 0.35
equilibrium = 0.68
beta = 1.0

kernel_size = 4
stride = 2
padding_mode = [1, 1, 1, 1, 1, 0]
dropout = 0.7

save_images = 5
mean = [0.5, 0.5, 0.5]
std = [0.5, 0.5, 0.5]

# [model, epoch]
# Trained model for stage II (model from stage I)
decoder_weights = ['gan_20220701-145331', 90]       # latent dim = 128


# Trained model for stage III (model from stage II)
cog_encoder_weights = ['gan_cog_2st_20220624-104800', 395]
