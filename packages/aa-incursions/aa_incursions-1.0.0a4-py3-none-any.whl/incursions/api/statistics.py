from ninja import NinjaAPI, Schema


class StatsResponse(Schema):
    fleet_seconds_by_hull_by_month: dict[str, dict[str, float]]
    xes_by_hull_by_month: dict[str, dict[str, float]]
    fleet_seconds_by_month: dict[str, float]
    pilots_by_month: dict[str, float]
    xes_by_hull_28d: dict[str, float]
    fleet_seconds_by_hull_28d: dict[str, float]
    x_vs_time_by_hull_28d: dict[str, dict[str, float]]
    time_spent_in_fleet_by_month: dict[str, dict[str, float]]


api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    StatisticsAPIEndpoints(api)


class StatisticsAPIEndpoints:

    tags = ["Statistics"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/stats", response={200: StatsResponse, 403: dict}, tags=self.tags)
        def statistics(request):
            if not request.user.has_perm("incursions.stats_view"):
                return 403, {"error": "Permission denied"}

            return StatsResponse()
            # return StatsResponse(
            #     fleet_seconds_by_hull_by_month=fleet_seconds_by_hull_by_month,
            #     xes_by_hull_by_month=xes_by_hull_by_month,
            #     fleet_seconds_by_month=fleet_seconds_by_month,
            #     pilots_by_month=pilots_by_month,
            #     xes_by_hull_28d=xes_by_hull_28d,
            #     fleet_seconds_by_hull_28d=fleet_seconds_by_hull_28d,
            #     x_vs_time_by_hull_28d=x_vs_time_by_hull_28d,
            #     time_spent_in_fleet_by_month=time_spent_in_fleet_by_month
            # )
