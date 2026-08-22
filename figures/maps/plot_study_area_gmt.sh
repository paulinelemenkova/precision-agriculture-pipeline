#!/usr/bin/env bash
# =============================================================================
# fig01 - Study-area map of Turkiye with four case-study provinces.
# PURE GMT 6 (not PyGMT). Composite layout:
#   [1] main country panel: SRTM15 shaded relief (elevation CPT) + 4 coloured
#       provinces + coast/lakes/rivers/borders + seas & neighbour labels +
#       graticule + scale bar + compass + boxed legend + world-locator inset
#   [2] four province zoom sub-panels: SRTM03 relief + province polygon + centre
#   [3] caption strip + CRS note
#
# REMOTE DATA (auto-fetched by GMT, no local files):
#   @earth_relief_15s  (SRTM15+, ~450 m)  -> country panel
#   @earth_relief_03s  (SRTM  ,  ~90 m)   -> zoom panels  (finer than GEBCO)
#   pscoast/coast GSHHG -> coastlines, LAKES (-C), RIVERS (-I), borders (-N)
#
# LOCAL DATA (only the province polygons for the coloured study areas):
#   geoBoundaries-TUR-ADM1.geojson   (field 'shapeName')
#
# PREREQUISITES:
#   * GMT >= 6.4 on PATH  (your GMT.app 6.5.0 is fine)
#   * ogr2ogr (GDAL) on PATH to slice the province polygons
#     -> it ships with your conda 'pygmt' env; either run inside that env
#        (conda activate pygmt) or install GDAL (brew install gdal).
#
# RUN:   bash plot_study_area_gmt.sh
# =============================================================================
set -e

# ---------------------------------------------------------------------------
# DATA_DIR: root folder holding the open-access source rasters/vectors.
# Override with:  export DATA_DIR=/path/to/your/data   (see README, Data sources)
DATA_DIR="${DATA_DIR:-$HOME/precision-ag-data}"
# ---------------------------------------------------------------------------


# --------------------------------------------------------------- CONFIG -----
PROV="${DATA_DIR}/geoBoundaries-TUR-ADM1.geojson"   # <-- your file
GEBCO="${DATA_DIR}/GEBCO_2023.nc"                    # <-- your relief grid
NAMECOL="shapeName"
OUT="fig01_study_area"

# study provinces (geoBoundaries spelling) + fill colours (paper scheme)
declare -a PN=("Antalya" "Izmir" "Konya" "Rize")
declare -a PC=("112/88/163" "255/234/0" "217/51/63" "44/169/225")
declare -a PF=("ant.gmt" "izm.gmt" "kon.gmt" "riz.gmt")

# province centres: lon lat name  (for dots + labels)
cat > centres.txt <<'TXT'
30.71 36.90 Antalya
27.14 38.42 Izmir
32.48 37.87 Konya
40.52 41.02 Rize
TXT

# zoom windows per province:  W E S N
declare -a Z_ANT=(29.2 32.0 36.05 37.55)
declare -a Z_IZM=(26.2 28.4 37.65 39.35)
declare -a Z_KON=(31.5 34.0 36.55 38.75)
declare -a Z_RIZ=(40.25 41.15 40.6 41.35)

# ------------------------------------------------- slice province polygons --
for i in 0 1 2 3; do
  rm -f "${PF[$i]}"
  ogr2ogr -f "OGR_GMT" "${PF[$i]}" "$PROV" \
          -where "\"${NAMECOL}\"='${PN[$i]}'"
done

# elevation CPT for the relief (built-in topo/bathy ramp; swap to taste:
#   geo | oleron | dem2 | terra | etopo1 )

# winbox <file> : echo "-Rw/e/s/n" framing the polygon's exact bbox, padded to the
# zoom-panel aspect (5.2/4.8) plus a 10% margin, so the province fills its box.
winbox () {
  set -- $(gmt info "$1" -C)      # xmin xmax ymin ymax
  awk -v w=$1 -v e=$2 -v s=$3 -v n=$4 -v A=1.083333 -v m=0.10 'BEGIN{
    dlon=e-w; dlat=n-s; cx=(w+e)/2; cy=(s+n)/2;
    if (dlon/dlat < A) dlon=A*dlat; else dlat=dlon/A;
    dlon*=(1+m); dlat*=(1+m);
    printf "-R%.4f/%.4f/%.4f/%.4f\n", cx-dlon/2, cx+dlon/2, cy-dlat/2, cy+dlat/2;
  }'
}

