"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import os as osys
import sys as s
import tempfile as tmpf

from babelplot.constant.project import NAME
from babelplot.runtime.figure import SHOWN_FIGURES, UN_SHOWN_FIGURES
from babelplot.type.figure import figure_t
from PyQt6.QtCore import QUrl as url_t
from PyQt6.QtWebEngineWidgets import QWebEngineView as widget_t
from PyQt6.QtWidgets import QApplication as application_t


def Show(figure: figure_t, /) -> None:
    """"""
    # The application must be instantiated in the same thread/process as the one running
    # exec().
    if (application := application_t.instance()) is None:
        application = application_t(s.argv)
    application.setApplicationName(f"{NAME}-{id(figure)}")
    widget = widget_t()

    html = figure.AsHTML()
    SetHTMLFromFile = lambda _: _SetHTMLFromFile(_, widget, html)
    widget.loadFinished.connect(SetHTMLFromFile)
    widget.setHtml(html)

    widget.show()
    application.exec()


def ShowAllFigures(
    *,
    modal: bool = True,
) -> None:
    """"""
    # TODO: Is this related to backend thread support (see associated constant)?
    if all(_.backend_name == "matplotlib" for _ in UN_SHOWN_FIGURES):
        for figure in UN_SHOWN_FIGURES:
            figure.AdjustLayout()

        SHOWN_FIGURES.extend(UN_SHOWN_FIGURES)  # /!\ Must be removed when closed.
        UN_SHOWN_FIGURES.clear()

        import matplotlib.pyplot as pypl  # noqa

        pypl.show()
    else:
        while UN_SHOWN_FIGURES.__len__() > 1:
            UN_SHOWN_FIGURES[0].Show(modal=False)
        if UN_SHOWN_FIGURES.__len__() > 0:
            UN_SHOWN_FIGURES[0].Show(modal=modal)


# def CloseFigure(figure: figure_t, /)->None:
#     """"""


# def CloseAllFigures()->None:
#     """"""


def _SetHTMLFromFile(success: bool, widget: widget_t, html: str, /) -> None:
    """
    From: https://doc.qt.io/qtforpython-6/PySide6/QtWebEngineWidgets/QWebEngineView.html#PySide6.QtWebEngineWidgets.PySide6.QtWebEngineWidgets.QWebEngineView.setHtml
        Content larger than 2 MB cannot be displayed...
        ...
        Thereby, the provided code becomes a URL that exceeds the 2 MB limit set by
        Chromium. If the content is too large, the loadFinished() signal is triggered
        with success=False.
    Solution: Use a temporary file (with html extension) and setUrl.
    """
    if success:
        return

    transfer = tmpf.NamedTemporaryFile(mode="w", suffix=".html", delete=False)
    with open(transfer.name, "w") as accessor:
        accessor.write(html)
    url = url_t.fromLocalFile(transfer.name)
    widget.setUrl(url)
    DeleteTemporaryFile = lambda: osys.remove(transfer.name)
    application_t.instance().lastWindowClosed.connect(DeleteTemporaryFile)


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
