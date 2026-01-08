from __future__ import annotations

from io import BytesIO

import pandas as pd

from traveltide.data.s3_loader import load_table_from_s3


class DummyS3:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload
        self.calls: list[tuple[str, str]] = []

    def get_object(self, *, Bucket: str, Key: str):
        self.calls.append((Bucket, Key))
        return {"Body": BytesIO(self.payload)}


def _set_env(monkeypatch) -> tuple[str, str]:
    bucket = "test-bucket"
    prefix = "bronze"
    monkeypatch.setenv("S3_ACCESS_KEY_ID", "access")
    monkeypatch.setenv("S3_SECRET_ACCESS_KEY", "secret")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("TRAVELTIDE_S3_BUCKET", bucket)
    monkeypatch.setenv("TRAVELTIDE_S3_PREFIX", prefix)
    return bucket, prefix


def test_load_table_from_s3_csv(monkeypatch):
    df = pd.DataFrame({"user_id": [1, 2], "value": [10, 20]})
    payload = df.to_csv(index=False).encode("utf-8")
    dummy = DummyS3(payload)
    bucket, prefix = _set_env(monkeypatch)

    monkeypatch.setattr("boto3.client", lambda *args, **kwargs: dummy)

    out = load_table_from_s3("sessions", ext="csv")

    pd.testing.assert_frame_equal(out, df)
    assert dummy.calls == [(bucket, f"{prefix}/sessions.csv")]


def test_load_table_from_s3_parquet(monkeypatch):
    df = pd.DataFrame({"user_id": [1, 2], "value": [10.5, 20.5]})
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    payload = buffer.getvalue()
    dummy = DummyS3(payload)
    bucket, prefix = _set_env(monkeypatch)

    monkeypatch.setattr("boto3.client", lambda *args, **kwargs: dummy)

    out = load_table_from_s3("sessions", ext="parquet")

    pd.testing.assert_frame_equal(out, df)
    assert dummy.calls == [(bucket, f"{prefix}/sessions.parquet")]
