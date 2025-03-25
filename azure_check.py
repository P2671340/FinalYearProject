from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient

def check_azure_vms():
    # Use Azure CLI Credential for authentication
    credential = AzureCliCredential()

    # Replace with your Azure subscription ID
    subscription_id = '1456672b-c10a-44ab-8058-6847fda2cef3'

    # Initialize the Azure ComputeManagementClient with the credential
    compute_client = ComputeManagementClient(credential, subscription_id)

    # List all virtual machines in the specified resource group
    vms = compute_client.virtual_machines.list('FinalYearProject')
    
    misconfigurations = []

    # Check for misconfigurations in VM size
    for vm in vms:
        if vm.hardware_profile.vm_size != "Standard_DS1_v2":
            misconfigurations.append(f"VM {vm.name} is not using the recommended size (Standard_DS1_v2).")

    return misconfigurations