from typing import Any

from liblaf import melon
from liblaf.melon.typed import StrPath

from . import writer_dispatcher

writer_dispatcher.register(melon.io.melon.DICOMWriter())
writer_dispatcher.register(melon.io.pyvista.PolyDataWriter())
writer_dispatcher.register(melon.io.pyvista.UnstructuredGridWriter())


def save(path: StrPath, obj: Any) -> None:
    writer_dispatcher.save(path, obj)
