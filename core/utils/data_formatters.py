def result_list_to_dict(result):
    return [row._asdict() for row in result]


def result_row_to_dict(result_row):
    return result_row.__dict__

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d