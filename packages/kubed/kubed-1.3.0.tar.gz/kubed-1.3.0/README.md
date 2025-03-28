# Kubed - Developer CLI Productivity Tool

Kubed enhances your terminal experience with powerful autocompletion for popular DevOps tools:
- Docker
- Terraform
- Helm
- Kubernetes (kubectl)

## Features

- Comprehensive autocompletion for common cloud-native development tools
- Automatic installation of useful aliases (e.g., `k` for `kubectl`)
- Enhanced help output with links to documentation at daleyarborough.com
- Cross-platform support (macOS, Linux)

## Installation

```bash
# Install from PyPI
pip install kubed

# Run the setup script
kubed-setup
```

## Manual Setup

If the automatic setup doesn't work for your shell, you can manually set up the completions:

```bash
# Add to your .bashrc, .zshrc, or equivalent
source $(kubed-completions-path)
source $(kubed-aliases-path)
```

## Usage

After installation, you'll have access to:

1. Tab completions for docker, terraform, helm, and kubectl commands
2. Aliases like `k` for `kubectl`, `d` for `docker`, etc.
3. Enhanced help output with links to daleyarborough.com when using --help

## Requirements

- Python 3.6+
- Bash, Zsh, or compatible shell
- Docker, Terraform, Helm, or Kubernetes CLI tools (for respective completions)

## License

MIT

## Author

Daley Yarborough 