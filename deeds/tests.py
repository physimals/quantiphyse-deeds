"""
Quantiphyse - tests for Deeds registration

Copyright (c) 2013-2018 University of Oxford
"""
import unittest

from quantiphyse.processes import Process
from quantiphyse.test import ProcessTest

class DeedsProcessTest(ProcessTest):
    
    def testMoco(self):
        yaml = """  
  - Reg:
      method: deeds
      mode: moco
      data: data_4d_moving
      ref-vol: median
      output-suffix: _deedsmoco
"""
        self.run_yaml(yaml)
        self.assertEqual(self.status, Process.SUCCEEDED)
        self.assertTrue("data_4d_moving_deedsmoco" in self.ivm.data)

    def testReg(self):
        yaml = """
  - Reg:
      method: deeds
      reg: data_3d
      ref: data_3d
      output-suffix: _deedsreg
      add-reg: mask
"""
        self.run_yaml(yaml)
        self.assertEqual(self.status, Process.SUCCEEDED)
        self.assertTrue("data_3d_deedsreg" in self.ivm.data)

    def testReg4dRef(self):
        yaml = """
  - Reg:
      method: deeds
      reg: data_3d
      ref: data_4d
      ref-vol: 1
      output-suffix: _deedsreg
      add-reg: mask
"""
        self.run_yaml(yaml)
        self.assertEqual(self.status, Process.SUCCEEDED)
        self.assertTrue("data_3d_deedsreg" in self.ivm.data)

    def testReg4dReg(self):
        yaml = """
  - Reg:
      method: deeds
      reg: data_4d
      ref: data_3d
      output-suffix: _deedsreg
"""
        self.run_yaml(yaml)
        self.assertEqual(self.status, Process.SUCCEEDED)
        self.assertTrue("data_4d_deedsreg" in self.ivm.data)

    def testRegApply(self):
        yaml = """
  - Reg:
      method: deeds
      reg: data_3d
      ref: data_3d
      output-suffix: _deedsreg
      add-reg: mask
      save-transform: deeds_xfm

  - ApplyTransform:
      data: data_3d
      transform: deeds_xfm
      output-name: data_3d_deedsreg2
"""
        self.run_yaml(yaml)
        self.assertEqual(self.status, Process.SUCCEEDED)
        self.assertTrue("data_3d_deedsreg" in self.ivm.data)
        self.assertTrue("deeds_xfm" in self.ivm.data)
        self.assertTrue("data_3d_deedsreg2" in self.ivm.data)
        # FIXME check if registered is the same as applied

if __name__ == '__main__':
    unittest.main()
