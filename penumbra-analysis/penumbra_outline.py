import nibabel as nib
import numpy as np
from scipy import ndimage
import os

# Load penumbra mask
penumbra_nii = nib.load("penumbra_mask.nii.gz")
penumbra = penumbra_nii.get_fdata()

# Generate 3D binary outline using morphological gradient
structure = ndimage.generate_binary_structure(3, 1)
dilated = ndimage.binary_dilation(penumbra, structure=structure)
eroded = ndimage.binary_erosion(penumbra, structure=structure)
outline = np.logical_xor(dilated, eroded).astype(np.uint8)

# Save the outline as a NIfTI image
outline_nii = nib.Nifti1Image(outline, affine=penumbra_nii.affine)
nib.save(outline_nii, "penumbra_outline_mask.nii.gz")

print("Saved penumbra outline mask as penumbra_outline_mask.nii.gz")
