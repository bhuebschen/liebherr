"""Liebherr HomeAPI models."""

from dataclasses import dataclass


@dataclass
class TemperatureControlRequest:
    zoneId: int
    target: int
    unit: str  # '°C' or '°F'


@dataclass
class ZoneToggleControlRequest:
    zoneId: int
    value: bool


@dataclass
class BaseToggleControlRequest:
    value: bool


@dataclass
class ModeZoneControlRequest:
    zoneId: int
    mode: str


@dataclass
class ModeControlRequest:
    mode: str

@dataclass
class IceMakerControlRequest:
    zoneId: int
    iceMakerMode: str  # "OFF", "ON", or "MAX_ICE"

@dataclass
class AutoDoorControl:
    zoneId: int
    value: bool  # True = open, False = close
