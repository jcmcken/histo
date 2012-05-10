def build_datum(line, key_expr, delim):
    pass

def parse_key_expr(expr):
    return [ parse_key_expr_item(item) for item in expr.split(',') ]

def parse_key_expr_item(item):
    if ':' in item:
        parse = parse_rangelike
        slice_up = slice_range
    else:
        parse = parse_intlike
        slice_up = lambda x: x
    return slice_up(parse(item))

def slice_int(val):
    return (val, val + 1)

def slice_range(items):
    return slice(items[0], items[1] + 1)

def parse_rangelike(item):
    items = item.split(':')
    invalid = SyntaxError('invalid slice syntax in key item "%s"' % item)
    if len(items) != 2: raise invalid
    try:
        item1, item2 = map(str_to_int, items)
    except SyntaxError, e:
        raise SyntaxError(e.args[0] + ' from slice "%s"' % item)
    if item1 > item2:
        raise SyntaxError('item 1 in slice "%s" is not less than item 2' % item)
    item2 = rectify_slice_item(item2)
    return (item1, item2)

def rectify_slice_item(item):
    if item == -1:
        item = None # do inclusive ranges, not half-open like Python
    else:
        item += 1
    return item 

def str_to_int(data):
    try:
        data = int(data)
    except (ValueError, TypeError):
        raise SyntaxError('non-integer input in key data "%s"' % data)
    return data

def parse_intlike(item):
    item1 = str_to_int(item)
    item2 = rectify_slice_item(item1)
    return (item1, item2)
