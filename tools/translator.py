import requests
import re
import html
import urllib.parse

def translate_text(text, target_language='hi', source_language='auto'):
    try:
        if len(text) > 5000:
            return f"[Translation failed - text too long ({len(text)} characters)]: {text}"

        escaped_text = urllib.parse.quote(text.encode('utf8'))
        url = f'https://translate.google.com/m?tl={target_language}&sl={source_language}&q={escaped_text}'

        response = requests.get(url, timeout=5)
        pattern = r'(?s)class="(?:t0|result-container)">(.*?)<'
        result = re.findall(pattern, response.text)

        if result:
            return html.unescape(result[0])
        else:
            return f"[Translation to {target_language} failed - no result]: {text}"

    except Exception as e:
        return f"[Translation to {target_language} failed]: {text}"
