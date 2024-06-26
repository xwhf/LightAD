import torch
import os
import random
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from PIL import Image
import numpy as np
import collections
import numbers
import math
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle


class PSMSegLoader(object):
    def __init__(self, data_path, seq_len, pre_len, step, mode="train"):
        self.mode = mode
        self.step = step
        self.win_size = seq_len + pre_len
        self.seq_len = seq_len
        self.pre_len = pre_len
        self.scaler = StandardScaler()
        data = pd.read_csv(data_path + '/train.csv')
        data = data.values[:, 1:]

        data = np.nan_to_num(data)

        self.scaler.fit(data)
        data = self.scaler.transform(data)
        test_data = pd.read_csv(data_path + '/test.csv')

        test_data = test_data.values[:, 1:]
        test_data = np.nan_to_num(test_data)

        self.test = self.scaler.transform(test_data)
        self.train = data
        self.val = self.test
        self.test_labels = pd.read_csv(data_path + '/test_label.csv').values[:, 1:]

        print("test:", self.test.shape)
        print("train:", self.train.shape)

    def __len__(self):
        """
        Number of images in the object dataset.
        """
        if self.mode == "train":
            return (self.train.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'val'):
            return (self.val.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'test'):
            return (self.test.shape[0] - self.win_size) // self.step + 1
        else:
            return (self.test.shape[0] - self.win_size) // self.pre_len + 1

    def __getitem__(self, index):
        index = index * self.step
        if self.mode == "train":
            return np.float32(self.train[index:index + self.seq_len]),\
                   np.float32(self.train[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(self.test_labels[0:self.win_size])
        elif (self.mode == 'val'):
            return np.float32(self.val[index:index + self.seq_len]), \
                   np.float32(self.val[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'test'):
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        else:
            index = index //self.step * self.pre_len
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[index + self.seq_len:index + self.seq_len + self.pre_len])

class MSLSegLoader(object):
    def __init__(self, data_path, seq_len, pre_len, step, mode="train"):
        self.mode = mode
        self.step = step
        self.win_size = seq_len + pre_len
        self.seq_len = seq_len
        self.pre_len = pre_len
        self.scaler = StandardScaler()
        data = np.load(data_path + "/MSL_train.npy")
        self.scaler.fit(data)
        data = self.scaler.transform(data)
        test_data = np.load(data_path + "/MSL_test.npy")
        self.test = self.scaler.transform(test_data)

        self.train = data
        self.val = self.test
        self.test_labels = np.load(data_path + "/MSL_test_label.npy")
        print("test:", self.test.shape)
        print("train:", self.train.shape)

    def __len__(self):
        """
        Number of images in the object dataset.
        """
        if self.mode == "train":
            return (self.train.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'val'):
            return (self.val.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'test'):
            return (self.test.shape[0] - self.win_size) // self.step + 1
        else:
            return (self.test.shape[0] - self.win_size) // self.pre_len + 1

    def __getitem__(self, index):
        index = index * self.step
        if self.mode == "train":
            return np.float32(self.train[index:index + self.seq_len]), \
                   np.float32(self.train[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'val'):
            return np.float32(self.val[index:index + self.seq_len]), \
                   np.float32(self.val[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'test'):
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        else:
            index = index // self.step * self.pre_len
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[index + self.seq_len:index + self.seq_len + self.pre_len])


class SMAPSegLoader(object):
    def __init__(self, data_path, seq_len, pre_len, step, mode="train"):
        self.mode = mode
        self.step = step
        self.win_size = seq_len + pre_len
        self.seq_len = seq_len
        self.pre_len = pre_len
        self.scaler = StandardScaler()
        data = np.load(data_path + "/SMAP_train.npy")
        self.scaler.fit(data)
        data = self.scaler.transform(data)
        test_data = np.load(data_path + "/SMAP_test.npy")
        self.test = self.scaler.transform(test_data)
        self.train = data
        self.val = self.test
        self.test_labels = np.load(data_path + "/SMAP_test_label.npy")
        print("test:", self.test.shape)
        print("train:", self.train.shape)

    def __len__(self):
        """
        Number of images in the object dataset.
        """
        if self.mode == "train":
            return (self.train.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'val'):
            return (self.val.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'test'):
            return (self.test.shape[0] - self.win_size) // self.step + 1
        else:
            return (self.test.shape[0] - self.win_size) // self.pre_len + 1

    def __getitem__(self, index):
        index = index * self.step
        if self.mode == "train":
            return np.float32(self.train[index:index + self.seq_len]), \
                   np.float32(self.train[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'val'):
            return np.float32(self.val[index:index + self.seq_len]), \
                   np.float32(self.val[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'test'):
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        else:
            index = index // self.step * self.pre_len
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[index + self.seq_len:index + self.seq_len + self.pre_len])


class SMDSegLoader(object):
    def __init__(self, data_path, seq_len, pre_len, step, mode="train"):
        self.mode = mode
        self.step = step
        self.win_size = seq_len + pre_len
        self.seq_len = seq_len
        self.pre_len = pre_len
        self.scaler = StandardScaler()
        data = np.load(data_path + "/SMD_train.npy")
        self.scaler.fit(data)
        data = self.scaler.transform(data)
        test_data = np.load(data_path + "/SMD_test.npy")

        self.test = self.scaler.transform(test_data)
        self.train = data
        data_len = len(self.train)
#        self.val = self.train[(int)(data_len * 0.8):]
        self.val = self.test
        self.test_labels = np.load(data_path + "/SMD_test_label.npy")

    def __len__(self):
        """
        Number of images in the object dataset.
        """
        if self.mode == "train":
            return (self.train.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'val'):
            return (self.val.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'test'):
            return (self.test.shape[0] - self.win_size) // self.step + 1
        else:
            return (self.test.shape[0] - self.win_size) // self.pre_len + 1

    def __getitem__(self, index):
        index = index * self.step
        if self.mode == "train":
            return np.float32(self.train[index:index + self.seq_len]), \
                   np.float32(self.train[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'val'):
            return np.float32(self.val[index:index + self.seq_len]), \
                   np.float32(self.val[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'test'):
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        else:
            index = index // self.step * self.pre_len
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[index + self.seq_len:index + self.seq_len + self.pre_len])


class SWATSegLoader(object):
    def __init__(self, data_path, seq_len, pre_len, step, mode="train"):
        self.mode = mode
        self.step = step
        self.win_size = seq_len + pre_len
        self.seq_len = seq_len
        self.pre_len = pre_len
        self.scaler = StandardScaler()
        data = pd.read_csv(data_path + '/train.csv')
        data = data.values[:, 1:]

        data = np.nan_to_num(data)

        self.scaler.fit(data)
        data = self.scaler.transform(data)
        test_data = pd.read_csv(data_path + '/test.csv')

        test_data = test_data.values[:, 1:]
        test_data = np.nan_to_num(test_data)

        self.test = self.scaler.transform(test_data)
        self.train = data
        self.val = self.test
        self.test_labels = pd.read_csv(data_path + '/test_label.csv').values[:, 1:]

        print("test:", self.test.shape)
        print("train:", self.train.shape)

    def __len__(self):
        """
        Number of images in the object dataset.
        """
        if self.mode == "train":
            return (self.train.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'val'):
            return (self.val.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'test'):
            return (self.test.shape[0] - self.win_size) // self.step + 1
        else:
            return (self.test.shape[0] - self.win_size) // self.pre_len + 1

    def __getitem__(self, index):
        index = index * self.step
        if self.mode == "train":
            return np.float32(self.train[index:index + self.seq_len]), \
                   np.float32(self.train[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'val'):
            return np.float32(self.val[index:index + self.seq_len]), \
                   np.float32(self.val[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'test'):
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        else:
            index = index // self.step * self.pre_len
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[index + self.seq_len:index + self.seq_len + self.pre_len])


class NIPS_TS_SwanSegLoader(object):
    def __init__(self, data_path, seq_len, pre_len, step, mode="train"):
        self.mode = mode
        self.step = step
        self.win_size = seq_len + pre_len
        self.seq_len = seq_len
        self.pre_len = pre_len
        self.scaler = StandardScaler()
        data = np.load(data_path + "/NIPS_TS_Swan_train.npy")

        self.scaler.fit(data)
        data = self.scaler.transform(data)
        test_data = np.load(data_path + "/NIPS_TS_Swan_test.npy")


        self.test = self.scaler.transform(test_data)
        self.train = data
        self.val = self.test
        self.test_labels = np.load(data_path + "/NIPS_TS_Swan_test_label.npy")

        print("test:", self.test.shape)
        print("train:", self.train.shape)

    def __len__(self):
        """
        Number of images in the object dataset.
        """
        if self.mode == "train":
            return (self.train.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'val'):
            return (self.val.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'test'):
            return (self.test.shape[0] - self.win_size) // self.step + 1
        else:
            return (self.test.shape[0] - self.win_size) // self.pre_len + 1

    def __getitem__(self, index):
        index = index * self.step
        if self.mode == "train":
            return np.float32(self.train[index:index + self.seq_len]), \
                   np.float32(self.train[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'val'):
            return np.float32(self.val[index:index + self.seq_len]), \
                   np.float32(self.val[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'test'):
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        else:
            index = index // self.step * self.pre_len
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[index + self.seq_len:index + self.seq_len + self.pre_len])

class NIPS_TS_WaterSegLoader(object):
    def __init__(self, data_path, seq_len, pre_len, step, mode="train"):
        self.mode = mode
        self.step = step
        self.win_size = seq_len + pre_len
        self.seq_len = seq_len
        self.pre_len = pre_len
        self.scaler = StandardScaler()
        data = np.load(data_path + "/NIPS_TS_Water_train.npy")


        self.scaler.fit(data)
        data = self.scaler.transform(data)
        test_data = np.load(data_path + "/NIPS_TS_Water_test.npy")


        self.test = self.scaler.transform(test_data)
        self.train = data
        self.val = self.test
        self.test_labels = np.load(data_path + "/NIPS_TS_Water_test_label.npy")

        print("test:", self.test.shape)
        print("train:", self.train.shape)

    def __len__(self):
        """
        Number of images in the object dataset.
        """
        if self.mode == "train":
            return (self.train.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'val'):
            return (self.val.shape[0] - self.win_size) // self.step + 1
        elif (self.mode == 'test'):
            return (self.test.shape[0] - self.win_size) // self.step + 1
        else:
            return (self.test.shape[0] - self.win_size) // self.pre_len + 1

    def __getitem__(self, index):
        index = index * self.step
        if self.mode == "train":
            return np.float32(self.train[index:index + self.seq_len]), \
                   np.float32(self.train[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'val'):
            return np.float32(self.val[index:index + self.seq_len]), \
                   np.float32(self.val[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        elif (self.mode == 'test'):
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[0:self.win_size])
        else:
            index = index // self.step * self.pre_len
            return np.float32(self.test[index:index + self.seq_len]), \
                   np.float32(self.test[index + self.seq_len:index + self.seq_len + self.pre_len]), np.float32(
                self.test_labels[index + self.seq_len:index + self.seq_len + self.pre_len])


def get_loader_segment(data_path, batch_size,seq_len,pre_len, step=1, mode='train', dataset='KDD'):


    # data准备两个方面：dataset dataloader(dataset准备__len__与__getitem__即可）
    if (dataset == 'MSL'):
        dataset = MSLSegLoader(data_path, seq_len,pre_len, step, mode)
    elif (dataset == 'SMAP'):
        dataset = SMAPSegLoader(data_path,seq_len,pre_len, step, mode)
    elif (dataset == 'SMD'):
        dataset = SMDSegLoader(data_path, seq_len, pre_len, step, mode)
    elif (dataset == 'PSM'):
        dataset = PSMSegLoader(data_path, seq_len,pre_len, step, mode)
    elif (dataset == 'SWAT'):
        dataset = SWATSegLoader(data_path, seq_len,pre_len, step, mode)
    elif (dataset == 'NIPS_TS_Swan'):
        dataset = NIPS_TS_SwanSegLoader(data_path, seq_len,pre_len, step, mode)
    elif (dataset == 'NIPS_TS_Water'):
        dataset = NIPS_TS_WaterSegLoader(data_path, seq_len,pre_len, step, mode)

    shuffle = False
    if mode == 'train':
        shuffle = True

    data_loader = DataLoader(dataset=dataset,
                             batch_size=batch_size,
                             shuffle=shuffle,
                             num_workers=0)
    return data_loader
