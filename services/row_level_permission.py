# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license

class PermissionConfig:

    # Camel casing is used for the member variables as they are going to be serialized and camel case is standard for JSON keys

    accessLevel = None
    identities = []
    username = ""
    roles = []
    datasets = []

    def __init__(self, accessLevel, identities, username, roles, datasets):
        self.accessLevel = accessLevel
        self.identities = identities
        self.identities.append({
            "username": username,
            "roles": roles,
            "datasets": datasets
        })
