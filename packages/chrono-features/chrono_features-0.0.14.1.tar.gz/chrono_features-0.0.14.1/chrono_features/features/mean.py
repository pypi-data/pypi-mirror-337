import numba
import numpy as np

from chrono_features.features._base import (
    _FromNumbaFuncWithoutCalculatedForEachTS,
    _FromNumbaFuncWithoutCalculatedForEachTSPoint,
    StrategySelector,
)
from chrono_features.window_type import WindowBase, WindowType


@numba.njit  # pragma: no cover
def process_expanding_mean(feature: np.ndarray, lens: np.ndarray) -> np.ndarray:
    """Efficiently calculate cumulative mean for expanding windows using Numba optimization.

    This function maintains a running sum and count for each time series, resetting when a new
    time series begins (indicated by lens[i] == 1).

    Args:
        feature (np.ndarray): Array of feature values.
        lens (np.ndarray): Array of window lengths for each point.

    Returns:
        np.ndarray: Cumulative mean values for each expanding window.
    """
    result = np.empty(len(feature), dtype=np.float64)
    cumulative_sum = 0.0

    for i in range(len(lens)):
        current_len = lens[i]
        if current_len == 1:
            cumulative_sum = feature[i]
        else:
            cumulative_sum += feature[i]
        result[i] = cumulative_sum / current_len

    return result


@numba.njit  # pragma: no cover
def process_dynamic_mean(feature: np.ndarray, lens: np.ndarray, ts_lens: np.ndarray) -> np.ndarray:
    """Calculate mean for dynamic windows using prefix sum optimization.

    This function uses a prefix sum array to efficiently calculate means for
    variable-sized windows within each time series.

    Args:
        feature (np.ndarray): Array of feature values.
        lens (np.ndarray): Array of window lengths for each point.
        ts_lens (np.ndarray): Lengths of individual time series.

    Returns:
        np.ndarray: Mean values for each dynamic window.
    """
    result = np.empty(len(feature), dtype=np.float64)

    buffer_size = ts_lens.max() + 1
    prefix_sum_array = np.empty(buffer_size, dtype=np.float64)

    end = 0
    for i in range(len(ts_lens)):
        current_len = ts_lens[i]
        start = end
        end = start + current_len

        prefix_sum_array[0] = 0
        for j in range(start, end):
            prefix_sum_array[j - start + 1] = prefix_sum_array[j - start] + feature[j]

        for j in range(start, end):
            v = j - start + 1
            start_window = v - lens[j]
            if lens[j] == 0:
                result[j] = np.nan
            else:
                # If window length is larger than available points, use all available points
                start_window = max(start_window, 0)
                window_sum = prefix_sum_array[v] - prefix_sum_array[start_window]
                result[j] = window_sum / lens[j]

    return result


@numba.njit  # pragma: no cover
def process_rolling_mean(feature: np.ndarray, lens: np.ndarray, ts_lens: np.ndarray) -> np.ndarray:
    """Optimized processing for rolling windows mean calculation.

    For rolling windows, this implementation uses the same algorithm as dynamic windows
    since both can be efficiently calculated using prefix sums.

    Args:
        feature (np.ndarray): Array of feature values.
        lens (np.ndarray): Array of window lengths for each point.
        ts_lens (np.ndarray): Lengths of individual time series.

    Returns:
        np.ndarray: Mean values for each rolling window.
    """
    return process_dynamic_mean(feature, lens, ts_lens)


class MeanWithPrefixSumOptimization(_FromNumbaFuncWithoutCalculatedForEachTS):
    """Mean feature generator with optimized implementation using prefix sums.

    This class provides efficient mean calculations for different window types
    by using specialized prefix sum algorithms that avoid redundant calculations.
    """

    def __init__(
        self,
        *,
        columns: list[str] | str,
        window_types: list[str] | WindowType,
        out_column_names: list[str] | str | None = None,
    ) -> None:
        """Initialize the optimized mean feature generator.

        Args:
            columns: Columns to calculate mean for.
            window_types: Types of windows to use.
            out_column_names: Names for output columns.
        """
        super().__init__(
            columns=columns,
            window_types=window_types,
            out_column_names=out_column_names,
            func_name="mean",
        )

    @staticmethod
    def process_all_ts(
        feature: np.ndarray,
        ts_lens: np.ndarray,
        lens: np.ndarray,
        window_type: WindowBase,
    ) -> np.ndarray:
        """Process all time series using the appropriate method based on window type.

        Selects the optimal algorithm for each window type to maximize performance.

        Args:
            feature: Array of feature values.
            ts_lens: Lengths of individual time series.
            lens: Array of window lengths for each point.
            window_type: Type of window to use.

        Returns:
            np.ndarray: Mean values for each window.

        Raises:
            ValueError: If an unsupported window type is provided.
        """
        if isinstance(window_type, WindowType.EXPANDING):
            return process_expanding_mean(
                feature=feature,
                lens=lens,
            )
        if isinstance(window_type, WindowType.ROLLING):
            return process_rolling_mean(feature=feature, lens=lens, ts_lens=ts_lens)
        if isinstance(window_type, WindowType.DYNAMIC):
            return process_dynamic_mean(feature=feature, lens=lens, ts_lens=ts_lens)

        msg = "Unsupported window type"
        raise ValueError(msg)


