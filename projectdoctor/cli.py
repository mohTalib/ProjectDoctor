# projectdoctor/cli.py
import click
import json as json_lib
from .analyzer import Analyzer
from .reporter import Reporter

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """
    ProjectDoctor 🩺
    A Python library to assess codebase health, detect structural risks,
    and guide maintainability improvements.
    """
    pass

@cli.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False, resolve_path=True), default='.')
@click.option(
    '--output',
    type=click.Choice(['markdown', 'cli', 'json']),
    default='cli',
    help="The format for the final report. Can be 'cli', 'markdown', or 'json'."
)
@click.option(
    '--thresholds',
    help="""
    JSON string to override default detector thresholds.
    Example: '{"file_size": {"max_lines": 1000}, "long_function": {"max_lines": 75}}'
    """
)
def analyze(project_path, output, thresholds):
    """
    Analyzes a Python project and generates a health report.

    PROJECT_PATH: The path to the project you want to analyze. Defaults to the current directory.
    """
    click.echo(f"🩺 Analyzing project at: {project_path}")
    
    custom_thresholds = {}
    if thresholds:
        try:
            custom_thresholds = json_lib.loads(thresholds)
        except json_lib.JSONDecodeError:
            click.echo("Error: Invalid JSON format for --thresholds.", err=True)
            return

    analyzer = Analyzer(project_path, custom_thresholds)
    analysis_results = analyzer.run()
    
    file_count = len(analysis_results.get("python_files", []))
    issue_count = len(analysis_results.get("issues", []))
    
    click.echo(f"✔ {file_count} files analyzed")
    if issue_count > 0:
        click.echo(f"🟡 {issue_count} issues found")
    else:
        click.echo("✅ No issues found!")

    reporter = Reporter(analysis_results)

    if output == 'markdown':
        report_filename = 'project_health_report.md'
        reporter.to_markdown(report_filename)
        click.echo(f"📄 Report saved to: {report_filename}")
    elif output == 'json':
        click.echo(reporter.to_json())
    else:
        reporter.to_cli()

if __name__ == '__main__':
    cli()