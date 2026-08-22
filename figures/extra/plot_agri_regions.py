#!/usr/bin/env python3
# =============================================================================
# Turkiye geographical regions over GEBCO relief - region borders built from
# geoBoundaries ADM1 (81 provinces), dissolved into classical regional groups.
#
# The province layer is geoBoundaries-TUR-ADM1 (open, CC-BY 4.0), whose province
# name column is `shapeName`. Provinces are grouped by name into geographical
# regions and DISSOLVED, so the dashed loops follow real province boundaries.
# Style (beige relief, flat blue sea, coloured dashed loops, boxed legend, scale
# bar, compass rose, highlighted case-study provinces) is preserved.
#
# Requires: pygmt, geopandas   (conda env: pygmt)
# =============================================================================

import os
import glob
import pygmt
import geopandas as gpd

# ------------------------------- CONFIG --------------------------------------
import os
DATA      = os.environ.get("DATA_DIR", os.path.expanduser("~/precision-ag-data"))
GEBCO     = f"{DATA}/GEBCO_2023.nc"                     # adjust if different
PROV      = f"{DATA}/geoBoundaries-TUR-ADM1.geojson"    # geoBoundaries ADM1
NAMECOL   = "shapeName"                                 # province-name column
OUT       = "fig11_agri_areas_corrected.png"
REGION    = [25, 45.6, 34.4, 42.7]                      # W, E, S, N (incl. Cyprus)
SPACING   = "0.01d"                                     # ~1 km; "0.02d" = faster
USE_ASCII = True

# auto-find a GEBCO .nc if the exact name is wrong
if not os.path.exists(GEBCO):
    cand = (glob.glob(f"{DATA}/**/*GEBCO*.nc", recursive=True)
            or glob.glob(f"{DATA}/**/*gebco*.nc", recursive=True))
    if cand:
        GEBCO = cand[0]; print("Using GEBCO grid:", GEBCO)
    else:
        raise FileNotFoundError("No GEBCO .nc found under DATA; set GEBCO explicitly.")

# ---- province (geoBoundaries shapeName) -> geographical region ---------------
# Whole-province assignment; officially split provinces go entirely to one region.
# The five regions shown in the legend match the paper; the eastern and
# south-eastern provinces are grouped too so every province is assigned.
REGIONS = {
    "Mediterranean":   ("46/174/62",  ["Antalya","Burdur","Isparta","Mersin","Adana",
                                        "Osmaniye","Hatay","Kahramanmaras"]),
    "Aegean":          ("30/120/210", ["Izmir","Aydin","Mugla","Denizli","Manisa",
                                        "Usak","Kutahya","Afyonkarahisar"]),
    "Marmara":         ("240/140/30", ["Istanbul","Tekirdag","Edirne","Kirklareli",
                                        "Canakkale","Balikesir","Bursa","Yalova",
                                        "Kocaeli","Sakarya","Bilecik"]),
    "BlackSea":        ("150/70/180", ["Zonguldak","Karabuk","Bartin","Kastamonu",
                                        "Sinop","Samsun","Ordu","Giresun","Trabzon",
                                        "Rize","Artvin","Gumushane","Bayburt","Amasya",
                                        "Tokat","Corum","Duzce","Bolu"]),
    "CentralAnatolia": ("225/40/40",  ["Ankara","Konya","Karaman","Aksaray","Nigde",
                                        "Nevsehir","Kirsehir","Kirikkale","Cankiri",
                                        "Yozgat","Sivas","Kayseri","Eskisehir"]),
    "EastAnatolia":    ("120/120/120",["Erzurum","Erzincan","Agri","Kars","Ardahan",
                                        "Igdir","Tunceli","Bingol","Mus","Bitlis","Van",
                                        "Hakkari","Malatya","Elazig"]),
    "SEAnatolia":      ("120/120/120",["Gaziantep","Kilis","Sanliurfa","Adiyaman",
                                        "Diyarbakir","Mardin","Batman","Sirnak","Siirt"]),
}
# only these five are drawn as dashed loops + shown in the legend (paper scope)
DRAW   = ["Mediterranean", "Aegean", "Marmara", "BlackSea", "CentralAnatolia"]
LEGEND = [("Mediterranean",   "1) Mediterranean Region"),
          ("Aegean",          "2) Aegean Region"),
          ("Marmara",         "3) Marmara Region"),
          ("BlackSea",        "4) Black Sea Region"),
          ("CentralAnatolia", "5) Central Anatolia Region")]

