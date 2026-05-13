import nibabel as nib
import numpy as np
from scipy.ndimage import binary_dilation, convolve
from skimage.morphology import diamond

#input is the segmentation mask file
nii = nib.load("FX21_CP.nii.gz") #copy path to your segmentation file
mask = nii.get_fdata().astype(np.uint8)
binary_mask = (mask > 0).astype(np.uint8)
patched_mask = binary_mask.copy()

#to count how many voxels have been added
added_voxels = 0

#4-connectivity kernel (no diagonals)
kernel_4 = np.array([[0, 1, 0],
                     [1, 0, 1],
                     [0, 1, 0]])

#helper function for diagonal patching (no two pixels on a single plane would be connected at one diagonal)
def fill_between(slice_2d, patched_slice, a, b, fill1, fill2):
    added = 0
    if slice_2d[a] == 1 and slice_2d[b] == 1 and slice_2d[fill1] == 0 and slice_2d[fill2] == 0:
        if patched_slice[fill1] == 0:
            patched_slice[fill1] = 1
            added += 1
        if patched_slice[fill2] == 0:
            patched_slice[fill2] = 1
            added += 1
    return added

#only looping over the saggital slices
for x in range(binary_mask.shape[0]):
    slice_2d = patched_mask[x, :, :]
    patched_slice = slice_2d.copy()
    slice_added_voxels = 0

    #patching up diagonals (step 1)
    for y in range(1, slice_2d.shape[0] - 1):
        for z in range(1, slice_2d.shape[1] - 1):
            slice_added_voxels += fill_between(slice_2d, patched_slice, (y, z), (y+1, z+1), (y+1, z), (y, z+1))
            slice_added_voxels += fill_between(slice_2d, patched_slice, (y, z+1), (y+1, z), (y, z), (y+1, z+1))
            slice_added_voxels += fill_between(slice_2d, patched_slice, (y, z), (y-1, z+1), (y-1, z), (y, z+1))
            slice_added_voxels += fill_between(slice_2d, patched_slice, (y, z+1), (y-1, z), (y, z), (y-1, z+1))

    #buffing up thin regions [neighbours<2] (step 2)
    neighbor_count = convolve(patched_slice, kernel_4, mode='constant', cval=0)
    thin_regions = ((patched_slice == 1) & (neighbor_count <= 2)).astype(np.uint8)

    dilated_thin = binary_dilation(thin_regions, structure=diamond(1))
    buffed = dilated_thin & (patched_slice == 0)

    slice_added_voxels += np.sum(buffed)

    #merging updated slices to a mask
    patched_mask[x, :, :] = patched_slice | buffed
    added_voxels += slice_added_voxels

#save new mask
nib.save(nib.Nifti1Image(patched_mask.astype(np.uint8), nii.affine), "FX21_newseg.nii.gz") #filled mask
diff = (patched_mask != binary_mask).astype(np.uint8)

#still contains some holes, would need manual finetuning

nib.save(nib.Nifti1Image(diff, nii.affine), "FX21_SegRefined.nii.gz") #mask containing only the newly added voxels [optional]