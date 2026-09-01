import re

def clean_text(text:str)->str:
    """clean extracted document text."""
    if not text:
        return" "

    text=text.replace("\r\n","\n")

    text=re.sub(r"[ \t]+"," ",text)

    text="\n".join(
        line.strip()
        for line in text.split("\n")
    )

    text=re.sub(r"\n{3,}","\n\n",text)

    text=text.strip()

    return text


