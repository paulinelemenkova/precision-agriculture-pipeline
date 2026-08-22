# Figure index

Mapping between the scripts in this repository, the image files they produce,
and the figure numbers in the manuscript (Acta agriculturae Slovenica version).

## Figures in the paper

| Paper | Script | Output file | Type |
|------|--------|-------------|------|
| Figure 1 | `figures/plot_architecture.py` | `fig02_architecture.png/pdf` | Matplotlib diagram |
| Figure 2 | `figures/plot_iwsn_topology.py` | `fig08_iwsn_node_topology.png/pdf` | Matplotlib diagram |
| Figure 3 | `figures/maps/plot_study_area_gmt.sh` | `fig01_study_area.*` | GMT map |
| Figure 4 | `figures/maps/plot_thematic_grid_gmt.sh` | `fig06_thematic_grid.*` | GMT map (4 provinces x 4 layers) |
| Figure 5 | `figures/plot_uniform_vs_sitespecific.py` | `fig10_uniform_vs_sitespecific.png/pdf` | Matplotlib figure |
| Figure 6 | `figures/plot_predictor_importance.py` | `fig09_predictor_importance.png/pdf` | Matplotlib figure (SHAP) |

The two Matplotlib diagrams (Figures 1-2) and the two synthetic figures
(Figures 5-6) are fully self-contained: they need only `numpy` and
`matplotlib` and write PNG + PDF into the working directory.

## Additional figures (`figures/extra/`)

These scripts belong to the wider study but their figures are not included in
the condensed journal version. They are provided for completeness.

| Script | Output |
|--------|--------|
| `plot_gis_database.py` | GIS database schematic |
| `plot_ai_workflow.py` | Learning-pipeline workflow |
| `plot_gis_workflow.py` | Geospatial-branch workflow |
| `plot_agri_regions.py` | Agricultural-area map (needs GeoPandas + source vectors) |
| `plot_future_ecosystem.py` | Future-ecosystem concept diagram |
