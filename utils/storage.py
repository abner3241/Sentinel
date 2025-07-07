class Storage:
    """Abstração de armazenamento de arquivos."""

    def save(self, path, content):
        with open(path, 'w') as f:
            f.write(content)

    def load(self, path):
        with open(path, 'r') as f:
            return f.read()
