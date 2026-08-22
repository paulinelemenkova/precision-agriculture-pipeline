# Reproducible spatial decision-support pipeline for precision agriculture

Code and reproducible figures for the manuscript:

> **Coupling Ensemble Learning, Multi-Criteria Weighting, and Geostatistical
> Interpolation: A Reproducible Spatial Decision-Support Pipeline for Precision
> Agriculture.** Polina Lemenkova and Abdullah Can Zülfikar. *Acta agriculturae
> Slovenica* (under review, 2026).

The paper specifies an integrated pipeline that couples five algorithm families
in one six-layer architecture: robust quality control of wireless-sensor
telemetry, ensemble and deep-learning prediction under **spatially blocked**
cross-validation, **Analytic Hierarchy Process (AHP)** weighting with a
consistency guard, **ordinary kriging** with an explicit variance surface, and a
**FAO-56** soil-water balance, with **SHAP** attribution throughout. This
repository holds the reference implementations of those methods and the scripts
that generate every figure in the article.

The study is a methodological *blueprint*: it is exercised on four climatically
contrasting Turkish provinces (Antalya, İzmir, Konya, Rize) using open-access
data. There is no primary field dataset; the pipeline modules are documented,
runnable building blocks rather than a trained model release.

## Repository layout

```
.
├── pipeline/                 Reference implementations of the paper's methods
│   ├── qc_stream.py            2.2  Hampel quality control of IWSN telemetry
│   ├── features.py             2.3  Spectral indices + multi-source stack
│   ├── sentinel2_prep.py       2.3  Sentinel-2 cloud masking + compositing
│   ├── train_blocked.py        2.4  Spatially blocked cross-validation
│   ├── tune_shap.py            2.4  Randomized search + SHAP attribution
│   ├── ahp.py                  2.5  AHP weighting + weighted overlay
│   ├── kriging.py              2.6  Ordinary kriging + variance surface
│   └── irrigation_fao56.py     2.7  FAO-56 soil-water balance + map
├── figures/                  Scripts that reproduce the paper's figures
│   ├── plot_architecture.py            Figure 1
│   ├── plot_iwsn_topology.py           Figure 2
│   ├── plot_uniform_vs_sitespecific.py Figure 5
│   ├── plot_predictor_importance.py    Figure 6
│   ├── maps/                            GMT map scripts + bundled grids
│   │   ├── plot_study_area_gmt.sh       Figure 3
│   │   ├── plot_thematic_grid_gmt.sh    Figure 4
│   │   ├── *.cpt, *.gmt, *.nc, *.grd    palettes, province polygons, grids
│   │   └── centres.txt
│   └── extra/                           Figures from the wider study (not in paper)
├── examples/
│   └── demo_ahp_fao56.py     Dependency-light demo (numpy + pandas only)
├── docs/
│   └── figure_index.md       Script → output → paper-figure mapping
├── requirements.txt          pip dependencies (Python bindings)
├── environment.yml           conda environment (incl. GMT C library + GDAL)
├── CITATION.cff
└── LICENSE                   MIT (code)
```

## Installation

The Matplotlib figures and most pipeline modules need only the Python
scientific stack. The **map scripts** (`figures/maps/`) and `pygmt` additionally
require the **GMT** C library and **GDAL**, which are easiest to obtain with
conda.

**Option A — conda (recommended, full reproducibility):**

```bash
conda env create -f environment.yml
conda activate precision-ag
```

**Option B — pip (Python parts only):**

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# For the .sh map scripts you must also install GMT >= 6.4 and GDAL yourself.
```

## Reproducing the figures

Self-contained figures (no external data, write PNG + PDF to the current folder):

```bash
cd figures
python plot_architecture.py             # Figure 1
python plot_iwsn_topology.py            # Figure 2
python plot_uniform_vs_sitespecific.py  # Figure 5
python plot_predictor_importance.py     # Figure 6
```

Map figures (GMT):

```bash
cd figures/maps
bash plot_study_area_gmt.sh      # Figure 3
bash plot_thematic_grid_gmt.sh   # Figure 4
```

The map scripts read the bundled per-province grids (`ndvi_*.nc`, `lst_*.nc`,
`dem*.grd`), province polygons (`*.gmt`) and colour palettes (`*.cpt`) that ship
in this folder. The NDVI, land-surface-temperature and elevation panels render
directly from those. The **land-cover** column and the shaded relief are built
from the full open-access source rasters; point the pipeline at them by setting

```bash
export DATA_DIR=/path/to/your/data
```

and placing the sources listed below under that folder. Without the sources the
scripts skip the source-dependent panels and still render the rest.

## Data sources (open access)

| Dataset | Source |
|---------|--------|
| Sentinel-2 | ESA Copernicus Data Space — https://dataspace.copernicus.eu |
| Landsat 8–9 | USGS EarthExplorer — https://earthexplorer.usgs.gov |
| Digital elevation / relief | GEBCO 2024 — https://www.gebco.net ; SRTM/ASTER via NASA Earthdata |
| Soil | ISRIC SoilGrids — https://soilgrids.org |
| Land cover (10 m) | CORINE Land Cover Plus, Copernicus Land Monitoring Service |
| Land-surface temperature (1 km) | MODIS MOD11A2, NASA LP DAAC |
| Vegetation index (NDVI, 1 km) | eVIIRS Global NDVI, U.S. Geological Survey |
| Administrative boundaries | geoBoundaries ADM1 (CC-BY 4.0) — https://www.geoboundaries.org |
| Meteorology | Turkish State Meteorological Service — https://www.mgm.gov.tr |

## Quick demo

```bash
python examples/demo_ahp_fao56.py
```

Runs the AHP consistency-checked weighting and the FAO-56 scheduler on synthetic
inputs, using only `numpy` and `pandas`.

## Citing

Please cite the article and this repository; see `CITATION.cff`. Update the
volume, pages and DOI once the article is published.

## License

Code is released under the MIT License (`LICENSE`). The manuscript text and
figures are distributed by the journal under CC BY 4.0.

## Acknowledgements

Supported by the Scientific and Technological Research Council of Türkiye
(TÜBİTAK), BIDEB Science Fellowships and Grant Programmes (grant 2221).
