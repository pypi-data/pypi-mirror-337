import ast
import importlib.util
import os
import shutil
import subprocess
import sys
import tomllib
import traceback
from importlib.metadata import entry_points
from pathlib import Path

import click
from click.core import Command, Context

import plain.runtime
from plain import preflight
from plain.assets.compile import compile_assets, get_compiled_path
from plain.exceptions import ImproperlyConfigured
from plain.packages import packages_registry
from plain.utils.crypto import get_random_string

from .formatting import PlainContext
from .registry import cli_registry


@click.group()
def plain_cli():
    pass


def symbolicate(file_path: Path):
    if "internal" in str(file_path).split("/"):
        return ""

    source = file_path.read_text()

    parsed = ast.parse(source)

    def should_skip(node):
        if isinstance(node, ast.ClassDef | ast.FunctionDef):
            if any(
                isinstance(d, ast.Name) and d.id == "internalcode"
                for d in node.decorator_list
            ):
                return True
            if node.name.startswith("_"):  # and not node.name.endswith("__"):
                return True
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Name) and target.id.startswith("_")
                    # and not target.id.endswith("__")
                ):
                    return True
        return False

    def process_node(node, indent=0):
        lines = []
        prefix = "    " * indent

        if should_skip(node):
            return []

        if isinstance(node, ast.ClassDef):
            decorators = [
                f"{prefix}@{ast.unparse(d)}"
                for d in node.decorator_list
                if not (isinstance(d, ast.Name) and d.id == "internal")
            ]
            lines.extend(decorators)
            bases = [ast.unparse(base) for base in node.bases]
            lines.append(f"{prefix}class {node.name}({', '.join(bases)})")
            # if ast.get_docstring(node):
            #     lines.append(f'{prefix}    """{ast.get_docstring(node)}"""')
            for child in node.body:
                child_lines = process_node(child, indent + 1)
                if child_lines:
                    lines.extend(child_lines)
            # if not has_body:
            #     lines.append(f"{prefix}    pass")

        elif isinstance(node, ast.FunctionDef):
            decorators = [f"{prefix}@{ast.unparse(d)}" for d in node.decorator_list]
            lines.extend(decorators)
            args = ast.unparse(node.args)
            lines.append(f"{prefix}def {node.name}({args})")
            # if ast.get_docstring(node):
            #     lines.append(f'{prefix}    """{ast.get_docstring(node)}"""')
            # lines.append(f"{prefix}    pass")

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    lines.append(f"{prefix}{target.id} = {ast.unparse(node.value)}")

        return lines

    symbolicated_lines = []
    for node in parsed.body:
        symbolicated_lines.extend(process_node(node))

    return "\n".join(symbolicated_lines)


