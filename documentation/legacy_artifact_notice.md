# Legacy synthetic dashboard notice

The `dashboard/` git-linked directory was created before the current no-synthetic-data research protocol. It contains explicitly simulated PMS values and is outside the scope of this study.

Safeguards:

- none of the analysis scripts read from `dashboard/`;
- the validated outcome path is fixed to `raw_data/pms_outcome.csv`;
- the outcome validator rejects synthetic, simulated, mock, dummy, or fabricated provenance; and
- the new `website/` reports the data gap rather than displaying synthetic outcomes.
