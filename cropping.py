import os, cv2, tifffile, glymur, numpy as np

def load(ip):
    ext = os.path.splitext(ip)[1].lower()
    if ext in [".tif", ".tiff"]:
        image = tifffile.imread(ip)
    elif ext == ".jp2":
        image = glymur.Jp2k(ip)[:]
    else:
        raise ValueError("ERROR - can only use .tif, .tiff, or .jp2 file formats")
    return image, ext

def save(image, ext, op):
    if ext in [".tif", ".tiff"]:
        tifffile.imwrite(op, image, compression=None)
    elif ext == ".jp2":
        glymur.Jp2k(op, data=image)
    print(f"Saved cropped image to: {op}")

def coord(ip, x1, x2, y1, y2):
    image, ext = load(ip)
    h, w = image.shape[:2]
    x1, x2 = sorted([max(0, x1), min(w, x2)])
    y1, y2 = sorted([max(0, y1), min(h, y2)])
    print(f"cropped coordinates: x1={x1}, x2={x2}, y1={y1}, y2={y2}")
    print(f"cropped size: width={x2 - x1}, height={y2 - y1}")
    cropped = image[y1:y2, x1:x2]
    op = os.path.join(os.path.dirname(ip), f"autocrop_{os.path.basename(ip)}")
    print("Saving:", op)
    print("Shape:", cropped.shape)
    print("Dtype:", cropped.dtype)
    print("Min:", cropped.min(), "Max:", cropped.max())
    save(cropped, ext, op)

def click_crop(e, x, y, f, p):
    global ref, cropping
    if e == cv2.EVENT_LBUTTONDOWN:
        ref[:] = [(x, y)]
        cropping = True
    elif e == cv2.EVENT_LBUTTONUP:
        ref.append((x, y))
        cropping = False
        cv2.rectangle(p, ref[0], ref[1], (0, 255, 0), 2)
        cv2.imshow("image", p)

def manual(ip):
    global ref
    ref = []
    image, ext = load(ip)
    image_disp = image
    if image_disp.dtype != np.uint8:
        norm = (image_disp - image_disp.min()) / (image_disp.ptp() + 1e-5)
        image_disp = (255 * norm).astype("uint8")
    if len(image_disp.shape) == 2:
        image_disp = cv2.cvtColor(image_disp, cv2.COLOR_GRAY2BGR)

    clone = image_disp.copy()
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", click_crop, clone)
    print("Drag to select ROI, then press Enter to crop")

    while True:
        cv2.imshow("image", clone)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # Enter key
            break
    cv2.destroyAllWindows()

    if len(ref) == 2:
        x1, y1 = ref[0]
        x2, y2 = ref[1]
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        print(f"cropped coordinates: x1={x1}, x2={x2}, y1={y1}, y2={y2}")
        print(f"cropped size: width={x2 - x1}, height={y2 - y1}")
        cropped = image[y1:y2, x1:x2]
        op = os.path.join(os.path.dirname(ip), f"autocrop_{os.path.basename(ip)}")
        print("Saving:", op)
        print("Shape:", cropped.shape)
        print("Dtype:", cropped.dtype)
        print("Min:", cropped.min(), "Max:", cropped.max())
        save(cropped, ext, op)
        return (x1, x2, y1, y2)
    else:
        print("Cropping not completed.")
        return None

def main():
    while True:
        a = int(input('1 - Manual crop, 2 - Crop by coordinates, 3 - Exit:'))
        b = input('Enter file name: ')
        if a == 1:
            manual(b)
        elif a == 2:
            n = input('Enter the coordinates x1 x2 y1 y2: ').strip().split()
            x1, x2, y1, y2 = map(int, n)
            coord(b, x1, x2, y1, y2)
        else:
            break

if __name__ == "__main__":
    main()
