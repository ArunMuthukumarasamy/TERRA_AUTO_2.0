import boto3
import subprocess

# List of AWS regions where you want to import VPCs
regions = ["us-east-1", "us-west-2"]  # Add other regions if needed

def get_vpcs(region):
    """
    Get list of VPCs in a specific AWS region
    """
    ec2_client = boto3.client("ec2", region_name=region)
    response = ec2_client.describe_vpcs()
    vpcs = response.get("Vpcs", [])
    return vpcs

def terraform_import(vpc_id, region):
    """
    Run the terraform import command to import the VPC
    """
    # Corrected the -var flag quoting
    terraform_cmd = f"terraform import -var=\"aws_region={region}\" -var=\"vpc_id={vpc_id}\" aws_vpc.imported_vpc {vpc_id}"
    print(f"Running: {terraform_cmd} in region: {region}")
    
    # Run the Terraform import command
    subprocess.run(terraform_cmd, shell=True, check=True)

def main():
    for region in regions:
        print(f"Fetching VPCs from region: {region}")
        vpcs = get_vpcs(region)
        
        for vpc in vpcs:
            vpc_id = vpc.get("VpcId")
            print(f"Importing VPC: {vpc_id} from region: {region}")
            
            # Run terraform import
            terraform_import(vpc_id, region)

if __name__ == "__main__":
    main()
