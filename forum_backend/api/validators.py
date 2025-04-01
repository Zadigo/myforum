def validate_post_content(content):
    from nltk.tokenize import TweetTokenizer
    
    tokenizer = TweetTokenizer()
    tokenizer.tokenize(content)
    return content
