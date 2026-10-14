import pandas as pd
from typing import Union, BinaryIO


def load_log_file(file_input: Union[str, BinaryIO, pd.DataFrame]) -> pd.DataFrame:
    """
    Reads CSV log data from a file path string, file buffer (Streamlit UploadedFile),
    or returns existing DataFrame.

    Parameters:
        file_input: Path to file, file handle/buffer, or DataFrame.

    Returns:
        pd.DataFrame containing raw log data.
    """
    if isinstance(file_input, pd.DataFrame):
        return file_input.copy()
    
    try:
        return pd.read_csv(file_input)
    except Exception as e:
        raise ValueError(f"Failed to load log file: {str(e)}")
