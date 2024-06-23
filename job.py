import datetime
from abc import abstractmethod, ABC
from typing import List

from ent.base_ds import BaseConfig, BacktestObject
from ent.service import DataProviderService, VisualizingService, StrategyService, GridService, \
    GroupByCorrelationService, GroupByCorrelationService2
from ent.trading_strategy import Strategy
from ent.utils import generate_file_path


class Job(ABC):

    @abstractmethod
    def execute(self):
        pass


class GroupByCorrelationPerStockJob(Job):

    def __init__(self, config: BaseConfig):
        self.config = config

    def execute(self):

        data = DataProviderService(self.config).read_5min_data()
        strategy_service = StrategyService(Strategy(sl=self.config.stop_loss, depth=self.config.depth))

        data_as_df = data.get_pandas_df()
        data_as_td = data.get_data_as_trading_days()

        test_results = {}

        for trading_date, trading_day in data_as_td.items():
            if trading_date in data_as_df.index:

                trade_test_result = strategy_service.test_strategy(trading_day)

                grid = GridService(
                    self.config.type_vol, self.config.depth, self.config.coordinates_basis, data_as_df.loc[trading_date]
                ).get()

                test_results[trading_date] = BacktestObject(trading_date, grid, trade_test_result)
            else:
                print(f"Trading date {trading_date} not found in DataFrame index")

        df = GroupByCorrelationService2().group(test_results)
        curr_time = datetime.datetime.now()
        output_folder = generate_file_path('output')
        df.to_csv(f'{output_folder}/{curr_time}.csv', index=False)


class VisualiseJob(Job):

    def __init__(self, config: BaseConfig, days: List[str]):
        self.config = config
        self.days = days

    def execute(self):
        data = DataProviderService(self.config).read_5min_data().get_data_as_trading_days()
        VisualizingService(data).visualise_days(self.days)
