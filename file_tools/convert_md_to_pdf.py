"""Convert Markdown files to PDF using pandoc."""

import os

import pypandoc


def markdown_to_pdf(input_md_file, output_pdf_file, extra_args=None):
    """Convert a Markdown file to PDF format.

    Args:
        input_md_file: Path to the input Markdown (.md) file.
        output_pdf_file: Path for the output PDF file.
        extra_args: Optional list of extra arguments for pandoc (e.g., ['--pdf-engine=xelatex']).

    Raises:
        FileNotFoundError: If the input file does not exist.
        RuntimeError: If the conversion fails.
    """
    if not os.path.exists(input_md_file):
        raise FileNotFoundError(f"Input file not found: {input_md_file}")

    try:
        pypandoc.convert_file(
            input_md_file,
            "pdf",
            outputfile=output_pdf_file,
            extra_args=extra_args or [],
        )
        print(f"Converted: {input_md_file} -> {output_pdf_file}")
    except Exception as e:
        raise RuntimeError(f"PDF conversion failed: {e}") from e


if __name__ == "__main__":
    markdown_to_pdf("input.md", "output.pdf")