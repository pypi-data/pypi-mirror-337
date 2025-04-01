from .base_pdt_strategy import BasePDTStrategy
from .models import PDTContext, PDTDecision
from ..models import OrderSide, PositionSide


class YoloStrategy(BasePDTStrategy):
    """YOLO strategy - open positions without PDT constraints

    This strategy ignores PDT rules for opening positions but prevents same-day closes
    to avoid day trade counts. Very risky as positions can't be closed same day even
    if they move against you.
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        """Disabled constructor - use YoloStrategy.create() instead."""
        raise TypeError("Use YoloStrategy.create() instead to create a new YoloStrategy")

    def evaluate_order(self, context: PDTContext) -> PDTDecision:
        """
        Evaluate a proposed order for the YOLO strategy.

        This strategy allows unlimited opening of positions but prevents
        closing any position that was opened today to avoid day trade counts.

        Args:
            context: PDT context with all relevant information

        Returns:
            PDTDecision with the evaluation result
        """
        rolling_day_trade_count = context.rolling_day_trade_count
        if (
            context.position is None
            or (context.position.side == PositionSide.LONG and context.order.side == OrderSide.BUY)
            or (context.position.side == PositionSide.SHORT and context.order.side == OrderSide.SELL)
        ):
            return PDTDecision(allowed=True, reason="Order allowed: YOLO strategy permits unlimited buys")
        else:
            if rolling_day_trade_count < 3:
                return PDTDecision(allowed=True, reason="Order allowed: YOLO strategy permits unlimited sells")
            else:
                return PDTDecision(
                    allowed=False, reason="Order not allowed: Closing this position would violate PDT rules"
                )
