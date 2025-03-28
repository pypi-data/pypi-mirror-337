import os
import shutil

import cogent3
import pytest
from click.testing import CliRunner

from ensembl_tui import _config as eti_config
from ensembl_tui import cli as eti_cli

RUNNER = CliRunner()


@pytest.mark.slow
@pytest.mark.internet
@pytest.mark.timeout(120)
def test_download(tmp_config):
    """runs download, install, drop according to a special test cfg"""
    tmp_dir = tmp_config.parent
    # now download

    r = RUNNER.invoke(eti_cli.download, [f"-c{tmp_config}"], catch_exceptions=False)
    assert r.exit_code == 0, r.output
    # make sure the download checkpoint file exists
    genome_dir = tmp_dir / "staging" / "genomes"
    dirnames = [dn for dn in os.listdir(genome_dir) if (genome_dir / dn).is_dir()]
    assert "saccharomyces_cerevisiae" in dirnames

    # make sure file sizes > 0
    paths = list((genome_dir / "saccharomyces_cerevisiae").glob("*"))
    size = sum(p.stat().st_size for p in paths)
    assert size > 0

    assert r.exit_code == 0, r.output


def test_download_no_config():
    r = RUNNER.invoke(eti_cli.download, ["-d"], catch_exceptions=False)
    assert r.exit_code != 0, r.output
    assert "No config" in r.output


def test_exportrc(tmp_dir):
    """exportrc works correctly"""
    outdir = tmp_dir / "exported"
    r = RUNNER.invoke(eti_cli.exportrc, [f"-o{outdir}"])
    assert r.exit_code == 0, r.output
    fnames = os.listdir(outdir)
    assert "species.tsv" in fnames
    assert len(fnames) == 2
    shutil.rmtree(tmp_dir)


@pytest.fixture(scope="module")
def installed(tmp_downloaded):
    # tmp_downloaded is a temp copy of the download folder
    # we add the verbose and force_overwrite flags to exercise
    # those conditional statements
    r = RUNNER.invoke(
        eti_cli.install,
        [f"-d{tmp_downloaded}", "-v", "-f"],
        catch_exceptions=False,
    )
    assert r.exit_code == 0, r.output
    return tmp_downloaded.parent / "install"


@pytest.mark.slow
def test_installed(installed):
    config = eti_config.read_installed_cfg(installed)
    assert config.homologies_path.exists()
    assert sum(f.stat().st_size for f in config.homologies_path.iterdir()) > 8_000
    r = RUNNER.invoke(eti_cli.installed, [f"-i{installed}"], catch_exceptions=False)
    assert r.exit_code == 0, r.output
    assert "Installed genomes" in r.output
    assert "caenorhabditis_elegans" in r.output
    path = config.installed_genome("caenorhabditis_elegans")
    # should be 2 combined attr parquet files
    assert len(list(path.glob("*attr.parquet"))) == 2


@pytest.mark.slow
def test_check_one_cds_seq(installed):
    # checking a single exon sequence with a rel_start > 0
    from ensembl_tui import _genome as eti_genome

    config = eti_config.read_installed_cfg(installed)
    genome = eti_genome.load_genome(
        config=config,
        species="saccharomyces_cerevisiae",
    )
    cds = next(iter(genome.get_cds(stable_id="YMR242C")))
    seq = cds.get_slice()
    expect = (
        "GCTCACTTTAAAGAATACCAAGTTATTGGCCGTCGTTTGCCAACTGAATCTGTTCCAGAA"
        "CCAAAGTTGTTCAGAATGAGAATCTTTGCTTCAAATGAAGTTATTGCCAAGTCTCGTTAC"
        "TGGTATTTCTTGCAAAAGTTGCACAAGGTTAAGAAGGCTTCTGGTGAAATTGTTTCCATC"
        "AACCAAATCAACGAAGCTCATCCAACCAAGGTCAAGAACTTCGGTGTCTGGGTTAGATAC"
        "GACTCCAGATCTGGTACTCACAATATGTACAAGGAAATCAGAGACGTCTCCAGAGTTGCT"
        "GCCGTCGAAACCTTATACCAAGACATGGCTGCCAGACACAGAGCTAGATTTAGATCTATT"
        "CACATCTTGAAGGTTGCTGAAATTGAAAAGACTGCTGACGTCAAGAGACAATACGTTAAG"
        "CAATTTTTGACCAAGGACTTGAAATTCCCATTGCCTCACAGAGTCCAAAAATCCACCAAG"
        "ACTTTCTCCTACAAGAGACCTTCCACTTTCTACTGA"
    )
    assert str(seq) == expect


