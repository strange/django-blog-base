from django.contrib.markup.templatetags import markup

# Available markup formats.

TEXTILE = 0
MARKDOWN = 1
RESTRUCTUREDTEXT = 2
HTML = 3
PLAIN_TEXT = 4

def to_html(subject, markup_style):
    """Convert ``subject`` to html from markup defined in ``markup_style``.
    
    This relies on the Django markup filters to render html. This isn't really
    ideal, but good enough for now.
    
    """
    if markup_style == TEXTILE:
        return markup.textile(subject)
    elif markup_style == MARKDOWN:
        return markup.markdown(subject)
    elif markup_style == RESTRUCTUREDTEXT:
        return markup.restructuredtext(subject)
    elif markup_style == PLAIN_TEXT:
        from django.utils.html import linebreaks
        return linebreaks(subject, False)
    else:
        return subject
