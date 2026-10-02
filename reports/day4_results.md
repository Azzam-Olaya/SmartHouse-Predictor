# Résultats du Jour 4

Les cellules de modélisation ont été exécutées avec un découpage entraînement/test 80/20 et une validation croisée à 5 folds. Les résultats sont en dollars.

## Comparaison sur le jeu de test

| Modèle | MAE | RMSE | R² |
|---|---:|---:|---:|
| Random Forest | 30,646 | 42,965 | 0.505 |
| Gradient Boosting | 30,271 | 43,893 | 0.483 |
| Linear Regression | 32,116 | 44,167 | 0.477 |

## Validation croisée (5 folds)

| Modèle | MAE moyenne | RMSE moyenne | R² moyen |
|---|---:|---:|---:|
| Gradient Boosting | 28,874 | 42,803 | 0.417 |
| Random Forest | 29,093 | 42,848 | 0.414 |
| Linear Regression | 30,910 | 45,745 | 0.334 |

## Random Forest : initial / optimisé

| Version | MAE | RMSE | R² |
|---|---:|---:|---:|
| Random Forest initial | 30,646 | 42,965 | 0.505 |
| Random Forest optimisé | 30,771 | 43,081 | 0.50 |

Le Random Forest optimisé a une meilleure RMSE moyenne en validation (42 340 $ contre 42 848 $ pour le modèle initial), mais une RMSE légèrement plus élevée sur le test (43 081 $ contre 42 965 $). Le modèle initial est donc retenu pour l’application.

## Plus grandes erreurs

| Id | Prix réel | Prédit | Erreur | Qualité | Surface habitable | Quartier | Année |
|---:|---:|---:|---:|---:|---:|---|---:|
| 692 | 755,000 | 434,329 | -320,671 | 10 | 4316 | NoRidge | 1994 |
| 1374 | 466,500 | 262,331 | -204,169 | 10 | 2633 | NoRidge | 2001 |
| 2683 | 209,375 | 401,134 | +191,759 | 9 | 3500 | NoRidge | 1993 |
| 232 | 403,000 | 234,865 | -168,135 | 8 | 2794 | NoRidge | 1995 |
| 179 | 501,837 | 333,828 | -168,009 | 9 | 2234 | StoneBr | 2008 |
| 2823 | 235,419 | 387,549 | +152,130 | 6 | 3672 | Edwards | 1935 |
| 2340 | 164,430 | 302,784 | +138,354 | 10 | 1966 | Somerst | 2007 |
| 46 | 319,900 | 186,634 | -133,266 | 9 | 1752 | NridgHt | 2005 |
| 314 | 375,000 | 251,189 | -123,811 | 7 | 2036 | Timber | 1965 |
| 528 | 446,261 | 323,298 | -122,963 | 9 | 2713 | NridgHt | 2008 |

Les erreurs extrêmes concernent des logements grands, de qualité élevée ou atypiques par leur rapport entre surface, quartier et prix. Le modèle manque peut-être d’exemples similaires ; il faut examiner les autres caractéristiques et vérifier les données avant d’attribuer une cause.

## Variables importantes

Le graphique `figures/variables_importantes.svg` montre que `TotalSF` arrive en tête, suivi notamment de `2ndFlrSF`, `LotArea`, `GrLivArea` et `OverallQual`. Ces importances décrivent le modèle, pas des causes du prix.

## Graphiques

Les prix réels/prédits, les résidus, la distribution des erreurs et la comparaison des modèles sont dans `reports/figures/`.
