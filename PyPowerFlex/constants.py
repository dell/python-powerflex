# Copyright (c) 2024 Dell Inc. or its subsidiaries.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""This module contains the definitions of constants used in the code."""

# pylint: disable=too-few-public-methods

class StoragePoolConstants:
    """
    This class holds constants related to StoragePool.
    """
    DEFAULT_STATISTICS_PROPERTIES = [
        "backgroundScanFixedReadErrorCount",
        "pendingMovingOutBckRebuildJobs",
        "degradedHealthyCapacityInKb",
        "activeMovingOutFwdRebuildJobs",
        "bckRebuildWriteBwc",
        "netFglUncompressedDataSizeInKb",
        "primaryReadFromDevBwc",
        "BackgroundScannedInMB",
        "volumeIds",
        "maxUserDataCapacityInKb",
        "persistentChecksumBuilderProgress",
        "rfcacheReadsSkippedAlignedSizeTooLarge",
        "pendingMovingInRebalanceJobs",
        "rfcacheWritesSkippedHeavyLoad",
        "unusedCapacityInKb",
        "userDataSdcReadLatency",
        "totalReadBwc",
        "numOfDeviceAtFaultRebuilds",
        "totalWriteBwc",
        "persistentChecksumCapacityInKb",
        "rmPendingAllocatedInKb",
        "numOfVolumes",
        "rfcacheIosOutstanding",
        "capacityAvailableForVolumeAllocationInKb",
        "numOfMappedToAllVolumes",
        "netThinUserDataCapacityInKb",
        "backgroundScanFixedCompareErrorCount",
        "volMigrationWriteBwc",
        "thinAndSnapshotRatio",
        "fglUserDataCapacityInKb",
        "pendingMovingInEnterProtectedMaintenanceModeJobs",
        "activeMovingInNormRebuildJobs",
        "aggregateCompressionLevel",
        "targetOtherLatency",
        "netUserDataCapacityInKb",
        "pendingMovingOutExitProtectedMaintenanceModeJobs",
        "overallUsageRatio",
        "volMigrationReadBwc",
        "netCapacityInUseNoOverheadInKb",
        "pendingMovingInBckRebuildJobs",
        "rfcacheReadsSkippedInternalError",
        "activeBckRebuildCapacityInKb",
        "rebalanceCapacityInKb",
        "pendingMovingInExitProtectedMaintenanceModeJobs",
        "rfcacheReadsSkippedLowResources",
        "rplJournalCapAllowed",
        "thinCapacityInUseInKb",
        "userDataSdcTrimLatency",
        "activeMovingInEnterProtectedMaintenanceModeJobs",
        "rfcacheWritesSkippedInternalError",
        "netUserDataCapacityNoTrimInKb",
        "rfcacheWritesSkippedCacheMiss",
        "degradedFailedCapacityInKb",
        "activeNormRebuildCapacityInKb",
        "fglSparesInKb",
        "snapCapacityInUseInKb",
        "numOfMigratingVolumes",
        "compressionRatio",
        "rfcacheWriteMiss",
        "primaryReadFromRmcacheBwc",
        "migratingVtreeIds",
        "numOfVtrees",
        "userDataCapacityNoTrimInKb",
        "rfacheReadHit",
        "compressedDataCompressionRatio",
        "rplUsedJournalCap",
        "pendingMovingCapacityInKb",
        "numOfSnapshots",
        "pendingFwdRebuildCapacityInKb",
        "tempCapacityInKb",
        "totalFglMigrationSizeInKb",
        "normRebuildCapacityInKb",
        "logWrittenBlocksInKb",
        "primaryWriteBwc",
        "numOfThickBaseVolumes",
        "enterProtectedMaintenanceModeReadBwc",
        "activeRebalanceCapacityInKb",
        "numOfReplicationJournalVolumes",
        "rfcacheReadsSkippedLockIos",
        "unreachableUnusedCapacityInKb",
        "netProvisionedAddressesInKb",
        "trimmedUserDataCapacityInKb",
        "provisionedAddressesInKb",
        "numOfVolumesInDeletion",
        "pendingMovingOutFwdRebuildJobs",
        "maxCapacityInKb",
        "rmPendingThickInKb",
        "protectedCapacityInKb",
        "secondaryWriteBwc",
        "normRebuildReadBwc",
        "thinCapacityAllocatedInKb",
        "netFglUserDataCapacityInKb",
        "metadataOverheadInKb",
        "rebalanceWriteBwc",
        "primaryVacInKb",
        "deviceIds",
        "netSnapshotCapacityInKb",
        "secondaryVacInKb",
        "numOfDevices",
        "rplTotalJournalCap",
        "failedCapacityInKb",
        "netMetadataOverheadInKb",
        "activeMovingOutBckRebuildJobs",
        "rfcacheReadsFromCache",
        "activeMovingOutEnterProtectedMaintenanceModeJobs",
        "enterProtectedMaintenanceModeCapacityInKb",
        "pendingMovingInNormRebuildJobs",
        "failedVacInKb",
        "primaryReadBwc",
        "fglUncompressedDataSizeInKb",
        "fglCompressedDataSizeInKb",
        "pendingRebalanceCapacityInKb",
        "rfcacheAvgReadTime",
        "semiProtectedCapacityInKb",
        "pendingMovingOutEnterProtectedMaintenanceModeJobs",
        "mgUserDdataCcapacityInKb",
        "snapshotCapacityInKb",
        "netMgUserDataCapacityInKb",
        "fwdRebuildReadBwc",
        "rfcacheWritesReceived",
        "netUnusedCapacityInKb",
        "protectedVacInKb",
        "activeMovingRebalanceJobs",
        "bckRebuildCapacityInKb",
        "activeMovingInFwdRebuildJobs",
        "netTrimmedUserDataCapacityInKb",
        "pendingMovingRebalanceJobs",
        "numOfMarkedVolumesForReplication",
        "degradedHealthyVacInKb",
        "semiProtectedVacInKb",
        "userDataReadBwc",
        "pendingBckRebuildCapacityInKb",
        "capacityLimitInKb",
        "vtreeIds",
        "activeMovingCapacityInKb",
        "targetWriteLatency",
        "pendingExitProtectedMaintenanceModeCapacityInKb",
        "rfcacheIosSkipped",
        "userDataWriteBwc",
        "inMaintenanceVacInKb",
        "exitProtectedMaintenanceModeReadBwc",
        "netFglSparesInKb",
        "rfcacheReadsSkipped",
        "activeExitProtectedMaintenanceModeCapacityInKb",
        "activeMovingOutExitProtectedMaintenanceModeJobs",
        "numOfUnmappedVolumes",
        "tempCapacityVacInKb",
        "volumeAddressSpaceInKb",
        "currentFglMigrationSizeInKb",
        "rfcacheWritesSkippedMaxIoSize",
        "netMaxUserDataCapacityInKb",
        "numOfMigratingVtrees",
        "atRestCapacityInKb",
        "rfacheWriteHit",
        "bckRebuildReadBwc",
        "rfcacheSourceDeviceWrites",
        "spareCapacityInKb",
        "enterProtectedMaintenanceModeWriteBwc",
        "rfcacheIoErrors",
        "inaccessibleCapacityInKb",
        "normRebuildWriteBwc",
        "capacityInUseInKb",
        "rebalanceReadBwc",
        "rfcacheReadsSkippedMaxIoSize",
        "activeMovingInExitProtectedMaintenanceModeJobs",
        "secondaryReadFromDevBwc",
        "secondaryReadBwc",
        "rfcacheWritesSkippedStuckIo",
        "secondaryReadFromRmcacheBwc",
        "inMaintenanceCapacityInKb",
        "exposedCapacityInKb",
        "netFglCompressedDataSizeInKb",
        "userDataSdcWriteLatency",
        "inUseVacInKb",
        "fwdRebuildCapacityInKb",
        "thickCapacityInUseInKb",
        "backgroundScanReadErrorCount",
        "activeMovingInRebalanceJobs",
        "migratingVolumeIds",
        "rfcacheWritesSkippedLowResources",
        "capacityInUseNoOverheadInKb",
        "exitProtectedMaintenanceModeWriteBwc",
        "rfcacheSkippedUnlinedWrite",
        "netCapacityInUseInKb",
        "numOfOutgoingMigrations",
        "rfcacheAvgWriteTime",
        "pendingNormRebuildCapacityInKb",
        "pendingMovingOutNormrebuildJobs",
        "rfcacheSourceDeviceReads",
        "rfcacheReadsPending",
        "volumeAllocationLimitInKb",
        "rfcacheReadsSkippedHeavyLoad",
        "fwdRebuildWriteBwc",
        "rfcacheReadMiss",
        "targetReadLatency",
        "userDataCapacityInKb",
        "activeMovingInBckRebuildJobs",
        "movingCapacityInKb",
        "activeEnterProtectedMaintenanceModeCapacityInKb",
        "backgroundScanCompareErrorCount",
        "pendingMovingInFwdRebuildJobs",
        "rfcacheReadsReceived",
        "spSdsIds",
        "pendingEnterProtectedMaintenanceModeCapacityInKb",
        "vtreeAddresSpaceInKb",
        "snapCapacityInUseOccupiedInKb",
        "activeFwdRebuildCapacityInKb",
        "rfcacheReadsSkippedStuckIo",
        "activeMovingOutNormRebuildJobs",
        "rfcacheWritePending",
        "numOfThinBaseVolumes",
        "degradedFailedVacInKb",
        "userDataTrimBwc",
        "numOfIncomingVtreeMigrations"]

    DEFAULT_STATISTICS_PROPERTIES_ABOVE_3_5 = [
        "thinCapacityAllocatedInKm", "thinUserDataCapacityInKb"]


