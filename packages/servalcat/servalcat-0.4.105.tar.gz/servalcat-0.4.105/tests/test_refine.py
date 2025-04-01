"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology

This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
import unittest
import json
import os
import shutil
import tempfile
import sys
import test_spa
from servalcat.__main__ import main

root = os.path.abspath(os.path.dirname(__file__))

class TestRefine(unittest.TestCase):
    def setUp(self):
        self.wd = tempfile.mkdtemp(prefix="servaltest_")
        os.chdir(self.wd)
        print("In", self.wd)
    # setUp()

    def tearDown(self):
        os.chdir(root)
        shutil.rmtree(self.wd)
    # tearDown()

    def test_refine_geom(self):
        pdbin = os.path.join(root, "5e5z", "5e5z.pdb.gz")
        sys.argv = ["", "refine_geom", "--model", pdbin, "--rand", "0.5"]
        main()
        stats = json.load(open("5e5z_refined_stats.json"))
        self.assertLess(stats[-1]["geom"]["summary"]["r.m.s.d."]["Bond distances, non H"], 0.01)
        
    def test_refine_xtal_int(self):
        mtzin = os.path.join(root, "5e5z", "5e5z.mtz.gz")
        pdbin = os.path.join(root, "5e5z", "5e5z.pdb.gz")
        sys.argv = ["", "refine_xtal_norefmac", "--model", pdbin, "--rand", "0.5",
                    "--hklin", mtzin, "-s", "xray", "--labin", "I,SIGI,FREE"]
        main()
        stats = json.load(open("5e5z_refined_stats.json"))
        self.assertGreater(stats[-1]["data"]["summary"]["CCIfreeavg"], 0.88)
        self.assertGreater(stats[-1]["data"]["summary"]["CCIworkavg"], 0.92)

    def test_refine_xtal(self):
        mtzin = os.path.join(root, "5e5z", "5e5z.mtz.gz")
        pdbin = os.path.join(root, "5e5z", "5e5z.pdb.gz")
        sys.argv = ["", "refine_xtal_norefmac", "--model", pdbin, "--rand", "0.5",
                    "--hklin", mtzin, "-s", "xray", "--labin", "FP,SIGFP,FREE"]
        main()
        stats = json.load(open("5e5z_refined_stats.json"))
        self.assertLess(stats[-1]["data"]["summary"]["Rfree"], 0.22)
        self.assertLess(stats[-1]["data"]["summary"]["Rwork"], 0.20)

    def test_refine_small_hkl(self):
        hklin = os.path.join(root, "biotin", "biotin_talos.hkl")
        xyzin = os.path.join(root, "biotin", "biotin_talos.ins")
        sys.argv = ["", "refine_xtal_norefmac", "--model", xyzin,
                    "--hklin", hklin, "-s", "electron", "--unrestrained"]
        main()
        stats = json.load(open("biotin_talos_refined_stats.json"))
        self.assertGreater(stats[-1]["data"]["summary"]["CCIavg"], 0.7)

    def test_refine_small_cif(self):
        cifin = os.path.join(root, "biotin", "biotin_talos.cif")
        sys.argv = ["", "refine_xtal_norefmac", "--model", cifin,
                    "--hklin", cifin, "-s", "electron", "--unrestrained"]
        main()
        stats = json.load(open("biotin_talos_refined_stats.json"))
        self.assertGreater(stats[-1]["data"]["summary"]["CCIavg"], 0.7)
    
    def test_refine_spa(self):
        data = test_spa.data
        sys.argv = ["", "refine_spa_norefmac", "--halfmaps", data["half1"], data["half2"],
                    "--model", data["pdb"],
                    "--resolution", "1.9", "--ncycle", "2", "--write_trajectory"]
        main()
        self.assertTrue(os.path.isfile("refined_fsc.json"))
        self.assertTrue(os.path.isfile("refined.mmcif"))
        self.assertTrue(os.path.isfile("refined_maps.mtz"))
        self.assertTrue(os.path.isfile("refined_expanded.pdb"))
        
        stats = json.load(open("refined_stats.json"))
        self.assertGreater(stats[-1]["data"]["summary"]["FSCaverage"], 0.66)
        
if __name__ == '__main__':
    unittest.main()

