import os

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a Django module using the project structure."

    def add_arguments(self, parser):
        parser.add_argument(
            "name",
            type=str,
            help="Module name, e.g. delivery",
        )

    def handle(self, *args, **options):
        name = options["name"].strip().lower()

        if not name.isidentifier():
            raise CommandError(
                f"Invalid module name: {name}"
            )

        base_dir = Path(settings.BASE_DIR)
        module_dir = base_dir / name

        if module_dir.exists():
            raise CommandError(
                f"Module '{name}' already exists."
            )

        self.create_directories(module_dir)
        self.create_files(module_dir, name)
        self.add_to_installed_apps(name)
        self.add_to_urls(name)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created module '{name}'."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Added '{name}' to LOCAL_APPS."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Registered '{name}' in config/urls.py."
            )
        )

        self.stdout.write("")
        self.stdout.write("Created structure:")

        for path in sorted(module_dir.rglob("*")):
            if path.is_file():
                self.stdout.write(
                    f"  {path.relative_to(base_dir)}"
                )

    def create_directories(self, module_dir):
        directories = [
            module_dir,
            module_dir / "migrations",
            module_dir / "models",
            module_dir / "serializers",
            module_dir / "services",
            module_dir / "views",
        ]

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    def create_files(self, module_dir, name):
        files = {
            module_dir / "__init__.py": "",

            module_dir / "migrations" / "__init__.py": "",
            module_dir / "models" / "__init__.py": "",
            module_dir / "serializers" / "__init__.py": "",
            module_dir / "services" / "__init__.py": "",
            module_dir / "views" / "__init__.py": "",

            module_dir / "admin.py": "",
            module_dir / "constants.py": "",
            module_dir / "tests.py": "",
            module_dir / "urls.py": "",

            module_dir / "models" / f"{name}.py": "",
            module_dir / "serializers" / f"{name}_serializer.py": "",
            module_dir / "services" / f"{name}_service.py": "",
            module_dir / "views" / f"{name}_view_set.py": "",

            module_dir / "apps.py": f"""from django.apps import AppConfig


class {self.class_name(name)}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{name}"
""",
        }

        for file_path, content in files.items():
            file_path.write_text(
                content,
                encoding="utf-8",
            )

    def add_to_installed_apps(self, name):
        settings_module = os.environ.get(
            "DJANGO_SETTINGS_MODULE"
        )

        if not settings_module:
            raise CommandError(
                "DJANGO_SETTINGS_MODULE is not configured."
            )

        try:
            settings_file = Path(
                __import__(
                    settings_module,
                    fromlist=[""],
                ).__file__
            )
        except (ImportError, AttributeError):
            raise CommandError(
                "Could not find Django settings file."
            )

        if not settings_file.exists():
            raise CommandError(
                "Could not find Django settings file."
            )

        content = settings_file.read_text(
            encoding="utf-8"
        )

        marker = "LOCAL_APPS = ["

        if marker not in content:
            raise CommandError(
                "Could not find LOCAL_APPS in settings."
            )

        app_entry = f'    "{name}",'

        if app_entry in content:
            return

        content = content.replace(
            marker,
            f"{marker}\n{app_entry}",
            1,
        )

        settings_file.write_text(
            content,
            encoding="utf-8",
        )

    def add_to_urls(self, name):
        base_dir = Path(settings.BASE_DIR)

        urls_file = base_dir / "config" / "urls.py"

        if not urls_file.exists():
            raise CommandError(
                f"URL file not found: {urls_file}"
            )

        content = urls_file.read_text(
            encoding="utf-8"
        )

        # Register the module under API v1.
        route = (
            f'    path("api/v1/{name}/", '
            f'include("{name}.urls")),'
        )

        # Don't register the same route twice.
        if route in content:
            return

        # Add include import.
        if "from django.urls import include, path" not in content:
            if "from django.urls import path" in content:
                content = content.replace(
                    "from django.urls import path",
                    "from django.urls import include, path",
                    1,
                )
            else:
                content = (
                    "from django.urls import include, path\n"
                    + content
                )

        marker = "urlpatterns = ["

        if marker not in content:
            raise CommandError(
                "Could not find urlpatterns in config/urls.py."
            )

        content = content.replace(
            marker,
            f"{marker}\n{route}",
            1,
        )

        urls_file.write_text(
            content,
            encoding="utf-8",
        )

    @staticmethod
    def class_name(name):
        return "".join(
            part.capitalize()
            for part in name.split("_")
        )