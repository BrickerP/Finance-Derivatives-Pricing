# -*- coding: utf-8 -*-

# -- Sheet --

import numpy as np
from scipy import optimize 
import matplotlib.pyplot as plt

r = 0.02 
R = 0.4 
premium1 = 0.01 
premium2 = 0.011 
premium3 = 0.012 
premium5 = 0.014 
P0 = 1
#Premium leg a cashflow of regular (usually quarterly) “insurance” premium payments, which continue until maturity or a credit event, such as default.
#Protection leg also called contingent leg. This leg pays at most once, when there is a credit event

# ### (a) Assume that hazard rate is piecewise-constant and bootstrap the CDS curve using the information above.


def p1(P1): 
    """
    We need contingent_leg = premium_leg, which means we want to find the zero point of contingent_leg - premium_leg
    """
    contingent_leg = premium1 / 2 * np.exp(-r*1.) * (P0 + P1)
    premium_leg = (1 - R) * np.exp(-r*1.) * (P0 - P1)
    return contingent_leg - premium_leg
P1 = optimize.root(p1, 0).x[0]
def p2(P2): 
    """
    We need contingent_leg = premium_leg, which means we want to find the zero point of contingent_leg - premium_leg
    """
    contingent_leg = premium2 / 2 * ( np.exp(-r*1.) * (P0 + P1) + np.exp(-r*2.) * (P1 + P2) )
    premium_leg = (1 - R) * ( np.exp(-r*1) * (P0 - P1) + np.exp(-r*2.) * (P1 - P2) )
    return contingent_leg - premium_leg
P2 = optimize.root(p2, 0).x[0]
def p3(P3): 
    """
    We need contingent_leg = premium_leg, which means we want to find the zero point of contingent_leg - premium_leg
    """
    contingent_leg = premium3 / 2 * ( np.exp(-r*1.) * (P0 + P1) + np.exp(-r*2.) * (P1 + P2) + np.exp(-r*3.) * (P2 + P3) )
    premium_leg = (1 - R) * ( np.exp(-r*1) * (P0 - P1) + np.exp(-r*2.) * (P1 - P2) + np.exp(-r*3.) * (P2 - P3))
    return contingent_leg - premium_leg
P3 = optimize.root(p3, 0).x[0]
def p5(P5): 
    """
    We need contingent_leg = premium_leg, which means we want to find the zero point of contingent_leg - premium_leg
    """
    contingent_leg = premium5 / 2 * ( np.exp(-r*1.) * (P0 + P1) + np.exp(-r*2.) * (P1 + P2) + np.exp(-r*3.) * \
    (P2 + P3) + 2 * np.exp(-r*5.) * (P3 + P5))
    premium_leg = (1 - R) * ( np.exp(-r*1) * (P0 - P1) + np.exp(-r*2.) * (P1 - P2) + np.exp(-r*3.) * (P2 - P3) + \
    np.exp(-r*5.) * (P3 - P5) )
    return contingent_leg - premium_leg
P5 = optimize.root(p5, 0).x[0]
def hazard_rate(P_tm_1, P_tm, tm_tm_1): # h(tm-1)
    return (np.log(P_tm_1) - np.log(P_tm)) / tm_tm_1

print(P0, P1, P2, P3, P5)
h0, h1, h2, h3 = hazard_rate(P0, P1, 1), hazard_rate(P1, P2, 1), hazard_rate(P2, P3, 1), hazard_rate(P3, P5, 2)
print(h0, h1, h2, h3)

# ### (b) What would be a fair spread for a 4y CDS, that starts today.


