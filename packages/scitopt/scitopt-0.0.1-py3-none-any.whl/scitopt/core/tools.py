import numpy as np


def dE_drho_simp(rho, E0, Emin, p):
    """
    Derivative of SIMP-style E(rho)
    E(rho) = Emin + (E0 - Emin) * rho^p
    """
    return p * (E0 - Emin) * np.maximum(rho, 1e-6) ** (p - 1)


def dC_drho_simp(rho, strain_energy, E0, Emin, p):
    """
    dC/drho = -p * (E0 - Emin) * rho^(p - 1) * strain_energy
    """
    # dE_drho = p * (E0 - Emin) * np.maximum(rho, 1e-6) ** (p - 1)
    dE_drho = dE_drho_simp(rho, E0, Emin, p)
    return - dE_drho * strain_energy


# def dE_drho_rationalSIMP(rho, E0, Emin, p):
def dE_drho_ramp(rho, E0, Emin, p):
    """
    Derivative of Rational SIMP-style E(rho)
    E(rho) = Emin + (E0 - Emin) * rho / (1 + p * (1 - rho))
    """
    denom = 1.0 + p * (1.0 - rho)
    return (E0 - Emin) * (denom - p * rho) / (denom ** 2)


def dC_drho_ramp(rho, strain_energy, E0, Emin, p):
    dE_drho = dE_drho_ramp(rho, E0, Emin, p)
    return - dE_drho * strain_energy


def heaviside_projection(rho, beta, eta=0.5):
    """
    Smooth Heaviside projection.
    Returns projected density in [0,1].
    """
    numerator = np.tanh(beta * eta) + np.tanh(beta * (rho - eta))
    denominator = np.tanh(beta * eta) + np.tanh(beta * (1.0 - eta))
    return numerator / (denominator + 1e-12)


def heaviside_projection_derivative(rho, beta, eta=0.5):
    """
    Derivative of the smooth Heaviside projection w.r.t. rho.
    d/d(rho)[heaviside_projection(rho)].
    """
    # y = tanh( beta*(rho-eta) )
    # dy/d(rho) = beta*sech^2( ... )
    # factor from normalization
    numerator = beta * (1.0 - np.tanh(beta*(rho - eta))**2)
    denominator = np.tanh(beta*eta) + np.tanh(beta*(1.0 - eta))
    return numerator / (denominator + 1e-12)
