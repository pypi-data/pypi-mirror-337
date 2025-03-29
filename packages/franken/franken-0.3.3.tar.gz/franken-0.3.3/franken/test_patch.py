import torch

from franken.datasets.registry import DATASET_REGISTRY
from franken.trainers.rf_cuda_lowmem import RandomFeaturesTrainer
from franken.data.base import BaseAtomsDataset
from franken.backbones.utils import CacheDir
from franken.rf.model import FrankenPotential

def run():
    # Parameters
    gnn_backbone_id = "MACE-L0"
    kernel_type = "multiscale-gaussian"
    kernel_params = {
        "num_random_features": 512,
        "length_scale_low": 4.0,
        "length_scale_high": 24.0,
        "length_scale_num": 4,
        "rng_seed": 42
    }
    solver_params = {
        "L2_penalty": [1e-8],
        "loss_lerp_weight": [0.99],
    }

    train_dset_8 = BaseAtomsDataset.from_path(
        data_path=DATASET_REGISTRY.get_path("water", "train", base_path=CacheDir.get()),
        split="train",
        gnn_backbone_id=gnn_backbone_id,
        num_random_subsamples=8,
        subsample_rng=42,
    )
    train_dl_8 = train_dset_8.get_dataloader(distributed=False)

    model = FrankenPotential(
        gnn_backbone_id,
        kernel_type,
        kernel_params,
        interaction_block=2,
        num_species=2,        # H and O
        jac_chunk_size=12,    # chosen to fit in the T4 on colab. You can set it to "auto" to adapt to available GPU memory.
    )
    model = model.to("cuda:0")
    trainer = RandomFeaturesTrainer(
        train_dataloader=train_dl_8,
        save_every_model=False,
        device="cuda:0" if torch.cuda.is_available() else "cpu",
        save_fmaps=False,
    )

    torch.cuda.is_available()
    from franken.backbones.wrappers.common_patches import patch_e3nn
    patch_e3nn()

    logs, weights = trainer.fit(model, solver_params)


if __name__ == "__main__":
    run()
