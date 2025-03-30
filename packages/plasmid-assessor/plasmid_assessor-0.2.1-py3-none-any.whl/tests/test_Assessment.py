import Bio.Restriction
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import plasmid_assessor as plasma


def test_assess_seq():
    # Also tests digest_seq()
    record = SeqRecord(
        Seq("AAAAACGTCTCAACTG" + "AAAAA" + "TATCAGAGACGAAAAA"),
        annotations={"topology": "circular"},
    )
    design = plasma.Assessment(record, "BsmBI")
    design.assess_seq()
    assert design.results["digest"]["left_overhang"] == "ACTG"
    assert design.results["digest"]["right_overhang"] == "TATC"


def test_get_number_of_sites():
    sequence = SeqRecord(
        Seq("ATCGATCG"), annotations={"topology": "circular"}
    )  # 0 site
    design = plasma.Assessment(sequence, "BsmBI")
    design.get_number_of_sites()
    assert design.results["number_of_sites"] == 0

    sequence = SeqRecord(
        Seq("AAAAACGTCTCAACTGAAAAAATATCAGAGACGAAAAA"),
        annotations={"topology": "circular"},
    )  # 2 sites
    design = plasma.Assessment(sequence, "BsmBI")
    design.get_number_of_sites()
    assert design.results["number_of_sites"] == 2


def test_evaluate_orientation():
    sequence = SeqRecord(
        Seq("AAAA" + "CGTCTCAACTG" + "AAAAA" + "TATCAGAGACG" + "AAAA"),
        annotations={"topology": "circular"},
    )
    design = plasma.Assessment(sequence, "BsmBI")
    design.evaluate_orientation()
    assert design.results["is_site_orientation_correct"]


def test_count_other_sites():
    sequence = SeqRecord(
        Seq("CGTCTCAACTG" + "AAA" + "TATCAGAGACG" + "AGGTCTC"),
        annotations={"topology": "circular"},
    )
    design = plasma.Assessment(sequence, "BsmBI")
    design.count_other_sites(other_enzymes=["BsaI"])
    assert design.results["other_sites"]["has_any_other_sites"]
    assert len(design.results["other_sites"]["enzyme"][Bio.Restriction.BsaI]) == 1


def test_linear_seq():
    record = SeqRecord(
        Seq("AAAAA" + "CGTCTCAACTG" + "AAAAA" + "TATCAGAGACG" + "AAAAA"),
        annotations={"topology": "linear"},
    )
    design = plasma.Assessment(record, "BsmBI")
    design.assess_seq()


def test_circular_seq():
    # The retained insert (part) is one continuous sequence
    record = SeqRecord(
        Seq("AAAAA" + "CGTCTCAACTG" + "AAAAA" + "TATCAGAGACG" + "AAAAA"),
        annotations={"topology": "circular"},
    )
    design = plasma.Assessment(record, "BsmBI")
    design.assess_seq()


def test_circular_seq_origin_in_insert():
    # In this version, the retained insert is split to the start and end of the seq
    record = SeqRecord(
        Seq("AAAAA" + "TATCAGAGACG" + "AAAAA" + "CGTCTCAACTG" + "AAAAA"),
        annotations={"topology": "circular"},
    )
    design = plasma.Assessment(record, "BsmBI")
    design.assess_seq()


def test_plot_sequence():
    sequence = SeqRecord(
        Seq("CGTCTCAACTG" + "AAA" + "TATCAGAGACG" + "AGGTCTC"),
        annotations={"topology": "circular"},
    )
    design = plasma.Assessment(sequence, "BsmBI")
    design.plot_sequence()
    assert design.fig
