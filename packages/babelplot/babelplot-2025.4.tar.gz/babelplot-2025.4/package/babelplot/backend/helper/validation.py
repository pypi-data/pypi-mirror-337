"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import importlib as mprt
import sys as s
from pathlib import Path as path_t

from babelplot.constant.backend import BACKEND_METHOD_TAG, TYPE_PY_PATHS, TYPES
from babelplot.definition.plot import plot_e
from babelplot.extension.ast_ import (
    CalledMethods,
    DefinedMethods,
    module_path_t,
    py_module_h,
)
from babelplot.extension.function import SignaturePairIssues

_MethodNameIsValid = lambda _: BACKEND_METHOD_TAG in _


def CheckBackend(backend: py_module_h | module_path_t, /) -> None:
    """"""
    backend_path = path_t(backend)
    if backend_path.is_file():
        py_backend = backend_path.stem
        spec = mprt.util.spec_from_file_location(py_backend, backend_path)
        imported = mprt.util.module_from_spec(spec)
        s.modules[py_backend] = imported
        spec.loader.exec_module(imported)
    else:
        try:
            imported = mprt.import_module(backend)
        except ModuleNotFoundError as exception:
            print(f"Backend {backend} failed to import:\n{exception}")
            return

    for reference, target_class in zip(TYPE_PY_PATHS, TYPES):
        print(f"--- {target_class}")
        required = CalledMethods(
            reference, target_class, NameIsValid=_MethodNameIsValid
        )
        how_required = DefinedMethods(
            reference,
            mprt.import_module(reference),
            target_class,
            NameIsValid=_MethodNameIsValid,
            should_keep_empty=True,
        )
        how_defined = DefinedMethods(
            backend, imported, target_class, NameIsValid=_MethodNameIsValid
        )

        missing = []
        for name in required:
            if name in how_defined:
                if name in how_required:
                    signa = how_required[name]
                    ture = how_defined[name]
                    issues = SignaturePairIssues(signa, ture)
                    if issues is not None:
                        print(f"{name}:\n    ", "\n    ".join(issues), sep="")
            else:
                missing.append(name)

        as_str = str(missing)[1:-1]
        if as_str.__len__() > 0:
            print("Missing required method(s):", as_str.replace("'", ""))

    if hasattr(imported, "PLOTS"):
        defined = getattr(imported, "PLOTS")
        if isinstance(defined, dict):
            issues = plot_e.PlotsIssues(defined)
            if issues is not None:
                print(f"--- PLOTS:\n    ", "\n    ".join(issues), sep="")
        else:
            print(
                f'--- {type(defined).__name__}: Invalid type for "PLOTS". Expected=dict.'
            )
    else:
        print('--- Missing "PLOTS" dictionary')


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
