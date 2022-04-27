# Inherited from
# https://deepayan137.github.io/blog/markdown/2020/08/29/building-ocr.html

import os, sys, pdb, six, random, lmdb, math, logging

from PIL import Image
import numpy as np
from collections import OrderedDict
from itertools import chain

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch.utils.data import sampler
import torchvision.transforms as transforms
from torch.optim.lr_scheduler import CosineAnnealingLR, StepLR
from torch.nn.utils.clip_grad import clip_grad_norm_
from torch.utils.data import random_split

#from src.utils.utils import AverageMeter, Eval, OCRLabelConverter
#from src.utils.utils import EarlyStopping, gmkdir
#from src.optim.optimizer import STLR
#from src.utils.utils import gaussian
from tqdm import *

class SynthDataset(Dataset):
    def __init__(self, opt):
        super(SynthDataset, self).__init__()
        self.path = os.path.join(opt['path'], opt['imgdir'])
        self.images = os.listdir(self.path)
        self.nSamples = len(self.images)
        f = lambda x : os.path.join(self.path, x)
        self.imagepaths = list(map(f, self.images))
        transform_list = [transforms.Grayscale(1),
                transforms.ToTensor(),
                transforms.Normalize((0.5,), (0.5,))]
        self.transform = transforms.Compose(transform_list)
        self.collate_fn = SynthCollator()

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'
        imagepath = self.imagepaths[index]
        imagefile = os.path.basename(imagepath)
        img = Image.open(imagepath)
        if self.transform is not None:
            img = self.transform(img)
        item = { 'img': img, 'idx': index }
        item['label'] = imagefile.split('.jpg')[0] ##
        print(item['label'])
        return item

