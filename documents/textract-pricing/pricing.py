"""
This file is meant to analyze the pricing of AWS Textract. It is not part of the main application.
We will analyze the pricing of AWS Textract on a per page basis.
The 4 pricing compenents are:
1. QUERIES: $15 per 1000 pages
2. TABLES: $15 per 1000 pages
3. FORMS: $50 per 1000 pages
4. SIGNITURES: $3.50 per 1000 pages
Other pricing components are shown in the self.prices dictionary.
"""

class CostStructure:
    """This class represents the cost structure of AWS Textract."""
    def __init__(self):
        self.prices = {
            "first_million": {
                "queries": 15,
                "tables": 15,
                "forms": 50,
                "signatures": 3.5,
                "queries_tables": 20,
                "forms_queries": 55,
                "tables_forms": 15 + 50,
                "all": 70
            },
            "after_million": {
                "queries": 10,
                "tables": 10,
                "forms": 40,
                "signatures": 1.4,
                "queries_tables": 15,
                "forms_queries": 45,
                "tables_forms": 10 + 40,
                "all": 55
            }
        }

    def calculate_cost(self, pages, type_of_operation):
        """Calculate the cost of operation depending on the number of pages processed"""
        if pages <= 1000000:
            cost_per_thousand_pages = self.prices['first_million'][type_of_operation]
        else:
            cost_per_thousand_pages = self.prices['after_million'][type_of_operation]

        # Cost for the first million pages
        if pages > 1000000:
            cost = cost_per_thousand_pages * 1000
            pages -= 1000000
        else:
            cost = cost_per_thousand_pages * (pages / 1000)
            pages = 0

        # Cost for pages after the first million
        if pages > 0:
            cost += self.prices['after_million'][type_of_operation] * (pages / 1000)

        return cost

if __name__ == '__main__':
    aws_textract = CostStructure()
    print(aws_textract.calculate_cost(20000, 'tables'))