gmt makecpt -Cgeo -T-4000/4000/100 -Z > elev.cpt

# =============================================================================
gmt begin ${OUT} png,pdf
  gmt set FONT_ANNOT_PRIMARY 9p,Helvetica FONT_LABEL 10p FONT_TITLE 12p,Helvetica-Bold \
          MAP_FRAME_TYPE plain PS_CHAR_ENCODING ISOLatin1+ \
          MAP_GRID_PEN_PRIMARY 0.25p,white MAP_FRAME_PEN 1p

  RG=-R25/45.6/35.4/42.6
  JM=-JM17c

  # ============================ MAIN COUNTRY PANEL ========================== #
  # cut local GEBCO to the region, resample to ~1 km, and hillshade
  gmt grdcut  "$GEBCO" $RG -Gcountry.grd
  gmt grdgradient country.grd -A300 -Ne0.6 -Gcountry_int.grd
  gmt grdimage country.grd $RG $JM -Celev.cpt -Icountry_int.grd
  gmt coast $RG $JM -Slightblue -Clightblue -Df -A80 \
            -I1/0.6p,steelblue -I2/0.3p,steelblue \
            -N1/0.9p,gray25 -N2/0.25p,gray55

  # coloured study provinces + thin outline
  for i in 0 1 2 3; do
    gmt plot "${PF[$i]}" $RG $JM -G"${PC[$i]}"@35 -W0.5p,gray25
  done

  # centres + labels
  gmt plot centres.txt $RG $JM -Sc0.11c -Gblack -W0.3p,white
  gmt text  centres.txt $RG $JM -F+f9p,Helvetica-Bold,black+jTL -D0.16c/-0.08c

  # country / sea / neighbour labels
  gmt text $RG $JM -F+f+j <<'TXT'
36.0 39.3 13p,Helvetica,white CM T\374rkiye
33.5 42.15 11p,Helvetica-Oblique,30/80/160 CM Black Sea
30.2 35.75 11p,Helvetica-Oblique,30/80/160 CM Mediterranean Sea
26.35 37.9 10p,Helvetica-Oblique,30/80/160 CM Aegean
26.35 37.4 10p,Helvetica-Oblique,30/80/160 CM Sea
26.2 42.45 7p,Helvetica,ivory CM BULGARIA
25.6 41.05 7p,Helvetica,ivory CM GREECE
43.9 42.3 7p,Helvetica,ivory CM GEORGIA
44.9 40.35 7p,Helvetica,ivory CM ARMENIA
45.1 38.3 7p,Helvetica,ivory CM IRAN
40.9 36.55 7p,Helvetica,ivory CM SYRIA
44.6 36.55 7p,Helvetica,ivory CM IRAQ
TXT

  # frame (annotate West+North only) + graticule + scale bar + compass rose
  gmt basemap $RG $JM -Bxa4f2g4 -Bya2f1g2 -BWsNe -Tdg27/41.6+w0.85c+f2+l,,,N
  gmt basemap $RG $JM -LjBR+w400k+f+u+o1.6c/0.5c+c37 -F+gwhite@35+p0.4p,gray40+r

  # ------------------------------- LEGEND box ------------------------------ #
  # placed just OUTSIDE the map, top-right
  gmt legend $RG $JM -DjTR+w4.6c+o-5.2c/0.0c -F+p0.8p,black+gwhite+i+s <<'LEG'
H 11p,Helvetica-Bold Legend
S 0.28c c 0.11c black 0.3p,white 0.7c Provincial Center
S 0.28c s 0.32c white 0.6p,black 0.7c Province Boundary
S 0.28c s 0.32c 240/230/210 0.4p,gray50 0.7c International Boundary
S 0.28c s 0.32c lightblue 0.4p,steelblue 0.7c Water Bodies
G 0.12c
H 10p,Helvetica-Bold Study Areas
H 10p,Helvetica-Bold (Representative Regions)
S 0.28c s 0.32c 112/88/163 0.3p,gray30 0.7c Antalya (Mediterranean)
S 0.28c s 0.32c 255/234/0 0.3p,gray30 0.7c Izmir (Aegean Region)
S 0.28c s 0.32c 217/51/63 0.3p,gray30 0.7c Konya (Central Anatolia)
S 0.28c s 0.32c 44/169/225 0.3p,gray30 0.7c Rize (Black Sea Region)
LEG

  # --------------------------- WORLD LOCATOR inset ------------------------- #
  gmt inset begin -DjBR+w4.6c/2.6c+o-5.2c/0.0c -F+p0.8p,black+gwhite
    gmt coast -Rg -JG35/39/4.6c -Ggray85 -Slightblue -A5000 -Bg
    # red rectangle around Turkiye
    gmt plot -Rg -JG35/39/4.6c -W1.4p,red <<'BOX'
