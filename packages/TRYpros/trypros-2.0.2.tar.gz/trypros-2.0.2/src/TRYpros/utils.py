# TITLE: Helper functions for TRYpros to use.
# Contributors: Gayathri Girish Nair (girishng@tcd.ie)

# IMPORTS
import datetime
import numpy as np
import pandas as pd
from pyproj import Transformer

def is_float(s):
    """ Checks if this string is that of a float or not.
    
    Keyword Arguments:
    s {str} -- String value.

    Returns:
    {bool} -- Whether this is a float string.
    """
    try: float(s)
    except: return False
    return True

def replace_month(val, with_m:bool):
    """ Replaces the month substring in the given string.

    val {str|nan} -- The string containing the month.
    with_m {bool} -- If True, the month substring is replaced with 'm'
                     else it gets replaced with the short representation
                     of the month.
    
    Returns:
    val {str|nan} -- Date string with month substring replaced.
    """
    # If date_str is not a "str" object then the same
    # value is returned without any processing.
    if val == val and type(val) == str:
        val = val.lower()
        for m in MONTHS:
            m_short = m[:3]
            val = val.replace(m, m_short)
        if with_m:
            for m in MONTHS_SHORT: 
                val = val.replace(m, "m")
    return val

def replace_season(val):
    """ Replaces any season name substrings in the given string with "s".
    
    Keyword Arguments:
    val {str|nan} -- The string containing the month.

    Returns:
    val {str|nan} -- String with the season name replaced by "s".
    """
    if val == val and type(val) == str: 
        val = val.lower()
        for s in SEASONS:
            val = val.replace(s, "s")
    return val

def get_form(val, num_placeholder='@', 
            rep_month=True, rep_season=True, make_lower=True):
    """ Gets general form of value with numbers replaced with '@'.
    
    Keyword Arguments:
    val {any} -- Value, the form of which, is to be returned.
    num_placeholder {str} -- The symbol that should replace 
                            numbers (Default '@').
    rep_month {bool} -- Whether or not to replace month substrings
                        in the val with character 'm'. (Default True)
    rep_season {bool} -- Whether or not to replace season substrings
                         in the val with character 's'. (Default True)
    make_lower {bool} -- Whether or not to make form all lowercase.
                         (Default True)
    
    Returns:
    val_form {str} -- General form of the given value.
    """
    # If value is NaN, return NaN.
    if val != val: return val
    val_str = str(val) if type(val) != str else val
    val_form = ""
    is_num = False
    num_points = 0
    for i in range(len(val_str)):
        c = val_str[i]
        if c.isnumeric():  # Character is a number.
            if not is_num:  # Previous character was not a number.
                is_num = True
                val_form += num_placeholder
        else:  # Character is not a number.
            if (c == "."):  # Character is a point.
                num_points += 1
            if not(
                c == 1 and  # This is the first point encountered
                is_num and  # since the previous character was a number.
                i + 1 < len(val_str) and  # There is a next character
                val_str[i+1].isnumeric()  # such that is is also a number.
            ):  # The above is not the case.
                is_num = False
                num_points = 0
                val_form += c
    if rep_month: 
        val_form = replace_month(val_form, with_m=True)
    if rep_season: 
        val_form = replace_season(val_form)
    if make_lower: 
        val_form = val_form.lower()
    val_form = val_form.strip()
    return val_form

def get_covariate_matches(df, search_str_list, print_matches):
    """  Returns DataIDs of matched covariates.

    Returns DataIDs of covariates whose names are matched
    with given search strings. Search characteristics
    involves an AND operation between words in each term and
    an OR operation between the terms themselves.

    Keyword Arguments:
    df {pd.DataFrame} -- Pandas data frame with data from TRY containing
                         columns "DataID" and "DataName".
    search_str_list {list} -- List of search strings.
    print_matches {bool} -- Whether or not matches are to be 
                            printed out.
    
    Returns:
    {list} -- List of DataIDs.
    """
    df_subset = df[["DataID", "DataName"]].dropna().drop_duplicates()
    ids = set([])
    for data_id, data_name in df_subset.values:
        name = str.lower(data_name)
        for search_str in search_str_list:
            all_words_present = True # All words in the same search term.
            for word in search_str.split():
                all_words_present &= (word in name)
            if all_words_present: ids.add(data_id)
    if print_matches:
        for data_id, data_name in df_subset[
            df_subset.DataID.isin(ids)].values:
            print(f"({data_id}) {data_name}")
    return list(ids)

def wgs84_m_utm_to_decimal_degrees(easting, northing, zone, hemisphere):
    """ Converts UTM values to decimal degrees.
    
    Converts X and Y values expressed in meters with the 
    coordinate reference system being UTM and  
    WGS84 reference datum to latitude and longitude values
    expressed in decimal degrees ([-180, 180], [-90, 90]).

    Keyword Arguments:
    easting {float} -- Longitude equivalent.
    northing {float} -- Latitude equivalent.
    zone {int} -- UTM Zone.
    hemisphere {str} -- Vertical geographic hemisphere (N/S).

    Returns:
    {pd.Series} -- Longitude and latitude.
    """
    latitude = np.nan
    longitude = np.nan
    if(
        easting == easting and 
        northing == northing and 
        zone == zone and 
        hemisphere == hemisphere
    ):
        # Build the UTM CRS string
        utm_crs = f"EPSG:326{zone}" if hemisphere == 'n' else f"EPSG:327{zone}"
        # Define the transformer (UTM to WGS84)
        transformer = Transformer.from_crs(utm_crs, "EPSG:4326", always_xy=True) 
        # Convert to decimal degrees (longitude, latitude)
        longitude, latitude = transformer.transform(easting, northing)
    return pd.Series([longitude, latitude])

