import math
import random


def scatter_photon(mcx,with_print=False):
    g = mcx.tis_g
    if g == 0:
        theta_cos = 2.0 * random.random() - 1.0
    else:
        temp = (1.0 - g * g) / (1.0 - g + 2 * g * random.random())
        theta_cos = (1.0 + g * g - temp * temp) / (2.0 * g)
    theta_sin = math.sqrt(1.0 - theta_cos * theta_cos)
    # Sample psi
    psi = 2.0 * math.pi * random.random()
    psi_cos = math.cos(psi)
    if psi < math.pi:
        psi_sin = math.sqrt(1.0 - psi_cos * psi_cos)
    else:
        psi_sin = -math.sqrt(1.0 - psi_cos * psi_cos)
    # New trajectory
    u_x,u_y,u_z = mcx.pho_u
    # u_x * u_x + u_y * u_y + u_z * u_z
    if (1 - math.fabs(u_z)) <= 1e-12:
        new_ux = theta_sin * psi_cos
        new_uy = theta_sin * psi_sin
        if u_z >= 0:
            new_uz = theta_cos
        else:
            new_uz = - theta_cos
    else:
        temp = math.sqrt(1.0-u_z*u_z)
        new_ux = theta_sin*(u_x * u_z * psi_cos - u_y * psi_sin) / temp + u_x * theta_cos
        new_uy = theta_sin*(u_y * u_z * psi_cos - u_x * psi_sin) / temp + u_y * theta_cos
        new_uz = -theta_sin*psi_cos*temp + u_z*theta_cos

    adjust = new_ux*new_ux + new_uy*new_uy + new_uz*new_uz
    if math.fabs(adjust-1) > 0.001:
        if with_print:
            print("原来这里平方和不为1吗？ {}".format(adjust))
        adjust_sqrt = math.sqrt(adjust)
        new_ux = new_ux/adjust_sqrt
        new_uy = new_uy/adjust_sqrt
        new_uz = new_uz/adjust_sqrt
        adjust = new_ux*new_ux + new_uy*new_uy + new_uz*new_uz
        if with_print:
            print("调整至当前平方和 {}".format(adjust))
    mcx.pho_u[0] = new_ux
    mcx.pho_u[1] = new_uy
    mcx.pho_u[2] = new_uz
    return mcx


def roulette(mcx):
    THRESHOLD, CHANCE = 0.01, 0.1
    if mcx.photon_w < THRESHOLD:
        if random.random() <= CHANCE:
            mcx.photon_w /= CHANCE
        else:
            mcx.photon_status = False
    return mcx