@plain_cli.command
@click.option("--llm", "llm", is_flag=True)
@click.option("--open")
@click.argument("module", default="")
def docs(module, llm, open):
    if not module and not llm:
        click.secho("You must specify a module or use --llm", fg="red")
        sys.exit(1)

    if llm:
        click.echo(
            "Below is all of the documentation and abbreviated source code for the Plain web framework. "
            "Your job is to read and understand it, and then act as the Plain Framework Assistant and "
            "help the developer accomplish whatever they want to do next."
            "\n\n---\n\n"
        )

        docs = set()
        sources = set()

        # Get everything for Plain core
        for path in Path(__file__).parent.parent.glob("**/*.md"):
            docs.add(path)
        for source in Path(__file__).parent.parent.glob("**/*.py"):
            sources.add(source)

        # Find every *.md file in the other plain packages and installed apps
        for package_config in packages_registry.get_package_configs():
            if package_config.name.startswith("app."):
                # Ignore app packages for now
                continue

            for path in Path(package_config.path).glob("**/*.md"):
                docs.add(path)

            for source in Path(package_config.path).glob("**/*.py"):
                sources.add(source)

        docs = sorted(docs)
        sources = sorted(sources)

        for doc in docs:
            try:
                display_path = doc.relative_to(Path.cwd())
            except ValueError:
                display_path = doc.absolute()
            click.secho(f"<Docs: {display_path}>", fg="yellow")
            click.echo(doc.read_text())
            click.secho(f"</Docs: {display_path}>", fg="yellow")
            click.echo()

        for source in sources:
            if symbolicated := symbolicate(source):
                try:
                    display_path = source.relative_to(Path.cwd())
                except ValueError:
                    display_path = source.absolute()
                click.secho(f"<Source: {display_path}>", fg="yellow")
                click.echo(symbolicated)
                click.secho(f"</Source: {display_path}>", fg="yellow")
                click.echo()

        click.secho(
            "That's everything! Copy this into your AI tool of choice.",
            err=True,
            fg="green",
        )

        return

    if module:
        # Automatically prefix if we need to
        if not module.startswith("plain"):
            module = f"plain.{module}"

        # Get the README.md file for the module
        spec = importlib.util.find_spec(module)
        if not spec:
            click.secho(f"Module {module} not found", fg="red")
            sys.exit(1)

        module_path = Path(spec.origin).parent
        readme_path = module_path / "README.md"
        if not readme_path.exists():
            click.secho(f"README.md not found for {module}", fg="red")
            sys.exit(1)

        if open:
            click.launch(str(readme_path))
        else:

            def _iterate_markdown(content):
                """
                Iterator that does basic markdown for a Click pager.

                Headings are yellow and bright, code blocks are indented.
                """

                in_code_block = False
                for line in content.splitlines():
                    if line.startswith("```"):
                        in_code_block = not in_code_block

                    if in_code_block:
                        yield click.style(line, dim=True)
                    elif line.startswith("# "):
                        yield click.style(line, fg="yellow", bold=True)
                    elif line.startswith("## "):
                        yield click.style(line, fg="yellow", bold=True)
                    elif line.startswith("### "):
                        yield click.style(line, fg="yellow", bold=True)
                    elif line.startswith("#### "):
                        yield click.style(line, fg="yellow", bold=True)
                    elif line.startswith("##### "):
                        yield click.style(line, fg="yellow", bold=True)
                    elif line.startswith("###### "):
                        yield click.style(line, fg="yellow", bold=True)
                    elif line.startswith("**") and line.endswith("**"):
                        yield click.style(line, bold=True)
                    elif line.startswith("> "):
                        yield click.style(line, italic=True)
                    else:
                        yield line

                    yield "\n"

            click.echo_via_pager(_iterate_markdown(readme_path.read_text()))


@plain_cli.command()
@click.option(
    "-i",
    "--interface",
    type=click.Choice(["ipython", "bpython", "python"]),
    help="Specify an interactive interpreter interface.",
)
def shell(interface):
    """
    Runs a Python interactive interpreter. Tries to use IPython or
    bpython, if one of them is available.
    """

    if interface:
        interface = [interface]
    else:

        def get_default_interface():
            try:
                import IPython  # noqa

                return ["python", "-m", "IPython"]
            except ImportError:
                pass

            return ["python"]

        interface = get_default_interface()

    result = subprocess.run(
        interface,
        env={
            "PYTHONSTARTUP": os.path.join(os.path.dirname(__file__), "startup.py"),
            **os.environ,
        },
    )
    if result.returncode:
        sys.exit(result.returncode)


@plain_cli.command()
@click.argument("script", nargs=1, type=click.Path(exists=True))
def run(script):
    """Run a Python script in the context of your app"""
    before_script = "import plain.runtime; plain.runtime.setup()"
    command = f"{before_script}; exec(open('{script}').read())"
    result = subprocess.run(["python", "-c", command])
    if result.returncode:
        sys.exit(result.returncode)


# @plain_cli.command()
# @click.option("--filter", "-f", "name_filter", help="Filter settings by name")
# @click.option("--overridden", is_flag=True, help="Only show overridden settings")
# def settings(name_filter, overridden):
#     """Print Plain settings"""
#     table = Table(box=box.MINIMAL)
#     table.add_column("Setting")
#     table.add_column("Default value")
#     table.add_column("App value")
#     table.add_column("Type")
#     table.add_column("Module")

#     for setting in dir(settings):
#         if setting.isupper():
#             if name_filter and name_filter.upper() not in setting:
#                 continue

#             is_overridden = settings.is_overridden(setting)

#             if overridden and not is_overridden:
#                 continue

#             default_setting = settings._default_settings.get(setting)
#             if default_setting:
#                 default_value = default_setting.value
#                 annotation = default_setting.annotation
#                 module = default_setting.module
#             else:
#                 default_value = ""
#                 annotation = ""
#                 module = ""

