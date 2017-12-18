#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# models/big_phi.py

"""Objects that represent cause-effect structures."""

from . import cmp, fmt
from .. import utils

# pylint: disable=too-many-arguments

_sia_attributes = ['phi', 'unpartitioned_ces',
                      'partitioned_ces', 'subsystem',
                      'cut_subsystem']


class SystemIrreducibilityAnalysis(cmp.Orderable):
    """An analysis of system irreducibility (|big_phi|).

    Contains the |big_phi| value of the |Subsystem|, the cause-effect
    structure, and all the intermediate results obtained in the course of
    computing them.

    These can be compared with the built-in Python comparison operators (``<``,
    ``>``, etc.). First, |big_phi| values are compared. Then, if these are
    equal up to |PRECISION|, the one with the larger subsystem is greater.

    Attributes:
        phi (float): The |big_phi| value for the subsystem when taken against
            this MIP, *i.e.* the difference between the unpartitioned
            cause-effect structure and this MIP's partitioned cause-effect
            structure.
        unpartitioned_ces (CauseEffectStructure): The cause-effect structure of
            the whole subsystem.
        partitioned_ces (CauseEffectStructure): The cause-effect structure when
            the subsystem is cut.
        subsystem (Subsystem): The subsystem this MIP was calculated for.
        cut_subsystem (Subsystem): The subsystem with the minimal cut applied.
        time (float): The number of seconds it took to calculate.
        small_phi_time (float): The number of seconds it took to calculate the
            unpartitioned cause-effect structure.
    """

    def __init__(self, phi=None, unpartitioned_ces=None,
                 partitioned_ces=None, subsystem=None,
                 cut_subsystem=None, time=None, small_phi_time=None):
        self.phi = phi
        self.unpartitioned_ces = unpartitioned_ces
        self.partitioned_ces = partitioned_ces
        self.subsystem = subsystem
        self.cut_subsystem = cut_subsystem
        self.time = time
        self.small_phi_time = small_phi_time

    def __repr__(self):
        return fmt.make_repr(self, _sia_attributes)

    def __str__(self, ces=True):
        return fmt.fmt_sia(self, ces=ces)

    def print(self, ces=True):
        """Print this |SystemIrreducibilityAnalysis|, optionally without
        cause-effect structures."""
        print(self.__str__(ces=ces))

    @property
    def cut(self):
        """The unidirectional cut that makes the least difference to the
        subsystem.
        """
        return self.cut_subsystem.cut

    @property
    def network(self):
        """The network the subsystem belongs to."""
        return self.subsystem.network

    unorderable_unless_eq = ['network']

    def order_by(self):
        return [self.phi, len(self.subsystem), self.subsystem.node_indices]

    def __eq__(self, other):
        return cmp.general_eq(self, other, _sia_attributes)

    def __bool__(self):
        """A |SystemIrreducibilityAnalysis| evaluates to``True`` if it has
        |big_phi > 0|.
        """
        return not utils.eq(self.phi, 0)

    def __hash__(self):
        return hash((self.phi,
                     self.unpartitioned_ces,
                     self.partitioned_ces,
                     self.subsystem,
                     self.cut_subsystem))

    def to_json(self):
        """Return a JSON-serializable representation."""
        return {
            attr: getattr(self, attr)
            for attr in _sia_attributes + ['time', 'small_phi_time']
        }


def _null_sia(subsystem, phi=0.0):
    """Return a |SystemIrreducibilityAnalysis| with zero |big_phi| and empty
    cause-effect structures.

    This is the analysis result for a reducible subsystem.
    """
    return SystemIrreducibilityAnalysis(subsystem=subsystem,
                                        cut_subsystem=subsystem,
                                        phi=phi,
                                        unpartitioned_ces=(),
                                        partitioned_ces=())
