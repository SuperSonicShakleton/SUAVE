## @ingroup Methods-Aerodynamics-Supersonic_Zero-Drag
# induced_drag_aircraft.py
# 
# Created:  Feb 2019, T. MacDonald
#  Modified: July 2019 B. Narayana
#         
     
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from SUAVE.Core import Data

import numpy as np
from .Cubic_Spline_Blender import Cubic_Spline_Blender

# ----------------------------------------------------------------------
#  Induced Drag Aicraft
# ----------------------------------------------------------------------

## @ingroup Methods-Aerodynamics-Supersonic_Zero-Drag
def induced_drag_aircraft(state,settings,geometry):
    """Determines induced drag for the full aircraft

    Assumptions:
    Based on fits

    Source:
    http://aerodesign.stanford.edu/aircraftdesign/aircraftdesign.html (Stanford AA241 A/B Course Notes)
    JAXA Equations

    Inputs:
    state.conditions.aerodynamics.lift_coefficient               [Unitless]
    state.conditions.aerodynamics.drag_breakdown.parasite.total  [Unitless]
    configuration.oswald_efficiency_factor                       [Unitless]
    configuration.viscous_lift_dependent_drag_factor             [Unitless]
    geometry.wings['main_wing'].span_efficiency                  [Unitless]
    geometry.wings['main_wing'].aspect_ratio                     [Unitless]


    lift_coefficient                                            [Unitless]
    reference_area                                              [m2]
    wing_area                                                   [m2]
    length of wing                                              [m]
    semispan                                                    [m]

    Outputs:
    total_induced_drag                                           [Unitless]

    Properties Used:
    N/A
    """

    # unpack inputs
    conditions = state.conditions
    configuration = settings    
    
    aircraft_lift = conditions.aerodynamics.lift_coefficient
    mach          = conditions.freestream.mach_number
    ar = geometry.wings['main_wing'].aspect_ratio
    Sref = geometry.reference_area                                     # reference area for the entire vehicle
    Sw = geometry.wings['main_wing'].areas.reference                   # this is expected to the area of the wing
    l = geometry.wings['main_wing'].total_length                       # not found in wing.py
    s = geometry.wings['main_wing'].spans.projected                    # this is expected to be semi-span although i couldn't find semi-span defined in concorde.py

    e             = configuration.oswald_efficiency_factor
    """
    Commented this part of the original code out - uncomment as needed 
    
    K             = configuration.viscous_lift_dependent_drag_factor
    wing_e        = geometry.wings['main_wing'].span_efficiency
    ar            = geometry.wings['main_wing'].aspect_ratio 
    CDp           = state.conditions.aerodynamics.drag_breakdown.parasite.total
    
    if e == None:
        e = 1/((1/wing_e)+np.pi*ar*K*CDp)    
"""

    # slenderness_ratio = s/l                                             # Slenderness Ratio
    p = (2*s)/(ar*l)                                                      # Planform Parameter

    spline = Cubic_Spline_Blender(.91,.99)
    h00 = lambda M:spline.compute(M)      
    """
    total_induced_drag_low  = aircraft_lift**2 / (np.pi*ar*e)
    total_induced_drag_high = aircraft_lift**2 / (np.pi*ar*wing_e) # oswald factor would include wave drag due to lift
     """                                                                               # which is not computed here

    Kv = (1 / 2) * (1 + 1 / p)

    CDv = (Sref / Sw) * (p * Kv / (np.pi * 2 * (s / l))) * (
                CL ** 2)                                                               # calculating vortex drag due to lift - assume CL to be a specific value
    total_induced_drag = CDv


""" 
    total_induced_drag      = total_induced_drag_low*h00(mach) + total_induced_drag_high*(1-h00(mach))
   """

    # store data
    try:
        conditions.aerodynamics.drag_breakdown.induced = Data(
            total             = total_induced_drag ,
            efficiency_factor = e                  ,
            aspect_ratio      = ar                 ,

        )
    except:
        print("Drag Polar Mode")
    
    return total_induced_drag

