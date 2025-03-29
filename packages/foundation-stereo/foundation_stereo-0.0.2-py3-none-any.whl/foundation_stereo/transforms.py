#!/usr/bin/env python

from dataclasses import dataclass

import torch

from torchvision.transforms.v2 import functional
from igniter.registry import transform_registry


@transform_registry
@dataclass
class ResizeToDivisible(object):
    factor: float
    interpolation: str = 'bilinear'

    def __post_init__(self):
        self.interpolation = functional.InterpolationMode(self.interpolation)

    def __call__(self, image: torch.Tensor) -> torch.Tensor:
        h, w = image.shape[1:]
        h, w = h - h % self.factor, w - w % self.factor
        return functional.resize(image, [h, w], interpolation=self.interpolation)
