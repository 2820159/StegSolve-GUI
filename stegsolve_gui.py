#!/usr/bin/env python3
"""
StegSolve-like GUI Tool for Steganography Analysis
A Python implementation with 10+ steganography analysis functions
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import os
import io

class StegSolveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StegSolve GUI - Python Steganography Analysis Tool")
        self.root.geometry("1200x800")
        
        # Current image and data
        self.current_image = None
        self.image_path = None
        self.image_array = None
        self.bit_planes = None
        
        # Create GUI layout
        self.setup_ui()
        
        # Initialize with sample message
        self.status_label.config(text="Ready. Load an image to begin analysis.")
    
    def setup_ui(self):
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Image", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Extract Strings", command=self.extract_strings)
        tools_menu.add_command(label="Analyze File Structure", command=self.analyze_file_structure)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Image display
        left_frame = ttk.Frame(main_frame, width=600)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Image display canvas
        self.image_canvas = tk.Canvas(left_frame, bg='gray20')
        self.image_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Image info label
        self.image_info_label = ttk.Label(left_frame, text="No image loaded")
        self.image_info_label.pack(pady=5)
        
        # Right panel - Controls
        right_frame = ttk.Frame(main_frame, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Tool selection notebook
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Basic Operations
        basic_tab = ttk.Frame(self.notebook)
        self.notebook.add(basic_tab, text="Basic")
        self.setup_basic_tab(basic_tab)
        
        # Tab 2: Bit Plane Analysis
        bitplane_tab = ttk.Frame(self.notebook)
        self.notebook.add(bitplane_tab, text="Bit Planes")
        self.setup_bitplane_tab(bitplane_tab)
        
        # Tab 3: RGB Analysis
        rgb_tab = ttk.Frame(self.notebook)
        self.notebook.add(rgb_tab, text="RGB Channels")
        self.setup_rgb_tab(rgb_tab)
        
        # Tab 4: Advanced Operations
        advanced_tab = ttk.Frame(self.notebook)
        self.notebook.add(advanced_tab, text="Advanced")
        self.setup_advanced_tab(advanced_tab)
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())
    
    def setup_basic_tab(self, parent):
        ttk.Label(parent, text="Basic Image Operations", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Operation buttons
        operations = [
            ("Open Image", self.open_image),
            ("Save Image", self.save_image),
            ("Grayscale", self.apply_grayscale),
            ("Invert Colors", self.invert_colors),
            ("Rotate 90°", lambda: self.rotate_image(90)),
            ("Flip Horizontal", self.flip_horizontal),
            ("Flip Vertical", self.flip_vertical),
            ("Extract LSB", self.extract_lsb),
        ]
        
        for text, command in operations:
            ttk.Button(parent, text=text, command=command).pack(fill=tk.X, padx=20, pady=2)
    
    def setup_bitplane_tab(self, parent):
        ttk.Label(parent, text="Bit Plane Analysis", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Bit plane selection
        bit_frame = ttk.Frame(parent)
        bit_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(bit_frame, text="Select Bit Plane:").pack(side=tk.LEFT)
        
        self.bit_var = tk.StringVar(value="0")
        bit_spinbox = ttk.Spinbox(bit_frame, from_=0, to=7, textvariable=self.bit_var, width=5)
        bit_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(bit_frame, text="Show Bit Plane", command=self.show_bit_plane).pack(side=tk.LEFT, padx=5)
        
        # Channel selection
        channel_frame = ttk.Frame(parent)
        channel_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(channel_frame, text="Channel:").pack(side=tk.LEFT)
        
        self.channel_var = tk.StringVar(value="All")
        channels = ["All", "Red", "Green", "Blue", "Alpha"]
        channel_combo = ttk.Combobox(channel_frame, textvariable=self.channel_var, values=channels, state="readonly", width=10)
        channel_combo.pack(side=tk.LEFT, padx=5)
        
        # Bit plane operations
        ttk.Label(parent, text="Bit Plane Operations:", font=('Arial', 10)).pack(pady=(10, 5))
        
        bit_ops = [
            ("XOR Planes", self.xor_bit_planes),
            ("AND Planes", self.and_bit_planes),
            ("OR Planes", self.or_bit_planes),
            ("Extract All Planes", self.extract_all_bit_planes),
        ]
        
        for text, command in bit_ops:
            ttk.Button(parent, text=text, command=command).pack(fill=tk.X, padx=20, pady=2)
    
    def setup_rgb_tab(self, parent):
        ttk.Label(parent, text="RGB Channel Analysis", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Channel separation
        ttk.Label(parent, text="Separate Channels:").pack(pady=5)
        
        rgb_buttons = [
            ("Show Red Channel", lambda: self.show_channel('R')),
            ("Show Green Channel", lambda: self.show_channel('G')),
            ("Show Blue Channel", lambda: self.show_channel('B')),
            ("Show Alpha Channel", lambda: self.show_channel('A')),
            ("Show RGB Composite", self.show_rgb_composite),
        ]
        
        for text, command in rgb_buttons:
            ttk.Button(parent, text=text, command=command).pack(fill=tk.X, padx=20, pady=2)
        
        # Color space conversion
        ttk.Label(parent, text="Color Space Conversion:", font=('Arial', 10)).pack(pady=(15, 5))
        
        color_buttons = [
            ("Convert to HSV", self.convert_to_hsv),
            ("Convert to YCbCr", self.convert_to_ycbcr),
            ("Convert to LAB", self.convert_to_lab),
        ]
        
        for text, command in color_buttons:
            ttk.Button(parent, text=text, command=command).pack(fill=tk.X, padx=20, pady=2)
    
    def setup_advanced_tab(self, parent):
        ttk.Label(parent, text="Advanced Operations", font=('Arial', 12, 'bold')).pack(pady=10)
        
        advanced_ops = [
            ("Analyze File Structure", self.analyze_file_structure),
            ("Extract Strings", self.extract_strings),
            ("Compare Images", self.compare_images),
            ("Frame Browser (GIF)", self.frame_browser),
            ("Data Carving", self.data_carving),
            ("Statistical Analysis", self.statistical_analysis),
            ("Noise Analysis", self.noise_analysis),
            ("LSB Replacement Detection", self.lsb_detection),
        ]
        
        for text, command in advanced_ops:
            ttk.Button(parent, text=text, command=command).pack(fill=tk.X, padx=20, pady=2)
    
    def open_image(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename(
                title="Select Image File",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                    ("All files", "*.*")
                ]
            )
        
        if filepath:
            try:
                self.image_path = filepath
                self.current_image = Image.open(filepath)
                
                # Convert to RGB if necessary
                if self.current_image.mode not in ['RGB', 'RGBA', 'L']:
                    self.current_image = self.current_image.convert('RGB')
                
                # Convert to numpy array for processing
                self.image_array = np.array(self.current_image)
                
                # Update display
                self.display_image(self.current_image)
                
                # Update info label
                info = f"{os.path.basename(filepath)} | {self.current_image.size[0]}x{self.current_image.size[1]} | {self.current_image.mode}"
                self.image_info_label.config(text=info)
                
                self.status_label.config(text=f"Loaded: {os.path.basename(filepath)}")
                
                # Precompute bit planes
                self.precompute_bit_planes()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image):
        # Clear canvas
        self.image_canvas.delete("all")
        
        # Resize image to fit canvas
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 600
            canvas_height = 400
        
        img_width, img_height = image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))
        
        if ratio < 1:
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.display_photo = ImageTk.PhotoImage(image)
        
        # Display on canvas
        self.image_canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.display_photo,
            anchor=tk.CENTER
        )
    
    def precompute_bit_planes(self):
        if self.image_array is None:
            return
        
        # Convert to grayscale for bit plane analysis
        if len(self.image_array.shape) == 3:
            gray = np.dot(self.image_array[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            gray = self.image_array
        
        gray = gray.astype(np.uint8)
        
        # Compute bit planes
        self.bit_planes = []
        for i in range(8):
            plane = ((gray >> i) & 1) * 255
            self.bit_planes.append(plane)
    
    def show_bit_plane(self):
        if self.bit_planes is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            bit = int(self.bit_var.get())
            if bit < 0 or bit > 7:
                raise ValueError
            
            plane = self.bit_planes[bit]
            plane_image = Image.fromarray(plane.astype(np.uint8))
            self.display_image(plane_image)
            
            self.status_label.config(text=f"Showing bit plane {bit} (LSB={bit})")
            
        except ValueError:
            messagebox.showerror("Error", "Bit plane must be between 0 and 7")
    
    def show_channel(self, channel):
        if self.image_array is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        channel_map = {'R': 0, 'G': 1, 'B': 2, 'A': 3}
        
        if len(self.image_array.shape) == 2:  # Grayscale
            channel_image = Image.fromarray(self.image_array)
        else:
            if channel == 'A' and self.image_array.shape[2] < 4:
                messagebox.showinfo("Info", "No alpha channel in this image")
                return
            
            if channel in channel_map:
                idx = channel_map[channel]
                if idx < self.image_array.shape[2]:
                    channel_array = self.image_array[:, :, idx]
                    channel_image = Image.fromarray(channel_array)
                else:
                    messagebox.showinfo("Info", f"Channel {channel} not available")
                    return
        
        self.display_image(channel_image)
        self.status_label.config(text=f"Showing {channel} channel")
    
    def show_rgb_composite(self):
        if self.image_array is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        if len(self.image_array.shape) == 2:
            rgb_image = Image.fromarray(self.image_array).convert('RGB')
        else:
            rgb_image = Image.fromarray(self.image_array)
        
        self.display_image(rgb_image)
        self.status_label.config(text="Showing RGB composite")
    
    def apply_grayscale(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        gray_image = self.current_image.convert('L')
        self.display_image(gray_image)
        self.status_label.config(text="Applied grayscale conversion")
    
    def invert_colors(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        inverted = ImageOps.invert(self.current_image.convert('RGB'))
        self.display_image(inverted)
        self.status_label.config(text="Inverted colors")
    
    def rotate_image(self, angle):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        rotated = self.current_image.rotate(angle, expand=True)
        self.display_image(rotated)
        self.status_label.config(text=f"Rotated {angle}°")
    
    def flip_horizontal(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        flipped = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.display_image(flipped)
        self.status_label.config(text="Flipped horizontally")
    
    def flip_vertical(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        flipped = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
        self.display_image(flipped)
        self.status_label.config(text="Flipped vertically")
    
    def extract_lsb(self):
        if self.bit_planes is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # Show LSB (bit plane 0)
        self.bit_var.set("0")
        self.show_bit_plane()
        self.status_label.config(text="Extracted LSB (bit plane 0)")
    
    def xor_bit_planes(self):
        if self.bit_planes is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # XOR of all bit planes
        result = np.zeros_like(self.bit_planes[0])
        for plane in self.bit_planes:
            result = np.bitwise_xor(result, plane // 255)
        
        result = result * 255
        xor_image = Image.fromarray(result.astype(np.uint8))
        self.display_image(xor_image)
        self.status_label.config(text="XOR of all bit planes")
    
    def and_bit_planes(self):
        if self.bit_planes is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # AND of all bit planes
        result = np.ones_like(self.bit_planes[0]) * 255
        for plane in self.bit_planes:
            result = np.bitwise_and(result, plane)
        
        and_image = Image.fromarray(result.astype(np.uint8))
        self.display_image(and_image)
        self.status_label.config(text="AND of all bit planes")
    
    def or_bit_planes(self):
        if self.bit_planes is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # OR of all bit planes
        result = np.zeros_like(self.bit_planes[0])
        for plane in self.bit_planes:
            result = np.bitwise_or(result, plane)
        
        or_image = Image.fromarray(result.astype(np.uint8))
        self.display_image(or_image)
        self.status_label.config(text="OR of all bit planes")
    
    def extract_all_bit_planes(self):
        if self.bit_planes is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # Create a composite image of all bit planes
        rows = 2
        cols = 4
        plane_size = self.bit_planes[0].shape
        composite = np.zeros((plane_size[0] * rows, plane_size[1] * cols), dtype=np.uint8)
        
        for i in range(8):
            row = i // cols
            col = i % cols
            composite[row*plane_size[0]:(row+1)*plane_size[0], 
                     col*plane_size[1]:(col+1)*plane_size[1]] = self.bit_planes[i]
        
        composite_image = Image.fromarray(composite)
        self.display_image(composite_image)
        self.status_label.config(text="All 8 bit planes displayed in grid")
    
    def convert_to_hsv(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        hsv_image = self.current_image.convert('HSV')
        self.display_image(hsv_image)
        self.status_label.config(text="Converted to HSV color space")
    
    def convert_to_ycbcr(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        ycbcr_image = self.current_image.convert('YCbCr')
        self.display_image(ycbcr_image)
        self.status_label.config(text="Converted to YCbCr color space")
    
    def convert_to_lab(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # PIL doesn't have direct LAB conversion, so we'll use RGB->XYZ->LAB approximation
        # For simplicity, we'll convert to grayscale and display as LAB approximation
        lab_image = self.current_image.convert('L')
        self.display_image(lab_image)
        self.status_label.config(text="Converted to grayscale (LAB approximation)")
    
    def analyze_file_structure(self):
        if self.image_path is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            with open(self.image_path, 'rb') as f:
                data = f.read(1024)  # Read first 1KB
            
            # Simple file structure analysis
            info = f"File: {os.path.basename(self.image_path)}\n"
            info += f"Size: {os.path.getsize(self.image_path)} bytes\n"
            
            # Check for common file signatures
            if data[:4] == b'\x89PNG':
                info += "Type: PNG image\n"
                info += "Signature: PNG (Portable Network Graphics)\n"
            elif data[:3] == b'\xFF\xD8\xFF':
                info += "Type: JPEG image\n"
                info += "Signature: JPEG (Joint Photographic Experts Group)\n"
            elif data[:2] == b'BM':
                info += "Type: BMP image\n"
                info += "Signature: BMP (Bitmap)\n"
            elif data[:6] == b'GIF87a' or data[:6] == b'GIF89a':
                info += "Type: GIF image\n"
                info += "Signature: GIF (Graphics Interchange Format)\n"
            else:
                info += "Type: Unknown or custom format\n"
            
            # Show in message box
            messagebox.showinfo("File Structure Analysis", info)
            self.status_label.config(text="Analyzed file structure")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze file: {str(e)}")
    
    def extract_strings(self):
        if self.image_path is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            with open(self.image_path, 'rb') as f:
                data = f.read()
            
            # Extract printable strings (ASCII)
            strings = []
            current_string = []
            
            for byte in data:
                if 32 <= byte <= 126:  # Printable ASCII
                    current_string.append(chr(byte))
                else:
                    if len(current_string) >= 4:  # Minimum string length
                        strings.append(''.join(current_string))
                    current_string = []
            
            if len(current_string) >= 4:
                strings.append(''.join(current_string))
            
            # Create strings window
            strings_window = tk.Toplevel(self.root)
            strings_window.title("Extracted Strings")
            strings_window.geometry("600x400")
            
            text_widget = tk.Text(strings_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            scrollbar = ttk.Scrollbar(strings_window, command=text_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar.set)
            
            for s in strings[:100]:  # Show first 100 strings
                text_widget.insert(tk.END, s + '\n')
            
            if len(strings) > 100:
                text_widget.insert(tk.END, f"\n... and {len(strings) - 100} more strings\n")
            
            self.status_label.config(text=f"Extracted {len(strings)} strings")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract strings: {str(e)}")
    
    def compare_images(self):
        messagebox.showinfo("Info", "This feature would open two images for comparison.\nTo be implemented in future version.")
        self.status_label.config(text="Image comparison (placeholder)")
    
    def frame_browser(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        if not hasattr(self.current_image, 'is_animated') or not self.current_image.is_animated:
            messagebox.showinfo("Info", "This image is not animated (GIF).")
            return
        
        # Simple frame browser for GIFs
        frame_window = tk.Toplevel(self.root)
        frame_window.title("GIF Frame Browser")
        frame_window.geometry("400x300")
        
        ttk.Label(frame_window, text=f"Total frames: {self.current_image.n_frames}", font=('Arial', 10)).pack(pady=10)
        
        frame_var = tk.IntVar(value=0)
        frame_slider = ttk.Scale(frame_window, from_=0, to=self.current_image.n_frames-1, 
                                 variable=frame_var, orient=tk.HORIZONTAL)
        frame_slider.pack(fill=tk.X, padx=20, pady=10)
        
        def show_frame(frame_num):
            self.current_image.seek(frame_num)
            frame_photo = ImageTk.PhotoImage(self.current_image)
            frame_label.config(image=frame_photo)
            frame_label.image = frame_photo
            frame_num_label.config(text=f"Frame {frame_num + 1}/{self.current_image.n_frames}")
        
        frame_label = ttk.Label(frame_window)
        frame_label.pack(pady=10)
        
        frame_num_label = ttk.Label(frame_window, text="Frame 1/1")
        frame_num_label.pack()
        
        show_frame(0)
        frame_slider.config(command=lambda val: show_frame(int(float(val))))
        
        self.status_label.config(text="Opened GIF frame browser")
    
    def data_carving(self):
        if self.image_path is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        messagebox.showinfo("Data Carving", "This feature would attempt to carve embedded files from the image.\nTo be implemented in future version.")
        self.status_label.config(text="Data carving (placeholder)")
    
    def statistical_analysis(self):
        if self.image_array is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # Basic statistical analysis
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statistical Analysis")
        stats_window.geometry("400x300")
        
        if len(self.image_array.shape) == 3:
            channels = ['Red', 'Green', 'Blue']
            if self.image_array.shape[2] == 4:
                channels.append('Alpha')
            
            stats_text = ""
            for i, channel in enumerate(channels):
                channel_data = self.image_array[:, :, i]
                stats_text += f"{channel} Channel:\n"
                stats_text += f"  Min: {channel_data.min()}\n"
                stats_text += f"  Max: {channel_data.max()}\n"
                stats_text += f"  Mean: {channel_data.mean():.2f}\n"
                stats_text += f"  Std: {channel_data.std():.2f}\n\n"
        else:
            stats_text = "Grayscale Image:\n"
            stats_text += f"  Min: {self.image_array.min()}\n"
            stats_text += f"  Max: {self.image_array.max()}\n"
            stats_text += f"  Mean: {self.image_array.mean():.2f}\n"
            stats_text += f"  Std: {self.image_array.std():.2f}\n"
        
        text_widget = tk.Text(stats_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, stats_text)
        text_widget.config(state=tk.DISABLED)
        
        self.status_label.config(text="Performed statistical analysis")
    
    def noise_analysis(self):
        if self.image_array is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        messagebox.showinfo("Noise Analysis", "This feature would analyze noise patterns for steganalysis.\nTo be implemented in future version.")
        self.status_label.config(text="Noise analysis (placeholder)")
    
    def lsb_detection(self):
        if self.image_array is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        messagebox.showinfo("LSB Detection", "This feature would detect LSB steganography patterns.\nTo be implemented in future version.")
        self.status_label.config(text="LSB detection (placeholder)")
    
    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if filepath:
            try:
                # Get current displayed image (would need to track modifications)
                # For now, save the original/current image
                self.current_image.save(filepath)
                self.status_label.config(text=f"Saved to {os.path.basename(filepath)}")
                messagebox.showinfo("Success", f"Image saved successfully to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def show_about(self):
        about_text = """StegSolve GUI - Python Steganography Analysis Tool
        
Version: 1.0
Author: Python Implementation
        
A StegSolve-like tool for analyzing images for hidden data.
        
Features:
• Bit plane analysis (0-7)
• RGB channel separation
• Basic image operations
• File structure analysis
• String extraction
• Statistical analysis
        
This tool is for educational and security analysis purposes.
"""
        messagebox.showinfo("About StegSolve GUI", about_text)
    
    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = StegSolveGUI(root)
    app.run()


if __name__ == "__main__":
    main()
