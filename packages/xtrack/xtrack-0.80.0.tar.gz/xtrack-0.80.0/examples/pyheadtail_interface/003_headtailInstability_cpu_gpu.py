# copyright ############################### #
# This file is part of the Xtrack Package.  #
# Copyright (c) CERN, 2021.                 #
# ######################################### #

import time
import numpy as np
from scipy import constants

protonMass = constants.value("proton mass energy equivalent in MeV") * 1e6
from scipy.stats import linregress
from scipy.signal import hilbert
from matplotlib import pyplot as plt
plt.close('all')

import xobjects as xo
import xtrack as xt
xt.enable_pyheadtail_interface()

from PyHEADTAIL.particles.generators import generate_Gaussian6DTwiss
from PyHEADTAIL.particles.slicing import UniformBinSlicer
from PyHEADTAIL.impedances.wakes import WakeTable, WakeField
from PyHEADTAIL.feedback.transverse_damper import TransverseDamper
from PyHEADTAIL.trackers.transverse_tracking import TransverseSegmentMap
from PyHEADTAIL.trackers.longitudinal_tracking import LinearMap
from PyHEADTAIL.trackers.detuners import ChromaticitySegment, AmplitudeDetuningSegment

context = xo.ContextCupy()

nTurn = 5000  # int(1E4)
bunch_intensity = 1.8e11
n_macroparticles = int(1e4)
energy = 7e3  # [GeV]
gamma = energy * 1e9 / protonMass
betar = np.sqrt(1 - 1 / gamma ** 2)
normemit = 1.8e-6
beta_x = 68.9
beta_y = 70.34
Q_x = 0.31
Q_y = 0.32
chroma = -5.0  # 10.0
sigma_4t = 1.2e-9
sigma_z = sigma_4t / 4.0 * constants.c
momentumCompaction = 3.483575072011584e-04
eta = momentumCompaction - 1.0 / gamma ** 2
voltage = 12.0e6
h = 35640
p0 = constants.m_p * betar * gamma * constants.c
Q_s = np.sqrt(constants.e * voltage * eta * h / (2 * np.pi * betar * constants.c * p0))
circumference = 26658.883199999
averageRadius = circumference / (2 * np.pi)
sigma_delta = Q_s * sigma_z / (averageRadius * eta)
beta_s = sigma_z / sigma_delta
emit_s = 4 * np.pi * sigma_z * sigma_delta * p0 / constants.e  # eVs for PyHEADTAIL

n_slices_wakes = 200
limit_z = 3 * sigma_z
wakefile = "wakes/wakeforhdtl_PyZbase_Allthemachine_7000GeV_B1_2021_TeleIndex1_wake.dat"
slicer_for_wakefields = UniformBinSlicer(n_slices_wakes, z_cuts=(-limit_z, limit_z))
waketable = WakeTable(
    wakefile, ["time", "dipole_x", "dipole_y", "quadrupole_x", "quadrupole_y"]
)
wake_field = WakeField(slicer_for_wakefields, waketable)
wake_field.needs_cpu = True
wake_field.needs_hidden_lost_particles = True

damping_time = 7000  # 33.
damper = TransverseDamper(dampingrate_x=damping_time, dampingrate_y=damping_time)
damper.needs_cpu = True
damper.needs_hidden_lost_particles = True
i_oct = 15.
det_xx = 1.4e5 * i_oct / 550.0  # from PTC with ATS optics, telescopic factor 1.0
det_xy = -1.0e5 * i_oct / 550.0

# expected octupole threshold with damper is 273A according to https://indico.cern.ch/event/902528/contributions/3798807/attachments/2010534/3359300/20200327_RunIII_stability_NMounet.pdf
# expected growth rate with damper but without octupole is ~0.3 [$10^{-4}$/turn] (also according to Nicolas' presentation)

checkTurn = 1000

########### PyHEADTAIL part ##############

particles = generate_Gaussian6DTwiss(
    macroparticlenumber=n_macroparticles,
    intensity=bunch_intensity,
    charge=constants.e,
    mass=constants.m_p,
    circumference=circumference,
    gamma=gamma,
    alpha_x=0.0,
    alpha_y=0.0,
    beta_x=beta_x,
    beta_y=beta_y,
    beta_z=beta_s,
    epsn_x=normemit,
    epsn_y=normemit,
    epsn_z=emit_s,
)

x0 = np.copy(particles.x)
px0 = np.copy(particles.xp)
y0 = np.copy(particles.y)
py0 = np.copy(particles.yp)
zeta0 = np.copy(particles.z)
delta0 = np.copy(particles.dp)

