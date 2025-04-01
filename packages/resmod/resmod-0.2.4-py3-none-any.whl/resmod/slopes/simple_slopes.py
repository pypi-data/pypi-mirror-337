#!/usr/bin/python3

def simple_slopes(outcome, pred, modx, data, controls=None, mod2=None,
                  modx_values=None, modx_legend_labels=None,
                  mod2_values=None, alpha=0.05):
    """
    Calculate simple slopes for an interaction model.

    This function estimates a moderated regression model with the formula:
        outcome ~ pred * modx [+ controls]
    and calculates the simple slope of `pred` at specific values of `modx`.

    For a continuous moderator:
      - If modx_values is not supplied, slopes are computed at [mean - SD, mean, mean + SD],
        with the simple slope defined as:
          slope = b_pred + v * b_int,
        and its standard error is given by:
          se = sqrt(Var(b_pred) + v^2 * Var(b_int) + 2*v*Cov(b_pred, b_int)).
      - The row index of the returned DataFrame will be set to the corresponding labels
        (by default, "-1SD", "Mean", "+1SD").

    For a categorical or binary moderator, the unique levels are used and converted to strings
    as row labels (or as provided by modx_legend_labels).

    If mod2 is provided, the function iterates over each specified level of mod2. For each level,
    it estimates the model on the subset of data corresponding to that level, computes the simple
    slopes, and adds a column "at_mod2_value" with the level. All these DataFrames are concatenated
    into one large DataFrame.

    Parameters
    ----------
    outcome : str
        The outcome variable name.
    pred : str
        The focal predictor variable name.
    modx : str
        The moderator variable name.
    data : pd.DataFrame
        DataFrame containing the data.
    controls : list of str, optional
        List of additional control variable names to include in the model.
    mod2 : str, optional
        A second moderator variable. If provided, simple slopes are computed separately for each
        level of mod2.
    modx_values : array-like, optional
        Values of modx at which to compute simple slopes. For continuous modx, if not provided,
        defaults to [mean - SD, mean, mean + SD]. For categorical moderators, defaults to sorted unique values.
    modx_legend_labels : list of str, optional
        Custom labels for the modx levels. For continuous modx, if not provided defaults to ["-1SD", "Mean", "+1SD"].
    mod2_values : array-like, optional
        Values of mod2 for which to calculate simple slopes. If provided, these values will be used;
        otherwise, the function uses the unique sorted values in the data.
    alpha : float, default 0.05
        Significance level for confidence intervals.

    Returns
    -------
    result : pd.DataFrame
        A DataFrame with the following columns:
          - at_mod2_value (if mod2 is provided)
          - modx (the modx value at which the slope was computed)
          - slope, se, t, p, ci_lower, ci_upper.
        The DataFrame's row index is set to modx_legend_labels.

    Methodology is based on standard moderated regression approaches (Aiken & West, 1991; Cohen et al., 2003).

    Citations:
      - Aiken, L. S., & West, S. G. (1991). Multiple Regression: Testing and Interpreting Interactions. Sage.
      - Cohen, J., Cohen, P., West, S. G., & Aiken, L. S. (2003). Applied Multiple Regression/Correlation Analysis for the Behavioral Sciences (3rd ed.). Lawrence Erlbaum Associates.
    """
    # Require packages import checking
    try:
      import numpy as np
      import pandas as pd
      import statsmodels.formula.api as smf
      import scipy.stats as st
    except ImportError as e:
        raise ImportError(f"Missing required package: {e.name}. Install it using `pip install {e.name}`")

    # Helper: compute slopes from a fitted model given a value of modx.
    def compute_slopes(fit, modx_val):
        try:
            b_pred = fit.params[pred]
            b_int = fit.params[f"{pred}:{modx}"]
        except KeyError:
            b_pred = fit.params[pred]
            b_int = fit.params[f"{modx}:{pred}"]

        cov = fit.cov_params()
        var_pred = cov.loc[pred, pred]
        # Get the interaction term variance (check for either naming)
        if f"{pred}:{modx}" in cov.index:
            var_int = cov.loc[f"{pred}:{modx}", f"{pred}:{modx}"]
            cov_pred_int = cov.loc[pred, f"{pred}:{modx}"]
        else:
            var_int = cov.loc[f"{modx}:{pred}", f"{modx}:{pred}"]
            cov_pred_int = cov.loc[pred, f"{modx}:{pred}"]

        slope = b_pred + modx_val * b_int
        se = np.sqrt(var_pred + (modx_val ** 2) * var_int + 2 * modx_val * cov_pred_int)
        t_val = slope / se
        df_resid = fit.df_resid
        p_val = 2 * (1 - st.t.cdf(np.abs(t_val), df=df_resid))
        t_crit = st.t.ppf(1 - alpha/2, df=df_resid)
        ci_lower = slope - t_crit * se
        ci_upper = slope + t_crit * se
        return slope, se, t_val, p_val, ci_lower, ci_upper

    # Determine modx values and corresponding labels.
    # For continuous moderator: use [mean - SD, mean, mean + SD] if modx_values is not provided.
    if data[modx].dtype.kind in 'biufc' and data[modx].nunique() > 2:
        if modx_values is None:
            modx_mean = data[modx].mean()
            modx_std = data[modx].std()
            modx_values = [modx_mean - modx_std, modx_mean, modx_mean + modx_std]
            if modx_legend_labels is None:
                modx_legend_labels = ["-1SD", "Mean", "+1SD"]
        else:
            if modx_legend_labels is None:
                modx_legend_labels = [str(val) for val in modx_values]
    else:
        # For categorical moderator.
        if modx_values is None:
            modx_values = sorted(data[modx].unique())
        if modx_legend_labels is None:
            modx_legend_labels = [str(val) for val in modx_values]

    # Build formula string.
    formula = f"{outcome} ~ {pred} * {modx}"
    if controls is not None and len(controls) > 0:
        formula += " + " + " + ".join(controls)

    # Define inner function to process a dataset and return a DataFrame with modx conditions.
    def process_data(df):
        fit = smf.ols(formula, data=df).fit()
        rows = []
        for val in modx_values:
            slope, se, t_val, p_val, ci_lower, ci_upper = compute_slopes(fit, val)
            rows.append({
                modx: val,
                'slope': slope,
                'se': se,
                't': t_val,
                'p': p_val,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper
            })
        result_df = pd.DataFrame(rows)
        result_df.index = modx_legend_labels  # set row index to legend labels
        return result_df

    # If mod2 is provided, process each mod2 level and combine the results.
    if mod2 is not None:
        # Determine mod2 levels: use provided mod2_values if supplied; otherwise, use unique sorted values.
        if mod2_values is None:
            mod2_levels = sorted(data[mod2].unique())
        else:
            mod2_levels = mod2_values
        all_dfs = []
        for level in mod2_levels:
            subset = data[data[mod2] == level]
            df_level = process_data(subset)
            # Insert a column "at_mod2_value" with the level repeated for all rows.
            df_level.insert(1, "at_mod2_value", level)
            all_dfs.append(df_level)
        result_df = pd.concat(all_dfs, axis=0)
        return result_df
    else:
        return process_data(data)



