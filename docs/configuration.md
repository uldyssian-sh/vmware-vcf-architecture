# Configuration Reference

## Configuration Hierarchy

1. Command Line Arguments (Highest Priority)
2. Environment Variables
3. Configuration Files
4. Default Values (Lowest Priority)

## Main Configuration File

```yaml
app:
  name: vmware-vcf-architecture
  version: "1.0.0"
  debug: false

vcf:
  endpoint: "https://vcf.example.com"
  username: "${VCF_USERNAME}"
  password: "${VCF_PASSWORD}"
  verify_ssl: true

logging:
  level: INFO
  format: json
```

## Environment Variables

- `VCF_ENDPOINT` - VMware VCF endpoint URL
- `VCF_USERNAME` - Authentication username
- `VCF_PASSWORD` - Authentication password
- `DEBUG` - Enable debug mode
- `LOG_LEVEL` - Logging level# Updated Sun Nov  9 12:49:47 CET 2025
