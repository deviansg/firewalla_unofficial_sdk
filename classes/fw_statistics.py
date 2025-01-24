from typing import Literal, TypeAlias
from classes.base import BaseFirewallaSDK

FlowType: TypeAlias = Literal["topBoxesByBlockedFlows", "topBoxesBySecurityAlarms", "topRegionsByBlockedFlows"]
StatsParams: TypeAlias = Literal["group", "limit"]

class Statistics(BaseFirewallaSDK):   
    def get_stats(self, params: StatsParams, type: FlowType=None):
        query_params = ["group", "limit"]
        for key, value in params.items():
            if key in query_params:
                params[key] = value
        return self._get("stats", params=params, identifier=type)
    
    def get_simple_stats(self, params: StatsParams):
        query_params = ["group"]
        for key, value in params.items():
            if key in query_params:
                params[key] = value
        return self._get("stats/simple", params=params)