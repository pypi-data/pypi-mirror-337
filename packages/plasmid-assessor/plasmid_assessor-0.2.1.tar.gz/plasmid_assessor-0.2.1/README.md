<p align="center">
<img alt="Plasma logo" title="Plasma" src="images/plasma_logo.png" width="120">
</p>

# Plasmid assessor

[![build](https://github.com/Edinburgh-Genome-Foundry/Plasmid_assessor/actions/workflows/build.yml/badge.svg)](https://github.com/Edinburgh-Genome-Foundry/Plasmid_assessor/actions/workflows/build.yml)
[![coverage](https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/Plasmid_assessor/badge.svg?branch=main)](https://coveralls.io/github/Edinburgh-Genome-Foundry/Plasmid_assessor?branch=main)

Plasmid and linear DNA part assessment for Golden Gate cloning. An important task in DNA assembly is creating or adapting a plasmid to serve as a backbone (receiver vector) for the assembled parts. This package provides tools for quickly checking a a plasmid (or other DNA) sequence file for this purpose.

Most important properties of a backbone are:

* two sites for the chosen restriction enzyme, flanking the insert segment
* no other sites for the restriction enzyme

The choice of the two backbone overhangs are also important, because they will be involved in all assemblies using that design or standard. Additionally, we can add selection for proper assembly (for example, by including a ccdB suicide cassette at the insertion location) and for presence of plasmid in the bacterium (psk), for example, by using antibiotic resistance. Finally, we can check that the replicon (ori) and the partitioning system in the plasmid suits the strain, compatibility and other requirements.

## Install

```bash
pip install plasmid_assessor
# pip install plasmid_assessor[report]  # install with dependencies for pdf reports
```

## Usage

```python
import plasmid_assessor as plasma

# Load your Genbank or FASTA file as a Biopython SeqRecord, or create a new one:
from Bio import SeqIO
sequence = SeqIO.read("HC_Amp_ccdB.gb", "genbank")
# Check that topology is set correctly ("circular" or "linear"):
sequence.annotations["topology"]
sequence.id = "HC_Amp_ccdB"  # specify a name for the part

# Evaluate plasmid:
design = plasma.Assessment(sequence, "BsmBI")
design.assess_seq(other_enzymes=["BsaI"])  # also check for the enzyme(s) of the 2nd (3rd..) level assembly
# Results are stored in:
design.results
# Save as a PDF report:
plasma.write_pdf_report("report.pdf", design)
```

Plasmid assessor checks the properties listed above, and if the plamid passes, then it gets a green ☑ symbol; if there are errors, it's flagged with a red ☒ symbol. Warning comments are marked with a yellow ⚠ sign.

<p align="center">
<img alt="Plasma report" title="Plasma report" src="images/plasma_report_screenshot.png" width="450">
</p>

For plasmid backbone parts, check that they contain the following functional elements:
  
    ☐ origin of replication (ori)
    ☐ selection for proper assembly and against intact backbone (e.g. ccdB in excised region)
    ☐ selection for presence of plasmid in the bacterium (psk, e.g. AmpR)

## Future improvements

Currently the package handles sequences with only one (retained) part per DNA molecule.

## Versioning

Plasmid assessor uses the [semantic versioning](https://semver.org) scheme.

## License = MIT

Plasmid assessor is free/libre and open-source software, which means the users have the freedom to run, study, change and distribute the software.

Plasmid assessor was written at the [Edinburgh Genome Foundry](https://edinburgh-genome-foundry.github.io/)
by [Peter Vegh](https://github.com/veghp).

Copyright 2021 Edinburgh Genome Foundry, University of Edinburgh
