def format_db_rows(columns, rows) -> str:
    number = 0
    list_rows = []
    list_rows.append('# Optional page number')
    
    # Итерация по строкам данных
    for row in rows:
        number += 1
        list_rows.append(f'# -[ RECORD {number} ]------------------------------')
        
        # Итерация по колонкам и значениям
        for column_name, value in zip(columns, row):
            list_rows.append(f'# {column_name:<20} | {value}')
    
    return "\n".join(list_rows)
        