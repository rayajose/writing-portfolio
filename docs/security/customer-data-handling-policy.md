# Customer data handling policy

## Purpose

This policy defines requirements for handling customer-sensitive information within the Commerce Integration API platform.

The policy establishes controls for storing, processing, masking, and protecting customer-related information used in transactional workflows.

The current implementation is intended for fictional demonstration data only.

## Scope

This policy applies to:

- Customer records
- Shipping address records
- Customer-linked order workflows
- API responses
- Database storage workflows
- Operational support activities

Applicable platform components include:

- Customers API
- Orders API
- PostgreSQL
- ETL and analytics workflows
- Operational logging systems

## Customer-sensitive data types

The following data elements are considered customer-sensitive:

- Email addresses
- Phone numbers
- Street addresses
- Postal codes

These values are treated as restricted operational data.

## Data handling objectives

The platform implements customer data handling controls designed to:

- Reduce exposure of sensitive values
- Demonstrate field-level encryption
- Prevent accidental disclosure through API responses
- Support safer operational logging behavior
- Demonstrate compliance-oriented API design

## Encryption requirements

Customer-sensitive fields must be encrypted before storage.

The current implementation uses:

- Python cryptography library
- Fernet symmetric encryption
- Environment-managed encryption keys

Encrypted fields currently include:

- Email addresses
- Phone numbers
- Street addresses
- Postal codes

## API response requirements

Customer-sensitive values must not be returned directly through standard API responses.

Responses return masked values such as:

```text
al***@example.com
***-***-0101
123 ***
***01
```

Encrypted database values are not exposed directly through customer endpoints.

## Logging restrictions

Operational logs must not contain:

- Raw customer-sensitive values
- Encrypted database fields
- Encryption keys
- Authentication secrets

Operational workflows should instead reference:

- Customer identifiers
- Address identifiers
- Order identifiers
- Job identifiers

## Identifier strategy

Customer workflows use structured identifiers.

| Prefix    | Resource         |
| --------- | ---------------- |
| `CUxxxxx` | Customer         |
| `ADxxxxx` | Customer address |
| `ORxxxxx` | Order            |
| `OIxxxxx` | Order item       |

## Storage requirements

Customer-sensitive data must:

- Be stored only in approved systems
- Be protected through authenticated API access
- Be excluded from public documentation
- Be excluded from source control repositories

Approved storage systems include:

- PostgreSQL
- Approved cloud infrastructure services

## Access requirements

Customer workflows require authenticated API access using:

```text
x-api-key
```

Unauthorized requests must be rejected.

## Development requirements

Development and testing activities should:

- Use fictional customer records only
- Avoid storing real PII
- Avoid exposing sensitive values in debugging output
- Avoid hardcoding secrets in source code

Example fictional customer records may use:

- Fictional names
- Sample email domains
- Placeholder phone numbers
- Non-real shipping addresses

## Operational considerations

Operational support activities should:

- Avoid viewing decrypted values unnecessarily
- Restrict database access to authorized personnel
- Protect environment configuration files
- Follow secure logging practices

## Compliance-oriented behaviors

The current implementation demonstrates:

- Field-level encryption
- Masked API responses
- Separation of customer and transactional workflows
- Restricted operational logging
- Authenticated API access

## Limitations

This platform is intended for portfolio and demonstration purposes only.

Production implementations handling real regulated customer data would require additional controls including:

- Formal compliance review
- Secrets management integration
- Centralized audit logging
- Role-based access control
- Key rotation procedures
- TLS enforcement
- Production security monitoring

## Responsibilities

### Developers

Responsible for:

- Implementing secure handling behavior
- Avoiding sensitive data exposure
- Maintaining encryption workflows
- Preserving masking behavior

### Operators

Responsible for:

- Protecting operational systems
- Restricting infrastructure access
- Maintaining secure operational workflows

### Administrators

Responsible for:

- Protecting secrets and configuration data
- Managing infrastructure access
- Supporting operational security controls

## Related documentation

- [Data classification policy](data-classification-policy.md)
- [Encryption policy](encryption-policy.md)
- [API access control and authentication policy](api-access-control-policy.md)
- [Customers API](../api/customers.md)
- [Orders API](../api/orders.md)