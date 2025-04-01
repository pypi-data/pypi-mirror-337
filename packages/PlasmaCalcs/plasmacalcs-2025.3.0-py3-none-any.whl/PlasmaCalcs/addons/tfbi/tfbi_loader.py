"""
File Purpose: loader for tfbi-related quantities
"""

from .tfbi_solver import TfbiSolver, _paramdocs_tfbi_solving
from ..addon_tools import register_addon_loader_if
from ...defaults import DEFAULTS
from ...errors import FluidValueError, InputMissingError
from ...quantities import QuantityLoader
from ...tools import (
    format_docstring,
    xarray_min,
)


''' --------------------- TfbiLoader --------------------- '''

@register_addon_loader_if(DEFAULTS.ADDONS.LOAD_TFBI)
@format_docstring(**_paramdocs_tfbi_solving)
class TfbiLoader(QuantityLoader):
    '''quantities related to the Thermal Farley Buneman Instability.
    
    NOTE: for simple calculations, consider using maindims_means=True!

    To solve TFBI theory, you can use the following pattern:
        {solving_pattern}
        
        Notes:
            {solving_pattern_notes}
    '''
    tfbi_solver_cls = TfbiSolver

    def tfbi_mask(self, *, kappae=1, ionfrac=1e-3, kappai=1, set=True):
        '''set & return self.mask appropriate for TFBI.
        kappae: None or number, default 1
            lower limit for kappae; mask points with kappae smaller than this value.
            (kappae = |qe| |B| / (me nuen))
            Internally, loaded as 'kappa' with fluid='e'.
            TFBI probably only matters when electrons are magnetized --> kappae >> 1.
            Applying TFBI theory to kappae masked points would still be fine,
                but will probably always say "instability doesn't grow there".
            None --> no mask on kappae
        ionfrac: None or number
            upper limit for ionfrac; mask points with ionfrac larger than this value.
            (ionfrac = ne / ntotal)
            Internally, loaded as 'SF_ionfrac' if available,
                else ne/(ne+n_neutral), with ne from self('n', fluid=self.fluids.get_electron()).
                (Note: checked in Bifrost: SF_ionfrac uses SF_n = sum of element densities.
                    SF_n does not include ne.
                    The formula SF_ionfrac = ne/(ne+nn) uses ne as a proxy for sum(ni),
                        which will be okay unless there are twice+ ionized species.)
            TFBI assumes weakly ionized.
            E_un0 also assumes weakly ionized, when self.assume_un='u'.
            Applying TFBI theory to ionfrac masked points would be a big issue,
                as it could lead to many false positives,
                where physical effects not included in the theory damp out the TFBI.
            None --> no mask on ionfrac.
        kappai: None or number, default 1
            upper limit for min kappai; mask points with all kappai larger than this value.
            (kappai = |qi| |B| / (mi nuin))
            Internally, loaded as 'kappa' with fluid=ions, then take min across fluids.
            TFBI probably only matters when at least 1 ion species is demagnetized --> kappai < 1.
            Applying TFBI theory to kappai masked points would still be fine,
                but will probably always say "instability doesn't grow there".
            None --> no mask on kappai.
        set: bool
            whether to set self.mask = result.
            if False, only returns the result, without also setting self.mask.
        '''
        if all(x is None for x in (kappae, ionfrac, kappai)):
            raise InputMissingError('At least one must be non-None: kappae, ionfrac, kappai.')
        with self.using(masking=False):
            if ionfrac is not None:
                if self.has_var('SF_ionfrac'):
                    ionfrac_vals = self('SF_ionfrac')
                else:
                    ne = self('n', fluid=self.fluids.get_electron())
                    nn = self('n_neutral')
                    ionfrac_vals = ne / (ne + nn)
            if kappae is not None:
                kappae_vals = self('kappa', fluid=self.fluids.get_electron())
            if kappai is not None:
                kappai_vals = self('kappa', fluid=self.fluids.ions())
                kappai_vals = xarray_min(kappai_vals, dim='fluid')
        mask = None
        if ionfrac is not None:
            mask_ionfrac = (ionfrac_vals > ionfrac)
            mask = mask_ionfrac if mask is None else (mask | mask_ionfrac)
        if kappae is not None:
            mask_kappae = (kappae_vals < kappae)
            mask = mask_kappae if mask is None else (mask | mask_kappae)
        if kappai is not None:
            mask_kappai = (kappai_vals > kappai)
            mask = mask_kappai if mask is None else (mask | mask_kappai)
        if set:
            self.mask = mask
            mask = self.mask  # <-- may have been altered slightly due to mask attr.
        return mask

    def tfbi_ds(self, ions=None, *, all=True, output_mask=True, **kw_get_var):
        '''returns Dataset of all the values needed & relevant to TFBI theory.
        Equivalent: self('tfbi_all', fluid=[electron, *ions], masking=True, ...)
        
        ions: None or specifier of multiple fluids (e.g. slice, or list of strs)
            list of ions to use. None --> self.fluids.ions()
        all: bool
            whether to include 'tfbi_all', or only 'tfbi_inputs'.
            With only 'tfbi_inputs', the theory is still solvable, but harder to inspect later.
        output_mask: bool
            whether to store_mask in results, if self.masking (and self.mask is not None)
        additional kwargs passed to self(...)
        '''
        if ions is None:
            ions = self.fluids.ions()
        fluid = [self.fluids.get_electron(), *ions]
        tfbi_var = 'tfbi_all' if all else 'tfbi_inputs'
        return self(tfbi_var, fluid=fluid, output_mask=output_mask, **kw_get_var)

    @format_docstring(tfbi_solver_docs=TfbiSolver.__doc__, sub_ntab=1)
    def tfbi_solver(self, ions=None, **kw_solver):
        '''return TfbiSolver object for solving TFBI theory based on values in self.
        all inputs here get passed to TfbiSolver. Equivalent: TfbiSolver(self, ...).

        docs for TfbiSolver copied below for convenience:
        -------------------------------------------------
        {tfbi_solver_docs}
        '''
        return self.tfbi_solver_cls(self, ions=ions, **kw_solver)

    # # # LOADING TFBI INPUTS & RELATED VARS # # #
    TFBI_VARS = ['mod_B', 'E_un0_perpmod_B', 'kB', 'T_n', 'm_n',  # "global" scalars
                    'm', 'nusn', 'skappa', 'eqperp_ldebye']  # scalars which depend on fluid.

    # extra vars, relevant to TFBI theory, but not necessary.
    TFBI_EXTRAS = ['SF_n', 'eps0', 'abs_qe', # "global" scalars
                    'n', 'n_n', 'eqperp_lmfp',
                    # 'tfbi_fscale_rel',  # this one turned out to be irrelevant --> exclude by default
                    ]   # scalars which depend on fluid.

    @known_var(deps=TFBI_VARS)
    def get_tfbi_inputs(self, **kw_get_vars):
        '''returns xarray.Dataset of values to input to the tfbi theory.
        "global" scalars (no dependence on component nor fluid)
            'mod_B': |magnetic field|
            'E_un0_perpmag_B': |E_un0 perp to B|. E_un0 = electric field in u_neutral=0 frame.
            'kB': boltzmann constant. kB * T = temperature in energy units.
            'T_n': temperature of neutrals.
            'm_n': mass of neutrals.
        scalars which depend on fluid. Note: checks self.fluid, not self.fluids.
            'm': mass of all non-neutral fluids
            'nusn': collision frequency between fluid and neutrals.
            'skappa': signed magnetization parameter; q |B| / (m nusn)
            'eqperp_ldebye': each fluid's debye length at its "equilibrium" temperature,
                        after considering zeroth order heating due to E_un0_perpmag_B.

        Results depend on self.fluid. May want to call as self('tfbi_inputs', fluid=CHARGED).
        '''
        if any(f.is_neutral() for f in self.iter_fluid()):
            errmsg = ('get_tfbi_inputs expects self.fluid to be charged fluids only,\n'
                      f'but it includes neutrals: {[f for f in self.iter_fluid() if f.is_neutral()]}')
            raise FluidValueError(errmsg)
        # [TODO][EFF] improve efficiency by avoiding redundant calculations,
        #    e.g. B is calculated separately for mod_B, E_un0_perpmag_B, and skappa,
        #    while E_un0 is calculated separately for E_un0_perpmag_B and eqperp_ldebye.
        tfbi_vars = self.TFBI_VARS
        return self(tfbi_vars, **kw_get_vars)

    @known_var(deps=TFBI_EXTRAS)
    def get_tfbi_extras(self, **kw_get_vars):
        '''returns xarray.Dataset of values relevant to TFBI theory but not necessary for inputs.
        Currently this just includes:
            'eqperp_lmfp': each fluid's collisional mean free path at its "equilibrium" temperature,
                        after considering zeroth order heating due to E_un0_perpmag_B.
            'SF_n': sum of number densities of all species (including neutrals)
            'n': number densities of each specie in self.fluid.
            'n_n': number density of neutral fluid.
            'n*kappa': number density times kappa.
                    TFBI dispersion relation terms scale with n*kappa for each fluid,
                    so this quantity roughly estimates the relative importance of each fluid.

        Results depend on self.fluid. May want to call as self('tfbi_extras', fluid=CHARGED).
        '''
        if any(f.is_neutral() for f in self.iter_fluid()):
            errmsg = ('get_tfbi_extras expects self.fluid to be charged fluids only,\n'
                      f'but it includes neutrals: {[f for f in self.iter_fluid() if f.is_neutral()]}')
            raise FluidValueError(errmsg)
        tfbi_extras = self.TFBI_EXTRAS
        kw_get_vars.setdefault('missing_vars', 'ignore')  # it's okay if some extras are un-gettable.
        return self(tfbi_extras, **kw_get_vars)

    @known_var(deps=['tfbi_inputs', 'tfbi_extras'])
    def get_tfbi_all(self, **kw_get_vars):
        '''returns xarray.Dataset of values relevant to TFBI theory.
        This includes tfbi_inputs (required for theory) and tfbi_extras (optional)

        Results depend on self.fluid. May want to call as self('tfbi_all', fluid=CHARGED).
        '''
        return self(['tfbi_inputs', 'tfbi_extras'], **kw_get_vars)

    @known_var(deps=['n*kappa'])
    def get_tfbi_fscale(self):
        '''tfbi_fscale = n * kappa
        tfbi dispersion relation sums terms proportional to n * kappa, for each fluid.
        '''
        return self('n*kappa')

    @known_var(deps=['tfbi_fscale'])
    def get_tfbi_fscale_rel(self):
        '''tfbi_fscale_rel = tfbi_fscale(this fluid) / tfbi_fscale(electrons).'''
        return self('tfbi_fscale') / self('tfbi_fscale', fluid=self.fluids.get_electron())

    # # # LOADING TFBI SOLUTION # # #
    @known_var(deps=['tfbi_inputs'])
    def get_tfbi_omega(self, *, kw_tfbi_solve=dict(), **kw_tfbi_solver):
        '''Thermal Farley Buneman Instability roots with largest imaginary part at each point in self.
        Equivalent: self.tfbi_solver(**kw_tfbi_solver).solve(**kw_solve)['omega'].

        Can provide kwargs, e.g. self('tfbi_omega', ions=['H_II', 'C_II'], kw_tfbi_solve=dict(ncpu=1)).

        For more control, use self.tfbi_solver() directly.
        For even more control, use the pattern described in help(self.tfbi_solver_cls).

        Recommended: consider using 'tfbi_omega_ds' instead of 'tfbi_omega'.
            'tfbi_omega_ds' gives the full Dataset of all values relevant to the solution.
            'tfbi_omega' just gives the DataArray of omega, which is harder to inspect later.
        '''
        kw_tfbi_solver.setdefault('tfbi_all', False)  # dropping ds0 later anyways so don't load it.
        solver = self.tfbi_solver(**kw_tfbi_solver)
        kw_tfbi_solve = kw_tfbi_solve.copy()
        kw_tfbi_solve.setdefault('return_ds', False)  # just return omega, not the full ds.
        # (if user specified return_ds=True, then they will get the full ds, but that's okay.)
        return solver(**kw_tfbi_solve)

    @known_var(deps=['tfbi_all'])
    def get_tfbi_omega_ds(self, *, kw_tfbi_solve=dict(), **kw_tfbi_solver):
        '''Thermal Farley Buneman Instability solution at each point in self.
        Equivalent: self.tfbi_solver(**kw_tfbi_solver).solve(**kw_solve).

        Can provide kwargs, e.g. self('tfbi_omega_ds', ions=['H_II', 'C_II'], kw_tfbi_solve=dict(ncpu=1)).

        For more control, use self.tfbi_solver() directly.
        For even more control, use the pattern described in help(self.tfbi_solver_cls).
        '''
        kw_tfbi_solver.setdefault('tfbi_all', True)
        solver = self.tfbi_solver(**kw_tfbi_solver)
        return solver(**kw_tfbi_solve)


    # # # --- SETTING VALUES; KNOWN SETTERS --- # # #
    # used when using set_var.

    @known_setter(aliases=['mag_B'])
    def set_mod_B(self, value, **kw):
        '''set mod_B to this value. Also sets mag_B, mod2_B, and mag2_B.'''
        # [TODO] pattern handling for setters, for mod; see issue #5 on git for more info.
        #   (implementing pattern handling should make this function obsolete / mostly obsolete.)
        self.set_var_internal('mod_B', value, ['snap'], **kw, ukey='b_field')
        self.set_var_internal('mag_B', value, ['snap'], **kw, ukey='b_field')
        value2 = value**2
        self.set_var_internal('mod2_B', value2, ['snap'], **kw, ukey='b_field2')
        self.set_var_internal('mag2_B', value2, ['snap'], **kw, ukey='b_field2')

    @known_setter(aliases=['E_un0_perpmag_B'])
    def set_E_un0_perpmod_B(self, value, **kw):
        '''set E_un0_perpmod_B to this value. Also sets E_un0_perpmag_B.'''
        self.set_var_internal('E_un0_perpmag_B', value, ['snap'], **kw, ukey='e_field')
        self.set_var_internal('E_un0_perpmod_B', value, ['snap'], **kw, ukey='e_field')
