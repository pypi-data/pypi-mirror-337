import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from shapely.geometry import Point
from pyproj import CRS



def df2shp(output_file, df, lat_name='lat', lon_name='lon', max_length=10):
    """
    Truncate DataFrame column names to a maximum length (default 10 characters) ensuring uniqueness,
    and convert the DataFrame to a shapefile.

    If the absolute longitude values exceed 190, adjust longitudes by subtracting 360 for those > 180.
    The function creates a GeoDataFrame using the specified longitude and latitude columns, sets the CRS
    to EPSG:4326, and writes the shapefile to the given output_file path.

    Parameters:
        output_file (str): Path where the shapefile will be saved.
        df (pd.DataFrame): Input DataFrame.
        lat_name (str): Name of the latitude column (default 'lat').
        lon_name (str): Name of the longitude column (default 'lon').
        max_length (int): Maximum length for truncated column names (default 10).

    Returns:
        None
    """
    # Truncate column names and ensure uniqueness
    new_columns = []
    for col in df.columns:
        truncated = col[:max_length]
        suffix = 1
        # Ensure the truncated name is unique among already processed columns.
        while truncated in new_columns:
            truncated = col[:max_length - len(str(suffix))] + str(suffix)
            suffix += 1
        new_columns.append(truncated)
    df.columns = new_columns

    # Adjust longitude values if necessary: if any absolute value exceeds 190, 
    # subtract 360 from values greater than 180.
    longs = df[lon_name].values
    if np.nanmax(np.abs(longs)) > 190:
        # Use boolean indexing for efficient adjustments.
        df.loc[df[lon_name] > 180, lon_name] -= 360

    # Create a geometry column using longitude and latitude
    df['geometry'] = [Point(lon, lat) for lon, lat in zip(df[lon_name], df[lat_name])]
    
    # Create GeoDataFrame and set CRS to EPSG:4326
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = CRS.from_epsg(4326)
    
    # Save the GeoDataFrame as a shapefile
    gdf.to_file(output_file)


def get_summary(r_arr, p_arr):
    """
    Summarize significant positive and negative results at various p-value thresholds.

    For each predefined p-value threshold, the function:
      - Filters the input arrays to include only valid values (p-values between 0 and 1, and non-NaN r_arr).
      - Copies r_arr and, for thresholds ≤ 0.1, replaces values with NaN if the corresponding p-value is ≥ threshold.
      - Counts the number of positive (r > 0) and negative (r < 0) values.
      - Computes percentages relative to both the total number of valid values and the significant subset.
      - Returns a DataFrame with:
          • 'Sig level': The p-value threshold (e.g., "p-value < 0.01") or 'Total' when the threshold is 1.01.
          • 'Pos count': Positive count and its percentage (of total valid values).
          • 'Neg count': Negative count and its percentage (of total valid values).
          • 'Pos/Neg ratio': The ratio of positive to negative percentages.
    
    Parameters:
        r_arr (np.ndarray): Array of test statistics (e.g., correlation coefficients).
        p_arr (np.ndarray): Array of corresponding p-values.
    
    Returns:
        pd.DataFrame: A summary table of significant results across thresholds.
    """
    # Filter out invalid values
    mask = ~np.isnan(r_arr) & (p_arr <= 1) & (p_arr >= 0)
    r_arr = r_arr[mask]
    p_arr = p_arr[mask]
    
    total = np.sum(mask)
    df_list = []
    for p_threshold in ['0.01', '0.05', '0.10', '1.01']:
        res = r_arr.copy()
        if float(p_threshold) <= 0.1:
            res[p_arr >= float(p_threshold)] = np.nan

        pos_num = np.sum(res > 0)
        neg_sum = np.sum(res < 0)
        total_sig = pos_num + neg_sum
        if total_sig == 0:
            total_sig = 1

        pos_ratio_sig = pos_num / total_sig * 100
        neg_ratio_sig = neg_sum / total_sig * 100
        pos_ratio_total = pos_num / total * 100
        neg_ratio_total = neg_sum / total * 100

        # Safely compute the positive/negative ratio to avoid division by zero
        if neg_ratio_sig == 0:
            ratio_str = "Inf" if pos_ratio_sig > 0 else "N/A"
        else:
            ratio_str = f"{pos_ratio_sig/neg_ratio_sig:.2f}"

        if p_threshold == '1.01':
            sig_level_label = 'Total'
        else:
            sig_level_label = f'p-value < {p_threshold}'

        new_row = pd.DataFrame({
            'Sig level': [sig_level_label],
            'Pos count': [f'{pos_num} ({pos_ratio_total:.2f}%)'],
            'Neg count': [f'{neg_sum} ({neg_ratio_total:.2f}%)'],
            'Pos/Neg ratio': [f"{pos_ratio_sig:.2f}% : {neg_ratio_sig:.2f}% = {ratio_str}"]
        })

        df_list.append(new_row)
    df = pd.concat(df_list).reset_index(drop=True)
    return df



