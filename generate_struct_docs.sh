#!/bin/bash

structs=(
    "Role"
    "AcPolicy"
    "Account"
    "AccountPasswordPolicy"
    "Cdn"
    "Cen"
    "ImageRepository"
    "ContainerImage"
    "Crt"
    "Db"
    "Ebs"
    "Ecr"
    "Ecs"
    "Eip"
    "Eni"
    "Firewall"
    "Image"
    "IPsec"
    "LaunchTemplates"
    "LoadBalance"
    "Mfa"
    "Mq"
    "NatGateway"
    "NatGateway2"
    "NatFirewall"
    "OssBucket"
    "Project_"
    "RouteTable"
    "Sas"
    "SecurityGroup"
    "Snapshot"
    "StorageAccount"
    "Subnet"
    "Vpc"
    "VpcPeer"
    "VpnGateway"
    "Waf"
    "Zone_"
)

for struct in "${structs[@]}"; do
    echo "Processing $struct..."
    output_file="${struct}.md"
    
    if ./struct_print.exe -dir . -struct "$struct" > "$output_file"; then
        echo "Successfully created $output_file"
    else
        echo "Error processing $struct"
    fi
done

echo "All structs processed!"
