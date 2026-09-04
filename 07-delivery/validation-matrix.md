# Validation matrix

> Where each kind of raw material lands, where its validated content goes,
> and what "validated" requires. This is the routing table of the pipeline.

| Source type | Landing zone | Canonical targets | Validation expectation |
|---|---|---|---|
| Meeting transcript | `01-meetings/transcripts/` | `06-decisions/`, `05-requirements/`, `03-work/`, `07-delivery/` | Promote only after review, via minutes |
| Meeting minutes | `01-meetings/minutes/` | Same as above | May summarize; must cite the transcript |
| Email / notes / brain-dumps | `99-inbox/` | Depends on topic | Evidence until validated |
| Vendor documentation | `09-references/vendor-docs/` | `03-work/`, `04-architecture/`, `08-vendors/` | Cite the exact document; vendor claims start PENDING VALIDATION |
| Contract / commercial doc | `09-references/contracts/` | `06-decisions/`, `08-vendors/`, `07-delivery/` | Capture only necessary non-sensitive facts; record conflicts in the source register |
| System observation | `09-references/` or work-unit folder | `03-work/<wu>/current-state.md` | Dated, method stated ("read-only navigation"), a visible screen implies no acceptance |
