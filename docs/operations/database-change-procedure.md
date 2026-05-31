# Database change procedure

This procedure defines the workflow for planning, validating, implementing, and verifying database changes for the Commerce Integration API platform.

Database changes require additional controls because schema modifications can affect application functionality, ETL processing, customer workflows, order management, analytics reporting, and operational stability.

Use this procedure whenever a change affects the PostgreSQL database schema, database objects, relationships, constraints, indexes, or application data structures.

For application deployment activities, see [Application deployment procedure](deployment-change-procedure.md).

<div class="doc-meta">
  <span>Database administration</span>
  <span>Schema management</span>
  <span>Change control</span>
  <span>Operational procedure</span>
</div>

## Purpose

This procedure is intended to:

- Standardize database change activities
- Reduce deployment-related risk
- Protect data integrity
- Maintain application compatibility
- Support rollback planning
- Improve operational traceability

## Scope

This procedure applies to:

- Table creation
- Table modification
- Column additions
- Column modifications
- Foreign key changes
- Index creation
- Constraint updates
- Data migrations
- Seed data updates
- Customer data model updates
- Order data model updates
- ETL-related schema changes
- Analytics-related schema changes

## Change management principles

Database changes should follow these principles:

- Validate locally before deployment
- Minimize production risk
- Preserve existing data
- Maintain referential integrity
- Test application compatibility
- Document schema changes
- Maintain rollback capability

## Change classification

### Low-risk changes

Examples include:

- New indexes
- New lookup tables
- New nullable columns
- Additional reporting structures

### Medium-risk changes

Examples include:

- New tables
- New foreign key relationships
- Additional constraints
- New ETL support structures

### High-risk changes

Examples include:

- Column removals
- Data type changes
- Primary key modifications
- Foreign key removals
- Data migration activities
- Customer or order schema modifications

High-risk changes require additional validation and rollback planning.

## Prerequisites

Before implementing a database change:

- Review the proposed schema modification
- Understand application dependencies
- Identify affected API endpoints
- Review ETL dependencies
- Review analytics dependencies
- Review operational workflows
- Confirm rollback strategy
- Confirm database availability

## Database architecture overview

The Commerce Integration API uses PostgreSQL as the processed data layer.

The database supports:

- Feed metadata
- Product catalog data
- Customer records
- Customer addresses
- Orders
- Order items
- Fulfillment workflows
- Analytics queries
- ETL processing metadata

Changes to shared entities may affect multiple application components.

## Change planning workflow

Before making a schema change:

1. Define the business requirement.
2. Identify affected tables.
3. Identify dependent application functionality.
4. Determine whether data migration is required.
5. Define validation criteria.
6. Define rollback requirements.
7. Update implementation documentation.

### Example planning questions

- Does the change affect API responses?
- Does the change affect ETL processing?
- Does the change affect analytics queries?
- Does the change affect existing customer data?
- Does the change require backfilling data?
- Does the change introduce new relationships?

## Local schema validation

Perform all schema modifications locally before updating deployed environments.

Recommended validation activities include:

- Schema creation testing
- Application startup validation
- API validation
- ETL validation
- Customer workflow validation
- Order workflow validation
- Analytics validation
- Automated test execution

### Example application validation

```powershell
pytest
```

Expected result:

```text
passed
```

### Example startup validation

```powershell
uvicorn main:app --reload
```

Verify that the application starts successfully and connects to PostgreSQL.

## Example schema changes

### Create a table

```sql
CREATE TABLE example_table (
    example_id TEXT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Add a column

```sql
ALTER TABLE customers
ADD COLUMN example_field TEXT;
```

### Add an index

```sql
CREATE INDEX idx_customers_example_field
ON customers(example_field);
```

### Add a foreign key

```sql
ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id);
```

## Schema review checklist

Before deployment, verify:

- Naming conventions are followed
- Constraints are appropriate
- Indexes are required
- Relationships are valid
- Queries remain performant
- Existing functionality remains compatible
- Documentation is updated

## Backup considerations

Before implementing schema changes in deployed environments:

- Verify recent database backups exist
- Confirm restore procedures are available
- Confirm rollback requirements are documented
- Review potential data loss scenarios

!!! warning "Backup requirement"

    High-risk schema changes should not be deployed without a verified backup and rollback plan.

## Deployment workflow

### Step 1: Review the change

Review:

- SQL statements
- Application dependencies
- Documentation updates
- Rollback strategy

### Step 2: Validate locally

Verify:

- Schema changes apply successfully
- Application startup succeeds
- Tests pass
- APIs function correctly

### Step 3: Update documentation

Update affected documentation, including:

- API reference documentation
- Architecture documentation
- Operations procedures
- Release notes

### Step 4: Apply the schema change

Connect to PostgreSQL and execute the approved change.

Example:

```sql
ALTER TABLE customers
ADD COLUMN example_field TEXT;
```

### Step 5: Validate the schema

Confirm:

- Tables exist
- Columns exist
- Constraints exist
- Indexes exist
- Relationships function correctly

Example:

```sql
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'customers';
```

#### Schema parity validation

Before deploying application changes, compare the deployed database schema with the validated local schema.

Verify:

- Required tables exist
- Required columns exist
- Required seed data exists
- Required identifier counters exist
- Required lookup data exists
- Schema versions are consistent between environments

Examples:

```sql
\d partners
\d feeds
\d products
\d orders

