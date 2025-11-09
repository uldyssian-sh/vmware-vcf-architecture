# API Reference

## REST API Endpoints

### Health Check
```
GET /health
```
Returns application health status.

### System Status
```
GET /api/v1/status
Authorization: Bearer <token>
```
Returns detailed system status.

### Automation Tasks
```
POST /api/v1/automation
Content-Type: application/json
Authorization: Bearer <token>

{
  "task": "infrastructure_scan",
  "parameters": {
    "scope": "datacenter",
    "deep_scan": true
  }
}
```

### Metrics
```
GET /metrics
```
Returns Prometheus metrics.

## Python API

```python
from vmware_vcf_architecture import VCFArchitecture

# Initialize
vcf = VCFArchitecture()

# Health check
health = await vcf.health_check()

# Run automation
result = await vcf.run()
```# Updated 20251109_123823
# Updated Sun Nov  9 12:49:47 CET 2025
