# rectangular_prism model
# Note: model title and parameter table are inserted automatically
r"""

This model provides the form factor, *P(q)*, for a hollow rectangular
prism with infinitely thin walls. It computes only the 1D scattering, not the 2D.


Definition
----------

The 1D scattering intensity for this model is calculated according to the
equations given by Nayuk and Huber (Nayuk, 2012).

Assuming a hollow parallelepiped with infinitely thin walls, edge lengths
:math:`A \le B \le C` and presenting an orientation with respect to the
scattering vector given by |theta| and |phi|, where |theta| is the angle
between the *z* axis and the longest axis of the parallelepiped *C*, and
|phi| is the angle between the scattering vector (lying in the *xy* plane)
and the *y* axis, the form factor is given by

.. math::
  P(q) =  \frac{1}{V^2} \frac{2}{\pi} \int_0^{\frac{\pi}{2}}
  \int_0^{\frac{\pi}{2}} [A_L(q)+A_T(q)]^2 \sin\theta d\theta d\phi

where

.. math::
  V = 2AB + 2AC + 2BC

.. math::
  A_L(q) =  8 \times \frac{ \sin \bigl( q \frac{A}{2} \sin\phi \sin\theta \bigr)
                              \sin \bigl( q \frac{B}{2} \cos\phi \sin\theta \bigr)
                              \cos \bigl( q \frac{C}{2} \cos\theta \bigr) }
                            {q^2 \, \sin^2\theta \, \sin\phi \cos\phi}

.. math::
  A_T(q) =  A_F(q) \times \frac{2 \, \sin \bigl( q \frac{C}{2} \cos\theta \bigr)}{q \, \cos\theta}

and

.. math::
  A_F(q) =  4 \frac{ \cos \bigl( q \frac{A}{2} \sin\phi \sin\theta \bigr)
                       \sin \bigl( q \frac{B}{2} \cos\phi \sin\theta \bigr) }
                     {q \, \cos\phi \, \sin\theta} +
              4 \frac{ \sin \bigl( q \frac{A}{2} \sin\phi \sin\theta \bigr)
                       \cos \bigl( q \frac{B}{2} \cos\phi \sin\theta \bigr) }
                     {q \, \sin\phi \, \sin\theta}

The 1D scattering intensity is then calculated as

.. math::
  I(q) = \mbox{scale} \times V \times (\rho_{\mbox{p}} - \rho_{\mbox{solvent}})^2 \times P(q)

where *V* is the volume of the rectangular prism, :math:`\rho_{\mbox{p}}`
is the scattering length of the parallelepiped, :math:`\rho_{\mbox{solvent}}`
is the scattering length of the solvent, and (if the data are in absolute
units) *scale* represents the volume fraction (which is unitless).

**The 2D scattering intensity is not computed by this model.**


Validation
----------

Validation of the code was conducted  by qualitatively comparing the output
of the 1D model to the curves shown in (Nayuk, 2012).

REFERENCES

R Nayuk and K Huber, *Z. Phys. Chem.*, 226 (2012) 837-854

"""

from numpy import pi, inf, sqrt

name = "hollow_rectangular_prism_infinitely_thin_walls"
title = "Hollow rectangular parallelepiped with infinitely thin walls."
description = """
    I(q)= scale*V*(sld - solvent_sld)^2*P(q)+background
        with P(q) being the form factor corresponding to a hollow rectangular
        parallelepiped with infinitely thin walls.
"""
category = "shape:parallelepiped"

#             ["name", "units", default, [lower, upper], "type","description"],
parameters = [["sld", "1e-6/Ang^2", 6.3, [-inf, inf], "",
               "Parallelepiped scattering length density"],
              ["solvent_sld", "1e-6/Ang^2", 1, [-inf, inf], "",
               "Solvent scattering length density"],
              ["a_side", "Ang", 35, [0, inf], "volume",
               "Shorter side of the parallelepiped"],
              ["b2a_ratio", "Ang", 1, [0, inf], "volume",
               "Ratio sides b/a"],
              ["c2a_ratio", "Ang", 1, [0, inf], "volume",
               "Ratio sides c/a"],
             ]

source = ["lib/J1.c", "lib/gauss76.c", "hollow_rectangular_prism_infinitely_thin_walls.c"]

def ER(a_side, b2a_ratio, c2a_ratio):
    """
        Return equivalent radius (ER)
    """
    b_side = a_side * b2a_ratio
    c_side = a_side * c2a_ratio

    # surface average radius (rough approximation)
    surf_rad = sqrt(a_side * b_side / pi)

    ddd = 0.75 * surf_rad * (2 * surf_rad * c_side + (c_side + surf_rad) * (c_side + pi * surf_rad))
    return 0.5 * (ddd) ** (1. / 3.)

def VR(a_side, b2a_ratio, c2a_ratio):
    """
        Return shell volume and total volume
    """
    b_side = a_side * b2a_ratio
    c_side = a_side * c2a_ratio
    vol_total = a_side * b_side * c_side
    vol_shell = 2.0 * (a_side*b_side + a_side*c_side + b_side*c_side)
    return vol_shell, vol_total


# parameters for demo
demo = dict(scale=1, background=0,
            sld=6.3e-6, solvent_sld=1.0e-6,
            a_side=35, b2a_ratio=1, c2a_ratio=1,
            a_side_pd=0.1, a_side_pd_n=10,
            b2a_ratio_pd=0.1, b2a_ratio_pd_n=1,
            c2a_ratio_pd=0.1, c2a_ratio_pd_n=1)

# For testing against the old sasview models, include the converted parameter
# names and the target sasview model name.
oldname = 'RectangularHollowPrismInfThinWallsModel'
oldpars = dict(a_side='short_side', b2a_ratio='b2a_ratio', c_side='c2a_ratio',
               sld='sldPipe', solvent_sld='sldSolv')

tests = [[{}, 0.2, 0.836719188592],
         [{}, [0.2], [0.836719188592]],
        ]


