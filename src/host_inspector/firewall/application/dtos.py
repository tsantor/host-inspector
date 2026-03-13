from dataclasses import dataclass


@dataclass(frozen=True)
class FirewallStatusDTO:
    overall: bool


@dataclass(frozen=True)
class FirewallRuleDTO:
    data: dict


@dataclass(frozen=True)
class FirewallRulesDTO:
    items: list[FirewallRuleDTO]
