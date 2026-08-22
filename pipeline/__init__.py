"""Reference implementations of the pipeline's algorithm families.

Modules correspond one-to-one to the paper's Methods subsections:
  qc_stream          - 2.2 sensor-stream quality control (Hampel filter)
  features           - 2.3 spectral indices and predictor stack
  sentinel2_prep     - 2.3 Sentinel-2 cloud masking and compositing
  train_blocked      - 2.4 spatially blocked cross-validation
  tune_shap          - 2.4 hyperparameter search and SHAP attribution
  ahp                - 2.5 AHP weighting with consistency guard
  kriging            - 2.6 ordinary kriging with variance surface
  irrigation_fao56   - 2.7 FAO-56 soil-water balance
"""
