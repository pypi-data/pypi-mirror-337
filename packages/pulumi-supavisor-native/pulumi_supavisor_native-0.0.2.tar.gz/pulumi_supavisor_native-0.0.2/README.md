# Pulumi Native Provider for Supavisor

Supavisor is a cloud-native, multi-tenant Postgres connection pooler developed by Supabase. This Pulumi provider allows you to manage Supavisor tenants and their configurations using infrastructure as code.

> This provider was generated using an upgraded pulschema and pulumi-provider-framework.

## Package SDKs

- Node.js: https://www.npmjs.com/package/@phillarson-xyz/pulumi-supavisor-native
- Python: https://pypi.org/project/pulumi-supavisor-native/
- .NET: https://www.nuget.org/packages/Pulumi.SupavisorNative
- Go: `import github.com/phillarson-xyz/pulumi-supavisor-native/sdk/go/supavisor-native`

## Using The Provider

Change the URL in `provider/cmd/provider-gen-supavisor-native/openapi.yml` to your url. You'll also need to configure the provider with your Supavisor JWT secret. Set it as a secret using:

```bash
pulumi config set --secret supavisor:jwtSecret <your-jwt-secret>
```

The JWT secret can also be set via the `SUPAVISOR_NATIVE_JWT_SECRET` environment variable or passed in as any `pulumi.Input` such as a stack reference.

### Basic Usage

Here's a basic example of creating a Supavisor tenant. The provider will use the JWT secret to sign a new auth token JWT that lasts for five minutes.

```python
import pulumi_supavisor_native as supavisor

# Configure the provider
provider = supavisor.Provider(
    "supavisor",
    jwt_secret="supavisor-jwt-secret",
)

# Create a tenant
tenant = supavisor.tenants.Tenant(
    "supavisor-tenant",
    external_id="unique-tenant-id-for-url",
    tenant=supavisor.tenants.TenantPropertiesArgs(
        db_host="upstream-postgres-url",
        db_port="upstream-postgres-port",
        db_database="upstream-postgres-db",
        external_id="same-unique-tenant-id",
        ip_version="auto",
        enforce_ssl=False,
        upstream_ssl=False,
        require_user=True,
        auth_query="SELECT rolname, rolpassword FROM pg_authid WHERE rolname=$1;",
        users=[
            supavisor.tenants.UserArgs(
                db_password="upstream-postgres-password",
                db_user="upstream-postgres-user",
                pool_size=20,
                mode_type="transaction",
                is_manager=False,
            )
        ],
    )
)
```

### Resource Types

The provider currently supports the following resource types:

- `supavisor:tenants:Tenant`: Manages Supavisor tenants
- `supavisor:Provider`: Configures the Supavisor provider

### Tenant Configuration Options

When creating a tenant, you can configure the following options:

#### Required Fields

- `external_id`: Unique identifier for the tenant
- `db_host`: Upstream Postgres host
- `db_port`: Upstream Postgres port (integer)
- `db_database`: Database name
- `require_user`: Whether to require user authentication
- `users`: List of database users (at least one user required)

#### Optional Fields

- `allow_list`: List of CIDR addresses (defaults to `["0.0.0.0/0", "::/0"]`)
- `auth_query`: Custom authentication query (defaults to `SELECT rolname, rolpassword FROM pg_authid WHERE rolname=$1`)
- `ip_version`: IP version ("auto", "4", or "6")
- `enforce_ssl`: Enable SSL for client connections (default: false)
- `upstream_ssl`: Enable SSL for upstream connections (default: true)
- `upstream_verify`: SSL verification mode (e.g., "none")
- `sni_hostname`: SNI hostname for SSL connections (e.g., "your.domain.com")

### User Configuration Options

Each user in the `users` array supports the following options:

#### Required Fields

- `db_user`: Database username
- `db_password`: Database password
- `pool_size`: Number of connections in the pool (integer)

#### Optional Fields

- `db_user_alias`: Alternative username for the connection
- `is_manager`: Whether the user has manager privileges (default: false)
- `max_clients`: Maximum number of allowed clients (default: 25000)
- `mode_type`: Pool mode type ("transaction" or "session")
- `pool_checkout_timeout`: Timeout for checking out connections from the pool (in milliseconds)
- `tenant_external_id`: External ID reference for the tenant

### Read-only Fields

The following fields are read-only and will be populated after resource creation:

- `id`: Resource identifier
- `inserted_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Importing Existing Resources

To import an existing Supavisor tenant, use:

```bash
pulumi import supavisor:tenants:Tenant {resourceName} {external_id}
```

Alternatively, you can use the `import` option in your Pulumi program:

```python
tenant = supavisor.tenants.Tenant(
    "existing-tenant",
    external_id="unique-tenant-id",
    tenant=supavisor.tenants.TenantPropertiesArgs(...),
    opts=pulumi.ResourceOptions(import_="unique-tenant-id")
)
```

### Functions

The provider includes the following utility functions:

- `getTenant(external_id: string)`: Retrieve a tenant by its external ID

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

Apache-2.0 License

## About Supavisor

Supavisor is a cloud-native, multi-tenant Postgres connection pooler that provides:

- Connection pooling
- Multi-tenancy support
- Authentication and authorization
- SSL/TLS support
- High availability
- Monitoring and metrics

For more information about Supavisor, visit [the official repository](https://github.com/supabase/supavisor).