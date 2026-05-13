import nibabel as nib
import numpy as np

# Load infarct and vein masks
core = nib.load("infarct_mask.nii.gz").get_fdata().astype(bool)
veins = nib.load("vein_mask.nii.gz").get_fdata().astype(bool)
affine = nib.load("infarct_mask.nii.gz").affine

# Penumbra = veins minus infarct
penumbra = veins & (~core)

# Save penumbra
nib.save(nib.Nifti1Image(penumbra.astype(np.uint8), affine), "penumbra_mask.nii.gz")
