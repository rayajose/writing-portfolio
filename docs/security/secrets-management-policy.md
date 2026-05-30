# Secrets management

## Purpose

This policy defines requirements for securely handling secrets, credentials, encryption keys, and sensitive configuration values within the Commerce Integration API platform.

The policy establishes operational practices supporting secure application configuration, restricted credential exposure, and protection of customer-sensitive workflows.


## Scope

This policy applies to:

- API keys
- Encryption keys
- Database credentials
- AWS credentials
- Application configuration secrets
- Deployment configuration workflows
- Development and operational environments

Applicable platform components include:

- FastAPI application services
- PostgreSQL
- Amazon S3
- Amazon ECS
- Deployment workflows
- Local development environments


## Security objectives

The platform implements secrets management practices designed to:

- Reduce credential exposure
- Prevent accidental disclosure
- Support secure deployment workflows
- Separate configuration from application code
- Protect customer-sensitive workflows
- Demonstrate compliance-oriented operational practices


## Managed secret types

The following values are considered operational secrets:

| Secret type               | Example                          |
| ------------------------- | -------------------------------- |
| API credentials           | `x-api-key`                      |
| Encryption keys           | `PII_ENCRYPTION_KEY`             |
| Database credentials      | PostgreSQL username and password |
| AWS credentials           | AWS access configuration         |
| Environment configuration | Deployment environment values    |


## Secret storage requirements

Secrets must:

- Be stored outside source code
- Be externalized through environment variables or approved secrets management systems
- Be restricted to authorized operational environments
- Be protected from public disclosure
- Never appear in public documentation examples


## Environment configuration

The current implementation uses environment-based configuration.

Example configuration values include:

```text
API_KEY
PII_ENCRYPTION_KEY
DB_HOST
DB_NAME
DB_USER
DB_PASSWORD
AWS_REGION
S3_RAW_BUCKET
```


## Source control restrictions

Secrets must never be:

- Committed to Git repositories
- Stored in public documentation
- Embedded directly in application source code
- Included in screenshots or debugging output

Files containing secrets should be excluded through `.gitignore` configuration where appropriate.


## Encryption key handling

Encryption keys must:

- Be protected as restricted operational data
- Remain external to application source code
- Be accessible only to authorized application workflows
- Never be exposed through API responses
- Never appear in operational logs

The current implementation uses:

```text
PII_ENCRYPTION_KEY
```

to support field-level encryption for customer-sensitive fields.


## Development environment guidance

Development environments should:

- Use fictional test credentials
- Use fictional customer data only
- Separate development and production configuration
- Avoid sharing operational credentials
- Protect local `.env` files


## Production environment considerations

Production-oriented environments should additionally implement:

- Centralized secrets management
- Secret rotation procedures
- Access auditing
- Infrastructure-level secret isolation
- Restricted administrative access
- Automated credential lifecycle management

Example production solutions may include:

- AWS Secrets Manager
- AWS Systems Manager Parameter Store
- Dedicated key management systems


## Logging restrictions

Operational logs must not contain:

- API keys
- Encryption keys
- Database passwords
- AWS credentials
- Authentication secrets

Operational troubleshooting should instead use:

- Structured identifiers
- Job metadata
- Processing status information
- Operational timestamps


## Access restrictions

Access to operational secrets should follow least privilege principles.

Examples include:

- Restricting database credentials to application services
- Restricting deployment credentials to authorized administrators
- Limiting infrastructure modification access
- Separating development and production credentials


## Incident handling considerations

Potential secret exposure events should be treated as operational security incidents.

Response activities may include:

- Rotating affected credentials
- Reviewing deployment activity
- Investigating operational logs
- Reviewing access history
- Validating infrastructure configuration


## Compliance-oriented behaviors

The platform demonstrates the following compliance-oriented practices:

- Environment-based configuration
- Externalized credentials
- Encryption key isolation
- Field-level encryption
- Restricted operational logging
- Separation of code and secrets


## Limitations

The current implementation is intended for portfolio and demonstration purposes only.

Production environments handling real regulated customer data would require additional controls including:

- Centralized secrets management
- Automated key rotation
- Infrastructure-level access auditing
- Production-grade IAM controls
- Dedicated compliance review


## Responsibilities

### Developers

Responsible for:

- Avoiding hardcoded credentials
- Protecting local environment configuration
- Preventing secret exposure in source code
- Following secure development practices


### Operators

Responsible for:

- Managing deployment configuration
- Protecting operational secrets
- Restricting infrastructure access
- Supporting secure deployment workflows


### Administrators

Responsible for:

- Managing production credentials
- Rotating secrets when required
- Maintaining secure infrastructure configuration
- Supporting operational access controls


## Related documentation

- [API access control policy](api-access-control-policy.md)
- [Encryption policy](encryption-policy.md)
- [Customer data handling policy](customer-data-handling-policy.md)
- [Data classification policy](data-classification-policy.md)
- [Platform architecture and operational flow](../architecture/platform-architecture.md)