def nztm_to_decimal_degrees(easting, northing):
    """ Converts NZTM to decimal degrees.
    
    Converts New Zealand Transverse Mercator (NZTM) 
    coordinates to decimal degrees ([-180, 180], [-90, 90]).
    
    Keyword Arguments:
    easting {float} -- Longitude equivalent.
    northing {float} -- Latitude equivalent.
    
    Returns:
    {pandas.Series} -- Longitude and latitude in decimal degrees.
    """
    latitude = np.nan
    longitude = np.nan
    if(easting == easting and northing == northing): # If not NaN.
        transformer = Transformer.from_crs(
            "EPSG:2193", # NZTM 
            "EPSG:4326", # WGS84 (decimal degrees)
            always_xy=True)
        longitude, latitude = transformer.transform(easting, northing)
    return pd.Series([longitude, latitude])

def value_std_latlon_deg(r):
    """ Converts non-standard decimal degrees into standard format.
    
    Given a longitude or latitude value expressed in
    degrees using any of many styles in the TRY DB,
    this function converts that style into the standard
    decimal degree format, which is a float value in
    the range -180 to 180 for longitude values and
    -90 to 90 for latitude values. Only those rows where
    OrigUnitStr == "decimal degrees" will be considered here.
    """
    value = r.OrigValueStr
    if value == value: # Not NaN
        value = str(value).lower()
        form = str(r.value_form).lower()
        unit = str(r.OrigUnitStr)

        # UTM values will be processed later by the 
        # value_transformation_latlon(...) function.
        # So for now, return UTM related values, as is.
        if unit == "decimal degrees": 
            # Standard formats.
            if form in ["@", "-@", "@.@", "-@.@"]: 
                return float(value)
    
            # Non Standard formats.
            # Standardize form's form.
            form = form.replace("n", "D")
            form = form.replace("e", "D")
            form = form.replace("w", "D")
            form = form.replace("deg", "d ")
            form = form.replace('sec', '"')
            form = form.replace("s", "D")
            form = form.replace("°", "d ")
            form = form.replace("''", "s ")
            form = form.replace("'", "m ")
            form = form.replace("´", "m ")
            form = form.replace('"', "s ")
            # Standardize value's form.
            value = value.replace("deg", "d")
            value = value.replace('sec', 's ')
            value = value.replace("°", "d ")
            value = value.replace("''", "s ")
            value = value.replace("'", "m ")
            value = value.replace("´", "m ")
            value = value.replace('"', "s ")

        # Proceed only if cardinal direction is available.
        if "D" in form:
            # Extract hemisphere, degrees, minutes, seconds.
            hemisphere = 1 # ["N", "E"]
            degrees = 0
            minutes = 0
            seconds = 0
            if str.upper(value[-1]) in ["S", "W"]: 
                hemisphere = -1
            value_split = [
                v.strip() for v in value.split(" ") 
                if v != " " and len(v.strip()) > 0
            ]
            for i in range(len(value_split)):
                v = value_split[i]
                if i == 0: # First value should always be degree.
                    v = v.replace("d", "")
                    if is_float(v):
                        degrees = float(v)
                    else: return np.nan
                else:
                    if "m" in v: # Value is minutes
                        v = v.replace("m", "")
                        if is_float(v):
                            minutes = float(v)
                    elif "s" in v:
                        v = v.replace("s", "")
                        if is_float(v):
                            minutes = float(v)
            decimal_degrees = hemisphere * (
                degrees + (minutes / 60) + (seconds / 3600))
            return decimal_degrees
    return value

def extract_year(date_str):
    """ Extracts year from given date string.

    Keyword Arguments:
    date_str {str} -- A string representation of date.
    
    Returns:
    {int} -- Year if the date form is a single matched date, 
             mean year if it is a date range date range, or NaN otherwise.
    """
    current_year = datetime.date.today().year

    if date_str == date_str: # No NaN.
        date_str = str(date_str)
        date_str = date_str.replace("(", "")
        date_str = date_str.replace(")", "")
        date_str = date_str.replace(",", "-")
        date_str = date_str.replace("/", "-")
        date_str = date_str.replace("&", "-")
        date_str = date_str.replace(".", "-")
        date_str = date_str.replace("t", "-")
        date_str = date_str.replace("?", "")
        date_str = date_str.replace(" ", "-")

        date_split = date_str.split("-")

        years = np.sort([
            y.strip() for y in date_split 
            if y.strip().isnumeric() and len(y.strip()) == 4
        ]).tolist()
        
        # If more than 1 year found, compute average.
        if len(years) > 0:
            year_start = int(years[0])
            year_end = int(years[-1])
            if (year_start <= current_year 
                and year_end <= current_year): # No future years.
                year_final = str(int(np.ceil((year_start + year_end) / 2)))
                return year_final
            
    # Any other situation is considered invalid. 
    return np.nan 

def validate_data_type(data_type):
    """ Raises exception if data_type is invalid.

    Keyword Arguments:
    data_type {str} -- String to check if valid.
    """
    global VALID_DATA_TYPES
    if not data_type in VALID_DATA_TYPES:
        raise Exception("Invalid data_type. "
                        + f"Expected one of {VALID_DATA_TYPES}.")
    
def validate_std_type(std_type):
    """ Raises exception if std_type is invalid.

    Keyword Arguments:
    std_type {str} -- String to check if valid.
    """
    global VALID_STD_TYPES
    if not std_type in VALID_STD_TYPES:
        raise Exception("Invalid std_type. "
                        + f"Expected one of {VALID_STD_TYPES}.")