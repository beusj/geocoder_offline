# Contributing to geocoder_offline

Thank you for your interest in contributing to geocoder_offline!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/beusj/geocoder_offline.git
cd geocoder_offline
```

2. Install in development mode:
```bash
pip install -e .
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests

Run the test suite:
```bash
python -m unittest discover tests
```

Run specific test file:
```bash
python -m unittest tests.test_normalize
```

Run with verbose output:
```bash
python -m unittest discover tests -v
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

## Testing Guidelines

- Write tests for new functionality
- Ensure all tests pass before submitting a PR
- Aim for high test coverage
- Test edge cases and error conditions

## Project Structure

```
geocoder_offline/
├── postgis_like/          # PostGIS-like functionality
│   └── normalize/         # Address normalization module
│       ├── normalize_address.py  # Main parsing logic
│       ├── pprint_addy.py       # Address formatting
│       ├── data_structures.py   # Data classes
│       ├── lookup_tables.py     # Reference data
│       ├── utils.py             # Utility functions
│       ├── state_extract.py     # State extraction
│       └── location_extract.py  # Location extraction
├── tests/                 # Unit tests
├── examples/              # Example scripts
└── README.md             # Main documentation
```

## Making Changes

1. Create a new branch for your changes
2. Make your changes with clear commit messages
3. Add tests for new functionality
4. Update documentation as needed
5. Ensure all tests pass
6. Submit a pull request

## Adding New Features

When adding new address normalization features:

1. Check the PostGIS implementation for reference
2. Add appropriate lookup data to `lookup_tables.py`
3. Implement the feature in the appropriate module
4. Add comprehensive tests
5. Update examples and documentation

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Example addresses that fail to parse correctly
- Expected vs actual results
- Python version and operating system

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the tests to cover your changes
3. Ensure all tests pass
4. Your PR will be reviewed by maintainers

## Questions?

Feel free to open an issue for questions or clarifications!
