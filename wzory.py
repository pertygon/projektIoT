import numpy as np
#stale
epsilon0 = 8.85e-14
pi = np.pi
#wzory
def Rho(Rp):
    return 1/Rp
def cip(rho,l,S):
    return ((rho*l)/S)
def cpp(rho,d,Pk):
    return ((rho*d)/Pk)
def wsplKonduktywnosci(sigma,f):
    return (np.log(sigma)/np.log(f))
def rSkladowaPrzenikalnosci(Cp,C0):
    return Cp/C0
def C0(A,d):
    return (epsilon0*(A/d))
def iSkladowaPrzenikalnosci(sigma,omega):
    return (sigma/(epsilon0*omega))
def omega(f):
    return 2*pi*f