chromatic_detuner = ChromaticitySegment(dQp_x=chroma, dQp_y=0.0)
transverse_detuner = AmplitudeDetuningSegment(
    dapp_x=det_xx * p0,
    dapp_y=det_xx * p0,
    dapp_xy=det_xy * p0,
    dapp_yx=det_xy * p0,
    alpha_x=0.0,
    beta_x=beta_x,
    alpha_y=0.0,
    beta_y=beta_y,
)
arc_transverse = TransverseSegmentMap(
    alpha_x_s0=0.0,
    beta_x_s0=beta_x,
    D_x_s0=0.0,
    alpha_x_s1=0.0,
    beta_x_s1=beta_x,
    D_x_s1=0.0,
    alpha_y_s0=0.0,
    beta_y_s0=beta_y,
    D_y_s0=0.0,
    alpha_y_s1=0.0,
    beta_y_s1=beta_y,
    D_y_s1=0.0,
    dQ_x=Q_x,
    dQ_y=Q_y,
    segment_detuners=[chromatic_detuner, transverse_detuner],
)
arc_longitudinal = LinearMap(
    alpha_array=[momentumCompaction], circumference=circumference, Q_s=Q_s
)

turns = np.arange(nTurn)
x = np.zeros(nTurn, dtype=float)
t_pyht_start = time.time()
for turn in range(nTurn):
    time0 = time.time()
    arc_transverse.track(particles)
    arc_longitudinal.track(particles)
    time1 = time.time()
    wake_field.track(particles)
    time2 = time.time()
    damper.track(particles)
    time3 = time.time()
    x[turn] = np.mean(particles.x)
    if turn % 1000 == 0:
        print(
            f"PyHt - turn {turn}: time for arc {time1-time0}s, for wake {time2-time1}s, for damper {time3-time2}s"
        )
t_pyht_end = time.time()
print(f'PyHT full loop: {t_pyht_end - t_pyht_start}s')

x /= np.sqrt(normemit * beta_x / gamma / betar)
plt.figure(0)
plt.plot(turns, x, label=f"{i_oct}A")
iMin = 1000
iMax = nTurn - 1000
if iMin >= iMax:
    iMin = 0
    iMax = nTurn
ampl = np.abs(hilbert(x))
b, a, r, p, stderr = linregress(turns[iMin:iMax], np.log(ampl[iMin:iMax]))
gr_pyht = b
plt.plot(turns, np.exp(a + b * turns), "--k", label=f"{1/b:.3E} turns")
print(f"Growth rate {b*1E4} [$10^{-4}$/turn]")
plt.title("PyHEADTAIL")
plt.legend(loc="upper left")
plt.xlabel("Turn")
plt.ylabel("x [$\sigma_x$]")

p_pht = particles

############ xsuite-PyHEADTAIL part (the WakeField instance is shared) ########################

particles = xt.Particles(
    _context=context,
    circumference=circumference,
    particlenumber_per_mp=bunch_intensity / n_macroparticles,
    q0=1,
    mass0=protonMass,
    gamma0=gamma,
    x=np.zeros(2*len(x0))
)

np2ctx = context.nparray_to_context_array
particles.x[::2] = np2ctx(x0)
particles.px[::2] = np2ctx(px0)
particles.y[::2] = np2ctx(y0)
particles.py[::2] = np2ctx(py0)
particles.zeta[::2] = np2ctx(zeta0)
particles.delta[::2] = np2ctx(delta0)
particles.state[1::2] = 0

#particles.x[:10000] = x0
#particles.px[:10000] = px0
#particles.y[:10000] = y0
#particles.py[:10000] = py0
#particles.zeta[:10000] = zeta0
#particles.delta[:10000] = delta0
#particles.state[10000:] = 0


arc = xt.LineSegmentMap(
    _context=context,
    betx=beta_x,
    bety=beta_y,
    qx=Q_x,
    qy=Q_y,
    bets=beta_s,
    qs=Q_s,
    dqx=chroma,
    det_xx=det_xx,
    det_xy=det_xy,
    det_yy=det_xx,
    det_yx=det_xy,
    energy_ref_increment=0.0,
    energy_increment=0,
)


line = xt.Line(elements=[arc, wake_field, damper],
                   element_names=['arc', 'wake_field', 'damper'])
line.build_tracker(_context=context)

t_xt_start = time.time()
turns = np.arange(nTurn)
x = np.zeros(nTurn, dtype=float)
for turn in range(nTurn):

    line.track(particles)

    x[turn] = np.average(particles.x[particles.state>0])
    if turn % 1000 == 0:
        print(
            f"PyHtXt - turn {turn}")
t_xt_end = time.time()

print(f'Xt full loop: {t_xt_end - t_xt_start}s')

x /= np.sqrt(normemit * beta_x / gamma / betar)
plt.figure(1)
plt.plot(turns, x, label=f"{i_oct}A")
iMin = 1000
iMax = nTurn - 1000
if iMin >= iMax:
    iMin = 0
    iMax = nTurn
ampl = np.abs(hilbert(x))
b, a, r, p, stderr = linregress(turns[iMin:iMax], np.log(ampl[iMin:iMax]))
gr_xtpyht = b
plt.plot(turns, np.exp(a + b * turns), "--k", label=f"{1/b:.3E} turns")
print(f"Growth rate {b*1E4} [$10^{-4}$/turn]")
plt.title("xsuite-PyHEADTAIL")
plt.legend(loc="upper left")
plt.xlabel("Turn")
plt.ylabel("x [$\sigma_x$]")

print(f'{gr_pyht=}, {gr_xtpyht=} {gr_pyht-gr_xtpyht=}')
plt.show()
assert np.isclose(gr_xtpyht, gr_pyht, rtol=1e-3, atol=1e-100)

