# Reten Service Core Library

Core library providing common components and utilities for Reten microservices.

## Features

- **Authentication**: API Key and JWT authentication
- **Logging**: Structured logging configuration
- **Monitoring**: Metrics and distributed tracing
- **Storage**: Database clients (BigQuery, Redis)
- **Testing**: Common fixtures and mocks
- **Utilities**: Common helper functions

## Installation

```bash
pip install reten-service-core
```

For development:
```bash
pip install reten-service-core[dev]
```

## Quick Start

```python
from fastapi import FastAPI
from reten_service_core import APIKeyAuth
from reten_service_core.logging import configure_logging
from reten_service_core.monitoring import metrics

# Configure logging
configure_logging()

# Create FastAPI app with auth
app = FastAPI()
app.include_middleware(APIKeyAuth)

# Add metrics
@app.get("/")
@metrics.track_latency()
async def root():
    return {"message": "Hello World"}
```

## Development

1. Clone the repository:
   ```bash
   git clone git@github.com:reten/service-core.git
   cd service-core
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Contributing

We welcome contributions to the Reten Service Core library! Whether it's:

- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🧪 Additional tests
- 🔧 Infrastructure updates

### Quick Start

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run quality checks:
   ```bash
   # Run tests
   pytest

   # Run linting
   ruff check .
   ruff format .
   ```
5. Commit your changes (using [Conventional Commits](https://www.conventionalcommits.org/))
6. Push to your fork
7. Open a Pull Request

### Development Environment

See the [Development](#development) section above for basic setup instructions.

### Detailed Guidelines

For detailed information about:
- Code style and standards
- Testing requirements
- Pull request process
- Development environment setup
- Commit message conventions

Please read our [Contributing Guide](CONTRIBUTING.md).

### Need Help?

- 📖 Check the [examples](examples/) directory for usage examples
- 🤔 Open an issue for questions or problems
- 💬 Contact the maintainers at dev@reten.ai

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### What does this mean?

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ No liability
- ⚠️ No warranty

The MIT License is a permissive license that allows you to do anything you want with the code as long as you include the original copyright and license notice in any copy of the software/source.
