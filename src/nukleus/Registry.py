from typing import List, Type

from nukleus.AbstractPlot import AbstractPlot

from .plot.PlotSvgWrite import PlotSvgWrite

class Registry():
    spice_path: List[str] = []
    library_path: List[str] = []
    PLOTTER: Type[AbstractPlot] = PlotSvgWrite

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Registry, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
