import click
import peewee
import model
import sqlite3
import utils

@click.group(context_settings={'max_content_width': 400})
@click.pass_context
def cli(ctx):
    pass


@cli.command(help="Creates database.")
def db():
    model.init()


@cli.command(help="Executes a raw TEXT analysis of a title.")
@click.argument('known_db_path')
@click.argument('text_path')
def raw_analysis(text_path, known_db_path):
    known_db = utils.get_known_db(known_db_path)
    title = utils._generate_title_morphs(text_path, text_path.split("/")[-1])
    title.print_evaluation(known_db)


@cli.command(help="Looks into folders and files of a path, and creates a morhpdata file based on all. Single-core process")
@click.argument('text_path')
@click.argument('title_name')
@click.argument('output_folder')
def generate_title_morphs(text_path, title_name, output_folder):
    utils.create_morph_file(_generate_title_morphs(
        text_path, title_name), title_name, output_folder)


@cli.command(help="""
Looks into folders and files of a path, and creates a morhpdata for each. Each folder is handled as a title. Each file on root level of the collection path is handled as a title. Multi-core process\n
""")
@click.argument('collection_path')
@click.argument('output_folder')
def generate_collection_morphs(collection_path, output_folder):
    utils._generate_collection_morphs(collection_path, output_folder)


@cli.command(help="Evaluates the readabity of a single morphdata file.")
@click.argument('known_db_path')
@click.argument('morphdata_path')
def evaluate_title_morphs(known_db_path, morphdata_path):
    known_db = utils.get_known_db(known_db_path)

    if morphdata_path.endswith("morphdata"):
        title = pickle.load(open(morphdata_path, 'rb'))
        title.print_evaluation(known_db)


@cli.command(help="Evaluates the readability of all the morphdata files in a single folder.")
@click.argument('known_db_path')
@click.argument('collection_path')
def evaluate_collection_morphs(known_db_path, collection_path):
    print(into_csv(utils._evaluate_collection_morphs(collection_path, known_db_path)))


if __name__ == '__main__':
    cli()
