import importlib
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent.resolve() / 'migrations'


def get_files():
    return [
        file for file in MIGRATIONS_DIR.glob('*.py')
        if file.name != '__init__.py'
    ]


def load_classes():
    files = get_files()
    classes = []

    for file in files:
        module_path = f'migrations.{file.stem}'
        module = importlib.import_module(module_path)

        for attr in dir(module):
            if not attr.startswith('Migration_'):
                continue

            element = getattr(module, attr)
            classes.append(element)

    return classes


if __name__ == '__main__':
    classes = load_classes()
    for class_ in classes:
        class_().run()
