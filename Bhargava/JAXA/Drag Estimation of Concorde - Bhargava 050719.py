#!/usr/bin/env python
# coding: utf-8

# In[47]:


# Main Wing

#_______________________________________# Input Data_________________________________________________________

M = 2                                                                              # Mach number           
Re_u = 8.07*(10**6)                                                                # Unit Reynolds Number
Sw =  412.23                                                                       # Wing Area                                  # m2
s = 12.8                                                                           # Semispan                                   # m
l = 35.8                                                                           # Max Chordwise Length                       # m
mu = 0                                                                             # Taper Ratio                                
thickness_ratio = 0.025 
dB = 3.086                                                                         # Diameter                                   # m

                                         
#_______________________________________# To be calculated_________________________________________________________

AR = ((2*s)**2)/Sw                                                                  # Aspect Ratio
slenderness_ratio = s/l                                                             # Slenderness Ratio 
p = (2*s)/(AR*l)                                                                    # Planform Parameter 
Cr = Sw/(s*(1+mu))                                                                  # Root Chord
def c(y):                                                                           # Chord distribution
    c_y = Cr*(1-(1-mu)*(y/s))
    return c_y

MAC = (2/3)*(Sw/s)*(1+mu+mu*mu)/((1+mu)**2)                                          # Mean Aerodynamic Chord

def Aw(y):                                                                           # Cross Sectional Area
    Aw_y = (1/2)*(thickness_ratio)*(c(y)**2)
    return Aw_y        


Vw = (1/3)*(thickness_ratio)*(1+mu+mu**2)*(Sw**2)/(((1+mu)**2)*s)                     # Volume
tau = Vw/(Sw**(3/2))                                                                  # Volume Parameter
Sw_wet = 2*(Sw - l*dB)                                                                # Wetted Area
Re_MAC = MAC*Re_u                                                                     # Reynolds number on MAC 


print("The aspect ratio is " + str(AR))
print("The slenderness ratio is " + str(slenderness_ratio))
print("The planform parameter is " + str(p))
print("The MAC is " + str(MAC))
print("The Volume is " + str(Vw))
print("The Volume parameter is " + str(tau))
print("The Wetted Area is " + str(Sw_wet))
print("The Reynolds number (in Million) on MAC is " + str(Re_MAC/(10**6))) 


# In[48]:


# Fuselage Geometry 

#_______________________________________# Input Data_________________________________________________________

lB = 62                                                                              # Fuselage Length 
dB = 3.086                                                                           # Fuselage Diameter
lN = 11                                                                              # Nose Cone Length 
lT = 13                                                                              # Tail Cone Length 
import math

#_______________________________________# To be calculated_________________________________________________________


lamda_N = lN/dB                                                                      # Nose Cone Ratio
lamda_T = lT/dB                                                                      # Tail Cone Ratio
SCross = (math.pi/4)*(dB**2)                                                         # Cross sectional area of cylindrical cone
SB_wet = 4*SCross*((lB/dB)-(1/3)*(lamda_N + lamda_T))                                # Wetted Area
VB = lB*SCross*(1-(7/15)*(dB/lB)*(lamda_N + lamda_T))                                # Volume of fuselage
Re_lB = lB*Re_u                                                                      # Reynolds number on fuselage length 


print("The nose cone ratio is " + str(lamda_N))
print("The tail cone ratio is " + str(lamda_T))
print("The Cross-section Area is " + str(SCross))

print("The Wetted Area is " + str(SB_wet))
print("The Volume is " + str(VB))
print("The Reynolds number (in Million) on fuselage length is " + str(Re_lB/(10**6))) 


# In[49]:



# Vertical Tail Geometry 

#_______________________________________# Input Data_________________________________________________________

Sv = 37.919                                                                         # Vertical Tail Area 
sv = 5.39                                                                           # semispan
lv = 14.07                                                                          # Max Chordwise Length 
muv = 0                                                                             # Taper Ratio
thickness_ratio_v = 0.03                                                            # Thickness Ratio
import math

#_______________________________________# To be calculated_________________________________________________________


slenderness_ratio_v = sv/lv                                                         # Slenderness Ratio Tail

pv = Sv/(2*sv*lv)                                                                   # Planform Parameter Tail

def cv(y):                                                                          # Tail Chord distribution
    cv_y = lv*(1-(1-muv)*(y/sv))
    return cv_y

MACv = (4/3)*(Sv/sv)*(1+muv+muv**2)/((1+muv)**2)                                    # Tail Mean Aerodynamic Chord

