import json
from scipy.stats import rankdata
from typing import List, Dict, Any, Optional, Union, Tuple
import numpy as np
import pandas as pd
from pydantic import BaseModel

from dantArrays import DantArray, index_field
from maic import Maic
from maic.models import EntityListModel
from birra.birra import birra
from ma_utils.rank_array_adapter import convert_rank_data, RankShape


class RankListMetadata(BaseModel):
    """
    Metadata for a single list within a rank-oriented DantArray.

    Fields:
    -------
    name : str
        Name of the list. Computed if none provided.
    category : str
        Category or grouping tag for the list.
    ranked : bool
        Whether the list is ranked.
    description : str, optional
        Description of the list.
    unique_items : int
        Count of valid (non-null) items in the list slice.
    """

    name: str = index_field("list_")
    category: str = index_field("category_")
    ranked: bool = True


class RankListAdapter:
    """
    Adapter that manages a DantArray of rank data (using RankListMetadata) and
    provides methods to run MAIC, BIRRA, and SR-Agreement analyses.

    Parameters:
    -----------
    data : np.ndarray, pd.DataFrame, or DantArray
        Rank data or an existing DantArray. If a raw array, a DantArray is created.
    categories : list of str, optional
        Categories for each list. Must match the number of lists.
    list_names : list of str, optional
        Names for each list. Must match the number of lists.
    shape : RankShape, default=RankShape.LISTCOL_RANKROW
        Format describing whether lists are rows or columns, etc.
    """

    def __init__(
        self,
        data: Union[np.ndarray, pd.DataFrame, DantArray],
        categories: Optional[List[str]] = None,
        list_names: Optional[List[str]] = None,
        shape: RankShape = RankShape.LISTCOL_RANKROW,
    ):
        if isinstance(data, DantArray):
            if data.metadata_class != RankListMetadata:
                raise ValueError("DantArray must use RankListMetadata")
            self.dant_array = data
        else:
            if isinstance(data, pd.DataFrame):
                array_data = data.values
                self._df_columns = data.columns.tolist()
                self._df_index = data.index.tolist()
            else:
                array_data = np.asarray(data)
                self._df_columns = None
                self._df_index = None

            if shape == RankShape.LISTCOL_RANKROW:
                major_axis = 1
            elif shape == RankShape.LISTROW_RANKCOL:
                major_axis = 0
            else:
                raise ValueError(
                    f"Initial data must be in LISTCOL_RANKROW or LISTROW_RANKCOL, got {shape}"
                )

            self.dant_array = DantArray(
                array_data, RankListMetadata, major_axis=major_axis
            )

        n_lists = self.dant_array.shape[self.dant_array.major_axis]

        if categories:
            if len(categories) != n_lists:
                raise ValueError(
                    f"Expected {n_lists} categories, got {len(categories)}"
                )
            for i, category in enumerate(categories):
                self.dant_array.meta(i).category = category

        if list_names:
            if len(list_names) != n_lists:
                raise ValueError(
                    f"Expected {n_lists} list names, got {len(list_names)}"
                )
            for i, name in enumerate(list_names):
                self.dant_array.meta(i).name = name

    def get_shape(self) -> Tuple[int, int]:
        """
        Return the shape of the underlying data array.
        """
        return self.dant_array.shape

    def get_data_as_shape(self, shape: RankShape) -> np.ndarray:
        """
        Convert and obtain data in the given rank shape.

        Parameters:
        -----------
        shape : RankShape
            Desired shape enum value.

        Returns:
        --------
        np.ndarray
            Data in the specified shape format.
        """
        if self.dant_array.major_axis == 0:
            current_shape = RankShape.LISTROW_RANKCOL
        else:
            current_shape = RankShape.LISTCOL_RANKROW

        if current_shape == shape:
            return self.dant_array.data.copy()

        return convert_rank_data(
            self.dant_array.data, from_shape=current_shape, to_shape=shape
        ).data

    def run_maic(
        self,
        threshold: float = 0.01,
        max_iterations: int = 100,
        output_folder: Optional[str] = None,
        plot: bool = False,
    ) -> Dict[str, Any]:
        """
        Run MAIC analysis using the data in this adapter.

        Parameters:
        -----------
        threshold : float
            Convergence threshold for MAIC.
        max_iterations : int
            Maximum number of iterations.
        output_folder : str, optional
            Folder to save outputs (logs, images). If None, nothing is saved.
        plot : bool
            Whether to plot distributions using a CrossValidationPlotter.

        Returns:
        --------
        dict
            The results of the analysis, sorted by descending MAIC score

            Results are returned as a list of score dictionaries, each containing the following keys:
            'name': the entity's name as recorded in the entity lists
            'maic_score': the final score assigned to this entity
            'contributors': a comma-separate list indicating the "winning" list for each category
            Additionally, the name of each list is added as a key with the value equal to that list's contriubting score.
        """
        entity_list_models = []
        n_lists = self.dant_array.shape[self.dant_array.major_axis]

        for i in range(n_lists):
            list_data = self.dant_array.get_slice(i)
            metadata = self.dant_array.get_metadata(i, create_default=True)
            if metadata is None:
                raise RuntimeError(f"Failed to get metadata for list {i}")

            valid_items = [
                item
                for item in list_data
                if item is not None
                and str(item).strip() != ""
                and not pd.isna(item)
            ]
            string_items = [str(item) for item in valid_items]
            elm = EntityListModel(
                name=metadata.name,
                category=metadata.category,
                ranked=metadata.ranked,
                entities=string_items,
            )
            entity_list_models.append(elm)

        maic = Maic(
            modellist=entity_list_models,
            threshold=threshold,
            maxiterations=max_iterations,
        )

        if output_folder:
            maic.output_folder = output_folder
            if plot:
                maic.add_plotter()

        maic.run(dump_result=(output_folder is not None))

        results = maic.sorted_results
        return results

    def _prepare_numeric_input_and_mapping(
        self,
    ) -> Tuple[np.ndarray, Dict[Any, int], Dict[int, Any], RankShape]:
        """
        Create numeric representations from items in DantArray. Ensures a
        consistent item_to_id map and identifies the current shape.

        Returns:
        --------
        (numeric_array, item_to_id, id_to_item, current_shape)
        """
        original_data = self.dant_array.data
        unique_original_items_set = set()
        flat_data = original_data.flat
        for val in flat_data:
            if pd.notna(val) and str(val).strip() != "":
                unique_original_items_set.add(val)

        if not unique_original_items_set:
            if pd.isna(original_data).all() or (original_data == "").all():
                raise ValueError(
                    "DantArray data is all NaN or empty; cannot proceed."
                )
            else:
                raise ValueError("Could not extract unique items.")

        try:
            sorted_original_items = sorted(list(unique_original_items_set))
        except TypeError:
            print(
                "Warning: Mixed item types. Converting to string for sorting."
            )
            sorted_original_items = sorted(
                [str(item) for item in unique_original_items_set]
            )

        item_to_id = {item: i for i, item in enumerate(sorted_original_items)}
        id_to_item = {i: item for item, i in item_to_id.items()}
        numeric_input_array = np.full_like(original_data, np.nan, dtype=float)

        for index, original_item in np.ndenumerate(original_data):
            if pd.notna(original_item) and str(original_item).strip() != "":
                internal_id = item_to_id.get(original_item)
                if internal_id is not None:
                    numeric_input_array[index] = float(internal_id)

        if self.dant_array.major_axis == 0:
            current_shape = RankShape.LISTROW_RANKCOL
        else:
            current_shape = RankShape.LISTCOL_RANKROW

        return numeric_input_array, id_to_item, current_shape

    def run_birra(
        self,
        prior: float = 0.05,
        n_bins: int = 50,
        n_iter: int = 10,
        return_all: bool = False,
        cor_stop: Optional[float] = 0.999,
        impute_method: Optional[str] = "random",
    ) -> Dict[str, Any]:
        """
        Run BIRRA analysis on the rank data.

        BIRRA parameters:
        ----------------
        prior : float
            Prior probability for an item to be included.
        n_bins : int
            Number of bins for distribution analysis.
        n_iter : int
            Iterations for BIRRA loop.
        return_all : bool
            Whether to return intermediate data.
        cor_stop : float, optional
            Stop correlation threshold for convergence.
        impute_method : str, optional
            Method for handling NaNs. E.g. 'random' or None.

        Returns:
        --------
        dict
            Contains final ranks and optional intermediate data.
        """
        try:
            (
                numeric_input_array,
                numeric_id_to_original_item,
                current_shape,
            ) = self._prepare_numeric_input_and_mapping()

            rank_data_for_birra = convert_rank_data(
                numeric_input_array,
                from_shape=current_shape,
                to_shape=RankShape.LISTCOL_ITEMROW,
                na_value=np.nan,
            )
            birra_input_numeric = rank_data_for_birra.data
            adapter_id_map = getattr(
                rank_data_for_birra, "id_to_index_mapping", None
            )
            num_unique_items = len(numeric_id_to_original_item)

            if birra_input_numeric.shape[0] != num_unique_items:
                raise ValueError("Mismatch between items and row dimension.")
            if not adapter_id_map:
                raise ValueError("No id_to_index_mapping in rank data result.")

            index_to_internal_id = {v: k for k, v in adapter_id_map.items()}
        except Exception as e:
            print(f"Error preparing data for BIRRA: {e}")
            raise

        try:
            birra_result = birra(
                data=birra_input_numeric,
                prior=prior,
                n_bins=n_bins,
                n_iter=n_iter,
                return_all=return_all,
                cor_stop=cor_stop,
                impute_method=impute_method,
            )
        except Exception as e:
            print(f"Error during BIRRA execution: {e}")
            raise

        results = {}
        final_ranks = (
            birra_result if not return_all else birra_result.get("result")
        )
        if not isinstance(final_ranks, np.ndarray) or final_ranks.ndim != 1:
            raise ValueError("BIRRA returned invalid rank results.")

        rankings = []
        birra_idx_to_original_item = {}
        for birra_idx in range(len(final_ranks)):
            internal_id = index_to_internal_id.get(birra_idx)
            original_item = None
            if internal_id is not None:
                original_item = numeric_id_to_original_item.get(internal_id)
            if original_item is None:
                original_item = f"UnknownItem_{birra_idx}"
                print(f"Warning: Could not map BIRRA index {birra_idx}.")
            birra_idx_to_original_item[birra_idx] = original_item
            rank_value = final_ranks[birra_idx]
            rankings.append((original_item, rank_value))
        rankings.sort(key=lambda x: x[1])

        if return_all:
            results = {
                "ranks": final_ranks,
                "sorted_items": rankings,
                "data": birra_result.get("data"),
                "bayes_factors": birra_result.get("BF"),
                "imputed_input": birra_result.get("imputed_input"),
                "item_mapping": birra_idx_to_original_item,
            }
        else:
            results = {
                "ranks": final_ranks,
                "sorted_items": rankings,
                "item_mapping": birra_idx_to_original_item,
            }

        return results


