#hongcheng

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def resize_images(img1, img2, size=(256, 256)):
    """ Resize two images to the same size. """
    return cv2.resize(img1, size), cv2.resize(img2, size)


def determine_patch_size(img, num_patches=64):
    """ Determine patch size based on image dimensions and desired number of patches. """
    height, width = img.shape[:2]
    aspect_ratio = width / height
    patch_area = (width * height) / num_patches
    patch_width = int(math.sqrt(patch_area * aspect_ratio))
    patch_height = int(patch_area / patch_width)
    return (patch_height, patch_width)

def split_into_patches(img, patch_size):
    """ Split an image into patches based on given patch size. """
    patches = []
    for i in range(0, img.shape[0], patch_size[0]):
        for j in range(0, img.shape[1], patch_size[1]):
            patch = img[i:i + patch_size[0], j:j + patch_size[1]]
            patches.append(patch)
    return patches


# def split_into_patches(img, patch_size=(32, 32)):
#     """ Split an image into patches. """
#     return [img[i:i + patch_size[0], j:j + patch_size[1]] 
#             for i in range(0, img.shape[0], patch_size[0]) 
#             for j in range(0, img.shape[1], patch_size[1])]

def mse(patch1, patch2):
    """ Calculate Mean Squared Error between two patches. """
    err = np.sum((patch1.astype("float") - patch2.astype("float")) ** 2)
    err /= float(patch1.shape[0] * patch1.shape[1])
    return err

def histogram_similarity(patch1, patch2):
    """ Calculate Histogram Similarity between two patches. """
    hist1 = cv2.calcHist([patch1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([patch2], [0], None, [256], [0, 256])
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

def compare_patches(patches1, patches2, ssim_threshold=0.5, mse_threshold=100, hist_threshold=0.5):
    """ Compare two sets of patches using SSIM, MSE, and Histogram Similarity. """
    ssim_scores, mse_scores, hist_scores = [], [], []
    ssim_above_threshold, mse_above_threshold, hist_above_threshold = 0, 0, 0
    for patch1, patch2 in zip(patches1, patches2):
        ssim_score = ssim(patch1, patch2, multichannel=True)
        mse_score = mse(patch1, patch2)
        hist_score = histogram_similarity(patch1, patch2)
        ssim_scores.append(ssim_score)
        mse_scores.append(mse_score)
        hist_scores.append(hist_score)
        if ssim_score > ssim_threshold:
            ssim_above_threshold += 1
        if mse_score > mse_threshold:
            mse_above_threshold += 1
        if hist_score > hist_threshold:
            hist_above_threshold += 1
    return ssim_scores, mse_scores, hist_scores, ssim_above_threshold, mse_above_threshold, hist_above_threshold

def main(image_path1, image_path2):
    # Load images
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # Resize images
    img1_resized, img2_resized = resize_images(img1, img2)

# Determine patch size based on image dimensions
    patch_size = determine_patch_size(img1_resized, num_patches)

    # Split images into patches
    patches1 = split_into_patches(img1_resized, patch_size)
    patches2 = split_into_patches(img2_resized, patch_size)

    # # Split images into patches
    # patches1 = split_into_patches(img1_resized)
    # patches2 = split_into_patches(img2_resized)

    # Compare patches
    ssim_scores, mse_scores, hist_scores, ssim_above_threshold, mse_above_threshold, hist_above_threshold = compare_patches(patches1, patches2)

    # Calculate overall differences and threshold ratios
    overall_ssim_diff = 1 - np.mean(ssim_scores)
    overall_mse_diff = np.mean(mse_scores)
    overall_hist_diff = np.mean(hist_scores)
    ssim_threshold_ratio = ssim_above_threshold / len(patches1)
    mse_threshold_ratio = mse_above_threshold / len(patches1)
    hist_threshold_ratio = hist_above_threshold / len(patches1)

    print(f"Overall SSIM Difference: {overall_ssim_diff}")
    print(f"Overall MSE Difference: {overall_mse_diff}")
    print(f"Overall Histogram Similarity: {overall_hist_diff}")
    print(f"Ratio of Patches with SSIM > 0.5: {ssim_threshold_ratio}")
    print(f"Ratio of Patches with MSE > 100: {mse_threshold_ratio}")
    print(f"Ratio of Patches with Histogram Similarity > 0.5: {hist_threshold_ratio}")