# case-study provinces to highlight - three faint, DISTINCT tints
# (Antalya+Konya share the warm tint as they anchor the S/central case;
#  Izmir gets a faint green, Rize a faint blue) with thin outlines.
CASE_STYLE = {
    "Antalya": ("255/214/120", "150/110/30"),
    "Konya":   ("255/214/120", "150/110/30"),
    "Izmir":   ("190/224/170", "70/120/60"),
    "Rize":    ("180/210/235", "50/90/140"),
}
CASE_PROVS = list(CASE_STYLE.keys())
CASE_ALPHA = 60

# --------------------------- BUILD REGION POLYGONS ---------------------------
prov = gpd.read_file(PROV)

# geoBoundaries uses Turkish characters in shapeName; normalise to ASCII so the
# region lookup is robust regardless of accents (Izmir vs Izmir, Mugla vs Mugla).
def deaccent(s):
    table = str.maketrans({
        "ı":"i","İ":"I","ş":"s","Ş":"S","ğ":"g","Ğ":"G","ü":"u","Ü":"U",
        "ö":"o","Ö":"O","ç":"c","Ç":"C","â":"a","î":"i","û":"u"})
    return (s or "").translate(table)

prov["key"] = prov[NAMECOL].map(deaccent)
code2reg = {deaccent(c): r for r, (col, codes) in REGIONS.items() for c in codes}
prov["region"] = prov["key"].map(code2reg)

n_assigned = prov["region"].notna().sum()
print(f"Provinces read: {len(prov)}; assigned to a region: {n_assigned}")

regions_gdf = prov.dropna(subset=["region"]).dissolve(by="region")
case_gdf    = prov[prov["key"].isin([deaccent(c) for c in CASE_PROVS])].copy()

# ------------------- RELIEF (cut + downsample + hillshade) -------------------
cut   = pygmt.grdcut(grid=GEBCO, region=REGION)
cut   = pygmt.grdsample(grid=cut, spacing=SPACING, region=REGION)
inten = pygmt.grdgradient(grid=cut, azimuth=300, normalize="e0.6")

# soft beige land ramp - CONTINUOUS cpt (4-column format: z0 c0 z1 c1)
cpt = "land_beige.cpt"
with open(cpt, "w") as f:
    f.write("-6000 200/226/240  0    236/230/212\n"   # (sea range; repainted later)
            "0     236/230/212  1200 214/196/165\n"
            "1200  214/196/165  3000 188/168/140\n"
            "B 236/230/212\nF 188/168/140\nN 200/226/240\n")

# --------------------------------- PLOT --------------------------------------
fig = pygmt.Figure()
pygmt.config(MAP_FRAME_TYPE="plain", FONT_ANNOT_PRIMARY="9p,Helvetica",
             FONT_LABEL="9p", PS_CHAR_ENCODING="ISOLatin1+",
             MAP_GRID_PEN_PRIMARY="0.25p,white,2_2")
proj = "Q22c"

# flat light-blue sea first
fig.coast(region=REGION, projection=proj, land="240/232/210",
          water="200/226/240", resolution="h")
# beige shaded relief over everything (slightly transparent), then repaint the
# sea flat blue on top so land keeps the hillshade and the sea stays clean
fig.grdimage(grid=cut, cmap=cpt, shading=inten, region=REGION,
             projection=proj, transparency=12)
fig.coast(region=REGION, projection=proj, resolution="h", water="200/226/240")

# highlighted case-study provinces (under the dashed loops), each tinted
for pname, (fillc, penc) in CASE_STYLE.items():
    sub = prov[prov["key"] == deaccent(pname)]
    if not sub.empty:
        fig.plot(data=sub, fill=f"{fillc}@{CASE_ALPHA}", pen=f"1.0p,{penc}")

# crisp coastline + international borders on top
fig.coast(region=REGION, projection=proj, shorelines="0.5p,gray20",
          borders="1/0.7p,gray45", resolution="h")

