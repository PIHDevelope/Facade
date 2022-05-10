import pyad.adquery as adquery
from prettytable import PrettyTable
from imp import * 

query = adquery.ADQuery()

is_once = False
args = sys.argv
arg_len = len(args)
table = PrettyTable(['Login', 'Enabled', 'Name', 'TelephoneNumber'])
table.align = "l"
while True:
    if arg_len > 1:
        search_attribute = args[1]
    else:
        search_attribute = "samAccountName"
    if arg_len > 2:
        search_value = args[2]
        is_once = True
    else:
       search_value = input(f"Enter {search_attribute}:")
    if search_value == "": search_value = "*"  
    if search_attribute.find("name") != -1:
        search_value = search_value + "*"
    query.execute_query(
        attributes = ["name", "samAccountName, Enabled, TelephoneNumber"],
        where_clause=(f"objectClass = 'user' and {search_attribute} = '{search_value}'"),
    )
    table.clear_rows()
    if query.get_row_count() == 0:
        print(f"{Bcolors.FAIL}Не найдено!{Bcolors.ENDC}")
    else:
        for row in query.get_results():
            table.add_row([row['samAccountName'], row['Enabled'], row['name'], row['TelephoneNumber']])
        print(table)
    if is_once: break