#             table.add_row(
#                 setting,
#                 Pretty(default_value) if default_value else "",
#                 Pretty(getattr(settings, setting))
#                 if is_overridden
#                 else Text("<Default>", style="italic dim"),
#                 Pretty(annotation) if annotation else "",
#                 str(module.__name__) if module else "",
#             )

#     console = Console()
#     console.print(table)


@plain_cli.command("preflight")
@click.argument("package_label", nargs=-1)
@click.option(
    "--deploy",
    is_flag=True,
    help="Check deployment settings.",
)
@click.option(
    "--fail-level",
    default="ERROR",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]),
    help="Message level that will cause the command to exit with a non-zero status. Default is ERROR.",
)
@click.option(
    "--database",
    "databases",
    multiple=True,
    help="Run database related checks against these aliases.",
)
def preflight_checks(package_label, deploy, fail_level, databases):
    """
    Use the system check framework to validate entire Plain project.
    Raise CommandError for any serious message (error or critical errors).
    If there are only light messages (like warnings), print them to stderr
    and don't raise an exception.
    """
    include_deployment_checks = deploy

    if package_label:
        package_configs = [
            packages_registry.get_package_config(label) for label in package_label
        ]
    else:
        package_configs = None

    all_issues = preflight.run_checks(
        package_configs=package_configs,
        include_deployment_checks=include_deployment_checks,
        databases=databases,
    )

    header, body, footer = "", "", ""
    visible_issue_count = 0  # excludes silenced warnings

    if all_issues:
        debugs = [
            e for e in all_issues if e.level < preflight.INFO and not e.is_silenced()
        ]
        infos = [
            e
            for e in all_issues
            if preflight.INFO <= e.level < preflight.WARNING and not e.is_silenced()
        ]
        warnings = [
            e
            for e in all_issues
            if preflight.WARNING <= e.level < preflight.ERROR and not e.is_silenced()
        ]
        errors = [
            e
            for e in all_issues
            if preflight.ERROR <= e.level < preflight.CRITICAL and not e.is_silenced()
        ]
        criticals = [
            e
            for e in all_issues
            if preflight.CRITICAL <= e.level and not e.is_silenced()
        ]
        sorted_issues = [
            (criticals, "CRITICALS"),
            (errors, "ERRORS"),
            (warnings, "WARNINGS"),
            (infos, "INFOS"),
            (debugs, "DEBUGS"),
        ]

        for issues, group_name in sorted_issues:
            if issues:
                visible_issue_count += len(issues)
                formatted = (
                    click.style(str(e), fg="red")
                    if e.is_serious()
                    else click.style(str(e), fg="yellow")
                    for e in issues
                )
                formatted = "\n".join(sorted(formatted))
                body += f"\n{group_name}:\n{formatted}\n"

    if visible_issue_count:
        header = "Preflight check identified some issues:\n"

    if any(
        e.is_serious(getattr(preflight, fail_level)) and not e.is_silenced()
        for e in all_issues
    ):
        footer += "\n"
        footer += "Preflight check identified {} ({} silenced).".format(
            "no issues"
            if visible_issue_count == 0
            else "1 issue"
            if visible_issue_count == 1
            else f"{visible_issue_count} issues",
            len(all_issues) - visible_issue_count,
        )
        msg = click.style(f"SystemCheckError: {header}", fg="red") + body + footer
        raise click.ClickException(msg)
    else:
        if visible_issue_count:
            footer += "\n"
            footer += "Preflight check identified {} ({} silenced).".format(
                "no issues"
                if visible_issue_count == 0
                else "1 issue"
                if visible_issue_count == 1
                else f"{visible_issue_count} issues",
                len(all_issues) - visible_issue_count,
            )
            msg = header + body + footer
            click.echo(msg, err=True)
        else:
            click.secho("✔ Preflight check identified no issues.", err=True, fg="green")


