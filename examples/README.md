# Basic Examples

## Python API Example

```python
from vmware_vcf_architecture import VCFArchitecture
import asyncio

async def main():
    # Initialize
    vcf = VCFArchitecture()
    
    # Health check
    health = await vcf.health_check()
    print(f"Status: {health['status']}")
    
    # Run automation
    result = await vcf.run()
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Docker Example

```bash
# Run with Docker
docker run -d \
  --name vmware-vcf \
  -p 8080:8080 \
  -e VCF_ENDPOINT=https://vcf.example.com \
  ghcr.io/uldyssian-sh/vmware-vcf-architecture:latest
```

## Configuration Example

```yaml
# config.yml
app:
  name: vmware-vcf-architecture
  debug: false

vcf:
  endpoint: https://vcf.example.com
  verify_ssl: true

logging:
  level: INFO
```

## REST API Example

```bash
# Health check
curl http://localhost:8080/health

# Get status
curl -H "Authorization: Bearer token" \
     http://localhost:8080/api/v1/status
```