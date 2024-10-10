import boto3
import subprocess
import json
import sys
import os

def fetch_vpcs_and_subnets():
    """Fetches all VPCs and their associated subnets from AWS."""
    session = boto3.Session()
    ec2_client = session.client("ec2")

    # Fetch all VPCs
    vpcs_response = ec2_client.describe_vpcs()
    vpc_configs = []

    for vpc in vpcs_response['Vpcs']:
        vpc_id = vpc['VpcId']
        cidr_block = vpc['CidrBlock']
        tags = {tag['Key']: tag['Value'] for tag in vpc.get('Tags', [])}

        # Fetch subnets for the VPC
        subnets_response = ec2_client.describe_subnets(
            Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
        )
        subnet_configs = []

        for subnet in subnets_response['Subnets']:
            subnet_id = subnet['SubnetId']
            subnet_cidr_block = subnet['CidrBlock']
            availability_zone = subnet['AvailabilityZone']
            subnet_tags = {tag['Key']: tag['Value'] for tag in subnet.get('Tags', [])}

            subnet_configs.append({
                "subnet_id": subnet_id,
                "cidr_block": subnet_cidr_block,
                "availability_zone": availability_zone,
                "tags": subnet_tags
            })

        vpc_configs.append({
            "vpc_id": vpc_id,
            "cidr_block": cidr_block,
            "tags": tags,
            "subnet_configs": subnet_configs
        })

    return vpc_configs

def write_tfvars_json(vpc_configs, aws_region, cwd):
    """Writes the variables to a terraform.auto.tfvars.json file."""
    tfvars = {
        "aws_region": aws_region,
        "vpc_configs": vpc_configs
    }

    tfvars_path = os.path.join(cwd if cwd else ".", "terraform.auto.tfvars.json")
    with open(tfvars_path, "w") as f:
        json.dump(tfvars, f, indent=2)
    print(f"Written variables to {tfvars_path}")

def run_terraform_command(command, cwd=None):
    """Runs a Terraform command."""
    if cwd and not os.path.isdir(cwd):
        print(f"Error: The directory '{cwd}' does not exist.")
        sys.exit(1)
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
    )
    stdout, stderr = process.communicate()
    if stdout:
        print(stdout.decode("utf-8"))
    if stderr:
        print(stderr.decode("utf-8"))
    # Do not exit on non-zero return code to allow for graceful handling

def init_terraform(cwd=None):
    """Initializes Terraform."""
    print("Initializing Terraform...")
    command = ["terraform", "init", "-reconfigure"]
    run_terraform_command(command, cwd=cwd)

def get_managed_resources(cwd=None):
    """Retrieves a list of resources currently managed by Terraform."""
    command = ["terraform", "state", "list"]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {' '.join(command)}")
        print(stderr.decode("utf-8"))
        sys.exit(1)
    resources = stdout.decode("utf-8").splitlines()
    return resources

def import_resources(vpc_configs, cwd=None):
    """Imports resources into Terraform state, skipping those already managed."""
    print("Importing resources...")
    # Get the list of managed resources
    managed_resources = get_managed_resources(cwd=cwd)
    for vpc_config in vpc_configs:
        vpc_id = vpc_config['vpc_id']
        vpc_resource = f'module.vpc_module.aws_vpc.vpcs["{vpc_id}"]'
        if vpc_resource in managed_resources:
            print(f"Skipping VPC {vpc_id}, already managed by Terraform.")
        else:
            print(f"Importing VPC: {vpc_id}")
            command = ["terraform", "import", vpc_resource, vpc_id]
            run_terraform_command(command, cwd=cwd)

        for subnet_config in vpc_config['subnet_configs']:
            subnet_id = subnet_config['subnet_id']
            subnet_resource = f'module.vpc_module.aws_subnet.subnets["{subnet_id}"]'
            if subnet_resource in managed_resources:
                print(f"Skipping Subnet {subnet_id}, already managed by Terraform.")
            else:
                print(f"Importing Subnet: {subnet_id}")
                command = ["terraform", "import", subnet_resource, subnet_id]
                run_terraform_command(command, cwd=cwd)

def plan_terraform(cwd=None):
    """Runs 'terraform plan'."""
    print("Planning Terraform...")
    command = ["terraform", "plan"]
    run_terraform_command(command, cwd=cwd)

# def apply_terraform(cwd=None):
#     """Runs 'terraform apply' with auto-approval."""
#     print("Applying Terraform...")
#     command = ["terraform", "apply", "-auto-approve"]
#     run_terraform_command(command, cwd=cwd)

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Set the working directory to 'child_module' relative to the script directory
    working_directory = os.path.join(script_dir, "child_module")

    # Verify that the child_module directory exists
    if not os.path.isdir(working_directory):
        print(f"Error: The directory '{working_directory}' does not exist.")
        sys.exit(1)

    aws_region = "us-east-1"  # Update as needed

    # Fetch all VPCs and their subnets
    vpc_configs = fetch_vpcs_and_subnets()

    # Write variables to a .tfvars.json file
    write_tfvars_json(vpc_configs, aws_region, cwd=working_directory)

    # Initialize Terraform
    init_terraform(cwd=working_directory)

    # Import the resources into Terraform state
    import_resources(vpc_configs, cwd=working_directory)

    # Plan and Apply Terraform with imported resources
    plan_terraform(cwd=working_directory)
    # apply_terraform(cwd=working_directory)