@pytest.mark.slow
def test_check_multi_exon_cds_seq_plus_strand(installed):
    # checking a multi exon sequence with a rel_start > 0
    # and rel_end != exon length
    from ensembl_tui import _genome as eti_genome

    config = eti_config.read_installed_cfg(installed)
    genome = eti_genome.load_genome(
        config=config,
        species="caenorhabditis_elegans",
    )
    cds = next(iter(genome.get_cds(stable_id="WBGene00185002")))
    aa = str(cds.get_slice().get_translation())
    # seq expected values from ensembl
    assert aa.startswith("MEMEDIDDDITVFYTDDRGTVQGPYGASTVLDWYQKGYFSDNHQMRFTDNGQRIGNLFTY")
    assert aa.endswith("IEKVKTNCRDAPSPLPPAMDPVAPYHVRDKCTQS")
    assert len(aa) == 274


@pytest.mark.slow
def test_check_two_exon_cds_seq_rev_strand(installed):
    # checking a two exon sequence with a rel_start > 0
    # and rel_end != exon length
    from ensembl_tui import _genome as eti_genome

    config = eti_config.read_installed_cfg(installed)
    genome = eti_genome.load_genome(
        config=config,
        species="caenorhabditis_elegans",
    )
    cds = next(iter(genome.get_cds(stable_id="WBGene00184990")))
    aa = str(cds.get_slice().get_translation())
    # seq expected values from ensembl
    assert aa.startswith("MSGVYNNSGSRMRSKNFEKHQVPSDMAFFQKFRKQSHSNETVDCKKKQEE")
    assert aa.endswith("DGHYSDETVEEKHNREHRNKTKADNRTRRIAEIRRKHNINA")
    assert len(aa) == 161


@pytest.mark.slow
def test_species_summary(installed):
    r = RUNNER.invoke(
        eti_cli.species_summary,
        [f"-i{installed}", "--species", "caenorhabditis_elegans"],
        catch_exceptions=False,
    )
    assert r.exit_code == 0, r.output
    assert "Caenorhabditis elegans" in r.output
    assert "protein_coding" in r.output


@pytest.mark.slow
def test_dump_genes(installed):
    species = "caenorhabditis_elegans"
    outdir = installed.parent
    args = [
        f"-i{installed}",
        "--species",
        species,
        "--outdir",
        str(outdir),
        "--limit",
        "10",
    ]
    r = RUNNER.invoke(
        eti_cli.dump_genes,
        args,
        catch_exceptions=False,
    )
    assert r.exit_code == 0, r.output
    tsv_path = next(iter(outdir.glob("*.tsv")))
    assert tsv_path.name.startswith(species)
    table = cogent3.load_table(tsv_path)
    assert table.shape[0] == 10


@pytest.mark.slow
def test_homologs(installed, tmp_dir):
    outdir = tmp_dir / "output"
    limit = 10
    args = [
        f"-i{installed}",
        "--ref",
        "caenorhabditis_elegans",
        "--outdir",
        f"{outdir}",
        "--limit",
        str(limit),
        "-ht",
        "ortholog_one2one",
        "-v",
    ]

    r = RUNNER.invoke(
        eti_cli.homologs,
        args,
        catch_exceptions=False,
    )
    assert r.exit_code == 0, r.output
    dstore = cogent3.open_data_store(outdir, suffix="fa", mode="r")
    assert len(dstore.completed) == limit


@pytest.mark.slow
def test_homologs_coord_name(installed, tmp_dir):
    outdir = tmp_dir / "output"
    limit = 10
    args = [
        f"-i{installed}",
        "--ref",
        "saccharomyces_cerevisiae",
        "--outdir",
        f"{outdir}",
        "--limit",
        str(limit),
        "--coord_names",
        "I,XVI,II",
        "-ht",
        "ortholog_one2one",
        "-v",
    ]

    r = RUNNER.invoke(
        eti_cli.homologs,
        args,
        catch_exceptions=False,
    )
    assert r.exit_code == 0, r.output
    dstore = cogent3.open_data_store(outdir, suffix="fa", mode="r")
    assert len(dstore.completed) == limit


@pytest.mark.slow
def test_compara_summary(installed):
    r = RUNNER.invoke(
        eti_cli.compara_summary,
        [f"-i{installed}"],
        catch_exceptions=False,
    )
    assert r.exit_code == 0, r.output
    assert "homology_type" in r.output
    assert "ortholog_one2many" in r.output
