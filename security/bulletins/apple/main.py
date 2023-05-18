import os
import pathlib
import typing

import parsel
import requests
import sentry_sdk


def get_security_updates() -> typing.Iterator:
    selector = parsel.Selector(
        text=requests.get("https://support.apple.com/en-us/HT201222", timeout=60).text
    )

    for raw in selector.xpath("//table/tbody/tr")[1:]:
        if not (
            (name := raw.xpath("./td/text()").get())
            and (url := raw.xpath("./td/a/@href").get())
        ):
            continue
        yield url.split("/")[-1], name


def main():
    sentry_token = os.environ["TOKEN_SENTRY"]
    sentry_sdk.init(
        dsn=sentry_token,
        traces_sample_rate=1.0,
    )
    path = pathlib.Path(os.environ["DATA_PATH"])
    new_data = dict(get_security_updates())
    delta = new_data.keys() - path.read_text().splitlines()

    chat_id = os.environ["CHAT_ID"]
    for key in delta:
        text = f"{new_data[key]}\nhttps://support.apple.com/kb/{key}\n"
        requests.get(
            "https://api.telegram.org/bot"
            + os.environ["TOKEN_TELEGRAM"]
            + "/sendMessage"
            + "?chat_id="
            + chat_id
            + "&text="
            + text
        )
    with open(path, "a") as f:
        f.writelines(sorted([key + "\n" for key in delta]))


if __name__ == "__main__":
    main()
