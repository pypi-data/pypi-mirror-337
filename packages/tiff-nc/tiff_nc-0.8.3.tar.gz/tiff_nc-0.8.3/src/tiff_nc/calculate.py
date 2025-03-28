import inspect
from typing import Callable,Mapping,Any,Literal
import xarray as xr
def get_func_args(func:Callable) -> dict:
    """
    Returns a list of arguments for a function.
    """
    return {name: param.annotation.__name__ 
            for name,param in inspect.signature(func).parameters.items()}
    
    
def calculate_by_dimension(
    func:Callable,
    ds: xr.Dataset,
    dim:str|list[str]="valid_time",
    kwargs:Mapping[str,Any]|None=None,
    chunks:dict[str,int]|None=None,
    var_name:str="variable",
    ):
    """
    沿一定维度计算数据集的函数

    Args:
        func (Callable): 计算函数(参数必须包括numpy.ndarray)[支持numba.njit加速计算]
        ds (xr.Dataset): 包含地理信息数据集
        dim (str|list[str], optional): 维度名称. Defaults to "valid_time".
        kwargs (Mapping[str,Any] | None, optional): func内除numpy.ndarray以外的参数. Defaults to None.
        chunks (dict[str,int] | None, optional): 分块大小. Defaults to None.
        var_name (str, optional): 数据变量名. Defaults to "variable".
    """
    dims = [[d] for d in ([dim] if isinstance(dim, str) else dim) if d in ds.dims]
    if not dims:
        raise ValueError(f"维度{dim}不存在" if isinstance(dim, str) else "维度不存在")
    if 'ndarray' not in get_func_args(func).values():
        raise ValueError("func必须包含numpy.ndarray参数")
    invalid_chunks = {dim_name: chunks[dim_name] for dim_name in chunks if dim_name in ds.sizes and chunks[dim_name] > ds.sizes[dim_name]}
    if invalid_chunks:
        raise ValueError(f"以下维度的分块大小超出限制: {invalid_chunks}")
    # 将dim设置为-1，表示不进行分块
    ds.chunk({
        dim: -1,
        **{
            dim_name: chunks[dim_name] for dim_name in chunks if dim_name != dim
        }
    })
    return xr.apply_ufunc(
        func,
        ds[var_name],
        input_core_dims=dims,
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        kwargs=kwargs,
    )
    
    
def calculate_by_time(
    func:Callable,
    ds:xr.Dataset,
    time_dim:str="valid_time",
    kwargs:Mapping[str,Any]|None=None,
    chunks:dict[str,int]|None=None,
    var_name:str="variable",
    time_selection:Literal['YE', 'ME', 'QS-DEC','QS-JAN'] = 'YE'
    ):
    """
    按时间维度计算数据集的函数,可指定时间粒度

    Args:
        func (Callable): func(ndarray,**kwargs)
        ds (xr.Dataset): 包含地理信息数据集
        time_dim (str, optional):   时间维度名称. Defaults to "valid_time".
        kwargs (Mapping[str,Any] | None, optional): func的额外参数. Defaults to None.
        chunks (dict[str,int] | None, optional): 分块大小. Defaults to None.
        var_name (str, optional): 数据变量名. Defaults to "variable".
        time_selection (Literal['YE', 'ME', 'QS-DEC'(季节),'QS-JAN'], optional): 时间粒度. Defaults to 'YE'.
    """ # 调试信息
    if time_dim not in ds.dims:
        raise ValueError(f"维度{time_dim}不存在")
    if 'ndarray' not in get_func_args(func).values():
        raise ValueError("func必须包含numpy.ndarray参数")
    ds = ds.chunk({
        time_dim: -1,
        **{
            dim_name: chunks[dim_name] for dim_name in chunks if dim_name != time_dim
        }
    })
    return ds[var_name].resample({
        time_dim: time_selection
    }).apply(lambda x: xr.apply_ufunc(
        func,
        x,
        input_core_dims=[[time_dim]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        kwargs=kwargs,
        ) )