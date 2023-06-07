from pathlib import Path; import sys; sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from lib.proc_init_utils import initialise_cpu; initialise_cpu()

import jax.numpy as jnp
import numpy as np
from transformers.models.llama.modeling_llama import LlamaRMSNorm

from lib.array_utils import np2jax, np2pt, pt2jax
from lib.model import config_7B, rms_norm

batch_size = 2
seq_len = 9
d_model = config_7B.d_model
rms_norm_eps = config_7B.rms_norm_eps

rms_norm_pt = LlamaRMSNorm(hidden_size=d_model, eps=rms_norm_eps)

params_pt = rms_norm_pt.weight
params_jax = pt2jax(params_pt)

x_np = np.random.rand(batch_size, seq_len, d_model).astype(np.float32)
x_jax = np2jax(x_np)
x_pt = np2pt(x_np)

y_pt = rms_norm_pt(x_pt)
y_jax = pt2jax(y_pt)
y_hat_jax = rms_norm(params_jax, x_jax, config=config_7B)
assert jnp.allclose(y_jax, y_hat_jax)