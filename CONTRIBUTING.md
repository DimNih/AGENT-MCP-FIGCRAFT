# Contributing to FigCraft MCP

Thank you for your interest in improving FigCraft MCP! We welcome contributions from developers, designers, and AI enthusiasts worldwide.

## How Can You Contribute?

- **Report Bugs:** Open an issue with environment details (OS, Python version, FigCraft version) and steps to reproduce.
- **Suggest Features:** Share workflows or design operations you'd like to automate.
- **Submit Pull Requests:** Enhance node helpers, improve platform discovery, or fix issues.

## Development Workflow

1. Fork and clone the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Verify your changes locally:
   ```bash
   python test-connection.py
   python -m figcraft_mcp check
   ```
4. Commit with descriptive messages.
5. Push to your branch and open a Pull Request.

## Coding Guidelines

- Keep the core client free from required heavy external dependencies (standard library first).
- Ensure all path operations remain cross-platform (Windows, macOS, Linux).
- Add docstrings to newly introduced helper methods.

