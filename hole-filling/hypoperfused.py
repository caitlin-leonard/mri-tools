import nibabel as nib
import numpy as np
import scipy.ndimage as ndi

# Load SWI
swi = nib.load("swi_reg.nii.gz")
swi_data = swi.get_fdata()
affine = swi.affine

# Threshold at top 5%
swi_thresh = np.percentile(swi_data, 95)
vein_mask = swi_data > swi_thresh

# Keep largest vein clusters
labeled, n = ndi.label(vein_mask)
sizes = ndi.sum(vein_mask, labeled, range(1, n + 1))
sorted_ids = np.argsort(sizes)[::-1]
filtered = np.zeros_like(vein_mask)

for idx in sorted_ids[:5]:  # Top 5 blobs
    filtered |= (labeled == (idx + 1))

# Restrict to same hemisphere
hemisphere = np.load("hemisphere.npy", allow_pickle=True).item()
final_veins = np.zeros_like(filtered)
labeled_veins, n_vein = ndi.label(filtered)

for i in range(1, n_vein + 1):
    blob = labeled_veins == i
    com = ndi.center_of_mass(blob)
    if (hemisphere == "left" and com[0] < swi_data.shape[0] // 2) or \
       (hemisphere == "right" and com[0] >= swi_data.shape[0] // 2):
        final_veins |= blob

# Save vein mask
nib.save(nib.Nifti1Image(final_veins.astype(np.uint8), affine), "vein_mask.nii.gz")
