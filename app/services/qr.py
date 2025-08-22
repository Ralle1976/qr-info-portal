import qrcode
from qrcode.image.svg import SvgPathImage
import io
import os
from pathlib import Path


class QRService:
    """Service for generating QR codes"""
    
    @staticmethod
    def generate_qr_png(data: str, size: int = 10) -> bytes:
        """Generate QR code as PNG bytes"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        byte_io = io.BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        return byte_io.getvalue()
    
    @staticmethod
    def generate_qr_svg(data: str) -> str:
        """Generate QR code as SVG string"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(image_factory=SvgPathImage)
        
        # Convert to string
        byte_io = io.BytesIO()
        img.save(byte_io)
        byte_io.seek(0)
        
        return byte_io.getvalue().decode('utf-8')
    
    @staticmethod
    def save_qr_files(url: str, base_path: str = 'app/static/qr'):
        """Save QR codes as PNG and SVG files"""
        # Ensure directory exists
        Path(base_path).mkdir(parents=True, exist_ok=True)
        
        # Generate and save PNG
        png_data = QRService.generate_qr_png(url)
        png_path = os.path.join(base_path, 'portal.png')
        with open(png_path, 'wb') as f:
            f.write(png_data)
        
        # Generate and save SVG
        svg_data = QRService.generate_qr_svg(url)
        svg_path = os.path.join(base_path, 'portal.svg')
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_data)
        
        return {
            'png': png_path,
            'svg': svg_path
        }