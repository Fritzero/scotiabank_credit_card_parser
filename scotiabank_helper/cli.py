#!/usr/bin/env python
import csv
import os

import click

from scotiabank_helper.scotiabank_credit_card_statement_reader import ScotiaBankCreditCardStatementReader

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}

@cli.command("pdf-to-csv")
@click.option("--bank-statement-directory",
              help="Directory which all pdf bank statements are located.",
              required=True)
@click.option("--output-directory",
              help="Directory where the csv files will be located.",
              required=True)
@click.pass_context
def pdf_to_csv(ctx, bank_statement_directory, output_directory):

    reader = ScotiaBankCreditCardStatementReader(bank_statement_directory)
    statements = reader.get_estatements()

    statement_map = reader.read_statements(statements)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for statement, purchases in statement_map.iteritems():
        out_path = os.path.join(output_directory, statement + ".csv")

        print "Creating {}".format(out_path)

        with open(out_path, mode='w') as out_file:
            writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for purchase in purchases:
                writer.writerow([purchase.ref_num,
                                 purchase.transaction_date,
                                 purchase.post_date,
                                 purchase.details,
                                 purchase.amount])
