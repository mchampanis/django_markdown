from django.conf import settings
from django.shortcuts import render
import markdown as markdown_module
import string

def preview(request):
    media_or_static = settings.STATIC_URL or settings.MEDIA_URL
    css = getattr(settings, 'DJANGO_MARKDOWN_STYLE', media_or_static + 'django_markdown/preview.css')

    content = request.REQUEST.get('data', 'No content posted')
    section_number = request.REQUEST.get('sectionNumber', 1)

    content = markdown_module.markdown(content)
    content = _parseListNumbers(section_number, content)

    return render(request, 'django_markdown/preview.html', {
        'content': content,
        'css': css
    })

def _parseListNumbers(start_number, text):
    token = "%% "
    token_style = '<div class="sub-section-number">{}</div>\n'
    text_style = '<div class="sub-section-text">{}</div>\n\n'

    text = text.replace("<p>", "")
    text = text.replace("</p>", "")

    index = 0
    parsed = ""
    found = string.find(text, token)

    if found == -1:
        parsed = text_style.replace("{}", text)
    else:
        parsed = text[:found]

        while found != -1:
            index += 1

            parsed += token_style.replace("{}", "{}.{}".format(start_number, index))
            newfound = string.find(text, token, found + 1)

            if newfound == -1:
                parsed += text_style.replace("{}", text[found + len(token):].strip())
            else:
                parsed += text_style.replace("{}", text[found + len(token):newfound].strip())

            found = newfound

    return parsed.strip()
