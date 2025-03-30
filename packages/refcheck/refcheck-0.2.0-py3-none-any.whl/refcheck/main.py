import sys
import requests
import logging
from typing import List
from dataclasses import dataclass

from refcheck.settings import settings
from refcheck.log_conf import setup_logging
from refcheck.parsers import MarkdownParser, Reference
from refcheck.validators import file_exists, is_valid_markdown_reference
from refcheck.utils import (
    get_markdown_files_from_args,
    print_red,
    print_green,
    print_yellow,
)

logger = logging.getLogger()


@dataclass
class BrokenReference(Reference):
    status: str


class ReferenceChecker:
    def __init__(self):
        self.broken_references: List[BrokenReference] = []

    def check_references(self, references: list[Reference]):
        for ref in references:
            logger.info(ref)

            if ref.is_remote and not settings.check_remote:
                logger.warning("Skipping remote reference check.")
                status = print_yellow("SKIPPED")
            elif ref.is_remote and settings.check_remote:
                # Check if remote reference is reachable
                try:
                    response = requests.head(ref.link, timeout=5, verify=False)
                    if response.status_code < 400:
                        status = print_green("OK")
                    else:
                        logger.info(f"Status code: {response.status_code}, Reason: {response.reason}")
                        status = print_red("BROKEN")
                        self.broken_references.append(BrokenReference(**ref.__dict__, status=status))
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error: Could not reach remote reference '{ref.link}': {e}")
                    status = print_red("BROKEN")
                    self.broken_references.append(BrokenReference(**ref.__dict__, status=status))
            else:
                if ".md" in ref.link or "#" in ref.link:
                    if is_valid_markdown_reference(ref):
                        status = print_green("OK")
                    else:
                        status = print_red("BROKEN")
                        self.broken_references.append(BrokenReference(**ref.__dict__, status=status))
                else:
                    if file_exists(ref.file_path, ref.link):
                        status = print_green("OK")
                    else:
                        status = print_red("BROKEN")
                        self.broken_references.append(BrokenReference(**ref.__dict__, status=status))
            print(f"{ref.file_path}:{ref.line_number}: {ref.syntax} - {status}")

    def print_summary(self):
        print("\nReference check complete.")
        print("\n============================| Summary |=============================")

        if self.broken_references:
            print(print_red(f"[!] {len(self.broken_references)} broken references found:"))
            self.broken_references = sorted(self.broken_references, key=lambda ref: (ref.file_path, ref.line_number))

            for broken_ref in self.broken_references:
                print(f"{broken_ref.file_path}:{broken_ref.line_number}: {broken_ref.syntax}")
        else:
            if settings.no_color:
                print("No broken references!")
            else:
                print(print_green("\U0001F389 No broken references!"))

        print("====================================================================")


def main() -> bool:
    # Check if settings configuration is valid
    if not settings.is_valid():
        sys.exit(1)

    # Setup logging based on the --verbose flag
    setup_logging(verbose=settings.verbose)

    check_remote: bool = settings.check_remote
    if not check_remote:
        print(print_yellow("[!] WARNING: Skipping remote reference check. Enable with arg --check-remote."))

    # Retrieve all markdown files specified by the user
    markdown_files = get_markdown_files_from_args(settings.paths, settings.exclude)
    if not markdown_files:
        print(print_red("[!] No Markdown files specified or found."))
        return False

    print(f"\n[+] {len(markdown_files)} Markdown files to check.")
    for file in markdown_files:
        print(f"- {file}")

    md_parser = MarkdownParser()
    checker = ReferenceChecker()

    for file in markdown_files:
        print(f"\n[+] FILE: {file}")
        references = md_parser.parse_markdown_file(file)

        basic_refs = references["basic_references"]
        logging.info(f"Checking {len(basic_refs)} basic references ...")
        checker.check_references(basic_refs)

        image_refs = references["basic_images"]
        logging.info(f"Checking {len(image_refs)} image references ...")
        checker.check_references(image_refs)

        if len(basic_refs) == 0 and len(image_refs) == 0:
            print("No references found.")

        # TODO: activate when pre-processing is implemented in parsers
        # inline_links = references["inline_links"]
        # logging.info(f"Checking {len(inline_links)} inline links ...")
        # checker.check_references(inline_links, check_remote)

    checker.print_summary()
    return not bool(checker.broken_references)


if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
