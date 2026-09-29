import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {"level": record.levelname, "message": record.getMessage(), "logger": record.name}
        baseline = logging.LogRecord("", 0, "", 0, "", (), None)
        standard = set(baseline.__dict__) | {"message", "asctime"}
        payload.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key not in standard and not key.startswith("_")
            }
        )
        return json.dumps(payload, default=str)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    if not root.handlers:
        root.addHandler(handler)
        root.setLevel(logging.INFO)
