# tests/test_vertex.py

import unittest
import os
import sys

file_dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, file_dir_path + "/../")

import vertex

class TestVERTEXMain(unittest.TestCase):

    def test_args(self):
        cifti_path = f"{file_dir_path}/sample_data/example.dtseries.nii"
        save_path = f"{file_dir_path}/outputs/example_vFC.npz"

        arg_list = f"-c {cifti_path} -o {save_path}"
        vertex.main(arg_list.split())

if __name__ == "__main__":
    unittest.main()
