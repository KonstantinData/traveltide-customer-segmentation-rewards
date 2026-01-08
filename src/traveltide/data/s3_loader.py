from __future__ import annotations

import os
from dataclasses import dataclass
from io import BytesIO
from typing import Iterable

import boto3
import pandas as pd
from dotenv import load_dotenv


@dataclass(frozen=True)
class S3Config:
    access_key_id: str
    secret_access_key: str
    region: str
    bucket: str
    prefix: str


def load_env() -> S3Config:
    load_dotenv()
    access_key = os.getenv("S3_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID", "")
    secret_key = os.getenv("S3_SECRET_ACCESS_KEY") or os.getenv(
        "AWS_SECRET_ACCESS_KEY", ""
    )
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    bucket = os.getenv("TRAVELTIDE_S3_BUCKET", "")
    prefix = os.getenv("TRAVELTIDE_S3_PREFIX", "bronze")

    if not access_key or not secret_key or not bucket:
        raise RuntimeError("Missing S3 credentials or bucket configuration.")

    return S3Config(
        access_key_id=access_key,
        secret_access_key=secret_key,
        region=region,
        bucket=bucket,
        prefix=prefix,
    )


def build_s3_key(table: str, ext: str = "csv", config: S3Config | None = None) -> str:
    cfg = config or load_env()
    suffix = f"{table}.{ext}"
    if not cfg.prefix:
        return suffix
    return f"{cfg.prefix.rstrip('/')}/{suffix}"


def build_s3_uri(table: str, ext: str = "csv", config: S3Config | None = None) -> str:
    cfg = config or load_env()
    key = build_s3_key(table, ext=ext, config=cfg)
    return f"s3://{cfg.bucket}/{key}"


def load_table_from_s3(table: str, ext: str = "csv") -> pd.DataFrame:
    cfg = load_env()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        region_name=cfg.region,
    )
    key = build_s3_key(table, ext=ext, config=cfg)
    obj = s3.get_object(Bucket=cfg.bucket, Key=key)
    body = obj["Body"].read()

    extension = ext.lower()
    if extension == "csv":
        return pd.read_csv(BytesIO(body))
    if extension == "parquet":
        return pd.read_parquet(BytesIO(body))
    raise ValueError(f"Unsupported extension: {ext}")


def load_bronze_tables(
    tables: Iterable[str],
    ext: str = "csv",
) -> dict[str, pd.DataFrame]:
    return {table: load_table_from_s3(table, ext=ext) for table in tables}
