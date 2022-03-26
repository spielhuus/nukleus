#!/bin/bash
set -e

USER_UID=${USER_UID:-1000}
USER_GID=${USER_GID:-1000}
USERNAME=${USERNAME:-hugo}

function create_user()
{
    groupadd -f -g $USER_GID $USERNAME #2> /dev/null # group
    useradd -d $WORKSPACE -M -s /bin/bash -u $USER_UID -g $USERNAME $USERNAME  #2> /dev/null # user
    echo "$USERNAME ALL=NOPASSWD:ALL" >> /etc/sudoers
}

# Create the user
create_user

# Execute the rest of the script with the new user
su $USERNAME -- /entrypoint-user.sh "$@"
