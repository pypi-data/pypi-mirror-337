"""
Command-line interface for the SHM Reader SDK.
"""
import argparse
import binascii
import time
import json
import struct
from typing import Optional, Dict, Any

from .core import ShmReader


def list_segments(shm_reader: ShmReader, args: Optional[argparse.Namespace] = None):
    """List all shared memory segments."""
    print("Looking for shared memory segments:")
    
    # Get all segments
    segments = shm_reader.list_segments()
    if not segments:
        print("  No shared memory segments found!")
        return
    
    # Group segments by type
    segments_by_type: Dict[str, list] = {}
    for segment in segments:
        segment_type = segment.segment_type
        if segment_type not in segments_by_type:
            segments_by_type[segment_type] = []
        segments_by_type[segment_type].append(segment)
    
    # Print segments by type
    for segment_type, type_segments in segments_by_type.items():
        print(f"\n{segment_type.capitalize()} segments:")
        for segment in type_segments:
            print(f"  {segment.name} (size: {segment.size} bytes)")


def clear_segments(shm_reader: ShmReader, args: Optional[argparse.Namespace] = None):
    """Clear shared memory segments."""
    pattern = args.clear_pattern if args and hasattr(args, 'clear_pattern') else None
    count = shm_reader.clear_segments(pattern)
    print(f"Cleared {count} shared memory segments")


def read_segment(shm_reader: ShmReader, args: argparse.Namespace):
    """Read and display the contents of a shared memory segment."""
    try:
        segment = shm_reader.read_segment(args.read)
        print(f"Shared memory segment size: {segment.size} bytes")
        
        # Print raw data in hex if requested
        if args.hex:
            print(f"Raw data (hex): {binascii.hexlify(segment.raw_data).decode()}")
        
        # Print parsed data if available
        if segment.parsed_data:
            print("\nParsed data:")
            for key, value in segment.parsed_data.items():
                print(f"  {key}: {value}")
        else:
            print("\nWarning: Could not parse data as a known format")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error reading or parsing data: {e}")


def monitor_segment(shm_reader: ShmReader, args: argparse.Namespace):
    """Monitor a shared memory segment for changes."""
    try:
        update_field = args.update_field
        print(f"Starting to monitor shared memory segment {args.monitor}, updating every {args.interval} seconds")
        if update_field:
            print(f"Watching for updates to field: {update_field}")
        print("Press Ctrl+C to stop...")
        
        def print_segment(segment):
            """Callback to print segment data."""
            timestamp = time.time()
            print(f"\nTime: {timestamp:.3f}")
            if segment.parsed_data:
                for key, value in segment.parsed_data.items():
                    print(f"  {key}: {value}")
            else:
                print("  (Raw data only, no parser available)")
        
        # Start monitoring using a generator
        for _ in shm_reader.monitor_segment(args.monitor, args.interval, print_segment, update_field):
            pass  # The callback handles printing
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nStopped monitoring")
    except Exception as e:
        print(f"Error monitoring segment: {e}")


def register_parsers(shm_reader: ShmReader, args: argparse.Namespace):
    """Register custom parsers from a JSON file."""
    try:
        with open(args.register_parsers, 'r') as f:
            parser_definitions = json.load(f)
        
        for parser_def in parser_definitions:
            if 'type' not in parser_def or 'format' not in parser_def:
                print(f"Error: Invalid parser definition: {parser_def}")
                continue
            
            segment_type = parser_def['type']
            format_str = parser_def['format']
            field_names = parser_def.get('fields', [])
            
            # Create a parser function
            def create_parser(fmt, fields):
                def parser(data):
                    size = struct.calcsize(fmt)
                    if len(data) < size:
                        raise ValueError(f"Data too short for format {fmt}")
                    values = struct.unpack(fmt, data[:size])
                    return dict(zip(fields, values))
                return parser
            
            # Register the parser
            shm_reader.register_parser(segment_type, create_parser(format_str, field_names))
            print(f"Registered parser for segment type: {segment_type}")
        
    except FileNotFoundError:
        print(f"Error: Parser definition file '{args.register_parsers}' not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in parser definition file '{args.register_parsers}'")
    except Exception as e:
        print(f"Error registering parsers: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Read and monitor shared memory segments")
    parser.add_argument("--list", action="store_true", help="List all available shared memory segments")
    parser.add_argument("--read", metavar="NAME", help="Read the specified shared memory segment")
    parser.add_argument("--hex", action="store_true", help="Show hex dump of raw data when reading")
    parser.add_argument("--monitor", metavar="NAME", help="Monitor the specified shared memory segment")
    parser.add_argument("--update-field", metavar="FIELD", help="Field to check for updates when monitoring")
    parser.add_argument("--interval", type=float, default=1.0, help="Update interval for monitoring (seconds)")
    parser.add_argument("--clear", action="store_true", help="Clear all shared memory segments")
    parser.add_argument("--clear-pattern", metavar="PATTERN", help="Clear shared memory segments matching the pattern")
    parser.add_argument("--register-parsers", metavar="FILE", help="Register parsers from a JSON configuration file")
    
    args = parser.parse_args()
    
    # Create the SHM reader
    shm_reader = ShmReader()
    
    # Register parsers if requested
    if args.register_parsers:
        register_parsers(shm_reader, args)
    
    # Process arguments
    if args.clear:
        clear_segments(shm_reader)
    elif args.clear_pattern:
        clear_segments(shm_reader, args)
    elif args.list or (not args.read and not args.monitor and not args.register_parsers):
        list_segments(shm_reader)
    
    if args.read:
        read_segment(shm_reader, args)
    
    if args.monitor:
        monitor_segment(shm_reader, args)


if __name__ == "__main__":
    main() 