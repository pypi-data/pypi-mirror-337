from .version import __version__
from typing import List

class AwsGateway:
    API_GATEWAY = 1,
    PRIVATE_API_GATEWAY = 2,
    GOV_API_GATEWAY = 3,
    GOV_PRIVATE_API_GATEWAY = 4

def request_account_privileges(privileges: [str]) -> None:
    """Requests privileges from the consumer specified by a string array passed to the function
    that contains the privileges. The specified privileges must be listed in the manifest file.

    Args:
        privileges: list of account level privileges

    Returns:
        None
    """
    pass

def request_reference(reference: str) -> None:
    """Requests a reference from the consumer specified by the string passed to the function.
    The reference passed to the function must be defined in the manifest file.
    Refer to Object types and privileges that a reference can contain for the objects that
    can be included in a reference and their supported privileges.

    Args:
        reference: reference name

    Returns:
        None
    """
    pass

def request_aws_api_integration(id: str, allowed_prefixes: [str], gateway: AwsGateway,
                                aws_role_arn: str,
                                api_key: str = None, name: str = None,
                                comment: str = None) -> None:
    """Requests an API integration from the consumer for the Amazon API Gateway.

    Args:
        id: The name of the API integration defined in the manifest file
        allowed_prefixes: Explicitly limits external functions that use the integration to reference one or more HTTPS proxy service endpoints
        gateway: Type of gateway can have the following values:
                - permissions.AwsGateway.API_GATEWAY
                - permissions.AwsGateway.PRIVATE_API_GATEWAY
                - permissions.AwsGateway.GOV_API_GATEWAY
                - permissions.AwsGateway.GOV_PRIVATE_API_GATEWAY
        aws_role_arn: ARN (Amazon resource name) of a cloud platform role.
        api_key:  API key for the integration
        name: API integration name
        comment: Description of the integration

    Returns:
        None
    """
    pass

def request_azure_api_integration(id: str, allowed_prefixes: [str], tenant_id: str, application_id: str,
                                  api_key: str = None, name: str = None,
                                  comment: str = None) -> None:
    """Requests an API integration from the consumer for the Amazon API Gateway.

    Args:
        id: The name of the API integration defined in the manifest file
        allowed_prefixes: Explicitly limits external functions that use the integration to reference one or more HTTPS proxy service endpoints
        gateway: Type of gateway can have the following values:
                - permissions.AwsGateway.API_GATEWAY
                - permissions.AwsGateway.PRIVATE_API_GATEWAY
                - permissions.AwsGateway.GOV_API_GATEWAY
                - permissions.AwsGateway.GOV_PRIVATE_API_GATEWAY
        aws_role_arn: ARN (Amazon resource name) of a cloud platform role.
        api_key:  API key for the integration
        name: API integration name
        comment: Description of the integration

    Returns:
        None
    """
    pass

def request_google_api_integration(id: str, allowed_prefixes: [str], audience: str, name: str = None,
                                   comment: str = None, api_key: str = None) -> None:
    """Requests an API integration from the consumer for Azure API Management.

    Args:
        id: The name of the API integration defined in the manifest file
        allowed_prefixes: Explicitly limits external functions that use the integration to reference one or more HTTPS proxy service endpoints
        audience: This is used as the audience claim when generating the JWT (JSON Web Token) to authenticate to the Google API Gateway.
        name: API integration name
        comment: Description of the integration
        api_key: API key for the integration

    Returns:
        None
    """
    pass

def request_share(share_name: str, db_name: str, db_role: str, accounts: [str]) -> None:
    pass

def request_application_specification_review(spec_names: [str] = None) -> None:
    """Opens a dialog on the Streamlit for consumer to review then approve, decline (only on optional spec)
    or take no action on given application specifications.

    Args:
        spec_names: Optional list of specifications for review, if not specified, display all the specifications.

    Returns:
        None
    """
    pass

def get_held_account_privileges(privilege_names: [str]) -> [str]:
    """Returns an array containing the privileges that have been granted to the Snowflake
    Native App based on the array of privileges passed to the function.

    Args:
        privilege_names: list of account level privileges to validate

    Returns:
        Array of granted account privileges
    """
    return []

def get_missing_account_privileges(privilege_names: [str]) -> [str]:
    """Returns an array containing the privileges that have not been granted to the Snowflake
    Native App based on the specified array of privileges.

    Args:
        privilege_names: array of privileges to validate

    Returns:
        Array of missing account privileges
    """
    return privilege_names

def get_reference_associations(reference_name: str) -> [str]:
    """Iterates through all associations for a reference and returns information about the associations.

    Args:
        reference_name: the name of the reference

    Returns:
        Array of reference associations
    """
    return []

def get_detailed_reference_associations(reference_name: str) -> List[dict]:
    """Iterates through all associations for a reference and returns detailed information about the associations.

    Args:
        reference_name: the name of the reference

    Returns:
        Returns an array of dictionaries. Each dictionary contains the following key/value pairs:
        {
          "alias": "<value>",
          "database": "<value>",
          "schema": "<value>",
          "name": "<value>"
        }
        - alias: The system-generated alias for the reference.
        - database: The parent database name of the consumer object, if the object resides in a database. Otherwise, null.
        - schema: The parent schema of the consumer object, if the object resides in a schema. Otherwise, null.
        - name: The name of the consumer object.
    """
    return []

def get_application_specifications() -> List[dict]:
    """Get all the specifications in the current application

    Returns:
        An array of dictionaries.
        Each dictionary contains the following key/value pairs:
            {
                “name”: “<value>”,
                “created_on”: “<value>”,
                “type”: “<value>”,
                “sequence_number”: “<value>”,
                “status”: “<value>”,
                "status_upgraded_on": “<value>”,
                “label”: “<value>”,
                “description”: “<value>”,
                “definition“: “<value>”,
                “optional”: “<value>”,
            }
    """
    return []

def request_event_sharing() -> None:
    """Opens a dialog for configuring event sharing"""
    pass

def is_event_sharing_enabled() -> bool:
    """Check if event sharing is enabled

    Returns:
        True if event sharing is enabled on the current app and the app has an active event table, else False.
    """
    return False

def is_application_local_to_package() -> bool:
    """Check if the application is installed from same account."""
    return False

def is_application_authorized_for_telemetry_event_sharing() -> bool:
    """Check if the current application is authorized for telemetry event sharing, false otherwise."""
    return False

def is_application_all_mandatory_telemetry_event_definitions_enabled() -> bool:
    """Check if all mandatory telemetry events are enabled, false otherwise. """
    return False

def request_external_data() -> None:
    """Request consent from the consumer to use external and iceberg table."""
    pass

def is_external_data_enabled() -> bool:
    """Check if the current application is enabled to use external and iceberg table."""
    return False