def get_gene_labels(n_genes: int) -> List[str]:
    """Get a sample of random gene names from a JSON file."""
    with open("all-human-genes.json", "r") as f:
        all_genes = json.load(f)

    # Ensure uniqueness and convert to list
    gene_pool = list(set(all_genes))
    return np.random.choice(gene_pool, size=n_genes, replace=False).tolist()


def generate_effect_df(
    gene_list: List[str], mu: float = 0, sigma: float = 1, noise: bool = False
) -> pd.DataFrame:
    """
    Generate effect sizes for genes using log-normal distribution and provide them in a ranked DataFrame.

    Args:
        gene_list: List of gene identifiers
        mu: Log-normal mu parameter
        sigma: Log-normal sigma parameter
        noise: If True, generate random effect sizes from normal distribution

    Returns:
        DataFrame with gene names, effect sizes, and true ranks.
        N.B.: Sorted by true rank, so *the indices of this df = true ranks*.
    """
    n_genes = len(gene_list)

    if noise:
        effect_size = np.random.normal(0, 1, size=n_genes)
    else:
        effect_size = np.random.lognormal(mu, sigma / 2, size=n_genes)

    df = pd.DataFrame({"gene": gene_list, "effect_size": effect_size})
    df["true_rank"] = rankdata(-df["effect_size"], method="average")

    df = df.sort_values(by="true_rank").reset_index(drop=True)

    return df


def study_rank(
    df: pd.DataFrame, n_studies: int, noise_sd: float = 1
) -> np.ndarray:
    """
    Create ranked matrices by adding noise to effect sizes.

    Args:
        df: DataFrame with genes and effect sizes
        n_studies: Number of study columns to generate
        noise_sd: Standard deviation of noise to add

    Returns:
        NumPy array of ranks with shape (n_genes, n_studies)
    """
    error_matrix = np.random.normal(0, noise_sd, size=(len(df), n_studies))
    measured_effects = error_matrix + df["effect_size"].values.reshape(-1, 1)

    ranked_effects = np.zeros_like(measured_effects)
    for i in range(n_studies):
        ranked_effects[:, i] = rankdata(-measured_effects[:, i])

    return ranked_effects

