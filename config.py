# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

class BaseConfig(object):

    # Can be set to 'MasterUser' or 'ServicePrincipal'
    AUTHENTICATION_MODE = 'ServicePrincipal'

    # Workspace Id in which the report is present
    WORKSPACE_ID = 'f29a7928-82e5-4a70-a517-9982210dee1f'
    
    # Report Id for which Embed token needs to be generated
    REPORT_ID = 'd6a28c7b-ed76-48f2-baa5-a56a3b9f1963'
    
    CUSTOM_REPORT_ID = '54f6dd95-c35c-4802-abac-69883afa0620'
    
    # Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
    TENANT_ID = '5b04df60-cde4-4be5-be64-827f13c2e760'
    
    # Client Id (Application Id) of the AAD app
    CLIENT_ID = 'f0535ab1-36a8-4186-baac-200021f2c8ad'
    
    # Client Secret (App Secret) of the AAD app. Required only for ServicePrincipal authentication mode.
    CLIENT_SECRET = 'C1P7Q~L5KDHG9coxeOlm.~5cunAswX8nXqQkg'
    
    # Scope of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
    SCOPE = ['https://analysis.windows.net/powerbi/api/.default']
    
    # URL used for initiating authorization request
    AUTHORITY = 'https://login.microsoftonline.com/organizations'
    
    # Master user email address. Required only for MasterUser authentication mode.
    POWER_BI_USER = ''
    
    # Master user email password. Required only for MasterUser authentication mode.
    POWER_BI_PASS = ''