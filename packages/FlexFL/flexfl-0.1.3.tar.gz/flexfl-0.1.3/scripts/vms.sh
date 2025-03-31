#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

KEY_NAME="fl"
KEY_PATH="keys/$KEY_NAME"
VM_LIST="scripts/hostfile.txt" # needs to end in empty line
USERNAME=$VM_USERNAME
PASSWORD=$VM_PASSWORD

# Check VM list
if [ ! -f "$VM_LIST" ]; then
    echo "Error: VM list file '$VM_LIST' not found!"
    exit 1
fi

# Generate SSH key if it doesn't exist
if [ ! -f "$KEY_PATH" ]; then
    echo "Generating SSH key..."
    mkdir -p keys
    ssh-keygen -t rsa -b 4096 -f "$KEY_PATH" -N "" > /dev/null 2>&1
    echo "SSH key generated at $KEY_PATH"
fi

# Copy SSH key to each VM
while read -r IP; do
    echo "Setting up $IP..." &&
    ssh-keyscan -H "$IP" >> ~/.ssh/known_hosts > /dev/null 2>&1 &&
    sshpass -p "$PASSWORD" ssh-copy-id -f -i "$KEY_PATH.pub" "$USERNAME@$IP" > /dev/null 2>&1 &&
    sshpass -p "$PASSWORD" scp "$KEY_PATH" "$USERNAME@$IP:~/.ssh/" &&
    sshpass -p "$PASSWORD" ssh "$USERNAME@$IP" "chmod 600 ~/.ssh/$KEY_NAME && touch ~/.ssh/known_hosts && mkdir scripts" &&
    sshpass -p "$PASSWORD" scp "$VM_LIST" "$USERNAME@$IP:~/$VM_LIST" &&
    sshpass -p "$PASSWORD" scp "scripts/vm.sh" "$USERNAME@$IP:~/scripts/vm.sh" &&
    echo "Running setup script on $IP..." &&
    sshpass -p "$PASSWORD" ssh "$USERNAME@$IP" "bash ~/scripts/vm.sh" > /dev/null 2>&1 &&
    echo "$IP setup done!" &
done < "$VM_LIST"
# Wait for all background jobs to finish
wait

echo "SSH setup completed!"