class VolumeConstants:
    """
    This class holds constants related to Volume.
    """
    DEFAULT_STATISTICS_PROPERTIES = [
        "rplUsedJournalCap",
        "replicationState",
        "numOfChildVolumes",
        "userDataWriteBwc",
        "rplTotalJournalCap",
        "initiatorSdcId",
        "userDataSdcReadLatency",
        "userDataSdcTrimLatency",
        "mappedSdcIds",
        "registrationKey",
        "registrationKeys",
        "descendantVolumeIds",
        "numOfMappedSdcs",
        "reservationType",
        "userDataReadBwc",
        "numOfDescendantVolumes",
        "replicationJournalVolume",
        "userDataTrimBwc",
        "childVolumeIds",
        "userDataSdcWriteLatency"]


class RCGConstants:
    """
    This class holds constants related to RCG.
    """
    DEFAULT_STATISTICS_PROPERTIES = [
        "rcgLocalReadBwc",
        "initialCopyNumPairs",
        "lagPersistentInMillis",
        "rplRemoteUserBwc",
        "rplApplyLatency",
        "lagReceivedInMillis",
        "nextPlannedCycle",
        "lagPersistentSkew",
        "lastSadBarrierId",
        "readyForTransmit",
        "initialCopyTransmit",
        "rplLocalUserBwc",
        "rplPairIds",
        "numOfRplPairs",
        "rplReceiveLatency",
        "rplLocalApplyBwc",
        "lagAppliedInMillis",
        "lastCsadBarrierId",
        "lastCompletedPeriodicBarrier",
        "lastAppliedBarrierId",
        "rplRemoteApplyBwc",
        "readyForApply",
        "initialCopyApply",
        "lagReceivedSkew",
        "initialCopyProgress",
        "rcgLocalWriteBwc",
        "notReadyForTransmit",
        "rplCgRpoCompliance",
        "notReadyForApply",
        "rplTransmitBwc",
        "lastCradBarrierId",
        "lagAppliedSkew",
        "lastRadBarrierId",
        "rplReceiveBwc",
        "rcgRemoteWriteBwc",
        "rcgRemoteReadBwc",
        "rplTransmitLatency"]
    DEFAULT_STATISTICS_PROPERTIES_ABOVE_3_5 = [
        "rcgLocalWriteBwc",
        "nextPlannedCycle",
        "rplTransmitLatency",
        "lagReceivedInMillis",
        "rcgRemoteReadBwc",
        "lastCradBarrierId",
        "lagAppliedSkew",
        "readyForApply",
        "rplUsedJournalCapacityDst",
        "rplReceiveBwc",
        "lastSadBarrierId",
        "isInSlimMode",
        "lastRadBarrierId",
        "lastAppliedBarrierId",
        "initialCopyTransmit",
        "initialCopyNumPairs",
        "lagAppliedInMillis",
        "lastCompletedPeriodicBarrier",
        "rplLocalApplyBwc",
        "rcgLocalReadBwc",
        "notReadyForTransmit",
        "rplCgRpoCompliance",
        "freezeTransmit",
        "lagPersistentInMillis",
        "lagReceivedSkew",
        "notReadyForApply",
        "initialCopyApply",
        "rplPairIds",
        "rplLocalUserBwc",
        "numOfRplPairs",
        "rplReceiveLatency",
        "lastCsadBarrierId",
        "rplRemoteApplyBwc",
        "rcgRemoteWriteBwc",
        "initialCopyProgress",
        "lagPersistentSkew",
        "rplSasBarriersBacklogSize",
        "rplTransmitBwc",
        "rplApplyLatency",
        "readyForTransmit",
        "rplRemoteUserBwc"]


