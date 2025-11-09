# Monitoring Guide

## Observability Stack

- **Prometheus** - Metrics collection
- **Grafana** - Visualization and dashboards
- **Health Checks** - Application monitoring
- **Alerting** - Notifications and alerts

## Available Metrics

### Application Metrics
- Response times
- Error rates
- Throughput
- Active connections

### System Metrics
- CPU usage
- Memory consumption
- Disk I/O
- Network traffic

### Business Metrics
- Automation success rates
- Compliance scores
- User activity

## Dashboards

Pre-built Grafana dashboards available for:
- Application performance
- System resources
- Security metrics
- Business KPIs

## Alerting

Configure alerts for:
- High error rates
- Performance degradation
- Security incidents
- System failures

## Setup

```bash
# Start monitoring stack
docker-compose --profile monitoring up -d

# Access Grafana
http://localhost:3000
```# Updated Sun Nov  9 12:49:47 CET 2025
# Updated Sun Nov  9 12:52:31 CET 2025
# Updated Sun Nov  9 12:56:20 CET 2025
