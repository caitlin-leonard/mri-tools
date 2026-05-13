<h2 align="center">MRI Cropping Tool</h2>
<p align="center">
  A GUI-based cropping tool for high-resolution medical MRI images —
  supports manual ROI selection and coordinate-based cropping
  for <code>.tif</code>, <code>.tiff</code>, and <code>.jp2</code> formats.
</p>

<hr>

<h3>🧠 Overview</h3>
<p>
Medical MRI scans are often large high-resolution volumes that need to be cropped
to isolate regions of interest (ROI) for further analysis. This tool provides two modes —
an interactive GUI for manual selection and a coordinate-based mode for scripted/batch cropping.
It handles high-bit-depth images (16-bit MRI) correctly, displaying a normalised 8-bit preview
while cropping the original full-resolution data.
</p>

<hr>

<h3>⚙️ Features</h3>
<ul>
  <li>🖱️ <b>Manual GUI crop</b> — drag to draw ROI, press Enter to crop</li>
  <li>📐 <b>Coordinate-based crop</b> — input exact pixel coordinates (x1 x2 y1 y2)</li>
  <li>🏥 <b>Medical format support</b> — <code>.tif</code>/<code>.tiff</code> (tifffile) and <code>.jp2</code> JPEG2000 (glymur)</li>
  <li>🔬 <b>High-bit-depth safe</b> — normalises 16-bit MRI to 8-bit for display only; crops original data</li>
  <li>✅ <b>Bounds checking</b> — clamps coordinates to image dimensions, never crashes on out-of-range input</li>
  <li>📊 <b>Crop diagnostics</b> — prints shape, dtype, min/max of cropped region for verification</li>
  <li>💾 <b>Auto-save</b> — saves output as <code>autocrop_filename</code> in the same directory</li>
</ul>

<hr>

<h3>▶️ How to Run</h3>

<h4>Install dependencies</h4>
<pre><code>pip install opencv-python tifffile glymur numpy</code></pre>

<h4>Run the tool</h4>
<pre><code>python crop.py</code></pre>

<h4>Usage</h4>
<pre><code>1 - Manual crop, 2 - Crop by coordinates, 3 - Exit: 1
Enter file name: brain_downsampled.tif
→ GUI window opens — drag to select ROI, press Enter to crop
→ Saves as autocrop_brain_downsampled.tif

1 - Manual crop, 2 - Crop by coordinates, 3 - Exit: 2
Enter file name: brain_downsampled.tif
Enter the coordinates x1 x2 y1 y2: 100 400 200 600
→ Saves as autocrop_brain_downsampled.tif
</code></pre>

<hr>

<h3>📁 Output</h3>
<pre><code>cropped coordinates: x1=100, x2=400, y1=200, y2=600
cropped size: width=300, height=400
Saving: autocrop_brain_downsampled.tif
Shape: (400, 300, 3)
Dtype: uint16
Min: 102  Max: 4891
Saved cropped image to: autocrop_brain_downsampled.tif
</code></pre>

<hr>

<h3>🛠️ Tech Stack</h3>
<ul>
  <li>Python</li>
  <li>OpenCV — GUI display and mouse interaction</li>
  <li>tifffile — TIFF read/write</li>
  <li>glymur — JPEG2000 (.jp2) read/write</li>
  <li>NumPy — array operations</li>
</ul>

<hr>


