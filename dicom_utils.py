import logging
from pydicom import dcmread
from PIL import Image
import numpy as np
import os

logger = logging.getLogger(__name__)

def extract_dicom_tag(filepath: str, tag: str):
    """
    Extracts the value of the given DICOM tag from the file.
    :param filepath: Path to the DICOM file.
    :param tag: DICOM tag (e.g., 'PatientName').
    :return: Tag value or None if not found.
    """
    try:
        dcm = dcmread(filepath)
        if hasattr(dcm, tag):
            return getattr(dcm, tag)
        return dcm.get(tag)
    except Exception as e:
        logger.error("Error extracting tag %s from %s: %s", tag, filepath, e)
        return None

def convert_dicom_to_png(filepath: str, output_dir: str):
    """
    Converts the pixel data of a DICOM file to PNG.
    :param filepath: Path to the DICOM file.
    :param output_dir: Directory to save the PNG.
    :return: Path to the PNG file, or None on failure.
    """
    try:
        dcm = dcmread(filepath)
        arr = dcm.pixel_array.astype(float)
        arr = (np.maximum(arr, 0) / arr.max()) * 255.0
        img = Image.fromarray(arr.astype('uint8'))
        out_name = os.path.splitext(os.path.basename(filepath))[0] + '.png'
        png_path = os.path.join(output_dir, out_name)
        img.save(png_path)
        logger.info("Converted %s to %s", filepath, png_path)
        return png_path
    except Exception as e:
        logger.error("Error converting %s to PNG: %s", filepath, e)
        return None
