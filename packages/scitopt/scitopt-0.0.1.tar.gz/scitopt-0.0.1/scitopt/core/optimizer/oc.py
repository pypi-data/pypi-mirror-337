import os
import inspect
import math
import shutil
import json
from dataclasses import dataclass, asdict
import numpy as np
import scipy
import scipy.sparse.linalg as spla
import skfem
import meshio
from scitopt import mesh


@dataclass
class OC_RAMP_Config():
    dst_path: str = "./result"
    record_times: int=20
    max_iters: int=200
    p: float = 3
    p_rate: float = 20.0
    vol_frac: float = 0.4  # the maximum valume ratio
    vol_frac_rate: float = 20.0
    beta: float = 8
    beta_rate: float = 20.
    beta_eta: float = 0.3
    dfilter_radius: float = 0.05
    eta: float = 0.3
    rho_min: float = 1e-3
    rho_max: float = 1.0
    move_limit: float = 0.2
    move_limit_rate: float = 20.0
    

    @classmethod
    def from_defaults(cls, **args):
        sig = inspect.signature(cls)
        valid_keys = sig.parameters.keys()
        filtered_args = {k: v for k, v in args.items() if k in valid_keys}
        return cls(**filtered_args)


    def export(self, path: str):
        with open(f"{path}/cfg.json", "w") as f:
            json.dump(asdict(self), f, indent=2)



class TopOptimizer():
    def __init__(
        self,
        prb: mesh.TaskConfig,
        cfg: OC_RAMP_Config
    ):
        self.prb = prb
        self.cfg = cfg
        if not os.path.exists(self.cfg.dst_path):
            os.makedirs(self.cfg.dst_path)
        self.prb.export(self.cfg.dst_path)
        self.cfg.export(self.cfg.dst_path)
        self.prb.nodes_stats(self.cfg.dst_path)
        
        if os.path.exists(f"{self.cfg.dst_path}/mesh_rho"):
            shutil.rmtree(f"{self.cfg.dst_path}/mesh_rho")
        os.makedirs(f"{self.cfg.dst_path}/mesh_rho")
        if os.path.exists(f"{self.cfg.dst_path}/rho-histo"):
            shutil.rmtree(f"{self.cfg.dst_path}/rho-histo")
        os.makedirs(f"{self.cfg.dst_path}/rho-histo")

        self.recorder = self.history.HistoriesLogger(self.cfg.dst_path)
        self.recorder.add("rho")
        self.recorder.add("rho_diff")
        self.recorder.add("lambda_v")
        self.recorder.add("vol_error")
        self.recorder.add("compliance")
        self.recorder.add("dC")
        self.recorder.add("scaling_rate")
        self.recorder.add("strain_energy")
        # self.recorder_params = self.history.HistoriesLogger(self.cfg.dst_path)
        # self.recorder_params.add("p")
        # self.recorder_params.add("vol_frac")
        # self.recorder_params.add("beta")
        # self.recorder_params.add("move_limit")
    
    
    def optimize(self):
        