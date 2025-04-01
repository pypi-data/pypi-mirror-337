import click
from pathlib import Path
from prisma_to_sqlmodel import PrismaConverter

@click.command()
@click.argument('prisma_file', type=click.Path(exists=True, path_type=Path))
@click.argument('output_file', type=click.Path(path_type=Path))
@click.option('--format/--no-format', default=True, help='Format the output with black')
def main(prisma_file: Path, output_file: Path, format: bool):
    """Convert a Prisma schema file to SQLModel models.
    
    PRISMA_FILE: Path to the input Prisma schema file
    OUTPUT_FILE: Path where the generated SQLModel code will be written
    """
    try:
        # Create the converter and run it
        converter = PrismaConverter(prisma_file)
        python_code = converter.convert()
        
        # Write the output
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(python_code)
        
        if format:
            try:
                import subprocess
                subprocess.run(['black', str(output_file)], check=True)
                click.echo(f"Generated and formatted SQLModel schema at {output_file}")
            except subprocess.CalledProcessError:
                click.echo(f"Generated SQLModel schema at {output_file}")
                click.echo("Warning: Failed to format with black")
            except FileNotFoundError:
                click.echo(f"Generated SQLModel schema at {output_file}")
                click.echo("Warning: black not found. Please install it with: pip install black")
        else:
            click.echo(f"Generated SQLModel schema at {output_file}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main() 