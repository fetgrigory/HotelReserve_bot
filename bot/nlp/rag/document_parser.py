import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from apps.support.models import DocumentChunk


# Load PDF and extract text
def parse_document(file_path: str) -> list[Document]:

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    full_text = "\n".join(doc.page_content for doc in documents)

    # Fix words broken by line breaks
    full_text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", full_text)
    full_text = re.sub(r"(\w)\s*\n\s*(\w)", r"\1 \2", full_text)
    full_text = re.sub(r" +", " ", full_text)

    # Separate list items with double line break
    markers = [
        r"\n\s*([а-яёa-z]\))",
        r"\n\s*(\d{1,2}\))",
        r"\n\s*(\d{1,2}\.\s+[А-ЯЁа-яёA-Za-z])",
        r"\n\s*([-•]\s+[А-ЯЁа-яёA-Za-z])",
    ]

    for pattern in markers:
        full_text = re.sub(pattern, r"\n\n\1", full_text)

    # Heading pattern
    heading_pattern = r"[А-ЯЁA-Z][А-ЯЁA-Z\s:,«»\-\(\)№\d]{10,150}"

    header_pattern = re.compile(
        rf"^{heading_pattern}$",
        re.MULTILINE,
    )

    # Separate text into sections by headings
    parts = re.split(
        rf"(\n\s*{heading_pattern}\s*\n)",
        full_text,
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
    )

    chunks = []
    current_header = ""

    for part in parts:
        part_stripped = part.strip()

        if not part_stripped:
            continue

        # Check if part is a heading
        if header_pattern.match(part_stripped):
            current_header = part_stripped
            continue

        sub_chunks = splitter.split_text(part_stripped)

        for sub in sub_chunks:
            if sub.strip():
                # Add heading to preserve context
                chunk_text = (
                    f"{current_header}\n\n{sub.strip()}"
                    if current_header
                    else sub.strip()
                )

                chunks.append(
                    Document(page_content=chunk_text)
                )

    return chunks


class DocumentProcessor:
    @staticmethod
    def process(
        file_path: str,
        document_title: str,
        file_name: str,
    ) -> list[DocumentChunk]:

        chunks = parse_document(file_path)

        if not chunks:
            return []

        document_chunks = [
            DocumentChunk(
                document_title=document_title,
                file=file_name,
                content=chunk.page_content,
                chunk_index=index,
            )
            for index, chunk in enumerate(chunks)
        ]

        return DocumentChunk.objects.bulk_create(document_chunks)