import argparse
import json
from tabulate import tabulate
from datetime import datetime

class Expense():
    def __init__(self):
        
        self.data = self.retrieve_data()

        self.parser = argparse.ArgumentParser(description="Add expenses")
        sub = self.parser.add_subparsers(dest="cmd", required= True)

        add_p = sub.add_parser("add")
        add_p.add_argument("-des", "-description", action="store", required=True)
        add_p.add_argument("-amt", "-amount", action="store", type=float)
        add_p.set_defaults(func=self.add)

        upd_p = sub.add_parser("update")
        upd_p.add_argument("--id", "--identification", action="store", required=True)
        upd_p.add_argument("-ndes", "-New Description", action="store")
        upd_p.add_argument("-namt", "-new amount", action="store", type=float) 
        upd_p.set_defaults(func=self.update)

        del_p = sub.add_parser("delete")
        del_p.add_argument("--id", '--identification', action="store", required=True)
        del_p.set_defaults(func=self.delete)

        list_p = sub.add_parser("list")
        list_p.add_argument('-y', '-year', action="store", required=False)
        list_p.add_argument('-m', '-month', action="store", required=False)
        list_p.add_argument('-d', '-day', action="store", required=False)
        list_p.set_defaults(func=self.list)

        summary_p = sub.add_parser("summary")
        summary_p.set_defaults(func=self.summary)

    def retrieve_data(self):
        try:
            with open('expenses_data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def overwrite_file(self, new_data, file_address):
        try:
            with open(file_address, 'w') as file:
                json.dump(new_data, file, indent=4)
        except FileNotFoundError:
            raise FileNotFoundError("Could not find file")

    def table_properties(self, data):
        tab_data = []
        headers = ['Id', 'Time', 'Description', 'Amount']
        for item in data:
            tab_data.append([item['id'], item['time'], item['des'], item['amt']])

        return {'data': data,'tab_data': tab_data, 'header': headers}

    def create_id(self):
        data = self.data
        
        if len(data) == 0:
            return "1"

        new_id = str(int(data[-1]['id']) + 1)

        return new_id

    def add(self, args):
        data = self.data
        now = datetime.now()

        new_data = {
            "id": self.create_id(),
            "time": now.strftime("%Y%m%d"),
            "des": args.des,
            "amt": args.amt
        }

        data.append(new_data)
        self.overwrite_file(data, 'expenses_data.json')

    def update(self, args):
        data = self.data
        now = datetime.now()
        new_data = {
            "id": args.id,
            "time": 0,
            "des": args.ndes,
            "amt": args.namt
        }

        for idx, item in enumerate(data):
            if item['id'] == args.id:
                original_time = data[idx]['time']
                data[idx] = new_data
                data[idx]['time'] = original_time
                
        self.overwrite_file(data, 'expenses_data.json')
                
    def delete(self, args):
        data = self.data

        for idx, item in enumerate(data):
            if item['id'] == args.id:
                data.pop(idx)

        self.overwrite_file(data, 'expenses_data.json')

    def list(self, args):
        if args.m:
            data = self.filter_month(args.m)
        else:
            data = self.data

        tab_props = self.table_properties(data)

        table = tabulate(tab_props['tab_data'], headers=tab_props['header'], tablefmt="grid")
        print(table)

    def filter_month(self, given_month):
        data = self.data
        filtered_list = []
        for idx, item in enumerate(data):
            month = item['time'][4:6]

            if month == given_month:
                filtered_list.append(data[idx])

        return filtered_list

    def summary(self, args):
        tab_props = self.table_properties(self.data)
        data = tab_props['data']
        total_amount = 0.0

        for item in data:
            total_amount += float(item['amt'])
        
        print(f"Total Expenses Amount: ${total_amount:.2f}")

    def run(self):
        args = self.parser.parse_args()
        args.func(args)


if __name__ == "__main__":
    exp = Expense()
    exp.run()