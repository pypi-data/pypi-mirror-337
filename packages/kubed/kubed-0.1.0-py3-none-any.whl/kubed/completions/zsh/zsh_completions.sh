# Kubed Zsh completions

# Check if commands exist before sourcing completions
if command -v kubectl >/dev/null 2>&1; then
    source <(kubectl completion zsh)
    # Enable completion for the k alias
    compdef k=kubectl
fi

if command -v docker >/dev/null 2>&1; then
    # Docker completions
    if [ -f /usr/share/zsh/vendor-completions/_docker ]; then
        source /usr/share/zsh/vendor-completions/_docker
    fi
fi

if command -v terraform >/dev/null 2>&1; then
    # Terraform completions - requires terraform plugin for zsh
    autoload -U +X bashcompinit && bashcompinit
    complete -o nospace -C $(which terraform) terraform
    complete -o nospace -C $(which terraform) tf
fi

if command -v helm >/dev/null 2>&1; then
    source <(helm completion zsh)
    # Enable completion for the h alias
    compdef h=helm
fi