@plain_cli.command()
@click.option(
    "--keep-original/--no-keep-original",
    "keep_original",
    is_flag=True,
    default=False,
    help="Keep the original assets",
)
@click.option(
    "--fingerprint/--no-fingerprint",
    "fingerprint",
    is_flag=True,
    default=True,
    help="Fingerprint the assets",
)
@click.option(
    "--compress/--no-compress",
    "compress",
    is_flag=True,
    default=True,
    help="Compress the assets",
)
def build(keep_original, fingerprint, compress):
    """Pre-deployment build step (compile assets, css, js, etc.)"""

    if not keep_original and not fingerprint:
        click.secho(
            "You must either keep the original assets or fingerprint them.",
            fg="red",
            err=True,
        )
        sys.exit(1)

    # Run user-defined build commands first
    pyproject_path = plain.runtime.APP_PATH.parent / "pyproject.toml"
    if pyproject_path.exists():
        with pyproject_path.open("rb") as f:
            pyproject = tomllib.load(f)

        for name, data in (
            pyproject.get("tool", {})
            .get("plain", {})
            .get("build", {})
            .get("run", {})
            .items()
        ):
            click.secho(f"Running {name} from pyproject.toml", bold=True)
            result = subprocess.run(data["cmd"], shell=True)
            print()
            if result.returncode:
                click.secho(f"Error in {name} (exit {result.returncode})", fg="red")
                sys.exit(result.returncode)

    # Then run installed package build steps (like tailwind, typically should run last...)
    for entry_point in entry_points(group="plain.build"):
        click.secho(f"Running {entry_point.name}", bold=True)
        result = entry_point.load()()
        print()

    # Compile our assets
    target_dir = get_compiled_path()
    click.secho(f"Compiling assets to {target_dir}", bold=True)
    if target_dir.exists():
        click.secho("(clearing previously compiled assets)")
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    total_files = 0
    total_compiled = 0

    for url_path, resolved_url_path, compiled_paths in compile_assets(
        target_dir=target_dir,
        keep_original=keep_original,
        fingerprint=fingerprint,
        compress=compress,
    ):
        if url_path == resolved_url_path:
            click.secho(url_path, bold=True)
        else:
            click.secho(url_path, bold=True, nl=False)
            click.secho(" → ", fg="yellow", nl=False)
            click.echo(resolved_url_path)

        print("\n".join(f"  {Path(p).relative_to(Path.cwd())}" for p in compiled_paths))

        total_files += 1
        total_compiled += len(compiled_paths)

    click.secho(
        f"\nCompiled {total_files} assets into {total_compiled} files", fg="green"
    )

    # TODO could do a jinja pre-compile here too?
    # environment.compile_templates() but it needs a target, ignore_errors=False


@plain_cli.command()
@click.argument("package_name")
def create(package_name):
    """
    Create a new local package.

    The PACKAGE_NAME is typically a plural noun, like "users" or "posts",
    where you might create a "User" or "Post" model inside of the package.
    """
    package_dir = plain.runtime.APP_PATH / package_name
    package_dir.mkdir(exist_ok=True)

    empty_dirs = (
        f"templates/{package_name}",
        "migrations",
    )
    for d in empty_dirs:
        (package_dir / d).mkdir(parents=True, exist_ok=True)

    empty_files = (
        "__init__.py",
        "migrations/__init__.py",
        "models.py",
        "views.py",
    )
    for f in empty_files:
        (package_dir / f).touch(exist_ok=True)

    # Create a urls.py file with a default namespace
    if not (package_dir / "urls.py").exists():
        (package_dir / "urls.py").write_text(
            f"""from plain.urls import path, Router


class {package_name.capitalize()}Router(Router):
    namespace = f"{package_name}"
    urls = [
        # path("", views.IndexView, name="index"),
    ]
"""
        )

    click.secho(
        f'Created {package_dir.relative_to(Path.cwd())}. Make sure to add "{package_name}" to INSTALLED_PACKAGES!',
        fg="green",
    )


@plain_cli.command()
@click.argument("setting_name")
def setting(setting_name):
    """Print the value of a setting at runtime"""
    try:
        setting = getattr(plain.runtime.settings, setting_name)
        click.echo(setting)
    except AttributeError:
        click.secho(f'Setting "{setting_name}" not found', fg="red")


@plain_cli.group()
def utils():
    pass


@utils.command()
def generate_secret_key():
    """Generate a new secret key"""
    new_secret_key = get_random_string(50)
    click.echo(new_secret_key)


