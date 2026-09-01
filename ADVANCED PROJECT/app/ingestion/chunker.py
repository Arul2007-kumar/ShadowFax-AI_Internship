from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(
        text: str,
        chunk_size: int=800,
        chunk_overlap:int=150
)->list[str]:
    if not text.strip():
        return[]

    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ".",
            " ",
            ""
        ]
    )

    chunks=splitter.split_text(text)

    return chunks

