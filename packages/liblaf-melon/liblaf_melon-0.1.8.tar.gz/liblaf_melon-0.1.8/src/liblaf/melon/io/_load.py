from typing import Any

from liblaf import melon
from liblaf.melon.typed import StrPath

from . import reader_dispatcher

reader_dispatcher.register(melon.io.melon.DICOMReader())
reader_dispatcher.register(melon.io.pyvista.PolyDataReader())
reader_dispatcher.register(melon.io.pyvista.UnstructuredGridReader())


def load(path: StrPath) -> Any:
    return reader_dispatcher.load(path)
