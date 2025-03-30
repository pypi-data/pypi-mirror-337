import datetime
import itertools
import pickle

import altair as alt
import geojson
import matplotlib
import numpy as np
import pandas as pd
from flask import flash

from geo_activity_playground.core.activities import ActivityRepository
from geo_activity_playground.core.config import ConfigAccessor
from geo_activity_playground.core.coordinates import Bounds
from geo_activity_playground.core.tiles import compute_tile
from geo_activity_playground.core.tiles import get_tile_upper_left_lat_lon
from geo_activity_playground.explorer.grid_file import get_border_tiles
from geo_activity_playground.explorer.grid_file import logger
from geo_activity_playground.explorer.grid_file import make_explorer_rectangle
from geo_activity_playground.explorer.grid_file import make_explorer_tile
from geo_activity_playground.explorer.grid_file import make_grid_file_geojson
from geo_activity_playground.explorer.grid_file import make_grid_file_gpx
from geo_activity_playground.explorer.grid_file import make_grid_points
from geo_activity_playground.explorer.tile_visits import compute_tile_evolution
from geo_activity_playground.explorer.tile_visits import TileEvolutionState
from geo_activity_playground.explorer.tile_visits import TileVisitAccessor


alt.data_transformers.enable("vegafusion")


class ExplorerController:
    def __init__(
        self,
        repository: ActivityRepository,
        tile_visit_accessor: TileVisitAccessor,
        config_accessor: ConfigAccessor,
    ) -> None:
        self._repository = repository
        self._tile_visit_accessor = tile_visit_accessor
        self._config_accessor = config_accessor

    def enable_zoom_level(self, zoom: int) -> None:
        if 0 <= zoom <= 19:
            self._config_accessor().explorer_zoom_levels.append(zoom)
            self._config_accessor().explorer_zoom_levels.sort()
            self._config_accessor.save()
            compute_tile_evolution(self._tile_visit_accessor, self._config_accessor())
            flash(f"Enabled {zoom=} for explorer tiles.", category="success")
        else:
            flash(f"{zoom=} is not valid, must be between 0 and 19.", category="danger")

    def render(self, zoom: int) -> dict:
        if zoom not in self._config_accessor().explorer_zoom_levels:
            return {"zoom_level_not_generated": zoom}

        tile_evolution_states = self._tile_visit_accessor.tile_state["evolution_state"]
        tile_visits = self._tile_visit_accessor.tile_state["tile_visits"]
        tile_histories = self._tile_visit_accessor.tile_state["tile_history"]

        medians = tile_histories[zoom].median()
        median_lat, median_lon = get_tile_upper_left_lat_lon(
            medians["tile_x"], medians["tile_y"], zoom
        )

        explored = get_three_color_tiles(
            tile_visits[zoom], self._repository, tile_evolution_states[zoom], zoom
        )

        return {
            "center": {
                "latitude": median_lat,
                "longitude": median_lon,
                "bbox": (
                    bounding_box_for_biggest_cluster(
                        tile_evolution_states[zoom].clusters.values(), zoom
                    )
                    if len(tile_evolution_states[zoom].memberships) > 0
                    else {}
                ),
            },
            "explored": explored,
            "plot_tile_evolution": plot_tile_evolution(tile_histories[zoom]),
            "plot_cluster_evolution": plot_cluster_evolution(
                tile_evolution_states[zoom].cluster_evolution
            ),
            "plot_square_evolution": plot_square_evolution(
                tile_evolution_states[zoom].square_evolution
            ),
            "zoom": zoom,
        }

    def export_missing_tiles(self, zoom, north, east, south, west, suffix: str) -> str:
        x1, y1 = compute_tile(north, west, zoom)
        x2, y2 = compute_tile(south, east, zoom)
        tile_bounds = Bounds(x1, y1, x2 + 2, y2 + 2)

        tile_histories = self._tile_visit_accessor.tile_state["tile_history"]
        tiles = tile_histories[zoom]
        points = get_border_tiles(tiles, zoom, tile_bounds)
        if suffix == "geojson":
            return make_grid_file_geojson(points)
        elif suffix == "gpx":
            return make_grid_file_gpx(points)

    def export_explored_tiles(self, zoom, north, east, south, west, suffix: str) -> str:
        x1, y1 = compute_tile(north, west, zoom)
        x2, y2 = compute_tile(south, east, zoom)
        tile_bounds = Bounds(x1, y1, x2 + 2, y2 + 2)

        tile_visits = self._tile_visit_accessor.tile_state["tile_visits"]
        tiles = tile_visits[zoom]
        points = make_grid_points(
            (tile for tile in tiles.keys() if tile_bounds.contains(*tile)), zoom
        )
        if suffix == "geojson":
            return make_grid_file_geojson(points)
        elif suffix == "gpx":
            return make_grid_file_gpx(points)
        ...


