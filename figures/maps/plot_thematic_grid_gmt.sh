#!/usr/bin/env bash
# =============================================================================
# fig06 - 4x4 thematic grid: Antalya, Izmir, Konya, Rize
#         columns = Land cover | NDVI | LST | Elevation
#
# THE ONLY THING THAT MATTERS FOR LAND COVER:
#   Use the CONDA pygmt gdalwarp. It streams the plain warp block-by-block and
#   builds the tiles fine. The homebrew gdalwarp gets OOM-killed ("Killed: 9")
#   on this machine. The script below points straight at the conda one, so it
#   works whether or not you `conda activate pygmt` first.
#
# RUN:  bash plot_thematic_grid_gmt.sh
# =============================================================================
rm -f gmt.history gmt.conf
export GMT_SESSION_NAME="fig06_$$"

# ---------------------------------------------------------------------------
# DATA_DIR: root folder holding the open-access source rasters/vectors.
# Override with:  export DATA_DIR=/path/to/your/data   (see README, Data sources)
DATA_DIR="${DATA_DIR:-$HOME/precision-ag-data}"
# ---------------------------------------------------------------------------


# ------------------------------------------------------------------ CONFIG --
PROV="${DATA_DIR}/geoBoundaries-TUR-ADM1.geojson"
NAMECOL="shapeName"
OUT="fig06_thematic_grid"

LC_TIF="${DATA_DIR}/CORINE_Land_Cover_Types/CLMS_CLCplus_RASTER_2018_010m_eu_03035_V1_1/Data/CLMS_CLCplus_RASTER_2018_010m_eu_03035_V1_1.tif"
NDVI_TIF="${DATA_DIR}/NDVI_VIIRS_2021/GN_eVSH_NDVI.2021.233-243.1KM.COMPRES.001.2023048053801/GN_eVSH_NDVI.2021.233-243.1KM.VI_NDVI.001.2023048013547.tif"
LST_TIF="${DATA_DIR}/MODIS_LST/clm_lst_mod11a2.aug.day_m_1km_s0..0cm_2000..2017_v1.0.tif"
DEM_SRC="${DATA_DIR}/GEBCO_2023.nc"

LST_MUL=0.02 ; LST_ADD=-273.15 ; LST_NODATA=-32767
NDVI_MUL=0.0001 ; NDVI_FILL=-1900 ; NDVI_BAND=1

# >>> LAND COVER warp runs INSIDE the pygmt conda env <<<
# Activating pygmt in a subshell gives gdalwarp its own correct PROJ/GDAL data,
# so there is no "another PROJ installation" clash and no OOM.
for c in "$HOME/anaconda3/etc/profile.d/conda.sh" \
         "$HOME/miniconda3/etc/profile.d/conda.sh" \
         "$HOME/opt/anaconda3/etc/profile.d/conda.sh" \
         "/opt/anaconda3/etc/profile.d/conda.sh"; do
  [ -f "$c" ] && source "$c" && break
done
warp () { ( conda activate pygmt 2>/dev/null && gdalwarp "$@" ); }

declare -a PN=("Antalya" "Izmir" "Konya" "Rize")
declare -a PF=("ant.gmt" "izm.gmt" "kon.gmt" "riz.gmt")
declare -a LCP=("lc_ant.tif" "lc_izm.tif" "lc_kon.tif" "lc_riz.tif")
declare -a LSP=("lst_ant.nc" "lst_izm.nc" "lst_kon.nc" "lst_riz.nc")
declare -a NVP=("ndvi_ant.nc" "ndvi_izm.nc" "ndvi_kon.nc" "ndvi_riz.nc")

for i in 0 1 2 3; do
  rm -f "${PF[$i]}"
  ogr2ogr -f OGR_GMT "${PF[$i]}" "$PROV" -where "\"${NAMECOL}\"='${PN[$i]}'" 2>/dev/null
done

winbox () {
  set -- $(gmt info "$1" -C)
  awk -v w=$1 -v e=$2 -v s=$3 -v n=$4 -v A=1.1364 -v m=0.08 'BEGIN{
    dlon=e-w; dlat=n-s; cx=(w+e)/2; cy=(s+n)/2;
    if (dlon/dlat < A) dlon=A*dlat; else dlat=dlon/A;
    dlon*=(1+m); dlat*=(1+m);
    printf "-R%.4f/%.4f/%.4f/%.4f\n", cx-dlon/2, cx+dlon/2, cy-dlat/2, cy+dlat/2;
  }'
}