25 35.4
45.6 35.4
45.6 42.6
25 42.6
25 35.4
BOX
  gmt inset end

  # ============================ PROVINCE ZOOM PANELS ======================= #
  # identical 5.2x4.8 cm boxes (fixed via -JX...d); each window is the province's
  # exact bounding box (winbox) so the region fills its square. Scale bars jBR.
  PROV_F=(ant.gmt izm.gmt kon.gmt riz.gmt)
  PROV_C=(112/88/163 255/234/0 217/51/63 44/169/225)
  PROV_LON=(30.71 27.14 32.48 40.52)
  PROV_LAT=(36.90 38.42 37.87 41.02)
  PROV_NM=(Antalya Izmir Konya Rize)
  PROV_SL=(50k 50k 50k 20k)
  JZ=-JX5.2cd/4.8cd

  gmt subplot begin 1x4 -Fs5.2c/4.8c -M0.06c -Y-5.4c \
      --FONT_ANNOT_PRIMARY=5p,Helvetica,white --FORMAT_GEO_MAP=dddF \
      --MAP_FRAME_TYPE=inside --MAP_TICK_LENGTH_PRIMARY=2p \
      --MAP_ANNOT_OFFSET_PRIMARY=1.5p
  for i in 0 1 2 3; do
    gmt subplot set $i
      RZ=$(winbox "${PROV_F[$i]}")
      CLAT=$(echo "$RZ" | sed 's/-R//' | awk -F/ '{printf "%.2f",($3+$4)/2}')
      gmt grdcut "$GEBCO" $RZ -Gz.grd
      gmt grdgradient z.grd -A300 -Ne0.6 -Gz_int.grd
      gmt grdimage z.grd $RZ $JZ -Celev.cpt -Iz_int.grd
      gmt coast $RZ $JZ -Slightblue -Clightblue -Df -N1/0.5p,gray30
      gmt plot "${PROV_F[$i]}" $RZ $JZ -G"${PROV_C[$i]}"@35 -W0.8p,gray20
      echo "${PROV_LON[$i]} ${PROV_LAT[$i]} ${PROV_NM[$i]}" | \
        gmt plot $RZ $JZ -Sc0.12c -Gblack -W0.3p,white
      echo "${PROV_LON[$i]} ${PROV_LAT[$i]} ${PROV_NM[$i]}" | \
        gmt text $RZ $JZ -F+f9p,Helvetica-Bold+jBC -D0c/0.16c
      if [ $i -eq 3 ]; then BB="-Bxa0.5f0.25g0.5 -Bya0.5f0.25g0.5"; else BB="-Bxa1f0.5g1 -Bya1f0.5g1"; fi
      gmt basemap $RZ $JZ $BB -BWSne
      gmt basemap $RZ $JZ -LjBR+w"${PROV_SL[$i]}"+u+o0.28c/0.55c+c${CLAT} \
          -F+gwhite@30+p0.3p,gray40+r --FONT_ANNOT_PRIMARY=6p,Helvetica,black
  done
  gmt subplot end

  # ------------------------------- CAPTION strip --------------------------- #
  gmt text -R0/22/0/1 -JX22c/0.55c -N -Y-1.1c -F+cTL+f9.5p,Helvetica,gray25+t"Study area: four representative agricultural regions of Turkiye (Antalya, Izmir, Konya, Rize), chosen to span diverse climatic, topographic and agricultural conditions."
  gmt text -R0/22/0/1 -JX22c/0.55c -N -Y-0.55c -F+cTL+f9p,Helvetica,gray40+t"Coordinate System: WGS 84 (EPSG:4326)"

gmt end show
