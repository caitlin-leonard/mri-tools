import SimpleITK as sitk

# === Input paths ===
adc_path = "adc.nii.gz"
swi_path = "swi.nii.gz"
output_path = "swi_reg.nii.gz"

# === Load fixed (ADC) and moving (SWI) images ===
fixed = sitk.ReadImage(adc_path, sitk.sitkFloat32)
moving = sitk.ReadImage(swi_path, sitk.sitkFloat32)

# === Initialize transform (rigid) ===
initial_transform = sitk.CenteredTransformInitializer(
    fixed, moving, sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.GEOMETRY
)

# === Set up registration method ===
registration_method = sitk.ImageRegistrationMethod()
registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
registration_method.SetInterpolator(sitk.sitkLinear)
registration_method.SetOptimizerAsRegularStepGradientDescent(
    learningRate=2.0, minStep=1e-4, numberOfIterations=200,
    gradientMagnitudeTolerance=1e-6
)
registration_method.SetInitialTransform(initial_transform, inPlace=False)
registration_method.SetShrinkFactorsPerLevel([4, 2, 1])
registration_method.SetSmoothingSigmasPerLevel([2, 1, 0])
registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

# === Execute registration ===
final_transform = registration_method.Execute(fixed, moving)

# === Apply transform to SWI and save output ===
resampled_swi = sitk.Resample(moving, fixed, final_transform, sitk.sitkLinear, 0.0, moving.GetPixelID())
sitk.WriteImage(resampled_swi, output_path)

print(f"✅ Registered SWI saved to: {output_path}")
