import torch
import numpy as np
from pyzjr.utils.check import is_tensor, is_numpy

def hwc2chw(x):
    """
    Conversion from 'HWC' to 'CHW' format.
    Example:
        hwc_image_numpy = np.random.rand(256, 256, 3)
        chw_image_numpy = hwc2chw(hwc_image_numpy)
        hwc_image_tensor = torch.rand(256, 256, 3)
        chw_image_tensor = hwc2chw(hwc_image_tensor)
    """
    if len(x.shape) == 3:
        if is_numpy(x):
            chw = np.transpose(x, axes=[2, 0, 1])
            return chw
        elif is_tensor(x):
            chw = x.permute(2, 0, 1).contiguous()
            return chw
        else:
            raise TypeError("The input data should be a NumPy array or "
                            "PyTorch tensor, but the provided type is: {}".format(type(img)))
    else:
        raise ValueError("The input data should be three-dimensional (height x width x channel), but the "
                         "provided number of dimensions is:{}".format(len(img.shape)))

def chw2hwc(x):
    """Conversion from 'CHW' to 'HWC' format."""
    if len(x.shape) == 3:
        if is_numpy(x):
            hwc = np.transpose(x, axes=[1, 2, 0])
            return hwc
        elif is_tensor(x):
            hwc = x.permute(1, 2, 0).contiguous()
            return hwc
        else:
            raise TypeError("The input data should be a NumPy array or "
                            "PyTorch tensor, but the provided type is: {}".format(type(img)))
    else:
        raise ValueError ("The input data should be three-dimensional (channel x height x width), but the "
                          "provided number of dimensions is: {}".format(len(img.shape)))

def to_bchw(x):
    """
    Convert to 'bchw' format
    Example:
        image_tensor = torch.rand(256, 256)
        bchw_image_tensor = to_bchw(image_tensor)
        print("Original shape:", image_tensor.shape)
        print("Converted shape:", bchw_image_tensor.shape)
    """
    if len(x.shape) < 2:
        raise ValueError(f"Input size must be a two, three or four dimensional tensor. Got {tensor.shape}")

    if len(x.shape) == 2:
        if is_tensor(x):
            x = x.unsqueeze(0)
        elif is_numpy(x):
            x = np.expand_dims(x, axis=0)

    if len(x.shape) == 3:
        if is_tensor(x):
            x = x.unsqueeze(0)
        elif is_numpy(x):
            x = np.expand_dims(x, axis=0)

    if len(x.shape) > 4:
        if is_tensor(x):
            x = x.view(-1, x.shape[-3], x.shape[-2], x.shape[-1])
        elif is_numpy(x):
            x = x.reshape((-1, x.shape[-3], x.shape[-2], x.shape[-1]))
    return x

if __name__=="__main__":
    x = torch.rand(2, 4, 3, 256, 256)
    x_n = np.random.rand(2, 4, 3, 256, 256)
    c = to_bchw(x)
    c_ = to_bchw(x_n)
    print(c.shape, c_.shape)