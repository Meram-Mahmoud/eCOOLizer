from PyQt5.QtCore import Qt, pyqtSignal
import pyqtgraph as pg
import numpy as np
from Graphs.cine_graph import CineGraph
class SelectableGraphRegion(pg.LinearRegionItem):
    """A custom region selection widget for the graph"""
    regionSelected = pyqtSignal(int, int)  # Emits start and end indices

    def __init__(self):
        super().__init__(
            brush=pg.mkBrush((255, 255, 0, 50)),  # Semi-transparent yellow
            pen=pg.mkPen((255, 255, 0)),  # Yellow border
            movable=True
        )
        self.sigRegionChanged.connect(self._on_region_change)
        self.time_data = None
        
    def set_time_data(self, time_data):
        """Set the time data for index calculation"""
        self.time_data = time_data
        
    def _on_region_change(self):
        """Convert region boundaries to data indices"""
        if self.time_data is None:
            return
            
        region = self.getRegion()
        start_time, end_time = region
        
        # Find closest indices
        start_idx = np.argmin(np.abs(self.time_data - start_time))
        end_idx = np.argmin(np.abs(self.time_data - end_time))
        
        self.regionSelected.emit(start_idx, end_idx)

class SelectableCineGraph(CineGraph):
    """Extension of CineGraph with region selection capability"""
    def __init__(self, title="Selectable Cine Viewer"):
        super().__init__(title)
        self.region = None
        
    def enable_region_selection(self):
        """Add a selectable region to the graph"""
        if self.region is None:
            self.region = SelectableGraphRegion()
            self.plot_widget.addItem(self.region)
            
        if self.signal is not None:
            time_data, _ = self.signal.get_time_domain_data()
            self.region.set_time_data(time_data)
            
            # Set initial region to middle 20% of the signal
            duration = time_data[-1] - time_data[0]
            middle = time_data[0] + duration/2
            self.region.setRegion([middle - duration*0.1, middle + duration*0.1])
            
    def disable_region_selection(self):
        """Remove the selectable region"""
        if self.region is not None:
            self.plot_widget.removeItem(self.region)
            self.region = None
            
    def connect_region_callback(self, callback):
        """Connect a callback to region selection changes"""
        if self.region is not None:
            self.region.regionSelected.connect(callback)