def fit_ols_model(x, y, degree):
    """
    Fit a polynomial Ordinary Least Squares (OLS) regression model to the data.
    
    This function creates polynomial features of a specified degree from the input predictor x,
    fits an OLS regression model to predict the response variable y, and computes various model statistics.
    It returns a range of x values for plotting the fitted curve, predicted y values over that range,
    along with key statistics including the coefficient, p-value, intercept, R-squared value, the fitted model,
    and the confidence interval bounds for the predictions.
    
    Parameters:
        x (np.ndarray): 1D array of predictor values.
        y (np.ndarray): 1D array of response values.
        degree (int): Degree of the polynomial to fit.
        
    Returns:
        tuple: A tuple containing:
            - x_range (np.ndarray): A linearly spaced array covering the range of x values.
            - y_range (np.ndarray): Predicted y values corresponding to x_range.
            - coef (float): Coefficient of the first polynomial feature (slope component).
            - p_val (float): p-value for the first predictor coefficient.
            - intercept (float): Intercept of the fitted model.
            - r2 (float): R-squared value of the model fit.
            - model: The fitted OLS model object.
            - ci_low (np.ndarray): Lower bounds of the confidence intervals for predictions.
            - ci_high (np.ndarray): Upper bounds of the confidence intervals for predictions.
    
    Example:
        >>> import numpy as np
        >>> x = np.linspace(0, 10, 50)
        >>> y = 3 * x + np.random.randn(50)
        >>> x_range, y_range, coef, p_val, intercept, r2, model, ci_low, ci_high = fit_ols_model(x, y, degree=1)
    """
    # Fit the polynomial transformation of x
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x.reshape(-1, 1))
    
    # Add a constant term and fit the OLS model
    X = sm.add_constant(x_poly)
    model = sm.OLS(y, X).fit()
    
    # Extract key statistics from the model
    r2 = model.rsquared
    p_val = model.pvalues[1]
    coef = model.params[1]
    intercept = model.params[0]
    
    # Generate a range of x values for plotting predictions
    x_range = np.linspace(x.min(), x.max(), 100)
    x_poly_range = poly.fit_transform(x_range.reshape(-1, 1))
    
    # Get predicted y values and confidence intervals
    y_range = model.predict(sm.add_constant(x_poly_range))
    predictions = model.get_prediction(sm.add_constant(x_poly_range))
    ci_low, ci_high = predictions.conf_int().T  # confidence intervals
    
    return x_range, y_range, coef, p_val, intercept, r2, model, ci_low, ci_high



def remove_outliers(data, threshold=3):
    """
    Function to remove outliers from a given data array.

    Parameters:
    - data: One-dimensional or multi-dimensional data array, can be a pandas Series, NumPy array, or xarray.DataArray.
    - threshold: Threshold for outliers in terms of the data standard deviation. Default is 3.

    Returns:
    - Processed data array with outliers beyond the threshold replaced with NaN.

    Note:
    - For NumPy arrays, the function directly modifies the input array, replacing outliers with NaN.
    - For xarray.DataArray, a new array is generated where outliers are replaced with NaN, and the original array remains unaffected.
    - If the input is a pandas Series, a new Series is generated with outliers replaced with NaN, and the original Series remains unaffected.

    """
    
    # Calculate the standard deviation, mean, and center the data
    data_std = np.nanstd(data)
    data_mean = np.nanmean(data)
    data_centered = np.abs(data - data_mean)
    
    # Remove outliers based on the threshold and data type
    if isinstance(data, xr.DataArray):
        data = xr.where(data_centered > threshold*data_std, np.nan, data)
    else:
        data[data_centered > threshold*data_std] = np.nan

    return data


