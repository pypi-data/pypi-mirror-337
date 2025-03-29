from pathlib import Path

from pheval_svanna.post_process.post_process_results_format import create_standardised_results
from pheval_svanna.tool_specific_configuration_parser import SvAnnaToolSpecificConfigurations


def post_process_results_format(
    raw_results_dir: Path,
    output_dir: Path,
    phenopacket_dir: Path,
    config: SvAnnaToolSpecificConfigurations,
):
    """Create pheval gene and variant result from SvAnna tsv output."""
    print("...creating pheval results format...")
    create_standardised_results(
        raw_results_dir=raw_results_dir,
        output_dir=output_dir,
        phenopacket_dir=phenopacket_dir,
        sort_order=config.post_process.sort_order,
    )
    print("done")
