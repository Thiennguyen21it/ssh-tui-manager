# Contributing to SSH TUI Manager

Thank you for considering contributing to SSH TUI Manager! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment information (OS, Python version, etc.)

### Suggesting Features

If you have an idea for a new feature, please create an issue with the following information:

- A clear, descriptive title
- A detailed description of the feature
- Any relevant examples or mockups
- Why this feature would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add or update tests as needed
5. Make sure all tests pass
6. Submit a pull request

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ssh-tui-manager.git
   cd ssh-tui-manager
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov black isort
   ```

## Coding Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep code modular and maintainable

## Testing

- Write tests for new features or bug fixes
- Run tests before submitting a pull request:
  ```bash
  pytest
  ```

## Documentation

- Update documentation when changing code
- Keep the README.md up to date
- Document new features in the appropriate places

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
