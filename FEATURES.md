# StegSolve GUI - 10 Implemented Functions

## 1. Bit Plane Analysis (0-7)
- View individual bit planes from LSB (0) to MSB (7)
- Each bit plane displayed as binary image
- Essential for LSB steganography analysis

## 2. RGB Channel Separation
- Separate Red, Green, Blue, and Alpha channels
- View each channel independently
- RGB composite view

## 3. Color Space Conversion
- Convert to HSV color space
- Convert to YCbCr color space  
- Convert to LAB (grayscale approximation)

## 4. Basic Image Operations
- Grayscale conversion
- Color inversion
- Image rotation (90°)
- Horizontal and vertical flip
- LSB extraction (bit plane 0)

## 5. Bit Plane Operations
- XOR all bit planes
- AND all bit planes  
- OR all bit planes
- Display all 8 bit planes in 2x4 grid

## 6. File Structure Analysis
- Analyze file signatures (PNG, JPEG, BMP, GIF)
- Display file size and format information
- Identify image type from binary signature

## 7. String Extraction
- Extract ASCII strings from binary data
- Minimum string length: 4 characters
- Display in scrollable text window
- Shows first 100 strings with count

## 8. GIF Frame Browser
- Browse individual frames of animated GIFs
- Slider to navigate through frames
- Frame counter display

## 9. Statistical Analysis
- Calculate min, max, mean, standard deviation
- Per-channel statistics for RGB images
- Grayscale image statistics
- Display in dedicated window

## 10. Advanced Operations (Placeholders)
- Image comparison (future implementation)
- Data carving (future implementation)  
- Noise analysis (future implementation)
- LSB replacement detection (future implementation)

## Additional Features
- **Graphical User Interface**: Tkinter-based with tabbed interface
- **Image Display**: Canvas with auto-scaling
- **File Operations**: Open/Save with common formats
- **Keyboard Shortcuts**: Ctrl+O (Open), Ctrl+S (Save)
- **Status Bar**: Operation feedback
- **Menu System**: File, Tools, Help menus

## Technical Implementation
- **GUI Framework**: Tkinter (standard Python)
- **Image Processing**: PIL/Pillow
- **Numerical Operations**: NumPy
- **Bit Plane Extraction**: NumPy bitwise operations
- **File Analysis**: Binary signature detection

## Usage Example
1. Load an image (Ctrl+O)
2. Go to "Bit Planes" tab
3. Select bit plane 0 (LSB)
4. Click "Show Bit Plane" to view hidden data
5. Use "Extract Strings" to find embedded text
