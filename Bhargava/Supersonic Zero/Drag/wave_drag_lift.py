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
    freestream   = conditions.freestream
    total_length = wing.total_length
    Sref = geometry.reference_area                         # this is expected to be reference area for the entire vehicle
    Sw = geometry.wings['main_wing'].areas.reference       # this is expected to the area of the wing
    sigma_w = geometry.wings['main_wing'].areas.box_ratio  # couldn't find this in wing.py or concorde - you may have to define it there
    # sigma_w = 0.6193                                     # box ratio for Concorde wing per JAXA
    beta = (1/0.577264)                                    # Setting value for Beta - how we get this value is not defined in JAXA
    s = geometry.wings['main_wing'].spans.projected        # this is expected to be semi-span although i couldn't find semi-span defined in concorde.py
    ar = geometry.wings['main_wing'].aspect_ratio

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

    p = (2 * s) / (ar * l)                                              # Planform Parameter

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
                CL ** 2)                                                 # calculating wave drag due to lift - assume CL to be a specific value
    wave_drag_lift = CDwl
    """
    Commented this part of the original code out - uncomment as needed 
    
    x = np.pi*ARL/4
    beta = np.array([[0.0]] * len(Mc))
    beta[Mc >= 1.01] = np.sqrt(Mc[Mc >= 1.01]**2-1)
    wave_drag_lift = np.array([[0.0]] * len(Mc))
    wave_drag_lift[Mc >= 1.01] = CL[Mc >= 1.01]**2*x/4*(np.sqrt(1+(beta[Mc >= 1.01]/x)**2)-1)
    wave_drag_lift[0:len(Mc[Mc >= 1.01]),0] = wave_drag_lift[Mc >= 1.01]
    """
    # Dump data to conditions
    wave_lift_result = Data(
        reference_area             = Sref   , 
        wave_drag_lift_coefficient = wave_drag_lift ,
        length_AR                  = ARL,
    )

    return wave_drag_lift
