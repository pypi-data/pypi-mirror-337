"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import ast
import importlib.util as mprt
import inspect as insp
import typing as h
from types import ModuleType as module_type_t

from babelplot.extension.function import (
    FunctionIsNotEmpty,
    FunctionSignature,
    signature_h,
)
from logger_36.instance.logger import L

py_module_h = h.TypeVar("py_module_h", bound=str)  # E.g. module.submodule.
module_path_t = str


def DefinedMethods(
    module: py_module_h | module_path_t,
    imported: module_type_t,
    target_class: str,
    /,
    *,
    NameIsValid: h.Callable[[str], bool] | None = None,
    should_keep_empty: bool = False,
) -> dict[str, signature_h]:
    """"""
    if NameIsValid is None:
        NameIsValid = lambda _: True

    output = {}

    if not hasattr(imported, target_class):
        L.error(f'Module {module} does not define a "{target_class}" class')
        return {}

    target_class = getattr(imported, target_class)
    for name in dir(target_class):
        attribute = getattr(target_class, name)

        if name == "__dict__":
            # Method added through type(...) (do not test non-emptiness).
            for key, value in attribute.items():
                if (
                    insp.isfunction(value)
                    and (not key.startswith("_"))
                    and NameIsValid(key)
                ):
                    output[key] = FunctionSignature(value)
        elif (
            insp.isfunction(attribute)
            and (not name.startswith("_"))
            and NameIsValid(name)
            and (FunctionIsNotEmpty(attribute) or should_keep_empty)
        ):
            # Method defined in class definition (do test non-emptiness).
            output[name] = FunctionSignature(attribute)

    # Note: Unfortunately, depending on whether a method was added through type or
    # defined in the class definition, the signature can be a string version of itself.
    # Why? Anyway, this is an issue for signature comparison.

    return output


def CalledMethods(
    py_module: py_module_h,
    target_class: str,
    /,
    *,
    NameIsValid: h.Callable[[str], bool] | None = None,
) -> h.Sequence[str]:
    """"""
    if NameIsValid is None:
        NameIsValid = lambda _: True

    output = []

    spec = mprt.find_spec(py_module)
    with open(spec.origin) as accessor:
        tree = ast.parse(accessor.read())

    for main_node in ast.iter_child_nodes(tree):
        if isinstance(main_node, ast.ClassDef) and (main_node.name == target_class):
            for node in ast.walk(main_node):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                ):
                    record = node.func
                    called = record.attr
                    context = record.value.id
                    if (
                        (context == "self")
                        and (not called.startswith("_"))
                        and NameIsValid(called)
                    ):
                        output.append(called)
            break

    return tuple(sorted(set(output)))


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
