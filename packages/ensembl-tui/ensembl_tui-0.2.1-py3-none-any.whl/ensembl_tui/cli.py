import pathlib
import shutil
import sys
import typing
from collections import OrderedDict
from collections.abc import Mapping

import click
import trogon
from cogent3 import get_app, open_data_store
from scitrack import CachingLogger

from ensembl_tui import __version__
from ensembl_tui import _config as eti_config
from ensembl_tui import _download as eti_download
from ensembl_tui import _genome as eti_genome
from ensembl_tui import _homology as eti_homology
from ensembl_tui import _species as eti_species
from ensembl_tui import _util as eti_util

if typing.TYPE_CHECKING:
    from click.core import Context, Option


def _values_from_csv_or_file(
    ctx: "Context",  # noqa: ARG001
    param: "Option",  # noqa: ARG001
    value: str | None,
) -> list[str] | None:
    """extract values from command line or a file

    Notes
    -----
    converts either comma separated values or a file with one value per line
    into values
    """
    if not value:
        return None

    path = pathlib.Path(value)
    if path.is_file():
        return [l.strip() for l in path.read_text().splitlines()]

    return [f.strip() for f in value.split(",")]


def _get_installed_config_path(
    ctx: "Context",  # noqa: ARG001
    param: "Option",  # noqa: ARG001
    path: pathlib.Path | str | None,
) -> pathlib.Path:
    """path to installed.cfg"""
    path = pathlib.Path(path or ".")
    if path.name == eti_config.INSTALLED_CONFIG_NAME:
        return path

    path = path / eti_config.INSTALLED_CONFIG_NAME
    if not path.exists():
        eti_util.print_colour(text=f"{path!s} missing", colour="red")
        sys.exit(1)
    return path


def _species_names_from_csv(
    ctx: "Context",
    param: "Option",
    species: str,
) -> list[str] | None:
    """returns species names"""
    species_names = _values_from_csv_or_file(ctx, param, species)
    if species_names is None:
        return None

    db_names = []
    for name in species_names:
        try:
            db_name = eti_species.Species.get_ensembl_db_prefix(name)
        except ValueError:
            eti_util.print_colour(text=f"ERROR: unknown species {name!r}", colour="red")
            sys.exit(1)

        db_names.append(db_name)

    return db_names


_csv_or_file_help = "(comma separated or a path to file of names, one per line)"

_click_command_opts = {
    "no_args_is_help": True,
    "context_settings": {"show_default": True},
}

# defining some of the options
_cfgpath = click.option(
    "-c",
    "--configpath",
    type=pathlib.Path,
    help="Path to config file specifying databases, (only "
    "species or compara at present).",
)
_download = click.option(
    "-d",
    "--download",
    type=pathlib.Path,
    help="Path to local download directory containing a cfg file.",
)
_installed = click.option(
    "-i",
    "--installed",
    required=True,
    callback=_get_installed_config_path,
    help="Path to root directory of an installation.",
)
_outdir = click.option(
    "-od",
    "--outdir",
    required=True,
    type=pathlib.Path,
    help="Path to write files",
)
_align_name = click.option(
    "--align_name",
    default=None,
    required=True,
    help="Ensembl alignment name or a glob pattern, e.g. '*primates*'.",
)
_ref = click.option("--ref", default=None, help="Reference species.")
_ref_genes_file = click.option(
    "--ref_genes_file",
    default=None,
    type=click.Path(resolve_path=True, exists=True),
    help=".csv or .tsv file with a header containing a stableid column.",
)
_mask_ref = click.option(
    "--mask_ref",
    is_flag=True,
    help="Masking uses features from ref species only.",
)
_limit = click.option(
    "--limit",
    type=int,
    default=None,
    help="Limit to this number of genes.",
    show_default=True,
)
_verbose = click.option(
    "-v",
    "--verbose",
    is_flag=True,
)
_force = click.option(
    "-f",
    "--force_overwrite",
    is_flag=True,
    help="Overwrite existing data.",
)
_debug = click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Maximum verbosity, and reduces number of downloads, etc...",
)
_dbrc_out = click.option(
    "-o",
    "--outpath",
    type=pathlib.Path,
    help="Path to directory to export all rc contents.",
)
_nprocs = click.option(
    "-np",
    "--num_procs",
    type=int,
    default=1,
    help="Number of procs to use.",
    show_default=True,
)
_outdir = click.option(
    "--outdir",
    type=pathlib.Path,
    default=".",
    help="Output directory name.",
    show_default=True,
)
_species = click.option(
    "--species",
    required=True,
    callback=_species_names_from_csv,
    help="Single species name or multiple (comma separated).",
)
_mask = click.option(
    "--mask",
    callback=_values_from_csv_or_file,
    help=f"mask the specified biotypes {_csv_or_file_help}.",
)
_mask_shadow = click.option(
    "--mask_shadow",
    callback=_values_from_csv_or_file,
    help=f"mask everything but the specified biotypes {_csv_or_file_help}.",
)
_coord_names = click.option(
    "--coord_names",
    default=None,
    callback=_values_from_csv_or_file,
    help=f"list of ref species chrom/coord names {_csv_or_file_help}.",
)


