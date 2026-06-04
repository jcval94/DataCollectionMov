from __future__ import annotations

import argparse

from .docs import build_docs
from .runner import run_notebook
from .sources.denue import run_denue
from .sources.ecobici import run_ecobici_catalog, run_ecobici_historical, run_ecobici_realtime
from .sources.google_routes import run_google_routes
from .sources.metrobus import run_metrobus_realtime, run_metrobus_static
from .sources.tomtom import run_tomtom


def main() -> int:
    parser = argparse.ArgumentParser(prog="historico_api")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Ejecuta el notebook y guarda snapshots.")
    run_parser.add_argument("--notebook", required=True)
    run_parser.add_argument("--config", default="configs/tables.yml")
    run_parser.add_argument("--run-date", default=None)
    run_parser.add_argument("--force", action="store_true")

    docs_parser = subparsers.add_parser("docs", help="Genera documentacion de tablas.")
    docs_parser.add_argument("--config", default="configs/tables.yml")

    source_parser = subparsers.add_parser("source", help="Ejecuta una fuente explicita.")
    source_parser.add_argument(
        "source",
        choices=[
            "metrobus_realtime",
            "metrobus_static",
            "tomtom",
            "ecobici_realtime",
            "ecobici_catalog",
            "ecobici_historical",
            "denue",
            "google_routes",
        ],
    )
    source_parser.add_argument("--config", default="configs/tables.yml")
    source_parser.add_argument("--run-date", default=None)
    source_parser.add_argument("--start-month", default=None)
    source_parser.add_argument("--end-month", default=None)

    args = parser.parse_args()

    if args.command == "run":
        run_notebook(args.notebook, args.config, args.run_date, args.force)
        return 0

    if args.command == "docs":
        build_docs(args.config)
        return 0

    if args.command == "source":
        if args.source == "metrobus_realtime":
            run_metrobus_realtime(args.config, args.run_date)
        elif args.source == "metrobus_static":
            run_metrobus_static(args.config, args.run_date)
        elif args.source == "tomtom":
            run_tomtom(args.config, args.run_date)
        elif args.source == "ecobici_realtime":
            run_ecobici_realtime(args.config, args.run_date)
        elif args.source == "ecobici_catalog":
            run_ecobici_catalog(args.config, args.run_date)
        elif args.source == "ecobici_historical":
            run_ecobici_historical(args.config, args.run_date, args.start_month, args.end_month)
        elif args.source == "denue":
            run_denue(args.config, args.run_date)
        elif args.source == "google_routes":
            run_google_routes(args.config, args.run_date)
        return 0

    return 1
