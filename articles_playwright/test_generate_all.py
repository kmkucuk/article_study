from playwright.sync_api import Page
from time import sleep
import csv


def test_all(page: Page):
    page.set_viewport_size({"width": 2560, "height": 1900})
    for i in range(1, 7):
        for font in ["Times New Roman", "Georgia", "Roboto"]:
            for link in [True, False]:
                f = "Times" if font == "Times New Roman" else font
                l = "Link" if link else "NoLink"

                url = f"http://localhost:8090/?article={i}&font={font}&links={link}"
                print(url)
                page.goto(url)

                if link:
                    with open(f"./output/article{i}_{f}_links.csv", "a") as output:
                        csv_writer = csv.writer(output)
                        csv_writer.writerow(
                            [
                                "text",
                                "x",
                                "y",
                                "width",
                                "height",
                                f"{f[0].upper()}{f[1:]}_Y",
                            ]
                        )

                        for locator in page.get_by_role("link").all():
                            bounding_box = locator.bounding_box()
                            if bounding_box is None:
                                continue
                            csv_writer.writerow(
                                [
                                    locator.inner_text(),
                                    bounding_box.get("x"),
                                    bounding_box.get("y") + bounding_box.get("height"),
                                    bounding_box.get("width"),
                                    bounding_box.get("height"),
                                ]
                            )

                sleep(2)
                page.screenshot(
                    path=f"./output/article{i}_{f}_{l}.jpg", full_page=True, type="jpeg"
                )

    for link in [True, False]:
        l = "Link" if link else "NoLink"
        page.goto(f"http://localhost:8090/?article=7&font=Open Sans&links=True")
        if link:
            with open(f"./output/article7_Open Sans_links.csv", "a") as output:
                csv_writer = csv.writer(output)
                csv_writer.writerow(
                    [
                        "text",
                        "x",
                        "y",
                        "width",
                        "height",
                        f"Open Sans_Y",
                    ]
                )

                for locator in page.get_by_role("link").all():
                    bounding_box = locator.bounding_box()
                    if bounding_box is None:
                        break
                    csv_writer.writerow(
                        [
                            locator.inner_text(),
                            bounding_box.get("x"),
                            bounding_box.get("y") + bounding_box.get("height"),
                            bounding_box.get("width"),
                            bounding_box.get("height"),
                        ]
                    )
        sleep(2)
        page.screenshot(
            path=f"./output/article7_Open Sans_{link}.jpg", full_page=True, type="jpeg"
        )