class OrderedGroup(click.Group):
    def __init__(
        self,
        name: str | None = None,
        commands: Mapping[str, click.Command] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(name, commands, **kwargs)
        #: the registered subcommands by their exported names.
        self.commands = commands or OrderedDict()

    def list_commands(self, ctx: click.Context) -> Mapping[str, click.Command]:
        return self.commands


@trogon.tui()
@click.group(cls=OrderedGroup, **_click_command_opts)
@click.version_option(__version__)
def main() -> None:
    """Tools for obtaining and interrogating subsets of https://ensembl.org genomic data."""


@main.command(**_click_command_opts)
@_dbrc_out
def exportrc(outpath: pathlib.Path) -> None:
    """exports sample config and species table to the nominated path"""

    outpath = outpath.expanduser()

    shutil.copytree(eti_util.ENSEMBLDBRC, outpath)
    # we assume all files starting with alphabetical characters are valid
    for fn in pathlib.Path(outpath).glob("*"):
        if not fn.stem.isalpha():
            if fn.is_file():
                fn.unlink()
            else:
                # __pycache__ directory
                shutil.rmtree(fn)
    eti_util.print_colour(text=f"Contents written to {outpath}", colour="green")


@main.command(**_click_command_opts)
@_cfgpath
@_debug
@_verbose
def download(configpath: pathlib.Path, debug: bool, verbose: bool) -> None:
    """download data from Ensembl's ftp site"""
    from rich import progress

    if not configpath:
        eti_util.print_colour(
            text="No config specified, exiting.",
            colour="red",
            style="bold",
        )
        sys.exit(1)

    config = eti_config.read_config(configpath, root_dir=pathlib.Path.cwd())

    if verbose:
        eti_util.print_colour(text=str(config), colour="yellow")

    if not any((config.species_dbs, config.align_names)):
        eti_util.print_colour(text="No genomes, no alignments specified", colour="red")
        sys.exit(1)

    if not config.species_dbs:
        species = eti_download.get_species_for_alignments(
            host=config.host,
            remote_path=config.remote_path,
            release=config.release,
            align_names=config.align_names,
        )
        config.update_species(species)

    if verbose:
        eti_util.print_colour(text=str(config.species_dbs), colour="yellow")

    config.write()
    with (
        eti_util.keep_running(),
        progress.Progress(
            progress.TextColumn("[progress.description]{task.description}"),
            progress.BarColumn(),
            progress.TaskProgressColumn(),
            progress.TimeRemainingColumn(),
            progress.TimeElapsedColumn(),
        ) as progress,
    ):
        eti_download.download_species(config, debug, verbose, progress=progress)
        eti_download.download_homology(config, debug, verbose, progress=progress)
        eti_download.download_aligns(config, debug, verbose, progress=progress)

    eti_util.print_colour(text=f"Downloaded to {config.staging_path}", colour="green")


@main.command(**_click_command_opts)
@_download
@_nprocs
@_force
@_verbose
def install(
    download: pathlib.Path,
    num_procs: int,
    force_overwrite: bool,
    verbose: bool,
) -> None:
    """create the local representations of the data"""
    from rich import progress

    from ensembl_tui._install import (
        local_install_alignments,
        local_install_genomes,
        local_install_homology,
    )

    configpath = download / eti_config.DOWNLOADED_CONFIG_NAME
    config = eti_config.read_config(configpath)
    if verbose:
        eti_util.print_colour(text=f"{config.install_path=}", colour="yellow")

    if force_overwrite:
        shutil.rmtree(config.install_path, ignore_errors=True)

    config.install_path.mkdir(parents=True, exist_ok=True)
    eti_config.write_installed_cfg(config)
    with (
        eti_util.keep_running(),
        progress.Progress(
            progress.TextColumn("[progress.description]{task.description}"),
            progress.BarColumn(),
            progress.TaskProgressColumn(),
            progress.TimeRemainingColumn(),
            progress.TimeElapsedColumn(),
        ) as progress,
    ):
        local_install_genomes(
            config,
            force_overwrite=force_overwrite,
            max_workers=num_procs,
            verbose=verbose,
            progress=progress,
        )
        local_install_homology(
            config,
            force_overwrite=force_overwrite,
            max_workers=num_procs,
            verbose=verbose,
            progress=progress,
        )
        local_install_alignments(
            config,
            force_overwrite=force_overwrite,
            max_workers=num_procs,
            verbose=verbose,
            progress=progress,
        )

    eti_util.print_colour(
        text=f"Contents installed to {str(config.install_path)!r}",
        colour="green",
    )


@main.command(**_click_command_opts)
@_installed
def installed(installed: pathlib.Path) -> None:
    """show what is installed"""
    from cogent3 import make_table

    config = eti_config.read_installed_cfg(installed)

    genome_dir = config.genomes_path
    if genome_dir.exists():
        species = [fn.name for fn in genome_dir.glob("*")]
        data = {"species": [], "common name": []}
        for name in species:
            cn = eti_species.Species.get_common_name(name, level="ignore")
            if not cn:
                continue
            data["species"].append(name)
            data["common name"].append(cn)

        table = make_table(data=data, title="Installed genomes:")
        eti_util.rich_display(table)

    if config.homologies_path.exists():
        eti_util.print_colour("Installed homologies: ✅", colour="blue", style="bold")

    # TODO as above
    compara_aligns = config.aligns_path
    if compara_aligns.exists():
        align_names = {
            fn.stem for fn in compara_aligns.glob("*") if not fn.name.startswith(".")
        }
        eti_util.print_colour(
            "Installed whole genome alignments:",
            colour="blue",
            style="bold",
        )
        table = make_table(
            data={"align name": list(align_names)},
        )
        eti_util.rich_display(table)


@main.command(**_click_command_opts)
@_installed
@_species
def species_summary(installed: pathlib.Path, species: str) -> None:
    """genome summary data for a species"""

    config = eti_config.read_installed_cfg(installed)
    if species is None:
        eti_util.print_colour(text="ERROR: a species name is required", colour="red")
        sys.exit(1)

    if len(species) > 1:
        eti_util.print_colour(
            text=f"ERROR: one species at a time, not {species!r}",
            colour="red",
        )
        sys.exit(1)

    species = species[0]
    annot_db = eti_genome.load_annotations_for_species(
        path=config.installed_genome(species=species),
    )
    summary = eti_genome.get_species_gene_summary(annot_db=annot_db, species=species)
    eti_util.rich_display(summary)
    summary = eti_genome.get_species_repeat_summary(annot_db=annot_db, species=species)
    eti_util.rich_display(summary)


@main.command(**_click_command_opts)
@_installed
@_species
@_outdir
@_limit
def dump_genes(
    installed: pathlib.Path,
    species: str,
    outdir: pathlib.Path,
    limit: int,
) -> None:
    """export meta-data table for genes from one species to <species>-<release>.gene_metadata.tsv"""

    config = eti_config.read_installed_cfg(installed)
    if species is None:
        eti_util.print_colour(text="ERROR: a species name is required", colour="red")
        sys.exit(1)

    if len(species) > 1:
        eti_util.print_colour(
            text=f"ERROR: one species at a time, not {species!r}",
            colour="red",
        )
        sys.exit(1)

    annot_db = eti_genome.load_annotations_for_species(
        path=config.installed_genome(species=species[0]),
    )
    path = annot_db.source
    table = eti_genome.get_gene_table_for_species(annot_db=annot_db, limit=limit)
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"{path.stem}-{config.release}-gene_metadata.tsv"
    table.write(outpath)
    eti_util.print_colour(text=f"Finished: wrote {str(outpath)!r}!", colour="green")


@main.command(**_click_command_opts)
@_installed
def compara_summary(installed: pathlib.Path) -> None:
    """summary data for compara"""

    config = eti_config.read_installed_cfg(installed)
    if config.homologies_path.exists():
        db = eti_homology.load_homology_db(
            path=config.homologies_path,
        )
        table = db.count_distinct(homology_type=True)
        table.title = "Homology types"
        table.format_column("count", lambda x: f"{x:,}")
        eti_util.rich_display(table)


@main.command(**_click_command_opts)
@_installed
@_outdir
@click.option(
    "-ht",
    "--homology_type",
    type=str,
    default="ortholog_one2one",
    help="type of homology",
)
@_ref
@_coord_names
@_nprocs
@_limit
@_force
@_verbose
def homologs(
    installed: pathlib.Path,
    outdir: pathlib.Path,
    homology_type: str,
    ref: str,
    coord_names: str,
    num_procs: int,
    limit: int,
    force_overwrite: bool,
    verbose: bool,
) -> None:
    """exports CDS sequence data in fasta format for homology type relationship"""
    from rich import progress

    LOGGER = CachingLogger()
    LOGGER.log_args()

    if ref is None:
        eti_util.print_colour(
            text="ERROR: a reference species name is required, use --ref",
            colour="red",
        )
        sys.exit(1)

    if force_overwrite:
        shutil.rmtree(outdir, ignore_errors=True)

    outdir.mkdir(parents=True, exist_ok=True)

    LOGGER.log_file_path = outdir / f"homologs-{ref}-{homology_type}.log"

    config = eti_config.read_installed_cfg(installed)
    eti_species.Species.update_from_file(config.genomes_path / "species.tsv")
    # we all the protein coding gene IDs from the reference species
    genome = eti_genome.load_genome(config=config, species=ref)

    if verbose:
        eti_util.print_colour(text=f"Loaded genome for {ref!r}", colour="yellow")

    # we don't use the limit argument for this query since we want the limit
    # to be the number of homology matches
    gene_ids = list(
        genome.get_ids_for_biotype(
            biotype="protein_coding",
            seqid=coord_names,
        ),
    )

    if verbose:
        eti_util.print_colour(
            text=f"Found {len(gene_ids):,} gene IDs for {ref!r}",
            colour="yellow",
        )

    db = eti_homology.load_homology_db(
        path=config.homologies_path,
    )
    related = []
    with progress.Progress(
        progress.TextColumn("[progress.description]{task.description}"),
        progress.BarColumn(),
        progress.TaskProgressColumn(),
        progress.TimeRemainingColumn(),
        progress.TimeElapsedColumn(),
    ) as progress:
        searching = progress.add_task(
            total=limit or len(gene_ids),
            description="Homolog search",
        )
        for gid in gene_ids:
            if rel := db.get_related_to(gene_id=gid, relationship_type=homology_type):
                related.append(rel)
                progress.update(searching, advance=1)

            if limit and len(related) >= limit:
                break

        progress.update(searching, advance=len(gene_ids))

        if verbose:
            eti_util.print_colour(
                text=f"Found {len(related)} homolog groups",
                colour="yellow",
            )

        get_seqs = eti_homology.collect_seqs(config=config)
        out_dstore = open_data_store(base_path=outdir, suffix="fa", mode="w")

        reading = progress.add_task(total=len(related), description="Extracting  🧬")
        for seqs in get_seqs.as_completed(
            related,
            parallel=num_procs > 1,
            show_progress=False,
            par_kw={"max_workers": num_procs},
        ):
            progress.update(reading, advance=1)
            if not seqs:
                if verbose:
                    eti_util.print_colour(text=f"{seqs=}", colour="yellow")

                out_dstore.write_not_completed(
                    data=seqs.to_json(),
                    unique_id=seqs.source,
                )
                continue
            if not seqs.seqs:
                if verbose:
                    eti_util.print_colour(text=f"{seqs.seqs=}", colour="yellow")
                continue

            txt = seqs.to_fasta()
            out_dstore.write(data=txt, unique_id=seqs.info.source)

    log_file_path = pathlib.Path(LOGGER.log_file_path)
    LOGGER.shutdown()
    out_dstore.write_log(unique_id=log_file_path.name, data=log_file_path.read_text())
    log_file_path.unlink()


@main.command(**_click_command_opts)
@_installed
@_outdir
@_align_name
@_ref
@_coord_names
@_ref_genes_file
@_mask
@_mask_shadow
@_mask_ref
@_limit
@_force
@_verbose
def alignments(
    installed: pathlib.Path,
    outdir: pathlib.Path,
    align_name: str,
    ref: str,
    coord_names: str,
    ref_genes_file: pathlib.Path,
    mask: pathlib.Path,
    mask_shadow: pathlib.Path,
    mask_ref: bool,
    limit: int,
    force_overwrite: bool,
    verbose: bool,
) -> None:
    """export multiple alignments in fasta format for named genes"""
    from cogent3 import load_table
    from rich import progress

    from ensembl_tui import _align as eti_align

    if mask and mask_shadow:
        eti_util.print_colour(
            text="ERROR: cannot specify both mask and mask_shadow",
            colour="red",
        )
        sys.exit(1)

    # TODO support genomic coordinates, e.g. coord_name:start-stop, for
    #  a reference species

    if not ref:
        eti_util.print_colour(
            text="ERROR: must specify a reference genome",
            colour="red",
        )
        sys.exit(1)

    if force_overwrite:
        shutil.rmtree(outdir, ignore_errors=True)

    config = eti_config.read_installed_cfg(installed)
    align_name = eti_util.strip_quotes(align_name)
    align_path = config.path_to_alignment(align_name, eti_align.ALIGN_STORE_SUFFIX)
    if align_path is None:
        eti_util.print_colour(
            text=f"{align_name!r} does not match any alignments under '{config.aligns_path}'",
            colour="red",
        )
        available = "\n".join(
            [
                fn.stem
                for fn in config.aligns_path.glob("*")
                if not fn.name.startswith(".") and fn.is_dir()
            ],
        )
        eti_util.print_colour(text=f"Available alignments:\n{available}", colour="red")
        sys.exit(1)

    align_db = eti_align.AlignDb(source=align_path)
    ref_species = eti_species.Species.get_ensembl_db_prefix(ref)
    if ref_species not in align_db.get_species_names():
        eti_util.print_colour(
            text=f"species {ref!r} not in the alignment",
            colour="red",
        )
        sys.exit(1)

    # get all the genomes
    if verbose:
        eti_util.print_colour(
            text=f"working on species {align_db.get_species_names()}",
            colour="yellow",
        )

    genomes = {
        sp: eti_genome.load_genome(config=config, species=sp)
        for sp in align_db.get_species_names()
    }

    # load the gene stable ID's
    if ref_genes_file:
        table = load_table(ref_genes_file)
        if "stableid" not in table.columns:
            eti_util.print_colour(
                text=f"'stableid' column missing from {str(ref_genes_file)!r}",
                colour="red",
            )
            sys.exit(1)
        stableids = table.columns["stableid"]
    elif coord_names:
        genome = genomes[ref_species]
        stableids = list(
            genome.get_ids_for_biotype(
                biotype="protein_coding",
                seqid=coord_names,
                limit=limit,
            ),
        )
    else:
        stableids = None

    locations = eti_genome.get_gene_segments(
        annot_db=genomes[ref_species].annotation_db,
        species=ref_species,
        limit=limit,
        stableids=stableids,
    )

    mask = mask_shadow or mask
    shadow = bool(mask_shadow)
    maker = eti_align.construct_alignment(
        align_db=align_db,
        genomes=genomes,
        mask_features=mask,
        shadow=shadow,
        mask_ref=mask_ref,
    )
    output = open_data_store(outdir, mode="w", suffix="fa")
    writer = get_app("write_seqs", format="fasta", data_store=output)
    with (
        eti_util.keep_running(),
        progress.Progress(
            progress.TextColumn("[progress.description]{task.description}"),
            progress.BarColumn(),
            progress.TaskProgressColumn(),
            progress.TimeRemainingColumn(),
            progress.TimeElapsedColumn(),
        ) as progress,
    ):
        task = progress.add_task(
            total=limit or len(locations),
            description="Getting alignment data",
        )
        for alignments in maker.as_completed(locations, show_progress=False):
            progress.update(task, advance=1)
            if not alignments:
                eti_util.print_colour(str(alignments), colour="red")
                continue
            input_source = alignments[0].info.source
            if len(alignments) == 1:
                writer(alignments[0], identifier=input_source)
                continue

            for i, aln in enumerate(alignments):
                identifier = f"{input_source}-{i}"
                writer(aln, identifier=identifier)

    eti_util.print_colour(text="Done!", colour="green")


if __name__ == "__main__":
    main()
