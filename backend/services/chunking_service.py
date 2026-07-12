from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_utils import read_file_safe

def chunk_repo_files(files: list[dict]) -> list[dict]:
    """
    Takes the file list from walk_repo_files.
    For each file: reads its content (using read_file_safe from utils.file_utils),
    splits it into chunks using RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150,
    separators=["\nclass ", "\ndef ", "\nfunction ", "\n\n", "\n", " "]),
    skips files that returned None from read_file_safe.

    Returns a list of dicts, one per chunk:
    {
        "id": f"{relative_path}::chunk_{i}",   # unique id per chunk
        "text": chunk_text,
        "metadata": { "file_path": relative_path, "chunk_index": i }
    }
    """
    # Why separators list is ordered this way:
    # RecursiveCharacterTextSplitter tries each separator in order.
    # Trying to split on code construct boundaries (\nclass, \ndef, \nfunction) FIRST
    # means chunks tend to align with actual code structures (keeping whole functions/classes together)
    # instead of cutting lines arbitrarily mid-statement.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\nclass ", "\ndef ", "\nfunction ", "\n\n", "\n", " "]
    )
    
    all_chunks = []
    
    for file_info in files:
        relative_path = file_info["path"]
        full_path = file_info["full_path"]
        
        content = read_file_safe(full_path)
        if content is None:
            # Skip binary files or decoding failure files
            continue
            
        # Perform chunking on the file content
        chunks = text_splitter.split_text(content)
        
        for i, chunk_text in enumerate(chunks):
            # Why chunk_overlap=150 matters:
            # Without overlap, if a function or class definition is split exactly on the 1000-character boundary,
            # its signature might end up in one chunk and its implementation body in the next.
            # Overlap preserves surrounding context across both halves, allowing queries about the function
            # to retrieve semantic information matching either side of the split.
            chunk_id = f"{relative_path}::chunk_{i}"
            all_chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    "file_path": relative_path,
                    "chunk_index": i
                }
            })
            
    return all_chunks
