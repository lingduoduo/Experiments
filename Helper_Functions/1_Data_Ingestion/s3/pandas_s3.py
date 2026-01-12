import numpy as np
import pandas as pd
import s3fs


def s3read(path: str, format: str) -> pd.DataFrame:
    fs = s3fs.S3FileSystem()
    paths = fs.glob(path)
    if len(paths) == 0:
        raise Exception(f'No files found on {path}')
    if format == 'parquet':
        rf = pd.read_parquet
    elif format == 'json':
        rf = pd.read_json
    elif format == 'csv':
        rf = pd.read_csv
    else:
        raise Exception(f'Invalid format `{format}`')
    dfs = [rf('s3://' + p) for p in paths]
    return pd.concat(dfs, ignore_index=True)


def s3write(df: pd.DataFrame, path: str, format: str) -> None:
    if format == 'parquet':
        wf = df.to_parquet
    elif format == 'json':
        wf = df.to_json
    elif format == 'csv':
        wf = df.to_csv
    else:
        raise Exception(f'Invalid format `{format}`')
    wf(path)


def get_dtypes(df: pd.DataFrame, drop_col=[]):
    name_of_col = list(df.columns)
    num_var_list = []
    str_var_list = name_of_col.copy()
    drop_var_list = drop_col.copy()

    for var in name_of_col:
        # check if column belongs to numeric type
        if (df[var].dtypes in (np.int, np.int64, np.uint, np.int32, np.float,
                               np.float64, np.float32, np.double)):
            str_var_list.remove(var)
            num_var_list.append(var)

        if min(df[var]) == max(df[var]):
            drop_var_list.append(var)

    # drop the omit column from list
    for var in drop_var_list:
        if var in str_var_list:
            str_var_list.remove(var)
        if var in num_var_list:
            num_var_list.remove(var)

    return str_var_list, num_var_list, drop_var_list
