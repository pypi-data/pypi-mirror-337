import os
import sys
import unittest

import numpy as np
import torch

TEST_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TEST_DIR_PATH + "/../../")

import vertex as vtx

# ----------------------------------------------------------------------------# 
# --------------------              Options               --------------------# 
# ----------------------------------------------------------------------------# 

PBAR_LEAVE = False
PRINT = False

# ----------------------------------------------------------------------------# 
# --------------------             Constants              --------------------# 
# ----------------------------------------------------------------------------# 

N_VOXELS_LARGE = 100_000
N_VOXELS_SMALL = 10_000
N_TRS = 900
BLOCK_SIZE = 5000

THRESHOLD = 0.1
SEED = 1

# ----------------------------------------------------------------------------# 
# --------------            Synthetic Data Creation             --------------# 
# ----------------------------------------------------------------------------# 

np.random.seed(SEED)
LARGE_VOXEL_DATA = np.random.randn(N_TRS, N_VOXELS_LARGE)
SMALL_VOXEL_DATA = np.random.randn(N_TRS, N_VOXELS_SMALL)

GPU_STR = "mps" if torch.mps.is_available() else "cuda"

DEVICE_BACKEND_PAIRS = [("torch", GPU_STR), ("torch", "cpu"), ("numpy", "cpu")]

# ----------------------------------------------------------------------------# 
# --------------------                Main                --------------------# 
# ----------------------------------------------------------------------------# 


def printer(*args):
    """ """
    if PRINT:
        print(*args)


class TestRunners(unittest.TestCase):

    def test_runner(self):
        sc = vtx.correlators.Runner.run(LARGE_VOXEL_DATA, mask=None, exclude_index=None, leave=True,
                                                   block_size=BLOCK_SIZE, symmetric=True,
                                                   backend="torch", device=GPU_STR)
    
    def test_maxxer(self):
        max_ = vtx.correlators.Maxxer.run(LARGE_VOXEL_DATA, mask=None, exclude_index=None, leave=True,
                                              block_size=BLOCK_SIZE, symmetric=True,
                                              backend="torch", device=GPU_STR)
        assert max_ <= 1
        assert max_ >= -1


class TestCorrelationAggregators(unittest.TestCase):

    def test_threshold_correlator(self):
        """ """
        for symmetric in [False, True]:
            for backend, device in DEVICE_BACKEND_PAIRS:

                printer(f"{backend.upper()} {device.upper()} symmetric = {symmetric} ::")
                sc = vtx.ThresholdCorrelator.run(SMALL_VOXEL_DATA, threshold=THRESHOLD,
                                                 mask=None, exclude_index=None, leave=PBAR_LEAVE,
                                                      block_size=BLOCK_SIZE, symmetric=symmetric,
                                                      backend=backend, device=device)
                
                printer("\tmat max:", sc.max(), "mat min:", sc.min(), "data min:",
                      sc.data.min(), "len data", len(sc.data))
                printer()
                self.assertLessEqual(sc.max(), 1)
                self.assertGreater(sc.data.min(), THRESHOLD)

    def test_sparse_correlator(self):
        """ """
        for symmetric in [False, True]:
            for backend, device in DEVICE_BACKEND_PAIRS:

                printer(f"{backend.upper()} {device.upper()} symmetric = {symmetric} ::")
                sc = vtx.SparseCorrelator.run(SMALL_VOXEL_DATA, mask=None, exclude_index=None, leave=PBAR_LEAVE,
                                                      block_size=BLOCK_SIZE, symmetric=symmetric,
                                                      backend=backend, device=device)
                
                printer("\tmat max:", sc.max(), "mat min:", sc.min(), "data min:",
                      sc.data.min(), "len data", len(sc.data))
                printer()
                self.assertLessEqual(sc.max(), 1)
                self.assertGreaterEqual(sc.data.min(), -1)


if __name__ == "__main__":
    unittest.main()

# ----------------------------------------------------------------------------# 
# --------------------                End                 --------------------# 
# ----------------------------------------------------------------------------#
