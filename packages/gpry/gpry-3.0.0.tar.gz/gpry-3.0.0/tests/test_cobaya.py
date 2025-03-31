"""
Simple test for the Cobaya interface.
"""

import numpy as np
from scipy import stats

import gpry.mpi as mpi

def gauss_ring_logp(x, y, mean_radius=1, std=0.02):
    """
    Defines a gaussian ring likelihood on cartesian coordinater,
    around some ``mean_radius`` and with some ``std``.
    """
    return stats.norm.logpdf(np.sqrt(x**2 + y**2), loc=mean_radius, scale=std)


info = {"likelihood": {"ring": gauss_ring_logp}}

info["params"] = {
    "x": {"prior": {"min": 0, "max": 2}, "ref": 0.5, "proposal": 0.01},
    "y": {"prior": {"min": 0, "max": 2}, "ref": 0.5, "proposal": 0.01}}


def get_r(x, y):
    return np.sqrt(x ** 2 + y ** 2)


def get_theta(x, y):
    return np.arctan(y / x)


def callback(runner):
    print(
        f" --- Hi, I am the callback function at rank {mpi.RANK}! "
        f"I have a runner: {runner}"
    )


info["params"]["r"] = {"derived": get_r}
info["params"]["theta"] = {"derived": get_theta,
                           "latex": r"\theta", "min": 0, "max": np.pi/2}

info["sampler"] = {"gpry.CobayaSampler": {
    # "gp_acquisition": "NORA",
    # "mc_sampler": "polychord",
    "plots": True,
    "callback": callback,
}}

info["output"] = "chains/coba"
#info["debug"] = True
#info["resume"] = True
info["force"] = True

def test_cobaya():
    from cobaya.run import run
    updated_info, sampler = run(info)


if __name__ == "__main__":
    test_cobaya()
