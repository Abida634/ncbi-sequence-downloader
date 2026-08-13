"""Command-line interface for the NCBI Sequence Downloader."""

import argparse
import logging
import sys

from rich.console import Console
from rich.table import Table

from downloader.config import Config
from downloader.downloader import Downloader
from downloader.exceptions import DownloaderError
from downloader.history import HistoryManager
from downloader.logger import setup_logging
from downloader.statistics import compute_stats

console = Console()


def build_parser() -> argparse.ArgumentParser:
    """Construct the argparse parser defining our CLI's arguments.

    Returns:
        A configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="ncbi-downloader",
        description="Download DNA, RNA, or protein sequences from NCBI.",
    )
    parser.add_argument(
        "-a", "--accession",
        type=str,
        help="Accession number to download, e.g. NM_001301717",
    )
    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["fasta", "genbank"],
        default="fasta",
        help="Download format (default: fasta)",
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show download history and exit",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (DEBUG-level) console logging",
    )
    return parser


def run_download(accession: str, fmt: str, downloader: Downloader) -> None:
    """Run a single download and display the result using Rich formatting.

    Args:
        accession: The accession number to download.
        fmt: The download format ("fasta" or "genbank").
        downloader: The Downloader instance to use.
    """
    try:
        with console.status(f"[bold green]Downloading {accession} ({fmt})..."):
            result = downloader.download(accession=accession, fmt=fmt)

        stats = compute_stats(result.record)

        console.print(f"[bold green]✔ Download complete![/bold green]")
        console.print(f"  Saved to: [cyan]{result.saved_path}[/cyan]")
        console.print(f"  {stats.summary()}")

    except DownloaderError as exc:
        console.print(f"[bold red]✘ Error:[/bold red] {exc}")
        sys.exit(1)


def show_history(history: HistoryManager) -> None:
    """Display the full download history as a Rich table.

    Args:
        history: The HistoryManager to load entries from.
    """
    entries = history.load_all()

    if not entries:
        console.print("[yellow]No download history yet.[/yellow]")
        return

    table = Table(title="Download History")
    table.add_column("Timestamp", style="dim")
    table.add_column("Accession", style="cyan")
    table.add_column("Format")
    table.add_column("Saved Path")

    for entry in entries:
        table.add_row(entry.timestamp, entry.accession, entry.format, entry.saved_path)

    console.print(table)


def run_interactive_menu(downloader: Downloader, history: HistoryManager) -> None:
    """Run a simple guided menu loop for users who prefer prompts over flags.

    Args:
        downloader: The Downloader instance to use.
        history: The HistoryManager to use for the "view history" option.
    """
    while True:
        console.print("\n[bold]NCBI Sequence Downloader[/bold]")
        console.print("1) Download a sequence")
        console.print("2) View download history")
        console.print("3) Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            accession = input("Enter accession number: ").strip()
            fmt = input("Format (fasta/genbank) [fasta]: ").strip().lower() or "fasta"
            run_download(accession, fmt, downloader)
        elif choice == "2":
            show_history(history)
        elif choice == "3":
            console.print("Goodbye!")
            break
        else:
            console.print("[yellow]Invalid choice, please enter 1, 2, or 3.[/yellow]")


def main() -> None:
    """The CLI's entry point: parse arguments and dispatch to the right mode."""
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(level=logging.DEBUG if args.verbose else logging.INFO)

    try:
        config = Config.from_env()
    except DownloaderError as exc:
        console.print(f"[bold red]Configuration error:[/bold red] {exc}")
        sys.exit(1)

    downloader = Downloader(config)
    history = HistoryManager()

    if args.history:
        show_history(history)
    elif args.accession:
        run_download(args.accession, args.format, downloader)
    else:
        run_interactive_menu(downloader, history)


if __name__ == "__main__":
    main()