class MeanWithoutOptimization(_FromNumbaFuncWithoutCalculatedForEachTSPoint):
    """Mean feature generator using the standard implementation.

    This class uses the base class's window processing logic with a simple mean function,
    which is less optimized but more straightforward than the prefix sum approach.
    """

    def __init__(
        self,
        *,
        columns: list[str] | str,
        window_types: list[WindowType] | WindowType,
        out_column_names: list[str] | str | None = None,
        func_name: str = "mean",
    ) -> None:
        """Initialize the standard mean feature generator.

        Args:
            columns: Columns to calculate mean for.
            window_types: Types of windows to use.
            out_column_names: Names for output columns.
            func_name: Name of the function for output column naming.
        """
        super().__init__(
            columns=columns,
            window_types=window_types,
            out_column_names=out_column_names,
            func_name=func_name,
        )

    @staticmethod
    @numba.njit  # pragma: no cover
    def _numba_func(xs: np.ndarray) -> np.ndarray:
        """Calculate the arithmetic mean of the input array.

        Args:
            xs: Input array.

        Returns:
            np.ndarray: Mean value.
        """
        return np.mean(xs)


class Mean(StrategySelector):
    """Factory class for creating mean feature generators with dynamic strategy selection.

    Provides a unified interface that dynamically selects the optimal implementation
    based on the window type. For expanding windows, it uses the optimized implementation,
    while for other window types it can use either optimized or standard implementation
    based on user preference.

    Examples:
        Basic usage with a single column and expanding window:

        >>> from chrono_features.features import Mean
        >>> from chrono_features.window_type import WindowType
        >>> from chrono_features.ts_dataset import TSDataset
        >>> import polars as pl
        >>>
        >>> # Create sample data
        >>> data = pl.DataFrame({
        ...     "id": [1, 1, 1, 2, 2],
        ...     "timestamp": [1, 2, 3, 1, 2],
        ...     "value": [10, 20, 30, 40, 50]
        ... })
        >>> dataset = TSDataset(data, id_column="id", timestamp_column="timestamp")
        >>>
        >>> # Create a mean feature generator for column 'value' with expanding window
        >>> mean_generator = Mean(
        ...     columns='value',
        ...     window_types=WindowType.EXPANDING(),
        ...     out_column_names='value_mean'
        ... )
        >>>
        >>> # Apply to dataset
        >>> transformed_dataset = mean_generator.transform(dataset)
        >>> print(transformed_dataset.data["value_mean"])
        shape: (5,)
        Series: 'value_mean' [f64]
        [
            10.0
            15.0
            20.0
            40.0
            45.0
        ]
    """

    def __init__(
        self,
        *,
        columns: list[str] | str,
        window_types: list[WindowType] | WindowType,
        out_column_names: list[str] | str | None = None,
        use_prefix_sum_optimization: bool = False,
    ) -> None:
        """Initialize the mean feature generator with dynamic strategy selection.

        Args:
            columns: Columns to calculate mean for.
            window_types: Types of windows to use.
            out_column_names: Names for output columns.
            use_prefix_sum_optimization: Whether to use the optimized implementation
                for non-expanding windows. Expanding windows always use optimization.
        """
        super().__init__(
            columns=columns,
            window_types=window_types,
            out_column_names=out_column_names,
        )
        self.use_prefix_sum_optimization = use_prefix_sum_optimization

    def _select_implementation_type(self, window_type: WindowBase) -> type:
        """Select the appropriate implementation class based on window type and optimization flag.

        Args:
            window_type: The window type to process.

        Returns:
            The appropriate implementation class.
        """
        # Use optimized implementation in these cases
        min_window_size_for_optimization = 50
        if any(
            [
                isinstance(window_type, WindowType.EXPANDING),
                isinstance(window_type, WindowType.ROLLING)
                and (self.use_prefix_sum_optimization or window_type.size > min_window_size_for_optimization),
                isinstance(window_type, WindowType.DYNAMIC) and self.use_prefix_sum_optimization,
            ],
        ):
            return MeanWithPrefixSumOptimization

        # Default to standard implementation
        return MeanWithoutOptimization
