#!/usr/bin/env python

# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import torch
import torch.nn.functional as F
import numpy as np


class InputPadder:
    """ Pads images such that dimensions are divisible by 8 """
    def __init__(self, dims, mode='sintel', divis_by=8, force_square=False):
        self.ht, self.wd = dims[-2:]
        if force_square:
          max_side = max(self.ht, self.wd)
          pad_ht = ((max_side // divis_by) + 1) * divis_by - self.ht
          pad_wd = ((max_side // divis_by) + 1) * divis_by - self.wd
        else:
          pad_ht = (((self.ht // divis_by) + 1) * divis_by - self.ht) % divis_by
          pad_wd = (((self.wd // divis_by) + 1) * divis_by - self.wd) % divis_by
        if mode == 'sintel':
            self._pad = [pad_wd//2, pad_wd - pad_wd//2, pad_ht//2, pad_ht - pad_ht//2]
        else:
            self._pad = [pad_wd//2, pad_wd - pad_wd//2, 0, pad_ht]

    def pad(self, *inputs):
        assert all((x.ndim == 4) for x in inputs)
        return [F.pad(x, self._pad, mode='replicate') for x in inputs]

    def unpad(self, x):
        assert x.ndim == 4
        ht, wd = x.shape[-2:]
        c = [self._pad[2], ht-self._pad[3], self._pad[0], wd-self._pad[1]]
        return x[..., c[0]:c[1], c[2]:c[3]]


def bilinear_sampler(img, coords, mode='bilinear', mask=False, low_memory=False):
    """ Wrapper for grid_sample, uses pixel coordinates """
    H, W = img.shape[-2:]
    xgrid, ygrid = coords.split([1,1], dim=-1)
    xgrid = 2*xgrid/(W-1) - 1   # Normalize to [-1,1]
    assert torch.unique(ygrid).numel() == 1 and H == 1 # This is a stereo problem
    grid = torch.cat([xgrid, ygrid], dim=-1).to(img.dtype)
    img = F.grid_sample(img, grid, align_corners=True)
    if mask:
        mask = (xgrid > -1) & (ygrid > -1) & (xgrid < 1) & (ygrid < 1)
        return img, mask.float()
    return img


def coords_grid(batch, ht, wd):
    coords = torch.meshgrid(torch.arange(ht), torch.arange(wd))
    coords = torch.stack(coords[::-1], dim=0).float()
    return coords[None].repeat(batch, 1, 1, 1)


def get_resize_keep_aspect_ratio(H, W, divider: int = 16, max_H: int = 1232, max_W: int = 1232):
  assert max_H % divider == 0 and max_W % divider == 0

  def round_by_divider(x):
    return int(np.ceil(x / divider) * divider)

  H_resize = round_by_divider(H)
  W_resize = round_by_divider(W)
  if H_resize > max_H or W_resize > max_W:
    if H_resize > W_resize:
      W_resize = round_by_divider(W_resize*max_H/H_resize)
      H_resize = max_H
    else:
      H_resize = round_by_divider(H_resize*max_W/W_resize)
      W_resize = max_W
  return int(H_resize), int(W_resize)


def freeze_model(model):
  model = model.eval()
  for p in model.parameters():
    p.requires_grad = False
  for p in model.buffers():
    p.requires_grad = False
  return model
