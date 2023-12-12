import os

ca_cert_file = 'python_scripts/us-east-2-bundle.p7b'  # Replace with the actual path to your CA certificate file

# Check if the file exists
if os.path.exists(ca_cert_file):
    # Check if the script has read access to the file
    if os.access(ca_cert_file, os.R_OK):
        print(f"The Python script has read access to '{ca_cert_file}'.")
    else:
        print(f"The Python script does not have read access to '{ca_cert_file}'.")
else:
    print(f"The file '{ca_cert_file}' does not exist.")