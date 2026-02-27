from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class PriceBreakdownItem:
    rule_name: str
    discount_amount: float
    description: str

@dataclass
class PricingResult:
    base_price: float
    final_price: float
    applied_rules: List[PriceBreakdownItem]

class PricingRuleEvaluator(ABC):
    @abstractmethod
    def evaluate(self, current_price: float, context: Dict[str, Any], rule_params: Dict[str, Any]) -> Optional[PriceBreakdownItem]:
        pass

class BulkDiscountEvaluator(PricingRuleEvaluator):
    def evaluate(self, current_price: float, context: Dict[str, Any], rule_params: Dict[str, Any]) -> Optional[PriceBreakdownItem]:
        min_quantity = rule_params.get("min_quantity", 0)
        discount_percentage = rule_params.get("discount_percentage", 0.0)
        
        if context.get("quantity", 0) >= min_quantity:
            discount = current_price * discount_percentage
            return PriceBreakdownItem(
                rule_name="Bulk Discount",
                discount_amount=discount,
                description=f"Applied {discount_percentage*100}% discount for {min_quantity}+ units"
            )
        return None

class UserTierDiscountEvaluator(PricingRuleEvaluator):
    def evaluate(self, current_price: float, context: Dict[str, Any], rule_params: Dict[str, Any]) -> Optional[PriceBreakdownItem]:
        target_tier = rule_params.get("user_tier")
        discount_percentage = rule_params.get("discount_percentage", 0.0)
        
        if context.get("user_tier") == target_tier:
            discount = current_price * discount_percentage
            return PriceBreakdownItem(
                rule_name=f"{target_tier} Tier Discount",
                discount_amount=discount,
                description=f"Applied {discount_percentage*100}% special discount for {target_tier} members"
            )
        return None

class SeasonalDiscountEvaluator(PricingRuleEvaluator):
    def evaluate(self, current_price: float, context: Dict[str, Any], rule_params: Dict[str, Any]) -> Optional[PriceBreakdownItem]:
        # Simple seasonal check for now, can be expanded with dates
        discount_percentage = rule_params.get("discount_percentage", 0.0)
        discount = current_price * discount_percentage
        return PriceBreakdownItem(
            rule_name="Seasonal Sale",
            discount_amount=discount,
            description=f"Applied {discount_percentage*100}% seasonal discount"
        )

class BOGODiscountEvaluator(PricingRuleEvaluator):
    def evaluate(self, current_price: float, context: Dict[str, Any], rule_params: Dict[str, Any]) -> Optional[PriceBreakdownItem]:
        quantity = context.get("quantity", 0)
        if quantity >= 2:
            # Buy X Get Y Free logic (simplified to BOGO 1+1)
            # Discount is the price of one item divided by the total quantity to get average discount per unit
            discount_per_unit = current_price / 2
            return PriceBreakdownItem(
                rule_name="BOGO",
                discount_amount=discount_per_unit,
                description="Buy One Get One Free applied"
            )
        return None

class PricingEngine:
    def __init__(self):
        self.evaluators = {
            "BULK": BulkDiscountEvaluator(),
            "USER_TIER": UserTierDiscountEvaluator(),
            "SEASONAL": SeasonalDiscountEvaluator(),
            "BOGO": BOGODiscountEvaluator()
        }

    def calculate_price(self, base_price: float, context: Dict[str, Any], rules: List[Any], product_category_id: Optional[int] = None, db: Optional[Any] = None) -> PricingResult:
        current_price = base_price
        applied_rules = []
        
        # 1. Apply active promotions (Category-wide or Site-wide)
        if db and product_category_id is not None:
            from app.models.models import Promotion
            import datetime
            now = datetime.datetime.utcnow()
            promotions = db.query(Promotion).filter(
                Promotion.is_active == 1,
                Promotion.start_date <= now,
                Promotion.end_date >= now,
                (Promotion.target_category_id == product_category_id) | (Promotion.target_category_id == None)
            ).all()
            
            for promo in promotions:
                discount = current_price * promo.discount_percentage
                applied_rules.append(PriceBreakdownItem(
                    rule_name=f"Promotion: {promo.name}",
                    discount_amount=discount,
                    description=f"Applied {promo.discount_percentage*100}% campaign discount"
                ))
                current_price -= discount

        # 2. Apply existing priority-based rules
        for rule in rules:
            evaluator = self.evaluators.get(rule.type)
            if evaluator:
                breakdown = evaluator.evaluate(current_price, context, rule.parameters)
                if breakdown:
                    applied_rules.append(breakdown)
                    current_price -= breakdown.discount_amount
        
        return PricingResult(
            base_price=base_price,
            final_price=max(0.0, current_price),
            applied_rules=applied_rules
        )
