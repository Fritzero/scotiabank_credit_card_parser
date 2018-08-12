#!/usr/bin/env python

import os

import PyPDF2


class Purchase(object):

    def __init__(self, ref_num, transaction_date, post_date, details, amount):
        self.ref_num = ref_num
        self.transaction_date = transaction_date
        self.post_date = post_date
        self.details = details
        self.amount = amount

    def __str__(self):
        msg = "{ref_num}\t{trans_date}\t{post_date}\t{amount}\t{details}"

        return msg.format(ref_num=self.ref_num,
                          trans_date=self.transaction_date,
                          post_date=self.post_date,
                          details=self.details,
                          amount=self.amount)


class ScotiaBankCreditCardStatementReader(object):

    def __init__(self, statements_directory):
        self.statement_directory = statements_directory

    def read_statements(self, statements):
        """
        Read a bunch of credit card statements and return a map listing the statements
        and all purchases in the statement.
        """
        statement_map = {}

        for statement in statements:
            purchases = []
            ref_num_counter = 1

            pdf_reader = self.get_statement_pdf_reader(statement)
            pages = self.get_pages_from_statement(pdf_reader)

            for page in pages:
                lines = page.extractText().split('\n')[10:]

                for line_number in range(0, len(lines)):
                    ref_num = self.construct_ref_number(ref_num_counter)
                    if ref_num in lines[line_number]:
                        purchase, line_number = self.construct_purchase(lines, line_number)
                        purchases.append(purchase)

                        ref_num_counter = ref_num_counter + 1

            statement_map[statement.replace("e-Statement.pdf", "").replace(" ", "")] = purchases

        return statement_map

    def get_statement_pdf_reader(self, statement):
        """
        Returns a pdf_reader object for the bank statement.
        """
        path = os.path.join(self.statement_directory, statement)
        pdf_file = open(path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        return pdf_reader

    def construct_purchase(self, lines, line_number):
        """
        Once a reference number is found, return the purchase object and where the
        new line number is located.
        """
        # Details starts after reference number, post date and transaction date
        iterator = line_number + 3
        details = ""

        while not self.is_money(lines[iterator]):
            details = details + " " + lines[iterator].replace('\n', '')
            iterator = iterator + 1

        amount = lines[iterator]

        purchase = Purchase(ref_num=lines[line_number],
                            transaction_date=lines[line_number + 1],
                            post_date=lines[line_number + 2],
                            details=details,
                            amount=amount.replace(",", ""))

        return (purchase, iterator)

    def get_estatements(self):
        """
        Get all estatements from the provided statement directory.
        """
        statements = []
        dirs = os.listdir(self.statement_directory)

        for dir_file in dirs:
            if "e-Statement" in dir_file:
                statements.append(dir_file)

        return statements

    @classmethod
    def is_money(cls, money_str):
        """
        Check if an inputted string is money by checking if there is a "." in the string
        and if it can be converted into a float.
        """
        if "." not in money_str:
            return False
        try:
            float(money_str.replace(",", ""))
            return True
        except ValueError:
            return False

    @classmethod
    def construct_ref_number(cls, num, length_of_ref_num=3):
        """
        Scotiabank reference numbers are numbers with 0 appended in front of them.
        """
        str_num = str(num)

        while len(str_num) != length_of_ref_num:
            str_num = "0" + str_num

        return str_num

    @classmethod
    def get_pages_from_statement(cls, pdf_reader):
        """
        Return a list of the page objects.
        """
        pages = []
        for i in range(0, pdf_reader.numPages):
            pages.append(pdf_reader.getPage(i))

        return pages
