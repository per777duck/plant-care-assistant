#!/usr/bin/env python3
"""Apply catalog-seed.sql using credentials from application.properties."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPS = ROOT / "src" / "main" / "resources" / "application.properties"
SQL = ROOT / "src" / "main" / "resources" / "db" / "catalog-seed.sql"


def read_props() -> dict[str, str]:
    values = {}
    for line in PROPS.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def parse_jdbc_url(url: str) -> tuple[str, int, str]:
    match = re.match(r"jdbc:postgresql://([^:/]+):(\d+)/(.+)", url)
    if not match:
        raise ValueError(f"Unsupported JDBC URL: {url}")
    return match.group(1), int(match.group(2)), match.group(3)


def main() -> None:
    import psycopg2

    props = read_props()
    host, port, dbname = parse_jdbc_url(props["spring.datasource.url"])
    user = props["spring.datasource.username"]
    password = props["spring.datasource.password"]
    sql = SQL.read_text(encoding="utf-8")

    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute("SELECT COUNT(*) FROM plants")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM plants WHERE image_path IS NOT NULL")
    with_images = cur.fetchone()[0]
    conn.close()
    print(f"Applied seed. Plants: {total}, with image_path: {with_images}")


if __name__ == "__main__":
    main()
