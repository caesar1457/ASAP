#!/usr/bin/env python3
"""
Script to check motion duration and timing information from motion files
"""

import joblib
import numpy as np
import torch
from pathlib import Path
import argparse
import sys

def check_motion_duration(motion_file_path):
    """Check the duration and timing information of a motion file"""
    
    print(f"Loading motion file: {motion_file_path}")
    
    try:
        # Load the motion data
        motion_data = joblib.load(motion_file_path)
        
        print("\n" + "="*50)
        print("MOTION FILE ANALYSIS")
        print("="*50)
        
        if isinstance(motion_data, dict):
            # Single motion file
            print(f"File type: Single motion file")
            print(f"Number of motions: 1")
            
            # Check if it's a nested structure
            if len(motion_data) == 1:
                key = list(motion_data.keys())[0]
                motion = motion_data[key]
                print(f"Motion key: {key}")
            else:
                motion = motion_data
                print("Direct motion data")
            
            analyze_single_motion(motion)
            
        elif isinstance(motion_data, list):
            # Multiple motion files
            print(f"File type: Multiple motion files")
            print(f"Number of motions: {len(motion_data)}")
            
            for i, motion_file in enumerate(motion_data):
                print(f"\n--- Motion {i+1}: {motion_file} ---")
                if Path(motion_file).exists():
                    try:
                        motion = joblib.load(motion_file)
                        analyze_single_motion(motion)
                    except Exception as e:
                        print(f"Error loading motion {i+1}: {e}")
                else:
                    print(f"File not found: {motion_file}")
        
        else:
            print(f"Unknown file format: {type(motion_data)}")
            
    except Exception as e:
        print(f"Error loading motion file: {e}")
        return False
    
    return True

def analyze_single_motion(motion):
    """Analyze a single motion's timing information"""
    
    print(f"Motion data type: {type(motion)}")
    
    if isinstance(motion, dict):
        # Dictionary format
        print("\nAvailable keys:")
        for key in motion.keys():
            print(f"  - {key}")
        
        # Check for timing-related keys
        if 'fps' in motion:
            fps = motion['fps']
            print(f"\nFPS: {fps}")
        
        # Check for pose data to determine duration
        pose_keys = ['pose_aa', 'pose_quat_global', 'dof_pos', 'root_trans_offset']
        for key in pose_keys:
            if key in motion:
                data = motion[key]
                if hasattr(data, 'shape'):
                    num_frames = data.shape[0]
                    if 'fps' in motion:
                        duration = num_frames / motion['fps']
                        print(f"\n{key}:")
                        print(f"  - Number of frames: {num_frames}")
                        print(f"  - Duration: {duration:.3f} seconds")
                        print(f"  - Shape: {data.shape}")
                    else:
                        print(f"\n{key}:")
                        print(f"  - Number of frames: {num_frames}")
                        print(f"  - Shape: {data.shape}")
                        print(f"  - Duration: Unknown (no fps information)")
        
        # Check for action data
        if 'action' in motion:
            action_data = motion['action']
            if hasattr(action_data, 'shape'):
                print(f"\nAction data:")
                print(f"  - Number of frames: {action_data.shape[0]}")
                print(f"  - Shape: {action_data.shape}")
        
        # Check for other timing-related information
        if 'dt' in motion:
            print(f"\nTime step (dt): {motion['dt']} seconds")
        
    elif hasattr(motion, 'fps'):
        # Object with fps attribute
        fps = motion.fps
        print(f"\nFPS: {fps}")
        
        # Try to get frame count from various attributes
        frame_attrs = ['global_rotation', 'local_rotation', 'global_translation', 'dof_pos']
        for attr in frame_attrs:
            if hasattr(motion, attr):
                data = getattr(motion, attr)
                if hasattr(data, 'shape'):
                    num_frames = data.shape[0]
                    duration = num_frames / fps
                    print(f"\n{attr}:")
                    print(f"  - Number of frames: {num_frames}")
                    print(f"  - Duration: {duration:.3f} seconds")
                    print(f"  - Shape: {data.shape}")
                    break
        
        # Check for action data
        if hasattr(motion, 'action'):
            action_data = motion.action
            if hasattr(action_data, 'shape'):
                print(f"\nAction data:")
                print(f"  - Number of frames: {action_data.shape[0]}")
                print(f"  - Shape: {action_data.shape}")
    
    else:
        print("No timing information found in motion data")

def main():
    parser = argparse.ArgumentParser(description="Check motion duration and timing information")
    parser.add_argument("motion_file", help="Path to the motion file (.pkl)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    motion_file_path = Path(args.motion_file)
    
    if not motion_file_path.exists():
        print(f"Error: Motion file not found: {motion_file_path}")
        sys.exit(1)
    
    success = check_motion_duration(motion_file_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 