# ------------------------------------------------------------------- CPTs ---
# CLC+ Backbone value -> colour (matches the 7-class legend). If your
# .tif.clr.txt uses other codes, edit these rows.
cat > clcplus.cpt <<'CPT'
0.5  230/0/77     1.5  230/0/77       ;1 Sealed
1.5  0/204/0      3.5  0/204/0        ;2-3 Woody (trees)
3.5  112/168/0    4.5  112/168/0      ;4 Shrubs
4.5  204/242/77   5.5  204/242/77     ;5 Herbaceous
5.5  255/230/128  6.5  255/230/128    ;6 Cropland
6.5  204/204/204  8.5  204/204/204    ;7-8 Bare/sparse
8.5  0/128/255    9.5  0/128/255      ;9 Water
9.5  230/242/255  10.5 230/242/255    ;10 Snow/ice
B white
F white
N 127
CPT
gmt makecpt -Cbamako -T0/0.9/0.05    -Z > ndvi.cpt
gmt makecpt -Cvik    -T10/50/2.5     -Z > lst.cpt
gmt makecpt -Cgeo    -T-500/3500/100 -Z > dem.cpt

JZ=-JX5.0cd/4.4cd

placeholder () {
  echo "$1" | sed 's/-R//' | awk -F/ '{printf "%s %s\n%s %s\n%s %s\n%s %s\n",$1,$3,$2,$3,$2,$4,$1,$4}' \
    | gmt plot $1 $JZ -Ggray95 -L
  printf "0.5 0.56 %s\n0.5 0.44 (no data yet)\n" "$2" \
    | gmt text -R0/1/0/1 -JX5.0c/4.4c -F+f8p,Helvetica-Oblique,gray45 -N
}

echo "land-cover warp : conda run -n pygmt gdalwarp"

# =============================================================================
# BUILD TILES  (only if missing)
# =============================================================================
for i in 0 1 2 3; do
  RZc=$(winbox "${PF[$i]}" | sed 's/-R//')
  W=$(echo $RZc|cut -d/ -f1); E=$(echo $RZc|cut -d/ -f2)
  S=$(echo $RZc|cut -d/ -f3); N=$(echo $RZc|cut -d/ -f4)

  # Land cover: plain streaming warp (NO -tr) inside the pygmt env
  if command -v conda >/dev/null 2>&1 && [ -f "$LC_TIF" ] && [ ! -f "${LCP[$i]}" ]; then
    warp -q -overwrite -t_srs EPSG:4326 -te $W $S $E $N \
      -r near -of GTiff -co COMPRESS=DEFLATE -co TILED=YES \
      "$LC_TIF" "${LCP[$i]}" || echo "  LC warp failed ${PN[$i]}"
  fi

  # LST: window read (memory-safe) -> degC
  if [ -f "$LST_TIF" ] && [ ! -f "${LSP[$i]}" ]; then
    if gdal_translate -q -projwin $W $N $E $S "$LST_TIF" "lst_tmp_$i.tif" 2>/dev/null; then
      gmt grdmath "lst_tmp_$i.tif" $LST_NODATA NAN $LST_MUL MUL $LST_ADD ADD = "${LSP[$i]}" 2>/dev/null
      rm -f "lst_tmp_$i.tif"
    fi
  fi

  # NDVI: window read (memory-safe) -> scale + mask fill
  if [ -f "$NDVI_TIF" ] && [ ! -f "${NVP[$i]}" ]; then
    if gdal_translate -q -b $NDVI_BAND -projwin $W $N $E $S "$NDVI_TIF" "ndvi_tmp_$i.tif" 2>/dev/null; then
      gmt grdmath "ndvi_tmp_$i.tif" $NDVI_MUL MUL \
                  "ndvi_tmp_$i.tif" $NDVI_FILL GT 0 NAN MUL = "${NVP[$i]}" 2>/dev/null
      rm -f "ndvi_tmp_$i.tif"
    fi
  fi
done

