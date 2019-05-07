import re


def find_string(text, search_string):
    start = re.search(re.escape(search_string), text)
    if start is None:
        return None
    return start.start()


def extract_data(text, search_string_start, search_string_end):
    start = find_string(text, search_string_start)
    if start is None:
        return None
    end = find_string(text[start:], search_string_end)
    if end is None:
        return None
    return text[start:start + end + len(search_string_end)]


def trim_tags(text):
    if text is None:
        return None
    while True:
        res = extract_data(text, "<", ">")
        if res is None:
            return text
        text = text.replace(res, "")


def remove_whitespaces(text):
    if text is None:
        return None
    return " ".join(text.split())


def remove_javascript(text):
    if text is None:
        return None
    while True:
        res = extract_data(text, "<script", "</script>")
        if res is None:
            return text
        text = text.replace(res, "")


def clean_text(text):
    return remove_whitespaces(trim_tags(remove_javascript(text)))