# log(P3)-log(P4) = h3 * 1
# P4 = exp(log(P3)-h3)
P4 = np.exp(np.log(P3) - h3)
def p4(premium4): 
    """
    We need contingent_leg = premium_leg, which means we want to find the zero point of contingent_leg - premium_leg
    """
    contingent_leg = premium4 / 2 * ( np.exp(-r*1.) * (P0 + P1) + np.exp(-r*2.) * (P1 + P2) + np.exp(-r*3.) * \
    (P2 + P3) + np.exp(-r*4.) * (P3 + P4))
    premium_leg = (1 - R) * ( np.exp(-r*1) * (P0 - P1) + np.exp(-r*2.) * (P1 - P2) + np.exp(-r*3.) * (P2 - P3) + \
    np.exp(-r*4.) * (P3 - P4))
    return contingent_leg - premium_leg
premium4 = optimize.root(p4, 0).x[0]
P4, premium4 * 10000

# ### (c) If you had bought a 5y CDS exactly one year ago with the contractual spread of 80bps, what would you charge me to buy it off you today.


premium5_0 = 0.008
RPV01_5 = 1/2 * (np.exp(-r*1) * (P0 + P1) + np.exp(-r*2.) * (P1 + P2) + np.exp(-r*3.) * (P2 + P3) + np.exp(-r*4.) * (P3 + P4))
# We say one year ago, the price of CDS is premium5_0 = 0.008, so premium5_1 = (premium5_1 - premium5_0)*RPV01_5
# We can find S(t) from contingent_leg and premium_leg equation.
def find(premium5_1):
    """
    let S(t) be the contractual spread of the contracts being issued at time t which have the same payment dates 
    as the remaining payment dates of our original contract.
    Here we need to calculate premium5_1, given premium5_0
    """
    contingent_leg = premium5_1 / 2 * (np.exp(-r*1) * (P0 + P1) + np.exp(-r*2.) * (P1 + P2) + np.exp(-r*3.) * (P2 + P3) + np.exp(-r*4.) * (P3 + P4))
    premium_leg = (1 - R) * (np.exp(-r*1) * (P0 - P1) + np.exp(-r*2.) * (P1 - P2) + np.exp(-r*3.) * (P2 - P3) + np.exp(-r*4.) * (P3 - P4))
    return contingent_leg - premium_leg
premium5_1 = optimize.root(find, 0).x[0]
(premium5_1 - premium5_0) * RPV01_5 * 10000



# ### (d) Working with the 4y CDS in (1.b), compute the dv01 of the CDS with respect to the CDS curve in Table 1.


#IR DV01 is an interest rate sensitivity measure.
#The price sensitivity with respect to h0, h1, h2, h3
#We first change h0
h0_ = h0 + 0.00001
P1_h0 = np.exp(np.log(P0) - h0_ * (1 - 0))
P2_h0 = np.exp(np.log(P1_h0) - h1 * (2 - 1))
P3_h0 = np.exp(np.log(P2_h0) - h2 * (3 - 2))
P4_h0 = np.exp(np.log(P3_h0) - h3 * (4 - 3))
premium_leg = (1 - R) * ( np.exp(-r*1.) * (P0 - P1_h0) + np.exp(-r*2.) * (P1_h0 - P2_h0) + \
                        np.exp(-r*3.) * (P2_h0 - P3_h0) + np.exp(-r*4.) * (P3_h0 - P4_h0)   )
RV = np.exp(-r*1.) * (P0 + P1_h0) + np.exp(-r*2.) * (P1_h0 + P2_h0) + np.exp(-r*3.) * (P2_h0 + P3_h0) + \
                        np.exp(-r*4.) * (P3_h0 + P4_h0)
premium4_h0 = 2 / RV * premium_leg
(premium4_h0 - premium4) * 10000

# h1 
h1_ = h1 + 0.00001
P1_h1 = P1
P2_h1 = np.exp(np.log(P1_h1) - h1_ * (2 - 1))
P3_h1 = np.exp(np.log(P2_h1) - h2 * (3 - 2))
P4_h1 = np.exp(np.log(P3_h1) - h3 * (4 - 3))
premium_leg = (1 - R) * ( np.exp(-r*1.) * (P0 - P1_h1) + np.exp(-r*2.) * (P1_h1 - P2_h1) + \
                        np.exp(-r*3.) * (P2_h1 - P3_h1) + np.exp(-r*4.) * (P3_h1 - P4_h1)   )