@plain_cli.command()
@click.option("--flat", is_flag=True, help="List all URLs in a flat list")
def urls(flat):
    """Print all URL patterns under settings.URLS_ROUTER"""
    from plain.runtime import settings
    from plain.urls import URLResolver, get_resolver

    if not settings.URLS_ROUTER:
        click.secho("URLS_ROUTER is not set", fg="red")
        sys.exit(1)

    resolver = get_resolver(settings.URLS_ROUTER)
    if flat:

        def flat_list(patterns, prefix="", curr_ns=""):
            for pattern in patterns:
                full_pattern = f"{prefix}{pattern.pattern}"
                if isinstance(pattern, URLResolver):
                    # Update current namespace
                    new_ns = (
                        f"{curr_ns}:{pattern.namespace}"
                        if curr_ns and pattern.namespace
                        else (pattern.namespace or curr_ns)
                    )
                    yield from flat_list(
                        pattern.url_patterns, prefix=full_pattern, curr_ns=new_ns
                    )
                else:
                    if pattern.name:
                        if curr_ns:
                            styled_namespace = click.style(f"{curr_ns}:", fg="yellow")
                            styled_name = click.style(pattern.name, fg="blue")
                            full_name = f"{styled_namespace}{styled_name}"
                        else:
                            full_name = click.style(pattern.name, fg="blue")
                        name_part = f" [{full_name}]"
                    else:
                        name_part = ""
                    yield f"{click.style(full_pattern)}{name_part}"

        for p in flat_list(resolver.url_patterns):
            click.echo(p)
    else:

        def print_tree(patterns, prefix="", curr_ns=""):
            count = len(patterns)
            for idx, pattern in enumerate(patterns):
                is_last = idx == (count - 1)
                connector = "└── " if is_last else "├── "
                styled_connector = click.style(connector)
                styled_pattern = click.style(pattern.pattern)
                if isinstance(pattern, URLResolver):
                    if pattern.namespace:
                        new_ns = (
                            f"{curr_ns}:{pattern.namespace}"
                            if curr_ns
                            else pattern.namespace
                        )
                        styled_namespace = click.style(f"[{new_ns}]", fg="yellow")
                        click.echo(
                            f"{prefix}{styled_connector}{styled_pattern} {styled_namespace}"
                        )
                    else:
                        new_ns = curr_ns
                        click.echo(f"{prefix}{styled_connector}{styled_pattern}")
                    extension = "    " if is_last else "│   "
                    print_tree(pattern.url_patterns, prefix + extension, new_ns)
                else:
                    if pattern.name:
                        if curr_ns:
                            styled_namespace = click.style(f"{curr_ns}:", fg="yellow")
                            styled_name = click.style(pattern.name, fg="blue")
                            full_name = f"[{styled_namespace}{styled_name}]"
                        else:
                            full_name = click.style(f"[{pattern.name}]", fg="blue")
                        click.echo(
                            f"{prefix}{styled_connector}{styled_pattern} {full_name}"
                        )
                    else:
                        click.echo(f"{prefix}{styled_connector}{styled_pattern}")

        print_tree(resolver.url_patterns)


class CLIRegistryGroup(click.Group):
    """
    Click Group that exposes commands from the CLI registry.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cli_registry.import_modules()

    def list_commands(self, ctx):
        return sorted(cli_registry.get_commands().keys())

    def get_command(self, ctx, name):
        commands = cli_registry.get_commands()
        return commands.get(name)


class PlainCommandCollection(click.CommandCollection):
    context_class = PlainContext

    def __init__(self, *args, **kwargs):
        sources = []

        try:
            plain.runtime.setup()

            sources = [
                CLIRegistryGroup(),
                plain_cli,
            ]
        except plain.runtime.AppPathNotFound:
            # Allow some commands to work regardless of being in a valid app
            click.secho(
                "Plain `app` directory not found. Some commands may be missing.",
                fg="yellow",
                err=True,
            )

            sources = [
                plain_cli,
            ]
        except ImproperlyConfigured as e:
            # Show what was configured incorrectly and exit
            click.secho(
                str(e),
                fg="red",
                err=True,
            )

            exit(1)
        except Exception as e:
            # Show the exception and exit
            print("---")
            print(traceback.format_exc())
            print("---")

            click.secho(
                f"Error: {e}",
                fg="red",
                err=True,
            )

            exit(1)

        super().__init__(*args, **kwargs)

        self.sources = sources

    def get_command(self, ctx: Context, cmd_name: str) -> Command | None:
        cmd = super().get_command(ctx, cmd_name)
        if cmd:
            # Pass the formatting down to subcommands automatically
            cmd.context_class = self.context_class
        return cmd


cli = PlainCommandCollection()
