import secrets

from django.shortcuts import get_object_or_404


def part_file(filename):
    return filename.split('.')


def images_upload_path(instance, filename):
    _, extension = part_file(filename)
    new_name = secrets.token_hex(nbytes=5)
    return f'images/{new_name}.{extension}'


def videos_upload_path(instance, filename):
    _, extension = part_file(filename)
    new_name = secrets.token_hex(nbytes=5)
    return f'videos/{new_name}.{extension}'


def files_upload_path(instance, filename):
    _, extension = part_file(filename)
    new_name = secrets.token_hex(nbytes=5)
    return f'files/{new_name}.{extension}'


def parse_quotes(new_comment, quotes: list[int]) -> list[int]:
    """Helper to parse quotes from a new comment"""
    from comments.models import Comment, Quote

    if quotes:
        quote_objs = []
        for quote_id in quotes:
            comment_to_quote = get_object_or_404(Comment(), pk=quote_id)
            quote_objs.append(Quote(
                comment=new_comment,
                quoted_comment=comment_to_quote,
                content=comment_to_quote.content,
                content_html=comment_to_quote.content_html
            ))
        quotes = Quote.objects.bulk_create(quote_objs)
        return quotes
    return []
