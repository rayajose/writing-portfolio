# Encryption policy

## Purpose

This policy defines encryption requirements and implementation guidance for protecting customer-sensitive data within the Commerce Integration API platform.

The policy supports secure handling of PII-like data, operational security controls, and compliance-oriented application design.


## Scope

This policy applies to:

- Customer records
- Shipping address records
- API authentication secrets
- Database credentials
- Application configuration secrets
- Operational workflows handling restricted data


## Encryption objectives

The platform uses encryption to:

- Reduce exposure of sensitive values
- Protect customer-related data at rest
- Support secure API response handling
- Demonstrate secure application design patterns
- Support operational security best practices


## Field-level encryption

Field-level encryption is implemented for customer-sensitive fields stored in PostgreSQL.

Encrypted fields currently include:

- Email addresses
- Phone numbers
- Street addresses
- Postal codes


## Encryption implementation

The current implementation uses:

| Component            | Implementation              |
| -------------------- | --------------------------- |
| Language             | Python                      |
| Encryption library   | `cryptography`              |
| Encryption mechanism | Fernet symmetric encryption |
| Key source           | Environment variable        |
| Response protection  | Masked API responses        |


## Key management

Encryption keys must:

- Be stored outside application source code
- Be injected through environment variables or approved secrets management systems
- Never be committed to source control
- Never appear in operational logs
- Be restricted to authorized environments only

Example environment variable:

```text
PII_ENCRYPTION_KEY
```


## API response behavior

Encrypted database values are not returned directly through customer API responses.

Responses return masked values such as:

```text
al***@example.com
***-***-0101
123 ***
***01
```

This reduces accidental disclosure of customer-sensitive information.


## Logging restrictions

Operational logs must not contain:

- Raw customer-sensitive values
- Encrypted database fields
- Encryption keys
- Database credentials
- Authentication secrets


## Operational guidance

Systems handling encrypted fields should:

- Avoid debugging output containing sensitive values
- Restrict database access
- Limit administrative access to authorized users
- Protect environment configuration files
- Rotate secrets periodically in production environments


## Development guidance

Development and test environments should:

- Use fictional customer data only
- Avoid storing real PII
- Avoid hardcoded encryption keys
- Separate development and production secrets


## Production considerations

Production implementations would typically additionally include:

- Centralized secrets management
- Automated key rotation
- Dedicated key management services
- TLS enforcement
- Audit logging
- Role-based access control
- Infrastructure-level encryption controls


## Compliance-oriented behaviors

The current implementation demonstrates the following compliance-oriented design patterns:

- Field-level encryption
- Masked API responses
- Separation of sensitive and transactional workflows
- Controlled API authentication
- Restricted operational logging


## Security limitations

The current implementation is intended for demonstration and portfolio purposes only.

The platform is not intended to process real regulated customer data without additional production-grade controls, legal review, and compliance validation.


## Related documentation

- [Data classification policy](data-classification-policy.md)
- [API access control and authentication policy](api-access-control-policy.md)
- [Customers](../api/customers.md)
- [Platform architecture and operational flow](../architecture/platform-architecture.md)