def Av(y):                                                                          # Tail Cross Sectional Area
    Av_y = (1/2)*(thickness_ratio_v)*(cv(y)**2)
    return Av_y        


Vv = (2/3)*(thickness_ratio_v)*(1+muv+muv**2)*(Sv**2)/(((1+muv)**2)*sv)             # Tail Volume
tau_v = Vv/(Sv**(3/2))                                                              # Tail Volume Parameter 
Sv_wet = 2*(Sv)                                                                     # Tail Wetted Area
Re_MACv = MACv*Re_u                                                                 # Reynolds number on Tail MAC 



print("The slenderness ratio is " + str(slenderness_ratio_v))
print("The planform parameter is " + str(pv))
print("The MAC is " + str(MACv))
print("The Volume is " + str(Vv))
print("The Volume parameter is " + str(tau_v))
print("The Wetted Area is " + str(Sv_wet))
print("The Reynolds number (in Million) on Tail MAC is " + str(Re_MACv/(10**6))) 


# In[50]:



Sref = 329.78  # Reference Area 


# ___________________________________ Friction Drag Calculations _______________________________



def CDf(ReL,M):                                                                   # friction drag for each component  
    Cfi = 0.455*(math.log10(ReL)**(-2.58))                                        # Prandtl's formula 
    fM = (1+0.15*M*M)**(-0.58)                                                    # Hoerner's formula 
    CDf = Cfi*fM
    return CDf


CDf_total = CDf(Re_MAC, M)*(Sw_wet/Sref)  + CDf(Re_MACv, M)*(Sv_wet/Sref) +  CDf(Re_lB, M)*(SB_wet/Sref) # Total Friction Drag

CDf_w = CDf(Re_MAC, M)*(Sw_wet/Sref)                  # friction drag for wing
CDf_v = CDf(Re_MACv, M)*(Sv_wet/Sref)                 # friction drag for tail
CDf_B = CDf(Re_lB, M)*(SB_wet/Sref)                   # friction drag for fuselage


print("The wing CDf is " + str(CDf_w)) 
print("The tail CDf is " + str(CDf_v)) 
print("The fuselage CDf is " + str(CDf_B)) 
print("The total CDf is " + str(CDf_total)) 


# In[51]:


sigma_w = 0.6193 # box ratio for wing
sigma_v = 0.6635 # box ratio for tail

beta = (1/0.577264)         # Setting value for Beta - how we get this value is not defined

# ___________________________________ Wave Drag Calculations _______________________________ 



CDwv_w = (128*Vw**2)/(math.pi*l**4)*(0.5114-0.4426*math.log10(sigma_w))/Sref      # wave drag for wing

CDwv_v = (128*Vv**2)/(math.pi*lv**4)*(0.5114-0.4426*math.log10(sigma_v))/Sref     # wave drag for tail

CDwv_B = (4.69/4)*(math.pi*dB**2/4)/Sref*((dB/lN)**2 + (dB/lT)**2)                # wave drag for fuselage

CDwv_add = 0.002                                                                  # wave drag for additional (assumed)                               

CDwv_total = CDwv_w + CDwv_v + CDwv_B + CDwv_add 


print("The wing CDwv is " + str(CDwv_w)) 
print("The tail CDwv is " + str(CDwv_v)) 
print("The fuselage CDwv is " + str(CDwv_B)) 
print("The total CDwv is " + str(CDwv_total)) 


# In[52]:



# ___________________________________ Lift Dependent Drag Calculations _______________________________ 

CL = 0.125  # CL = (L/(q*Sref))                                                          # Change as required 


def fw(x):                                                                              # defining function fw
    if x <= 0.178: 
        fwx = 0.0
    else:
        fwx = 0.4935 - 0.2382*x + 1.6306*(x**2) - 0.86*(x**3) + 0.2232*(x**4) - 0.0365*(x**5) - 0.5 
    return fwx 

Kw = (1+1/p)*fw(sigma_w)/(2*(sigma_w**2))

CDwl = (Sref/Sw)*(((beta**2)*p*s*Kw)/(math.pi*l))*(CL**2)                                 # calculating wave drag due to lift - assume CL to be a specific value



Kv = (1/2)*(1+1/p) 

CDv = (Sref/Sw)*(p*Kv/(math.pi*2*(s/l)))*(CL**2)                                          # calculating vortex drag due to lift - assume CL to be a specific value


print("The wing CDwl is " + str(CDwl)) 
print("The wing CDv is " + str(CDv)) 


