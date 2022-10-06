from aws_cdk import (
    Stack,
    aws_servicecatalog as servicecatalog,
    aws_iam as _iam,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct

class CdkServiceCatalogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create portfolio and product

        portfolio = servicecatalog.Portfolio(self, "Portfolio_Kafka",
            display_name="Test_Portfolio",
            provider_name="Provider"
        )

        product = servicecatalog.CloudFormationProduct(self, "ProductKafka",
            product_name="Kafka Product",
            owner="Product Owner",
            product_versions=[servicecatalog.CloudFormationProductVersion(
                product_version_name="v1",
                cloud_formation_template=servicecatalog.CloudFormationTemplate.from_asset('cdk_service_catalog/service_catalog_kafka.yaml')
            )
            ]
        )

        portfolio.add_product(product)

        # Launch role permissions

        launch_role = _iam.Role(self, "LaunchRole",
            assumed_by=_iam.ServicePrincipal("servicecatalog.amazonaws.com")
        )

        launch_role.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name(
                                    "PowerUserAccess"))

        portfolio.set_launch_role(product, launch_role)

        # Create End User IAM group and a test user
        
        end_users = _iam.Group(self, "EndUsers")

        end_users.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'AWSServiceCatalogEndUserFullAccess'))

        end_users.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'ReadOnlyAccess'))
        
        test_password = secretsmanager.Secret(self, "TestPassword")
        test_user = _iam.User(self, "TestUser",
                user_name="TestUser",
                password=test_password.secret_value
        )

        end_users.add_user(test_user)

        portfolio.give_access_to_user(test_user)
