
#
# import undulator radiation from file
#
import h5py

code = 'SRW'
hf = h5py.File('//users/srio/OASYS1.2/modelling_team_scripts_and_workspaces/id18n/DATA/undulator_radiation_7.h5','r')
flux3D = hf["/XOPPY_RADIATION/Radiation/stack_data"][:]
energy = hf["/XOPPY_RADIATION/Radiation/axis0"][:]
horizontal = hf["/XOPPY_RADIATION/Radiation/axis1"][:]
vertical = hf["/XOPPY_RADIATION/Radiation/axis2"][:]
hf.close()

# example plot
from srxraylib.plot.gol import plot_image
plot_image(flux3D[0],horizontal,vertical,title="Flux [photons/s] per 0.1 bw per mm2 at %9.3f eV"%(6000.0),xtitle="H [mm]",ytitle="V [mm]")
#
# end script
#

