import click

from doc_embeddings import save_all_doc_embeddings
from package_extract import convert_all_xml_files_to_pdf


@click.group()
def cli():
    pass


@click.group()
def main():
    pass


@main.command()
def extract_files():
    convert_all_xml_files_to_pdf()

@main.command()
#@click.option("--count", default=1, help="Number of greetings.")
#@click.option("--name", prompt="Your name", help="The person to greet.")
def save_docs_to_chroma():
    save_all_doc_embeddings()

cli.add_command(main)


if __name__ == '__main__':
    cli()