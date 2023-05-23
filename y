version = 0.1
[y.deploy.parameters]
stack_name = "invinsource"
resolve_s3 = true
s3_prefix = "invinsource"
region = "ap-south-1"
confirm_changeset = true
capabilities = "CAPABILITY_NAMED_IAM"
disable_rollback = true
parameter_overrides = "ApiGatewayStageName=\"Dev\""
image_repositories = []

[default.deploy.parameters]
stack_name = "invinsource"
resolve_s3 = true
s3_prefix = "invinsource"
region = "ap-south-1"
confirm_changeset = true
capabilities = "CAPABILITY_NAMED_IAM"
disable_rollback = true
parameter_overrides = "ApiGatewayStageName=\"Dev\""
image_repositories = []
