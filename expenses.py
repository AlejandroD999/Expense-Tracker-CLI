import argparse
import json
from tabulate import tabulate
import time

class Expense():
    def __init__(self):
        
        self.parser = argparse.ArgumentParser(description="Add expenses")
        sub = self.parser.add_subparsers(dest="cmd", required= True)

        add_p = sub.add_parser("add")
        add_p.add_argument("--des", "--description", action="store")
        add_p.add_argument("--amt", "--amount", action="store", type=float)
        add_p.set_defaults(func=self.add)

        list_p = sub.add_parser("list")
        list_p.set_defaults(func=self.list)

        summary_p = sub.add_parser("summary")
        summary_p.set_defaults(func=self.summary)

    def retrieve(self):
        try:
            with open('expenses_data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def table_properties(self):
        data = self.retrieve()
        tab_data = []
        headers = ['Id', 'Time', 'Description', 'Amount']
        for item in data:
            tab_data.append([item['id'], item['time'], item['des'], item['amt']])

        return {'data': data,'tab_data': tab_data, 'header': headers}

    def add(self, args):
        new_data = {
            "id": self.create_id,
            "time": time.ctime,
            "des": args.des,
            "amt": args.amt
        }

        try:
            with open('expenses_data.json', 'r') as file:
                data = json.load(file)
                print(data)
        except FileNotFoundError:
            data = []

                
    
    def create_id(self):
        data = self.retrieve()
        new_id = str(int(data[-1]['id']) + 1)

        return


    def update(self):
        pass
 
    def delete(self):
        pass

    def list(self, args):
        tab_props = self.table_properties()

        table = tabulate(tab_props['tab_data'], headers=tab_props['header'], tablefmt="grid")
        print(table)

    def summary(self, args):
        tab_props = self.table_properties()
        data = tab_props['data']
        total_amount = 0

        for item in data:
            total_amount += item['amt']
        
        print(f"Total Expenses Amount: ${total_amount}")

    
    def run(self):
        args = self.parser.parse_args()
        args.func(args)


if __name__ == "__main__":
    exp = Expense()
    exp.run()