# =============================================================================
gmt begin ${OUT} png,pdf
  gmt set FONT_ANNOT_PRIMARY 6p,Helvetica FONT_TITLE 11p,Helvetica-Bold \
          FONT_HEADING=12p,Helvetica-Bold FONT_TAG 11p,Helvetica-Bold FONT_LABEL 8p \
          MAP_FRAME_TYPE plain PS_CHAR_ENCODING ISOLatin1+ \
          MAP_GRID_PEN_PRIMARY 0.2p,white MAP_FRAME_PEN 0.8p MAP_TICK_LENGTH_PRIMARY 2p

  gmt subplot begin 4x4 -Fs5.0c/4.4c -M0.85c/0.7c -A \
      -Bxa1f0.5 -Bya1f0.5 -BWSne \
      -T"Thematic layers for the four case-study provinces"

    for r in 0 1 2 3; do
      RZ=$(winbox "${PF[$r]}")
      CLAT=$(echo "$RZ" | sed 's/-R//' | awk -F/ '{printf "%.2f",($3+$4)/2}')
      if [ $r -eq 0 ]; then T1="+tNDVI"; T2="+tLST"; T3="+tElevation"; else T1=""; T2=""; T3=""; fi
      if [ $r -eq 3 ]; then SLEN=20k; else SLEN=50k; fi
      SB="-LjBR+w${SLEN}+u+o0.35c/0.45c+c${CLAT} -F+gwhite@30+p0.2p,gray40+r --FONT_ANNOT_PRIMARY=5p,Helvetica,black"

      # --- Land cover ---
      gmt subplot set $((r*4+0))
        if [ -f "${LCP[$r]}" ]; then gmt grdimage "${LCP[$r]}" $RZ $JZ -Cclcplus.cpt -nn
        else placeholder "$RZ" "Land cover"; fi
        gmt plot "${PF[$r]}" $RZ $JZ -W0.6p,black
        gmt basemap $RZ $JZ -Bxa1f0.5 -Bya1f0.5 "-BWSne+t${PN[$r]}" $SB
        if [ $r -eq 3 ]; then
          gmt legend -DJBC+w5.0c+o0/1.25c -F+p0.3p,gray50+gwhite --FONT_ANNOT_PRIMARY=5.5p <<'LCL'
N 2
S 0.10c s 0.15c 0/204/0     0.2p,gray40 0.20c Woody (trees)
S 0.10c s 0.15c 112/168/0   0.2p,gray40 0.20c Shrubs
S 0.10c s 0.15c 204/242/77  0.2p,gray40 0.20c Herbaceous
S 0.10c s 0.15c 255/230/128 0.2p,gray40 0.20c Cropland
S 0.10c s 0.15c 230/0/77    0.2p,gray40 0.20c Sealed
S 0.10c s 0.15c 204/204/204 0.2p,gray40 0.20c Bare/sparse
S 0.10c s 0.15c 0/128/255   0.2p,gray40 0.20c Water
LCL
        fi

      # --- NDVI ---
      gmt subplot set $((r*4+1))
        if [ -f "${NVP[$r]}" ]; then gmt grdimage "${NVP[$r]}" $RZ $JZ -Cndvi.cpt -Q
        else placeholder "$RZ" "NDVI"; fi
        gmt plot "${PF[$r]}" $RZ $JZ -W0.6p,black
        gmt basemap $RZ $JZ -Bxa1f0.5 -Bya1f0.5 "-BWSne${T1}" $SB
        if [ $r -eq 3 ]; then
          gmt colorbar -Cndvi.cpt -DJBC+w4.4c/0.20c+h+o0/1.25c -Bxa0.3+l"NDVI" \
              --FONT_ANNOT_PRIMARY=6p --FONT_LABEL=7p
        fi

      # --- LST ---
      gmt subplot set $((r*4+2))
        if [ -f "${LSP[$r]}" ]; then gmt grdimage "${LSP[$r]}" $RZ $JZ -Clst.cpt
        else placeholder "$RZ" "LST"; fi
        gmt plot "${PF[$r]}" $RZ $JZ -W0.6p,black
        gmt basemap $RZ $JZ -Bxa1f0.5 -Bya1f0.5 "-BWSne${T2}" $SB
        if [ $r -eq 3 ]; then
          gmt colorbar -Clst.cpt -DJBC+w4.4c/0.20c+h+o0/1.25c -Bxa10+l"LST (@~\260@~C)" \
              --FONT_ANNOT_PRIMARY=6p --FONT_LABEL=7p
        fi

      # --- Elevation ---
      gmt subplot set $((r*4+3))
        gmt grdcut "$DEM_SRC" $RZ -Gdem.grd 2>/dev/null
        gmt grdgradient dem.grd -A300 -Ne0.6 -Gdem_int.grd 2>/dev/null
        gmt grdimage dem.grd $RZ $JZ -Cdem.cpt -Idem_int.grd
        gmt plot "${PF[$r]}" $RZ $JZ -W0.6p,black
        gmt basemap $RZ $JZ -Bxa1f0.5 -Bya1f0.5 "-BWSne${T3}" $SB
        if [ $r -eq 3 ]; then
          gmt colorbar -Cdem.cpt -DJBC+w4.4c/0.20c+h+o0/1.25c -Bxa1000+l"Elevation (m)" \
              --FONT_ANNOT_PRIMARY=6p --FONT_LABEL=7p
        fi
    done
  gmt subplot end

  gmt text -R0/22.55/0/1 -JX22.55c/0.5c -N -Y-3.4c \
      -F+cBL+f7p,Helvetica,gray45+t"Data: CLC+ Backbone 2018 10 m (EEA/Copernicus); eVIIRS NDVI; MODIS LST; GEBCO/SRTM DEM. Boundaries: geoBoundaries ADM1. CRS: WGS 84 (EPSG:4326)."
gmt end show
