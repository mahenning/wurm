import torch
from torch import nn
from typing import Optional, Dict, List
import os

from .core import Callback


class ModelCheckpoint(Callback):
    """Periodically saves models.

    `filepath` can contain named formatting options, which will be filled with
    the values of keys in `logs` (passed in `after_step`).

    For example: if `filepath` is `steps={steps:.2e}__species={i_species}.pt`
    then the checkpoint will be saved with the number of training steps and
    the species index.

    Args:
        save_folder:
        filepath:
        models:
        interval:
    """
    def __init__(self,
                 save_folder: str,
                 filepath: str,
                 models: List[nn.Module],
                 interval: Optional[int] = 1000):
        super(ModelCheckpoint, self).__init__()
        self.save_folder = save_folder
        self.filepath = filepath
        self.interval = interval
        self.models = models

        os.makedirs(save_folder, exist_ok=True)

        self.i = 0

    def after_step(self,
                   logs: Optional[dict],
                   obs: Optional[Dict[str, torch.Tensor]] = None,
                   rewards: Optional[Dict[str, torch.Tensor]] = None,
                   dones: Optional[Dict[str, torch.Tensor]] = None,
                   infos: Optional[Dict[str, torch.Tensor]] = None):
        if self.i % self.interval == 0:
            for i, model in enumerate(self.models):
                filepath = self.filepath.format(i_species=i, **logs)
                torch.save(model.state_dict(), f'{self.save_folder}/{filepath}')

        self.i += 1