import logging
import uuid
import os
from barcode import Code128
from barcode.writer import ImageWriter
from typing import Literal

def generate_barcode(uuid_value: uuid.UUID, pertinent_to: Literal["patron", "copy"]) -> str:
    os.makedirs(f"{pertinent_to}_barcodes", exist_ok=True)    
    barcode = Code128(str(uuid_value), writer=ImageWriter())    
    barcode_path = os.path.join(output_dir, f"{pertinent_to}_{uuid_value}.png")    
    barcode.save(barcode_path)
    return barcode_path