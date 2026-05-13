<h2 align="center">MRI Tools</h2>
<p align="center">
  A collection of medical image processing tools for MRI segmentation —
  cropping, mask hole filling, and penumbra analysis.
</p>


<hr>

<h3>📁 Tools</h3>

<table>
  <tr>
    <th>#</th>
    <th>Tool</th>
    <th>Description</th>
    <th>Key Libraries</th>
  </tr>
  <tr>
    <td>1</td>
    <td><a href="cropping-tool/"><b>MRI Cropping Tool</b></a></td>
    <td>GUI-based and coordinate-based cropping of high-resolution MRI images (.tif, .tiff, .jp2)</td>
    <td>OpenCV, tifffile, glymur, NumPy</td>
  </tr>
  <tr>
    <td>2</td>
    <td><a href="hole-filling/"><b>Mask Hole Filling</b></a></td>
    <td>Post-processing tool for NIfTI segmentation masks — fills diagonal disconnections and buffers thin regions</td>
    <td>NiBabel, NumPy, SciPy, scikit-image</td>
  </tr>
  <tr>
    <td>3</td>
    <td><a href="penumbra-analysis/"><b>Penumbra Analysis Pipeline</b></a></td>
    <td>5-step pipeline for ischemic stroke penumbra analysis — SWI registration, infarct core segmentation, hypoperfused region detection, penumbra computation, and 3D outline generation</td>
    <td>NiBabel, NumPy, SciPy, SimpleITK</td>
  </tr>
</table>

<hr>

<h3>🗂️ Repository Structure</h3>
<pre><code>mri-tools/
├── cropping-tool/
│   ├── crop.py
│   ├── brain_downsampled.tif
│   ├── autocrop_brain_downsampled.tif
│   └── README.md
├── hole-filling/
│   ├── hole_fill.py
│   ├── image.png
│   └── README.md
├── penumbra-analysis/
│   ├── reg.py
│   ├── core.py
│   ├── hypoperfused.py
│   ├── penumbra.py
│   ├── penumbra_outline.py
│   ├── penumbra_outline.png
│   └── README.md
└── README.md
</code></pre>

<hr>

<h3>🛠️ Tech Stack</h3>
<ul>
  <li>Python</li>
  <li>NiBabel — NIfTI file I/O</li>
  <li>SimpleITK — image registration</li>
  <li>OpenCV — GUI display and mouse interaction</li>
  <li>SciPy — morphological operations, connected components</li>
  <li>tifffile / glymur — TIFF and JPEG2000 support</li>
  <li>NumPy — array operations</li>
</ul>

<hr>

<h3>🏫 Context</h3>
<p>
  All tools were built during a Summer Research Internship at the
  <b>Sudha Gopalakrishnan Brain Centre, IIT Madras</b>
  as part of a foetal and adult brain MRI preprocessing and analysis pipeline.
</p>
