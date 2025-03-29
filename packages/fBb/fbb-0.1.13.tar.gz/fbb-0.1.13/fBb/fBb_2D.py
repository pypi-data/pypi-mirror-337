#!/usr/bin/env python3

"""
An open source package to interpolate time series by multipoint fractional Brownian bridges 
url="https://github.com/fiddir/fBb"
license="MIT license"
"""

import numpy as np
from stochastic.processes.continuous import FractionalBrownianMotion

class SWF:
    def __init__(self, H, dx, dy, N_x, N_y, sigma=None): 
        self.H = H
        self.dx = dx
        self.dy = dy
        self.N_x = N_x
        self.N_y = N_y
        if sigma is None:
             self.sigma = 1. 
        else:
            self.sigma = sigma
        kx = np.linspace(0,N_x//2,N_x//2+1)
        ky = np.linspace(-N_y//2,N_y//2-1,N_y)
        self.KX,self.KY = np.meshgrid(kx, ky)
        self.K2 = np.square(self.KX)+np.square(self.KY)
        self.K2[N_x//2,0] = 1 #fix
        self.K = np.sqrt(self.K2)

    def field(self):
        random_phases_x = np.exp(1j*np.random.random_sample((self.N_y, self.N_x//2+1))*2*np.pi)
        random_phases_y = np.exp(1j*np.random.random_sample((self.N_y, self.N_x//2+1))*2*np.pi)
        u_hat = self.K**(-1./2-self.H)*(-random_phases_x*self.KY+ random_phases_y*self.KX)/self.K2
        v_hat = self.K**(-1./2-self.H)*(-random_phases_x*self.KX+ random_phases_y*self.KY)/self.K2
        u = np.fft.irfft2(np.fft.ifftshift(u_hat,0))
        v = np.fft.irfft2(np.fft.ifftshift(v_hat,0))
        return u, v

H=0.33; N_x=256; N_y=256; dx=1./N_x; dy=1./N_x
swf = SWF(H, dx, dy, N_x, N_y)
u, v = swf.field()

