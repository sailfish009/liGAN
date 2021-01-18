import sys, os, pytest
import numpy as numpy
from numpy import isclose
from numpy.linalg import norm
import torch

os.environ['GLOG_minloglevel'] = '1'
import caffe

sys.path.insert(0, '.')
import liGAN.models as models


class TestEncoder(object):

    @pytest.fixture
    def enc(self):
        return models.Encoder(
            n_channels=19,
            grid_dim=8,
            n_filters=5,
            width_factor=2,
            n_levels=3,
            conv_per_level=1,
            kernel_size=3,
            relu_leak=0.1,
            pool_type='a',
            pool_factor=2,
            n_output=128,
        )

    def test_init(self, enc):
        assert len(enc.modules) == 6
        assert enc.n_channels == 20
        assert enc.grid_dim == 2

    def test_forward(self, enc):
        x = torch.zeros(10, 19, 8, 8, 8)
        y = enc(x)
        assert y.shape == (10, 128)

    def test_backward(self, enc):
        x = torch.zeros(10, 19, 8, 8, 8)
        y = enc(x)
        y.backward(torch.zeros(10, 128))


class TestDecoder(object):

    @pytest.fixture
    def dec(self):
        return models.Decoder(
            n_input=128,
            grid_dim=2,
            n_channels=64,
            width_factor=2,
            n_levels=3,
            deconv_per_level=1,
            kernel_size=3,
            relu_leak=0.1,
            unpool_type='n',
            unpool_factor=2,
            n_output=19,
        )

    def test_init(self, dec):
        assert len(dec.modules) == 7
        assert dec.n_channels == 19
        assert dec.grid_dim == 8

    def test_forward(self, dec):
        x = torch.zeros(10, 128)
        y = dec(x)
        assert y.shape == (10, 19, 8, 8, 8)

    def test_backward(self, dec):
        x = torch.zeros(10, 128)
        y = dec(x)
        y.backward(torch.zeros(10, 19, 8, 8, 8))


class TestEncoderDecoder(object):

    @pytest.fixture
    def enc_dec(self):
        return models.EncoderDecoder(
            n_channels=19,
            grid_dim=8,
            n_filters=5,
            width_factor=2,
            n_levels=3,
            conv_per_level=1,
            kernel_size=3,
            relu_leak=0.1,
            pool_type='a',
            unpool_type='n',
            n_latent=128,
        )

    def test_init(self, enc_dec):
        pass
