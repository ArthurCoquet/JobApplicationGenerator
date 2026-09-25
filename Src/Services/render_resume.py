from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright


class ResumeRenderer:

    def __init__(
        self,
        template_path: str,
        output_dir: str,
    ):
        self.template_path = Path(template_path)
        self.output_dir = Path(output_dir)

    async def render(self, job_offer) -> None:

        env = Environment(
            loader=FileSystemLoader(self.template_path.parent)
        )

        template = env.get_template(self.template_path.name)

        html = template.render(
            resume=job_offer.resume
        )

        # output/{job_offer.title}/
        job_output_dir = self.output_dir / job_offer.title / "resume"
        job_output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        html_path = job_output_dir / "output.html"
        pdf_path = job_output_dir / "output.pdf"

        html_path.write_text(
            html,
            encoding="utf-8"
        )

        async with async_playwright() as p:

            browser = await p.chromium.launch()

            page = await browser.new_page(
                viewport={
                    "width": 794,
                    "height": 1123,
                }
            )

            await page.goto(
                html_path.resolve().as_uri(),
                wait_until="networkidle"
            )

            await page.pdf(
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

            await browser.close()