RV = np.exp(-r*1.) * (P0 + P1_h1) + np.exp(-r*2.) * (P1_h1 + P2_h1) + np.exp(-r*3.) * (P2_h1 + P3_h1) + \
                        np.exp(-r*4.) * (P3_h1 + P4_h1)
premium4_h1 = 2 / RV * premium_leg
(premium4_h1 - premium4) * 10000

# h2 
h2_ = h2 + 0.00001
P1_h2 = P1
P2_h2 = P2
P3_h2 = np.exp(np.log(P2_h2) - h2_ * (3 - 2))
P4_h2 = np.exp(np.log(P3_h2) - h3 * (4 - 3))
premium_leg = (1 - R) * ( np.exp(-r*1.) * (P0 - P1_h2) + np.exp(-r*2.) * (P1_h2 - P2_h2) + \
                        np.exp(-r*3.) * (P2_h2 - P3_h2) + np.exp(-r*4.) * (P3_h2 - P4_h2)   )
RV = np.exp(-r*1.) * (P0 + P1_h2) + np.exp(-r*2.) * (P1_h2 + P2_h2) + np.exp(-r*3.) * (P2_h2 + P3_h2) + \
                        np.exp(-r*4.) * (P3_h2 + P4_h2)
premium4_h2 = 2 / RV * premium_leg
(premium4_h2 - premium4) * 10000

# h3 
h3_ = h3 + 0.00001
P1_h3 = P1
P2_h3 = P2
P3_h3 = P3
P4_h3 = np.exp(np.log(P3_h3) - h3_ * (4 - 3))
premium_leg = (1 - R) * ( np.exp(-r*1.) * (P0 - P1_h3) + np.exp(-r*2.) * (P1_h3 - P2_h3) + \
                        np.exp(-r*3.) * (P2_h3 - P3_h3) + np.exp(-r*4.) * (P3_h3 - P4_h3)   )
RV = np.exp(-r*1.) * (P0 + P1_h3) + np.exp(-r*2.) * (P1_h3 + P2_h3) + np.exp(-r*3.) * (P2_h3 + P3_h3) + \
                        np.exp(-r*4.) * (P3_h3 + P4_h3)
premium4_h3 = 2 / RV * premium_leg
(premium4_h3 - premium4) * 10000

# ### (e) Compute the dv01 wrt the interest rate curve.


# We change r to r + 0.00001
r_r = r + 0.00001
premium_leg = (1-R) * ( np.exp(-r_r*1.) * (P0 - P1) + np.exp(-r_r*2.) * (P1 - P2) + np.exp(-r_r*3.) * (P2 - P3) + np.exp(-r_r*4.) * (P3 - P4))
RV = np.exp(-r_r*1.) * (P0 + P1) + np.exp(-r_r*2.) * (P1 + P2) + np.exp(-r_r*3.) * (P2 + P3) + np.exp(-r_r*4.) * (P3 + P4)
premium4_r = 2 / RV * premium_leg
(premium4_r - premium4) * 10000

# ### (f) Compute sensitivity wrt R.


# We change R to R + 0.00001
R_R = R + 0.00001
premium_leg = (1-R_R) * ( np.exp(-r*1.) * (P0 - P1) + np.exp(-r*2.) * (P1 - P2) + np.exp(-r*3.) * (P2 - P3) + np.exp(-r*4.) * (P3 - P4))
RV = np.exp(-r*1.) * (P0 + P1) + np.exp(-r*2.) * (P1 + P2) + np.exp(-r*3.) * (P2 + P3) + np.exp(-r*4.) * (P3 + P4)
premium4_r = 2 / RV * premium_leg
(premium4_r - premium4) * 10000

