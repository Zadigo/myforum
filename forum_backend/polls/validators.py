from moderation.utils import moderate_text

def validate_possibility(item):
    text = item['text']
    moderate_text(text)
    item['text'] = text.lower().title()
    return item
