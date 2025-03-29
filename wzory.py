import numpy as np
#stale
epsilon0 = 8.85e-12
pi = np.pi
#wzory
def Rho(Rp):
    return 1/Rp
def cip(Rp,S,l):
    return (l*1e-2)/(Rp*S*1e-4)
def cpp(Rp,d,Pk):
    return  (d*1e-2)/(Rp*Pk*1e-4)
def wsplKonduktywnosci(sigma,f):
    return (np.log1p(sigma)/np.log1p(f))
def rSkladowaPrzenikalnosci(Cp,C0):
    return Cp/C0
def C0(A,d):
    return epsilon0*((A*1e-4)/(d*1e-2))
def iSkladowaPrzenikalnosci(sigma,omega):
    return (sigma/(epsilon0*omega))
def omega(f):
    return 2*pi*f