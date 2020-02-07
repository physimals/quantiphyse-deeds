"""
Quantiphyse - Registration method using DEEDS

Copyright (c) 2013-2018 University of Oxford
"""
import numpy as np

try:
    from PySide import QtGui, QtCore, QtGui as QtWidgets
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets

from quantiphyse.data import QpData, NumpyData
from quantiphyse.gui.widgets import Citation
from quantiphyse.gui.options import OptionBox, NumericOption
from quantiphyse.utils import get_plugins
from quantiphyse.utils.exceptions import QpException

from .deeds_wrapper import deedsReg, deedsWarp

CITE_TITLE = "MRF-Based Deformable Registration and Ventilation Estimation of Lung CT"
CITE_AUTHOR = "Mattias P. Heinrich, M. Jenkinson, M. Brady and J.A. Schnabel"
CITE_JOURNAL = "IEEE Transactions on Medical Imaging 2013, Volume 32, Issue 7, July 2013, Pages 1239-1248"
CITE_LINK = "http://dx.doi.org/10.1109/TMI.2013.2246577"

RegMethod = get_plugins("base-classes", class_name="RegMethod")[0]

class DeedsRegMethod(RegMethod):
    """
    Registration method using Matthias Heinrich's DEEDS code via a Python wrapper
    """
    def __init__(self, ivm):
        RegMethod.__init__(self, "deeds", ivm, display_name="DEEDS")
        self.options_widget = None

    @classmethod
    def reg_3d(cls, reg_data, ref_data, options, queue):
        """
        Basic 3d registration

        This is the only method that DEEDS implements - 4d and moco are implemented
        using the default multiple calls to reg_3d
        """
        # Handle output space by resampling onto whichever grid we want to output on
        output_space = options.pop("output-space", "ref")
        order = options.pop("interp-order", 1)
        if output_space == "ref":
            if not reg_data.grid.matches(ref_data.grid):
                reg_data = reg_data.resample(ref_data.grid, suffix="", order=order)
        elif output_space == "reg":
            if not reg_data.grid.matches(ref_data.grid):
                ref_data = ref_data.resample(reg_data.grid, suffix="", order=order)
        else:
            raise QpException("DEEDS does not support output in transformed space")

        # FIXME DEEDS is currently ignoring voxel sizes?
        data, trans, log = deedsReg(reg_data.raw(), ref_data.raw(), **options)
        qpdata = NumpyData(data, grid=reg_data.grid, name=reg_data.name)
        trans_data = np.zeros(list(reg_data.grid.shape) + [len(trans),])
        for idx, data in enumerate(trans):
            trans_data[..., idx] = data.reshape(reg_data.grid.shape)

        qptrans = NumpyData(trans_data, grid=reg_data.grid, name="deeds_warp")
        qptrans.metadata["QpReg"] = "deeds"
        return qpdata, qptrans, log.decode("UTF-8")

    @classmethod
    def apply_transform(cls, reg_data, transform, options, queue):
        """
        Apply a previously calculated DEEDS transformation
        """
        if not isinstance(transform, QpData) or transform.nvols != 3 or transform.metadata["QpReg"] != "deeds":
            raise QpException("Transform provided is not a DEEDS transform")

        # Handle output space by resampling onto whichever grid we want to output on
        output_space = options.pop("output-space", "ref")
        order = options.pop("interp-order", 1)
        if output_space == "ref":
            if not reg_data.grid.matches(transform.grid):
                reg_data = reg_data.resample(transform.grid, suffix="", order=order)
        elif output_space == "reg":
            if not reg_data.grid.matches(transform.grid):
                transform = transform.resample(reg_data.grid, suffix="", order=order)
        else:
            raise QpException("DEEDS does not support output in transformed space")

        ux, vx, wx = transform.volume(0), transform.volume(1), transform.volume(2)
        npdata, log = deedsWarp(reg_data.raw(), ux, vx, wx)
        return NumpyData(npdata, grid=reg_data.grid, name=reg_data.name), log.decode("UTF-8")

    def interface(self, generic_options=None):
        """
        :return: QtGui.QWidget containing DEEDS options
        """
        if self.options_widget is None:
            self.options_widget = QtGui.QWidget()  
            vbox = QtGui.QVBoxLayout()
            self.options_widget.setLayout(vbox)

            cite = Citation(CITE_TITLE, CITE_AUTHOR, CITE_JOURNAL)
            vbox.addWidget(cite)

            self.optbox = OptionBox()
            self.optbox.add("Regularisation parameter (alpha)", NumericOption(minval=0, maxval=10, default=2), key="alpha")
            self.optbox.add("Num random samples per node", NumericOption(intonly=True, minval=1, maxval=100, default=50), key="randsamp")
            self.optbox.add("Number of levels", NumericOption(intonly=True, minval=1, maxval=10, default=5), key="levels")

            #grid.addWidget(QtGui.QLabel("Grid spacing for each level"), 3, 0)
            #self.spacing = QtGui.QLineEdit()

            #grid.addWidget(QtGui.QLabel("Search radius for each level"),4, 0)
            #self.radius = QtGui.QLineEdit()

            #grid.addWidget(QtGui.QLabel("Quantisation of search step size for each level"),5, 0)
            #self.radius = QtGui.QLineEdit()

            #grid.addWidget(QtGui.QLabel("Use symmetric approach"),6, 0)
            #self.symm = QtGui.QCheckBox()
            #self.symm.setChecked(True)

            vbox.addWidget(self.optbox)
        return self.options_widget

    def options(self):
        self.interface()
        return self.optbox.values()
