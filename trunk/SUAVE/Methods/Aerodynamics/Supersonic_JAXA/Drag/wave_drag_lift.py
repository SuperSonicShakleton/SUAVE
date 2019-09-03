## @ingroup Methods-Aerodynamics-Supersonic_Zero-Drag
# wave_drag_lift.py
# 
# Created:  Feb 2019, T. MacDonald
# Modified: July 2019 B. Narayana

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
from SUAVE.Core import Data
from SUAVE.Components.Wings import Main_Wing

# ----------------------------------------------------------------------
#   Wave Drag Lift
# ----------------------------------------------------------------------

## @ingroup Methods-Aerodynamics-Supersonic_Zero-Drag
def wave_drag_lift(conditions,configuration,wing):
    """Computes wave drag due to lift

    Assumptions:
    Simplified equations

    Source:
    http://aerodesign.stanford.edu/aircraftdesign/drag/ssdragcalc.html
    JAXA Equations

    Inputs:
    conditions.freestream.mach_number        [Unitless]
    conditions.aerodynamics.lift_coefficient [Unitless]
    wing.total_length                        [m]
    wing.areas.reference                     [m^2]



    wing_area                                                   [m2]
    length of wing                                              [m]
    semispan                                                    [m]



    Outputs:
    wave_drag_lift                           [Unitless]

    Properties Used:
    N/A
    """  

    # Unpack
    freestream      = conditions.freestream
    total_length    = wing.total_length
    Sref            = geometry.reference_area
    Sw              = geometry.wings['main_wing'].areas.reference
    sigma_w         = geometry.wings['main_wing'].areas.box_ratio
    # sigma_w       = 0.6193
    beta            = (1/0.577264)
    s               = geometry.wings['main_wing'].spans.projected
    ar              = geometry.wings['main_wing'].aspect_ratio

    # Conditions
    Mc  = freestream.mach_number * 1.0

    # Length-wise aspect ratio
    ARL = total_length**2/Sref
    
    # Lift coefficient
    if isinstance(wing,Main_Wing):
        CL = conditions.aerodynamics.lift_coefficient
    else:
        CL = np.zeros_like(conditions.aerodynamics.lift_coefficient)
    
    mach_ind = Mc >= 1.01


    # Computations

    p = (2 * s) / (ar * l)

    # defining function fw
    def fw(x):
        if x <= 0.178:
            fwx = 0.0
        else:
            fwx = 0.4935 - 0.2382 * x + 1.6306 * (x ** 2) - 0.86 * (x ** 3) + 0.2232 * (x ** 4) - 0.0365 * (
                        x ** 5) - 0.5
        return fwx

    Kw = (1 + 1 / p) * fw(sigma_w) / (2 * (sigma_w ** 2))

    CDwl = (Sref / Sw) * (((beta ** 2) * p * s * Kw) / (math.pi * l)) * (
                CL ** 2)
    wave_drag_lift = CDwl

    # Dump data to conditions
    wave_lift_result = Data(
        reference_area             = Sref   , 
        wave_drag_lift_coefficient = wave_drag_lift ,
        length_AR                  = ARL,
    )

    return wave_drag_lift
