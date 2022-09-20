import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_service_catalog.cdk_service_catalog_stack import CdkServiceCatalogStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_service_catalog/cdk_service_catalog_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkServiceCatalogStack(app, "cdk-service-catalog")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
