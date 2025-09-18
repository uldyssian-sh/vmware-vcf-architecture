# Development Guide

## Development Setup

1. Fork and clone repository
2. Set up development environment
3. Install pre-commit hooks
4. Create feature branch

## Code Standards

- Follow PEP 8 style guide
- Use Black for formatting
- Add type hints
- Write comprehensive tests
- Document all functions

## Testing

```bash
# Run all tests
make test

# Run with coverage
pytest --cov=.

# Run specific tests
pytest tests/unit/
```

## Contributing

1. Create feature branch
2. Make changes
3. Add tests
4. Update documentation
5. Submit pull request

## Code Review Process

All changes require:
- Code review approval
- Passing tests
- Security scan approval
- Documentation updates