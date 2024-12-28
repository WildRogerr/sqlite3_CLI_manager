from typing import List
from db import PAGE_SIZE

def format_db_rows(columns: List[str], rows: List[tuple], page_number:int,table_size:int) -> str:
    number = (page_number - 1) * PAGE_SIZE
    list_rows = []
    end_page = int(table_size/PAGE_SIZE)
    list_rows.append(f'# Page number: {page_number}/{end_page}')
    
    for row in rows:
        number += 1
        list_rows.append(f'# -[ RECORD {number} ]------------------------------')
        for column_name, value in zip(columns, row):
            list_rows.append(f'# {column_name:<20} | {value}')
    list_rows.append('# -------------------------------------------')
    list_rows.append(f'# End page.')
    
    return "\n".join(list_rows)
        