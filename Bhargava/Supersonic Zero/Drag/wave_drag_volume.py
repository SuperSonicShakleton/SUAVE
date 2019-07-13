## @ingroup Methods-Aerodynamics-Supersonic_Zero-Drag
# wave_drag_volume.py
# 
# Created:  Jun 2014, T. MacDonald
# Modified: Feb 2019, T. MacDonald
#           July 2019 B. Narayana

import numpy as np
from SUAVE.Core import Units
from .Cubic_Spline_Blender import Cubic_Spline_Blender
from SUAVE.Components.Wings import Main_Wing                     # do we need to import other body elements (vertical and fuselage) here as well?

## @ingroup Methods-Aerodynamics-Supersonic_Zero-Drag
def wave_drag_volume(vehicle,mach,scaling_factor):
    """Computes the volume drag

    Assumptions:
    Basic fit

    Source:
    D. Raymer, Aircraft Design: A Conceptual Approach, Fifth Ed. pg. 448-449
    JAXA Equations

    Inputs:
    vehicle.
      wings.main_wing.sweeps.leading_edge [rad]
      total_length                        [m]
      maximum_cross_sectional_area        [m^2]
      reference_area                      [m^2]
      box_ratio                           [unitless]         # needs to be defined in ocncorde
    wing.
     length                               [m]                # this is expected to be the length of the wing not the entire vehicle
     thickness_to_chord                   [unitless]
     taper                                [unitless ]       # expected to be 0



    Outputs:
    vehicle_wave_drag                     [Unitless]

    Properties Used:
    N/A
    """ 
    
    num_main_wings = 0
    for wing in vehicle.wings:
        if isinstance(wing,Main_Wing):
            main_wing = wing
            num_main_wings += 1
        if num_main_wings > 1:
            raise NotImplementedError('This function is not designed to handle multiple main wings.')

    #unpack

    LE_sweep = main_wing.sweeps.leading_edge / Units.deg
    L        = vehicle.total_length
    Ae       = vehicle.maximum_cross_sectional_area
    S        = vehicle.reference_area
    dB       = fuselage.effective_diameter                                                       # this is how it is defined in concorde.py
    lN       = fuselage.nose_cone_length                                                         # this was not defined in concorde.py, I added it here
    lT       = fuselage.tail_cone_length                                                         # this was not defined in concorde.py, I added it here
    Sref     = vehicle.reference_area                                                                # make sure this is correctly defined (same as S defined a few lines prior)


# parameters for vertical wing (stabilizer)
    sv       = vertical_stabilizer.spans.projected           # semi-span of vertical tail               # not sure if this is the right way to define it. Guessing!
    lv       = vertical_stabilizer.total_length                                                         # not sure if this is the right way to define it. Guessing!
    thickness_ratio_v =  geometry.wings[
        'vertical_stabilizer'].thickness_to_chord                                                 # make sure this is correctly defined
    muv = geometry.wings['vertical_stabilizer'].taper                                             # make sure this is correctly defined. As you can see i tried different ways of defining
    Sv = geometry.wings['vertical_stabilizer'].areas.reference                                    # this is expected to the area of the wing


# parameters for main wing
    Sw = geometry.wings['main_wing'].areas.reference                                             # this is expected to the area of the wing
    thickness_ratio = thickness_to_chord = geometry.wings['main_wing'].thickness_to_chord        # make sure this is correctly defined
    mu = geometry.wings['main_wing'].taper                                                       # make sure this is correctly defined
    s = geometry.wings[
        'main_wing'].spans.projected                                                             # this is expected to be semi-span although i couldn't find semi-span defined in concorde.py
    beta = (1 / 0.577264)                                                                        # Setting value for Beta - how we get this value is not defined
    l = geometry.wings['main_wing'].total_length                                                 # make sure this is correctly defined


    #calculations

    Vw = (1 / 3) * (thickness_ratio) * (1 + mu + mu ** 2) * (Sw ** 2) / (((1 + mu) ** 2) * s)     # Volume of main wing
    Vv = (2 / 3) * (thickness_ratio_v) * (1 + muv + muv ** 2) * (Sv ** 2) / (((1 + muv) ** 2) * sv)  # Tail Volume

sigma_w = beta*(s/l)         # box_ratio for main wing
sigma_v = beta*(sv/lv)       # box_ratio for vertical wing (stabilizer)


    CDwv_w = (128 * Vw ** 2) / (np.pi * l ** 4) * (0.5114 - 0.4426 * np.log10(sigma_w)) / Sref    # wave drag for wing

    CDwv_v = (128 * Vv ** 2) / (np.pi * lv ** 4) * (
                0.5114 - 0.4426 * np.log10(sigma_v)) / Sref  # wave drag for tail

    CDwv_B = (4.69 / 4) * (np.pi * dB ** 2 / 4) / Sref * ((dB / lN) ** 2 + (dB / lT) ** 2)        # wave drag for fuselage

    CDwv_add = 0.002                                                                              # wave drag for additional (assumed)

    CDwv_total = CDwv_w + CDwv_v + CDwv_B + CDwv_add

    CD_c_vehicle = CDwv_total

"""
Commented this part of the original code out - uncomment as needed 

    # Compute sears-hack D/q
    Dq_SH = 9*np.pi/2*(Ae/L)*(Ae/L)
    
    spline = Cubic_Spline_Blender(1.2,1.3)
    h00 = lambda M:spline.compute(M)    
    
    # Compute full vehicle D/q
    Dq_vehicle           = np.zeros_like(mach)
    Dq_vehicle_simpified = np.zeros_like(mach)
    
    Dq_vehicle[mach>=1.2] = scaling_factor*(1-0.2*(mach[mach>=1.2]-1.2)**0.57*(1-np.pi*LE_sweep**.77/100))*Dq_SH
    Dq_vehicle_simpified  = scaling_factor*Dq_SH
    
    Dq_vehicle = Dq_vehicle_simpified*h00(mach) + Dq_vehicle*(1-h00(mach))
    
    CD_c_vehicle = Dq_vehicle/S
"""
    return CD_c_vehicle


