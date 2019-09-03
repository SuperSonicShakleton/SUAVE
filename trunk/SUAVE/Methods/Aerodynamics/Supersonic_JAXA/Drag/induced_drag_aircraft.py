## @ingroup Methods-Aerodynamics-Supersonic_Zero-Drag
# induced_drag_aircraft.py
# 
# Created:  Feb 2019, T. MacDonald
# Modified: Jul 2019 B. Narayana
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
    conditions    = state.conditions
    configuration = settings    
    
    aircraft_lift = conditions.aerodynamics.lift_coefficient
    mach          = conditions.freestream.mach_number
    ar            = geometry.wings['main_wing'].aspect_ratio
    Sref          = geometry.reference_area
    Sw            = geometry.wings['main_wing'].areas.reference
    l             = geometry.wings['main_wing'].total_length
    s             = geometry.wings['main_wing'].spans.projected
    e             = configuration.oswald_efficiency_factor


    # slenderness_ratio = s/l
    p      = (2 * s) / (ar * l)  # Planform Parameter
    spline = Cubic_Spline_Blender(.91, .99)
    h00    = lambda M: spline.compute(M)


    Kv                  = (1 / 2) * (1 + 1 / p)
    CDv                 = (Sref / Sw) * (p * Kv / (np.pi * 2 * (s / l))) * (
                CL * CL)
    total_induced_drag  = CDv




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