# ------------------------------- CITIES --------------------------------------
CITIES = [
    (28.98, 41.01, "Istanbul"),   (27.51, 40.98, "Tekirdag"),
    (26.41, 40.15, "Canakkale"),  (29.06, 40.19, "Bursa"),
    (27.14, 38.42, "Izmir"),      (27.85, 37.85, "Aydin"),
    (29.09, 37.78, "Denizli"),    (28.36, 37.22, "Mugla"),
    (30.71, 36.90, "Antalya"),    (34.63, 36.81, "Mersin"),
    (35.33, 37.00, "Adana"),      (36.16, 36.20, "Hatay"),
    (30.52, 39.78, "Eskisehir"),  (32.85, 39.93, "Ankara"),
    (32.48, 37.87, "Konya"),      (35.48, 38.73, "Kayseri"),
    (37.02, 39.75, "Sivas"),      (36.33, 41.29, "Samsun"),
    (39.72, 41.00, "Trabzon"),    (41.28, 39.90, "Erzurum"),
    (43.38, 38.49, "Van"),        (40.22, 37.91, "Diyarbakir"),
    (37.38, 37.07, "Gaziantep"),  (40.52, 41.02, "Rize"),
]
# label placement overrides for crowded coastal cities: (justify, offset)
LBL = {
    "Samsun":  ("CB", "0c/0.22c"),     # up into the Black Sea
    "Trabzon": ("RB", "-0.14c/0.20c"), # up-left into the sea
    "Rize":    ("LB", "0.14c/0.20c"),  # up-right into the sea (separates from Trabzon)
    "Istanbul":("LM", "0.18c/0.10c"),
    "Tekirdag":("RM", "-0.18c/0.10c"),
}
for lon, lat, name in CITIES:
    fig.plot(x=lon, y=lat, style="c0.09c", fill="black", pen="0.3p,black")
    just, off = LBL.get(name, ("LM", "0.18c/0c"))
    fig.text(x=lon, y=lat, text=name, font="9p,Helvetica,black",
             justify=just, offset=off)

# ------------------------------ SEA LABELS -----------------------------------
for x, y, t in [(33.8, 42.35, "Black Sea"),
                (30.0, 35.75, "Mediterranean Sea")]:
    fig.text(x=x, y=y, text=t, font="10p,Helvetica-Oblique,30/80/160", justify="CM")
# Sea of Marmara - tiny, two lines (space is small)
fig.text(x=28.05, y=40.98, text="Sea of", font="6p,Helvetica-Oblique,30/80/160", justify="CM")
fig.text(x=28.05, y=40.75, text="Marmara", font="6p,Helvetica-Oblique,30/80/160", justify="CM")
# Aegean label on two lines (own centre, clean break)
fig.text(x=25.5, y=38.45, text="Aegean", font="10p,Helvetica-Oblique,30/80/160", justify="CM")
fig.text(x=25.5, y=38.05, text="Sea",    font="10p,Helvetica-Oblique,30/80/160", justify="CM")

# ------------------- FRAME, SCALE BAR, COMPASS ROSE --------------------------
fig.basemap(region=REGION, projection=proj,
            frame=["WeSN", "xa4f2g4", "ya2f1g2"],
            map_scale="g28.7/35.35+w400k+f+u+jLM",
            rose="jTR+w0.9c+f2+lW,E,S,N+o0.5c/0.5c")

# ---------------------- LEGEND (boxed, lower-right) --------------------------
bx0, bx1, by0, by1 = 41.4, 45.5, 34.55, 36.85
fig.plot(x=[bx0, bx1, bx1, bx0, bx0], y=[by0, by0, by1, by1, by0],
         fill="white", pen="0.8p,black")
rows_y = [36.55, 36.24, 35.93, 35.62, 35.31, 34.92]
for (key, label), yy in zip(LEGEND, rows_y):
    col = REGIONS[key][0]
    fig.plot(x=[bx0 + 0.20, bx0 + 0.85], y=[yy, yy], pen=f"1.4p,{col}")
    fig.text(x=bx0 + 1.05, y=yy, text=label, font="7p,Helvetica,black", justify="LM")
# case-study swatch row: three faint tinted squares (warm / green / blue)
yy = rows_y[5]
swx = [bx0 + 0.26, bx0 + 0.52, bx0 + 0.78]
swc = [("255/214/120","150/110/30"), ("190/224/170","70/120/60"),
       ("180/210/235","50/90/140")]
for xx, (fc, pc) in zip(swx, swc):
    fig.plot(x=[xx], y=[yy], style="s0.18c", fill=f"{fc}@{CASE_ALPHA}", pen=f"0.5p,{pc}")
fig.text(x=bx0 + 1.05, y=yy, text="Case-study provinces",
         font="7p,Helvetica,black", justify="LM")

# region borders drawn LAST so they sit above relief, provinces, and labels
for name in DRAW:
    col = REGIONS[name][0]
    if name in regions_gdf.index:
        fig.plot(data=regions_gdf.loc[[name]], pen=f"0.7p,{col}")

fig.savefig(OUT, dpi=300)
print("wrote", OUT)

# =============================================================================
# NOTES
# * Province layer: geoBoundaries-TUR-ADM1 (CC-BY 4.0). Region borders are a
#   WHOLE-PROVINCE dissolve into the classical geographical regions; officially
#   split provinces are assigned entirely to one region (state this in caption).
# * Only the five paper regions are drawn as dashed loops and listed in the
#   legend; eastern/south-eastern provinces are still grouped internally.
# * Speed/heat: grdcut -> grdsample to ~1 km keeps hillshading light; set
#   SPACING="0.02d" if the external drive is slow.
# =============================================================================
