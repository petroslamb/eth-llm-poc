# Proposal Summary PDF

Generate the PDF from the markdown using pandoc with the tectonic engine:

```sh
pandoc docs/proposal/summary/PROPOSAL_SUMMARY.md \
  -o docs/proposal/summary/PROPOSAL_SUMMARY.pdf \
  --pdf-engine=tectonic
```
