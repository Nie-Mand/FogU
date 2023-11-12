"""
The ``yafs`` module is the main component who perform the simulation.

The following tables list all of the available components in this module.

{toc}

"""
from pkgutil import extend_path

from src.core import Sim
from src.placement import Placement, ClusterPlacement
from src.selection import Selection, OneRandomPath, First_ShortestPath
from src.topology import Topology
from src.population import Population, Statical
from src.application import Application, Message
from src.metrics import Metrics
from src.distribution import *


def compile_toc(entries, section_marker='='):
    """Compiles a list of sections with objects into sphinx formatted
    autosummary directives."""
    toc = ''
    for section, objs in entries:
        toc += '\n\n%s\n%s\n\n' % (section, section_marker * len(section))

        toc += '.. autosummary::\n\n'

        for obj in objs:
            toc += '    ~%s.%s\n' % (obj.__module__, obj.__name__)
    return toc


toc = (
    ('Core', [Sim]),
    ('Topology', [Topology]),
    ('Application', [Application, Message]),
    ('Population', [Population, Statical]),
    ('Placement', [Placement, ClusterPlacement]),
    ('Selection', [Selection, OneRandomPath, First_ShortestPath]),
    ('Metrics', [Metrics]),
    ('Distribution', [Distribution,
     deterministic_distribution, exponential_distribution])
)


# Use the toc to keep the documentation and the implementation in sync.
if __doc__:
    __doc__ = __doc__.format(toc=compile_toc(toc))

__all__ = [obj.__name__ for section, objs in toc for obj in objs]

__path__ = extend_path(__path__, __name__)
__version__ = '1.0'
