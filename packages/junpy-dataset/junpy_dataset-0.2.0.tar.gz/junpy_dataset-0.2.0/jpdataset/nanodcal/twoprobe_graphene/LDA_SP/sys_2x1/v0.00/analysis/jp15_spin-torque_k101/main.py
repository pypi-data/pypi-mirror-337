import numpy as np
import junpy as jp
from junpy.factory import nanodcal
#from junpy.experiment.extend_center_2 import extend_center

#==============================================================================

filename = '../../NanodcalStructObject.mat'
device = nanodcal.load_nanodcal_device(filename)
#device = extend_center(device, repeatL=1, repeatR=3)
#jp.print(device.structure.central.sites)

#==============================================================================

calc = jp.SpinTorque(
    device=device,
    kpoints=jp.UniformKspaceSampling(
        gridNumber=(101,1,1),
        isTimeReversalSymmetry=False,
    ),
    nonequilibriumEnergies=jp.BiasWindow(interval=1e-3),
    equilibriumEnergies=dict(
        circlePoints=50,
        lowestEnergy=-30,
    ),
    etaSigma=1e-2,
    spinAccumulationDetail=True,
)
jp.run(calc)

#==============================================================================

