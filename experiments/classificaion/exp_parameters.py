import os

import numpy as np
from torch.optim.lr_scheduler import StepLR
from torchvision.transforms import Compose, ToTensor, Resize, Normalize
from torchvision.datasets import ImageFolder, MNIST, CIFAR10, FashionMNIST
from torchvision.models import resnet18, resnet50, resnet101

from core.models.cnn.classification_models import resnet18_one_channel
from simple_conv_net import SimpleConvNet3, prune_simple_conv_net

DATASETS_ROOT = '/media/n31v/data/datasets'
MODELS_PATH = '/media/n31v/data/models'
energy_thresholds = [0.1, 0.3, 0.5, 0.7, 0.9, 0.93, 0.96, 0.99, 0.999]
pruning_ratio = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
energy_sfp =[0.9, 0.93, 0.96, 0.99, 0.999]


TASKS = {
    'MNIST': {
        'ds_name': 'MNIST',
        'dataset': MNIST(
            root=DATASETS_ROOT,
            transform=Compose([ToTensor(), Normalize(mean=(0.13066,), std=(0.3081,))])
        ),
        'folds': np.load(os.path.join(DATASETS_ROOT, 'MNIST', 'folds.npy')),
        'dataloader_params': {'batch_size': 512, 'num_workers': 8},
        'model': SimpleConvNet3,
        'model_name': 'SimpleConvNet',
        'model_params': {'num_classes': 10, 'in_channels': 1},
        'fit_params': [{'num_epochs': 10, 'models_path': MODELS_PATH}],
        'ft_params': {'num_epochs': 3, 'models_path': MODELS_PATH},
        'svd_params': {
            'energy_thresholds': energy_thresholds,
            'decomposing_mode': ['channel', 'spatial'],
            'hoer_loss_factor': [0.1, 0.01, 0.001, 0.0001],
            'orthogonal_loss_factor': [1, 10, 100, 1000]
        },
        'sfp_params': {
            'zeroing': {
                'percentage': [{'pruning_ratio': p} for p in pruning_ratio],
                'energy': [{'energy_threshold': e} for e in energy_sfp],
            },
            'final_pruning_fn': prune_simple_conv_net,
            'model_class': SimpleConvNet3,
        },
    },
    'FashionMNIST': {
        'ds_name': 'FashionMNIST',
        'dataset': FashionMNIST(
            root=DATASETS_ROOT,
            transform=Compose([ToTensor(), Normalize(mean=(0.286,), std=(0.353,))])
        ),
        'folds': np.load(os.path.join(DATASETS_ROOT, 'FashionMNIST', 'folds.npy')),
        'dataloader_params': {'batch_size': 512, 'num_workers': 8},
        'model': SimpleConvNet3,
        'model_name': 'SimpleConvNet',
        'model_params': {'num_classes': 10, 'in_channels': 1},
        'fit_params': [{'num_epochs': 10, 'models_path': MODELS_PATH}],
        'ft_params': {'num_epochs': 3, 'models_path': MODELS_PATH},
        'svd_params': {
            'energy_thresholds': energy_thresholds,
            'decomposing_mode': ['channel', 'spatial'],
            'hoer_loss_factor': [0.1, 0.01, 0.001, 0.0001],
            'orthogonal_loss_factor': [1, 10, 100, 1000]
        },
        'sfp_params': {
            'zeroing': {
                'percentage': [{'pruning_ratio': p} for p in pruning_ratio],
                'energy': [{'energy_threshold': e} for e in energy_sfp],
            },
            'final_pruning_fn': prune_simple_conv_net,
            'model_class': SimpleConvNet3,
        },
    },
    'CIFAR10': {
        'ds_name': 'CIFAR10',
        'dataset': CIFAR10(
            root=os.path.join(DATASETS_ROOT, 'CIFAR10'),
            transform=Compose([
                ToTensor(),
                Resize(28),
                Normalize(mean=(0.4914, 0.4822, 0.4465), std=(0.247, 0.2435, 0.2616))
            ])
        ),
        'folds': np.load(os.path.join(DATASETS_ROOT, 'CIFAR10', 'folds.npy')),
        'dataloader_params': {'batch_size': 32, 'num_workers': 8},
        'model': SimpleConvNet3,
        'model_name': 'SimpleConvNet',
        'model_params': {'num_classes': 10},
        'fit_params': [
            {
                'num_epochs': 20,
                'lr_scheduler': StepLR,
                'lr_scheduler_params': {'step_size': 5, 'gamma': 0.2, 'verbose': True},
                'models_path': MODELS_PATH,
            }
        ],
        'ft_params':
            {
                'num_epochs': 6,
                'optimizer_params': {'lr': 0.001},
                'lr_scheduler': StepLR,
                'lr_scheduler_params': {'step_size': 2, 'gamma': 0.2, 'verbose': True},
                'models_path': MODELS_PATH,
            },
        'svd_params': {
            'energy_thresholds': energy_thresholds,
            'decomposing_mode': ['channel', 'spatial'],
            'hoer_loss_factor': [0.1, 0.01, 0.001, 0.0001],
            'orthogonal_loss_factor': [1, 10, 100, 1000]
        },
        'sfp_params': {
            'zeroing': {
                'percentage': [{'pruning_ratio': p} for p in pruning_ratio],
                'energy': [{'energy_threshold': e} for e in energy_sfp],
            },
            'final_pruning_fn': prune_simple_conv_net,
            'model_class': SimpleConvNet3,
        },
    },
    'minerals200': {
        'ds_name': 'minerals(200x200)',
        'dataset': ImageFolder(
            root=os.path.join(DATASETS_ROOT, 'minerals200'),
            transform=Compose([
                ToTensor(),
                Normalize(mean=(0.444, 0.562, 0.556), std=(0.207, 0.235, 0.231))
            ])
        ),
        'folds': np.load(os.path.join(DATASETS_ROOT, 'minerals200', 'folds.npy')),
        'dataloader_params': {'batch_size': 16, 'num_workers': 8},
        'model': resnet18,
        'model_name': 'ResNet18',
        'model_params': {'num_classes': 24},
        'fit_params': [
            {
                'num_epochs': 20,
                'lr_scheduler': StepLR,
                'lr_scheduler_params': {'step_size': 5, 'gamma': 0.2, 'verbose': True},
                'models_path': MODELS_PATH,
                'class_metrics': True,
            }
        ],
        'ft_params':
            {
                'num_epochs': 6,
                'optimizer_params': {'lr': 0.001},
                'lr_scheduler': StepLR,
                'lr_scheduler_params': {'step_size': 2, 'gamma': 0.2, 'verbose': True},
                'models_path': MODELS_PATH,
            },
        'svd_params': {
            'energy_thresholds': energy_thresholds,
            'decomposing_mode': ['channel', 'spatial'],
            'hoer_loss_factor': [0.1, 0.01, 0.001, 0.0001],
            'orthogonal_loss_factor': [1, 10, 100, 1000]
        },
        'sfp_params': {
            'zeroing': {
                'percentage': [{'pruning_ratio': p} for p in pruning_ratio],
                'energy': [{'energy_threshold': e} for e in energy_sfp],
            },
        },
    },
}