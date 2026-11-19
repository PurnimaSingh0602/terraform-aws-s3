
import re
import sys
from pathlib import Path

# Read Terraform configuration
terraform_file = Path("main.tf")

if not terraform_file.exists():
    print("ERROR: main.tf not found")
    sys.exit(1)

source = terraform_file.read_text(encoding="utf-8")

violations = []

def get_resource(resource_type):
    pattern = (
        r'resource\s+"' + re.escape(resource_type) +
        r'"\s+"[^"]+"\s*\{(.*?)(?=\nresource\s+"|\Z)'
    )
    match = re.search(pattern, source, re.DOTALL)
    return match.group(1) if match else None


# Policy 1: S3 public access must be blocked
public_block = get_resource("aws_s3_bucket_public_access_block")

if public_block and all(
    re.search(r"\b" + setting + r"\s*=\s*true\b", public_block)
    for setting in [
        "block_public_acls",
        "block_public_policy",
        "ignore_public_acls",
        "restrict_public_buckets"
    ]
):
    print("PASS: S3 public access is blocked")
else:
    print("FAIL: S3 public access is not fully blocked")
    violations.append("Public access protection")


# Policy 2: S3 encryption must use AES256
encryption = get_resource("aws_s3_bucket_server_side_encryption_configuration")

if encryption and re.search(r'sse_algorithm\s*=\s*"AES256"', encryption):
    print("PASS: S3 AES256 encryption is enabled")
else:
    print("FAIL: S3 AES256 encryption is missing")
    violations.append("S3 encryption")


# Policy 3: S3 bucket versioning must be enabled
versioning = get_resource("aws_s3_bucket_versioning")

if versioning and re.search(r'status\s*=\s*"Enabled"', versioning):
    print("PASS: S3 bucket versioning is enabled")
else:
    print("FAIL: S3 bucket versioning is disabled")
    violations.append("S3 versioning")


# Final compliance result
print("\nCOMPLIANCE CHECK RESULTS")

if violations:
    print("Compliance Status: FAILED")
    print("Violations:", ", ".join(violations))
    sys.exit(1)
else:
    print("Compliance Status: PASSED")
    sys.exit(0)

