#!/usr/bin/env python3
"""
Test script for StegSolve GUI
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import tkinter
        print("✓ tkinter imported successfully")
    except ImportError as e:
        print(f"✗ tkinter import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ PIL imported successfully")
    except ImportError as e:
        print(f"✗ PIL import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ numpy import failed: {e}")
        return False
    
    return True

def test_image_processing():
    """Test basic image processing functions"""
    print("\nTesting image processing...")
    
    try:
        from PIL import Image
        import numpy as np
        
        # Create a test image
        test_array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        test_image = Image.fromarray(test_array)
        
        # Test grayscale conversion
        gray_image = test_image.convert('L')
        
        # Test bit plane extraction
        gray_array = np.array(gray_image)
        bit_plane = ((gray_array >> 0) & 1) * 255
        
        print("✓ Image processing functions work")
        return True
    except Exception as e:
        print(f"✗ Image processing test failed: {e}")
        return False

def test_main_module():
    """Test if the main module can be imported"""
    print("\nTesting main module...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Try to import the module without running GUI
        import stegsolve_gui
        print("✓ Main module imported successfully")
        
        # Check if class exists
        if hasattr(stegsolve_gui, 'StegSolveGUI'):
            print("✓ StegSolveGUI class found")
        else:
            print("✗ StegSolveGUI class not found")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Main module import failed: {e}")
        return False

def main():
    print("=" * 50)
    print("StegSolve GUI Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    if not test_imports():
        all_passed = False
    
    if not test_image_processing():
        all_passed = False
    
    if not test_main_module():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed!")
        print("\nTo run the application:")
        print("  python stegsolve_gui.py")
    else:
        print("✗ Some tests failed")
        print("\nPlease check the error messages above.")
    
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
