def validate_possibility(item):
    text = item['text']
    item['text'] = text.lower().title()
    return item
