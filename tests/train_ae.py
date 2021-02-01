import sys
from torch import optim

sys.path.insert(0, '.')
import liGAN

print('creating data loader')
data = liGAN.data.AtomGridData(
    data_root='data/molport',
    batch_size=10,
    rec_map_file='data/my_rec_map',
    lig_map_file='data/my_lig_map',
    resolution=0.5,
    dimension=23.5,
    shuffle=False,
    ligand_only=True,
)

print('loading data')
data.populate('data/molportFULL_rand_test0_1000.types')

print('creating model')
model = liGAN.models.Generator(
    n_channels_in=19,
    n_channels_out=19,
    grid_dim=48,
    n_filters=32,
    width_factor=2,
    n_levels=4,
    conv_per_level=3,
    kernel_size=3,
    relu_leak=0.1,
    pool_type='a',
    unpool_type='n',
    pool_factor=2,
    n_latent=1024,
).cuda()

print('defining loss function')
def loss_fn(y_pred, y_true):
    return ((y_true - y_pred)**2).sum() / 2

print('creating solver')
solver = liGAN.training.AESolver(
    data, data, model, loss_fn, optim.Adam, lr=1e-5
)

print('training model')
solver.train(
	n_iters=1000000,
	test_interval=10,
	test_iters=10,
	save_interval=1000,
	print_interval=10,
)

print('done')
