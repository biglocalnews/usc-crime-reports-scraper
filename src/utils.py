import os
import typing
from pathlib import Path

import requests
from rich import print
from documentcloud import DocumentCloud
from documentcloud.exceptions import APIError

# Set directories we'll use all over
THIS_DIR = Path(__file__).parent.absolute()
ROOT_DIR = THIS_DIR.parent
PDF_DIR = ROOT_DIR / "pdfs"


def format_pdf_url(dt):
    """Format the provided datetime to fit the PDF URL expected on our source."""
    return f'https://dps.usc.edu/wp-content/uploads/{dt.strftime("%Y")}/{dt.strftime("%m")}/{dt.strftime("%m%d%y")}.pdf'


def download_url(url: str, output_path: Path, timeout: int = 180):
    """Download the provided URL to the provided path."""
    print(f"Downloading {url}")
    with requests.get(url, stream=True, timeout=timeout) as r:
        if r.status_code == 404:
            print(f"404: {url}")
            return
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def upload_pdf(
    pdf_name: str, verbose: bool = False
) -> tuple[typing.Optional[str], bool]:
    """Upload the provided object's PDF to DocumentCloud.

    Returns tuple with document URL and boolean indicating if it was uploaded.
    """
    # Get PDF path
    pdf_path = PDF_DIR / pdf_name

    # Make sure it exists
    assert pdf_path.exists()

    # Connect to DocumentCloud
    client = DocumentCloud(
        os.getenv("DOCUMENTCLOUD_USER"), os.getenv("DOCUMENTCLOUD_PASSWORD")
    )

    # Search to see if it's already up there
    project_id = os.getenv("DOCUMENTCLOUD_PROJECT_ID")
    query = f"+project:{project_id} AND data_uid:{pdf_name}"
    search = client.documents.search(query)

    # If it is, we're done
    if len(list(search)) > 0:
        if verbose:
            print(f"{pdf_name} already uploaded")
        return search[0].canonical_url, False

    # If it isn't, upload it now
    if verbose:
        print(f"Uploading {pdf_path}")
    try:
        document = client.documents.upload(
            pdf_path,
            title=f"{pdf_name.replace('.pdf', '')}",
            project="210827",
            access="public",
            data={"uid": pdf_name},
        )
        return document.canonical_url, True
    except APIError as e:
        if verbose:
            print(f"API error {e}")
        return None, False
