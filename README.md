# wind-energy-forecasting
Predicting wind energy produced with a Bayesian generalized linear multilevel model (Bayesian GLMM). Case study in Finland with weather data from the Finnish Meteorological Institute and wind energy data from Fingrid.

## Model
* Wind speed
    * GLM:
        * Logit link function for atleast wind speed (seems to best follow the wind turbine power curve)
        * Gaussian distribution for error (error size not particularly dependent on prediction?)
    * Prior:
        Gamma prior (Positive and continuous)?

* Air pressure
    * GLM:
        * linear, log, logit?
        * Gaussian or gamma error distribution (error might increase with mean?)
    * Prior:
        * Gamma prior (Positive and continuous)?

* Temperature
    * No idea, requires some plotting
    * Read from somewhere that winter is the windiest season in Finland
* Relative humidity
    * Wonder what kind of a relation this has

## Preprosessing

* Mean center
* Divide each feature with its variance

## Questions

* Using multiple regions to predict common outcome
    * All of them as separate features?
    * Mean of regions?
* Predictions with stan
    * X_new -> Compute predictions with all posterior draws -> predictive distribution for X?
* Prior suggestions