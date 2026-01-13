# TODO:
# no 4d in the defaults --> use twiss4d/twiss6d methods
# search closed orbit where?
# models integrators
# cycle to ip7?
# how to set octupoles
# experimental magnets
# crabs from the beginning?, no correctors?


import xtrack as xt

# Load lattice
lhc = xt.load('lhc.json')

# Load optics
lhc.vars.load('opt_round_150_1500.madx')

# Cycle
lhc.b1.cycle('ip3')
lhc.b2.cycle('ip3')

# Reference particles
lhc.b1.set_particle_ref('proton', p0c=7000e9)
lhc.b2.set_particle_ref('proton', p0c=7000e9)

# Twiss
twb1 = lhc.b1.twiss4d()
twb2 = lhc.b2.twiss4d()

opt_chrom = lhc.b1.match(
    solve=False,
    method='4d',
    vary=xt.VaryList(['ksf.b1', 'ksd.b1'], step=1e-4),
    targets=xt.TargetSet(dqx=20, dqy=20, tol=1e-4),
)
opt_chrom.solve()


bump_settings = dict(
    on_x1=250,            # [urad]
    on_sep1=0,            # [mm]
    on_x2=-170,           # [urad]
    on_sep2=0.138,        # [mm]
    on_x5=250,            # [urad]
    on_sep5=0,            # [mm]
    on_x8=-250,           # [urad]
    on_sep8=-0.043,       # [mm]
    on_disp=1,            # Value to choose could be optics-dependent
)

lhc.vars.update(bump_settings)

# Sextupolar error in on one of the inner triplet quadrupoles
# (to have some feed-down on the orbit)
lhc['mqxfa.a3l5/lhcb1'].knl[2] = 0.0002
lhc['mqxfa.a3l1/lhcb1'].knl[2] = 0.0002
lhc['mqxfa.a3r1/lhcb1'].knl[2] = -0.0002
lhc['mqxfa.a3r5/lhcb1'].knl[2] = -0.0002
