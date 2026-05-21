# Data classification policy

## Purpose

This policy defines how data is classified, protected, stored, transmitted, and handled within the Commerce Integration API platform.

The policy supports operational consistency, security-oriented design, and protection of customer-sensitive information.

## Scope

This policy applies to:

- API services
- ETL processing workflows
- Database systems
- Operational logging
- Cloud storage systems
- Analytics workflows
- Documentation and support operations

## Classification levels

| Classification | Description                                                           | Examples                            |
| -------------- | --------------------------------------------------------------------- | ----------------------------------- |
| Public         | Information approved for public disclosure                            | Public API documentation            |
| Internal       | Operational information intended for internal use                     | ETL logs, deployment metadata       |
| Confidential   | Sensitive operational or customer-related information                 | Order records, customer identifiers |
| Restricted     | Highly sensitive information requiring additional protection controls | Encrypted customer-sensitive fields |

## Restricted data types

The following data elements are classified as restricted:

- Email addresses
- Phone numbers
- Street addresses
- Postal codes
- API secrets
- Encryption keys
- Database credentials

## Confidential data types

The following data elements are classified as confidential:

- Order records
- Job execution metadata
- Feed processing history
- Internal analytics data
- Operational monitoring data

## Public data types

The following data may be publicly accessible:

- Public API documentation
- Example requests and responses
- Fictional sample product data
- Architecture diagrams
- Deployment screenshots intended for portfolio use

## Data protection requirements

### Public data

Public data may be disclosed externally without additional restrictions.

### Internal data

Internal data should:

- Be accessible only to authorized personnel
- Avoid public exposure when possible
- Be retained according to operational requirements

### Confidential data

Confidential data must:

- Be protected through authenticated access
- Avoid unnecessary disclosure
- Be retained only for required operational purposes
- Be restricted to authorized workflows

### Restricted data

Restricted data must:

- Be encrypted at rest when possible
- Be masked in API responses
- Be excluded from operational logs
- Be protected through authentication controls
- Never be committed to source control
- Be stored only in approved systems

## Storage requirements

Restricted and confidential data must be stored only in approved systems including:

- PostgreSQL
- Amazon S3
- Approved cloud infrastructure services

Sensitive data must not be stored in:

- Source control repositories
- Debugging output
- Public documentation
- Unprotected local files

## Logging requirements

Operational logs must not contain:

- Raw customer-sensitive values
- Encryption keys
- API secrets
- Database credentials
- Authentication tokens

Logs should instead contain:

- Structured identifiers
- Job IDs
- Feed IDs
- Order IDs
- Processing status information

## API handling requirements

Systems exposing confidential or restricted data must:

- Require authenticated API access
- Validate request inputs
- Return masked customer-sensitive values
- Avoid exposing encrypted database fields directly

## Encryption requirements

Restricted customer-sensitive fields should be encrypted before storage.

Current encrypted field examples include:

- Email addresses
- Phone numbers
- Street addresses
- Postal codes

## Retention considerations

Data retention periods should align with:

- Operational requirements
- Troubleshooting requirements
- Audit-oriented traceability needs
- Business reporting requirements

## Compliance considerations

This platform demonstrates compliance-oriented design patterns including:

- Field-level encryption
- Masked API responses
- Operational traceability
- Separation of raw and processed data
- Controlled API authentication

The current implementation is intended for fictional portfolio demonstration data only.

## Responsibilities

Developers and operators are responsible for:

- Correctly classifying data
- Avoiding exposure of restricted information
- Following approved storage and logging practices
- Protecting authentication secrets and encryption keys
- Maintaining operational security controls

## Related documentation

- [API access control and authentication policy](api-access-control-policy.md)
- [Data retention policy](data-retention-policy.md)
- [Incident response plan](incident-response.md)
- [Customers API](../api/customers.md)
- [Platform architecture and operational flow](../architecture/platform-architecture.md)