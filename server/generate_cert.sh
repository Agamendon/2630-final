#!/bin/bash
# Generate self-signed SSL certificate for localhost

mkdir -p certs

openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout certs/localhost-key.pem \
  -out certs/localhost-cert.pem \
  -days 365 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1"

echo "SSL certificates generated in certs/ directory:"
echo "  - certs/localhost-cert.pem (certificate)"
echo "  - certs/localhost-key.pem (private key)"

