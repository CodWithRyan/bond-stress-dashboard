## Objectifs
- Implémenter : **DF**, **zero rates**, **pricing par actualisation**, **DV01**, **duration modifiée**, **convexité**.
- Produire un rapport par ligne et total : prix, DV01, contributions ∆P sous stress.
## Portée V1
- Courbe : interpolation **log-linéaire sur ln(DF)** à partir de points (maturité, taux continu).
- Obligations : plain vanilla, coupons **annuels**, pas d’accumulé.
- Stress : chocs **parallèles** +25 bps / +100 bps.
- Sensibilités : différences finies ±1 bp (DV01/duration/convexité numériques).
## Données
- Fichier d’entrée **data/portfolio.csv** (exemple de contenu) :
\`\`\`
id,face,coupon,freq,maturity
BOND_ZC,100,0.00,1,2028-12-30
BOND_A,100,0.03,1,2030-12-30
BOND_B,100,0.05,1,2035-12-30
\`\`\`
## Résultats attendus
- Par ligne : \`price\`, \`dv01\`, \`dur_mod\`, \`conv\`, \`∆P(+25bps)\`, \`∆P(+100bps)\`.
- Graphiques : courbe avant/après, barres ∆P par ligne.
- Sanity checks : Zéro-coupon (duration ≈ maturité, convexité > 0) ; ∑DV01≈DV01 portefeuille (±2%) ; signe de ∆P correct quand la courbe monte.
## Installation
\`\`\`bash
python3 -m venv bond_stress_env
source bond_stress_env/bin/activate
pip install -r requirements.txt
\`\`\`
## Exécution (V1)
- Ouvrir \`notebooks/01_demo.ipynb\` et exécuter toutes les cellules.
- Les figures et tables sont écrites dans \`outputs/\`.

## Arborescence du repo
\`\`\`
.
├─ src/
├─ tests/
├─ data/
├─ notebooks/
├─ outputs/
├─ requirements.txt
├─ .gitignore
└─ README.md
\`\`\`
### Références
- Hull (11e, éd. française) — Chap. 4 (taux, zéro, pricing, duration, convexité).
