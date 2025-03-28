from datetime import datetime
from typing import cast

import numpy as np
import pandas as pd
from typing_extensions import Unpack

from finter.backtest.config.simulator import SimulatorInputConfig
from finter.backtest.config.templates import (
    AVAILABLE_MARKETS,
    MarketTemplates,
)
from finter.data.data_handler.main import DataHandler
from finter.log import PromtailLogger


class Simulator:
    _data_handler_instance = None
    _cached_start = None
    _cached_end = None

    @classmethod
    def _get_cached_data_handler(cls, _handler_cls, **kwargs):
        start = kwargs.get("start")
        end = kwargs.get("end")

        if (
            cls._data_handler_instance is None
            or start != cls._cached_start
            or end != cls._cached_end
            or not isinstance(cls._data_handler_instance, _handler_cls)
        ):
            cls._data_handler_instance = _handler_cls(**kwargs)
            cls._cached_start = start
            cls._cached_end = end
        return cls._data_handler_instance

    def __init__(
        self,
        market_type: AVAILABLE_MARKETS,
        start: int = 20000101,
        end: int = int(datetime.now().strftime("%Y%m%d")),
        _handler_cls=DataHandler,
    ):
        self.market_type = market_type

        self.data_handler = self._get_cached_data_handler(
            _handler_cls=_handler_cls,
            start=start,
            end=end,
            cache_timeout=300,
        )

        self.builder = MarketTemplates.create_simulator(
            cast(
                AVAILABLE_MARKETS,
                self.market_type,
            )
        )
        self.set_market_builder()

    def set_market_builder(self):
        price = (
            self.data_handler.universe(self.market_type)
            .price(adj=False)
            .dropna(how="all")
        )
        if self.market_type in ("us_stock", "us_etf", "id_bond"):
            price = price.ffill()
        elif self.market_type == "crypto_spot_binance":
            price = price.fillna(np.nan).applymap(float)

        adjustment_ratio = self.data_handler.universe(
            self.market_type
        ).adjustment_ratio()

        self.builder.update_data(price=price, adjustment_ratio=adjustment_ratio)

    def post_init(self):
        if self.use_drip:
            self.builder.update_data(
                dividend_ratio=self.data_handler.universe(self.market_type)
                .dividend_factor()
                .dropna(how="all"),
            )

        if self.use_currency:
            base_currency = MarketTemplates.get_config_value(
                cast(AVAILABLE_MARKETS, self.market_type),
                "base_currency",
            )
            if base_currency != self.use_currency:
                currency_pair = f"{base_currency}{self.use_currency}"
                inverse_pair = f"{self.use_currency}{base_currency}"

                currency_data = self.data_handler.common.currency()
                if currency_pair in currency_data.columns:
                    exchange_rate = currency_data[[currency_pair]].dropna()
                elif inverse_pair in currency_data.columns:
                    exchange_rate = (1 / currency_data[[inverse_pair]]).dropna()
                else:
                    raise ValueError(
                        f"No exchange rate found for conversion from {base_currency} to {self.use_currency}"
                    )
            else:
                return

            if exchange_rate is not None:
                self.builder.update_data(
                    exchange_rate=exchange_rate,
                )
            else:
                raise ValueError(f"Unsupported currency: {self.use_currency}")
        if (
            self.use_volume_capacity_ratio is not None
            and (
                self.use_volume_capacity_ratio > 0
                and self.use_volume_capacity_ratio <= 1
            )
        ) or (self.use_target_volume_limit is not None):
            self.builder.update_data(
                volume=self.data_handler.universe(self.market_type).volume(),
            )

    def run(self, position: pd.DataFrame, **kwargs: Unpack[SimulatorInputConfig]):
        self.use_currency = kwargs.pop("currency", None)

        self.use_volume_capacity_ratio = kwargs.get(
            "volume_capacity_ratio",
            getattr(self.builder.trade, "volume_capacity_ratio", None),
        )
        self.use_target_volume_limit = kwargs.get(
            "target_volume_limit_args",
            getattr(self.builder.trade, "target_volume_limit_args", None),
        )
        self.use_drip = kwargs.get(
            "drip",
            getattr(self.builder.execution, "drip", None),
        )

        self.post_init()

        self.builder.update(**kwargs)

        position.iloc[:, :] = np.trunc(position.values / 1e4) * 1e4

        simulator = self.builder.build(position)

        ### run with log
        try:
            simulator.run()
            status = "success"
        except Exception as e:
            status = "error"
            raise e
        finally:
            PromtailLogger.send_log(
                level="INFO",
                message=f"{self.market_type}",
                service="finterlabs-jupyterhub",
                user_id=PromtailLogger.get_user_info(),
                operation="simulation",
                status=status,
            )

        return simulator
