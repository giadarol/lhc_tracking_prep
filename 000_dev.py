# TODO:
# no 4d in the defaults --> use twiss4d/twiss6d methods
# search closed orbit where?
# models integrators
# cycle to ip7?
# how to set octupoles
# experimental magnets
# crabs from the beginning?, no correctors?
# orbit correction strategy: in the past we had a reference machine with expressions
# only on the correctors (was robust!).


import xtrack as xt
import xdeps as xd

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

# Build a reference models
lhc_ref = lhc.copy() # deep copy
lhc_ref._var_management = None
lhc_ref._init_var_management() # kills all knobs on the elements
lhc_ref.vars.default_to_zero = True
lhc_ref.vars.update(lhc.vars.get_table().to_dict()) # transfer all knobs (no effect on the lattice)
tt_ref = lhc_ref.elements.get_table()
tt_correctors = tt_ref.rows.match(name='mcb.*')

formatter = xd.refs.CompactFormatter(scope=None)
for nn in tt_correctors.name:
    if hasattr(lhc_ref[nn], 'knl'):
        expr_knl = lhc.ref[nn].knl[0]._expr
        if expr_knl is not None:
            lhc_ref[nn].knl[0] = expr_knl._formatted(formatter)
    if hasattr(lhc_ref[nn], 'ksl'):
        expr_ksl = lhc.ref[nn].ksl[0]._expr
        if expr_ksl is not None:
            lhc_ref[nn].ksl[0] = expr_ksl._formatted(formatter)

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

# Transfer selected knobs to reference lattice
tt_vars = lhc.vars.get_table()
tt_ref = tt_vars.rows['on_sep.*|on_x.*|on_a.*|on_o.*']


