import click
import requests
from bs4 import BeautifulSoup

from . import utils


@click.command()
def cli():
    """Scrape the latest PDF from the USC website."""
    # Get page
    url = "https://dps.usc.edu/alerts/log/"
    r = requests.get(url)
    assert r.ok

    # Scrape out the PDF link
    soup = BeautifulSoup(r.content, "html5lib")
    link_list = soup.find_all("a")
    pdf_list = [a for a in link_list if a["href"].endswith(".pdf")]
    current_pdf = next(a for a in pdf_list if "current" in a.text.lower())

    # Download it
    pdf_name = current_pdf["href"].split("/")[-1]
    pdf_path = utils.PDF_DIR / pdf_name
    utils.download_url(current_pdf["href"], pdf_path)

    # Upload it
    utils.upload_pdf(pdf_name, verbose=True)


if __name__ == "__main__":
    cli()
