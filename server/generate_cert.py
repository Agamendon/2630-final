#!/usr/bin/env python3
"""
Generate self-signed SSL certificate for localhost
Alternative to the shell script for cross-platform compatibility
"""

import subprocess
import os
from pathlib import Path

def generate_certificates():
    """Generate self-signed SSL certificates for localhost"""
    certs_dir = Path("certs")
    certs_dir.mkdir(exist_ok=True)
    
    cert_path = certs_dir / "localhost-cert.pem"
    key_path = certs_dir / "localhost-key.pem"
    
    # Check if certificates already exist
    if cert_path.exists() and key_path.exists():
        print("Certificates already exist. Delete them first if you want to regenerate.")
        return
    
    try:
        # Generate certificate using openssl
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:4096", "-nodes",
            "-keyout", str(key_path),
            "-out", str(cert_path),
            "-days", "365",
            "-subj", "/CN=localhost",
            "-addext", "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1"
        ], check=True)
        
        print("SSL certificates generated successfully!")
        print(f"  - {cert_path} (certificate)")
        print(f"  - {key_path} (private key)")
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating certificates: {e}")
        print("Make sure OpenSSL is installed on your system.")
    except FileNotFoundError:
        print("Error: OpenSSL not found. Please install OpenSSL or use the shell script.")
        print("On macOS: brew install openssl")
        print("On Linux: sudo apt-get install openssl (or equivalent)")
        print("On Windows: Install OpenSSL from https://slproweb.com/products/Win32OpenSSL.html")

if __name__ == "__main__":
    generate_certificates()

