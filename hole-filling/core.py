
import nibabel as nib
import numpy as np
from scipy.ndimage import label

# Load images
adc_img = nib.load("adc.nii.gz")
dwi_img = nib.load("dwi.nii.gz")
brain_mask = nib.load("brain_mask.nii.gz")  # Binary brain mask
data_adc = adc_img.get_fdata()
data_dwi = dwi_img.get_fdata()
mask = brain_mask.get_fdata()

# Define thresholds
adc_thresh = (100, 690)
dwi_thresh = (140, 700)

# Apply thresholds and mask
core_mask = (
    (data_adc >= adc_thresh[0]) & (data_adc <= adc_thresh[1]) &
    (data_dwi >= dwi_thresh[0]) & (data_dwi <= dwi_thresh[1]) &
    (mask > 0)
)

# Restrict to left hemisphere only (or right, depending on infarct side)
midline = core_mask.shape[0] // 2
core_mask[midline:, :, :] = 0

# Keep only largest connected component (big blob)
labeled_array, num_features = label(core_mask)
sizes = [(labeled_array == i).sum() for i in range(1, num_features + 1)]
if sizes:
    largest_label = np.argmax(sizes) + 1
    core_mask = (labeled_array == largest_label)
else:
    core_mask = np.zeros_like(core_mask)

# Save result
core_img = nib.Nifti1Image(core_mask.astype(np.uint8), affine=adc_img.affine)
nib.save(core_img, "core_mask.nii.gz")