class SnapshotPolicyConstants:
    """
    This class holds constants related to SnapshotPolicy.
    """
    DEFAULT_STATISTICS_PROPERTIES = [
        "autoSnapshotVolIds",
        "expiredButLockedSnapshotsIds",
        "numOfAutoSnapshots",
        "numOfExpiredButLockedSnapshots",
        "numOfSrcVols",
        "srcVolIds"]


class CredentialConstants:
    """
    Constants specific to PowerFlex credential management.
    """
    # The minimum Gateway version that supports credential management
    MIN_GATEWAY_VERSION_FOR_CREDENTIALS = "4.0"

    # The base URL for credential operations
    BASE_CREDENTIAL_URL = "/Api/V1/Credential"

    # Credential types
    SERVER_CREDENTIAL = "serverCredential"
    IOM_CREDENTIAL = "iomCredential"
    VCENTER_CREDENTIAL = "vCenterCredential"
    EM_CREDENTIAL = "emCredential"
    SCALEIO_CREDENTIAL = "scaleIoCredential"
    PS_CREDENTIAL = "psCredential"
    OS_CREDENTIAL = "osCredential"
    OS_USER_CREDENTIAL = "osUserCredential"

    # List of all valid credential types
    ALL_CREDENTIAL_TYPES = [
        SERVER_CREDENTIAL,
        IOM_CREDENTIAL,
        VCENTER_CREDENTIAL,
        EM_CREDENTIAL,
        SCALEIO_CREDENTIAL,
        PS_CREDENTIAL,
        OS_CREDENTIAL,
        OS_USER_CREDENTIAL
    ]

    # Credential types that support domain parameter
    DOMAIN_SUPPORTED_TYPES = [
        "vCenterCredential",
        "emCredential",
        "psCredential",
        "osCredential",
        "osUserCredential"
    ]

    # Content types for credential operations
    XML_CONTENT_TYPE = "application/xml"
    JSON_CONTENT_TYPE = "application/json"

    # Create credential XML template
    CREATE_CREDENTIAL_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
{credential_content}
"""

    # Update credential XML template
    UPDATE_CREDENTIAL_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
{credential_content}
"""
