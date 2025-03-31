import scipy.io as sio
import torch
from torch.utils.data import Dataset
from torch.optim.lr_scheduler import StepLR, MultiStepLR, CosineAnnealingLR


class KanDataset(Dataset):
    def __init__(self, data_path):
        self.path = data_path
        self.data = sio.loadmat(data_path)
        self.features = torch.tensor(self.data['features']).double()
        self.labels = torch.tensor(self.data['labels'].squeeze()).double()

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        feature = self.features[idx]
        label = self.labels[idx]
        return feature, label

