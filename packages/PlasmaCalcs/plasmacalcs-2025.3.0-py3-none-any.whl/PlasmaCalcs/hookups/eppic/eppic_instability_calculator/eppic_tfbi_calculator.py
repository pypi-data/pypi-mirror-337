"""
File Purpose: EppicInstabilityCalculator with tfbi-specific methods
"""


from .eppic_instability_calculator import EppicInstabilityCalculator

from ....dimensions import ELECTRON
from ....tools import xarray_grid


class EppicTfbiCalculator(EppicInstabilityCalculator):
    '''EppicInstabilityCalculator with tfbi-specific methods.
    [TODO] some of these are generic enough to [MV] to a TfbiCalculator parent,
        if ever wanting to use a non-Eppic TfbiCalculator.
        E.g., with_chargesep_e_scaling could work for any TfbiCalculator.
    '''

    def chargesep_e_scaling(self, N=24, *, safety=0.1, name='n_mul'):
        '''returns xarray_grid of n_mul from 1 to safety * ne_at_wplasma_eq_nusn / ne.
        (Implementation assumes ne > ne_at_wplasma_eq_nusn; will crash otherwise.)

        n_at_wplasma_eq_nusn = epsilon0 nusn^2 m / q^2,
            and has aliases rosenberg_n, n_at_lmfp_eq_ldebye.

        (result * ne) spans (evenly in logspace) from ne to ne_at_wplasma_eq_nusn.

        N: int
            number of points in result
        name: str
            name of resulting array and coordinate.
        safety: number, probably less than 1
            safety factor for the range of n_mul.
            smaller safety is MORE safe (extending the search into more drastic n_mul).
        '''
        ne = self('n', fluid=ELECTRON)
        ne_at_wplasma_eq_nusn = self('n_at_wplasma_eq_nusn', fluid=ELECTRON)
        rat = ne_at_wplasma_eq_nusn/ne
        if rat.size == 1:     # if rat can be converted to a single scalar, do that,
            rat = rat.item()  #   to avoid using array_lims mode (which includes 'n_mul_dim').
        result = xarray_grid(safety*rat, 1, N, name=name, logspace=True, reverse=True)
        return result

    def with_chargesep_e_scaling(self, N=24, safety=0.1, **kw_init):
        '''returns self with_scaling all n by grid from 1 to safety * ne_at_wplasma_eq_nusn / ne.
        solve tfbi across result to evaluate the "okay-ness" of scaling all number densities.
        At some point in this range, will probably see significant changes in tfbi solution.

        smaller safety is MORE safe (extending the search into more drastic n_mul).

        Equivalent: self.with_scaling({'n': self.chargesep_e_scaling(...)})
        '''
        chargesep_e_scaling = self.chargesep_e_scaling(N, safety=safety, name='n_mul')
        return self.with_scaling({'n': chargesep_e_scaling}, **kw_init)
