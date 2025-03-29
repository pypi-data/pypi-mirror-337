# Overview

G-Confid is Statistics Canada’s Disclosure Avoidance software. It consists of 4 main modules:

- **Sensitivity**, which aggregates micro data into table cells then calculates the sensitivity of the cells as well as the combination of cells.
- **Suppression**, which identifies cells to be suppressed in a table, in addition to the sensitive cells, to prevent confidential data disclosure. This is referred to as a suppression pattern.
- **Auditing**, which verifies the validity of a suppression pattern primarily used when adjustments are made to the recommended pattern.
- **Optimized Rounding**, which rounds multi-dimensional tables, creating uncertainty while providing a solution that is as close to the given table as possible that respects the provided constraints.
