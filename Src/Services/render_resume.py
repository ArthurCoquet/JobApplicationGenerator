from pathlib import Path
import json

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright


def render_resume(json_path: str, template_path: str) -> str:

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    template_path = Path(template_path)

    env = Environment(
        loader=FileSystemLoader(template_path.parent)
    )

    template = env.get_template(template_path.name)

    return template.render(
        resume=data["resume"]
    )


def html_to_pdf(
    html: str,
    html_path: str,
    pdf_path: str,
) -> None:

    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    html_path.write_text(
        html,
        encoding="utf-8"
    )

    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page(
            viewport={
                "width": 794,
                "height": 1123,
            }
        )

        page.goto(
            html_path.as_uri(),
            wait_until="networkidle"
        )

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0",
            },
        )

        browser.close()


if __name__ == "__main__":

    html = render_resume(
        json_path=r"Offers\Data Analyst - Audensiel Technologies.json",
        template_path=r"C:\Users\arthu\OneDrive\Bureau\TailoredResume\Templates\resume_template.html"
    )

    html_to_pdf(
        html=html,
        html_path="output.html",
        pdf_path="output.pdf",
    )

    print("HTML généré : output.html")
    print("PDF généré  : output.pdf")