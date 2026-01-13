from cpymad.madx import Madx
import xtrack as xt

mad = Madx()
mad.input(
    '''
    ! Get the toolkit
    call,file="macro.madx";
    call,file="lhc.seq";

    !Install HL-LHC
    call, file="hllhc_sequence.madx";

    ! Install crab cavities (they are off)
    call, file='enable_crabcavities.madx';
    on_crab1 = 0;
    on_crab5 = 0;

    beam, sequence=lhcb1, particle=proton, pc=7000;
    beam, sequence=lhcb2, particle=proton, pc=7000, bv=-1;

    set, format="12d", "-18.12e", "25s";
    save, file="temp_lhc_thick.seq";

    ''')

env = xt.load('temp_lhc_thick.seq', s_tol=1e-6,
              _rbend_correct_k0=True, # LHC sequences are defined with rbarc=False
              reverse_lines=['lhcb2'])


env.lhcb1.twiss_default['method'] = '4d'
env.lhcb2.twiss_default['method'] = '4d'
env.lhcb2.twiss_default['reverse'] = True

env.to_json('lhc.json')
