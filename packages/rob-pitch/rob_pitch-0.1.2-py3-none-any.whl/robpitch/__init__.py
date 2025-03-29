#!/usr/bin/env python3
# Copyright (c) 2025 Mingqi Jiang (mqjiang_learning@163.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Union
import hashlib
import urllib
import warnings
from tqdm import tqdm
import os
import torch
from robpitch.pitch.mel2pitch.inference import RobPitch


_MODELS = {
    "robpitch":
    "https://modelscope.cn/models/pandamq/robpitch-16k/resolve/master/model.bin"
}

_CONFIGS = {
    "robpitch":
    "https://modelscope.cn/models/pandamq/robpitch-16k/resolve/master/config.yaml"
}

_SHA256S = {
    "robpitch":
    "6b88659bf1e68f1bdcd56e375d7a6fb6152ad2a4dcc1d9f009f2babc68796789",

}

def load_model(
    name: str = "robpitch",
    download_root: str = None,
    device: torch.device = torch.device("cpu")
):
    """
    Load a RobPitch model

    Parameters
    ----------
    name : str
        one of the official model names
    download_root: str
        path to download the model files; by default,
        it uses "~/.cache/robpitch"

    Returns
    -------
    model : RobPitch
        The RobPitch model instance
    """

    if download_root is None:
        default = os.path.join(os.path.expanduser("~"), ".cache")
        download_root = os.path.join(os.getenv("XDG_CACHE_HOME", default),
                                     "robpitch")

    if name in _MODELS:
        checkpoint_file = _download(name, download_root)
    elif os.path.isfile(name):
        checkpoint_file = name
    else:
        raise RuntimeError(
            f"Model {name} not found; available models = {available_models()}")
    model = RobPitch()
    model = model.load_from_checkpoint(config_path = os.path.dirname(checkpoint_file) + f'/{name}.yaml',
                               ckpt_path = checkpoint_file, device=device)
    return model

def available_models() -> List[str]:
    """Returns the names of available models"""
    return list(_MODELS.keys())

def _download(name: str, root: str) -> Union[bytes, str]:
    os.makedirs(root, exist_ok=True)

    expected_sha256 = _SHA256S[name]
    model_url = _MODELS[name]
    download_target = os.path.join(root, f"{name}.bin")

    config_url = _CONFIGS[name]
    config_target = os.path.join(root, f"{name}.yaml")

    if os.path.exists(download_target) and not os.path.isfile(download_target):
        raise RuntimeError(
            f"{download_target} exists and is not a regular file")

    if os.path.isfile(download_target):
        with open(download_target, "rb") as f:
            model_bytes = f.read()
        if hashlib.sha256(model_bytes).hexdigest() == expected_sha256:
            return download_target
        else:
            warnings.warn(
                f"{download_target} exists, but the SHA256 checksum does not"
                " match; re-downloading the file")

    with urllib.request.urlopen(model_url) as source, open(download_target,
                                                     "wb") as output:
        with tqdm(
                total=int(source.info().get("Content-Length")),
                ncols=80,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
                desc="Downloading onnx checkpoint",
        ) as loop:
            while True:
                buffer = source.read(8192)
                if not buffer:
                    break

                output.write(buffer)
                loop.update(len(buffer))

    model_bytes = open(download_target, "rb").read()
    if hashlib.sha256(model_bytes).hexdigest() != expected_sha256:
        raise RuntimeError(
            "Model has been downloaded but the SHA256 checksum does not not"
            " match. Please retry loading the model.")

    if not os.path.exists(config_target):
        with urllib.request.urlopen(config_url) as source, open(config_target,
                                                         "wb") as output:
            with tqdm(
                    total=int(source.info().get("Content-Length")),
                    ncols=80,
                    unit="iB",
                    unit_scale=True,
                    unit_divisor=1024,
                    desc="Downloading config file",
            ) as loop:
                while True:
                    buffer = source.read(8192)
                    if not buffer:
                        break

                    output.write(buffer)
                    loop.update(len(buffer))

    return download_target
