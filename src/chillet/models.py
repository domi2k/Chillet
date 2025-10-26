"""Typed models for the Palworld REST API.

This module defines two families of Pydantic models:

- *Response models* (`ResponseModel` and subclasses): immutable, permissive
  on extra fields (`extra="allow"`) to stay resilient to server-side changes.
- *Request models* (`RequestModel` and subclasses): immutable, **strict**
  (`extra="forbid"`) to ensure only documented fields are serialized.

All models are frozen (`frozen=True`) which makes them hashable and safe to reuse.
"""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel, ConfigDict

ResponseT = TypeVar("ResponseT", bound=BaseModel)
RequestT = TypeVar("RequestT", bound=BaseModel)


class ResponseModel(BaseModel):
    """Response model without strict field handling."""

    model_config = ConfigDict(extra="allow", frozen=True)


class InfoResponse(ResponseModel):
    """Response type for server info."""

    version: str
    servername: str
    description: str
    worldguid: str


class Player(ResponseModel):
    name: str
    accountName: str
    playerId: str
    userId: str
    ip: str
    ping: float
    location_x: float
    location_y: float
    level: int


class PlayersResponse(ResponseModel):
    """Response type for the player list."""

    players: list[Player]


class SettingsResponse(ResponseModel):
    """Response type for the server settings."""

    Difficulty: str
    RandomizerType: str
    RandomizerSeed: str
    bIsRandomizerPalLevelRandom: bool
    DayTimeSpeedRate: float
    NightTimeSpeedRate: float
    ExpRate: float
    PalCaptureRate: float
    PalSpawnNumRate: float
    PalDamageRateAttack: float
    PalDamageRateDefense: float
    PlayerDamageRateAttack: float
    PlayerDamageRateDefense: float
    PlayerStomachDecreaceRate: float
    PlayerStaminaDecreaceRate: float
    PlayerAutoHPRegeneRate: float
    PlayerAutoHpRegeneRateInSleep: float
    PalStomachDecreaceRate: float
    PalStaminaDecreaceRate: float
    PalAutoHPRegeneRate: float
    PalAutoHpRegeneRateInSleep: float
    BuildObjectHpRate: float
    BuildObjectDamageRate: float
    BuildObjectDeteriorationDamageRate: float
    CollectionDropRate: float
    CollectionObjectHpRate: float
    CollectionObjectRespawnSpeedRate: float
    EnemyDropItemRate: float
    DeathPenalty: str
    bEnablePlayerToPlayerDamage: bool
    bEnableFriendlyFire: bool
    bEnableInvaderEnemy: bool
    bActiveUNKO: bool
    bEnableAimAssistPad: bool
    bEnableAimAssistKeyboard: bool
    DropItemMaxNum: int
    DropItemMaxNum_UNKO: int
    BaseCampMaxNum: int
    BaseCampWorkerMaxNum: int
    DropItemAliveMaxHours: int
    bAutoResetGuildNoOnlinePlayers: bool
    AutoResetGuildTimeNoOnlinePlayers: int
    GuildPlayerMaxNum: int
    BaseCampMaxNumInGuild: int
    PalEggDefaultHatchingTime: int
    WorkSpeedRate: float
    autoSaveSpan: int
    bIsMultiplay: bool
    bIsPvP: bool
    bHardcore: bool
    bPalLost: bool
    bCharacterRecreateInHardcore: bool
    bCanPickupOtherGuildDeathPenaltyDrop: bool
    bEnableNonLoginPenalty: bool
    bEnableFastTravel: bool
    bIsStartLocationSelectByMap: bool
    bExistPlayerAfterLogout: bool
    bEnableDefenseOtherGuildPlayer: bool
    bInvisibleOtherGuildBaseCampAreaFX: bool
    bBuildAreaLimit: bool
    ItemWeightRate: float
    CoopPlayerMaxNum: int
    ServerPlayerMaxNum: int
    ServerName: str
    ServerDescription: str
    PublicPort: int
    PublicIP: str
    RCONEnabled: bool
    RCONPort: int
    Region: str
    bUseAuth: bool
    BanListURL: str
    RESTAPIEnabled: bool
    RESTAPIPort: int
    bShowPlayerList: bool
    ChatPostLimitPerMinute: int
    CrossplayPlatforms: list[str]
    bIsUseBackupSaveData: bool
    LogFormatType: str
    SupplyDropSpan: int
    EnablePredatorBossPal: bool
    MaxBuildingLimitNum: int
    ServerReplicatePawnCullDistance: int
    bAllowGlobalPalboxExport: bool
    bAllowGlobalPalboxImport: bool
    EquipmentDurabilityDamageRate: float
    ItemContainerForceMarkDirtyInterval: int
    ItemCorruptionMultiplier: float


class MetricsResponse(ResponseModel):
    """Response type for the server metrics."""

    serverfps: int
    serverframetime: float
    currentplayernum: int
    maxplayernum: int
    uptime: int
    days: int


class RequestModel(BaseModel):
    """Request model with strict field handling."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class AnnounceRequest(RequestModel):
    """Explicit request type for announce operations."""

    message: str


class KickRequest(RequestModel):
    """Explicit request type for kick operations."""

    userid: str
    message: str | None = None


class BanRequest(RequestModel):
    """Explicit request type for ban operations."""

    userid: str
    message: str | None = None


class UnbanRequest(RequestModel):
    """Explicit request type for unban operations."""

    userid: str


class SaveRequest(RequestModel):
    """Explicit request type for save operations."""


class ShutdownRequest(RequestModel):
    """Explicit request type for shutdown operations"""

    waittime: int
    message: str | None = None


class StopRequest(RequestModel):
    """Explicit request type for stop operations."""