def get_three_color_tiles(
    tile_visits: dict,
    repository: ActivityRepository,
    cluster_state: TileEvolutionState,
    zoom: int,
) -> str:
    logger.info("Generate data for explorer tile map …")
    today = datetime.date.today()
    cmap_first = matplotlib.colormaps["plasma"]
    cmap_last = matplotlib.colormaps["plasma"]
    tile_dict = {}
    for tile, tile_data in tile_visits.items():
        if not pd.isna(tile_data["first_time"]):
            first_age_days = (today - tile_data["first_time"].date()).days
            last_age_days = (today - tile_data["last_time"].date()).days
        else:
            first_age_days = 10000
            last_age_days = 10000
        tile_dict[tile] = {
            "first_activity_id": str(tile_data["first_id"]),
            "first_activity_name": repository.get_activity_by_id(tile_data["first_id"])[
                "name"
            ],
            "last_activity_id": str(tile_data["last_id"]),
            "last_activity_name": repository.get_activity_by_id(tile_data["last_id"])[
                "name"
            ],
            "first_age_days": first_age_days,
            "first_age_color": matplotlib.colors.to_hex(
                cmap_first(max(1 - first_age_days / (2 * 365), 0.0))
            ),
            "last_age_days": last_age_days,
            "last_age_color": matplotlib.colors.to_hex(
                cmap_last(max(1 - last_age_days / (2 * 365), 0.0))
            ),
            "cluster": False,
            "color": "#303030",
            "first_visit": tile_data["first_time"].date().isoformat(),
            "last_visit": tile_data["last_time"].date().isoformat(),
            "num_visits": len(tile_data["activity_ids"]),
            "square": False,
            "tile": f"({zoom}, {tile[0]}, {tile[1]})",
        }

    # Mark biggest square.
    if cluster_state.max_square_size:
        for x in range(
            cluster_state.square_x,
            cluster_state.square_x + cluster_state.max_square_size,
        ):
            for y in range(
                cluster_state.square_y,
                cluster_state.square_y + cluster_state.max_square_size,
            ):
                tile_dict[(x, y)]["square"] = True

    # Add cluster information.
    for members in cluster_state.clusters.values():
        for member in members:
            tile_dict[member]["this_cluster_size"] = len(members)
            tile_dict[member]["cluster"] = True
    if len(cluster_state.cluster_evolution) > 0:
        max_cluster_size = cluster_state.cluster_evolution["max_cluster_size"].iloc[-1]
    else:
        max_cluster_size = 0
    num_cluster_tiles = len(cluster_state.memberships)

    # Apply cluster colors.
    cluster_cmap = matplotlib.colormaps["tab10"]
    for color, members in zip(
        itertools.cycle(map(cluster_cmap, [0, 1, 2, 3, 4, 5, 6, 8, 9])),
        sorted(
            cluster_state.clusters.values(),
            key=lambda members: len(members),
            reverse=True,
        ),
    ):
        hex_color = matplotlib.colors.to_hex(color)
        for member in members:
            tile_dict[member]["color"] = hex_color

    if cluster_state.max_square_size:
        square_geojson = geojson.dumps(
            geojson.FeatureCollection(
                features=[
                    make_explorer_rectangle(
                        cluster_state.square_x,
                        cluster_state.square_y,
                        cluster_state.square_x + cluster_state.max_square_size,
                        cluster_state.square_y + cluster_state.max_square_size,
                        zoom,
                    )
                ]
            )
        )
    else:
        square_geojson = "{}"

    try:
        feature_collection = geojson.FeatureCollection(
            features=[
                make_explorer_tile(x, y, v, zoom) for (x, y), v in tile_dict.items()
            ]
        )
        explored_geojson = geojson.dumps(feature_collection)
    except TypeError as e:
        logger.error(f"Encountered TypeError while building GeoJSON: {e=}")
        logger.error(f"{tile_dict = }")
        raise

    result = {
        "explored_geojson": explored_geojson,
        "max_cluster_size": max_cluster_size,
        "num_cluster_tiles": num_cluster_tiles,
        "num_tiles": len(tile_dict),
        "square_size": cluster_state.max_square_size,
        "square_x": cluster_state.square_x,
        "square_y": cluster_state.square_y,
        "square_geojson": square_geojson,
    }
    return result


def bounding_box_for_biggest_cluster(
    clusters: list[list[tuple[int, int]]], zoom: int
) -> str:
    biggest_cluster = max(clusters, key=lambda members: len(members))
    min_x = min(x for x, y in biggest_cluster)
    max_x = max(x for x, y in biggest_cluster)
    min_y = min(y for x, y in biggest_cluster)
    max_y = max(y for x, y in biggest_cluster)
    lat_max, lon_min = get_tile_upper_left_lat_lon(min_x, min_y, zoom)
    lat_min, lon_max = get_tile_upper_left_lat_lon(max_x, max_y, zoom)
    return geojson.dumps(
        geojson.Feature(
            geometry=geojson.Polygon(
                [
                    [
                        (lon_min, lat_max),
                        (lon_max, lat_max),
                        (lon_max, lat_min),
                        (lon_min, lat_min),
                        (lon_min, lat_max),
                    ]
                ]
            ),
        )
    )


def plot_tile_evolution(tiles: pd.DataFrame) -> str:
    if len(tiles) == 0:
        return ""
    tiles["count"] = np.arange(1, len(tiles) + 1)
    return (
        alt.Chart(tiles, title="Tiles")
        .mark_line(interpolate="step-after")
        .encode(alt.X("time", title="Time"), alt.Y("count", title="Number of tiles"))
        .interactive(bind_y=False)
        .to_json(format="vega")
    )


def plot_cluster_evolution(cluster_evolution: pd.DataFrame) -> str:
    if len(cluster_evolution) == 0:
        return ""
    return (
        alt.Chart(cluster_evolution, title="Cluster")
        .mark_line(interpolate="step-after")
        .encode(
            alt.X("time", title="Time"),
            alt.Y("max_cluster_size", title="Maximum cluster size"),
        )
        .interactive(bind_y=False)
        .to_json(format="vega")
    )


def plot_square_evolution(square_evolution: pd.DataFrame) -> str:
    if len(square_evolution) == 0:
        return ""
    return (
        alt.Chart(square_evolution, title="Square")
        .mark_line(interpolate="step-after")
        .encode(
            alt.X("time", title="Time"),
            alt.Y("max_square_size", title="Maximum square size"),
        )
        .interactive(bind_y=False)
        .to_json(format="vega")
    )
