"""Determine machine-specific parameters affecting floating-point arithmetic.

Function to determine machine-specific parameters affecting
floating-point arithmetic.

* This is build after "NUMERICAL RECIPES in C", second edition,
  Reprinted 1996, pp.  889.
"""

from __future__ import annotations

import math

DEFAULT_RADIX = 2


def machar() -> dict[str, float | int]:  # noqa:PLR0915,PLR0912,C901
    """Determine and returns machine-spec. paras affecting floating-point arithmetic.

    Returns
    -------
      dict: Values in result dictionary are:

      ``ibeta`` (int)
        The radix in which numbers are represented, almost
        always 2, but occasionally 16, or even 10
      ``it`` (int)
        The number of base-``ibeta`` digits in the floating point
        mantissa
      ``machep`` (int)
        Is the exponent of the smallest (most negative) power if ``ibeta``
        that, added to 1.0 gives something different from 1.0.
      ``eps`` (float)
        Is the floating-point number ``ibeta`` ** ``machdep``, loosly
        referred to as the *floating-point precision*.
      ``negep`` (int)
        Is the exponenet of the smalles power of ``ibeta`` that, subtracted from
        1.0, gives something different from 1.0.
      ``epsneg`` (float)
        Is ``ibeta`` ** ``negep``, another way of defining floating-point precision.
        Not infrequently ``epsneg`` is 0.5 times ``eps``; occasionally ``eps`` and
        ``epsneg`` are equal.
      ``iexp`` (int)
        Is the number of bits in the exponent (including its sign or bias)
      ``minexp`` (int)
        Is the smallest (most negative) power if ``ibeta`` consistent with there no
        leading zeros in the mantissa.
      ``xmin`` (float)
        Is the floating-point number ``ibeta`` ** ``minexp``, generally the smallest
        (in magnitude) usable floating value
      ``maxexp`` (int)
        Is the smallest (positive) power of ``ibeta`` that causes overflow.
      ``xmax`` (float)
        Is (1 - ``epsneg``) x ``ibeta`` ** ``maxexp``, generally the largest (in
        magnitude) usable floating value.
      ``irnd`` (int)
        Returns a code in the range 0...5, giving information on what kind of rounding
        is done in addition, and on how underflow is handled.

        If ``irnd`` returns 2 or 5, then your computer is compilant with the IEEE
        standard for rounding. If it returns 1 or 4, then it is doing some kind of
        rounding, but not the IEEE standard. If ``irnd`` returns 0 or 3, then it is
        truncating the result, not rounding it.
      ``ngrd`` (int)
        Is the number of *guard digits* used when truncating the product of two
        mantissas to fit the representation

    This is taken from "NUMERICAL RECIPES in C", second edition,
    Reprinted 1996.
    """
    one = float(1)
    two = one + one
    zero = one - one
    # Determine ``ibeta`` and ``beta`` by the method of M. Malcom.
    a = temp1 = one
    while temp1 - one == zero:
        a += a
        temp = a + one
        temp1 = temp - a
    b = one
    itemp = 0
    while itemp == 0:
        b += b
        temp = a + b
        itemp = int(temp - a)
    ibeta = itemp
    beta = float(ibeta)
    # Determine ``it`` and ``irnd``.
    it = 0
    b = temp1 = one
    while temp1 - one == zero:
        it = it + 1
        b = beta * b
        temp = b + one
        temp1 = temp - b
    irnd = 0
    betah = beta / two
    temp = a + betah
    if temp - a != zero:
        irnd = 1
    tempa = a + beta
    temp = tempa + betah
    if irnd == 0 and temp - tempa != zero:
        irnd = 2
    # Determine ``negep`` und ``epsneg``.
    negep = it + 3
    betain = one / beta
    a = one
    i = 1
    while i <= negep:
        i = i + 1
        a = betain * a
    b = a
    while 1:
        temp = one - a
        if temp - one != zero:
            break
        a = beta * a
        negep = negep - 1
    negep = -negep
    epsneg = a
    # Determine ``machdep`` and ``eps``.
    machdep = -it - 3
    a = b
    while 1:
        temp = one + a
        if temp - one != zero:
            break
        a = a * beta
        machdep = machdep + 1
    eps = a
    # Deterrmine ``ngrd``.
    ngrd = 0
    temp = one + eps
    if irnd == 0 and temp * one - one != zero:
        ngrd = 1
    # Determine ``iexp``.
    i = 0
    k = 1
    z = betain
    t = one + eps
    nxres = 0
    while 1:  # Loop until underflow ocurs, then exit.
        y = z
        z = y * y
        a = z * one  # check for underflow
        temp = z * t
        if a + a == zero or math.fabs(z) >= y:
            break
        temp1 = temp * betain
        if temp1 * beta == z:
            break
        i = i + 1
        k = k + k
    if ibeta != 10:  # noqa:PLR2004
        iexp = i + 1
        mx = k + k
    else:  # For decimal machines only
        iexp = i + i
        iz = ibeta
        while k >= iz:
            iz = ibeta * iz
            iexp = iexp + 1
        mx = iz + iz - 1
    # To determine ``minexp`` and ``xmin``, loop until an underflow
    # occurs, then exit.
    while True:
        xmin = y
        y = betain * y
        a = y * one  # Check here for the underflow
        temp = y * t
        if a + a != zero or math.fabs(y) < xmin:
            k = k + 1
            temp1 = temp * betain
            if temp1 * beta == y and temp != y:
                nxres = 3
                xmin = y
                break
        else:
            break
    minexp = -k
    # Determine maxexp, xmax.
    if mx <= k + k + 3 and ibeta != 10:  # noqa:PLR2004
        mx = mx + mx
        iexp = iexp + 1
    maxexp = mx + minexp
    irnd = nxres + irnd  # Adjust ``irnd`` to reflect partial underflow
    if irnd >= 2:  # noqa:PLR2004
        maxexp = maxexp - 2  # Adjust for IEEE-stype machines
    i = maxexp + minexp
    # Adjust for machines with implicit leading bit in binary mantissa,
    # and machines with radix point at extreme right of mantissa.
    if ibeta == DEFAULT_RADIX and not i:
        maxexp = maxexp - 1
    if i > 20:  # noqa:PLR2004
        maxexp = maxexp - 1
    if a != y:
        maxexp = maxexp - 2
    xmax = one - epsneg
    if xmax * one != xmax:
        xmax = one - beta * epsneg
    xmax = xmax / (xmin * beta * beta * beta)
    i = maxexp + minexp + 3
    j = 1
    while j <= i:
        j = j + 1
        xmax = xmax + xmax if ibeta == DEFAULT_RADIX else xmax * beta
    return {
        "ibeta": ibeta,
        "it": it,
        "irnd": irnd,
        "ngrd": ngrd,
        "machdep": machdep,
        "negep": negep,
        "iexp": iexp,
        "minexp": minexp,
        "maxexp": maxexp,
        "eps": eps,
        "epsneg": epsneg,
        "xmin": xmin,
        "xmax": xmax,
    }


