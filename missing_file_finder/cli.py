import click
from . import core

@click.command()
@click.argument('subset_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
@click.argument('superset_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
def main(subset_dir, superset_dir):
    """
    Finds files in SUBSET_DIR that are not present in SUPERSET_DIR by comparing file content.
    """
    missing_files = core.find_missing_files(subset_dir, superset_dir)
    
    if not missing_files:
        click.echo("All files in the subset folder are present in the superset folder.")
    else:
        click.echo("The following files were found in the subset folder but not in the superset folder:")
        for f in missing_files:
            click.echo(f)
        click.echo(f"Total missing files number: {len(missing_files)}")