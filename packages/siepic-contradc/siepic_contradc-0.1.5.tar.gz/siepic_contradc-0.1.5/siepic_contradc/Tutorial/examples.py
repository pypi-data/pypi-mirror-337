# %% append Python path to code location
import os, sys, inspect
import matplotlib.pyplot as plt
import numpy as np
from siepic_contradc.ContraDC import ContraDC
from siepic_contradc.modules import *


def examples(num):
    """Function implements 4 use-case examples"""

    """ Example 1: regular SOI Contra-DC """
    if num == 1:

        # instantiate, simulate and show result
        device = ContraDC().simulate().displayResults()

        # calculate thimpe group delay
        device.getGroupDelay()

        # plot group delay
        plt.figure()
        plt.plot(device.wavelength * 1e9, device.group_delay * 1e12)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Tg (ps)")

        plt.show()

    """ Example 2: Full chirped example.
        Create a CDC with chirped w1, w2, period, temperature.
    """
    if num == 2:

        # Waveguide chirp
        w1 = [0.56e-6, 0.56e-6]
        w2 = [0.44e-6, 0.44e-6]
        w_chirp_step = 0.1e-9

        # Period chirp
        period = [310e-9, 320e-9]

        # apod shape
        apod_shape = "gaussian"

        N = 10000

        device = ContraDC(
            N=N,
            w1=w1,
            w2=w2,
            apod_shape=apod_shape,
            period_chirp_step=1e-9,
            w_chirp_step=w_chirp_step,
            period=period,
            N_seg=1500,
            kappa=10000,
            a=0,
            alpha=1.5,
            wvl_range=[1500e-9, 1600e-9],
        )

        device.simulate().displayResults()

    """ Example 3: defining custom chirp profiles
    """
    if num == 3:

        device = ContraDC(apod_shape="tanh")

        z = np.linspace(0, device.N_seg, device.N_seg)
        device.w1_profile = device.w1 * np.cos(z / 600)
        device.w2_profile = device.w2 * np.cos(z / 600)

        device.simulate().displayResults()

    """ Example 4: using custom supermode indices.
        You might want to use this if you are designing 
        with silicon nitride, of using other waveguide specs than
        SOI, 100-nm gap.
    """
    if num == 4:

        import os

        current_dir = os.path.dirname(__file__)
        polyfit_file_path = os.path.join(
            current_dir, "SiN_1550_TE_w1_850nm_w2_1150nm_thickness_400nm.txt"
        )
        device = ContraDC(polyfit_file=polyfit_file_path, period=335e-9)
        device.simulate().displayResults()

    """Example 5: Lumerical-assisted flow
    """
    if num == 5:

        apod_shape = "tanh"
        period = 318e-9
        w1 = 560e-9
        w2 = 440e-9

        device = ContraDC(w1=w1, w2=w2, apod_shape=apod_shape, period=period)

        device.simulate()
        plt.plot(device.wavelength * 1e9, device.drop)
        plt.plot(device.wavelength * 1e9, device.thru)
        plt.show()

        # Generate compact model for Lumerical INTERCONNECT
        device.gen_sparams()  # this will create a ContraDC_sparams.dat file to import into INTC

    """Example 6: Complete Lumerical flow - simulate coupling coefficient (not simulating mode profiles)
    """
    if num == 6:

        apod_shape = "tanh"
        period = 318e-9
        w1 = 560e-9
        dw1 = 25e-9
        w2 = 440e-9
        dw2 = 50e-9
        gap = 100e-9

        device = ContraDC(
            w1=w1,
            dw1=dw1,
            w2=w2,
            dw2=dw2,
            gap=gap,
            apod_shape=apod_shape,
            period=period,
        )

        device.simulate_kappa()
        device.simulate().displayResults()
        plt.plot(device.wavelength * 1e9, device.drop)
        plt.plot(device.wavelength * 1e9, device.thru)
        plt.show()

        # Generate compact model for Lumerical INTERCONNECT
        device.gen_sparams()  # this will create a ContraDC_sparams.dat file to import into INTC

    """ Example 7: regular SOI Contra-DC, update the INTERCONNECT Design Kit for the EBeam PDK  """
    if num == 7:

        # instantiate, simulate and show result
        device = ContraDC(N=1000, period=322e-9, polyfit_file=None, a=10, apod_shape="gaussian",
                 kappa=48000, T=300, resolution=500, N_seg=100, wvl_range=[1499e-9, 1601e-9],
                 central_wvl=1550e-9, 
                 alpha=10, w1=.56e-6, w2=.44e-6, dw1=50e-9, dw2=25e-9, gap=.1e-6,
                 w_chirp_step=1e-9, period_chirp_step=2e-9, angle=85, 
                 mat_device='Si (Silicon) - Dispersive & Lossless',
                 thickness_device=.22e-6, thickness_rib=90e-9, rib=False, pol='TE')
        
        device.simulate().displayResults()

        # Update the INTERCONNECT model
        filename = device.update_DesignKit_model('EBeam')
        print(f'Sparameter data saved to: {filename}')

    """ Example 12: O-Band SOI Contra-DC, simulate, update the INTERCONNECT Design Kit for the EBeam PDK  """
    if num == 12:

        # instantiate, simulate and show result
        device = ContraDC(N=1000, period=291e-9, polyfit_file=None, a=10, apod_shape="gaussian",
                 kappa=48000, T=300, resolution=500, N_seg=100, wvl_range=[1259e-9, 1361e-9],
                 central_wvl=1310e-9, 
                 alpha=10, w1=.56e-6, w2=.44e-6, dw1=50e-9, dw2=25e-9, gap=.1e-6,
                 w_chirp_step=1e-9, period_chirp_step=2e-9, angle=85, 
                 mat_device='Si (Silicon) - Dispersive & Lossless',
                 thickness_device=.22e-6, thickness_rib=90e-9, rib=False, pol='TE')
        
        device.simulate().displayResults()

        # Update the INTERCONNECT model
        filename = device.update_DesignKit_model('EBeam')
        print(f'Sparameter data saved to: {filename}')

    """ Example 13: Exporting design to a layout test structure"""
    if num == 13:
        # Device's physical parameters, used for the layout
        apod_shape = "gaussian"
        period = 318e-9
        w1 = 560e-9
        dw1 = 25e-9
        w2 = 440e-9
        dw2 = 50e-9
        gap = 100e-9
        N = 1000

        device = ContraDC(
            N=N,
            w1=[w1],
            dw1=dw1,
            w2=[w2],
            dw2=dw2,
            gap=gap,
            apod_shape=apod_shape,
            period=[period],
        )
        device.layout(pdk="SiEPIC_EBeam_PDK")

if __name__ == "__main__":
    examples(13)

# %%
