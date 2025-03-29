from pathlib import Path

import pandas
import xarray

from cmip_ref_core.constraints import (
    AddSupplementaryDataset,
    RequireContiguousTimerange,
    RequireFacets,
    RequireOverlappingTimerange,
)
from cmip_ref_core.datasets import FacetFilter, SourceDatasetType
from cmip_ref_core.metrics import DataRequirement
from cmip_ref_metrics_esmvaltool.metrics.base import ESMValToolMetric
from cmip_ref_metrics_esmvaltool.recipe import dataframe_to_recipe
from cmip_ref_metrics_esmvaltool.types import OutputBundle, Recipe


class EquilibriumClimateSensitivity(ESMValToolMetric):
    """
    Calculate the global mean equilibrium climate sensitivity for a dataset.
    """

    name = "Equilibrium Climate Sensitivity"
    slug = "esmvaltool-equilibrium-climate-sensitivity"
    base_recipe = "recipe_ecs.yml"

    variables = (
        "rlut",
        "rsdt",
        "rsut",
        "tas",
    )
    experiments = (
        "abrupt-4xCO2",
        "piControl",
    )
    data_requirements = (
        DataRequirement(
            source_type=SourceDatasetType.CMIP6,
            filters=(
                FacetFilter(
                    facets={
                        "variable_id": variables,
                        "experiment_id": experiments,
                    },
                ),
            ),
            group_by=("source_id", "member_id", "grid_label"),
            constraints=(
                RequireFacets("variable_id", variables),
                RequireFacets("experiment_id", experiments),
                RequireContiguousTimerange(group_by=("instance_id",)),
                RequireOverlappingTimerange(group_by=("instance_id",)),
                AddSupplementaryDataset.from_defaults("areacella", SourceDatasetType.CMIP6),
            ),
        ),
    )

    @staticmethod
    def update_recipe(recipe: Recipe, input_files: pandas.DataFrame) -> None:
        """Update the recipe."""
        # Only run the diagnostic that computes ECS for a single model.
        recipe["diagnostics"] = {
            "cmip6": {
                "description": "Calculate ECS.",
                "variables": {
                    "tas": {
                        "preprocessor": "spatial_mean",
                    },
                    "rtnt": {
                        "preprocessor": "spatial_mean",
                        "derive": True,
                    },
                },
                "scripts": {
                    "ecs": {
                        "script": "climate_metrics/ecs.py",
                        "calculate_mmm": False,
                    },
                },
            },
        }

        # Prepare updated datasets section in recipe. It contains two
        # datasets, one for the "abrupt-4xCO2" and one for the "piControl"
        # experiment.
        recipe_variables = dataframe_to_recipe(input_files)
        recipe_variables = {k: v for k, v in recipe_variables.items() if k != "areacella"}

        # Select a timerange covered by all datasets.
        start_times, end_times = [], []
        for variable in recipe_variables.values():
            for dataset in variable["additional_datasets"]:
                start, end = dataset["timerange"].split("/")
                start_times.append(start)
                end_times.append(end)
        timerange = f"{max(start_times)}/{min(end_times)}"

        datasets = recipe_variables["tas"]["additional_datasets"]
        for dataset in datasets:
            dataset["timerange"] = timerange

        recipe["datasets"] = datasets

    @staticmethod
    def format_result(result_dir: Path) -> OutputBundle:
        """Format the result."""
        ecs_file = result_dir / "work/cmip6/ecs/ecs.nc"
        ecs = xarray.open_dataset(ecs_file)

        source_id = ecs.dataset.values[0].decode("utf-8")
        cmec_metric = {
            "DIMENSIONS": {
                "model": {source_id: {}},
                "region": {"global": {}},
                "metric": {"ecs": {}},
                "json_structure": [
                    "model",
                    "region",
                    "metric",
                ],
            },
            "RESULTS": {
                source_id: {"global": {"ecs": ecs.ecs.values[0]}},
            },
        }

        return cmec_metric