select * from id_counters;
```

### Step 6: Validate application functionality

Verify:

- Application startup succeeds
- API endpoints respond correctly
- Customer workflows function correctly
- Order workflows function correctly
- ETL processing functions correctly
- Analytics endpoints function correctly

### Step 7: Deploy application changes

If application code depends on the schema update:

1. Complete schema validation.
2. Follow the Application deployment procedure.
3. Deploy the updated application.
4. Execute smoke tests.

## Post-change verification

After deployment, verify:

- Application health checks pass
- Database connectivity succeeds
- APIs respond correctly
- ETL jobs execute successfully
- Customer workflows function correctly
- Order workflows function correctly
- Analytics endpoints return expected results

### Health endpoint validation

```powershell
curl http://<application-load-balancer-dns-name>/health
```

Expected result:

```json
{
  "status": "healthy"
}
```

## Referential integrity validation

Verify that relationships behave correctly.

Examples include:

- Customer-to-address relationships
- Customer-to-order relationships
- Order-to-order-item relationships
- Feed-to-product relationships

### Example validation query

```sql
SELECT *
FROM orders
WHERE customer_id IS NOT NULL;
```

Review results for expected relationships.

## Data migration considerations

Some schema changes require migration of existing data.

Examples include:

- New required columns
- Data type changes
- Data normalization efforts
- New foreign key relationships

When migration is required:

1. Define migration logic.
2. Validate migration locally.
3. Test application compatibility.
4. Validate migrated records.
5. Document migration activities.

## Rollback considerations

Rollback planning should occur before deployment.

Examples:

- Restore database backup
- Revert schema changes
- Redeploy previous application version
- Disable dependent functionality

### Example rollback workflow

1. Stop change activities.
2. Restore previous schema state.
3. Validate application functionality.
4. Validate database integrity.
5. Verify operational workflows.

## Common database change failures

| Failure type         | Example                            |
| -------------------- | ---------------------------------- |
| Constraint violation | Foreign key conflict               |
| Duplicate data       | Unique constraint failure          |
| Migration error      | Invalid transformation             |
| Schema mismatch      | Application expects missing column |
| Query failure        | Invalid SQL statement              |
| Performance issue    | Missing index                      |

## Troubleshooting

### Foreign key violation

#### Example

```text
update or delete on table violates foreign key constraint
```

#### Resolution

- Review dependent records
- Review relationship design
- Validate deletion logic
- Confirm referential integrity requirements

### Missing column

#### Example

```text
column does not exist
```

#### Resolution

- Verify schema deployment completed
- Verify application code matches schema
- Validate database environment

### Duplicate key error

#### Example

```text
duplicate key value violates unique constraint
```

#### Resolution

- Review existing records
- Review migration logic
- Validate identifier generation

### Application startup failure

#### Example

```text
UndefinedColumn
```

#### Resolution

- Verify deployed schema version
- Verify application version compatibility
- Review deployment sequence

## Operational monitoring

After a schema change, monitor:

- Application logs
- ECS task health
- Database performance
- API response behavior
- ETL execution
- Analytics queries

Review CloudWatch logs for unexpected errors following deployment.

## Responsibilities

### Platform administrators

Responsible for:

- Database administration
- Backup verification
- Schema deployment
- Rollback coordination

### Developers

Responsible for:

- Schema design
- Local validation
- Application compatibility testing
- Documentation updates

### Integration operators

Responsible for:

- Workflow validation
- ETL verification
- Operational issue escalation

## Database change checklist

Use this checklist before closing a database change activity.

- Change reviewed
- Impact assessed
- Rollback plan documented
- Backup verified
- Schema validated locally
- Production schema verified against local schema
- Required seed data verified
- Identifier counters verified
- Tests passed
- Documentation updated
- Release notes updated
- Schema deployed
- Application validated
- Health checks passed
- Smoke tests completed
- Logs reviewed

## Related documentation

- [Application deployment procedure](deployment-change-procedure.md)
- [Deployment guide](../architecture/deployment.md)
- [Backup and recovery procedure](backup-recovery-procedure.md)
- [Release notes](../releases/release-history.md)