__tmp = machar()

ibeta = __tmp["ibeta"]
"""``ibeta`` (int)
  The radix in which numbers are represented, almost
  always 2, but occasionally 16, or even 10
"""

it = __tmp["it"]
"""``it`` (int)
  The number of base-``ibeta`` digits in the floating point
  mantissa
"""

machdep = __tmp["machdep"]
"""``machep`` (int)
  Is the exponent of the smallest (most negative) power if ``ibeta``
  that, added to 1.0 gives something different from 1.0.
"""

eps = __tmp["eps"]
"""``eps`` (float)
  Is the floating-point number ``ibeta`` ** ``machdep``, loosly
  referred to as the *floating-point precision*.
"""

negep = __tmp["negep"]
"""``negep`` (int)
  Is the exponenet of the smalles power of ``ibeta`` that, subtracted from
  1.0, gives something different from 1.0.
"""

epsneg = __tmp["epsneg"]
"""``epsneg`` (float)
  Is ``ibeta`` ** ``negep``, another way of defining floating-point precision.
  Not infrequently ``epsneg`` is 0.5 times ``eps``; occasionally ``eps`` and ``epsneg``
  are equal.
"""

iexp = __tmp["iexp"]
"""``iexp`` (int)
  Is the number of bits in the exponent (including its sign or bias)
"""

minexp = __tmp["minexp"]
"""``minexp`` (int)
  Is the smallest (most negative) power if ``ibeta`` consistent with there no
  leading zeros in the mantissa.
"""

xmin = __tmp["xmin"]
"""``xmin`` (float)
  Is the floating-point number ``ibeta`` ** ``minexp``, generally the smallest
  (in magnitude) usable floating value
"""

maxexp = __tmp["maxexp"]
"""``maxexp`` (int)
  Is the smallest (positive) power of ``ibeta`` that causes overflow.
"""

xmax = __tmp["xmax"]
"""``xmax`` (float)
  Is (1 - ``epsneg``) x ``ibeta`` ** ``maxexp``, generally the largest (in magnitude)
  usable floating value.
"""

irnd = __tmp["irnd"]
"""``irnd`` (int)
  Returns a code in the range 0...5, giving information on what kind of rounding is done
  in addition, and on how underflow is handled.

  If ``irnd`` returns 2 or 5, then your computer is compilant with the IEEE standard for
  rounding. If it returns 1 or 4, then it is doing some kind of rounding, but not the
  IEEE standard. If ``irnd`` returns 0 or 3, then it is truncating the result, not
  rounding it.
"""

ngrd = __tmp["ngrd"]
"""``ngrd`` (int)
  Is the number of *guard digits* used when truncating the product of two mantissas to
  fit the representation"
"""
