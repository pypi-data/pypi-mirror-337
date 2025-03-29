import threading
import time

import requests

DATADOG_SITES = {
    "US1": "datadoghq.com",
    "US3": "us3.datadoghq.com",
    "US5": "us5.datadoghq.com",
    "EU1": "datadoghq.eu",
    "US1-FED": "ddog-gov.com",
    "AP1": "ap1.datadoghq.com",
}

INTERVAL = 10


TYPE_COUNT = 1
TYPE_RATE = 2  # not used
TYPE_GAUGE = 3


def to_series(metrics: dict) -> dict:
    now = int(time.time())
    return {
        "series": [
            {
                "metric": name,
                "type": metric["type"],
                "points": [
                    {
                        "timestamp": now,
                        "value": metric["value"],
                    }
                ],
            }
            for name, metric in metrics.items()
        ]
    }


# https://docs.datadoghq.com/api/latest/metrics/?site=us3#submit-metrics
class Stats:
    def __init__(self, site: str, api_key: str):
        self.url = f"https://api.{DATADOG_SITES[site]}/api/v2/series"
        self.headers = {"DD-API-KEY": api_key}
        self.metrics = {}
        self.lock = threading.Lock()
        self.sending = False

    def _new_metric(self, name: str, type: int) -> dict:
        if name in self.metrics:
            s = self.metrics[name]
            assert s["type"] == type
            return s

        s = {"type": type, "value": 0}
        self.metrics[name] = s
        return s

    def gauge(self, name: str, value: float) -> None:
        with self.lock:
            s = self._new_metric(name, TYPE_GAUGE)
            s["value"] = value
        self._set_timer()

    def inc(self, name: str, value: int = 1) -> None:
        with self.lock:
            s = self._new_metric(name, TYPE_COUNT)
            s["value"] += value
        self._set_timer()

    def _set_timer(self):
        with self.lock:
            if not self.sending:
                self.sending = True
                timer = threading.Timer(INTERVAL, self._submit)
                timer.start()

    def _submit(self):
        with self.lock:
            metrics = self.metrics
            self.metrics = {}
            self.sending = False

        data = to_series(metrics)
        res = requests.post(self.url, json=data, headers=self.headers)
        if res.status_code != 202:
            raise Exception(f"failed to submit metrics: {res.status_code}, {res.text}")
