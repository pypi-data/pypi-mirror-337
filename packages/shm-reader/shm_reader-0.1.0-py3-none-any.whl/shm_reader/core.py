"""
Core functionality for the SHM Reader SDK.
"""
import os
import glob
import struct
import time
import binascii
from dataclasses import dataclass
from typing import List, Dict, Optional, Generator, Union, Tuple, Any, Callable


@dataclass
class SharedMemorySegment:
    """Represents a shared memory segment with parsed data if available."""
    name: str
    path: str
    size: int
    raw_data: Optional[bytes] = None
    parsed_data: Optional[Dict[str, Any]] = None
    
    @property
    def segment_type(self) -> str:
        """Get the segment type based on its name."""
        if ":" in self.name:
            return self.name.split(":", 1)[0]
        return "unknown"


class ShmReader:
    """
    SDK for reading shared memory segments.
    
    Provides functionality to:
    - List available shared memory segments
    - Read data from shared memory segments
    - Monitor shared memory segments for changes
    - Clear shared memory segments
    """
    
    # Registry of data parsers
    _parsers: Dict[str, Callable[[bytes], Dict[str, Any]]] = {}
    
    def __init__(self, base_path: str = "/dev/shm"):
        """
        Initialize the ShmReader.
        
        Args:
            base_path: Base path for shared memory segments, defaults to /dev/shm
        """
        self.base_path = base_path
    
    @classmethod
    def register_parser(cls, segment_type: str, parser_func: Callable[[bytes], Dict[str, Any]]):
        """
        Register a parser function for a specific segment type.
        
        Args:
            segment_type: Type identifier for segments to parse
            parser_func: Function that takes bytes and returns a dictionary of parsed values
        """
        cls._parsers[segment_type] = parser_func
    
    def list_segments(self, pattern: Optional[str] = None) -> List[SharedMemorySegment]:
        """
        List all available shared memory segments.
        
        Args:
            pattern: Optional glob pattern to filter segments
            
        Returns:
            List of SharedMemorySegment objects
        """
        if pattern:
            segment_paths = glob.glob(os.path.join(self.base_path, pattern))
        else:
            segment_paths = glob.glob(os.path.join(self.base_path, "*"))
        
        return [
            SharedMemorySegment(
                name=os.path.basename(path),
                path=path,
                size=os.path.getsize(path)
            )
            for path in segment_paths
            if os.path.isfile(path)
        ]
    
    def list_segments_by_type(self, segment_type: str) -> List[SharedMemorySegment]:
        """
        Get shared memory segments with a specific type prefix.
        
        Args:
            segment_type: The segment type to filter by
            
        Returns:
            List of SharedMemorySegment objects of the specified type
        """
        all_segments = self.list_segments()
        return [seg for seg in all_segments if seg.segment_type == segment_type]
    
    def clear_segments(self, pattern: Optional[str] = None) -> int:
        """
        Clear shared memory segments matching the pattern.
        
        Args:
            pattern: Glob pattern for segments to clear
            
        Returns:
            Number of segments cleared
        """
        if pattern is None:
            pattern = "*"
        
        segments = self.list_segments(pattern)
        count = 0
        
        for segment in segments:
            try:
                os.remove(segment.path)
                count += 1
            except Exception:
                # Ignore errors for now, could be permission issues
                pass
        
        return count
    
    def read_segment(self, name: str) -> SharedMemorySegment:
        """
        Read data from a shared memory segment.
        
        Args:
            name: Name of the shared memory segment to read
            
        Returns:
            SharedMemorySegment with raw_data and parsed_data if available
            
        Raises:
            FileNotFoundError: If the segment doesn't exist
        """
        path = os.path.join(self.base_path, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Shared memory segment {path} does not exist")
        
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            data = f.read(size)
        
        segment = SharedMemorySegment(
            name=name,
            path=path,
            size=size,
            raw_data=data
        )
        
        # Try to parse the data using registered parsers
        segment_type = segment.segment_type
        if segment_type in self._parsers:
            try:
                segment.parsed_data = self._parsers[segment_type](data)
            except Exception:
                # If parsing fails, leave parsed_data as None
                pass
        
        return segment
    
    def monitor_segment(self, name: str, interval: float = 1.0, 
                        callback=None, update_field: str = None) -> Generator[SharedMemorySegment, None, None]:
        """
        Monitor a shared memory segment for changes.
        
        Args:
            name: Name of the shared memory segment to monitor
            interval: Update interval in seconds
            callback: Optional callback function to call on each update
            update_field: Optional field name to check for updates (if None, will yield on every check)
            
        Yields:
            SharedMemorySegment objects on each update
            
        Raises:
            FileNotFoundError: If the segment doesn't exist
        """
        path = os.path.join(self.base_path, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Shared memory segment {path} does not exist")
        
        last_update_value = None
        
        try:
            while True:
                segment = self.read_segment(name)
                
                # Determine if we should yield this segment
                should_yield = False
                
                if update_field and segment.parsed_data and update_field in segment.parsed_data:
                    current_value = segment.parsed_data[update_field]
                    if last_update_value is None or current_value != last_update_value:
                        last_update_value = current_value
                        should_yield = True
                else:
                    # If no update field specified, or it doesn't exist, yield every time
                    should_yield = True
                
                if should_yield:
                    if callback:
                        callback(segment)
                    yield segment
                
                time.sleep(interval)
        except KeyboardInterrupt:
            # Let the client handle this
            return


# Register the default volatility parser for backward compatibility
def _volatility_parser(data: bytes) -> Dict[str, Any]:
    """Parse volatility data format."""
    if len(data) >= 56:  # 7 double/long values (8 bytes each)
        values = struct.unpack("dddddqq", data[:56])
        return {
            "timestamp": values[0],
            "price": values[1],
            "volatility_1s": values[2],
            "high_1s": values[3],
            "low_1s": values[4],
            "volume_1s": values[5],
            "update_count": values[6]
        }
    raise ValueError("Data too short for volatility format")

# Register the built-in parser
ShmReader.register_parser("volatility", _volatility_parser) 