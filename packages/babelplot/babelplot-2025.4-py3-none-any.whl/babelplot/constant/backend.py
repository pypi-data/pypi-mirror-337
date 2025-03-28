"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

from pathlib import Path as path_t

from babelplot.constant.path import BACKEND_CATALOG_PY_PATH

_BASE_PY_PATH = "babelplot.type"

TYPE_PY_PATHS = (
    f"{_BASE_PY_PATH}.plot",
    f"{_BASE_PY_PATH}.frame",
    f"{_BASE_PY_PATH}.figure",
)
TYPES = ("plot_t", "frame_t", "figure_t")

BACKEND_METHOD_TAG = "Backend"
BACKEND_PLOT_STRIPE = "backend_plot_t"

BACKENDS = {}
_parent = path_t(__file__).parent.parent.parent
_catalog_path = _parent / path_t(*BACKEND_CATALOG_PY_PATH.split("."))
for node in _catalog_path.glob("*"):
    if node.name.startswith("_"):
        continue

    if node.is_dir():
        main = node / "main.py"
        if main.is_file():
            node = main
        else:
            continue

    py_path = ".".join(node.relative_to(_parent).parent.parts + (node.stem,))
    # try:
    #     module = mprt.import_module(py_path)
    # except ModuleNotFoundError:
    #     continue
    #
    # stripe = getattr(module, BACKEND_PLOT_STRIPE, None)
    # if stripe is None:
    #     backend_import_name = "<UNKNOWN_BACKEND_IMPORT_NAME>"
    # else:
    #     backend_import_name = stripe.__module__.split(".")[0]

    BACKENDS[node.stem[:-1]] = (node, py_path)


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
