from tkinter import *
from tkinter import filedialog
import subprocess
import json
from collections import deque
from itertools import islice
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from queue import Queue, Empty
import re

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = root
        self.grid()
        self.create_widgets()
        self.create_scrollbar_data()



        self._var = StringVar()

        self.ShellOutputWindow = Toplevel(width=500, height=700)
        self.ShellOutputWindow.title("Shell Output")
        self.ShellOutputWindow.grid()


        self.ShellOutputText = Text(self.ShellOutputWindow, width=100, height=40, wrap=WORD)
        self.ShellOutputText.grid(row=0, column=1, columnspan=2, sticky=W)

    def create_widgets(self):
        # Declare variables ######################################################
        # self.SourceServerString = StringVar()
        # self.SourceDatabaseString = StringVar()

        # self.TargetServerString = StringVar()
        # self.TargetDatabaseString = StringVar()

        # self.InformationString = StringVar()

        # self.PreDeploymentQueryString = StringVar()

        self.ShellOutputPreDeploymentString = StringVar()
        self.ShellOutputExtractString = StringVar()
        self.ShellOutputPublishString = StringVar()
        self.ShellOutputScriptString = StringVar()

        self.WinAuthSrcVariable = BooleanVar()
        self.WinAuthSrcVariable.set(True)
        self.WinAuthTrgtVariable = BooleanVar()
        self.WinAuthTrgtVariable.set(True)

        self.EncryptSrcVariable = BooleanVar()
        self.EncryptSrcVariable.set(False)
        self.EncryptTrgtVariable = BooleanVar()
        self.EncryptTrgtVariable.set(False)

        self.SetDplyPropertyVariable = BooleanVar()
        self.SetDplyPropertyVariable.set(False)

        # Declare variables for CHECKBUTTONS of Scroll Options #####################################
        ###########################################################################
        self.ChkButtonAllowDropBlockingAssemblies = BooleanVar()
        self.ChkButtonAllowIncompatiblePlatform = BooleanVar()
        self.ChkButtonBackupDatabaseBeforeChanges = BooleanVar()
        self.ChkButtonBlockOnPossibleDataLoss = BooleanVar()
        self.ChkButtonBlockWhenDriftDetected = BooleanVar()
        self.ChkButtonCommandTimeout = BooleanVar()
        self.ChkButtonCommentOutSetVarDeclarations = BooleanVar()
        self.ChkButtonCompareUsingTargetCollation = BooleanVar()
        self.ChkButtonCreateNewDatabase = BooleanVar()
        self.ChkButtonDeployDatabaseInSingleUserMode = BooleanVar()
        self.ChkButtonDisableAndReenableDdlTriggers = BooleanVar()
        self.ChkButtonDoNotAlterChangeDataCaptureObjects = BooleanVar()
        self.ChkButtonDoNotAlterReplicatedObjects = BooleanVar()
        self.ChkButtonDoNotDropObjectTypes = BooleanVar()
        self.ChkButtonDropConstraintsNotInSource = BooleanVar()
        self.ChkButtonDropDmlTriggersNotInSource = BooleanVar()
        self.ChkButtonDropExtendedPropertiesNotInSource = BooleanVar()
        self.ChkButtonDropIndexesNotInSource = BooleanVar()
        self.ChkButtonDropObjectsNotInSource = BooleanVar()
        self.ChkButtonDropPermissionsNotInSource = BooleanVar()
        self.ChkButtonDropRoleMembersNotInSource = BooleanVar()
        self.ChkButtonExcludeObjectTypes = BooleanVar()
        self.ChkButtonGenerateSmartDefaults = BooleanVar()
        self.ChkButtonIgnoreAnsiNulls = BooleanVar()
        self.ChkButtonIgnoreAuthorizer = BooleanVar()
        self.ChkButtonIgnoreColumnCollation = BooleanVar()
        self.ChkButtonIgnoreComments = BooleanVar()
        self.ChkButtonIgnoreCryptographicProviderFilePath = BooleanVar()
        self.ChkButtonIgnoreDdlTriggerOrder = BooleanVar()
        self.ChkButtonIgnoreDdlTriggerState = BooleanVar()
        self.ChkButtonIgnoreDefaultSchema = BooleanVar()
        self.ChkButtonIgnoreDmlTriggerOrder = BooleanVar()
        self.ChkButtonIgnoreDmlTriggerState = BooleanVar()
        self.ChkButtonIgnoreExtendedProperties = BooleanVar()
        self.ChkButtonIgnoreFileAndLogFilePath = BooleanVar()
        self.ChkButtonIgnoreFilegroupPlacement = BooleanVar()
        self.ChkButtonIgnoreFileSize = BooleanVar()
        self.ChkButtonIgnoreFillFactor = BooleanVar()
        self.ChkButtonIgnoreFullTextCatalogFilePath = BooleanVar()
        self.ChkButtonIgnoreIdentitySeed = BooleanVar()
        self.ChkButtonIgnoreIncrement = BooleanVar()
        self.ChkButtonIgnoreIndexOptions = BooleanVar()
        self.ChkButtonIgnoreIndexPadding = BooleanVar()
        self.ChkButtonIgnoreKeywordCasing = BooleanVar()
        self.ChkButtonIgnoreLockHintsOnIndexes = BooleanVar()
        self.ChkButtonIgnoreLoginSids = BooleanVar()
        self.ChkButtonIgnoreNotForReplication = BooleanVar()
        self.ChkButtonIgnoreObjectPlacementOnPartitionScheme = BooleanVar()
        self.ChkButtonIgnorePartitionSchemes = BooleanVar()
        self.ChkButtonIgnorePermissions = BooleanVar()
        self.ChkButtonIgnoreQuotedIdentifiers = BooleanVar()
        self.ChkButtonIgnoreRoleMembership = BooleanVar()
        self.ChkButtonIgnoreRouteLifetime = BooleanVar()
        self.ChkButtonIgnoreSemicolonBetweenStatements = BooleanVar()
        self.ChkButtonIgnoreTableOptions = BooleanVar()
        self.ChkButtonIgnoreUserSettingsObjects = BooleanVar()
        self.ChkButtonIgnoreWhitespace = BooleanVar()
        self.ChkButtonIgnoreWithNocheckOnCheckConstraints = BooleanVar()
        self.ChkButtonIgnoreWithNocheckOnForeignKeys = BooleanVar()
        self.ChkButtonIncludeCompositeObjects = BooleanVar()
        self.ChkButtonIncludeTransactionalScripts = BooleanVar()
        self.ChkButtonNoAlterStatementsToChangeClrTypes = BooleanVar()
        self.ChkButtonPopulateFilesOnFilegroups = BooleanVar()
        self.ChkButtonRegisterDataTierApplication = BooleanVar()
        self.ChkButtonRunDeploymentPlanExecutors = BooleanVar()
        self.ChkButtonScriptDatabaseCollation = BooleanVar()
        self.ChkButtonScriptDatabaseCompatibility = BooleanVar()
        self.ChkButtonScriptDatabaseOptions = BooleanVar()
        self.ChkButtonScriptDeployStateChecks = BooleanVar()
        self.ChkButtonScriptFileSize = BooleanVar()
        self.ChkButtonScriptNewConstraintValidation = BooleanVar()
        self.ChkButtonScriptRefreshModule = BooleanVar()
        self.ChkButtonStorage = BooleanVar()
        self.ChkButtonTreatVerificationErrorsAsWarnings = BooleanVar()
        self.ChkButtonUnmodifiableObjectWarnings = BooleanVar()
        self.ChkButtonVerifyCollationCompatibility = BooleanVar()
        self.ChkButtonVerifyDeployment = BooleanVar()
        ###########################################################################
        ###########################################################################

        # #Set variables for checkbuttons of Scroll Options##########################
        # ###########################################################################
        # self.ChkButtonAllowDropBlockingAssemblies.set(False)
        # self.ChkButtonAllowIncompatiblePlatform.set(False)
        # self.ChkButtonBackupDatabaseBeforeChanges.set(False)
        # self.ChkButtonBlockOnPossibleDataLoss.set(False)
        # self.ChkButtonBlockWhenDriftDetected.set(False)
        # self.ChkButtonCommandTimeout.set(False)
        # self.ChkButtonCommentOutSetVarDeclarations.set(False)
        # self.ChkButtonCompareUsingTargetCollation.set(False)
        # self.ChkButtonCreateNewDatabase.set(False)
        # self.ChkButtonDeployDatabaseInSingleUserMode.set(False)
        # self.ChkButtonDisableAndReenableDdlTriggers.set(False)
        # self.ChkButtonDoNotAlterChangeDataCaptureObjects.set(False)
        # self.ChkButtonDoNotAlterReplicatedObjects.set(False)
        # self.ChkButtonDoNotDropObjectTypes.set(False)
        # self.ChkButtonDropConstraintsNotInSource.set(False)
        # self.ChkButtonDropDmlTriggersNotInSource.set(False)
        # self.ChkButtonDropExtendedPropertiesNotInSource.set(False)
        # self.ChkButtonDropIndexesNotInSource.set(False)
        # self.ChkButtonDropObjectsNotInSource.set(False)
        # self.ChkButtonDropPermissionsNotInSource.set(False)
        # self.ChkButtonDropRoleMembersNotInSource.set(False)
        # self.ChkButtonExcludeObjectTypes.set(False)
        # self.ChkButtonGenerateSmartDefaults.set(False)
        # self.ChkButtonIgnoreAnsiNulls.set(False)
        # self.ChkButtonIgnoreAuthorizer.set(False)
        # self.ChkButtonIgnoreColumnCollation.set(False)
        # self.ChkButtonIgnoreComments.set(False)
        # self.ChkButtonIgnoreCryptographicProviderFilePath.set(False)
        # self.ChkButtonIgnoreDdlTriggerOrder.set(False)
        # self.ChkButtonIgnoreDdlTriggerState.set(False)
        # self.ChkButtonIgnoreDefaultSchema.set(False)
        # self.ChkButtonIgnoreDmlTriggerOrder.set(False)
        # self.ChkButtonIgnoreDmlTriggerState.set(False)
        # self.ChkButtonIgnoreExtendedProperties.set(False)
        # self.ChkButtonIgnoreFileAndLogFilePath.set(False)
        # self.ChkButtonIgnoreFilegroupPlacement.set(False)
        # self.ChkButtonIgnoreFileSize.set(False)
        # self.ChkButtonIgnoreFillFactor.set(False)
        # self.ChkButtonIgnoreFullTextCatalogFilePath.set(False)
        # self.ChkButtonIgnoreIdentitySeed.set(False)
        # self.ChkButtonIgnoreIncrement.set(False)
        # self.ChkButtonIgnoreIndexOptions.set(False)
        # self.ChkButtonIgnoreIndexPadding.set(False)
        # self.ChkButtonIgnoreKeywordCasing.set(False)
        # self.ChkButtonIgnoreLockHintsOnIndexes.set(False)
        # self.ChkButtonIgnoreLoginSids.set(False)
        # self.ChkButtonIgnoreNotForReplication.set(False)
        # self.ChkButtonIgnoreObjectPlacementOnPartitionScheme.set(False)
        # self.ChkButtonIgnorePartitionSchemes.set(False)
        # self.ChkButtonIgnorePermissions.set(False)
        # self.ChkButtonIgnoreQuotedIdentifiers.set(False)
        # self.ChkButtonIgnoreRoleMembership.set(False)
        # self.ChkButtonIgnoreRouteLifetime.set(False)
        # self.ChkButtonIgnoreSemicolonBetweenStatements.set(False)
        # self.ChkButtonIgnoreTableOptions.set(False)
        # self.ChkButtonIgnoreUserSettingsObjects.set(False)
        # self.ChkButtonIgnoreWhitespace.set(False)
        # self.ChkButtonIgnoreWithNocheckOnCheckConstraints.set(False)
        # self.ChkButtonIgnoreWithNocheckOnForeignKeys.set(False)
        # self.ChkButtonIncludeCompositeObjects.set(False)
        # self.ChkButtonIncludeTransactionalScripts.set(False)
        # self.ChkButtonNoAlterStatementsToChangeClrTypes.set(False)
        # self.ChkButtonPopulateFilesOnFilegroups.set(False)
        # self.ChkButtonRegisterDataTierApplication.set(False)
        # self.ChkButtonRunDeploymentPlanExecutors.set(False)
        # self.ChkButtonScriptDatabaseCollation.set(False)
        # self.ChkButtonScriptDatabaseCompatibility.set(False)
        # self.ChkButtonScriptDatabaseOptions.set(False)
        # self.ChkButtonScriptDeployStateChecks.set(False)
        # self.ChkButtonScriptFileSize.set(False)
        # self.ChkButtonScriptNewConstraintValidation.set(False)
        # self.ChkButtonScriptRefreshModule.set(False)
        # self.ChkButtonStorage.set(False)
        # self.ChkButtonTreatVerificationErrorsAsWarnings.set(False)
        # self.ChkButtonUnmodifiableObjectWarnings.set(False)
        # self.ChkButtonVerifyCollationCompatibility.set(False)
        # self.ChkButtonVerifyDeployment.set(False)
        # ###########################################################################
        # ###########################################################################


        # Declare variables for Values of ScrollOptions ENTRY/DROPDOWN #############################
        ###########################################################################
        self.ValueAllowDropBlockingAssemblies = StringVar()
        self.ValueAllowIncompatiblePlatform = StringVar()
        self.ValueBackupDatabaseBeforeChanges = StringVar()
        self.ValueBlockOnPossibleDataLoss = StringVar()
        self.ValueBlockWhenDriftDetected = StringVar()
        self.ValueCommandTimeout = StringVar()
        self.ValueCommentOutSetVarDeclarations = StringVar()
        self.ValueCompareUsingTargetCollation = StringVar()
        self.ValueCreateNewDatabase = StringVar()
        self.ValueDeployDatabaseInSingleUserMode = StringVar()
        self.ValueDisableAndReenableDdlTriggers = StringVar()
        self.ValueDoNotAlterChangeDataCaptureObjects = StringVar()
        self.ValueDoNotAlterReplicatedObjects = StringVar()
        self.ValueDoNotDropObjectTypes = StringVar()
        self.ValueDropConstraintsNotInSource = StringVar()
        self.ValueDropDmlTriggersNotInSource = StringVar()
        self.ValueDropExtendedPropertiesNotInSource = StringVar()
        self.ValueDropIndexesNotInSource = StringVar()
        self.ValueDropObjectsNotInSource = StringVar()
        self.ValueDropPermissionsNotInSource = StringVar()
        self.ValueDropRoleMembersNotInSource = StringVar()
        self.ValueExcludeObjectTypes = StringVar()
        self.ValueGenerateSmartDefaults = StringVar()
        self.ValueIgnoreAnsiNulls = StringVar()
        self.ValueIgnoreAuthorizer = StringVar()
        self.ValueIgnoreColumnCollation = StringVar()
        self.ValueIgnoreComments = StringVar()
        self.ValueIgnoreCryptographicProviderFilePath = StringVar()
        self.ValueIgnoreDdlTriggerOrder = StringVar()
        self.ValueIgnoreDdlTriggerState = StringVar()
        self.ValueIgnoreDefaultSchema = StringVar()
        self.ValueIgnoreDmlTriggerOrder = StringVar()
        self.ValueIgnoreDmlTriggerState = StringVar()
        self.ValueIgnoreExtendedProperties = StringVar()
        self.ValueIgnoreFileAndLogFilePath = StringVar()
        self.ValueIgnoreFilegroupPlacement = StringVar()
        self.ValueIgnoreFileSize = StringVar()
        self.ValueIgnoreFillFactor = StringVar()
        self.ValueIgnoreFullTextCatalogFilePath = StringVar()
        self.ValueIgnoreIdentitySeed = StringVar()
        self.ValueIgnoreIncrement = StringVar()
        self.ValueIgnoreIndexOptions = StringVar()
        self.ValueIgnoreIndexPadding = StringVar()
        self.ValueIgnoreKeywordCasing = StringVar()
        self.ValueIgnoreLockHintsOnIndexes = StringVar()
        self.ValueIgnoreLoginSids = StringVar()
        self.ValueIgnoreNotForReplication = StringVar()
        self.ValueIgnoreObjectPlacementOnPartitionScheme = StringVar()
        self.ValueIgnorePartitionSchemes = StringVar()
        self.ValueIgnorePermissions = StringVar()
        self.ValueIgnoreQuotedIdentifiers = StringVar()
        self.ValueIgnoreRoleMembership = StringVar()
        self.ValueIgnoreRouteLifetime = StringVar()
        self.ValueIgnoreSemicolonBetweenStatements = StringVar()
        self.ValueIgnoreTableOptions = StringVar()
        self.ValueIgnoreUserSettingsObjects = StringVar()
        self.ValueIgnoreWhitespace = StringVar()
        self.ValueIgnoreWithNocheckOnCheckConstraints = StringVar()
        self.ValueIgnoreWithNocheckOnForeignKeys = StringVar()
        self.ValueIncludeCompositeObjects = StringVar()
        self.ValueIncludeTransactionalScripts = StringVar()
        self.ValueNoAlterStatementsToChangeClrTypes = StringVar()
        self.ValuePopulateFilesOnFilegroups = StringVar()
        self.ValueRegisterDataTierApplication = StringVar()
        self.ValueRunDeploymentPlanExecutors = StringVar()
        self.ValueScriptDatabaseCollation = StringVar()
        self.ValueScriptDatabaseCompatibility = StringVar()
        self.ValueScriptDatabaseOptions = StringVar()
        self.ValueScriptDeployStateChecks = StringVar()
        self.ValueScriptFileSize = StringVar()
        self.ValueScriptNewConstraintValidation = StringVar()
        self.ValueScriptRefreshModule = StringVar()
        self.ValueStorage = StringVar()
        self.ValueTreatVerificationErrorsAsWarnings = StringVar()
        self.ValueUnmodifiableObjectWarnings = StringVar()
        self.ValueVerifyCollationCompatibility = StringVar()
        self.ValueVerifyDeployment = StringVar()
        #############################################################################
        #############################################################################


        # #Set Values of ScrollOptions ENTRY/DROPDOWN################################
        # ###########################################################################
        # self.ValueAllowDropBlockingAssemblies.set("False")
        # self.ValueAllowIncompatiblePlatform.set("False")
        # self.ValueBackupDatabaseBeforeChanges.set("False")
        # self.ValueBlockOnPossibleDataLoss.set("True")
        # self.ValueBlockWhenDriftDetected.set("True")
        # # self.ValueCommandTimeout.set("60")
        # self.ValueCommentOutSetVarDeclarations.set("False")
        # self.ValueCompareUsingTargetCollation.set("False")
        # self.ValueCreateNewDatabase.set("False")
        # self.ValueDeployDatabaseInSingleUserMode.set("False")
        # self.ValueDisableAndReenableDdlTriggers.set("True")
        # self.ValueDoNotAlterChangeDataCaptureObjects.set("True")
        # self.ValueDoNotAlterReplicatedObjects.set("True")
        # # self.ValueDoNotDropObjectTypes.set("N/A.")
        # self.ValueDropConstraintsNotInSource.set("True")
        # self.ValueDropDmlTriggersNotInSource.set("True")
        # self.ValueDropExtendedPropertiesNotInSource.set("True")
        # self.ValueDropIndexesNotInSource.set("True")
        # self.ValueDropObjectsNotInSource.set("False")
        # self.ValueDropPermissionsNotInSource.set("False")
        # self.ValueDropRoleMembersNotInSource.set("False")
        # # self.ValueExcludeObjectTypes.set("N/A.")
        # self.ValueGenerateSmartDefaults.set("False")
        # self.ValueIgnoreAnsiNulls.set("False")
        # self.ValueIgnoreAuthorizer.set("False")
        # self.ValueIgnoreColumnCollation.set("False")
        # self.ValueIgnoreComments.set("False")
        # self.ValueIgnoreCryptographicProviderFilePath.set("True")
        # self.ValueIgnoreDdlTriggerOrder.set("False")
        # self.ValueIgnoreDdlTriggerState.set("False")
        # self.ValueIgnoreDefaultSchema.set("False")
        # self.ValueIgnoreDmlTriggerOrder.set("False")
        # self.ValueIgnoreDmlTriggerState.set("False")
        # self.ValueIgnoreExtendedProperties.set("False")
        # self.ValueIgnoreFileAndLogFilePath.set("True")
        # self.ValueIgnoreFilegroupPlacement.set("True")
        # self.ValueIgnoreFileSize.set("True")
        # self.ValueIgnoreFillFactor.set("True")
        # self.ValueIgnoreFullTextCatalogFilePath.set("True")
        # self.ValueIgnoreIdentitySeed.set("False")
        # self.ValueIgnoreIncrement.set("False")
        # self.ValueIgnoreIndexOptions.set("False")
        # self.ValueIgnoreIndexPadding.set("True")
        # self.ValueIgnoreKeywordCasing.set("True")
        # self.ValueIgnoreLockHintsOnIndexes.set("False")
        # self.ValueIgnoreLoginSids.set("True")
        # self.ValueIgnoreNotForReplication.set("False")
        # self.ValueIgnoreObjectPlacementOnPartitionScheme.set("True")
        # self.ValueIgnorePartitionSchemes.set("False")
        # self.ValueIgnorePermissions.set("False")
        # self.ValueIgnoreQuotedIdentifiers.set("False")
        # self.ValueIgnoreRoleMembership.set("False")
        # self.ValueIgnoreRouteLifetime.set("True")
        # self.ValueIgnoreSemicolonBetweenStatements.set("True")
        # self.ValueIgnoreTableOptions.set("False")
        # self.ValueIgnoreUserSettingsObjects.set("False")
        # self.ValueIgnoreWhitespace.set("True")
        # self.ValueIgnoreWithNocheckOnCheckConstraints.set("False")
        # self.ValueIgnoreWithNocheckOnForeignKeys.set("False")
        # self.ValueIncludeCompositeObjects.set("False")
        # self.ValueIncludeTransactionalScripts.set("False")
        # self.ValueNoAlterStatementsToChangeClrTypes.set("False")
        # self.ValuePopulateFilesOnFilegroups.set("True")
        # self.ValueRegisterDataTierApplication.set("False")
        # self.ValueRunDeploymentPlanExecutors.set("False")
        # self.ValueScriptDatabaseCollation.set("False")
        # self.ValueScriptDatabaseCompatibility.set("True")
        # self.ValueScriptDatabaseOptions.set("True")
        # self.ValueScriptDeployStateChecks.set("False")
        # self.ValueScriptFileSize.set("False")
        # self.ValueScriptNewConstraintValidation.set("True")
        # self.ValueScriptRefreshModule.set("True")
        # self.ValueStorage.set("Memory")
        # self.ValueTreatVerificationErrorsAsWarnings.set("False")
        # self.ValueUnmodifiableObjectWarnings.set("True")
        # self.ValueVerifyCollationCompatibility.set("True")
        # self.ValueVerifyDeployment.set("True")
        # ###########################################################################
        # ###########################################################################


        # Declare variables CHECKBUTTON for DoNotDropObjectType objects #########################
        ###########################################################################
        self.DoNotDropObjectTypesAggregates = BooleanVar()
        self.DoNotDropObjectTypesApplicationRoles = BooleanVar()
        self.DoNotDropObjectTypesAssemblies = BooleanVar()
        self.DoNotDropObjectTypesAsymmetricKeys = BooleanVar()
        self.DoNotDropObjectTypesBrokerPriorities = BooleanVar()
        self.DoNotDropObjectTypesCertificates = BooleanVar()
        self.DoNotDropObjectTypesContracts = BooleanVar()
        self.DoNotDropObjectTypesDatabaseRoles = BooleanVar()
        self.DoNotDropObjectTypesDatabaseTriggers = BooleanVar()
        self.DoNotDropObjectTypesDefaults = BooleanVar()
        self.DoNotDropObjectTypesExtendedProperties = BooleanVar()
        self.DoNotDropObjectTypesFilegroups = BooleanVar()
        self.DoNotDropObjectTypesFileTables = BooleanVar()
        self.DoNotDropObjectTypesFullTextCatalogs = BooleanVar()
        self.DoNotDropObjectTypesFullTextStoplists = BooleanVar()
        self.DoNotDropObjectTypesMessageTypes = BooleanVar()
        self.DoNotDropObjectTypesPartitionFunctions = BooleanVar()
        self.DoNotDropObjectTypesPartitionSchemes = BooleanVar()
        self.DoNotDropObjectTypesPermissions = BooleanVar()
        self.DoNotDropObjectTypesQueues = BooleanVar()
        self.DoNotDropObjectTypesRemoteServiceBindings = BooleanVar()
        self.DoNotDropObjectTypesRoleMembership = BooleanVar()
        self.DoNotDropObjectTypesRules = BooleanVar()
        self.DoNotDropObjectTypesScalarValuedFunctions = BooleanVar()
        self.DoNotDropObjectTypesSearchPropertyLists = BooleanVar()
        self.DoNotDropObjectTypesSequences = BooleanVar()
        self.DoNotDropObjectTypesServices = BooleanVar()
        self.DoNotDropObjectTypesSignatures = BooleanVar()
        self.DoNotDropObjectTypesStoredProcedures = BooleanVar()
        self.DoNotDropObjectTypesSymmetricKeys = BooleanVar()
        self.DoNotDropObjectTypesSynonyms = BooleanVar()
        self.DoNotDropObjectTypesTables = BooleanVar()
        self.DoNotDropObjectTypesTableValuedFunctions = BooleanVar()
        self.DoNotDropObjectTypesUserDefinedDataTypes = BooleanVar()
        self.DoNotDropObjectTypesUserDefinedTableTypes = BooleanVar()
        self.DoNotDropObjectTypesClrUserDefinedTypes = BooleanVar()
        self.DoNotDropObjectTypesUsers = BooleanVar()
        self.DoNotDropObjectTypesViews = BooleanVar()
        self.DoNotDropObjectTypesXmlSchemaCollections = BooleanVar()
        self.DoNotDropObjectTypesAudits = BooleanVar()
        self.DoNotDropObjectTypesCredentials = BooleanVar()
        self.DoNotDropObjectTypesCryptographicProviders = BooleanVar()
        self.DoNotDropObjectTypesDatabaseAuditSpecifications = BooleanVar()
        self.DoNotDropObjectTypesEndpoints = BooleanVar()
        self.DoNotDropObjectTypesErrorMessages = BooleanVar()
        self.DoNotDropObjectTypesEventNotifications = BooleanVar()
        self.DoNotDropObjectTypesEventSessions = BooleanVar()
        self.DoNotDropObjectTypesLinkedServerLogins = BooleanVar()
        self.DoNotDropObjectTypesLinkedServers = BooleanVar()
        self.DoNotDropObjectTypesLogins = BooleanVar()
        self.DoNotDropObjectTypesRoutes = BooleanVar()
        self.DoNotDropObjectTypesServerAuditSpecifications = BooleanVar()
        self.DoNotDropObjectTypesServerRoleMembership = BooleanVar()
        self.DoNotDropObjectTypesServerRoles = BooleanVar()
        self.DoNotDropObjectTypesServerTriggers = BooleanVar()
        ###########################################################################
        ###########################################################################

        # #Set variables CHECKBUTTON for DoNotDropObjectType objects#########################
        # ###########################################################################
        # self.DoNotDropObjectTypesAggregates.set(False)
        # self.DoNotDropObjectTypesApplicationRoles.set(False)
        # self.DoNotDropObjectTypesAssemblies.set(False)
        # self.DoNotDropObjectTypesAsymmetricKeys.set(False)
        # self.DoNotDropObjectTypesBrokerPriorities.set(False)
        # self.DoNotDropObjectTypesCertificates.set(False)
        # self.DoNotDropObjectTypesContracts.set(False)
        # self.DoNotDropObjectTypesDatabaseRoles.set(False)
        # self.DoNotDropObjectTypesDatabaseTriggers.set(False)
        # self.DoNotDropObjectTypesDefaults.set(False)
        # self.DoNotDropObjectTypesExtendedProperties.set(False)
        # self.DoNotDropObjectTypesFilegroups.set(False)
        # self.DoNotDropObjectTypesFileTables.set(False)
        # self.DoNotDropObjectTypesFullTextCatalogs.set(False)
        # self.DoNotDropObjectTypesFullTextStoplists.set(False)
        # self.DoNotDropObjectTypesMessageTypes.set(False)
        # self.DoNotDropObjectTypesPartitionFunctions.set(False)
        # self.DoNotDropObjectTypesPartitionSchemes.set(False)
        # self.DoNotDropObjectTypesPermissions.set(False)
        # self.DoNotDropObjectTypesQueues.set(False)
        # self.DoNotDropObjectTypesRemoteServiceBindings.set(False)
        # self.DoNotDropObjectTypesRoleMembership.set(False)
        # self.DoNotDropObjectTypesRules.set(False)
        # self.DoNotDropObjectTypesScalarValuedFunctions.set(False)
        # self.DoNotDropObjectTypesSearchPropertyLists.set(False)
        # self.DoNotDropObjectTypesSequences.set(False)
        # self.DoNotDropObjectTypesServices.set(False)
        # self.DoNotDropObjectTypesSignatures.set(False)
        # self.DoNotDropObjectTypesStoredProcedures.set(False)
        # self.DoNotDropObjectTypesSymmetricKeys.set(False)
        # self.DoNotDropObjectTypesSynonyms.set(False)
        # self.DoNotDropObjectTypesTables.set(False)
        # self.DoNotDropObjectTypesTableValuedFunctions.set(False)
        # self.DoNotDropObjectTypesUserDefinedDataTypes.set(False)
        # self.DoNotDropObjectTypesUserDefinedTableTypes.set(False)
        # self.DoNotDropObjectTypesClrUserDefinedTypes.set(False)
        # self.DoNotDropObjectTypesUsers.set(False)
        # self.DoNotDropObjectTypesViews.set(False)
        # self.DoNotDropObjectTypesXmlSchemaCollections.set(False)
        # self.DoNotDropObjectTypesAudits.set(False)
        # self.DoNotDropObjectTypesCredentials.set(False)
        # self.DoNotDropObjectTypesCryptographicProviders.set(False)
        # self.DoNotDropObjectTypesDatabaseAuditSpecifications.set(False)
        # self.DoNotDropObjectTypesEndpoints.set(False)
        # self.DoNotDropObjectTypesErrorMessages.set(False)
        # self.DoNotDropObjectTypesEventNotifications.set(False)
        # self.DoNotDropObjectTypesEventSessions.set(False)
        # self.DoNotDropObjectTypesLinkedServerLogins.set(False)
        # self.DoNotDropObjectTypesRoutes.set(False)
        # self.DoNotDropObjectTypesServerAuditSpecifications.set(False)
        # self.DoNotDropObjectTypesServerRoleMembership.set(False)
        # self.DoNotDropObjectTypesServerRoles.set(False)
        # self.DoNotDropObjectTypesServerTriggers.set(False)
        # ###########################################################################
        # ###########################################################################


        # Declare variables CHECKHUTTON for ExcludeObjectType objects ##########################
        ###########################################################################
        self.ExcludeObjectTypesAggregates = BooleanVar()
        self.ExcludeObjectTypesApplicationRoles = BooleanVar()
        self.ExcludeObjectTypesAssemblies = BooleanVar()
        self.ExcludeObjectTypesAsymmetricKeys = BooleanVar()
        self.ExcludeObjectTypesBrokerPriorities = BooleanVar()
        self.ExcludeObjectTypesCertificates = BooleanVar()
        self.ExcludeObjectTypesContracts = BooleanVar()
        self.ExcludeObjectTypesDatabaseRoles = BooleanVar()
        self.ExcludeObjectTypesDatabaseTriggers = BooleanVar()
        self.ExcludeObjectTypesDefaults = BooleanVar()
        self.ExcludeObjectTypesExtendedProperties = BooleanVar()
        self.ExcludeObjectTypesFilegroups = BooleanVar()
        self.ExcludeObjectTypesFileTables = BooleanVar()
        self.ExcludeObjectTypesFullTextCatalogs = BooleanVar()
        self.ExcludeObjectTypesFullTextStoplists = BooleanVar()
        self.ExcludeObjectTypesMessageTypes = BooleanVar()
        self.ExcludeObjectTypesPartitionFunctions = BooleanVar()
        self.ExcludeObjectTypesPartitionSchemes = BooleanVar()
        self.ExcludeObjectTypesPermissions = BooleanVar()
        self.ExcludeObjectTypesQueues = BooleanVar()
        self.ExcludeObjectTypesRemoteServiceBindings = BooleanVar()
        self.ExcludeObjectTypesRoleMembership = BooleanVar()
        self.ExcludeObjectTypesRules = BooleanVar()
        self.ExcludeObjectTypesScalarValuedFunctions = BooleanVar()
        self.ExcludeObjectTypesSearchPropertyLists = BooleanVar()
        self.ExcludeObjectTypesSequences = BooleanVar()
        self.ExcludeObjectTypesServices = BooleanVar()
        self.ExcludeObjectTypesSignatures = BooleanVar()
        self.ExcludeObjectTypesStoredProcedures = BooleanVar()
        self.ExcludeObjectTypesSymmetricKeys = BooleanVar()
        self.ExcludeObjectTypesSynonyms = BooleanVar()
        self.ExcludeObjectTypesTables = BooleanVar()
        self.ExcludeObjectTypesTableValuedFunctions = BooleanVar()
        self.ExcludeObjectTypesUserDefinedDataTypes = BooleanVar()
        self.ExcludeObjectTypesUserDefinedTableTypes = BooleanVar()
        self.ExcludeObjectTypesClrUserDefinedTypes = BooleanVar()
        self.ExcludeObjectTypesUsers = BooleanVar()
        self.ExcludeObjectTypesViews = BooleanVar()
        self.ExcludeObjectTypesXmlSchemaCollections = BooleanVar()
        self.ExcludeObjectTypesAudits = BooleanVar()
        self.ExcludeObjectTypesCredentials = BooleanVar()
        self.ExcludeObjectTypesCryptographicProviders = BooleanVar()
        self.ExcludeObjectTypesDatabaseAuditSpecifications = BooleanVar()
        self.ExcludeObjectTypesEndpoints = BooleanVar()
        self.ExcludeObjectTypesErrorMessages = BooleanVar()
        self.ExcludeObjectTypesEventNotifications = BooleanVar()
        self.ExcludeObjectTypesEventSessions = BooleanVar()
        self.ExcludeObjectTypesLinkedServerLogins = BooleanVar()
        self.ExcludeObjectTypesLinkedServers = BooleanVar()
        self.ExcludeObjectTypesLogins = BooleanVar()
        self.ExcludeObjectTypesRoutes = BooleanVar()
        self.ExcludeObjectTypesServerAuditSpecifications = BooleanVar()
        self.ExcludeObjectTypesServerRoleMembership = BooleanVar()
        self.ExcludeObjectTypesServerRoles = BooleanVar()
        self.ExcludeObjectTypesServerTriggers = BooleanVar()
        ###########################################################################
        ###########################################################################



        # #Set variables CHECKBUTTON for ExcludeObjectType objects ##########################
        # ###########################################################################
        # self.ExcludeObjectTypesAggregates.set(False)
        # self.ExcludeObjectTypesApplicationRoles.set(False)
        # self.ExcludeObjectTypesAssemblies.set(False)
        # self.ExcludeObjectTypesAsymmetricKeys.set(False)
        # self.ExcludeObjectTypesBrokerPriorities.set(False)
        # self.ExcludeObjectTypesCertificates.set(False)
        # self.ExcludeObjectTypesContracts.set(False)
        # self.ExcludeObjectTypesDatabaseRoles.set(False)
        # self.ExcludeObjectTypesDatabaseTriggers.set(False)
        # self.ExcludeObjectTypesDefaults.set(False)
        # self.ExcludeObjectTypesExtendedProperties.set(False)
        # self.ExcludeObjectTypesFilegroups.set(False)
        # self.ExcludeObjectTypesFileTables.set(False)
        # self.ExcludeObjectTypesFullTextCatalogs.set(False)
        # self.ExcludeObjectTypesFullTextStoplists.set(False)
        # self.ExcludeObjectTypesMessageTypes.set(False)
        # self.ExcludeObjectTypesPartitionFunctions.set(False)
        # self.ExcludeObjectTypesPartitionSchemes.set(False)
        # self.ExcludeObjectTypesPermissions.set(False)
        # self.ExcludeObjectTypesQueues.set(False)
        # self.ExcludeObjectTypesRemoteServiceBindings.set(False)
        # self.ExcludeObjectTypesRoleMembership.set(False)
        # self.ExcludeObjectTypesRules.set(False)
        # self.ExcludeObjectTypesScalarValuedFunctions.set(False)
        # self.ExcludeObjectTypesSearchPropertyLists.set(False)
        # self.ExcludeObjectTypesSequences.set(False)
        # self.ExcludeObjectTypesServices.set(False)
        # self.ExcludeObjectTypesSignatures.set(False)
        # self.ExcludeObjectTypesStoredProcedures.set(False)
        # self.ExcludeObjectTypesSymmetricKeys.set(False)
        # self.ExcludeObjectTypesSynonyms.set(False)
        # self.ExcludeObjectTypesTables.set(False)
        # self.ExcludeObjectTypesTableValuedFunctions.set(False)
        # self.ExcludeObjectTypesUserDefinedDataTypes.set(False)
        # self.ExcludeObjectTypesUserDefinedTableTypes.set(False)
        # self.ExcludeObjectTypesClrUserDefinedTypes.set(False)
        # self.ExcludeObjectTypesUsers.set(False)
        # self.ExcludeObjectTypesViews.set(False)
        # self.ExcludeObjectTypesXmlSchemaCollections.set(False)
        # self.ExcludeObjectTypesAudits.set(False)
        # self.ExcludeObjectTypesCredentials.set(False)
        # self.ExcludeObjectTypesCryptographicProviders.set(False)
        # self.ExcludeObjectTypesDatabaseAuditSpecifications.set(False)
        # self.ExcludeObjectTypesEndpoints.set(False)
        # self.ExcludeObjectTypesErrorMessages.set(False)
        # self.ExcludeObjectTypesEventNotifications.set(False)
        # self.ExcludeObjectTypesEventSessions.set(False)
        # self.ExcludeObjectTypesLinkedServerLogins.set(False)
        # self.ExcludeObjectTypesRoutes.set(False)
        # self.ExcludeObjectTypesServerAuditSpecifications.set(False)
        # self.ExcludeObjectTypesServerRoleMembership.set(False)
        # self.ExcludeObjectTypesServerRoles.set(False)
        # self.ExcludeObjectTypesServerTriggers.set(False)
        # ###########################################################################
        # ###########################################################################

        # Options to open JSON file
        self.options = {}
        self.options['defaultextension'] = '.json'
        self.options['filetypes'] = [('JSON files', '.json'), ('All files', '.*')]

        ########  Widgets  ######################################################################################
        #########################################################################################################
        # Create widgets ###########################################################
        # Label and Text Area for Pre-Deployment Script#############################
        self.PreDeploymentLabel = Label(self, text="Enter Pre-deployment script")
        self.PreDeploymentLabel.grid(row=0, column=0, sticky=W)

        self.PreDeploymentText = Text(self, width=40, height=5, wrap=WORD)
        self.PreDeploymentText.grid(row=0, column=1, columnspan=2, sticky=W)

        self.emetricImage = PhotoImage(file="emetric.gif")
        self.emetricImageLabel = Label(self, image=self.emetricImage)
        self.emetricImageLabel.grid(row=0, column=3, sticky=W)

        # Label and Textbox for Source Connection
        self.SourceServerLabel = Label(self, text="Source Server")
        self.SourceServerLabel.grid(row=1, column=0, sticky=W)
        self.SourceServerEntry = Entry(self)
        self.SourceServerEntry.grid(row=1, column=1, sticky=W)

        self.SourceDatabaseLabel = Label(self, text="Source Database")
        self.SourceDatabaseLabel.grid(row=2, column=0, sticky=W)
        self.SourceDatabaseEntry = Entry(self)
        self.SourceDatabaseEntry.grid(row=2, column=1, sticky=W)

        # Label and Textbox for Target Connection
        self.TargetServerLabel = Label(self, text="Target Server")
        self.TargetServerLabel.grid(row=1, column=2, sticky=W)
        self.TargetServerEntry = Entry(self)
        self.TargetServerEntry.grid(row=1, column=3, sticky=W)
        self.TargetServerEntry.insert(0, "localhost")

        self.TargetDatabaseLabel = Label(self, text="Target Database")
        self.TargetDatabaseLabel.grid(row=2, column=2, sticky=W)
        self.TargetDatabaseEntry = Entry(self)
        self.TargetDatabaseEntry.grid(row=2, column=3, sticky=W)

        # Windows Authentication checkboxes
        self.WinAuthSrcCheckButton = Checkbutton(self, text="Source Windows Auth", var=self.WinAuthSrcVariable, command=self.SrcCredentials_Visibility)
        self.WinAuthSrcCheckButton.grid(row=3, column=0, sticky=W)
        self.WinAuthTrgtCheckButton = Checkbutton(self, text="Target Windows Auth", var=self.WinAuthTrgtVariable, command=self.TrgtCredentials_Visibility)
        self.WinAuthTrgtCheckButton.grid(row=3, column=2, sticky=W)

        # Label and Textbox for Source Credentials
        self.SourceUsernameLabel = Label(self, text="Source Username")
        self.SourceUsernameEntry = Entry(self)
        self.SourcePasswordLabel = Label(self, text="Source Password")
        self.SourcePasswordEntry = Entry(self, show="*")

        # Label and Textbox for Target Credentials
        self.TargetUsernameLabel = Label(self, text="Target Username")
        self.TargetUsernameEntry = Entry(self)
        self.TargetPasswordLabel = Label(self, text="Target Password")
        self.TargetPasswordEntry = Entry(self, show="*")

        # Encryption connection checkboxes
        self.EncryptSrcCheckButton = Checkbutton(self, text="Source Encrypt Connection", var=self.EncryptSrcVariable)
        self.EncryptSrcCheckButton.grid(row=6, column=0, sticky=W)
        self.EncryptTrgtCheckButton = Checkbutton(self, text="Target Encrypt Connection", var=self.EncryptTrgtVariable)
        self.EncryptTrgtCheckButton.grid(row=6, column=2, sticky=W)

        # Set Deployment Property default parameters
        self.SetDplyPropertyCheckButton = Checkbutton(self, text="Set Deployment Properties", var=self.SetDplyPropertyVariable, command=self.DplyScroll_Visibility)
        self.SetDplyPropertyCheckButton.grid(row=7, column=2, sticky=W)

        # Button(self, text="Ok", command=self.print_variable_values).grid(row=20, column=1, sticky=W)

        # Create Scrolling bar for Extract Properties################################
        ############################################################################
        # def ExtPrpWidgetsFunction():
        #     Checkbutton(ExtPrpCanvasFrame,var=self.ChkButtonAllowDropBlockingAssemblies).grid(row=0, column=0, sticky=W)
        #     Label(ExtPrpCanvasFrame,text="AllowDropBlockingAssemblies").grid(row=0,column=1,sticky=W)
        #
        # def configExtPrpCanvasFunction(event):
        #     ExtPrpCanvas.configure(scrollregion=ExtPrpCanvas.bbox("all"),width=200,height=200)
        #
        # ExtPrpFrame=Frame(self,relief=GROOVE,width=50,height=100, bd=1)
        # ExtPrpFrame.grid(row=7,column=0,sticky=W)
        #
        # ExtPrpCanvas=Canvas(ExtPrpFrame)
        # ExtPrpCanvasFrame=Frame(ExtPrpCanvas)
        # ExtPrpScrollbar=Scrollbar(ExtPrpFrame,orient="vertical",command=ExtPrpCanvas.yview)
        # ExtPrpCanvas.configure(yscrollcommand=ExtPrpScrollbar.set)
        #
        # ExtPrpScrollbar.pack(side="right",fill="y")
        # ExtPrpCanvas.pack(side="left")
        # ExtPrpCanvas.create_window((0,0),window=ExtPrpCanvasFrame,anchor='nw')
        # ExtPrpCanvasFrame.bind("<Configure>",configExtPrpCanvasFunction)
        # ExtPrpWidgetsFunction()
        ############################################################################
        ############################################################################


        # Create Scrolling bar for Deploy Properties#################################
        ############################################################################
        def DplyPrpWidgetsFunction():
            # Checkbuttons, Labels and option menus #################################
            ########################################################################
            self.LblAllowDropBlockingAssemblies = Label(DplyPrpCanvasFrame, text="AllowDropBlockingAssemblies")
            self.LblAllowIncompatiblePlatform = Label(DplyPrpCanvasFrame, text="AllowIncompatiblePlatform")
            self.LblBackupDatabaseBeforeChanges = Label(DplyPrpCanvasFrame, text="BackupDatabaseBeforeChanges")
            self.LblBlockOnPossibleDataLoss = Label(DplyPrpCanvasFrame, text="BlockOnPossibleDataLoss")
            self.LblBlockWhenDriftDetected = Label(DplyPrpCanvasFrame, text="BlockWhenDriftDetected")
            self.LblCommandTimeout = Label(DplyPrpCanvasFrame, text="CommandTimeout")
            self.LblCommentOutSetVarDeclarations = Label(DplyPrpCanvasFrame, text="CommentOutSetVarDeclarations")
            self.LblCompareUsingTargetCollation = Label(DplyPrpCanvasFrame, text="CompareUsingTargetCollation")
            self.LblCreateNewDatabase = Label(DplyPrpCanvasFrame, text="CreateNewDatabase")
            self.LblDeployDatabaseInSingleUserMode = Label(DplyPrpCanvasFrame, text="DeployDatabaseInSingleUserMode")
            self.LblDisableAndReenableDdlTriggers = Label(DplyPrpCanvasFrame, text="DisableAndReenableDdlTriggers")
            self.LblDoNotAlterChangeDataCaptureObjects = Label(DplyPrpCanvasFrame, text="DoNotAlterChangeDataCaptureObjects")
            self.LblDoNotAlterReplicatedObjects = Label(DplyPrpCanvasFrame, text="DoNotAlterReplicatedObjects")
            self.LblDoNotDropObjectTypes = Label(DplyPrpCanvasFrame, text="DoNotDropObjectTypes")
            self.LblDropConstraintsNotInSource = Label(DplyPrpCanvasFrame, text="DropConstraintsNotInSource")
            self.LblDropDmlTriggersNotInSource = Label(DplyPrpCanvasFrame, text="DropDmlTriggersNotInSource")
            self.LblDropExtendedPropertiesNotInSource = Label(DplyPrpCanvasFrame, text="DropExtendedPropertiesNotInSource")
            self.LblDropIndexesNotInSource = Label(DplyPrpCanvasFrame, text="DropIndexesNotInSource")
            self.LblDropObjectsNotInSource = Label(DplyPrpCanvasFrame, text="DropObjectsNotInSource")
            self.LblDropPermissionsNotInSource = Label(DplyPrpCanvasFrame, text="DropPermissionsNotInSource")
            self.LblDropRoleMembersNotInSource = Label(DplyPrpCanvasFrame, text="DropRoleMembersNotInSource")
            self.LblExcludeObjectTypes = Label(DplyPrpCanvasFrame, text="ExcludeObjectTypes")
            self.LblGenerateSmartDefaults = Label(DplyPrpCanvasFrame, text="GenerateSmartDefaults")
            self.LblIgnoreAnsiNulls = Label(DplyPrpCanvasFrame, text="IgnoreAnsiNulls")
            self.LblIgnoreAuthorizer = Label(DplyPrpCanvasFrame, text="IgnoreAuthorizer")
            self.LblIgnoreColumnCollation = Label(DplyPrpCanvasFrame, text="IgnoreColumnCollation")
            self.LblIgnoreComments = Label(DplyPrpCanvasFrame, text="IgnoreComments")
            self.LblIgnoreCryptographicProviderFilePath = Label(DplyPrpCanvasFrame, text="IgnoreCryptographicProviderFilePath")
            self.LblIgnoreDdlTriggerOrder = Label(DplyPrpCanvasFrame, text="IgnoreDdlTriggerOrder")
            self.LblIgnoreDdlTriggerState = Label(DplyPrpCanvasFrame, text="IgnoreDdlTriggerState")
            self.LblIgnoreDefaultSchema = Label(DplyPrpCanvasFrame, text="IgnoreDefaultSchema")
            self.LblIgnoreDmlTriggerOrder = Label(DplyPrpCanvasFrame, text="IgnoreDmlTriggerOrder")
            self.LblIgnoreDmlTriggerState = Label(DplyPrpCanvasFrame, text="IgnoreDmlTriggerState")
            self.LblIgnoreExtendedProperties = Label(DplyPrpCanvasFrame, text="IgnoreExtendedProperties")
            self.LblIgnoreFileAndLogFilePath = Label(DplyPrpCanvasFrame, text="IgnoreFileAndLogFilePath")
            self.LblIgnoreFilegroupPlacement = Label(DplyPrpCanvasFrame, text="IgnoreFilegroupPlacement")
            self.LblIgnoreFileSize = Label(DplyPrpCanvasFrame, text="IgnoreFileSize")
            self.LblIgnoreFillFactor = Label(DplyPrpCanvasFrame, text="IgnoreFillFactor")
            self.LblIgnoreFullTextCatalogFilePath = Label(DplyPrpCanvasFrame, text="IgnoreFullTextCatalogFilePath")
            self.LblIgnoreIdentitySeed = Label(DplyPrpCanvasFrame, text="IgnoreIdentitySeed")
            self.LblIgnoreIncrement = Label(DplyPrpCanvasFrame, text="IgnoreIncrement")
            self.LblIgnoreIndexOptions = Label(DplyPrpCanvasFrame, text="IgnoreIndexOptions")
            self.LblIgnoreIndexPadding = Label(DplyPrpCanvasFrame, text="IgnoreIndexPadding")
            self.LblIgnoreKeywordCasing = Label(DplyPrpCanvasFrame, text="IgnoreKeywordCasing")
            self.LblIgnoreLockHintsOnIndexes = Label(DplyPrpCanvasFrame, text="IgnoreLockHintsOnIndexes")
            self.LblIgnoreLoginSids = Label(DplyPrpCanvasFrame, text="IgnoreLoginSids")
            self.LblIgnoreNotForReplication = Label(DplyPrpCanvasFrame, text="IgnoreNotForReplication")
            self.LblIgnoreObjectPlacementOnPartitionScheme = Label(DplyPrpCanvasFrame, text="IgnoreObjectPlacementOnPartitionScheme")
            self.LblIgnorePartitionSchemes = Label(DplyPrpCanvasFrame, text="IgnorePartitionSchemes")
            self.LblIgnorePermissions = Label(DplyPrpCanvasFrame, text="IgnorePermissions")
            self.LblIgnoreQuotedIdentifiers = Label(DplyPrpCanvasFrame, text="IgnoreQuotedIdentifiers")
            self.LblIgnoreRoleMembership = Label(DplyPrpCanvasFrame, text="IgnoreRoleMembership")
            self.LblIgnoreRouteLifetime = Label(DplyPrpCanvasFrame, text="IgnoreRouteLifetime")
            self.LblIgnoreSemicolonBetweenStatements = Label(DplyPrpCanvasFrame, text="IgnoreSemicolonBetweenStatements")
            self.LblIgnoreTableOptions = Label(DplyPrpCanvasFrame, text="IgnoreTableOptions")
            self.LblIgnoreUserSettingsObjects = Label(DplyPrpCanvasFrame, text="IgnoreUserSettingsObjects")
            self.LblIgnoreWhitespace = Label(DplyPrpCanvasFrame, text="IgnoreWhitespace")
            self.LblIgnoreWithNocheckOnCheckConstraints = Label(DplyPrpCanvasFrame, text="IgnoreWithNocheckOnCheckConstraints")
            self.LblIgnoreWithNocheckOnForeignKeys = Label(DplyPrpCanvasFrame, text="IgnoreWithNocheckOnForeignKeys")
            self.LblIncludeCompositeObjects = Label(DplyPrpCanvasFrame, text="IncludeCompositeObjects")
            self.LblIncludeTransactionalScripts = Label(DplyPrpCanvasFrame, text="IncludeTransactionalScripts")
            self.LblNoAlterStatementsToChangeClrTypes = Label(DplyPrpCanvasFrame, text="NoAlterStatementsToChangeClrTypes")
            self.LblPopulateFilesOnFilegroups = Label(DplyPrpCanvasFrame, text="PopulateFilesOnFilegroups")
            self.LblRegisterDataTierApplication = Label(DplyPrpCanvasFrame, text="RegisterDataTierApplication")
            self.LblRunDeploymentPlanExecutors = Label(DplyPrpCanvasFrame, text="RunDeploymentPlanExecutors")
            self.LblScriptDatabaseCollation = Label(DplyPrpCanvasFrame, text="ScriptDatabaseCollation")
            self.LblScriptDatabaseCompatibility = Label(DplyPrpCanvasFrame, text="ScriptDatabaseCompatibility")
            self.LblScriptDatabaseOptions = Label(DplyPrpCanvasFrame, text="ScriptDatabaseOptions")
            self.LblScriptDeployStateChecks = Label(DplyPrpCanvasFrame, text="ScriptDeployStateChecks")
            self.LblScriptFileSize = Label(DplyPrpCanvasFrame, text="ScriptFileSize")
            self.LblScriptNewConstraintValidation = Label(DplyPrpCanvasFrame, text="ScriptNewConstraintValidation")
            self.LblScriptRefreshModule = Label(DplyPrpCanvasFrame, text="ScriptRefreshModule")
            self.LblStorage = Label(DplyPrpCanvasFrame, text="Storage")
            self.LblTreatVerificationErrorsAsWarnings = Label(DplyPrpCanvasFrame, text="TreatVerificationErrorsAsWarnings")
            self.LblUnmodifiableObjectWarnings = Label(DplyPrpCanvasFrame, text="UnmodifiableObjectWarnings")
            self.LblVerifyCollationCompatibility = Label(DplyPrpCanvasFrame, text="VerifyCollationCompatibility")
            self.LblVerifyDeployment = Label(DplyPrpCanvasFrame, text="VerifyDeployment")

            # Insert labels inside the grid ############################################################################################
            self.LblAllowDropBlockingAssemblies.grid(row=0, column=1, sticky=W)
            self.LblAllowIncompatiblePlatform.grid(row=1, column=1, sticky=W)
            self.LblBackupDatabaseBeforeChanges.grid(row=2, column=1, sticky=W)
            self.LblBlockOnPossibleDataLoss.grid(row=3, column=1, sticky=W)
            self.LblBlockWhenDriftDetected.grid(row=4, column=1, sticky=W)
            self.LblCommandTimeout.grid(row=5, column=1, sticky=W)
            self.LblCommentOutSetVarDeclarations.grid(row=6, column=1, sticky=W)
            self.LblCompareUsingTargetCollation.grid(row=7, column=1, sticky=W)
            self.LblCreateNewDatabase.grid(row=8, column=1, sticky=W)
            self.LblDeployDatabaseInSingleUserMode.grid(row=9, column=1, sticky=W)
            self.LblDisableAndReenableDdlTriggers.grid(row=10, column=1, sticky=W)
            self.LblDoNotAlterChangeDataCaptureObjects.grid(row=11, column=1, sticky=W)
            self.LblDoNotAlterReplicatedObjects.grid(row=12, column=1, sticky=W)
            self.LblDoNotDropObjectTypes.grid(row=13, column=1, sticky=W)
            self.LblDropConstraintsNotInSource.grid(row=14, column=1, sticky=W)
            self.LblDropDmlTriggersNotInSource.grid(row=15, column=1, sticky=W)
            self.LblDropExtendedPropertiesNotInSource.grid(row=16, column=1, sticky=W)
            self.LblDropIndexesNotInSource.grid(row=17, column=1, sticky=W)
            self.LblDropObjectsNotInSource.grid(row=18, column=1, sticky=W)
            self.LblDropPermissionsNotInSource.grid(row=19, column=1, sticky=W)
            self.LblDropRoleMembersNotInSource.grid(row=20, column=1, sticky=W)
            self.LblExcludeObjectTypes.grid(row=21, column=1, sticky=W)
            self.LblGenerateSmartDefaults.grid(row=22, column=1, sticky=W)
            self.LblIgnoreAnsiNulls.grid(row=23, column=1, sticky=W)
            self.LblIgnoreAuthorizer.grid(row=24, column=1, sticky=W)
            self.LblIgnoreColumnCollation.grid(row=25, column=1, sticky=W)
            self.LblIgnoreComments.grid(row=26, column=1, sticky=W)
            self.LblIgnoreCryptographicProviderFilePath.grid(row=27, column=1, sticky=W)
            self.LblIgnoreDdlTriggerOrder.grid(row=28, column=1, sticky=W)
            self.LblIgnoreDdlTriggerState.grid(row=29, column=1, sticky=W)
            self.LblIgnoreDefaultSchema.grid(row=30, column=1, sticky=W)
            self.LblIgnoreDmlTriggerOrder.grid(row=31, column=1, sticky=W)
            self.LblIgnoreDmlTriggerState.grid(row=32, column=1, sticky=W)
            self.LblIgnoreExtendedProperties.grid(row=33, column=1, sticky=W)
            self.LblIgnoreFileAndLogFilePath.grid(row=34, column=1, sticky=W)
            self.LblIgnoreFilegroupPlacement.grid(row=35, column=1, sticky=W)
            self.LblIgnoreFileSize.grid(row=36, column=1, sticky=W)
            self.LblIgnoreFillFactor.grid(row=37, column=1, sticky=W)
            self.LblIgnoreFullTextCatalogFilePath.grid(row=38, column=1, sticky=W)
            self.LblIgnoreIdentitySeed.grid(row=39, column=1, sticky=W)
            self.LblIgnoreIncrement.grid(row=40, column=1, sticky=W)
            self.LblIgnoreIndexOptions.grid(row=41, column=1, sticky=W)
            self.LblIgnoreIndexPadding.grid(row=42, column=1, sticky=W)
            self.LblIgnoreKeywordCasing.grid(row=43, column=1, sticky=W)
            self.LblIgnoreLockHintsOnIndexes.grid(row=44, column=1, sticky=W)
            self.LblIgnoreLoginSids.grid(row=45, column=1, sticky=W)
            self.LblIgnoreNotForReplication.grid(row=46, column=1, sticky=W)
            self.LblIgnoreObjectPlacementOnPartitionScheme.grid(row=47, column=1, sticky=W)
            self.LblIgnorePartitionSchemes.grid(row=48, column=1, sticky=W)
            self.LblIgnorePermissions.grid(row=49, column=1, sticky=W)
            self.LblIgnoreQuotedIdentifiers.grid(row=50, column=1, sticky=W)
            self.LblIgnoreRoleMembership.grid(row=51, column=1, sticky=W)
            self.LblIgnoreRouteLifetime.grid(row=52, column=1, sticky=W)
            self.LblIgnoreSemicolonBetweenStatements.grid(row=53, column=1, sticky=W)
            self.LblIgnoreTableOptions.grid(row=54, column=1, sticky=W)
            self.LblIgnoreUserSettingsObjects.grid(row=55, column=1, sticky=W)
            self.LblIgnoreWhitespace.grid(row=56, column=1, sticky=W)
            self.LblIgnoreWithNocheckOnCheckConstraints.grid(row=57, column=1, sticky=W)
            self.LblIgnoreWithNocheckOnForeignKeys.grid(row=58, column=1, sticky=W)
            self.LblIncludeCompositeObjects.grid(row=59, column=1, sticky=W)
            self.LblIncludeTransactionalScripts.grid(row=60, column=1, sticky=W)
            self.LblNoAlterStatementsToChangeClrTypes.grid(row=61, column=1, sticky=W)
            self.LblPopulateFilesOnFilegroups.grid(row=62, column=1, sticky=W)
            self.LblRegisterDataTierApplication.grid(row=63, column=1, sticky=W)
            self.LblRunDeploymentPlanExecutors.grid(row=64, column=1, sticky=W)
            self.LblScriptDatabaseCollation.grid(row=65, column=1, sticky=W)
            self.LblScriptDatabaseCompatibility.grid(row=66, column=1, sticky=W)
            self.LblScriptDatabaseOptions.grid(row=67, column=1, sticky=W)
            self.LblScriptDeployStateChecks.grid(row=68, column=1, sticky=W)
            self.LblScriptFileSize.grid(row=69, column=1, sticky=W)
            self.LblScriptNewConstraintValidation.grid(row=70, column=1, sticky=W)
            self.LblScriptRefreshModule.grid(row=71, column=1, sticky=W)
            self.LblStorage.grid(row=72, column=1, sticky=W)
            self.LblTreatVerificationErrorsAsWarnings.grid(row=73, column=1, sticky=W)
            self.LblUnmodifiableObjectWarnings.grid(row=74, column=1, sticky=W)
            self.LblVerifyCollationCompatibility.grid(row=75, column=1, sticky=W)
            self.LblVerifyDeployment.grid(row=76, column=1, sticky=W)

            ###########################################################################################################################
            # Declare and create DROPDOWNS   ###########################################################################################
            self.EnDisValueAllowDropBlockingAssemblies = OptionMenu(DplyPrpCanvasFrame, self.ValueAllowDropBlockingAssemblies, "True", "False")
            self.EnDisValueAllowIncompatiblePlatform = OptionMenu(DplyPrpCanvasFrame, self.ValueAllowIncompatiblePlatform, "True", "False")
            self.EnDisValueBackupDatabaseBeforeChanges = OptionMenu(DplyPrpCanvasFrame, self.ValueBackupDatabaseBeforeChanges, "True", "False")
            self.EnDisValueBlockOnPossibleDataLoss = OptionMenu(DplyPrpCanvasFrame, self.ValueBlockOnPossibleDataLoss, "True", "False")
            self.EnDisValueBlockWhenDriftDetected = OptionMenu(DplyPrpCanvasFrame, self.ValueBlockWhenDriftDetected, "True", "False")
            self.EntryCommandTimeout = Entry(DplyPrpCanvasFrame, width=11, justify=RIGHT)
            # self.EntryCommandTimeout.insert(0, "60")

            self.EnDisValueCommentOutSetVarDeclarations = OptionMenu(DplyPrpCanvasFrame, self.ValueCommentOutSetVarDeclarations, "True", "False")
            self.EnDisValueCompareUsingTargetCollation = OptionMenu(DplyPrpCanvasFrame, self.ValueCompareUsingTargetCollation, "True", "False")
            self.EnDisValueCreateNewDatabase = OptionMenu(DplyPrpCanvasFrame, self.ValueCreateNewDatabase, "True", "False")
            self.EnDisValueDeployDatabaseInSingleUserMode = OptionMenu(DplyPrpCanvasFrame, self.ValueDeployDatabaseInSingleUserMode, "True", "False")
            self.EnDisValueDisableAndReenableDdlTriggers = OptionMenu(DplyPrpCanvasFrame, self.ValueDisableAndReenableDdlTriggers, "True", "False")
            self.EnDisValueDoNotAlterChangeDataCaptureObjects = OptionMenu(DplyPrpCanvasFrame, self.ValueDoNotAlterChangeDataCaptureObjects, "True", "False")
            self.EnDisValueDoNotAlterReplicatedObjects = OptionMenu(DplyPrpCanvasFrame, self.ValueDoNotAlterReplicatedObjects, "True", "False")

            self.EnDisValueDoNotDropObjectTypes = Button(DplyPrpCanvasFrame, text="Select Objects", command=self.DoNotDropObjectTypes)

            self.EnDisValueDropConstraintsNotInSource = OptionMenu(DplyPrpCanvasFrame, self.ValueDropConstraintsNotInSource, "True", "False")
            self.EnDisValueDropDmlTriggersNotInSource = OptionMenu(DplyPrpCanvasFrame, self.ValueDropDmlTriggersNotInSource, "True", "False")
            self.EnDisValueDropExtendedPropertiesNotInSource = OptionMenu(DplyPrpCanvasFrame, self.ValueDropExtendedPropertiesNotInSource, "True", "False")
            self.EnDisValueDropIndexesNotInSource = OptionMenu(DplyPrpCanvasFrame, self.ValueDropIndexesNotInSource, "True", "False")
            self.EnDisValueDropObjectsNotInSource = OptionMenu(DplyPrpCanvasFrame, self.ValueDropObjectsNotInSource, "True", "False")
            self.EnDisValueDropPermissionsNotInSource = OptionMenu(DplyPrpCanvasFrame, self.ValueDropPermissionsNotInSource, "True", "False")
            self.EnDisValueDropRoleMembersNotInSource = OptionMenu(DplyPrpCanvasFrame, self.ValueDropRoleMembersNotInSource, "True", "False")

            self.EnDisValueExcludeObjectTypes = Button(DplyPrpCanvasFrame, text="Select Objects", command=self.ExcludeObjectTypes)

            self.EnDisValueGenerateSmartDefaults = OptionMenu(DplyPrpCanvasFrame, self.ValueGenerateSmartDefaults, "True", "False")
            self.EnDisValueIgnoreAnsiNulls = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreAnsiNulls, "True", "False")
            self.EnDisValueIgnoreAuthorizer = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreAuthorizer, "True", "False")
            self.EnDisValueIgnoreColumnCollation = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreColumnCollation, "True", "False")
            self.EnDisValueIgnoreComments = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreComments, "True", "False")
            self.EnDisValueIgnoreCryptographicProviderFilePath = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreCryptographicProviderFilePath, "True", "False")
            self.EnDisValueIgnoreDdlTriggerOrder = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreDdlTriggerOrder, "True", "False")
            self.EnDisValueIgnoreDdlTriggerState = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreDdlTriggerState, "True", "False")
            self.EnDisValueIgnoreDefaultSchema = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreDefaultSchema, "True", "False")
            self.EnDisValueIgnoreDmlTriggerOrder = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreDmlTriggerOrder, "True", "False")
            self.EnDisValueIgnoreDmlTriggerState = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreDmlTriggerState, "True", "False")
            self.EnDisValueIgnoreExtendedProperties = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreExtendedProperties, "True", "False")
            self.EnDisValueIgnoreFileAndLogFilePath = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreFileAndLogFilePath, "True", "False")
            self.EnDisValueIgnoreFilegroupPlacement = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreFilegroupPlacement, "True", "False")
            self.EnDisValueIgnoreFileSize = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreFileSize, "True", "False")
            self.EnDisValueIgnoreFillFactor = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreFillFactor, "True", "False")
            self.EnDisValueIgnoreFullTextCatalogFilePath = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreFullTextCatalogFilePath, "True", "False")
            self.EnDisValueIgnoreIdentitySeed = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreIdentitySeed, "True", "False")
            self.EnDisValueIgnoreIncrement = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreIncrement, "True", "False")
            self.EnDisValueIgnoreIndexOptions = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreIndexOptions, "True", "False")
            self.EnDisValueIgnoreIndexPadding = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreIndexPadding, "True", "False")
            self.EnDisValueIgnoreKeywordCasing = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreKeywordCasing, "True", "False")
            self.EnDisValueIgnoreLockHintsOnIndexes = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreLockHintsOnIndexes, "True", "False")
            self.EnDisValueIgnoreLoginSids = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreLoginSids, "True", "False")
            self.EnDisValueIgnoreNotForReplication = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreNotForReplication, "True", "False")
            self.EnDisValueIgnoreObjectPlacementOnPartitionScheme = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreObjectPlacementOnPartitionScheme, "True",
                                                                               "False")
            self.EnDisValueIgnorePartitionSchemes = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnorePartitionSchemes, "True", "False")
            self.EnDisValueIgnorePermissions = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnorePermissions, "True", "False")
            self.EnDisValueIgnoreQuotedIdentifiers = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreQuotedIdentifiers, "True", "False")
            self.EnDisValueIgnoreRoleMembership = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreRoleMembership, "True", "False")
            self.EnDisValueIgnoreRouteLifetime = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreRouteLifetime, "True", "False")
            self.EnDisValueIgnoreSemicolonBetweenStatements = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreSemicolonBetweenStatements, "True", "False")
            self.EnDisValueIgnoreTableOptions = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreTableOptions, "True", "False")
            self.EnDisValueIgnoreUserSettingsObjects = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreUserSettingsObjects, "True", "False")
            self.EnDisValueIgnoreWhitespace = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreWhitespace, "True", "False")
            self.EnDisValueIgnoreWithNocheckOnCheckConstraints = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreWithNocheckOnCheckConstraints, "True", "False")
            self.EnDisValueIgnoreWithNocheckOnForeignKeys = OptionMenu(DplyPrpCanvasFrame, self.ValueIgnoreWithNocheckOnForeignKeys, "True", "False")
            self.EnDisValueIncludeCompositeObjects = OptionMenu(DplyPrpCanvasFrame, self.ValueIncludeCompositeObjects, "True", "False")
            self.EnDisValueIncludeTransactionalScripts = OptionMenu(DplyPrpCanvasFrame, self.ValueIncludeTransactionalScripts, "True", "False")
            self.EnDisValueNoAlterStatementsToChangeClrTypes = OptionMenu(DplyPrpCanvasFrame, self.ValueNoAlterStatementsToChangeClrTypes, "True", "False")
            self.EnDisValuePopulateFilesOnFilegroups = OptionMenu(DplyPrpCanvasFrame, self.ValuePopulateFilesOnFilegroups, "True", "False")
            self.EnDisValueRegisterDataTierApplication = OptionMenu(DplyPrpCanvasFrame, self.ValueRegisterDataTierApplication, "True", "False")
            self.EnDisValueRunDeploymentPlanExecutors = OptionMenu(DplyPrpCanvasFrame, self.ValueRunDeploymentPlanExecutors, "True", "False")
            self.EnDisValueScriptDatabaseCollation = OptionMenu(DplyPrpCanvasFrame, self.ValueScriptDatabaseCollation, "True", "False")
            self.EnDisValueScriptDatabaseCompatibility = OptionMenu(DplyPrpCanvasFrame, self.ValueScriptDatabaseCompatibility, "True", "False")
            self.EnDisValueScriptDatabaseOptions = OptionMenu(DplyPrpCanvasFrame, self.ValueScriptDatabaseOptions, "True", "False")
            self.EnDisValueScriptDeployStateChecks = OptionMenu(DplyPrpCanvasFrame, self.ValueScriptDeployStateChecks, "True", "False")
            self.EnDisValueScriptFileSize = OptionMenu(DplyPrpCanvasFrame, self.ValueScriptFileSize, "True", "False")
            self.EnDisValueScriptNewConstraintValidation = OptionMenu(DplyPrpCanvasFrame, self.ValueScriptNewConstraintValidation, "True", "False")
            self.EnDisValueScriptRefreshModule = OptionMenu(DplyPrpCanvasFrame, self.ValueScriptRefreshModule, "True", "False")
            self.EnDisValueStorage = OptionMenu(DplyPrpCanvasFrame, self.ValueStorage, "File", "Memory")
            self.EnDisValueTreatVerificationErrorsAsWarnings = OptionMenu(DplyPrpCanvasFrame, self.ValueTreatVerificationErrorsAsWarnings, "True", "False")
            self.EnDisValueUnmodifiableObjectWarnings = OptionMenu(DplyPrpCanvasFrame, self.ValueUnmodifiableObjectWarnings, "True", "False")
            self.EnDisValueVerifyCollationCompatibility = OptionMenu(DplyPrpCanvasFrame, self.ValueVerifyCollationCompatibility, "True", "False")
            self.EnDisValueVerifyDeployment = OptionMenu(DplyPrpCanvasFrame, self.ValueVerifyDeployment, "True", "False")

            # Put DROPDOWNS inside Grid
            self.EnDisValueAllowDropBlockingAssemblies.grid(row=0, column=2, sticky=W)
            self.EnDisValueAllowIncompatiblePlatform.grid(row=1, column=2, sticky=W)
            self.EnDisValueBackupDatabaseBeforeChanges.grid(row=2, column=2, sticky=W)
            self.EnDisValueBlockOnPossibleDataLoss.grid(row=3, column=2, sticky=W)
            self.EnDisValueBlockWhenDriftDetected.grid(row=4, column=2, sticky=W)
            self.EntryCommandTimeout.grid(row=5, column=2, sticky=W)
            self.EnDisValueCommentOutSetVarDeclarations.grid(row=6, column=2, sticky=W)
            self.EnDisValueCompareUsingTargetCollation.grid(row=7, column=2, sticky=W)
            self.EnDisValueCreateNewDatabase.grid(row=8, column=2, sticky=W)
            self.EnDisValueDeployDatabaseInSingleUserMode.grid(row=9, column=2, sticky=W)
            self.EnDisValueDisableAndReenableDdlTriggers.grid(row=10, column=2, sticky=W)
            self.EnDisValueDoNotAlterChangeDataCaptureObjects.grid(row=11, column=2, sticky=W)
            self.EnDisValueDoNotAlterReplicatedObjects.grid(row=12, column=2, sticky=W)
            self.EnDisValueDoNotDropObjectTypes.grid(row=13, column=2, sticky=W)
            self.EnDisValueDropConstraintsNotInSource.grid(row=14, column=2, sticky=W)
            self.EnDisValueDropDmlTriggersNotInSource.grid(row=15, column=2, sticky=W)
            self.EnDisValueDropExtendedPropertiesNotInSource.grid(row=16, column=2, sticky=W)
            self.EnDisValueDropIndexesNotInSource.grid(row=17, column=2, sticky=W)
            self.EnDisValueDropObjectsNotInSource.grid(row=18, column=2, sticky=W)
            self.EnDisValueDropPermissionsNotInSource.grid(row=19, column=2, sticky=W)
            self.EnDisValueDropRoleMembersNotInSource.grid(row=20, column=2, sticky=W)
            self.EnDisValueExcludeObjectTypes.grid(row=21, column=2, sticky=W)
            self.EnDisValueGenerateSmartDefaults.grid(row=22, column=2, sticky=W)
            self.EnDisValueIgnoreAnsiNulls.grid(row=23, column=2, sticky=W)
            self.EnDisValueIgnoreAuthorizer.grid(row=24, column=2, sticky=W)
            self.EnDisValueIgnoreColumnCollation.grid(row=25, column=2, sticky=W)
            self.EnDisValueIgnoreComments.grid(row=26, column=2, sticky=W)
            self.EnDisValueIgnoreCryptographicProviderFilePath.grid(row=27, column=2, sticky=W)
            self.EnDisValueIgnoreDdlTriggerOrder.grid(row=28, column=2, sticky=W)
            self.EnDisValueIgnoreDdlTriggerState.grid(row=29, column=2, sticky=W)
            self.EnDisValueIgnoreDefaultSchema.grid(row=30, column=2, sticky=W)
            self.EnDisValueIgnoreDmlTriggerOrder.grid(row=31, column=2, sticky=W)
            self.EnDisValueIgnoreDmlTriggerState.grid(row=32, column=2, sticky=W)
            self.EnDisValueIgnoreExtendedProperties.grid(row=33, column=2, sticky=W)
            self.EnDisValueIgnoreFileAndLogFilePath.grid(row=34, column=2, sticky=W)
            self.EnDisValueIgnoreFilegroupPlacement.grid(row=35, column=2, sticky=W)
            self.EnDisValueIgnoreFileSize.grid(row=36, column=2, sticky=W)
            self.EnDisValueIgnoreFillFactor.grid(row=37, column=2, sticky=W)
            self.EnDisValueIgnoreFullTextCatalogFilePath.grid(row=38, column=2, sticky=W)
            self.EnDisValueIgnoreIdentitySeed.grid(row=39, column=2, sticky=W)
            self.EnDisValueIgnoreIncrement.grid(row=40, column=2, sticky=W)
            self.EnDisValueIgnoreIndexOptions.grid(row=41, column=2, sticky=W)
            self.EnDisValueIgnoreIndexPadding.grid(row=42, column=2, sticky=W)
            self.EnDisValueIgnoreKeywordCasing.grid(row=43, column=2, sticky=W)
            self.EnDisValueIgnoreLockHintsOnIndexes.grid(row=44, column=2, sticky=W)
            self.EnDisValueIgnoreLoginSids.grid(row=45, column=2, sticky=W)
            self.EnDisValueIgnoreNotForReplication.grid(row=46, column=2, sticky=W)
            self.EnDisValueIgnoreObjectPlacementOnPartitionScheme.grid(row=47, column=2, sticky=W)
            self.EnDisValueIgnorePartitionSchemes.grid(row=48, column=2, sticky=W)
            self.EnDisValueIgnorePermissions.grid(row=49, column=2, sticky=W)
            self.EnDisValueIgnoreQuotedIdentifiers.grid(row=50, column=2, sticky=W)
            self.EnDisValueIgnoreRoleMembership.grid(row=51, column=2, sticky=W)
            self.EnDisValueIgnoreRouteLifetime.grid(row=52, column=2, sticky=W)
            self.EnDisValueIgnoreSemicolonBetweenStatements.grid(row=53, column=2, sticky=W)
            self.EnDisValueIgnoreTableOptions.grid(row=54, column=2, sticky=W)
            self.EnDisValueIgnoreUserSettingsObjects.grid(row=55, column=2, sticky=W)
            self.EnDisValueIgnoreWhitespace.grid(row=56, column=2, sticky=W)
            self.EnDisValueIgnoreWithNocheckOnCheckConstraints.grid(row=57, column=2, sticky=W)
            self.EnDisValueIgnoreWithNocheckOnForeignKeys.grid(row=58, column=2, sticky=W)
            self.EnDisValueIncludeCompositeObjects.grid(row=59, column=2, sticky=W)
            self.EnDisValueIncludeTransactionalScripts.grid(row=60, column=2, sticky=W)
            self.EnDisValueNoAlterStatementsToChangeClrTypes.grid(row=61, column=2, sticky=W)
            self.EnDisValuePopulateFilesOnFilegroups.grid(row=62, column=2, sticky=W)
            self.EnDisValueRegisterDataTierApplication.grid(row=63, column=2, sticky=W)
            self.EnDisValueRunDeploymentPlanExecutors.grid(row=64, column=2, sticky=W)
            self.EnDisValueScriptDatabaseCollation.grid(row=65, column=2, sticky=W)
            self.EnDisValueScriptDatabaseCompatibility.grid(row=66, column=2, sticky=W)
            self.EnDisValueScriptDatabaseOptions.grid(row=67, column=2, sticky=W)
            self.EnDisValueScriptDeployStateChecks.grid(row=68, column=2, sticky=W)
            self.EnDisValueScriptFileSize.grid(row=69, column=2, sticky=W)
            self.EnDisValueScriptNewConstraintValidation.grid(row=70, column=2, sticky=W)
            self.EnDisValueScriptRefreshModule.grid(row=71, column=2, sticky=W)
            self.EnDisValueStorage.grid(row=72, column=2, sticky=W)
            self.EnDisValueTreatVerificationErrorsAsWarnings.grid(row=73, column=2, sticky=W)
            self.EnDisValueUnmodifiableObjectWarnings.grid(row=74, column=2, sticky=W)
            self.EnDisValueVerifyCollationCompatibility.grid(row=75, column=2, sticky=W)
            self.EnDisValueVerifyDeployment.grid(row=76, column=2, sticky=W)

            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonAllowDropBlockingAssemblies, command=self.EnDisScrAllowDropBlockingAssemblies).grid(row=0, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonAllowIncompatiblePlatform, command=self.EnDisScrAllowIncompatiblePlatform).grid(row=1, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonBackupDatabaseBeforeChanges, command=self.EnDisScrBackupDatabaseBeforeChanges).grid(row=2, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonBlockOnPossibleDataLoss, command=self.EnDisScrBlockOnPossibleDataLoss).grid(row=3, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonBlockWhenDriftDetected, command=self.EnDisScrBlockWhenDriftDetected).grid(row=4, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonCommandTimeout, command=self.EnDisScrCommandTimeout).grid(row=5, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonCommentOutSetVarDeclarations, command=self.EnDisScrCommentOutSetVarDeclarations).grid(row=6, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonCompareUsingTargetCollation, command=self.EnDisScrCompareUsingTargetCollation).grid(row=7, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonCreateNewDatabase, command=self.EnDisScrCreateNewDatabase).grid(row=8, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDeployDatabaseInSingleUserMode, command=self.EnDisScrDeployDatabaseInSingleUserMode).grid(row=9, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDisableAndReenableDdlTriggers, command=self.EnDisScrDisableAndReenableDdlTriggers).grid(row=10, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDoNotAlterChangeDataCaptureObjects, command=self.EnDisScrDoNotAlterChangeDataCaptureObjects).grid(row=11, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDoNotAlterReplicatedObjects, command=self.EnDisScrDoNotAlterReplicatedObjects).grid(row=12, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDoNotDropObjectTypes, command=self.EnDisScrDoNotDropObjectTypes).grid(row=13, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDropConstraintsNotInSource, command=self.EnDisScrDropConstraintsNotInSource).grid(row=14, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDropDmlTriggersNotInSource, command=self.EnDisScrDropDmlTriggersNotInSource).grid(row=15, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDropExtendedPropertiesNotInSource, command=self.EnDisScrDropExtendedPropertiesNotInSource).grid(row=16, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDropIndexesNotInSource, command=self.EnDisScrDropIndexesNotInSource).grid(row=17, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDropObjectsNotInSource, command=self.EnDisScrDropObjectsNotInSource).grid(row=18, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDropPermissionsNotInSource, command=self.EnDisScrDropPermissionsNotInSource).grid(row=19, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonDropRoleMembersNotInSource, command=self.EnDisScrDropRoleMembersNotInSource).grid(row=20, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonExcludeObjectTypes, command=self.EnDisScrExcludeObjectTypes).grid(row=21, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonGenerateSmartDefaults, command=self.EnDisScrGenerateSmartDefaults).grid(row=22, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreAnsiNulls, command=self.EnDisScrIgnoreAnsiNulls).grid(row=23, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreAuthorizer, command=self.EnDisScrIgnoreAuthorizer).grid(row=24, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreColumnCollation, command=self.EnDisScrIgnoreColumnCollation).grid(row=25, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreComments, command=self.EnDisScrIgnoreComments).grid(row=26, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreCryptographicProviderFilePath, command=self.EnDisScrIgnoreCryptographicProviderFilePath).grid(row=27, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreDdlTriggerOrder, command=self.EnDisScrIgnoreDdlTriggerOrder).grid(row=28, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreDdlTriggerState, command=self.EnDisScrIgnoreDdlTriggerState).grid(row=29, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreDefaultSchema, command=self.EnDisScrIgnoreDefaultSchema).grid(row=30, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreDmlTriggerOrder, command=self.EnDisScrIgnoreDmlTriggerOrder).grid(row=31, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreDmlTriggerState, command=self.EnDisScrIgnoreDmlTriggerState).grid(row=32, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreExtendedProperties, command=self.EnDisScrIgnoreExtendedProperties).grid(row=33, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreFileAndLogFilePath, command=self.EnDisScrIgnoreFileAndLogFilePath).grid(row=34, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreFilegroupPlacement, command=self.EnDisScrIgnoreFilegroupPlacement).grid(row=35, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreFileSize, command=self.EnDisScrIgnoreFileSize).grid(row=36, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreFillFactor, command=self.EnDisScrIgnoreFillFactor).grid(row=37, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreFullTextCatalogFilePath, command=self.EnDisScrIgnoreFullTextCatalogFilePath).grid(row=38, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreIdentitySeed, command=self.EnDisScrIgnoreIdentitySeed).grid(row=39, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreIncrement, command=self.EnDisScrIgnoreIncrement).grid(row=40, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreIndexOptions, command=self.EnDisScrIgnoreIndexOptions).grid(row=41, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreIndexPadding, command=self.EnDisScrIgnoreIndexPadding).grid(row=42, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreKeywordCasing, command=self.EnDisScrIgnoreKeywordCasing).grid(row=43, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreLockHintsOnIndexes, command=self.EnDisScrIgnoreLockHintsOnIndexes).grid(row=44, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreLoginSids, command=self.EnDisScrIgnoreLoginSids).grid(row=45, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreNotForReplication, command=self.EnDisScrIgnoreNotForReplication).grid(row=46, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreObjectPlacementOnPartitionScheme, command=self.EnDisScrIgnoreObjectPlacementOnPartitionScheme).grid(row=47, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnorePartitionSchemes, command=self.EnDisScrIgnorePartitionSchemes).grid(row=48, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnorePermissions, command=self.EnDisScrIgnorePermissions).grid(row=49, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreQuotedIdentifiers, command=self.EnDisScrIgnoreQuotedIdentifiers).grid(row=50, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreRoleMembership, command=self.EnDisScrIgnoreRoleMembership).grid(row=51, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreRouteLifetime, command=self.EnDisScrIgnoreRouteLifetime).grid(row=52, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreSemicolonBetweenStatements, command=self.EnDisScrIgnoreSemicolonBetweenStatements).grid(row=53, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreTableOptions, command=self.EnDisScrIgnoreTableOptions).grid(row=54, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreUserSettingsObjects, command=self.EnDisScrIgnoreUserSettingsObjects).grid(row=55, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreWhitespace, command=self.EnDisScrIgnoreWhitespace).grid(row=56, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreWithNocheckOnCheckConstraints, command=self.EnDisScrIgnoreWithNocheckOnCheckConstraints).grid(row=57, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIgnoreWithNocheckOnForeignKeys, command=self.EnDisScrIgnoreWithNocheckOnForeignKeys).grid(row=58, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIncludeCompositeObjects, command=self.EnDisScrIncludeCompositeObjects).grid(row=59, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonIncludeTransactionalScripts, command=self.EnDisScrIncludeTransactionalScripts).grid(row=60, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonNoAlterStatementsToChangeClrTypes, command=self.EnDisScrNoAlterStatementsToChangeClrTypes).grid(row=61, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonPopulateFilesOnFilegroups, command=self.EnDisScrPopulateFilesOnFilegroups).grid(row=62, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonRegisterDataTierApplication, command=self.EnDisScrRegisterDataTierApplication).grid(row=63, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonRunDeploymentPlanExecutors, command=self.EnDisScrRunDeploymentPlanExecutors).grid(row=64, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonScriptDatabaseCollation, command=self.EnDisScrScriptDatabaseCollation).grid(row=65, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonScriptDatabaseCompatibility, command=self.EnDisScrScriptDatabaseCompatibility).grid(row=66, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonScriptDatabaseOptions, command=self.EnDisScrScriptDatabaseOptions).grid(row=67, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonScriptDeployStateChecks, command=self.EnDisScrScriptDeployStateChecks).grid(row=68, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonScriptFileSize, command=self.EnDisScrScriptFileSize).grid(row=69, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonScriptNewConstraintValidation, command=self.EnDisScrScriptNewConstraintValidation).grid(row=70, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonScriptRefreshModule, command=self.EnDisScrScriptRefreshModule).grid(row=71, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonStorage, command=self.EnDisScrStorage).grid(row=72, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonTreatVerificationErrorsAsWarnings, command=self.EnDisScrTreatVerificationErrorsAsWarnings).grid(row=73, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonUnmodifiableObjectWarnings, command=self.EnDisScrUnmodifiableObjectWarnings).grid(row=74, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonVerifyCollationCompatibility, command=self.EnDisScrVerifyCollationCompatibility).grid(row=75, column=0, sticky=W)
            Checkbutton(DplyPrpCanvasFrame, var=self.ChkButtonVerifyDeployment, command=self.EnDisScrVerifyDeployment).grid(row=76, column=0, sticky=W)

            # USED TO RESET THE SCROLLBAR, also used with DplyScroll_Visibility function
            #####################
            #####################
            #####################
            self.SetScrollBarDefault("all")
            #####################
            #####################
            #####################

        ########################################################################
        ########################################################################

        def configDplyPrpCanvasFunction(event):
            DplyPrpCanvas.configure(scrollregion=DplyPrpCanvas.bbox("all"), width=350, height=200)

        self.DplyPrpFrame = Frame(self, relief=GROOVE, width=80, height=100, bd=1)
        # self.DplyPrpFrame.grid(row=8,column=2,sticky=W)

        DplyPrpCanvas = Canvas(self.DplyPrpFrame)
        DplyPrpCanvasFrame = Frame(DplyPrpCanvas)
        DplyPrpScrollbar = Scrollbar(self.DplyPrpFrame, orient="vertical", command=DplyPrpCanvas.yview)
        DplyPrpCanvas.configure(yscrollcommand=DplyPrpScrollbar.set)

        DplyPrpScrollbar.pack(side="right", fill="y")
        DplyPrpCanvas.pack(side="left")
        DplyPrpCanvas.create_window((0, 0), window=DplyPrpCanvasFrame, anchor='nw')
        DplyPrpCanvasFrame.bind("<Configure>", configDplyPrpCanvasFunction)
        DplyPrpWidgetsFunction()
        ############################################################################
        ############################################################################

        # Button to compare and Generate script
        self.ExecuteButton = Button(self, text="Compare & Generate Script", command=self.compare_generate_script)  # button click calls shell output
        self.ExecuteButton.grid(row=10, column=2, sticky=W)

        # Button for initiating the deployment
        self.ExecuteButton = Button(self, text="Compare & Deploy", command=self.compare_and_deploy)
        self.ExecuteButton.grid(row=10, column=1, sticky=W)

        # Button to check Shell Output
        self.ExecuteButton = Button(self, text="Shell Output", command=self.shell_output)  # button click calls shell output
        self.ExecuteButton.grid(row=10, column=3, sticky=W)

        # Button to save profile
        self.SaveProfileButton = Button(self, text="Save Profile", command=self.save_profile)
        self.SaveProfileButton.grid(row=1, column=4, sticky=W)

        # Button to load profile
        self.LoadProfileButton = Button(self, text="Load Profile", command=self.load_profile)
        self.LoadProfileButton.grid(row=2, column=4, sticky=W)

        # # Connection information
        # self.InformationLabel = Label(self, text="Connection Info:", justify=LEFT)
        # self.InformationLabel.grid(row=12, column=0, sticky=W)

    ################################################################################
    # METHODS ######################################################################
    # method that initiates the process to compare & deploy SQL Server database
    # self.PreDeploymentText.get(1.0, END)
    # self.SourceServerEntry.get()   |   self.SourceDatabaseEntry.get()
    # self.TargetServerEntry.get()   |   self.TargetDatabaseEntry.get()
    # self.SourceUsernameEntry.get() |   self.SourcePasswordEntry.get()
    # self.TargetUsernameEntry.get() |   self.TargetPasswordEntry.get()




    # method to display shell output
    def shell_output(self):
        # Shell output window
        self.ShellOutputnewWindow = Toplevel(width=500, height=700)
        self.ShellOutputnewWindow.title("Shell Output")
        self.ShellOutputnewWindow.grid()


        self.ShellOutputnewText = Text(self.ShellOutputnewWindow, width=100, height=40, wrap=WORD)
        self.ShellOutputnewText.grid(row=0, column=1, columnspan=2, sticky=W)
        self.ShellOutputnewText.insert(END,self.ShellOutputText.get(1.0,END))
        # ShellOutputText.insert(END, self.ShellOutputExtractString)
        # ShellOutputText.insert(END, self.ShellOutputPublishString)

        # print("Check Button Allow Drop Block Assemblies: ",self.ChkButtonAllowDropBlockingAssemblies)
        # print("Value Drop Down Allow Drop Block Assemblies",self.ValueAllowDropBlockingAssemblies)
        # print("Check Button Aggregates - Do Not Drop",self.DoNotDropObjectTypesAggregates)
        # print("Check Button Aggregates - Exclude Objects",self.ExcludeObjectTypesAggregates)

    def SrcCredentials_Visibility(self):
        if self.WinAuthSrcVariable.get() is True:
            self.SourceUsernameLabel.grid_remove()
            self.SourceUsernameEntry.grid_forget()
            self.SourcePasswordLabel.grid_forget()
            self.SourcePasswordEntry.grid_forget()

        else:
            self.SourceUsernameLabel.grid(row=4, column=0, sticky=W)
            self.SourceUsernameEntry.grid(row=4, column=1, sticky=W)
            self.SourcePasswordLabel.grid(row=5, column=0, sticky=W)
            self.SourcePasswordEntry.grid(row=5, column=1, sticky=W)

    def TrgtCredentials_Visibility(self):
        if self.WinAuthTrgtVariable.get() is True:
            self.TargetUsernameLabel.grid_forget()
            self.TargetUsernameEntry.grid_forget()
            self.TargetPasswordLabel.grid_forget()
            self.TargetPasswordEntry.grid_forget()

        else:
            self.TargetUsernameLabel.grid(row=4, column=2, sticky=W)
            self.TargetUsernameEntry.grid(row=4, column=3, sticky=W)
            self.TargetPasswordLabel.grid(row=5, column=2, sticky=W)
            self.TargetPasswordEntry.grid(row=5, column=3, sticky=W)

    def DplyScroll_Visibility(self):
        if self.SetDplyPropertyVariable.get() is False:
            self.DplyPrpFrame.grid_forget()
            self.SetScrollBarDefault("all")

        else:
            self.DplyPrpFrame.grid(row=8, column=2, sticky=W)

    def DoNotDropObjectTypes(self):
        DoNotDropObjectTypesWindow = Toplevel(width=500, height=700)
        DoNotDropObjectTypesWindow.title("Select the Objects not to drop during deployment")
        DoNotDropObjectTypesWindow.grid()

        def DoNotDropWidgetsFunction():
            # Checkbuttons, Labels and option menus #################################
            ########################################################################
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesAggregates, text="Aggregates").grid(row=1, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesApplicationRoles, text="ApplicationRoles").grid(row=2, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesAssemblies, text="Assemblies").grid(row=3, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesAsymmetricKeys, text="AsymmetricKeys").grid(row=4, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesBrokerPriorities, text="BrokerPriorities").grid(row=5, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesCertificates, text="Certificates").grid(row=6, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesContracts, text="Contracts").grid(row=7, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesDatabaseRoles, text="DatabaseRoles").grid(row=8, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesDatabaseTriggers, text="DatabaseTriggers").grid(row=9, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesDefaults, text="Defaults").grid(row=10, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesExtendedProperties, text="ExtendedProperties").grid(row=11, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesFilegroups, text="Filegroups").grid(row=12, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesFileTables, text="FileTables").grid(row=13, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesFullTextCatalogs, text="FullTextCatalogs").grid(row=14, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesFullTextStoplists, text="FullTextStoplists").grid(row=15, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesMessageTypes, text="MessageTypes").grid(row=16, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesPartitionFunctions, text="PartitionFunctions").grid(row=17, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesPartitionSchemes, text="PartitionSchemes").grid(row=18, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesPermissions, text="Permissions").grid(row=19, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesQueues, text="Queues").grid(row=20, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesRemoteServiceBindings, text="RemoteServiceBindings").grid(row=21, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesRoleMembership, text="RoleMembership").grid(row=22, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesRules, text="Rules").grid(row=23, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesScalarValuedFunctions, text="ScalarValuedFunctions").grid(row=24, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesSearchPropertyLists, text="SearchPropertyLists").grid(row=25, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesSequences, text="Sequences").grid(row=26, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesServices, text="Services").grid(row=27, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesSignatures, text="Signatures").grid(row=28, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesStoredProcedures, text="StoredProcedures").grid(row=29, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesSymmetricKeys, text="SymmetricKeys").grid(row=30, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesSynonyms, text="Synonyms").grid(row=31, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesTables, text="Tables").grid(row=32, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesTableValuedFunctions, text="TableValuedFunctions").grid(row=33, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesUserDefinedDataTypes, text="UserDefinedDataTypes").grid(row=34, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesUserDefinedTableTypes, text="UserDefinedTableTypes").grid(row=35, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesClrUserDefinedTypes, text="ClrUserDefinedTypes").grid(row=36, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesUsers, text="Users").grid(row=37, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesViews, text="Views").grid(row=38, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesXmlSchemaCollections, text="XmlSchemaCollections").grid(row=39, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesAudits, text="Audits").grid(row=40, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesCredentials, text="Credentials").grid(row=41, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesCryptographicProviders, text="CryptographicProviders").grid(row=42, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesDatabaseAuditSpecifications, text="DatabaseAuditSpecifications").grid(row=43, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesEndpoints, text="Endpoints").grid(row=44, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesErrorMessages, text="ErrorMessages").grid(row=45, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesEventNotifications, text="EventNotifications").grid(row=46, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesEventSessions, text="EventSessions").grid(row=47, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesLinkedServerLogins, text="LinkedServerLogins").grid(row=48, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesLinkedServers, text="LinkedServers").grid(row=49, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesLogins, text="Logins").grid(row=50, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesRoutes, text="Routes").grid(row=51, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesServerAuditSpecifications, text="ServerAuditSpecifications").grid(row=52, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesServerRoleMembership, text="ServerRoleMembership").grid(row=53, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesServerRoles, text="ServerRoles").grid(row=54, column=0, sticky=W)
            Checkbutton(DoNotDropCanvasFrame, var=self.DoNotDropObjectTypesServerTriggers, text="ServerTriggers").grid(row=55, column=0, sticky=W)

        def configDoNotDropCanvasFunction(event):
            DoNotDropCanvas.configure(scrollregion=DoNotDropCanvas.bbox("all"), width=200, height=400)

        def DoNotDrop_window_visibility():
            DoNotDropObjectTypesWindow.withdraw()

        self.DoNotDropFrame = Frame(DoNotDropObjectTypesWindow, relief=GROOVE, width=100, height=200, bd=1)
        self.DoNotDropFrame.grid(row=0, column=0, sticky=W)

        DoNotDropCanvas = Canvas(self.DoNotDropFrame)
        DoNotDropCanvasFrame = Frame(DoNotDropCanvas)
        DoNotDropScrollbar = Scrollbar(self.DoNotDropFrame, orient="vertical", command=DoNotDropCanvas.yview)
        DoNotDropCanvas.configure(yscrollcommand=DoNotDropScrollbar.set)

        DoNotDropScrollbar.pack(side="right", fill="y")
        DoNotDropCanvas.pack(side="left")
        DoNotDropCanvas.create_window((0, 0), window=DoNotDropCanvasFrame, anchor='nw')
        DoNotDropCanvasFrame.bind("<Configure>", configDoNotDropCanvasFunction)
        DoNotDropWidgetsFunction()

        Label(DoNotDropObjectTypesWindow, text="Note: Only Applicable when DropObjectsNotInSource is true").grid(row=0, column=1, sticky=W)
        Button(DoNotDropObjectTypesWindow, text="Ok", command=DoNotDrop_window_visibility).grid(row=1, column=1, sticky=W)

    def ExcludeObjectTypes(self):
        ExcludeObjectTypesWindow = Toplevel(width=500, height=700)
        ExcludeObjectTypesWindow.title("Select the Objects to Exclude from Deployment")
        ExcludeObjectTypesWindow.grid()

        def ExcludeObjectWidgetsFunction():
            # Checkbuttons, Labels and option menus #################################
            ########################################################################
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesAggregates, text="Aggregates").grid(row=1, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesApplicationRoles, text="ApplicationRoles").grid(row=2, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesAssemblies, text="Assemblies").grid(row=3, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesAsymmetricKeys, text="AsymmetricKeys").grid(row=4, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesBrokerPriorities, text="BrokerPriorities").grid(row=5, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesCertificates, text="Certificates").grid(row=6, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesContracts, text="Contracts").grid(row=7, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesDatabaseRoles, text="DatabaseRoles").grid(row=8, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesDatabaseTriggers, text="DatabaseTriggers").grid(row=9, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesDefaults, text="Defaults").grid(row=10, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesExtendedProperties, text="ExtendedProperties").grid(row=11, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesFilegroups, text="Filegroups").grid(row=12, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesFileTables, text="FileTables").grid(row=13, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesFullTextCatalogs, text="FullTextCatalogs").grid(row=14, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesFullTextStoplists, text="FullTextStoplists").grid(row=15, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesMessageTypes, text="MessageTypes").grid(row=16, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesPartitionFunctions, text="PartitionFunctions").grid(row=17, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesPartitionSchemes, text="PartitionSchemes").grid(row=18, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesPermissions, text="Permissions").grid(row=19, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesQueues, text="Queues").grid(row=20, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesRemoteServiceBindings, text="RemoteServiceBindings").grid(row=21, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesRoleMembership, text="RoleMembership").grid(row=22, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesRules, text="Rules").grid(row=23, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesScalarValuedFunctions, text="ScalarValuedFunctions").grid(row=24, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesSearchPropertyLists, text="SearchPropertyLists").grid(row=25, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesSequences, text="Sequences").grid(row=26, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesServices, text="Services").grid(row=27, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesSignatures, text="Signatures").grid(row=28, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesStoredProcedures, text="StoredProcedures").grid(row=29, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesSymmetricKeys, text="SymmetricKeys").grid(row=30, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesSynonyms, text="Synonyms").grid(row=31, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesTables, text="Tables").grid(row=32, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesTableValuedFunctions, text="TableValuedFunctions").grid(row=33, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesUserDefinedDataTypes, text="UserDefinedDataTypes").grid(row=34, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesUserDefinedTableTypes, text="UserDefinedTableTypes").grid(row=35, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesClrUserDefinedTypes, text="ClrUserDefinedTypes").grid(row=36, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesUsers, text="Users").grid(row=37, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesViews, text="Views").grid(row=38, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesXmlSchemaCollections, text="XmlSchemaCollections").grid(row=39, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesAudits, text="Audits").grid(row=40, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesCredentials, text="Credentials").grid(row=41, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesCryptographicProviders, text="CryptographicProviders").grid(row=42, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesDatabaseAuditSpecifications, text="DatabaseAuditSpecifications").grid(row=43, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesEndpoints, text="Endpoints").grid(row=44, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesErrorMessages, text="ErrorMessages").grid(row=45, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesEventNotifications, text="EventNotifications").grid(row=46, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesEventSessions, text="EventSessions").grid(row=47, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesLinkedServerLogins, text="LinkedServerLogins").grid(row=48, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesLinkedServers, text="LinkedServers").grid(row=49, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesLogins, text="Logins").grid(row=50, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesRoutes, text="Routes").grid(row=51, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesServerAuditSpecifications, text="ServerAuditSpecifications").grid(row=52, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesServerRoleMembership, text="ServerRoleMembership").grid(row=53, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesServerRoles, text="ServerRoles").grid(row=54, column=0, sticky=W)
            Checkbutton(ExcludeObjectCanvasFrame, var=self.ExcludeObjectTypesServerTriggers, text="ServerTriggers").grid(row=55, column=0, sticky=W)

        def configExcludeObjectCanvasFunction(event):
            ExcludeObjectCanvas.configure(scrollregion=ExcludeObjectCanvas.bbox("all"), width=200, height=400)

        def ExcludeObject_window_visibility():
            ExcludeObjectTypesWindow.withdraw()

        self.ExcludeObjectFrame = Frame(ExcludeObjectTypesWindow, relief=GROOVE, width=100, height=200, bd=1)
        self.ExcludeObjectFrame.grid(row=0, column=0, sticky=W)

        ExcludeObjectCanvas = Canvas(self.ExcludeObjectFrame)
        ExcludeObjectCanvasFrame = Frame(ExcludeObjectCanvas)
        ExcludeObjectScrollbar = Scrollbar(self.ExcludeObjectFrame, orient="vertical", command=ExcludeObjectCanvas.yview)
        ExcludeObjectCanvas.configure(yscrollcommand=ExcludeObjectScrollbar.set)

        ExcludeObjectScrollbar.pack(side="right", fill="y")
        ExcludeObjectCanvas.pack(side="left")
        ExcludeObjectCanvas.create_window((0, 0), window=ExcludeObjectCanvasFrame, anchor='nw')
        ExcludeObjectCanvasFrame.bind("<Configure>", configExcludeObjectCanvasFunction)
        ExcludeObjectWidgetsFunction()

        Button(ExcludeObjectTypesWindow, text="Ok", command=ExcludeObject_window_visibility).grid(row=1, column=1, sticky=W)

    # def print_variable_values(self):
    #     abc=self.ChkButtonAllowDropBlockingAssemblies.get()
    #     print("Check Button Allow Drop Block Assemblies: ",abc)
    #     print("Value Drop Down Allow Drop Block Assemblies: ",self.ValueAllowDropBlockingAssemblies.get())
    #     print("Check Button Aggregates - Do Not Drop: ",self.DoNotDropObjectTypesAggregates.get())
    #     print("Check Button Aggregates - Exclude Objects: ",self.ExcludeObjectTypesAggregates.get())

    def SetScrollBarDefault(self, Reset_Value):
        if Reset_Value == "all":
            # RESET CHECKBUTTONS ALL
            self.ChkButtonAllowDropBlockingAssemblies.set(False)
            self.ChkButtonAllowIncompatiblePlatform.set(False)
            self.ChkButtonBackupDatabaseBeforeChanges.set(False)
            self.ChkButtonBlockOnPossibleDataLoss.set(False)
            self.ChkButtonBlockWhenDriftDetected.set(False)
            self.ChkButtonCommandTimeout.set(False)
            self.ChkButtonCommentOutSetVarDeclarations.set(False)
            self.ChkButtonCompareUsingTargetCollation.set(False)
            self.ChkButtonCreateNewDatabase.set(False)
            self.ChkButtonDeployDatabaseInSingleUserMode.set(False)
            self.ChkButtonDisableAndReenableDdlTriggers.set(False)
            self.ChkButtonDoNotAlterChangeDataCaptureObjects.set(False)
            self.ChkButtonDoNotAlterReplicatedObjects.set(False)
            self.ChkButtonDoNotDropObjectTypes.set(False)
            self.ChkButtonDropConstraintsNotInSource.set(False)
            self.ChkButtonDropDmlTriggersNotInSource.set(False)
            self.ChkButtonDropExtendedPropertiesNotInSource.set(False)
            self.ChkButtonDropIndexesNotInSource.set(False)
            self.ChkButtonDropObjectsNotInSource.set(False)
            self.ChkButtonDropPermissionsNotInSource.set(False)
            self.ChkButtonDropRoleMembersNotInSource.set(False)
            self.ChkButtonExcludeObjectTypes.set(False)
            self.ChkButtonGenerateSmartDefaults.set(False)
            self.ChkButtonIgnoreAnsiNulls.set(False)
            self.ChkButtonIgnoreAuthorizer.set(False)
            self.ChkButtonIgnoreColumnCollation.set(False)
            self.ChkButtonIgnoreComments.set(False)
            self.ChkButtonIgnoreCryptographicProviderFilePath.set(False)
            self.ChkButtonIgnoreDdlTriggerOrder.set(False)
            self.ChkButtonIgnoreDdlTriggerState.set(False)
            self.ChkButtonIgnoreDefaultSchema.set(False)
            self.ChkButtonIgnoreDmlTriggerOrder.set(False)
            self.ChkButtonIgnoreDmlTriggerState.set(False)
            self.ChkButtonIgnoreExtendedProperties.set(False)
            self.ChkButtonIgnoreFileAndLogFilePath.set(False)
            self.ChkButtonIgnoreFilegroupPlacement.set(False)
            self.ChkButtonIgnoreFileSize.set(False)
            self.ChkButtonIgnoreFillFactor.set(False)
            self.ChkButtonIgnoreFullTextCatalogFilePath.set(False)
            self.ChkButtonIgnoreIdentitySeed.set(False)
            self.ChkButtonIgnoreIncrement.set(False)
            self.ChkButtonIgnoreIndexOptions.set(False)
            self.ChkButtonIgnoreIndexPadding.set(False)
            self.ChkButtonIgnoreKeywordCasing.set(False)
            self.ChkButtonIgnoreLockHintsOnIndexes.set(False)
            self.ChkButtonIgnoreLoginSids.set(False)
            self.ChkButtonIgnoreNotForReplication.set(False)
            self.ChkButtonIgnoreObjectPlacementOnPartitionScheme.set(False)
            self.ChkButtonIgnorePartitionSchemes.set(False)
            self.ChkButtonIgnorePermissions.set(False)
            self.ChkButtonIgnoreQuotedIdentifiers.set(False)
            self.ChkButtonIgnoreRoleMembership.set(False)
            self.ChkButtonIgnoreRouteLifetime.set(False)
            self.ChkButtonIgnoreSemicolonBetweenStatements.set(False)
            self.ChkButtonIgnoreTableOptions.set(False)
            self.ChkButtonIgnoreUserSettingsObjects.set(False)
            self.ChkButtonIgnoreWhitespace.set(False)
            self.ChkButtonIgnoreWithNocheckOnCheckConstraints.set(False)
            self.ChkButtonIgnoreWithNocheckOnForeignKeys.set(False)
            self.ChkButtonIncludeCompositeObjects.set(False)
            self.ChkButtonIncludeTransactionalScripts.set(False)
            self.ChkButtonNoAlterStatementsToChangeClrTypes.set(False)
            self.ChkButtonPopulateFilesOnFilegroups.set(False)
            self.ChkButtonRegisterDataTierApplication.set(False)
            self.ChkButtonRunDeploymentPlanExecutors.set(False)
            self.ChkButtonScriptDatabaseCollation.set(False)
            self.ChkButtonScriptDatabaseCompatibility.set(False)
            self.ChkButtonScriptDatabaseOptions.set(False)
            self.ChkButtonScriptDeployStateChecks.set(False)
            self.ChkButtonScriptFileSize.set(False)
            self.ChkButtonScriptNewConstraintValidation.set(False)
            self.ChkButtonScriptRefreshModule.set(False)
            self.ChkButtonStorage.set(False)
            self.ChkButtonTreatVerificationErrorsAsWarnings.set(False)
            self.ChkButtonUnmodifiableObjectWarnings.set(False)
            self.ChkButtonVerifyCollationCompatibility.set(False)
            self.ChkButtonVerifyDeployment.set(False)

            self.reset_DoNotDropObjects("all")
            self.reset_ExcludeObjectTypes("all")

            # Reset VALUES
            self.ValueAllowDropBlockingAssemblies.set("False")
            self.ValueAllowIncompatiblePlatform.set("False")
            self.ValueBackupDatabaseBeforeChanges.set("False")
            self.ValueBlockOnPossibleDataLoss.set("True")
            self.ValueBlockWhenDriftDetected.set("True")
            # self.ValueCommandTimeout.set("60")
            self.ValueCommentOutSetVarDeclarations.set("False")
            self.ValueCompareUsingTargetCollation.set("False")
            self.ValueCreateNewDatabase.set("False")
            self.ValueDeployDatabaseInSingleUserMode.set("False")
            self.ValueDisableAndReenableDdlTriggers.set("True")
            self.ValueDoNotAlterChangeDataCaptureObjects.set("True")
            self.ValueDoNotAlterReplicatedObjects.set("True")
            # self.ValueDoNotDropObjectTypes.set("N/A.")
            self.ValueDropConstraintsNotInSource.set("True")
            self.ValueDropDmlTriggersNotInSource.set("True")
            self.ValueDropExtendedPropertiesNotInSource.set("True")
            self.ValueDropIndexesNotInSource.set("True")
            self.ValueDropObjectsNotInSource.set("False")
            self.ValueDropPermissionsNotInSource.set("False")
            self.ValueDropRoleMembersNotInSource.set("False")
            # self.ValueExcludeObjectTypes.set("N/A.")
            self.ValueGenerateSmartDefaults.set("False")
            self.ValueIgnoreAnsiNulls.set("False")
            self.ValueIgnoreAuthorizer.set("False")
            self.ValueIgnoreColumnCollation.set("False")
            self.ValueIgnoreComments.set("False")
            self.ValueIgnoreCryptographicProviderFilePath.set("True")
            self.ValueIgnoreDdlTriggerOrder.set("False")
            self.ValueIgnoreDdlTriggerState.set("False")
            self.ValueIgnoreDefaultSchema.set("False")
            self.ValueIgnoreDmlTriggerOrder.set("False")
            self.ValueIgnoreDmlTriggerState.set("False")
            self.ValueIgnoreExtendedProperties.set("False")
            self.ValueIgnoreFileAndLogFilePath.set("True")
            self.ValueIgnoreFilegroupPlacement.set("True")
            self.ValueIgnoreFileSize.set("True")
            self.ValueIgnoreFillFactor.set("True")
            self.ValueIgnoreFullTextCatalogFilePath.set("True")
            self.ValueIgnoreIdentitySeed.set("False")
            self.ValueIgnoreIncrement.set("False")
            self.ValueIgnoreIndexOptions.set("False")
            self.ValueIgnoreIndexPadding.set("True")
            self.ValueIgnoreKeywordCasing.set("True")
            self.ValueIgnoreLockHintsOnIndexes.set("False")
            self.ValueIgnoreLoginSids.set("True")
            self.ValueIgnoreNotForReplication.set("False")
            self.ValueIgnoreObjectPlacementOnPartitionScheme.set("True")
            self.ValueIgnorePartitionSchemes.set("False")
            self.ValueIgnorePermissions.set("False")
            self.ValueIgnoreQuotedIdentifiers.set("False")
            self.ValueIgnoreRoleMembership.set("False")
            self.ValueIgnoreRouteLifetime.set("True")
            self.ValueIgnoreSemicolonBetweenStatements.set("True")
            self.ValueIgnoreTableOptions.set("False")
            self.ValueIgnoreUserSettingsObjects.set("False")
            self.ValueIgnoreWhitespace.set("True")
            self.ValueIgnoreWithNocheckOnCheckConstraints.set("False")
            self.ValueIgnoreWithNocheckOnForeignKeys.set("False")
            self.ValueIncludeCompositeObjects.set("False")
            self.ValueIncludeTransactionalScripts.set("False")
            self.ValueNoAlterStatementsToChangeClrTypes.set("False")
            self.ValuePopulateFilesOnFilegroups.set("True")
            self.ValueRegisterDataTierApplication.set("False")
            self.ValueRunDeploymentPlanExecutors.set("False")
            self.ValueScriptDatabaseCollation.set("False")
            self.ValueScriptDatabaseCompatibility.set("True")
            self.ValueScriptDatabaseOptions.set("True")
            self.ValueScriptDeployStateChecks.set("False")
            self.ValueScriptFileSize.set("False")
            self.ValueScriptNewConstraintValidation.set("True")
            self.ValueScriptRefreshModule.set("True")
            self.ValueStorage.set("Memory")
            self.ValueTreatVerificationErrorsAsWarnings.set("False")
            self.ValueUnmodifiableObjectWarnings.set("True")
            self.ValueVerifyCollationCompatibility.set("True")
            self.ValueVerifyDeployment.set("True")

            # self.EntryCommandTimeout.delete(0, END)
            self.EntryCommandTimeout.insert(0, "60")

            # DISABLE LABELS ALL
            self.LblAllowDropBlockingAssemblies.config(state='disabled')
            self.LblAllowIncompatiblePlatform.config(state='disabled')
            self.LblBackupDatabaseBeforeChanges.config(state='disabled')
            self.LblBlockOnPossibleDataLoss.config(state='disabled')
            self.LblBlockWhenDriftDetected.config(state='disabled')
            self.LblCommandTimeout.config(state='disabled')
            self.LblCommentOutSetVarDeclarations.config(state='disabled')
            self.LblCompareUsingTargetCollation.config(state='disabled')
            self.LblCreateNewDatabase.config(state='disabled')
            self.LblDeployDatabaseInSingleUserMode.config(state='disabled')
            self.LblDisableAndReenableDdlTriggers.config(state='disabled')
            self.LblDoNotAlterChangeDataCaptureObjects.config(state='disabled')
            self.LblDoNotAlterReplicatedObjects.config(state='disabled')
            self.LblDoNotDropObjectTypes.config(state='disabled')
            self.LblDropConstraintsNotInSource.config(state='disabled')
            self.LblDropDmlTriggersNotInSource.config(state='disabled')
            self.LblDropExtendedPropertiesNotInSource.config(state='disabled')
            self.LblDropIndexesNotInSource.config(state='disabled')
            self.LblDropObjectsNotInSource.config(state='disabled')
            self.LblDropPermissionsNotInSource.config(state='disabled')
            self.LblDropRoleMembersNotInSource.config(state='disabled')
            self.LblExcludeObjectTypes.config(state='disabled')
            self.LblGenerateSmartDefaults.config(state='disabled')
            self.LblIgnoreAnsiNulls.config(state='disabled')
            self.LblIgnoreAuthorizer.config(state='disabled')
            self.LblIgnoreColumnCollation.config(state='disabled')
            self.LblIgnoreComments.config(state='disabled')
            self.LblIgnoreCryptographicProviderFilePath.config(state='disabled')
            self.LblIgnoreDdlTriggerOrder.config(state='disabled')
            self.LblIgnoreDdlTriggerState.config(state='disabled')
            self.LblIgnoreDefaultSchema.config(state='disabled')
            self.LblIgnoreDmlTriggerOrder.config(state='disabled')
            self.LblIgnoreDmlTriggerState.config(state='disabled')
            self.LblIgnoreExtendedProperties.config(state='disabled')
            self.LblIgnoreFileAndLogFilePath.config(state='disabled')
            self.LblIgnoreFilegroupPlacement.config(state='disabled')
            self.LblIgnoreFileSize.config(state='disabled')
            self.LblIgnoreFillFactor.config(state='disabled')
            self.LblIgnoreFullTextCatalogFilePath.config(state='disabled')
            self.LblIgnoreIdentitySeed.config(state='disabled')
            self.LblIgnoreIncrement.config(state='disabled')
            self.LblIgnoreIndexOptions.config(state='disabled')
            self.LblIgnoreIndexPadding.config(state='disabled')
            self.LblIgnoreKeywordCasing.config(state='disabled')
            self.LblIgnoreLockHintsOnIndexes.config(state='disabled')
            self.LblIgnoreLoginSids.config(state='disabled')
            self.LblIgnoreNotForReplication.config(state='disabled')
            self.LblIgnoreObjectPlacementOnPartitionScheme.config(state='disabled')
            self.LblIgnorePartitionSchemes.config(state='disabled')
            self.LblIgnorePermissions.config(state='disabled')
            self.LblIgnoreQuotedIdentifiers.config(state='disabled')
            self.LblIgnoreRoleMembership.config(state='disabled')
            self.LblIgnoreRouteLifetime.config(state='disabled')
            self.LblIgnoreSemicolonBetweenStatements.config(state='disabled')
            self.LblIgnoreTableOptions.config(state='disabled')
            self.LblIgnoreUserSettingsObjects.config(state='disabled')
            self.LblIgnoreWhitespace.config(state='disabled')
            self.LblIgnoreWithNocheckOnCheckConstraints.config(state='disabled')
            self.LblIgnoreWithNocheckOnForeignKeys.config(state='disabled')
            self.LblIncludeCompositeObjects.config(state='disabled')
            self.LblIncludeTransactionalScripts.config(state='disabled')
            self.LblNoAlterStatementsToChangeClrTypes.config(state='disabled')
            self.LblPopulateFilesOnFilegroups.config(state='disabled')
            self.LblRegisterDataTierApplication.config(state='disabled')
            self.LblRunDeploymentPlanExecutors.config(state='disabled')
            self.LblScriptDatabaseCollation.config(state='disabled')
            self.LblScriptDatabaseCompatibility.config(state='disabled')
            self.LblScriptDatabaseOptions.config(state='disabled')
            self.LblScriptDeployStateChecks.config(state='disabled')
            self.LblScriptFileSize.config(state='disabled')
            self.LblScriptNewConstraintValidation.config(state='disabled')
            self.LblScriptRefreshModule.config(state='disabled')
            self.LblStorage.config(state='disabled')
            self.LblTreatVerificationErrorsAsWarnings.config(state='disabled')
            self.LblUnmodifiableObjectWarnings.config(state='disabled')
            self.LblVerifyCollationCompatibility.config(state='disabled')
            self.LblVerifyDeployment.config(state='disabled')

            # DISABLE DROPDOWNS/BUTTONS ALL
            self.EnDisValueAllowDropBlockingAssemblies.config(state='disabled')
            self.EnDisValueAllowIncompatiblePlatform.config(state='disabled')
            self.EnDisValueBackupDatabaseBeforeChanges.config(state='disabled')
            self.EnDisValueBlockOnPossibleDataLoss.config(state='disabled')
            self.EnDisValueBlockWhenDriftDetected.config(state='disabled')
            self.EntryCommandTimeout.config(state='disabled')
            self.EnDisValueCommentOutSetVarDeclarations.config(state='disabled')
            self.EnDisValueCompareUsingTargetCollation.config(state='disabled')
            self.EnDisValueCreateNewDatabase.config(state='disabled')
            self.EnDisValueDeployDatabaseInSingleUserMode.config(state='disabled')
            self.EnDisValueDisableAndReenableDdlTriggers.config(state='disabled')
            self.EnDisValueDoNotAlterChangeDataCaptureObjects.config(state='disabled')
            self.EnDisValueDoNotAlterReplicatedObjects.config(state='disabled')
            self.EnDisValueDoNotDropObjectTypes.config(state='disabled')
            self.EnDisValueDropConstraintsNotInSource.config(state='disabled')
            self.EnDisValueDropDmlTriggersNotInSource.config(state='disabled')
            self.EnDisValueDropExtendedPropertiesNotInSource.config(state='disabled')
            self.EnDisValueDropIndexesNotInSource.config(state='disabled')
            self.EnDisValueDropObjectsNotInSource.config(state='disabled')
            self.EnDisValueDropPermissionsNotInSource.config(state='disabled')
            self.EnDisValueDropRoleMembersNotInSource.config(state='disabled')
            self.EnDisValueExcludeObjectTypes.config(state='disabled')
            self.EnDisValueGenerateSmartDefaults.config(state='disabled')
            self.EnDisValueIgnoreAnsiNulls.config(state='disabled')
            self.EnDisValueIgnoreAuthorizer.config(state='disabled')
            self.EnDisValueIgnoreColumnCollation.config(state='disabled')
            self.EnDisValueIgnoreComments.config(state='disabled')
            self.EnDisValueIgnoreCryptographicProviderFilePath.config(state='disabled')
            self.EnDisValueIgnoreDdlTriggerOrder.config(state='disabled')
            self.EnDisValueIgnoreDdlTriggerState.config(state='disabled')
            self.EnDisValueIgnoreDefaultSchema.config(state='disabled')
            self.EnDisValueIgnoreDmlTriggerOrder.config(state='disabled')
            self.EnDisValueIgnoreDmlTriggerState.config(state='disabled')
            self.EnDisValueIgnoreExtendedProperties.config(state='disabled')
            self.EnDisValueIgnoreFileAndLogFilePath.config(state='disabled')
            self.EnDisValueIgnoreFilegroupPlacement.config(state='disabled')
            self.EnDisValueIgnoreFileSize.config(state='disabled')
            self.EnDisValueIgnoreFillFactor.config(state='disabled')
            self.EnDisValueIgnoreFullTextCatalogFilePath.config(state='disabled')
            self.EnDisValueIgnoreIdentitySeed.config(state='disabled')
            self.EnDisValueIgnoreIncrement.config(state='disabled')
            self.EnDisValueIgnoreIndexOptions.config(state='disabled')
            self.EnDisValueIgnoreIndexPadding.config(state='disabled')
            self.EnDisValueIgnoreKeywordCasing.config(state='disabled')
            self.EnDisValueIgnoreLockHintsOnIndexes.config(state='disabled')
            self.EnDisValueIgnoreLoginSids.config(state='disabled')
            self.EnDisValueIgnoreNotForReplication.config(state='disabled')
            self.EnDisValueIgnoreObjectPlacementOnPartitionScheme.config(state='disabled')
            self.EnDisValueIgnorePartitionSchemes.config(state='disabled')
            self.EnDisValueIgnorePermissions.config(state='disabled')
            self.EnDisValueIgnoreQuotedIdentifiers.config(state='disabled')
            self.EnDisValueIgnoreRoleMembership.config(state='disabled')
            self.EnDisValueIgnoreRouteLifetime.config(state='disabled')
            self.EnDisValueIgnoreSemicolonBetweenStatements.config(state='disabled')
            self.EnDisValueIgnoreTableOptions.config(state='disabled')
            self.EnDisValueIgnoreUserSettingsObjects.config(state='disabled')
            self.EnDisValueIgnoreWhitespace.config(state='disabled')
            self.EnDisValueIgnoreWithNocheckOnCheckConstraints.config(state='disabled')
            self.EnDisValueIgnoreWithNocheckOnForeignKeys.config(state='disabled')
            self.EnDisValueIncludeCompositeObjects.config(state='disabled')
            self.EnDisValueIncludeTransactionalScripts.config(state='disabled')
            self.EnDisValueNoAlterStatementsToChangeClrTypes.config(state='disabled')
            self.EnDisValuePopulateFilesOnFilegroups.config(state='disabled')
            self.EnDisValueRegisterDataTierApplication.config(state='disabled')
            self.EnDisValueRunDeploymentPlanExecutors.config(state='disabled')
            self.EnDisValueScriptDatabaseCollation.config(state='disabled')
            self.EnDisValueScriptDatabaseCompatibility.config(state='disabled')
            self.EnDisValueScriptDatabaseOptions.config(state='disabled')
            self.EnDisValueScriptDeployStateChecks.config(state='disabled')
            self.EnDisValueScriptFileSize.config(state='disabled')
            self.EnDisValueScriptNewConstraintValidation.config(state='disabled')
            self.EnDisValueScriptRefreshModule.config(state='disabled')
            self.EnDisValueStorage.config(state='disabled')
            self.EnDisValueTreatVerificationErrorsAsWarnings.config(state='disabled')
            self.EnDisValueUnmodifiableObjectWarnings.config(state='disabled')
            self.EnDisValueVerifyCollationCompatibility.config(state='disabled')
            self.EnDisValueVerifyDeployment.config(state='disabled')
            #
            # elif Reset_Value=="AllowDropBlockingAssemblies":
            #     self.LblAllowDropBlockingAssemblies.config(state='disabled')
            #     self.EnDisValueAllowDropBlockingAssemblies.config(state='disabled')

    def reset_DoNotDropObjects(self, DoNotDrop_Reset_Value):
        if DoNotDrop_Reset_Value == "all":
            self.DoNotDropObjectTypesAggregates.set(False)
            self.DoNotDropObjectTypesApplicationRoles.set(False)
            self.DoNotDropObjectTypesAssemblies.set(False)
            self.DoNotDropObjectTypesAsymmetricKeys.set(False)
            self.DoNotDropObjectTypesBrokerPriorities.set(False)
            self.DoNotDropObjectTypesCertificates.set(False)
            self.DoNotDropObjectTypesContracts.set(False)
            self.DoNotDropObjectTypesDatabaseRoles.set(False)
            self.DoNotDropObjectTypesDatabaseTriggers.set(False)
            self.DoNotDropObjectTypesDefaults.set(False)
            self.DoNotDropObjectTypesExtendedProperties.set(False)
            self.DoNotDropObjectTypesFilegroups.set(False)
            self.DoNotDropObjectTypesFileTables.set(False)
            self.DoNotDropObjectTypesFullTextCatalogs.set(False)
            self.DoNotDropObjectTypesFullTextStoplists.set(False)
            self.DoNotDropObjectTypesMessageTypes.set(False)
            self.DoNotDropObjectTypesPartitionFunctions.set(False)
            self.DoNotDropObjectTypesPartitionSchemes.set(False)
            self.DoNotDropObjectTypesPermissions.set(False)
            self.DoNotDropObjectTypesQueues.set(False)
            self.DoNotDropObjectTypesRemoteServiceBindings.set(False)
            self.DoNotDropObjectTypesRoleMembership.set(False)
            self.DoNotDropObjectTypesRules.set(False)
            self.DoNotDropObjectTypesScalarValuedFunctions.set(False)
            self.DoNotDropObjectTypesSearchPropertyLists.set(False)
            self.DoNotDropObjectTypesSequences.set(False)
            self.DoNotDropObjectTypesServices.set(False)
            self.DoNotDropObjectTypesSignatures.set(False)
            self.DoNotDropObjectTypesStoredProcedures.set(False)
            self.DoNotDropObjectTypesSymmetricKeys.set(False)
            self.DoNotDropObjectTypesSynonyms.set(False)
            self.DoNotDropObjectTypesTables.set(False)
            self.DoNotDropObjectTypesTableValuedFunctions.set(False)
            self.DoNotDropObjectTypesUserDefinedDataTypes.set(False)
            self.DoNotDropObjectTypesUserDefinedTableTypes.set(False)
            self.DoNotDropObjectTypesClrUserDefinedTypes.set(False)
            self.DoNotDropObjectTypesUsers.set(False)
            self.DoNotDropObjectTypesViews.set(False)
            self.DoNotDropObjectTypesXmlSchemaCollections.set(False)
            self.DoNotDropObjectTypesAudits.set(False)
            self.DoNotDropObjectTypesCredentials.set(False)
            self.DoNotDropObjectTypesCryptographicProviders.set(False)
            self.DoNotDropObjectTypesDatabaseAuditSpecifications.set(False)
            self.DoNotDropObjectTypesEndpoints.set(False)
            self.DoNotDropObjectTypesErrorMessages.set(False)
            self.DoNotDropObjectTypesEventNotifications.set(False)
            self.DoNotDropObjectTypesEventSessions.set(False)
            self.DoNotDropObjectTypesLinkedServerLogins.set(False)
            self.DoNotDropObjectTypesLinkedServers.set(False)
            self.DoNotDropObjectTypesLogins.set(False)
            self.DoNotDropObjectTypesRoutes.set(False)
            self.DoNotDropObjectTypesServerAuditSpecifications.set(False)
            self.DoNotDropObjectTypesServerRoleMembership.set(False)
            self.DoNotDropObjectTypesServerRoles.set(False)
            self.DoNotDropObjectTypesServerTriggers.set(False)

    def reset_ExcludeObjectTypes(self, ExcludeObject_Reset_Value):
        if ExcludeObject_Reset_Value == "all":
            self.ExcludeObjectTypesAggregates.set(False)
            self.ExcludeObjectTypesApplicationRoles.set(False)
            self.ExcludeObjectTypesAssemblies.set(False)
            self.ExcludeObjectTypesAsymmetricKeys.set(False)
            self.ExcludeObjectTypesBrokerPriorities.set(False)
            self.ExcludeObjectTypesCertificates.set(False)
            self.ExcludeObjectTypesContracts.set(False)
            self.ExcludeObjectTypesDatabaseRoles.set(False)
            self.ExcludeObjectTypesDatabaseTriggers.set(False)
            self.ExcludeObjectTypesDefaults.set(False)
            self.ExcludeObjectTypesExtendedProperties.set(False)
            self.ExcludeObjectTypesFilegroups.set(False)
            self.ExcludeObjectTypesFileTables.set(False)
            self.ExcludeObjectTypesFullTextCatalogs.set(False)
            self.ExcludeObjectTypesFullTextStoplists.set(False)
            self.ExcludeObjectTypesMessageTypes.set(False)
            self.ExcludeObjectTypesPartitionFunctions.set(False)
            self.ExcludeObjectTypesPartitionSchemes.set(False)
            self.ExcludeObjectTypesPermissions.set(False)
            self.ExcludeObjectTypesQueues.set(False)
            self.ExcludeObjectTypesRemoteServiceBindings.set(False)
            self.ExcludeObjectTypesRoleMembership.set(False)
            self.ExcludeObjectTypesRules.set(False)
            self.ExcludeObjectTypesScalarValuedFunctions.set(False)
            self.ExcludeObjectTypesSearchPropertyLists.set(False)
            self.ExcludeObjectTypesSequences.set(False)
            self.ExcludeObjectTypesServices.set(False)
            self.ExcludeObjectTypesSignatures.set(False)
            self.ExcludeObjectTypesStoredProcedures.set(False)
            self.ExcludeObjectTypesSymmetricKeys.set(False)
            self.ExcludeObjectTypesSynonyms.set(False)
            self.ExcludeObjectTypesTables.set(False)
            self.ExcludeObjectTypesTableValuedFunctions.set(False)
            self.ExcludeObjectTypesUserDefinedDataTypes.set(False)
            self.ExcludeObjectTypesUserDefinedTableTypes.set(False)
            self.ExcludeObjectTypesClrUserDefinedTypes.set(False)
            self.ExcludeObjectTypesUsers.set(False)
            self.ExcludeObjectTypesViews.set(False)
            self.ExcludeObjectTypesXmlSchemaCollections.set(False)
            self.ExcludeObjectTypesAudits.set(False)
            self.ExcludeObjectTypesCredentials.set(False)
            self.ExcludeObjectTypesCryptographicProviders.set(False)
            self.ExcludeObjectTypesDatabaseAuditSpecifications.set(False)
            self.ExcludeObjectTypesEndpoints.set(False)
            self.ExcludeObjectTypesErrorMessages.set(False)
            self.ExcludeObjectTypesEventNotifications.set(False)
            self.ExcludeObjectTypesEventSessions.set(False)
            self.ExcludeObjectTypesLinkedServerLogins.set(False)
            self.ExcludeObjectTypesLinkedServers.set(False)
            self.ExcludeObjectTypesLogins.set(False)
            self.ExcludeObjectTypesRoutes.set(False)
            self.ExcludeObjectTypesServerAuditSpecifications.set(False)
            self.ExcludeObjectTypesServerRoleMembership.set(False)
            self.ExcludeObjectTypesServerRoles.set(False)
            self.ExcludeObjectTypesServerTriggers.set(False)

    def EnDisScrAllowDropBlockingAssemblies(self):
        if self.ChkButtonAllowDropBlockingAssemblies.get() is True:
            self.LblAllowDropBlockingAssemblies.config(state='normal')
            self.EnDisValueAllowDropBlockingAssemblies.config(state='normal')

        elif self.ChkButtonAllowDropBlockingAssemblies.get() is False:
            self.ValueAllowDropBlockingAssemblies.set("False")
            self.LblAllowDropBlockingAssemblies.config(state='disabled')
            self.EnDisValueAllowDropBlockingAssemblies.config(state='disabled')

    def EnDisScrAllowIncompatiblePlatform(self):
        if self.ChkButtonAllowIncompatiblePlatform.get() is True:
            self.LblAllowIncompatiblePlatform
            self.LblAllowIncompatiblePlatform.config(state='normal')
            self.EnDisValueAllowIncompatiblePlatform.config(state='normal')

        elif self.ChkButtonAllowIncompatiblePlatform.get() is False:
            self.ValueAllowIncompatiblePlatform.set("False")
            self.LblAllowIncompatiblePlatform.config(state='disabled')
            self.EnDisValueAllowIncompatiblePlatform.config(state='disabled')

    def EnDisScrBackupDatabaseBeforeChanges(self):
        if self.ChkButtonBackupDatabaseBeforeChanges.get() is True:
            self.LblBackupDatabaseBeforeChanges.config(state='normal')
            self.EnDisValueBackupDatabaseBeforeChanges.config(state='normal')

        elif self.ChkButtonBackupDatabaseBeforeChanges.get() is False:
            self.ValueBackupDatabaseBeforeChanges.set("False")
            self.LblBackupDatabaseBeforeChanges.config(state='disabled')
            self.EnDisValueBackupDatabaseBeforeChanges.config(state='disabled')

    def EnDisScrBlockOnPossibleDataLoss(self):
        if self.ChkButtonBlockOnPossibleDataLoss.get() is True:
            self.LblBlockOnPossibleDataLoss.config(state='normal')
            self.EnDisValueBlockOnPossibleDataLoss.config(state='normal')

        elif self.ChkButtonBlockOnPossibleDataLoss.get() is False:
            self.ValueBlockOnPossibleDataLoss.set("True")
            self.LblBlockOnPossibleDataLoss.config(state='disabled')
            self.EnDisValueBlockOnPossibleDataLoss.config(state='disabled')

    def EnDisScrBlockWhenDriftDetected(self):
        if self.ChkButtonBlockWhenDriftDetected.get() is True:
            self.LblBlockWhenDriftDetected.config(state='normal')
            self.EnDisValueBlockWhenDriftDetected.config(state='normal')

        elif self.ChkButtonBlockWhenDriftDetected.get() is False:
            self.ValueBlockWhenDriftDetected.set("True")
            self.LblBlockWhenDriftDetected.config(state='disabled')
            self.EnDisValueBlockWhenDriftDetected.config(state='disabled')

    def EnDisScrCommandTimeout(self):
        if self.ChkButtonCommandTimeout.get() is True:
            self.LblCommandTimeout.config(state='normal')
            self.EntryCommandTimeout.config(state='normal')

        elif self.ChkButtonCommandTimeout.get() is False:
            self.EntryCommandTimeout.delete(0, END)
            self.EntryCommandTimeout.insert(0, "60")
            self.LblCommandTimeout.config(state='disabled')
            self.EntryCommandTimeout.config(state='disabled')

    def EnDisScrCommentOutSetVarDeclarations(self):
        if self.ChkButtonCommentOutSetVarDeclarations.get() is True:
            self.LblCommentOutSetVarDeclarations.config(state='normal')
            self.EnDisValueCommentOutSetVarDeclarations.config(state='normal')

        elif self.ChkButtonCommentOutSetVarDeclarations.get() is False:
            self.ValueCommentOutSetVarDeclarations.set("False")
            self.LblCommentOutSetVarDeclarations.config(state='disabled')
            self.EnDisValueCommentOutSetVarDeclarations.config(state='disabled')

    def EnDisScrCompareUsingTargetCollation(self):
        if self.ChkButtonCompareUsingTargetCollation.get() is True:
            self.LblCompareUsingTargetCollation.config(state='normal')
            self.EnDisValueCompareUsingTargetCollation.config(state='normal')

        elif self.ChkButtonCompareUsingTargetCollation.get() is False:
            self.ValueCompareUsingTargetCollation.set("False")
            self.LblCompareUsingTargetCollation.config(state='disabled')
            self.EnDisValueCompareUsingTargetCollation.config(state='disabled')

    def EnDisScrCreateNewDatabase(self):
        if self.ChkButtonCreateNewDatabase.get() is True:
            self.LblCreateNewDatabase.config(state='normal')
            self.EnDisValueCreateNewDatabase.config(state='normal')

        elif self.ChkButtonCreateNewDatabase.get() is False:
            self.ValueCreateNewDatabase.set("False")
            self.LblCreateNewDatabase.config(state='disabled')
            self.EnDisValueCreateNewDatabase.config(state='disabled')

    def EnDisScrDeployDatabaseInSingleUserMode(self):
        if self.ChkButtonDeployDatabaseInSingleUserMode.get() is True:
            self.LblDeployDatabaseInSingleUserMode.config(state='normal')
            self.EnDisValueDeployDatabaseInSingleUserMode.config(state='normal')

        elif self.ChkButtonDeployDatabaseInSingleUserMode.get() is False:
            self.ValueDeployDatabaseInSingleUserMode.set("False")
            self.LblDeployDatabaseInSingleUserMode.config(state='disabled')
            self.EnDisValueDeployDatabaseInSingleUserMode.config(state='disabled')

    def EnDisScrDisableAndReenableDdlTriggers(self):
        if self.ChkButtonDisableAndReenableDdlTriggers.get() is True:
            self.LblDisableAndReenableDdlTriggers.config(state='normal')
            self.EnDisValueDisableAndReenableDdlTriggers.config(state='normal')

        elif self.ChkButtonDisableAndReenableDdlTriggers.get() is False:
            self.ValueDisableAndReenableDdlTriggers.set("True")
            self.LblDisableAndReenableDdlTriggers.config(state='disabled')
            self.EnDisValueDisableAndReenableDdlTriggers.config(state='disabled')

    def EnDisScrDoNotAlterChangeDataCaptureObjects(self):
        if self.ChkButtonDoNotAlterChangeDataCaptureObjects.get() is True:
            self.LblDoNotAlterChangeDataCaptureObjects.config(state='normal')
            self.EnDisValueDoNotAlterChangeDataCaptureObjects.config(state='normal')

        elif self.ChkButtonDoNotAlterChangeDataCaptureObjects.get() is False:
            self.ValueDoNotAlterChangeDataCaptureObjects.set("True")
            self.LblDoNotAlterChangeDataCaptureObjects.config(state='disabled')
            self.EnDisValueDoNotAlterChangeDataCaptureObjects.config(state='disabled')

    def EnDisScrDoNotAlterReplicatedObjects(self):
        if self.ChkButtonDoNotAlterReplicatedObjects.get() is True:
            self.LblDoNotAlterReplicatedObjects.config(state='normal')
            self.EnDisValueDoNotAlterReplicatedObjects.config(state='normal')

        elif self.ChkButtonDoNotAlterReplicatedObjects.get() is False:
            self.ValueDoNotAlterReplicatedObjects.set("True")
            self.LblDoNotAlterReplicatedObjects.config(state='disabled')
            self.EnDisValueDoNotAlterReplicatedObjects.config(state='disabled')

    def EnDisScrDoNotDropObjectTypes(self):
        if self.ChkButtonDoNotDropObjectTypes.get() is True:
            self.LblDoNotDropObjectTypes.config(state='normal')
            self.EnDisValueDoNotDropObjectTypes.config(state='normal')

        elif self.ChkButtonDoNotDropObjectTypes.get() is False:
            # self.ValueDoNotDropObjectTypes.set("N/A.")
            self.reset_DoNotDropObjects("all")
            self.LblDoNotDropObjectTypes.config(state='disabled')
            self.EnDisValueDoNotDropObjectTypes.config(state='disabled')

    def EnDisScrDropConstraintsNotInSource(self):
        if self.ChkButtonDropConstraintsNotInSource.get() is True:
            self.LblDropConstraintsNotInSource.config(state='normal')
            self.EnDisValueDropConstraintsNotInSource.config(state='normal')

        elif self.ChkButtonDropConstraintsNotInSource.get() is False:
            self.ValueDropConstraintsNotInSource.set("True")
            self.LblDropConstraintsNotInSource.config(state='disabled')
            self.EnDisValueDropConstraintsNotInSource.config(state='disabled')

    def EnDisScrDropDmlTriggersNotInSource(self):
        if self.ChkButtonDropDmlTriggersNotInSource.get() is True:
            self.LblDropDmlTriggersNotInSource.config(state='normal')
            self.EnDisValueDropDmlTriggersNotInSource.config(state='normal')

        elif self.ChkButtonDropDmlTriggersNotInSource.get() is False:
            self.ValueDropDmlTriggersNotInSource.set("True")
            self.LblDropDmlTriggersNotInSource.config(state='disabled')
            self.EnDisValueDropDmlTriggersNotInSource.config(state='disabled')

    def EnDisScrDropExtendedPropertiesNotInSource(self):
        if self.ChkButtonDropExtendedPropertiesNotInSource.get() is True:
            self.LblDropExtendedPropertiesNotInSource.config(state='normal')
            self.EnDisValueDropExtendedPropertiesNotInSource.config(state='normal')

        elif self.ChkButtonDropExtendedPropertiesNotInSource.get() is False:
            self.ValueDropExtendedPropertiesNotInSource.set("True")
            self.LblDropExtendedPropertiesNotInSource.config(state='disabled')
            self.EnDisValueDropExtendedPropertiesNotInSource.config(state='disabled')

    def EnDisScrDropIndexesNotInSource(self):
        if self.ChkButtonDropIndexesNotInSource.get() is True:
            self.LblDropIndexesNotInSource.config(state='normal')
            self.EnDisValueDropIndexesNotInSource.config(state='normal')

        elif self.ChkButtonDropIndexesNotInSource.get() is False:
            self.ValueDropIndexesNotInSource.set("True")
            self.LblDropIndexesNotInSource.config(state='disabled')
            self.EnDisValueDropIndexesNotInSource.config(state='disabled')

    def EnDisScrDropObjectsNotInSource(self):
        if self.ChkButtonDropObjectsNotInSource.get() is True:
            self.LblDropObjectsNotInSource.config(state='normal')
            self.EnDisValueDropObjectsNotInSource.config(state='normal')

        elif self.ChkButtonDropObjectsNotInSource.get() is False:
            self.ValueDropObjectsNotInSource.set("False")
            self.LblDropObjectsNotInSource.config(state='disabled')
            self.EnDisValueDropObjectsNotInSource.config(state='disabled')

    def EnDisScrDropPermissionsNotInSource(self):
        if self.ChkButtonDropPermissionsNotInSource.get() is True:
            self.LblDropPermissionsNotInSource.config(state='normal')
            self.EnDisValueDropPermissionsNotInSource.config(state='normal')

        elif self.ChkButtonDropPermissionsNotInSource.get() is False:
            self.ValueDropPermissionsNotInSource.set("False")
            self.LblDropPermissionsNotInSource.config(state='disabled')
            self.EnDisValueDropPermissionsNotInSource.config(state='disabled')

    def EnDisScrDropRoleMembersNotInSource(self):
        if self.ChkButtonDropRoleMembersNotInSource.get() is True:
            self.LblDropRoleMembersNotInSource.config(state='normal')
            self.EnDisValueDropRoleMembersNotInSource.config(state='normal')

        elif self.ChkButtonDropRoleMembersNotInSource.get() is False:
            self.ValueDropRoleMembersNotInSource.set("False")
            self.LblDropRoleMembersNotInSource.config(state='disabled')
            self.EnDisValueDropRoleMembersNotInSource.config(state='disabled')

    def EnDisScrExcludeObjectTypes(self):
        if self.ChkButtonExcludeObjectTypes.get() is True:
            self.LblExcludeObjectTypes.config(state='normal')
            self.EnDisValueExcludeObjectTypes.config(state='normal')

        elif self.ChkButtonExcludeObjectTypes.get() is False:
            # self.ValueExcludeObjectTypes.set("N/A.")
            self.reset_ExcludeObjectTypes("all")
            self.LblExcludeObjectTypes.config(state='disabled')
            self.EnDisValueExcludeObjectTypes.config(state='disabled')

    def EnDisScrGenerateSmartDefaults(self):
        if self.ChkButtonGenerateSmartDefaults.get() is True:
            self.LblGenerateSmartDefaults.config(state='normal')
            self.EnDisValueGenerateSmartDefaults.config(state='normal')

        elif self.ChkButtonGenerateSmartDefaults.get() is False:
            self.ValueGenerateSmartDefaults.set("False")
            self.LblGenerateSmartDefaults.config(state='disabled')
            self.EnDisValueGenerateSmartDefaults.config(state='disabled')

    def EnDisScrIgnoreAnsiNulls(self):
        if self.ChkButtonIgnoreAnsiNulls.get() is True:
            self.LblIgnoreAnsiNulls.config(state='normal')
            self.EnDisValueIgnoreAnsiNulls.config(state='normal')

        elif self.ChkButtonIgnoreAnsiNulls.get() is False:
            self.ValueIgnoreAnsiNulls.set("False")
            self.LblIgnoreAnsiNulls.config(state='disabled')
            self.EnDisValueIgnoreAnsiNulls.config(state='disabled')

    def EnDisScrIgnoreAuthorizer(self):
        if self.ChkButtonIgnoreAuthorizer.get() is True:
            self.LblIgnoreAuthorizer.config(state='normal')
            self.EnDisValueIgnoreAuthorizer.config(state='normal')

        elif self.ChkButtonIgnoreAuthorizer.get() is False:
            self.ValueIgnoreAuthorizer.set("False")
            self.LblIgnoreAuthorizer.config(state='disabled')
            self.EnDisValueIgnoreAuthorizer.config(state='disabled')

    def EnDisScrIgnoreColumnCollation(self):
        if self.ChkButtonIgnoreColumnCollation.get() is True:
            self.LblIgnoreColumnCollation.config(state='normal')
            self.EnDisValueIgnoreColumnCollation.config(state='normal')

        elif self.ChkButtonIgnoreColumnCollation.get() is False:
            self.ValueIgnoreColumnCollation.set("False")
            self.LblIgnoreColumnCollation.config(state='disabled')
            self.EnDisValueIgnoreColumnCollation.config(state='disabled')

    def EnDisScrIgnoreComments(self):
        if self.ChkButtonIgnoreComments.get() is True:
            self.LblIgnoreComments.config(state='normal')
            self.EnDisValueIgnoreComments.config(state='normal')

        elif self.ChkButtonIgnoreComments.get() is False:
            self.ValueIgnoreComments.set("False")
            self.LblIgnoreComments.config(state='disabled')
            self.EnDisValueIgnoreComments.config(state='disabled')

    def EnDisScrIgnoreCryptographicProviderFilePath(self):
        if self.ChkButtonIgnoreCryptographicProviderFilePath.get() is True:
            self.LblIgnoreCryptographicProviderFilePath.config(state='normal')
            self.EnDisValueIgnoreCryptographicProviderFilePath.config(state='normal')

        elif self.ChkButtonIgnoreCryptographicProviderFilePath.get() is False:
            self.ValueIgnoreCryptographicProviderFilePath.set("True")
            self.LblIgnoreCryptographicProviderFilePath.config(state='disabled')
            self.EnDisValueIgnoreCryptographicProviderFilePath.config(state='disabled')

    def EnDisScrIgnoreDdlTriggerOrder(self):
        if self.ChkButtonIgnoreDdlTriggerOrder.get() is True:
            self.LblIgnoreDdlTriggerOrder.config(state='normal')
            self.EnDisValueIgnoreDdlTriggerOrder.config(state='normal')

        elif self.ChkButtonIgnoreDdlTriggerOrder.get() is False:
            self.ValueIgnoreDdlTriggerOrder.set("False")
            self.LblIgnoreDdlTriggerOrder.config(state='disabled')
            self.EnDisValueIgnoreDdlTriggerOrder.config(state='disabled')

    def EnDisScrIgnoreDdlTriggerState(self):
        if self.ChkButtonIgnoreDdlTriggerState.get() is True:
            self.LblIgnoreDdlTriggerState.config(state='normal')
            self.EnDisValueIgnoreDdlTriggerState.config(state='normal')

        elif self.ChkButtonIgnoreDdlTriggerState.get() is False:
            self.ValueIgnoreDdlTriggerState.set("False")
            self.LblIgnoreDdlTriggerState.config(state='disabled')
            self.EnDisValueIgnoreDdlTriggerState.config(state='disabled')

    def EnDisScrIgnoreDefaultSchema(self):
        if self.ChkButtonIgnoreDefaultSchema.get() is True:
            self.LblIgnoreDefaultSchema.config(state='normal')
            self.EnDisValueIgnoreDefaultSchema.config(state='normal')

        elif self.ChkButtonIgnoreDefaultSchema.get() is False:
            self.ValueIgnoreDefaultSchema.set("False")
            self.LblIgnoreDefaultSchema.config(state='disabled')
            self.EnDisValueIgnoreDefaultSchema.config(state='disabled')

    def EnDisScrIgnoreDmlTriggerOrder(self):
        if self.ChkButtonIgnoreDmlTriggerOrder.get() is True:
            self.LblIgnoreDmlTriggerOrder.config(state='normal')
            self.EnDisValueIgnoreDmlTriggerOrder.config(state='normal')

        elif self.ChkButtonIgnoreDmlTriggerOrder.get() is False:
            self.ValueIgnoreDmlTriggerOrder.set("False")
            self.LblIgnoreDmlTriggerOrder.config(state='disabled')
            self.EnDisValueIgnoreDmlTriggerOrder.config(state='disabled')

    def EnDisScrIgnoreDmlTriggerState(self):
        if self.ChkButtonIgnoreDmlTriggerState.get() is True:
            self.LblIgnoreDmlTriggerState.config(state='normal')
            self.EnDisValueIgnoreDmlTriggerState.config(state='normal')

        elif self.ChkButtonIgnoreDmlTriggerState.get() is False:
            self.ValueIgnoreDmlTriggerState.set("False")
            self.LblIgnoreDmlTriggerState.config(state='disabled')
            self.EnDisValueIgnoreDmlTriggerState.config(state='disabled')

    def EnDisScrIgnoreExtendedProperties(self):
        if self.ChkButtonIgnoreExtendedProperties.get() is True:
            self.LblIgnoreExtendedProperties.config(state='normal')
            self.EnDisValueIgnoreExtendedProperties.config(state='normal')

        elif self.ChkButtonIgnoreExtendedProperties.get() is False:
            self.ValueIgnoreExtendedProperties.set("False")
            self.LblIgnoreExtendedProperties.config(state='disabled')
            self.EnDisValueIgnoreExtendedProperties.config(state='disabled')

    def EnDisScrIgnoreFileAndLogFilePath(self):
        if self.ChkButtonIgnoreFileAndLogFilePath.get() is True:
            self.LblIgnoreFileAndLogFilePath.config(state='normal')
            self.EnDisValueIgnoreFileAndLogFilePath.config(state='normal')

        elif self.ChkButtonIgnoreFileAndLogFilePath.get() is False:
            self.ValueIgnoreFileAndLogFilePath.set("True")
            self.LblIgnoreFileAndLogFilePath.config(state='disabled')
            self.EnDisValueIgnoreFileAndLogFilePath.config(state='disabled')

    def EnDisScrIgnoreFilegroupPlacement(self):
        if self.ChkButtonIgnoreFilegroupPlacement.get() is True:
            self.LblIgnoreFilegroupPlacement.config(state='normal')
            self.EnDisValueIgnoreFilegroupPlacement.config(state='normal')

        elif self.ChkButtonIgnoreFilegroupPlacement.get() is False:
            self.ValueIgnoreFilegroupPlacement.set("True")
            self.LblIgnoreFilegroupPlacement.config(state='disabled')
            self.EnDisValueIgnoreFilegroupPlacement.config(state='disabled')

    def EnDisScrIgnoreFileSize(self):
        if self.ChkButtonIgnoreFileSize.get() is True:
            self.LblIgnoreFileSize.config(state='normal')
            self.EnDisValueIgnoreFileSize.config(state='normal')

        elif self.ChkButtonIgnoreFileSize.get() is False:
            self.ValueIgnoreFileSize.set("True")
            self.LblIgnoreFileSize.config(state='disabled')
            self.EnDisValueIgnoreFileSize.config(state='disabled')

    def EnDisScrIgnoreFillFactor(self):
        if self.ChkButtonIgnoreFillFactor.get() is True:
            self.LblIgnoreFillFactor.config(state='normal')
            self.EnDisValueIgnoreFillFactor.config(state='normal')

        elif self.ChkButtonIgnoreFillFactor.get() is False:
            self.ValueIgnoreFillFactor.set("True")
            self.LblIgnoreFillFactor.config(state='disabled')
            self.EnDisValueIgnoreFillFactor.config(state='disabled')

    def EnDisScrIgnoreFullTextCatalogFilePath(self):
        if self.ChkButtonIgnoreFullTextCatalogFilePath.get() is True:
            self.LblIgnoreFullTextCatalogFilePath.config(state='normal')
            self.EnDisValueIgnoreFullTextCatalogFilePath.config(state='normal')

        elif self.ChkButtonIgnoreFullTextCatalogFilePath.get() is False:
            self.ValueIgnoreFullTextCatalogFilePath.set("True")
            self.LblIgnoreFullTextCatalogFilePath.config(state='disabled')
            self.EnDisValueIgnoreFullTextCatalogFilePath.config(state='disabled')

    def EnDisScrIgnoreIdentitySeed(self):
        if self.ChkButtonIgnoreIdentitySeed.get() is True:
            self.LblIgnoreIdentitySeed.config(state='normal')
            self.EnDisValueIgnoreIdentitySeed.config(state='normal')

        elif self.ChkButtonIgnoreIdentitySeed.get() is False:
            self.ValueIgnoreIdentitySeed.set("False")
            self.LblIgnoreIdentitySeed.config(state='disabled')
            self.EnDisValueIgnoreIdentitySeed.config(state='disabled')

    def EnDisScrIgnoreIncrement(self):
        if self.ChkButtonIgnoreIncrement.get() is True:
            self.LblIgnoreIncrement.config(state='normal')
            self.EnDisValueIgnoreIncrement.config(state='normal')

        elif self.ChkButtonIgnoreIncrement.get() is False:
            self.ValueIgnoreIncrement.set("False")
            self.LblIgnoreIncrement.config(state='disabled')
            self.EnDisValueIgnoreIncrement.config(state='disabled')

    def EnDisScrIgnoreIndexOptions(self):
        if self.ChkButtonIgnoreIndexOptions.get() is True:
            self.LblIgnoreIndexOptions.config(state='normal')
            self.EnDisValueIgnoreIndexOptions.config(state='normal')

        elif self.ChkButtonIgnoreIndexOptions.get() is False:
            self.ValueIgnoreIndexOptions.set("False")
            self.LblIgnoreIndexOptions.config(state='disabled')
            self.EnDisValueIgnoreIndexOptions.config(state='disabled')

    def EnDisScrIgnoreIndexPadding(self):
        if self.ChkButtonIgnoreIndexPadding.get() is True:
            self.LblIgnoreIndexPadding.config(state='normal')
            self.EnDisValueIgnoreIndexPadding.config(state='normal')

        elif self.ChkButtonIgnoreIndexPadding.get() is False:
            self.ValueIgnoreIndexPadding.set("True")
            self.LblIgnoreIndexPadding.config(state='disabled')
            self.EnDisValueIgnoreIndexPadding.config(state='disabled')

    def EnDisScrIgnoreKeywordCasing(self):
        if self.ChkButtonIgnoreKeywordCasing.get() is True:
            self.LblIgnoreKeywordCasing.config(state='normal')
            self.EnDisValueIgnoreKeywordCasing.config(state='normal')

        elif self.ChkButtonIgnoreKeywordCasing.get() is False:
            self.ValueIgnoreKeywordCasing.set("True")
            self.LblIgnoreKeywordCasing.config(state='disabled')
            self.EnDisValueIgnoreKeywordCasing.config(state='disabled')

    def EnDisScrIgnoreLockHintsOnIndexes(self):
        if self.ChkButtonIgnoreLockHintsOnIndexes.get() is True:
            self.LblIgnoreLockHintsOnIndexes.config(state='normal')
            self.EnDisValueIgnoreLockHintsOnIndexes.config(state='normal')

        elif self.ChkButtonIgnoreLockHintsOnIndexes.get() is False:
            self.ValueIgnoreLockHintsOnIndexes.set("False")
            self.LblIgnoreLockHintsOnIndexes.config(state='disabled')
            self.EnDisValueIgnoreLockHintsOnIndexes.config(state='disabled')

    def EnDisScrIgnoreLoginSids(self):
        if self.ChkButtonIgnoreLoginSids.get() is True:
            self.LblIgnoreLoginSids.config(state='normal')
            self.EnDisValueIgnoreLoginSids.config(state='normal')

        elif self.ChkButtonIgnoreLoginSids.get() is False:
            self.ValueIgnoreLoginSids.set("True")
            self.LblIgnoreLoginSids.config(state='disabled')
            self.EnDisValueIgnoreLoginSids.config(state='disabled')

    def EnDisScrIgnoreNotForReplication(self):
        if self.ChkButtonIgnoreNotForReplication.get() is True:
            self.LblIgnoreNotForReplication.config(state='normal')
            self.EnDisValueIgnoreNotForReplication.config(state='normal')

        elif self.ChkButtonIgnoreNotForReplication.get() is False:
            self.ValueIgnoreNotForReplication.set("False")
            self.LblIgnoreNotForReplication.config(state='disabled')
            self.EnDisValueIgnoreNotForReplication.config(state='disabled')

    def EnDisScrIgnoreObjectPlacementOnPartitionScheme(self):
        if self.ChkButtonIgnoreObjectPlacementOnPartitionScheme.get() is True:
            self.LblIgnoreObjectPlacementOnPartitionScheme.config(state='normal')
            self.EnDisValueIgnoreObjectPlacementOnPartitionScheme.config(state='normal')

        elif self.ChkButtonIgnoreObjectPlacementOnPartitionScheme.get() is False:
            self.ValueIgnoreObjectPlacementOnPartitionScheme.set("True")
            self.LblIgnoreObjectPlacementOnPartitionScheme.config(state='disabled')
            self.EnDisValueIgnoreObjectPlacementOnPartitionScheme.config(state='disabled')

    def EnDisScrIgnorePartitionSchemes(self):
        if self.ChkButtonIgnorePartitionSchemes.get() is True:
            self.LblIgnorePartitionSchemes.config(state='normal')
            self.EnDisValueIgnorePartitionSchemes.config(state='normal')

        elif self.ChkButtonIgnorePartitionSchemes.get() is False:
            self.ValueIgnorePartitionSchemes.set("False")
            self.LblIgnorePartitionSchemes.config(state='disabled')
            self.EnDisValueIgnorePartitionSchemes.config(state='disabled')

    def EnDisScrIgnorePermissions(self):
        if self.ChkButtonIgnorePermissions.get() is True:
            self.LblIgnorePermissions.config(state='normal')
            self.EnDisValueIgnorePermissions.config(state='normal')

        elif self.ChkButtonIgnorePermissions.get() is False:
            self.ValueIgnorePermissions.set("False")
            self.LblIgnorePermissions.config(state='disabled')
            self.EnDisValueIgnorePermissions.config(state='disabled')

    def EnDisScrIgnoreQuotedIdentifiers(self):
        if self.ChkButtonIgnoreQuotedIdentifiers.get() is True:
            self.LblIgnoreQuotedIdentifiers.config(state='normal')
            self.EnDisValueIgnoreQuotedIdentifiers.config(state='normal')

        elif self.ChkButtonIgnoreQuotedIdentifiers.get() is False:
            self.ValueIgnoreQuotedIdentifiers.set("False")
            self.LblIgnoreQuotedIdentifiers.config(state='disabled')
            self.EnDisValueIgnoreQuotedIdentifiers.config(state='disabled')

    def EnDisScrIgnoreRoleMembership(self):
        if self.ChkButtonIgnoreRoleMembership.get() is True:
            self.LblIgnoreRoleMembership.config(state='normal')
            self.EnDisValueIgnoreRoleMembership.config(state='normal')

        elif self.ChkButtonIgnoreRoleMembership.get() is False:
            self.ValueIgnoreRoleMembership.set("False")
            self.LblIgnoreRoleMembership.config(state='disabled')
            self.EnDisValueIgnoreRoleMembership.config(state='disabled')

    def EnDisScrIgnoreRouteLifetime(self):
        if self.ChkButtonIgnoreRouteLifetime.get() is True:
            self.LblIgnoreRouteLifetime.config(state='normal')
            self.EnDisValueIgnoreRouteLifetime.config(state='normal')

        elif self.ChkButtonIgnoreRouteLifetime.get() is False:
            self.ValueIgnoreRouteLifetime.set("True")
            self.LblIgnoreRouteLifetime.config(state='disabled')
            self.EnDisValueIgnoreRouteLifetime.config(state='disabled')

    def EnDisScrIgnoreSemicolonBetweenStatements(self):
        if self.ChkButtonIgnoreSemicolonBetweenStatements.get() is True:
            self.LblIgnoreSemicolonBetweenStatements.config(state='normal')
            self.EnDisValueIgnoreSemicolonBetweenStatements.config(state='normal')

        elif self.ChkButtonIgnoreSemicolonBetweenStatements.get() is False:
            self.ValueIgnoreSemicolonBetweenStatements.set("True")
            self.LblIgnoreSemicolonBetweenStatements.config(state='disabled')
            self.EnDisValueIgnoreSemicolonBetweenStatements.config(state='disabled')

    def EnDisScrIgnoreTableOptions(self):
        if self.ChkButtonIgnoreTableOptions.get() is True:
            self.LblIgnoreTableOptions.config(state='normal')
            self.EnDisValueIgnoreTableOptions.config(state='normal')

        elif self.ChkButtonIgnoreTableOptions.get() is False:
            self.ValueIgnoreTableOptions.set("False")
            self.LblIgnoreTableOptions.config(state='disabled')
            self.EnDisValueIgnoreTableOptions.config(state='disabled')

    def EnDisScrIgnoreUserSettingsObjects(self):
        if self.ChkButtonIgnoreUserSettingsObjects.get() is True:
            self.LblIgnoreUserSettingsObjects.config(state='normal')
            self.EnDisValueIgnoreUserSettingsObjects.config(state='normal')

        elif self.ChkButtonIgnoreUserSettingsObjects.get() is False:
            self.ValueIgnoreUserSettingsObjects.set("False")
            self.LblIgnoreUserSettingsObjects.config(state='disabled')
            self.EnDisValueIgnoreUserSettingsObjects.config(state='disabled')

    def EnDisScrIgnoreWhitespace(self):
        if self.ChkButtonIgnoreWhitespace.get() is True:
            self.LblIgnoreWhitespace.config(state='normal')
            self.EnDisValueIgnoreWhitespace.config(state='normal')

        elif self.ChkButtonIgnoreWhitespace.get() is False:
            self.ValueIgnoreWhitespace.set("True")
            self.LblIgnoreWhitespace.config(state='disabled')
            self.EnDisValueIgnoreWhitespace.config(state='disabled')

    def EnDisScrIgnoreWithNocheckOnCheckConstraints(self):
        if self.ChkButtonIgnoreWithNocheckOnCheckConstraints.get() is True:
            self.LblIgnoreWithNocheckOnCheckConstraints.config(state='normal')
            self.EnDisValueIgnoreWithNocheckOnCheckConstraints.config(state='normal')

        elif self.ChkButtonIgnoreWithNocheckOnCheckConstraints.get() is False:
            self.ValueIgnoreWithNocheckOnCheckConstraints.set("False")
            self.LblIgnoreWithNocheckOnCheckConstraints.config(state='disabled')
            self.EnDisValueIgnoreWithNocheckOnCheckConstraints.config(state='disabled')

    def EnDisScrIgnoreWithNocheckOnForeignKeys(self):
        if self.ChkButtonIgnoreWithNocheckOnForeignKeys.get() is True:
            self.LblIgnoreWithNocheckOnForeignKeys.config(state='normal')
            self.EnDisValueIgnoreWithNocheckOnForeignKeys.config(state='normal')

        elif self.ChkButtonIgnoreWithNocheckOnForeignKeys.get() is False:
            self.ValueIgnoreWithNocheckOnForeignKeys.set("False")
            self.LblIgnoreWithNocheckOnForeignKeys.config(state='disabled')
            self.EnDisValueIgnoreWithNocheckOnForeignKeys.config(state='disabled')

    def EnDisScrIncludeCompositeObjects(self):
        if self.ChkButtonIncludeCompositeObjects.get() is True:
            self.LblIncludeCompositeObjects.config(state='normal')
            self.EnDisValueIncludeCompositeObjects.config(state='normal')

        elif self.ChkButtonIncludeCompositeObjects.get() is False:
            self.ValueIncludeCompositeObjects.set("False")
            self.LblIncludeCompositeObjects.config(state='disabled')
            self.EnDisValueIncludeCompositeObjects.config(state='disabled')

    def EnDisScrIncludeTransactionalScripts(self):
        if self.ChkButtonIncludeTransactionalScripts.get() is True:
            self.LblIncludeTransactionalScripts.config(state='normal')
            self.EnDisValueIncludeTransactionalScripts.config(state='normal')

        elif self.ChkButtonIncludeTransactionalScripts.get() is False:
            self.ValueIncludeTransactionalScripts.set("False")
            self.LblIncludeTransactionalScripts.config(state='disabled')
            self.EnDisValueIncludeTransactionalScripts.config(state='disabled')

    def EnDisScrNoAlterStatementsToChangeClrTypes(self):
        if self.ChkButtonNoAlterStatementsToChangeClrTypes.get() is True:
            self.LblNoAlterStatementsToChangeClrTypes.config(state='normal')
            self.EnDisValueNoAlterStatementsToChangeClrTypes.config(state='normal')

        elif self.ChkButtonNoAlterStatementsToChangeClrTypes.get() is False:
            self.ValueNoAlterStatementsToChangeClrTypes.set("False")
            self.LblNoAlterStatementsToChangeClrTypes.config(state='disabled')
            self.EnDisValueNoAlterStatementsToChangeClrTypes.config(state='disabled')

    def EnDisScrPopulateFilesOnFilegroups(self):
        if self.ChkButtonPopulateFilesOnFilegroups.get() is True:
            self.LblPopulateFilesOnFilegroups.config(state='normal')
            self.EnDisValuePopulateFilesOnFilegroups.config(state='normal')

        elif self.ChkButtonPopulateFilesOnFilegroups.get() is False:
            self.ValuePopulateFilesOnFilegroups.set("True")
            self.LblPopulateFilesOnFilegroups.config(state='disabled')
            self.EnDisValuePopulateFilesOnFilegroups.config(state='disabled')

    def EnDisScrRegisterDataTierApplication(self):
        if self.ChkButtonRegisterDataTierApplication.get() is True:
            self.LblRegisterDataTierApplication.config(state='normal')
            self.EnDisValueRegisterDataTierApplication.config(state='normal')

        elif self.ChkButtonRegisterDataTierApplication.get() is False:
            self.ValueRegisterDataTierApplication.set("False")
            self.LblRegisterDataTierApplication.config(state='disabled')
            self.EnDisValueRegisterDataTierApplication.config(state='disabled')

    def EnDisScrRunDeploymentPlanExecutors(self):
        if self.ChkButtonRunDeploymentPlanExecutors.get() is True:
            self.LblRunDeploymentPlanExecutors.config(state='normal')
            self.EnDisValueRunDeploymentPlanExecutors.config(state='normal')

        elif self.ChkButtonRunDeploymentPlanExecutors.get() is False:
            self.ValueRunDeploymentPlanExecutors.set("False")
            self.LblRunDeploymentPlanExecutors.config(state='disabled')
            self.EnDisValueRunDeploymentPlanExecutors.config(state='disabled')

    def EnDisScrScriptDatabaseCollation(self):
        if self.ChkButtonScriptDatabaseCollation.get() is True:
            self.LblScriptDatabaseCollation.config(state='normal')
            self.EnDisValueScriptDatabaseCollation.config(state='normal')

        elif self.ChkButtonScriptDatabaseCollation.get() is False:
            self.ValueScriptDatabaseCollation.set("False")
            self.LblScriptDatabaseCollation.config(state='disabled')
            self.EnDisValueScriptDatabaseCollation.config(state='disabled')

    def EnDisScrScriptDatabaseCompatibility(self):
        if self.ChkButtonScriptDatabaseCompatibility.get() is True:
            self.LblScriptDatabaseCompatibility.config(state='normal')
            self.EnDisValueScriptDatabaseCompatibility.config(state='normal')

        elif self.ChkButtonScriptDatabaseCompatibility.get() is False:
            self.ValueScriptDatabaseCompatibility.set("True")
            self.LblScriptDatabaseCompatibility.config(state='disabled')
            self.EnDisValueScriptDatabaseCompatibility.config(state='disabled')

    def EnDisScrScriptDatabaseOptions(self):
        if self.ChkButtonScriptDatabaseOptions.get() is True:
            self.LblScriptDatabaseOptions.config(state='normal')
            self.EnDisValueScriptDatabaseOptions.config(state='normal')

        elif self.ChkButtonScriptDatabaseOptions.get() is False:
            self.ValueScriptDatabaseOptions.set("True")
            self.LblScriptDatabaseOptions.config(state='disabled')
            self.EnDisValueScriptDatabaseOptions.config(state='disabled')

    def EnDisScrScriptDeployStateChecks(self):
        if self.ChkButtonScriptDeployStateChecks.get() is True:
            self.LblScriptDeployStateChecks.config(state='normal')
            self.EnDisValueScriptDeployStateChecks.config(state='normal')

        elif self.ChkButtonScriptDeployStateChecks.get() is False:
            self.ValueScriptDeployStateChecks.set("False")
            self.LblScriptDeployStateChecks.config(state='disabled')
            self.EnDisValueScriptDeployStateChecks.config(state='disabled')

    def EnDisScrScriptFileSize(self):
        if self.ChkButtonScriptFileSize.get() is True:
            self.LblScriptFileSize.config(state='normal')
            self.EnDisValueScriptFileSize.config(state='normal')

        elif self.ChkButtonScriptFileSize.get() is False:
            self.ValueScriptFileSize.set("False")
            self.LblScriptFileSize.config(state='disabled')
            self.EnDisValueScriptFileSize.config(state='disabled')

    def EnDisScrScriptNewConstraintValidation(self):
        if self.ChkButtonScriptNewConstraintValidation.get() is True:
            self.LblScriptNewConstraintValidation.config(state='normal')
            self.EnDisValueScriptNewConstraintValidation.config(state='normal')

        elif self.ChkButtonScriptNewConstraintValidation.get() is False:
            self.ValueScriptNewConstraintValidation.set("True")
            self.LblScriptNewConstraintValidation.config(state='disabled')
            self.EnDisValueScriptNewConstraintValidation.config(state='disabled')

    def EnDisScrScriptRefreshModule(self):
        if self.ChkButtonScriptRefreshModule.get() is True:
            self.LblScriptRefreshModule.config(state='normal')
            self.EnDisValueScriptRefreshModule.config(state='normal')

        elif self.ChkButtonScriptRefreshModule.get() is False:
            self.ValueScriptRefreshModule.set("True")
            self.LblScriptRefreshModule.config(state='disabled')
            self.EnDisValueScriptRefreshModule.config(state='disabled')

    def EnDisScrStorage(self):
        if self.ChkButtonStorage.get() is True:
            self.LblStorage.config(state='normal')
            self.EnDisValueStorage.config(state='normal')

        elif self.ChkButtonStorage.get() is False:
            self.ValueStorage.set("Memory")
            self.LblStorage.config(state='disabled')
            self.EnDisValueStorage.config(state='disabled')

    def EnDisScrTreatVerificationErrorsAsWarnings(self):
        if self.ChkButtonTreatVerificationErrorsAsWarnings.get() is True:
            self.LblTreatVerificationErrorsAsWarnings.config(state='normal')
            self.EnDisValueTreatVerificationErrorsAsWarnings.config(state='normal')

        elif self.ChkButtonTreatVerificationErrorsAsWarnings.get() is False:
            self.ValueTreatVerificationErrorsAsWarnings.set("False")
            self.LblTreatVerificationErrorsAsWarnings.config(state='disabled')
            self.EnDisValueTreatVerificationErrorsAsWarnings.config(state='disabled')

    def EnDisScrUnmodifiableObjectWarnings(self):
        if self.ChkButtonUnmodifiableObjectWarnings.get() is True:
            self.LblUnmodifiableObjectWarnings.config(state='normal')
            self.EnDisValueUnmodifiableObjectWarnings.config(state='normal')

        elif self.ChkButtonUnmodifiableObjectWarnings.get() is False:
            self.ValueUnmodifiableObjectWarnings.set("True")
            self.LblUnmodifiableObjectWarnings.config(state='disabled')
            self.EnDisValueUnmodifiableObjectWarnings.config(state='disabled')

    def EnDisScrVerifyCollationCompatibility(self):
        if self.ChkButtonVerifyCollationCompatibility.get() is True:
            self.LblVerifyCollationCompatibility.config(state='normal')
            self.EnDisValueVerifyCollationCompatibility.config(state='normal')

        elif self.ChkButtonVerifyCollationCompatibility.get() is False:
            self.ValueVerifyCollationCompatibility.set("True")
            self.LblVerifyCollationCompatibility.config(state='disabled')
            self.EnDisValueVerifyCollationCompatibility.config(state='disabled')

    def EnDisScrVerifyDeployment(self):
        if self.ChkButtonVerifyDeployment.get() is True:
            self.LblVerifyDeployment.config(state='normal')
            self.EnDisValueVerifyDeployment.config(state='normal')

        elif self.ChkButtonVerifyDeployment.get() is False:
            self.ValueVerifyDeployment.set("True")
            self.LblVerifyDeployment.config(state='disabled')
            self.EnDisValueVerifyDeployment.config(state='disabled')

    def Prepare_Queries(self, source_button):
        # Query string for Pre-Deployment
        self.CmpExePreDeploymentQuery = 'sqlcmd -S ' + self.TargetServerEntry.get()
        # Query string for Extract
        self.CmpExeExtractQuery = 'CompareDeploy\\sqlpackage /Action:Extract /SourceServerName:' + self.SourceServerEntry.get() + ' /SourceDatabaseName:' + self.SourceDatabaseEntry.get()
        # Query string for Publish
        self.CmpExePublishQuery = 'CompareDeploy\\sqlpackage /Action:Publish /SourceFile:CompareDeploy\\temp\\' + self.SourceDatabaseEntry.get() + '.dacpac /TargetServerName:' + self.TargetServerEntry.get() + ' /TargetDatabaseName:' + self.TargetDatabaseEntry.get()
        # Query string for Script Generation
        self.CmpExeScriptQuery = 'CompareDeploy\\sqlpackage /Action:Script /SourceFile:CompareDeploy\\temp\\' + self.SourceDatabaseEntry.get() + '.dacpac /TargetServerName:' + self.TargetServerEntry.get() + ' /TargetDatabaseName:' + self.TargetDatabaseEntry.get() + ' /OutputPath:CompareDeploy\\temp\\' + self.TargetDatabaseEntry.get() + '.sql'

        if self.WinAuthSrcVariable.get() is False:
            self.CmpExeExtractQuery += ' /SourceUser:' + self.SourceUsernameEntry.get() + ' /SourcePassword:' + self.SourcePasswordEntry.get()

        if self.WinAuthTrgtVariable.get() is False:
            self.CmpExePreDeploymentQuery += ' -U ' + self.TargetUsernameEntry.get() + ' -P ' + self.TargetPasswordEntry.get()
            self.CmpExePublishQuery += ' /TargetUser:' + self.TargetUsernameEntry.get() + ' /TargetPassword:' + self.TargetPasswordEntry.get()
            self.CmpExeScriptQuery += ' /TargetUser:' + self.TargetUsernameEntry.get() + ' /TargetPassword:' + self.TargetPasswordEntry.get()

        if self.EncryptSrcVariable.get() is True:
            self.CmpExeExtractQuery += ' /SourceEncryptConnection:True '

        if self.EncryptTrgtVariable.get() is True:
            self.CmpExePreDeploymentQuery += ' -N '
            self.CmpExePublishQuery += ' /TargetEncryptConnection:True'
            self.CmpExeScriptQuery += ' /TargetEncryptConnection:True'

        self.CmpExePreDeploymentQuery += ' -d master -Q " ' + self.PreDeploymentText.get(1.0, END) + ' "'
        print("self.CmpExePreDeploymentQuery=", self.CmpExePreDeploymentQuery)

        self.CmpExeExtractQuery += ' /TargetFile:CompareDeploy\\temp\\' + self.SourceDatabaseEntry.get() + '.dacpac'
        print("self.CmpExeExtractQuery=", self.CmpExeExtractQuery)

        print("self.CmpExeScriptQuery", self.CmpExeScriptQuery)

        # self.CmpExePublishQuery += ' /p:ExcludeObjectTypes=RoleMembership;Users /p:ScriptDatabaseOptions=False'

        if self.ChkButtonAllowDropBlockingAssemblies.get() is True and self.ValueAllowDropBlockingAssemblies.get() == "True":
            self.CmpExePublishQuery += ' /p:AllowDropBlockingAssemblies=True '

        if self.ChkButtonAllowIncompatiblePlatform.get() is True and self.ValueAllowIncompatiblePlatform.get() == "True":
            self.CmpExePublishQuery += ' /p:AllowIncompatiblePlatform=True '

        if self.ChkButtonBackupDatabaseBeforeChanges.get() is True and self.ValueBackupDatabaseBeforeChanges.get() == "True":
            self.CmpExePublishQuery += ' /p:BackupDatabaseBeforeChanges=True '

        if self.ChkButtonBlockOnPossibleDataLoss.get() is True and self.ValueBlockOnPossibleDataLoss.get() == "False":
            self.CmpExePublishQuery += ' /p:BlockOnPossibleDataLoss=False '

        if self.ChkButtonBlockWhenDriftDetected.get() is True and self.ValueBlockWhenDriftDetected.get() == "False":
            self.CmpExePublishQuery += ' /p:BlockWhenDriftDetected=False '

        if self.ChkButtonCommandTimeout.get() is True and self.EntryCommandTimeout.get() != "60":
            self.CmpExePublishQuery += ' /p:CommandTimeout=' + self.EntryCommandTimeout.get() + ' '

        if self.ChkButtonCommentOutSetVarDeclarations.get() is True and self.ValueCommentOutSetVarDeclarations.get() == "True":
            self.CmpExePublishQuery += ' /p:CommentOutSetVarDeclarations=True '

        if self.ChkButtonCompareUsingTargetCollation.get() is True and self.ValueCompareUsingTargetCollation.get() == "True":
            self.CmpExePublishQuery += ' /p:CompareUsingTargetCollation=True '

        if self.ChkButtonCreateNewDatabase.get() is True and self.ValueCreateNewDatabase.get() == "True":
            self.CmpExePublishQuery += ' /p:CreateNewDatabase=True '

        if self.ChkButtonDeployDatabaseInSingleUserMode.get() is True and self.ValueDeployDatabaseInSingleUserMode.get() == "True":
            self.CmpExePublishQuery += ' /p:DeployDatabaseInSingleUserMode=True '

        if self.ChkButtonDisableAndReenableDdlTriggers.get() is True and self.ValueDisableAndReenableDdlTriggers.get() == "False":
            self.CmpExePublishQuery += ' /p:DisableAndReenableDdlTriggers=False '

        if self.ChkButtonDoNotAlterChangeDataCaptureObjects.get() is True and self.ValueDoNotAlterChangeDataCaptureObjects.get() == "False":
            self.CmpExePublishQuery += ' /p:DoNotAlterChangeDataCaptureObjects=False '

        if self.ChkButtonDoNotAlterReplicatedObjects.get() is True and self.ValueDoNotAlterReplicatedObjects.get() == "False":
            self.CmpExePublishQuery += ' /p:DoNotAlterReplicatedObjects=False '

        if self.ChkButtonDoNotDropObjectTypes.get() is True:
            self.CmpExePublishQuery += ' /p:DoNotDropObjectTypes='
            if self.DoNotDropObjectTypesAggregates.get() is True:
                self.CmpExePublishQuery += 'Aggregates;'
            if self.DoNotDropObjectTypesApplicationRoles.get() is True:
                self.CmpExePublishQuery += 'ApplicationRoles;'

            if self.DoNotDropObjectTypesAssemblies.get() is True:
                self.CmpExePublishQuery += 'Assemblies;'

            if self.DoNotDropObjectTypesAsymmetricKeys.get() is True:
                self.CmpExePublishQuery += 'AsymmetricKeys;'

            if self.DoNotDropObjectTypesBrokerPriorities.get() is True:
                self.CmpExePublishQuery += 'BrokerPriorities;'

            if self.DoNotDropObjectTypesCertificates.get() is True:
                self.CmpExePublishQuery += 'Certificates;'

            if self.DoNotDropObjectTypesContracts.get() is True:
                self.CmpExePublishQuery += 'Contracts;'

            if self.DoNotDropObjectTypesDatabaseRoles.get() is True:
                self.CmpExePublishQuery += 'DatabaseRoles;'

            if self.DoNotDropObjectTypesDatabaseTriggers.get() is True:
                self.CmpExePublishQuery += 'DatabaseTriggers;'

            if self.DoNotDropObjectTypesDefaults.get() is True:
                self.CmpExePublishQuery += 'Defaults;'

            if self.DoNotDropObjectTypesExtendedProperties.get() is True:
                self.CmpExePublishQuery += 'ExtendedProperties;'

            if self.DoNotDropObjectTypesFilegroups.get() is True:
                self.CmpExePublishQuery += 'Filegroups;'

            if self.DoNotDropObjectTypesFileTables.get() is True:
                self.CmpExePublishQuery += 'FileTables;'

            if self.DoNotDropObjectTypesFullTextCatalogs.get() is True:
                self.CmpExePublishQuery += 'FullTextCatalogs;'

            if self.DoNotDropObjectTypesFullTextStoplists.get() is True:
                self.CmpExePublishQuery += 'FullTextStoplists;'

            if self.DoNotDropObjectTypesMessageTypes.get() is True:
                self.CmpExePublishQuery += 'MessageTypes;'

            if self.DoNotDropObjectTypesPartitionFunctions.get() is True:
                self.CmpExePublishQuery += 'PartitionFunctions;'

            if self.DoNotDropObjectTypesPartitionSchemes.get() is True:
                self.CmpExePublishQuery += 'PartitionSchemes;'

            if self.DoNotDropObjectTypesPermissions.get() is True:
                self.CmpExePublishQuery += 'Permissions;'

            if self.DoNotDropObjectTypesQueues.get() is True:
                self.CmpExePublishQuery += 'Queues;'

            if self.DoNotDropObjectTypesRemoteServiceBindings.get() is True:
                self.CmpExePublishQuery += 'RemoteServiceBindings;'

            if self.DoNotDropObjectTypesRoleMembership.get() is True:
                self.CmpExePublishQuery += 'RoleMembership;'

            if self.DoNotDropObjectTypesRules.get() is True:
                self.CmpExePublishQuery += 'Rules;'

            if self.DoNotDropObjectTypesScalarValuedFunctions.get() is True:
                self.CmpExePublishQuery += 'ScalarValuedFunctions;'

            if self.DoNotDropObjectTypesSearchPropertyLists.get() is True:
                self.CmpExePublishQuery += 'SearchPropertyLists;'

            if self.DoNotDropObjectTypesSequences.get() is True:
                self.CmpExePublishQuery += 'Sequences;'

            if self.DoNotDropObjectTypesServices.get() is True:
                self.CmpExePublishQuery += 'Services;'

            if self.DoNotDropObjectTypesSignatures.get() is True:
                self.CmpExePublishQuery += 'Signatures;'

            if self.DoNotDropObjectTypesStoredProcedures.get() is True:
                self.CmpExePublishQuery += 'StoredProcedures;'

            if self.DoNotDropObjectTypesSymmetricKeys.get() is True:
                self.CmpExePublishQuery += 'SymmetricKeys;'

            if self.DoNotDropObjectTypesSynonyms.get() is True:
                self.CmpExePublishQuery += 'Synonyms;'

            if self.DoNotDropObjectTypesTables.get() is True:
                self.CmpExePublishQuery += 'Tables;'

            if self.DoNotDropObjectTypesTableValuedFunctions.get() is True:
                self.CmpExePublishQuery += 'TableValuedFunctions;'

            if self.DoNotDropObjectTypesUserDefinedDataTypes.get() is True:
                self.CmpExePublishQuery += 'UserDefinedDataTypes;'

            if self.DoNotDropObjectTypesUserDefinedTableTypes.get() is True:
                self.CmpExePublishQuery += 'UserDefinedTableTypes;'

            if self.DoNotDropObjectTypesClrUserDefinedTypes.get() is True:
                self.CmpExePublishQuery += 'ClrUserDefinedTypes;'

            if self.DoNotDropObjectTypesUsers.get() is True:
                self.CmpExePublishQuery += 'Users;'

            if self.DoNotDropObjectTypesViews.get() is True:
                self.CmpExePublishQuery += 'Views;'

            if self.DoNotDropObjectTypesXmlSchemaCollections.get() is True:
                self.CmpExePublishQuery += 'XmlSchemaCollections;'

            if self.DoNotDropObjectTypesAudits.get() is True:
                self.CmpExePublishQuery += 'Audits;'

            if self.DoNotDropObjectTypesCredentials.get() is True:
                self.CmpExePublishQuery += 'Credentials;'

            if self.DoNotDropObjectTypesCryptographicProviders.get() is True:
                self.CmpExePublishQuery += 'CryptographicProviders;'

            if self.DoNotDropObjectTypesDatabaseAuditSpecifications.get() is True:
                self.CmpExePublishQuery += 'DatabaseAuditSpecifications;'

            if self.DoNotDropObjectTypesEndpoints.get() is True:
                self.CmpExePublishQuery += 'Endpoints;'

            if self.DoNotDropObjectTypesErrorMessages.get() is True:
                self.CmpExePublishQuery += 'ErrorMessages;'

            if self.DoNotDropObjectTypesEventNotifications.get() is True:
                self.CmpExePublishQuery += 'EventNotifications;'

            if self.DoNotDropObjectTypesEventSessions.get() is True:
                self.CmpExePublishQuery += 'EventSessions;'

            if self.DoNotDropObjectTypesLinkedServerLogins.get() is True:
                self.CmpExePublishQuery += 'LinkedServerLogins;'

            if self.DoNotDropObjectTypesLinkedServers.get() is True:
                self.CmpExePublishQuery += 'LinkedServers;'

            if self.DoNotDropObjectTypesLogins.get() is True:
                self.CmpExePublishQuery += 'Logins;'

            if self.DoNotDropObjectTypesRoutes.get() is True:
                self.CmpExePublishQuery += 'Routes;'

            if self.DoNotDropObjectTypesServerAuditSpecifications.get() is True:
                self.CmpExePublishQuery += 'ServerAuditSpecifications;'

            if self.DoNotDropObjectTypesServerRoleMembership.get() is True:
                self.CmpExePublishQuery += 'ServerRoleMembership;'

            if self.DoNotDropObjectTypesServerRoles.get() is True:
                self.CmpExePublishQuery += 'ServerRoles;'

            if self.DoNotDropObjectTypesServerTriggers.get() is True:
                self.CmpExePublishQuery += 'ServerTriggers;'

        if self.ChkButtonDropConstraintsNotInSource.get() is True and self.ValueDropConstraintsNotInSource.get() == "False":
            self.CmpExePublishQuery += ' /p:DropConstraintsNotInSource=False '
        if self.ChkButtonDropDmlTriggersNotInSource.get() is True and self.ValueDropDmlTriggersNotInSource.get() == "False":
            self.CmpExePublishQuery += ' /p:DropDmlTriggersNotInSource=False '
        if self.ChkButtonDropExtendedPropertiesNotInSource.get() is True and self.ValueDropExtendedPropertiesNotInSource.get() == "False":
            self.CmpExePublishQuery += ' /p:DropExtendedPropertiesNotInSource=False '
        if self.ChkButtonDropIndexesNotInSource.get() is True and self.ValueDropIndexesNotInSource.get() == "False":
            self.CmpExePublishQuery += ' /p:DropIndexesNotInSource=False '
        if self.ChkButtonDropObjectsNotInSource.get() is True and self.ValueDropObjectsNotInSource.get() == "True":
            self.CmpExePublishQuery += ' /p:DropObjectsNotInSource=True '
        if self.ChkButtonDropPermissionsNotInSource.get() is True and self.ValueDropPermissionsNotInSource.get() == "True":
            self.CmpExePublishQuery += ' /p:DropPermissionsNotInSource=True '
        if self.ChkButtonDropRoleMembersNotInSource.get() is True and self.ValueDropRoleMembersNotInSource.get() == "True":
            self.CmpExePublishQuery += ' /p:DropRoleMembersNotInSource=True '

        if self.ChkButtonExcludeObjectTypes.get() is True:
            self.CmpExePublishQuery += ' /p:ExcludeObjectTypes='
            if self.ExcludeObjectTypesAggregates.get() is True:
                self.CmpExePublishQuery += 'Aggregates;'
            if self.ExcludeObjectTypesApplicationRoles.get() is True:
                self.CmpExePublishQuery += 'ApplicationRoles;'

            if self.ExcludeObjectTypesAssemblies.get() is True:
                self.CmpExePublishQuery += 'Assemblies;'

            if self.ExcludeObjectTypesAsymmetricKeys.get() is True:
                self.CmpExePublishQuery += 'AsymmetricKeys;'

            if self.ExcludeObjectTypesBrokerPriorities.get() is True:
                self.CmpExePublishQuery += 'BrokerPriorities;'

            if self.ExcludeObjectTypesCertificates.get() is True:
                self.CmpExePublishQuery += 'Certificates;'

            if self.ExcludeObjectTypesContracts.get() is True:
                self.CmpExePublishQuery += 'Contracts;'

            if self.ExcludeObjectTypesDatabaseRoles.get() is True:
                self.CmpExePublishQuery += 'DatabaseRoles;'

            if self.ExcludeObjectTypesDatabaseTriggers.get() is True:
                self.CmpExePublishQuery += 'DatabaseTriggers;'

            if self.ExcludeObjectTypesDefaults.get() is True:
                self.CmpExePublishQuery += 'Defaults;'

            if self.ExcludeObjectTypesExtendedProperties.get() is True:
                self.CmpExePublishQuery += 'ExtendedProperties;'

            if self.ExcludeObjectTypesFilegroups.get() is True:
                self.CmpExePublishQuery += 'Filegroups;'

            if self.ExcludeObjectTypesFileTables.get() is True:
                self.CmpExePublishQuery += 'FileTables;'

            if self.ExcludeObjectTypesFullTextCatalogs.get() is True:
                self.CmpExePublishQuery += 'FullTextCatalogs;'

            if self.ExcludeObjectTypesFullTextStoplists.get() is True:
                self.CmpExePublishQuery += 'FullTextStoplists;'

            if self.ExcludeObjectTypesMessageTypes.get() is True:
                self.CmpExePublishQuery += 'MessageTypes;'

            if self.ExcludeObjectTypesPartitionFunctions.get() is True:
                self.CmpExePublishQuery += 'PartitionFunctions;'

            if self.ExcludeObjectTypesPartitionSchemes.get() is True:
                self.CmpExePublishQuery += 'PartitionSchemes;'

            if self.ExcludeObjectTypesPermissions.get() is True:
                self.CmpExePublishQuery += 'Permissions;'

            if self.ExcludeObjectTypesQueues.get() is True:
                self.CmpExePublishQuery += 'Queues;'

            if self.ExcludeObjectTypesRemoteServiceBindings.get() is True:
                self.CmpExePublishQuery += 'RemoteServiceBindings;'

            if self.ExcludeObjectTypesRoleMembership.get() is True:
                self.CmpExePublishQuery += 'RoleMembership;'

            if self.ExcludeObjectTypesRules.get() is True:
                self.CmpExePublishQuery += 'Rules;'

            if self.ExcludeObjectTypesScalarValuedFunctions.get() is True:
                self.CmpExePublishQuery += 'ScalarValuedFunctions;'

            if self.ExcludeObjectTypesSearchPropertyLists.get() is True:
                self.CmpExePublishQuery += 'SearchPropertyLists;'

            if self.ExcludeObjectTypesSequences.get() is True:
                self.CmpExePublishQuery += 'Sequences;'

            if self.ExcludeObjectTypesServices.get() is True:
                self.CmpExePublishQuery += 'Services;'

            if self.ExcludeObjectTypesSignatures.get() is True:
                self.CmpExePublishQuery += 'Signatures;'

            if self.ExcludeObjectTypesStoredProcedures.get() is True:
                self.CmpExePublishQuery += 'StoredProcedures;'

            if self.ExcludeObjectTypesSymmetricKeys.get() is True:
                self.CmpExePublishQuery += 'SymmetricKeys;'

            if self.ExcludeObjectTypesSynonyms.get() is True:
                self.CmpExePublishQuery += 'Synonyms;'

            if self.ExcludeObjectTypesTables.get() is True:
                self.CmpExePublishQuery += 'Tables;'

            if self.ExcludeObjectTypesTableValuedFunctions.get() is True:
                self.CmpExePublishQuery += 'TableValuedFunctions;'

            if self.ExcludeObjectTypesUserDefinedDataTypes.get() is True:
                self.CmpExePublishQuery += 'UserDefinedDataTypes;'

            if self.ExcludeObjectTypesUserDefinedTableTypes.get() is True:
                self.CmpExePublishQuery += 'UserDefinedTableTypes;'

            if self.ExcludeObjectTypesClrUserDefinedTypes.get() is True:
                self.CmpExePublishQuery += 'ClrUserDefinedTypes;'

            if self.ExcludeObjectTypesUsers.get() is True:
                self.CmpExePublishQuery += 'Users;'

            if self.ExcludeObjectTypesViews.get() is True:
                self.CmpExePublishQuery += 'Views;'

            if self.ExcludeObjectTypesXmlSchemaCollections.get() is True:
                self.CmpExePublishQuery += 'XmlSchemaCollections;'

            if self.ExcludeObjectTypesAudits.get() is True:
                self.CmpExePublishQuery += 'Audits;'

            if self.ExcludeObjectTypesCredentials.get() is True:
                self.CmpExePublishQuery += 'Credentials;'

            if self.ExcludeObjectTypesCryptographicProviders.get() is True:
                self.CmpExePublishQuery += 'CryptographicProviders;'

            if self.ExcludeObjectTypesDatabaseAuditSpecifications.get() is True:
                self.CmpExePublishQuery += 'DatabaseAuditSpecifications;'

            if self.ExcludeObjectTypesEndpoints.get() is True:
                self.CmpExePublishQuery += 'Endpoints;'

            if self.ExcludeObjectTypesErrorMessages.get() is True:
                self.CmpExePublishQuery += 'ErrorMessages;'

            if self.ExcludeObjectTypesEventNotifications.get() is True:
                self.CmpExePublishQuery += 'EventNotifications;'

            if self.ExcludeObjectTypesEventSessions.get() is True:
                self.CmpExePublishQuery += 'EventSessions;'

            if self.ExcludeObjectTypesLinkedServerLogins.get() is True:
                self.CmpExePublishQuery += 'LinkedServerLogins;'

            if self.ExcludeObjectTypesLinkedServers.get() is True:
                self.CmpExePublishQuery += 'LinkedServers;'

            if self.ExcludeObjectTypesLogins.get() is True:
                self.CmpExePublishQuery += 'Logins;'

            if self.ExcludeObjectTypesRoutes.get() is True:
                self.CmpExePublishQuery += 'Routes;'

            if self.ExcludeObjectTypesServerAuditSpecifications.get() is True:
                self.CmpExePublishQuery += 'ServerAuditSpecifications;'

            if self.ExcludeObjectTypesServerRoleMembership.get() is True:
                self.CmpExePublishQuery += 'ServerRoleMembership;'

            if self.ExcludeObjectTypesServerRoles.get() is True:
                self.CmpExePublishQuery += 'ServerRoles;'

            if self.ExcludeObjectTypesServerTriggers.get() is True:
                self.CmpExePublishQuery += 'ServerTriggers;'

        if self.ChkButtonGenerateSmartDefaults.get() is True and self.ValueGenerateSmartDefaults.get() == "True":
            self.CmpExePublishQuery += ' /p:GenerateSmartDefaults=True '
        if self.ChkButtonIgnoreAnsiNulls.get() is True and self.ValueIgnoreAnsiNulls.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreAnsiNulls=True '
        if self.ChkButtonIgnoreAuthorizer.get() is True and self.ValueIgnoreAuthorizer.get() == "True":
            self.CmpExePublishQuery += ' /p: IgnoreAuthorizer=True '
        if self.ChkButtonIgnoreColumnCollation.get() is True and self.ValueIgnoreColumnCollation.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreColumnCollation=True '
        if self.ChkButtonIgnoreComments.get() is True and self.ValueIgnoreComments.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreComments=True '
        if self.ChkButtonIgnoreCryptographicProviderFilePath.get() is True and self.ValueIgnoreCryptographicProviderFilePath.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreCryptographicProviderFilePath=False '
        if self.ChkButtonIgnoreDdlTriggerOrder.get() is True and self.ValueIgnoreDdlTriggerOrder.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreDdlTriggerOrder=True '
        if self.ChkButtonIgnoreDdlTriggerState.get() is True and self.ValueIgnoreDdlTriggerState.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreDdlTriggerState=True '
        if self.ChkButtonIgnoreDefaultSchema.get() is True and self.ValueIgnoreDefaultSchema.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreDefaultSchema=True '
        if self.ChkButtonIgnoreDmlTriggerOrder.get() is True and self.ValueIgnoreDmlTriggerOrder.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreDmlTriggerOrder=True '
        if self.ChkButtonIgnoreDmlTriggerState.get() is True and self.ValueIgnoreDmlTriggerState.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreDmlTriggerState=True '
        if self.ChkButtonIgnoreExtendedProperties.get() is True and self.ValueIgnoreExtendedProperties.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreExtendedProperties=True '
        if self.ChkButtonIgnoreFileAndLogFilePath.get() is True and self.ValueIgnoreFileAndLogFilePath.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreFileAndLogFilePath=False '
        if self.ChkButtonIgnoreFilegroupPlacement.get() is True and self.ValueIgnoreFilegroupPlacement.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreFilegroupPlacement=False '
        if self.ChkButtonIgnoreFileSize.get() is True and self.ValueIgnoreFileSize.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreFileSize=False '
        if self.ChkButtonIgnoreFillFactor.get() is True and self.ValueIgnoreFillFactor.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreFillFactor=False '
        if self.ChkButtonIgnoreFullTextCatalogFilePath.get() is True and self.ValueIgnoreFullTextCatalogFilePath.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreFullTextCatalogFilePath=False '
        if self.ChkButtonIgnoreIdentitySeed.get() is True and self.ValueIgnoreIdentitySeed.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreIdentitySeed=True '
        if self.ChkButtonIgnoreIncrement.get() is True and self.ValueIgnoreIncrement.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreIncrement=True '
        if self.ChkButtonIgnoreIndexOptions.get() is True and self.ValueIgnoreIndexOptions.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreIndexOptions=True '
        if self.ChkButtonIgnoreIndexPadding.get() is True and self.ValueIgnoreIndexPadding.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreIndexPadding=False '
        if self.ChkButtonIgnoreKeywordCasing.get() is True and self.ValueIgnoreKeywordCasing.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreKeywordCasing=False '
        if self.ChkButtonIgnoreLockHintsOnIndexes.get() is True and self.ValueIgnoreLockHintsOnIndexes.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreLockHintsOnIndexes=True '
        if self.ChkButtonIgnoreLoginSids.get() is True and self.ValueIgnoreLoginSids.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreLoginSids=False '
        if self.ChkButtonIgnoreNotForReplication.get() is True and self.ValueIgnoreNotForReplication.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreNotForReplication=True '
        if self.ChkButtonIgnoreObjectPlacementOnPartitionScheme.get() is True and self.ValueIgnoreObjectPlacementOnPartitionScheme.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreObjectPlacementOnPartitionScheme=False '
        if self.ChkButtonIgnorePartitionSchemes.get() is True and self.ValueIgnorePartitionSchemes.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnorePartitionSchemes=True '
        if self.ChkButtonIgnorePermissions.get() is True and self.ValueIgnorePermissions.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnorePermissions=True '
        if self.ChkButtonIgnoreQuotedIdentifiers.get() is True and self.ValueIgnoreQuotedIdentifiers.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreQuotedIdentifiers=True '
        if self.ChkButtonIgnoreRoleMembership.get() is True and self.ValueIgnoreRoleMembership.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreRoleMembership=True '
        if self.ChkButtonIgnoreRouteLifetime.get() is True and self.ValueIgnoreRouteLifetime.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreRouteLifetime=False '
        if self.ChkButtonIgnoreSemicolonBetweenStatements.get() is True and self.ValueIgnoreSemicolonBetweenStatements.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreSemicolonBetweenStatements=False '
        if self.ChkButtonIgnoreTableOptions.get() is True and self.ValueIgnoreTableOptions.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreTableOptions=True '
        if self.ChkButtonIgnoreUserSettingsObjects.get() is True and self.ValueIgnoreUserSettingsObjects.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreUserSettingsObjects=True '
        if self.ChkButtonIgnoreWhitespace.get() is True and self.ValueIgnoreWhitespace.get() == "False":
            self.CmpExePublishQuery += ' /p:IgnoreWhitespace=False '
        if self.ChkButtonIgnoreWithNocheckOnCheckConstraints.get() is True and self.ValueIgnoreWithNocheckOnCheckConstraints.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreWithNocheckOnCheckConstraints=True '
        if self.ChkButtonIgnoreWithNocheckOnForeignKeys.get() is True and self.ValueIgnoreWithNocheckOnForeignKeys.get() == "True":
            self.CmpExePublishQuery += ' /p:IgnoreWithNocheckOnForeignKeys=True '
        if self.ChkButtonIncludeCompositeObjects.get() is True and self.ValueIncludeCompositeObjects.get() == "True":
            self.CmpExePublishQuery += ' /p:IncludeCompositeObjects=True '
        if self.ChkButtonIncludeTransactionalScripts.get() is True and self.ValueIncludeTransactionalScripts.get() == "True":
            self.CmpExePublishQuery += ' /p:IncludeTransactionalScripts=True '
        if self.ChkButtonNoAlterStatementsToChangeClrTypes.get() is True and self.ValueNoAlterStatementsToChangeClrTypes.get() == "True":
            self.CmpExePublishQuery += ' /p:NoAlterStatementsToChangeClrTypes=True '
        if self.ChkButtonPopulateFilesOnFilegroups.get() is True and self.ValuePopulateFilesOnFilegroups.get() == "False":
            self.CmpExePublishQuery += ' /p:PopulateFilesOnFilegroups=False '
        if self.ChkButtonRegisterDataTierApplication.get() is True and self.ValueRegisterDataTierApplication.get() == "True":
            self.CmpExePublishQuery += ' /p:RegisterDataTierApplication=True '
        if self.ChkButtonRunDeploymentPlanExecutors.get() is True and self.ValueRunDeploymentPlanExecutors.get() == "True":
            self.CmpExePublishQuery += ' /p:RunDeploymentPlanExecutors=True '
        if self.ChkButtonScriptDatabaseCollation.get() is True and self.ValueScriptDatabaseCollation.get() == "True":
            self.CmpExePublishQuery += ' /p:ScriptDatabaseCollation=True '
        if self.ChkButtonScriptDatabaseCompatibility.get() is True and self.ValueScriptDatabaseCompatibility.get() == "False":
            self.CmpExePublishQuery += ' /p:ScriptDatabaseCompatibility=False '
        if self.ChkButtonScriptDatabaseOptions.get() is True and self.ValueScriptDatabaseOptions.get() == "False":
            self.CmpExePublishQuery += ' /p:ScriptDatabaseOptions=False '
        if self.ChkButtonScriptDeployStateChecks.get() is True and self.ValueScriptDeployStateChecks.get() == "True":
            self.CmpExePublishQuery += ' /p:ScriptDeployStateChecks=True '
        if self.ChkButtonScriptFileSize.get() is True and self.ValueScriptFileSize.get() == "True":
            self.CmpExePublishQuery += ' /p:ScriptFileSize=True '
        if self.ChkButtonScriptNewConstraintValidation.get() is True and self.ValueScriptNewConstraintValidation.get() == "False":
            self.CmpExePublishQuery += ' /p:ScriptNewConstraintValidation=False '
        if self.ChkButtonScriptRefreshModule.get() is True and self.ValueScriptRefreshModule.get() == "False":
            self.CmpExePublishQuery += ' /p:ScriptRefreshModule=False '
        if self.ChkButtonStorage.get() is True and self.ValueStorage.get() == "File":
            self.CmpExePublishQuery += ' /p:Storage=File '
        if self.ChkButtonTreatVerificationErrorsAsWarnings.get() is True and self.ValueTreatVerificationErrorsAsWarnings.get() == "True":
            self.CmpExePublishQuery += ' /p:TreatVerificationErrorsAsWarnings=True '
        if self.ChkButtonUnmodifiableObjectWarnings.get() is True and self.ValueUnmodifiableObjectWarnings.get() == "False":
            self.CmpExePublishQuery += ' /p:UnmodifiableObjectWarnings=False '
        if self.ChkButtonVerifyCollationCompatibility.get() is True and self.ValueVerifyCollationCompatibility.get() == "False":
            self.CmpExePublishQuery += ' /p:VerifyCollationCompatibility=False '
        if self.ChkButtonVerifyDeployment.get() is True and self.ValueVerifyDeployment.get() == "False":
            self.CmpExePublishQuery += ' /p:VerifyDeployment=False '

        print("self.CmpExePublishQuery=", self.CmpExePublishQuery)

    def save_profile(self):
        self.save_profile_data = {
            'self.PreDeploymentText': self.PreDeploymentText.get(1.0, END),
            'self.SourceServerEntry': self.SourceServerEntry.get(),
            'self.SourceDatabaseEntry': self.SourceDatabaseEntry.get(),
            'self.TargetServerEntry': self.TargetServerEntry.get(),
            'self.TargetDatabaseEntry': self.TargetDatabaseEntry.get(),
            'self.SourceUsernameEntry': self.SourceUsernameEntry.get(),
            'self.SourcePasswordEntry': self.SourcePasswordEntry.get(),
            'self.TargetUsernameEntry': self.TargetUsernameEntry.get(),
            'self.TargetPasswordEntry': self.TargetPasswordEntry.get(),
            'self.WinAuthSrcVariable': self.WinAuthSrcVariable.get(),
            'self.WinAuthTrgtVariable': self.WinAuthTrgtVariable.get(),
            'self.EncryptSrcVariable': self.EncryptSrcVariable.get(),
            'self.EncryptTrgtVariable': self.EncryptTrgtVariable.get(),
            'self.SetDplyPropertyVariable': self.SetDplyPropertyVariable.get(),

            'self.ChkButtonAllowDropBlockingAssemblies': self.ChkButtonAllowDropBlockingAssemblies.get(),
            'self.ChkButtonAllowIncompatiblePlatform': self.ChkButtonAllowIncompatiblePlatform.get(),
            'self.ChkButtonBackupDatabaseBeforeChanges': self.ChkButtonBackupDatabaseBeforeChanges.get(),
            'self.ChkButtonBlockOnPossibleDataLoss': self.ChkButtonBlockOnPossibleDataLoss.get(),
            'self.ChkButtonBlockWhenDriftDetected': self.ChkButtonBlockWhenDriftDetected.get(),
            'self.ChkButtonCommandTimeout': self.ChkButtonCommandTimeout.get(),
            'self.ChkButtonCommentOutSetVarDeclarations': self.ChkButtonCommentOutSetVarDeclarations.get(),
            'self.ChkButtonCompareUsingTargetCollation': self.ChkButtonCompareUsingTargetCollation.get(),
            'self.ChkButtonCreateNewDatabase': self.ChkButtonCreateNewDatabase.get(),
            'self.ChkButtonDeployDatabaseInSingleUserMode': self.ChkButtonDeployDatabaseInSingleUserMode.get(),
            'self.ChkButtonDisableAndReenableDdlTriggers': self.ChkButtonDisableAndReenableDdlTriggers.get(),
            'self.ChkButtonDoNotAlterChangeDataCaptureObjects': self.ChkButtonDoNotAlterChangeDataCaptureObjects.get(),
            'self.ChkButtonDoNotAlterReplicatedObjects': self.ChkButtonDoNotAlterReplicatedObjects.get(),
            'self.ChkButtonDoNotDropObjectTypes': self.ChkButtonDoNotDropObjectTypes.get(),
            'self.ChkButtonDropConstraintsNotInSource': self.ChkButtonDropConstraintsNotInSource.get(),
            'self.ChkButtonDropDmlTriggersNotInSource': self.ChkButtonDropDmlTriggersNotInSource.get(),
            'self.ChkButtonDropExtendedPropertiesNotInSource': self.ChkButtonDropExtendedPropertiesNotInSource.get(),
            'self.ChkButtonDropIndexesNotInSource': self.ChkButtonDropIndexesNotInSource.get(),
            'self.ChkButtonDropObjectsNotInSource': self.ChkButtonDropObjectsNotInSource.get(),
            'self.ChkButtonDropPermissionsNotInSource': self.ChkButtonDropPermissionsNotInSource.get(),
            'self.ChkButtonDropRoleMembersNotInSource': self.ChkButtonDropRoleMembersNotInSource.get(),
            'self.ChkButtonExcludeObjectTypes': self.ChkButtonExcludeObjectTypes.get(),
            'self.ChkButtonGenerateSmartDefaults': self.ChkButtonGenerateSmartDefaults.get(),
            'self.ChkButtonIgnoreAnsiNulls': self.ChkButtonIgnoreAnsiNulls.get(),
            'self.ChkButtonIgnoreAuthorizer': self.ChkButtonIgnoreAuthorizer.get(),
            'self.ChkButtonIgnoreColumnCollation': self.ChkButtonIgnoreColumnCollation.get(),
            'self.ChkButtonIgnoreComments': self.ChkButtonIgnoreComments.get(),
            'self.ChkButtonIgnoreCryptographicProviderFilePath': self.ChkButtonIgnoreCryptographicProviderFilePath.get(),
            'self.ChkButtonIgnoreDdlTriggerOrder': self.ChkButtonIgnoreDdlTriggerOrder.get(),
            'self.ChkButtonIgnoreDdlTriggerState': self.ChkButtonIgnoreDdlTriggerState.get(),
            'self.ChkButtonIgnoreDefaultSchema': self.ChkButtonIgnoreDefaultSchema.get(),
            'self.ChkButtonIgnoreDmlTriggerOrder': self.ChkButtonIgnoreDmlTriggerOrder.get(),
            'self.ChkButtonIgnoreDmlTriggerState': self.ChkButtonIgnoreDmlTriggerState.get(),
            'self.ChkButtonIgnoreExtendedProperties': self.ChkButtonIgnoreExtendedProperties.get(),
            'self.ChkButtonIgnoreFileAndLogFilePath': self.ChkButtonIgnoreFileAndLogFilePath.get(),
            'self.ChkButtonIgnoreFilegroupPlacement': self.ChkButtonIgnoreFilegroupPlacement.get(),
            'self.ChkButtonIgnoreFileSize': self.ChkButtonIgnoreFileSize.get(),
            'self.ChkButtonIgnoreFillFactor': self.ChkButtonIgnoreFillFactor.get(),
            'self.ChkButtonIgnoreFullTextCatalogFilePath': self.ChkButtonIgnoreFullTextCatalogFilePath.get(),
            'self.ChkButtonIgnoreIdentitySeed': self.ChkButtonIgnoreIdentitySeed.get(),
            'self.ChkButtonIgnoreIncrement': self.ChkButtonIgnoreIncrement.get(),
            'self.ChkButtonIgnoreIndexOptions': self.ChkButtonIgnoreIndexOptions.get(),
            'self.ChkButtonIgnoreIndexPadding': self.ChkButtonIgnoreIndexPadding.get(),
            'self.ChkButtonIgnoreKeywordCasing': self.ChkButtonIgnoreKeywordCasing.get(),
            'self.ChkButtonIgnoreLockHintsOnIndexes': self.ChkButtonIgnoreLockHintsOnIndexes.get(),
            'self.ChkButtonIgnoreLoginSids': self.ChkButtonIgnoreLoginSids.get(),
            'self.ChkButtonIgnoreNotForReplication': self.ChkButtonIgnoreNotForReplication.get(),
            'self.ChkButtonIgnoreObjectPlacementOnPartitionScheme': self.ChkButtonIgnoreObjectPlacementOnPartitionScheme.get(),
            'self.ChkButtonIgnorePartitionSchemes': self.ChkButtonIgnorePartitionSchemes.get(),
            'self.ChkButtonIgnorePermissions': self.ChkButtonIgnorePermissions.get(),
            'self.ChkButtonIgnoreQuotedIdentifiers': self.ChkButtonIgnoreQuotedIdentifiers.get(),
            'self.ChkButtonIgnoreRoleMembership': self.ChkButtonIgnoreRoleMembership.get(),
            'self.ChkButtonIgnoreRouteLifetime': self.ChkButtonIgnoreRouteLifetime.get(),
            'self.ChkButtonIgnoreSemicolonBetweenStatements': self.ChkButtonIgnoreSemicolonBetweenStatements.get(),
            'self.ChkButtonIgnoreTableOptions': self.ChkButtonIgnoreTableOptions.get(),
            'self.ChkButtonIgnoreUserSettingsObjects': self.ChkButtonIgnoreUserSettingsObjects.get(),
            'self.ChkButtonIgnoreWhitespace': self.ChkButtonIgnoreWhitespace.get(),
            'self.ChkButtonIgnoreWithNocheckOnCheckConstraints': self.ChkButtonIgnoreWithNocheckOnCheckConstraints.get(),
            'self.ChkButtonIgnoreWithNocheckOnForeignKeys': self.ChkButtonIgnoreWithNocheckOnForeignKeys.get(),
            'self.ChkButtonIncludeCompositeObjects': self.ChkButtonIncludeCompositeObjects.get(),
            'self.ChkButtonIncludeTransactionalScripts': self.ChkButtonIncludeTransactionalScripts.get(),
            'self.ChkButtonNoAlterStatementsToChangeClrTypes': self.ChkButtonNoAlterStatementsToChangeClrTypes.get(),
            'self.ChkButtonPopulateFilesOnFilegroups': self.ChkButtonPopulateFilesOnFilegroups.get(),
            'self.ChkButtonRegisterDataTierApplication': self.ChkButtonRegisterDataTierApplication.get(),
            'self.ChkButtonRunDeploymentPlanExecutors': self.ChkButtonRunDeploymentPlanExecutors.get(),
            'self.ChkButtonScriptDatabaseCollation': self.ChkButtonScriptDatabaseCollation.get(),
            'self.ChkButtonScriptDatabaseCompatibility': self.ChkButtonScriptDatabaseCompatibility.get(),
            'self.ChkButtonScriptDatabaseOptions': self.ChkButtonScriptDatabaseOptions.get(),
            'self.ChkButtonScriptDeployStateChecks': self.ChkButtonScriptDeployStateChecks.get(),
            'self.ChkButtonScriptFileSize': self.ChkButtonScriptFileSize.get(),
            'self.ChkButtonScriptNewConstraintValidation': self.ChkButtonScriptNewConstraintValidation.get(),
            'self.ChkButtonScriptRefreshModule': self.ChkButtonScriptRefreshModule.get(),
            'self.ChkButtonStorage': self.ChkButtonStorage.get(),
            'self.ChkButtonTreatVerificationErrorsAsWarnings': self.ChkButtonTreatVerificationErrorsAsWarnings.get(),
            'self.ChkButtonUnmodifiableObjectWarnings': self.ChkButtonUnmodifiableObjectWarnings.get(),
            'self.ChkButtonVerifyCollationCompatibility': self.ChkButtonVerifyCollationCompatibility.get(),
            'self.ChkButtonVerifyDeployment': self.ChkButtonVerifyDeployment.get(),

            'self.ValueAllowDropBlockingAssemblies': self.ValueAllowDropBlockingAssemblies.get(),
            'self.ValueAllowIncompatiblePlatform': self.ValueAllowIncompatiblePlatform.get(),
            'self.ValueBackupDatabaseBeforeChanges': self.ValueBackupDatabaseBeforeChanges.get(),
            'self.ValueBlockOnPossibleDataLoss': self.ValueBlockOnPossibleDataLoss.get(),
            'self.ValueBlockWhenDriftDetected': self.ValueBlockWhenDriftDetected.get(),
            'self.ValueCommandTimeout': self.ValueCommandTimeout.get(),
            'self.ValueCommentOutSetVarDeclarations': self.ValueCommentOutSetVarDeclarations.get(),
            'self.ValueCompareUsingTargetCollation': self.ValueCompareUsingTargetCollation.get(),
            'self.ValueCreateNewDatabase': self.ValueCreateNewDatabase.get(),
            'self.ValueDeployDatabaseInSingleUserMode': self.ValueDeployDatabaseInSingleUserMode.get(),
            'self.ValueDisableAndReenableDdlTriggers': self.ValueDisableAndReenableDdlTriggers.get(),
            'self.ValueDoNotAlterChangeDataCaptureObjects': self.ValueDoNotAlterChangeDataCaptureObjects.get(),
            'self.ValueDoNotAlterReplicatedObjects': self.ValueDoNotAlterReplicatedObjects.get(),
            'self.ValueDoNotDropObjectTypes': self.ValueDoNotDropObjectTypes.get(),
            'self.ValueDropConstraintsNotInSource': self.ValueDropConstraintsNotInSource.get(),
            'self.ValueDropDmlTriggersNotInSource': self.ValueDropDmlTriggersNotInSource.get(),
            'self.ValueDropExtendedPropertiesNotInSource': self.ValueDropExtendedPropertiesNotInSource.get(),
            'self.ValueDropIndexesNotInSource': self.ValueDropIndexesNotInSource.get(),
            'self.ValueDropObjectsNotInSource': self.ValueDropObjectsNotInSource.get(),
            'self.ValueDropPermissionsNotInSource': self.ValueDropPermissionsNotInSource.get(),
            'self.ValueDropRoleMembersNotInSource': self.ValueDropRoleMembersNotInSource.get(),
            'self.ValueExcludeObjectTypes': self.ValueExcludeObjectTypes.get(),
            'self.ValueGenerateSmartDefaults': self.ValueGenerateSmartDefaults.get(),
            'self.ValueIgnoreAnsiNulls': self.ValueIgnoreAnsiNulls.get(),
            'self.ValueIgnoreAuthorizer': self.ValueIgnoreAuthorizer.get(),
            'self.ValueIgnoreColumnCollation': self.ValueIgnoreColumnCollation.get(),
            'self.ValueIgnoreComments': self.ValueIgnoreComments.get(),
            'self.ValueIgnoreCryptographicProviderFilePath': self.ValueIgnoreCryptographicProviderFilePath.get(),
            'self.ValueIgnoreDdlTriggerOrder': self.ValueIgnoreDdlTriggerOrder.get(),
            'self.ValueIgnoreDdlTriggerState': self.ValueIgnoreDdlTriggerState.get(),
            'self.ValueIgnoreDefaultSchema': self.ValueIgnoreDefaultSchema.get(),
            'self.ValueIgnoreDmlTriggerOrder': self.ValueIgnoreDmlTriggerOrder.get(),
            'self.ValueIgnoreDmlTriggerState': self.ValueIgnoreDmlTriggerState.get(),
            'self.ValueIgnoreExtendedProperties': self.ValueIgnoreExtendedProperties.get(),
            'self.ValueIgnoreFileAndLogFilePath': self.ValueIgnoreFileAndLogFilePath.get(),
            'self.ValueIgnoreFilegroupPlacement': self.ValueIgnoreFilegroupPlacement.get(),
            'self.ValueIgnoreFileSize': self.ValueIgnoreFileSize.get(),
            'self.ValueIgnoreFillFactor': self.ValueIgnoreFillFactor.get(),
            'self.ValueIgnoreFullTextCatalogFilePath': self.ValueIgnoreFullTextCatalogFilePath.get(),
            'self.ValueIgnoreIdentitySeed': self.ValueIgnoreIdentitySeed.get(),
            'self.ValueIgnoreIncrement': self.ValueIgnoreIncrement.get(),
            'self.ValueIgnoreIndexOptions': self.ValueIgnoreIndexOptions.get(),
            'self.ValueIgnoreIndexPadding': self.ValueIgnoreIndexPadding.get(),
            'self.ValueIgnoreKeywordCasing': self.ValueIgnoreKeywordCasing.get(),
            'self.ValueIgnoreLockHintsOnIndexes': self.ValueIgnoreLockHintsOnIndexes.get(),
            'self.ValueIgnoreLoginSids': self.ValueIgnoreLoginSids.get(),
            'self.ValueIgnoreNotForReplication': self.ValueIgnoreNotForReplication.get(),
            'self.ValueIgnoreObjectPlacementOnPartitionScheme': self.ValueIgnoreObjectPlacementOnPartitionScheme.get(),
            'self.ValueIgnorePartitionSchemes': self.ValueIgnorePartitionSchemes.get(),
            'self.ValueIgnorePermissions': self.ValueIgnorePermissions.get(),
            'self.ValueIgnoreQuotedIdentifiers': self.ValueIgnoreQuotedIdentifiers.get(),
            'self.ValueIgnoreRoleMembership': self.ValueIgnoreRoleMembership.get(),
            'self.ValueIgnoreRouteLifetime': self.ValueIgnoreRouteLifetime.get(),
            'self.ValueIgnoreSemicolonBetweenStatements': self.ValueIgnoreSemicolonBetweenStatements.get(),
            'self.ValueIgnoreTableOptions': self.ValueIgnoreTableOptions.get(),
            'self.ValueIgnoreUserSettingsObjects': self.ValueIgnoreUserSettingsObjects.get(),
            'self.ValueIgnoreWhitespace': self.ValueIgnoreWhitespace.get(),
            'self.ValueIgnoreWithNocheckOnCheckConstraints': self.ValueIgnoreWithNocheckOnCheckConstraints.get(),
            'self.ValueIgnoreWithNocheckOnForeignKeys': self.ValueIgnoreWithNocheckOnForeignKeys.get(),
            'self.ValueIncludeCompositeObjects': self.ValueIncludeCompositeObjects.get(),
            'self.ValueIncludeTransactionalScripts': self.ValueIncludeTransactionalScripts.get(),
            'self.ValueNoAlterStatementsToChangeClrTypes': self.ValueNoAlterStatementsToChangeClrTypes.get(),
            'self.ValuePopulateFilesOnFilegroups': self.ValuePopulateFilesOnFilegroups.get(),
            'self.ValueRegisterDataTierApplication': self.ValueRegisterDataTierApplication.get(),
            'self.ValueRunDeploymentPlanExecutors': self.ValueRunDeploymentPlanExecutors.get(),
            'self.ValueScriptDatabaseCollation': self.ValueScriptDatabaseCollation.get(),
            'self.ValueScriptDatabaseCompatibility': self.ValueScriptDatabaseCompatibility.get(),
            'self.ValueScriptDatabaseOptions': self.ValueScriptDatabaseOptions.get(),
            'self.ValueScriptDeployStateChecks': self.ValueScriptDeployStateChecks.get(),
            'self.ValueScriptFileSize': self.ValueScriptFileSize.get(),
            'self.ValueScriptNewConstraintValidation': self.ValueScriptNewConstraintValidation.get(),
            'self.ValueScriptRefreshModule': self.ValueScriptRefreshModule.get(),
            'self.ValueStorage': self.ValueStorage.get(),
            'self.ValueTreatVerificationErrorsAsWarnings': self.ValueTreatVerificationErrorsAsWarnings.get(),
            'self.ValueUnmodifiableObjectWarnings': self.ValueUnmodifiableObjectWarnings.get(),
            'self.ValueVerifyCollationCompatibility': self.ValueVerifyCollationCompatibility.get(),
            'self.ValueVerifyDeployment': self.ValueVerifyDeployment.get(),

            'self.DoNotDropObjectTypesAggregates': self.DoNotDropObjectTypesAggregates.get(),
            'self.DoNotDropObjectTypesApplicationRoles': self.DoNotDropObjectTypesApplicationRoles.get(),
            'self.DoNotDropObjectTypesAssemblies': self.DoNotDropObjectTypesAssemblies.get(),
            'self.DoNotDropObjectTypesAsymmetricKeys': self.DoNotDropObjectTypesAsymmetricKeys.get(),
            'self.DoNotDropObjectTypesBrokerPriorities': self.DoNotDropObjectTypesBrokerPriorities.get(),
            'self.DoNotDropObjectTypesCertificates': self.DoNotDropObjectTypesCertificates.get(),
            'self.DoNotDropObjectTypesContracts': self.DoNotDropObjectTypesContracts.get(),
            'self.DoNotDropObjectTypesDatabaseRoles': self.DoNotDropObjectTypesDatabaseRoles.get(),
            'self.DoNotDropObjectTypesDatabaseTriggers': self.DoNotDropObjectTypesDatabaseTriggers.get(),
            'self.DoNotDropObjectTypesDefaults': self.DoNotDropObjectTypesDefaults.get(),
            'self.DoNotDropObjectTypesExtendedProperties': self.DoNotDropObjectTypesExtendedProperties.get(),
            'self.DoNotDropObjectTypesFilegroups': self.DoNotDropObjectTypesFilegroups.get(),
            'self.DoNotDropObjectTypesFileTables': self.DoNotDropObjectTypesFileTables.get(),
            'self.DoNotDropObjectTypesFullTextCatalogs': self.DoNotDropObjectTypesFullTextCatalogs.get(),
            'self.DoNotDropObjectTypesFullTextStoplists': self.DoNotDropObjectTypesFullTextStoplists.get(),
            'self.DoNotDropObjectTypesMessageTypes': self.DoNotDropObjectTypesMessageTypes.get(),
            'self.DoNotDropObjectTypesPartitionFunctions': self.DoNotDropObjectTypesPartitionFunctions.get(),
            'self.DoNotDropObjectTypesPartitionSchemes': self.DoNotDropObjectTypesPartitionSchemes.get(),
            'self.DoNotDropObjectTypesPermissions': self.DoNotDropObjectTypesPermissions.get(),
            'self.DoNotDropObjectTypesQueues': self.DoNotDropObjectTypesQueues.get(),
            'self.DoNotDropObjectTypesRemoteServiceBindings': self.DoNotDropObjectTypesRemoteServiceBindings.get(),
            'self.DoNotDropObjectTypesRoleMembership': self.DoNotDropObjectTypesRoleMembership.get(),
            'self.DoNotDropObjectTypesRules': self.DoNotDropObjectTypesRules.get(),
            'self.DoNotDropObjectTypesScalarValuedFunctions': self.DoNotDropObjectTypesScalarValuedFunctions.get(),
            'self.DoNotDropObjectTypesSearchPropertyLists': self.DoNotDropObjectTypesSearchPropertyLists.get(),
            'self.DoNotDropObjectTypesSequences': self.DoNotDropObjectTypesSequences.get(),
            'self.DoNotDropObjectTypesServices': self.DoNotDropObjectTypesServices.get(),
            'self.DoNotDropObjectTypesSignatures': self.DoNotDropObjectTypesSignatures.get(),
            'self.DoNotDropObjectTypesStoredProcedures': self.DoNotDropObjectTypesStoredProcedures.get(),
            'self.DoNotDropObjectTypesSymmetricKeys': self.DoNotDropObjectTypesSymmetricKeys.get(),
            'self.DoNotDropObjectTypesSynonyms': self.DoNotDropObjectTypesSynonyms.get(),
            'self.DoNotDropObjectTypesTables': self.DoNotDropObjectTypesTables.get(),
            'self.DoNotDropObjectTypesTableValuedFunctions': self.DoNotDropObjectTypesTableValuedFunctions.get(),
            'self.DoNotDropObjectTypesUserDefinedDataTypes': self.DoNotDropObjectTypesUserDefinedDataTypes.get(),
            'self.DoNotDropObjectTypesUserDefinedTableTypes': self.DoNotDropObjectTypesUserDefinedTableTypes.get(),
            'self.DoNotDropObjectTypesClrUserDefinedTypes': self.DoNotDropObjectTypesClrUserDefinedTypes.get(),
            'self.DoNotDropObjectTypesUsers': self.DoNotDropObjectTypesUsers.get(),
            'self.DoNotDropObjectTypesViews': self.DoNotDropObjectTypesViews.get(),
            'self.DoNotDropObjectTypesXmlSchemaCollections': self.DoNotDropObjectTypesXmlSchemaCollections.get(),
            'self.DoNotDropObjectTypesAudits': self.DoNotDropObjectTypesAudits.get(),
            'self.DoNotDropObjectTypesCredentials': self.DoNotDropObjectTypesCredentials.get(),
            'self.DoNotDropObjectTypesCryptographicProviders': self.DoNotDropObjectTypesCryptographicProviders.get(),
            'self.DoNotDropObjectTypesDatabaseAuditSpecifications': self.DoNotDropObjectTypesDatabaseAuditSpecifications.get(),
            'self.DoNotDropObjectTypesEndpoints': self.DoNotDropObjectTypesEndpoints.get(),
            'self.DoNotDropObjectTypesErrorMessages': self.DoNotDropObjectTypesErrorMessages.get(),
            'self.DoNotDropObjectTypesEventNotifications': self.DoNotDropObjectTypesEventNotifications.get(),
            'self.DoNotDropObjectTypesEventSessions': self.DoNotDropObjectTypesEventSessions.get(),
            'self.DoNotDropObjectTypesLinkedServerLogins': self.DoNotDropObjectTypesLinkedServerLogins.get(),
            'self.DoNotDropObjectTypesLinkedServers': self.DoNotDropObjectTypesLinkedServers.get(),
            'self.DoNotDropObjectTypesLogins': self.DoNotDropObjectTypesLogins.get(),
            'self.DoNotDropObjectTypesRoutes': self.DoNotDropObjectTypesRoutes.get(),
            'self.DoNotDropObjectTypesServerAuditSpecifications': self.DoNotDropObjectTypesServerAuditSpecifications.get(),
            'self.DoNotDropObjectTypesServerRoleMembership': self.DoNotDropObjectTypesServerRoleMembership.get(),
            'self.DoNotDropObjectTypesServerRoles': self.DoNotDropObjectTypesServerRoles.get(),
            'self.DoNotDropObjectTypesServerTriggers': self.DoNotDropObjectTypesServerTriggers.get(),

            'self.ExcludeObjectTypesAggregates': self.ExcludeObjectTypesAggregates.get(),
            'self.ExcludeObjectTypesApplicationRoles': self.ExcludeObjectTypesApplicationRoles.get(),
            'self.ExcludeObjectTypesAssemblies': self.ExcludeObjectTypesAssemblies.get(),
            'self.ExcludeObjectTypesAsymmetricKeys': self.ExcludeObjectTypesAsymmetricKeys.get(),
            'self.ExcludeObjectTypesBrokerPriorities': self.ExcludeObjectTypesBrokerPriorities.get(),
            'self.ExcludeObjectTypesCertificates': self.ExcludeObjectTypesCertificates.get(),
            'self.ExcludeObjectTypesContracts': self.ExcludeObjectTypesContracts.get(),
            'self.ExcludeObjectTypesDatabaseRoles': self.ExcludeObjectTypesDatabaseRoles.get(),
            'self.ExcludeObjectTypesDatabaseTriggers': self.ExcludeObjectTypesDatabaseTriggers.get(),
            'self.ExcludeObjectTypesDefaults': self.ExcludeObjectTypesDefaults.get(),
            'self.ExcludeObjectTypesExtendedProperties': self.ExcludeObjectTypesExtendedProperties.get(),
            'self.ExcludeObjectTypesFilegroups': self.ExcludeObjectTypesFilegroups.get(),
            'self.ExcludeObjectTypesFileTables': self.ExcludeObjectTypesFileTables.get(),
            'self.ExcludeObjectTypesFullTextCatalogs': self.ExcludeObjectTypesFullTextCatalogs.get(),
            'self.ExcludeObjectTypesFullTextStoplists': self.ExcludeObjectTypesFullTextStoplists.get(),
            'self.ExcludeObjectTypesMessageTypes': self.ExcludeObjectTypesMessageTypes.get(),
            'self.ExcludeObjectTypesPartitionFunctions': self.ExcludeObjectTypesPartitionFunctions.get(),
            'self.ExcludeObjectTypesPartitionSchemes': self.ExcludeObjectTypesPartitionSchemes.get(),
            'self.ExcludeObjectTypesPermissions': self.ExcludeObjectTypesPermissions.get(),
            'self.ExcludeObjectTypesQueues': self.ExcludeObjectTypesQueues.get(),
            'self.ExcludeObjectTypesRemoteServiceBindings': self.ExcludeObjectTypesRemoteServiceBindings.get(),
            'self.ExcludeObjectTypesRoleMembership': self.ExcludeObjectTypesRoleMembership.get(),
            'self.ExcludeObjectTypesRules': self.ExcludeObjectTypesRules.get(),
            'self.ExcludeObjectTypesScalarValuedFunctions': self.ExcludeObjectTypesScalarValuedFunctions.get(),
            'self.ExcludeObjectTypesSearchPropertyLists': self.ExcludeObjectTypesSearchPropertyLists.get(),
            'self.ExcludeObjectTypesSequences': self.ExcludeObjectTypesSequences.get(),
            'self.ExcludeObjectTypesServices': self.ExcludeObjectTypesServices.get(),
            'self.ExcludeObjectTypesSignatures': self.ExcludeObjectTypesSignatures.get(),
            'self.ExcludeObjectTypesStoredProcedures': self.ExcludeObjectTypesStoredProcedures.get(),
            'self.ExcludeObjectTypesSymmetricKeys': self.ExcludeObjectTypesSymmetricKeys.get(),
            'self.ExcludeObjectTypesSynonyms': self.ExcludeObjectTypesSynonyms.get(),
            'self.ExcludeObjectTypesTables': self.ExcludeObjectTypesTables.get(),
            'self.ExcludeObjectTypesTableValuedFunctions': self.ExcludeObjectTypesTableValuedFunctions.get(),
            'self.ExcludeObjectTypesUserDefinedDataTypes': self.ExcludeObjectTypesUserDefinedDataTypes.get(),
            'self.ExcludeObjectTypesUserDefinedTableTypes': self.ExcludeObjectTypesUserDefinedTableTypes.get(),
            'self.ExcludeObjectTypesClrUserDefinedTypes': self.ExcludeObjectTypesClrUserDefinedTypes.get(),
            'self.ExcludeObjectTypesUsers': self.ExcludeObjectTypesUsers.get(),
            'self.ExcludeObjectTypesViews': self.ExcludeObjectTypesViews.get(),
            'self.ExcludeObjectTypesXmlSchemaCollections': self.ExcludeObjectTypesXmlSchemaCollections.get(),
            'self.ExcludeObjectTypesAudits': self.ExcludeObjectTypesAudits.get(),
            'self.ExcludeObjectTypesCredentials': self.ExcludeObjectTypesCredentials.get(),
            'self.ExcludeObjectTypesCryptographicProviders': self.ExcludeObjectTypesCryptographicProviders.get(),
            'self.ExcludeObjectTypesDatabaseAuditSpecifications': self.ExcludeObjectTypesDatabaseAuditSpecifications.get(),
            'self.ExcludeObjectTypesEndpoints': self.ExcludeObjectTypesEndpoints.get(),
            'self.ExcludeObjectTypesErrorMessages': self.ExcludeObjectTypesErrorMessages.get(),
            'self.ExcludeObjectTypesEventNotifications': self.ExcludeObjectTypesEventNotifications.get(),
            'self.ExcludeObjectTypesEventSessions': self.ExcludeObjectTypesEventSessions.get(),
            'self.ExcludeObjectTypesLinkedServerLogins': self.ExcludeObjectTypesLinkedServerLogins.get(),
            'self.ExcludeObjectTypesLinkedServers': self.ExcludeObjectTypesLinkedServers.get(),
            'self.ExcludeObjectTypesLogins': self.ExcludeObjectTypesLogins.get(),
            'self.ExcludeObjectTypesRoutes': self.ExcludeObjectTypesRoutes.get(),
            'self.ExcludeObjectTypesServerAuditSpecifications': self.ExcludeObjectTypesServerAuditSpecifications.get(),
            'self.ExcludeObjectTypesServerRoleMembership': self.ExcludeObjectTypesServerRoleMembership.get(),
            'self.ExcludeObjectTypesServerRoles': self.ExcludeObjectTypesServerRoles.get(),
            'self.ExcludeObjectTypesServerTriggers': self.ExcludeObjectTypesServerTriggers.get()

        }

        self.save_file_path = filedialog.asksaveasfilename(**self.options)

        with open(self.save_file_path, 'w') as f:
            json.dump(self.save_profile_data, f, indent=4)

    def load_profile(self):
        self.open_file_path = filedialog.askopenfilename(**self.options)

        with open(self.open_file_path, 'r') as f:
            self.open_profile_data = json.load(f)

        self.PreDeploymentText.delete(1.0, END)
        self.PreDeploymentText.insert(END, self.open_profile_data["self.PreDeploymentText"])

        self.SourceServerEntry.delete(0, END)
        self.SourceServerEntry.insert(0, self.open_profile_data["self.SourceServerEntry"])

        self.SourceDatabaseEntry.delete(0, END)
        self.SourceDatabaseEntry.insert(0, self.open_profile_data["self.SourceDatabaseEntry"])

        self.TargetServerEntry.delete(0, END)
        self.TargetServerEntry.insert(0, self.open_profile_data["self.TargetServerEntry"])

        self.TargetDatabaseEntry.delete(0, END)
        self.TargetDatabaseEntry.insert(0, self.open_profile_data["self.TargetDatabaseEntry"])

        self.SourceUsernameEntry.delete(0, END)
        self.SourceUsernameEntry.insert(0, self.open_profile_data["self.SourceUsernameEntry"])

        self.SourcePasswordEntry.delete(0, END)
        self.SourcePasswordEntry.insert(0, self.open_profile_data["self.SourcePasswordEntry"])

        self.TargetUsernameEntry.delete(0, END)
        self.TargetUsernameEntry.insert(0, self.open_profile_data["self.TargetUsernameEntry"])

        self.TargetPasswordEntry.delete(0, END)
        self.TargetPasswordEntry.insert(0, self.open_profile_data["self.TargetPasswordEntry"])

        self.WinAuthSrcVariable.set(self.open_profile_data["self.WinAuthSrcVariable"])
        self.WinAuthTrgtVariable.set(self.open_profile_data["self.WinAuthTrgtVariable"])
        self.EncryptSrcVariable.set(self.open_profile_data["self.EncryptSrcVariable"])
        self.EncryptTrgtVariable.set(self.open_profile_data["self.EncryptTrgtVariable"])
        self.SetDplyPropertyVariable.set(self.open_profile_data["self.SetDplyPropertyVariable"])

        self.ChkButtonAllowDropBlockingAssemblies.set(self.open_profile_data["self.ChkButtonAllowDropBlockingAssemblies"])
        self.ChkButtonAllowIncompatiblePlatform.set(self.open_profile_data["self.ChkButtonAllowIncompatiblePlatform"])
        self.ChkButtonBackupDatabaseBeforeChanges.set(self.open_profile_data["self.ChkButtonBackupDatabaseBeforeChanges"])
        self.ChkButtonBlockOnPossibleDataLoss.set(self.open_profile_data["self.ChkButtonBlockOnPossibleDataLoss"])
        self.ChkButtonBlockWhenDriftDetected.set(self.open_profile_data["self.ChkButtonBlockWhenDriftDetected"])
        self.ChkButtonCommandTimeout.set(self.open_profile_data["self.ChkButtonCommandTimeout"])
        self.ChkButtonCommentOutSetVarDeclarations.set(self.open_profile_data["self.ChkButtonCommentOutSetVarDeclarations"])
        self.ChkButtonCompareUsingTargetCollation.set(self.open_profile_data["self.ChkButtonCompareUsingTargetCollation"])
        self.ChkButtonCreateNewDatabase.set(self.open_profile_data["self.ChkButtonCreateNewDatabase"])
        self.ChkButtonDeployDatabaseInSingleUserMode.set(self.open_profile_data["self.ChkButtonDeployDatabaseInSingleUserMode"])
        self.ChkButtonDisableAndReenableDdlTriggers.set(self.open_profile_data["self.ChkButtonDisableAndReenableDdlTriggers"])
        self.ChkButtonDoNotAlterChangeDataCaptureObjects.set(self.open_profile_data["self.ChkButtonDoNotAlterChangeDataCaptureObjects"])
        self.ChkButtonDoNotAlterReplicatedObjects.set(self.open_profile_data["self.ChkButtonDoNotAlterReplicatedObjects"])
        self.ChkButtonDoNotDropObjectTypes.set(self.open_profile_data["self.ChkButtonDoNotDropObjectTypes"])
        self.ChkButtonDropConstraintsNotInSource.set(self.open_profile_data["self.ChkButtonDropConstraintsNotInSource"])
        self.ChkButtonDropDmlTriggersNotInSource.set(self.open_profile_data["self.ChkButtonDropDmlTriggersNotInSource"])
        self.ChkButtonDropExtendedPropertiesNotInSource.set(self.open_profile_data["self.ChkButtonDropExtendedPropertiesNotInSource"])
        self.ChkButtonDropIndexesNotInSource.set(self.open_profile_data["self.ChkButtonDropIndexesNotInSource"])
        self.ChkButtonDropObjectsNotInSource.set(self.open_profile_data["self.ChkButtonDropObjectsNotInSource"])
        self.ChkButtonDropPermissionsNotInSource.set(self.open_profile_data["self.ChkButtonDropPermissionsNotInSource"])
        self.ChkButtonDropRoleMembersNotInSource.set(self.open_profile_data["self.ChkButtonDropRoleMembersNotInSource"])
        self.ChkButtonExcludeObjectTypes.set(self.open_profile_data["self.ChkButtonExcludeObjectTypes"])
        self.ChkButtonGenerateSmartDefaults.set(self.open_profile_data["self.ChkButtonGenerateSmartDefaults"])
        self.ChkButtonIgnoreAnsiNulls.set(self.open_profile_data["self.ChkButtonIgnoreAnsiNulls"])
        self.ChkButtonIgnoreAuthorizer.set(self.open_profile_data["self.ChkButtonIgnoreAuthorizer"])
        self.ChkButtonIgnoreColumnCollation.set(self.open_profile_data["self.ChkButtonIgnoreColumnCollation"])
        self.ChkButtonIgnoreComments.set(self.open_profile_data["self.ChkButtonIgnoreComments"])
        self.ChkButtonIgnoreCryptographicProviderFilePath.set(self.open_profile_data["self.ChkButtonIgnoreCryptographicProviderFilePath"])
        self.ChkButtonIgnoreDdlTriggerOrder.set(self.open_profile_data["self.ChkButtonIgnoreDdlTriggerOrder"])
        self.ChkButtonIgnoreDdlTriggerState.set(self.open_profile_data["self.ChkButtonIgnoreDdlTriggerState"])
        self.ChkButtonIgnoreDefaultSchema.set(self.open_profile_data["self.ChkButtonIgnoreDefaultSchema"])
        self.ChkButtonIgnoreDmlTriggerOrder.set(self.open_profile_data["self.ChkButtonIgnoreDmlTriggerOrder"])
        self.ChkButtonIgnoreDmlTriggerState.set(self.open_profile_data["self.ChkButtonIgnoreDmlTriggerState"])
        self.ChkButtonIgnoreExtendedProperties.set(self.open_profile_data["self.ChkButtonIgnoreExtendedProperties"])
        self.ChkButtonIgnoreFileAndLogFilePath.set(self.open_profile_data["self.ChkButtonIgnoreFileAndLogFilePath"])
        self.ChkButtonIgnoreFilegroupPlacement.set(self.open_profile_data["self.ChkButtonIgnoreFilegroupPlacement"])
        self.ChkButtonIgnoreFileSize.set(self.open_profile_data["self.ChkButtonIgnoreFileSize"])
        self.ChkButtonIgnoreFillFactor.set(self.open_profile_data["self.ChkButtonIgnoreFillFactor"])
        self.ChkButtonIgnoreFullTextCatalogFilePath.set(self.open_profile_data["self.ChkButtonIgnoreFullTextCatalogFilePath"])
        self.ChkButtonIgnoreIdentitySeed.set(self.open_profile_data["self.ChkButtonIgnoreIdentitySeed"])
        self.ChkButtonIgnoreIncrement.set(self.open_profile_data["self.ChkButtonIgnoreIncrement"])
        self.ChkButtonIgnoreIndexOptions.set(self.open_profile_data["self.ChkButtonIgnoreIndexOptions"])
        self.ChkButtonIgnoreIndexPadding.set(self.open_profile_data["self.ChkButtonIgnoreIndexPadding"])
        self.ChkButtonIgnoreKeywordCasing.set(self.open_profile_data["self.ChkButtonIgnoreKeywordCasing"])
        self.ChkButtonIgnoreLockHintsOnIndexes.set(self.open_profile_data["self.ChkButtonIgnoreLockHintsOnIndexes"])
        self.ChkButtonIgnoreLoginSids.set(self.open_profile_data["self.ChkButtonIgnoreLoginSids"])
        self.ChkButtonIgnoreNotForReplication.set(self.open_profile_data["self.ChkButtonIgnoreNotForReplication"])
        self.ChkButtonIgnoreObjectPlacementOnPartitionScheme.set(self.open_profile_data["self.ChkButtonIgnoreObjectPlacementOnPartitionScheme"])
        self.ChkButtonIgnorePartitionSchemes.set(self.open_profile_data["self.ChkButtonIgnorePartitionSchemes"])
        self.ChkButtonIgnorePermissions.set(self.open_profile_data["self.ChkButtonIgnorePermissions"])
        self.ChkButtonIgnoreQuotedIdentifiers.set(self.open_profile_data["self.ChkButtonIgnoreQuotedIdentifiers"])
        self.ChkButtonIgnoreRoleMembership.set(self.open_profile_data["self.ChkButtonIgnoreRoleMembership"])
        self.ChkButtonIgnoreRouteLifetime.set(self.open_profile_data["self.ChkButtonIgnoreRouteLifetime"])
        self.ChkButtonIgnoreSemicolonBetweenStatements.set(self.open_profile_data["self.ChkButtonIgnoreSemicolonBetweenStatements"])
        self.ChkButtonIgnoreTableOptions.set(self.open_profile_data["self.ChkButtonIgnoreTableOptions"])
        self.ChkButtonIgnoreUserSettingsObjects.set(self.open_profile_data["self.ChkButtonIgnoreUserSettingsObjects"])
        self.ChkButtonIgnoreWhitespace.set(self.open_profile_data["self.ChkButtonIgnoreWhitespace"])
        self.ChkButtonIgnoreWithNocheckOnCheckConstraints.set(self.open_profile_data["self.ChkButtonIgnoreWithNocheckOnCheckConstraints"])
        self.ChkButtonIgnoreWithNocheckOnForeignKeys.set(self.open_profile_data["self.ChkButtonIgnoreWithNocheckOnForeignKeys"])
        self.ChkButtonIncludeCompositeObjects.set(self.open_profile_data["self.ChkButtonIncludeCompositeObjects"])
        self.ChkButtonIncludeTransactionalScripts.set(self.open_profile_data["self.ChkButtonIncludeTransactionalScripts"])
        self.ChkButtonNoAlterStatementsToChangeClrTypes.set(self.open_profile_data["self.ChkButtonNoAlterStatementsToChangeClrTypes"])
        self.ChkButtonPopulateFilesOnFilegroups.set(self.open_profile_data["self.ChkButtonPopulateFilesOnFilegroups"])
        self.ChkButtonRegisterDataTierApplication.set(self.open_profile_data["self.ChkButtonRegisterDataTierApplication"])
        self.ChkButtonRunDeploymentPlanExecutors.set(self.open_profile_data["self.ChkButtonRunDeploymentPlanExecutors"])
        self.ChkButtonScriptDatabaseCollation.set(self.open_profile_data["self.ChkButtonScriptDatabaseCollation"])
        self.ChkButtonScriptDatabaseCompatibility.set(self.open_profile_data["self.ChkButtonScriptDatabaseCompatibility"])
        self.ChkButtonScriptDatabaseOptions.set(self.open_profile_data["self.ChkButtonScriptDatabaseOptions"])
        self.ChkButtonScriptDeployStateChecks.set(self.open_profile_data["self.ChkButtonScriptDeployStateChecks"])
        self.ChkButtonScriptFileSize.set(self.open_profile_data["self.ChkButtonScriptFileSize"])
        self.ChkButtonScriptNewConstraintValidation.set(self.open_profile_data["self.ChkButtonScriptNewConstraintValidation"])
        self.ChkButtonScriptRefreshModule.set(self.open_profile_data["self.ChkButtonScriptRefreshModule"])
        self.ChkButtonStorage.set(self.open_profile_data["self.ChkButtonStorage"])
        self.ChkButtonTreatVerificationErrorsAsWarnings.set(self.open_profile_data["self.ChkButtonTreatVerificationErrorsAsWarnings"])
        self.ChkButtonUnmodifiableObjectWarnings.set(self.open_profile_data["self.ChkButtonUnmodifiableObjectWarnings"])
        self.ChkButtonVerifyCollationCompatibility.set(self.open_profile_data["self.ChkButtonVerifyCollationCompatibility"])
        self.ChkButtonVerifyDeployment.set(self.open_profile_data["self.ChkButtonVerifyDeployment"])

        self.ValueAllowDropBlockingAssemblies.set(self.open_profile_data["self.ValueAllowDropBlockingAssemblies"])
        self.ValueAllowIncompatiblePlatform.set(self.open_profile_data["self.ValueAllowIncompatiblePlatform"])
        self.ValueBackupDatabaseBeforeChanges.set(self.open_profile_data["self.ValueBackupDatabaseBeforeChanges"])
        self.ValueBlockOnPossibleDataLoss.set(self.open_profile_data["self.ValueBlockOnPossibleDataLoss"])
        self.ValueBlockWhenDriftDetected.set(self.open_profile_data["self.ValueBlockWhenDriftDetected"])
        self.EntryCommandTimeout.delete(0, END)
        self.EntryCommandTimeout.insert(0, "60")
        self.ValueCommentOutSetVarDeclarations.set(self.open_profile_data["self.ValueCommentOutSetVarDeclarations"])
        self.ValueCompareUsingTargetCollation.set(self.open_profile_data["self.ValueCompareUsingTargetCollation"])
        self.ValueCreateNewDatabase.set(self.open_profile_data["self.ValueCreateNewDatabase"])
        self.ValueDeployDatabaseInSingleUserMode.set(self.open_profile_data["self.ValueDeployDatabaseInSingleUserMode"])
        self.ValueDisableAndReenableDdlTriggers.set(self.open_profile_data["self.ValueDisableAndReenableDdlTriggers"])
        self.ValueDoNotAlterChangeDataCaptureObjects.set(self.open_profile_data["self.ValueDoNotAlterChangeDataCaptureObjects"])
        self.ValueDoNotAlterReplicatedObjects.set(self.open_profile_data["self.ValueDoNotAlterReplicatedObjects"])
        self.ValueDoNotDropObjectTypes.set(self.open_profile_data["self.ValueDoNotDropObjectTypes"])
        self.ValueDropConstraintsNotInSource.set(self.open_profile_data["self.ValueDropConstraintsNotInSource"])
        self.ValueDropDmlTriggersNotInSource.set(self.open_profile_data["self.ValueDropDmlTriggersNotInSource"])
        self.ValueDropExtendedPropertiesNotInSource.set(self.open_profile_data["self.ValueDropExtendedPropertiesNotInSource"])
        self.ValueDropIndexesNotInSource.set(self.open_profile_data["self.ValueDropIndexesNotInSource"])
        self.ValueDropObjectsNotInSource.set(self.open_profile_data["self.ValueDropObjectsNotInSource"])
        self.ValueDropPermissionsNotInSource.set(self.open_profile_data["self.ValueDropPermissionsNotInSource"])
        self.ValueDropRoleMembersNotInSource.set(self.open_profile_data["self.ValueDropRoleMembersNotInSource"])
        self.ValueExcludeObjectTypes.set(self.open_profile_data["self.ValueExcludeObjectTypes"])
        self.ValueGenerateSmartDefaults.set(self.open_profile_data["self.ValueGenerateSmartDefaults"])
        self.ValueIgnoreAnsiNulls.set(self.open_profile_data["self.ValueIgnoreAnsiNulls"])
        self.ValueIgnoreAuthorizer.set(self.open_profile_data["self.ValueIgnoreAuthorizer"])
        self.ValueIgnoreColumnCollation.set(self.open_profile_data["self.ValueIgnoreColumnCollation"])
        self.ValueIgnoreComments.set(self.open_profile_data["self.ValueIgnoreComments"])
        self.ValueIgnoreCryptographicProviderFilePath.set(self.open_profile_data["self.ValueIgnoreCryptographicProviderFilePath"])
        self.ValueIgnoreDdlTriggerOrder.set(self.open_profile_data["self.ValueIgnoreDdlTriggerOrder"])
        self.ValueIgnoreDdlTriggerState.set(self.open_profile_data["self.ValueIgnoreDdlTriggerState"])
        self.ValueIgnoreDefaultSchema.set(self.open_profile_data["self.ValueIgnoreDefaultSchema"])
        self.ValueIgnoreDmlTriggerOrder.set(self.open_profile_data["self.ValueIgnoreDmlTriggerOrder"])
        self.ValueIgnoreDmlTriggerState.set(self.open_profile_data["self.ValueIgnoreDmlTriggerState"])
        self.ValueIgnoreExtendedProperties.set(self.open_profile_data["self.ValueIgnoreExtendedProperties"])
        self.ValueIgnoreFileAndLogFilePath.set(self.open_profile_data["self.ValueIgnoreFileAndLogFilePath"])
        self.ValueIgnoreFilegroupPlacement.set(self.open_profile_data["self.ValueIgnoreFilegroupPlacement"])
        self.ValueIgnoreFileSize.set(self.open_profile_data["self.ValueIgnoreFileSize"])
        self.ValueIgnoreFillFactor.set(self.open_profile_data["self.ValueIgnoreFillFactor"])
        self.ValueIgnoreFullTextCatalogFilePath.set(self.open_profile_data["self.ValueIgnoreFullTextCatalogFilePath"])
        self.ValueIgnoreIdentitySeed.set(self.open_profile_data["self.ValueIgnoreIdentitySeed"])
        self.ValueIgnoreIncrement.set(self.open_profile_data["self.ValueIgnoreIncrement"])
        self.ValueIgnoreIndexOptions.set(self.open_profile_data["self.ValueIgnoreIndexOptions"])
        self.ValueIgnoreIndexPadding.set(self.open_profile_data["self.ValueIgnoreIndexPadding"])
        self.ValueIgnoreKeywordCasing.set(self.open_profile_data["self.ValueIgnoreKeywordCasing"])
        self.ValueIgnoreLockHintsOnIndexes.set(self.open_profile_data["self.ValueIgnoreLockHintsOnIndexes"])
        self.ValueIgnoreLoginSids.set(self.open_profile_data["self.ValueIgnoreLoginSids"])
        self.ValueIgnoreNotForReplication.set(self.open_profile_data["self.ValueIgnoreNotForReplication"])
        self.ValueIgnoreObjectPlacementOnPartitionScheme.set(self.open_profile_data["self.ValueIgnoreObjectPlacementOnPartitionScheme"])
        self.ValueIgnorePartitionSchemes.set(self.open_profile_data["self.ValueIgnorePartitionSchemes"])
        self.ValueIgnorePermissions.set(self.open_profile_data["self.ValueIgnorePermissions"])
        self.ValueIgnoreQuotedIdentifiers.set(self.open_profile_data["self.ValueIgnoreQuotedIdentifiers"])
        self.ValueIgnoreRoleMembership.set(self.open_profile_data["self.ValueIgnoreRoleMembership"])
        self.ValueIgnoreRouteLifetime.set(self.open_profile_data["self.ValueIgnoreRouteLifetime"])
        self.ValueIgnoreSemicolonBetweenStatements.set(self.open_profile_data["self.ValueIgnoreSemicolonBetweenStatements"])
        self.ValueIgnoreTableOptions.set(self.open_profile_data["self.ValueIgnoreTableOptions"])
        self.ValueIgnoreUserSettingsObjects.set(self.open_profile_data["self.ValueIgnoreUserSettingsObjects"])
        self.ValueIgnoreWhitespace.set(self.open_profile_data["self.ValueIgnoreWhitespace"])
        self.ValueIgnoreWithNocheckOnCheckConstraints.set(self.open_profile_data["self.ValueIgnoreWithNocheckOnCheckConstraints"])
        self.ValueIgnoreWithNocheckOnForeignKeys.set(self.open_profile_data["self.ValueIgnoreWithNocheckOnForeignKeys"])
        self.ValueIncludeCompositeObjects.set(self.open_profile_data["self.ValueIncludeCompositeObjects"])
        self.ValueIncludeTransactionalScripts.set(self.open_profile_data["self.ValueIncludeTransactionalScripts"])
        self.ValueNoAlterStatementsToChangeClrTypes.set(self.open_profile_data["self.ValueNoAlterStatementsToChangeClrTypes"])
        self.ValuePopulateFilesOnFilegroups.set(self.open_profile_data["self.ValuePopulateFilesOnFilegroups"])
        self.ValueRegisterDataTierApplication.set(self.open_profile_data["self.ValueRegisterDataTierApplication"])
        self.ValueRunDeploymentPlanExecutors.set(self.open_profile_data["self.ValueRunDeploymentPlanExecutors"])
        self.ValueScriptDatabaseCollation.set(self.open_profile_data["self.ValueScriptDatabaseCollation"])
        self.ValueScriptDatabaseCompatibility.set(self.open_profile_data["self.ValueScriptDatabaseCompatibility"])
        self.ValueScriptDatabaseOptions.set(self.open_profile_data["self.ValueScriptDatabaseOptions"])
        self.ValueScriptDeployStateChecks.set(self.open_profile_data["self.ValueScriptDeployStateChecks"])
        self.ValueScriptFileSize.set(self.open_profile_data["self.ValueScriptFileSize"])
        self.ValueScriptNewConstraintValidation.set(self.open_profile_data["self.ValueScriptNewConstraintValidation"])
        self.ValueScriptRefreshModule.set(self.open_profile_data["self.ValueScriptRefreshModule"])
        self.ValueStorage.set(self.open_profile_data["self.ValueStorage"])
        self.ValueTreatVerificationErrorsAsWarnings.set(self.open_profile_data["self.ValueTreatVerificationErrorsAsWarnings"])
        self.ValueUnmodifiableObjectWarnings.set(self.open_profile_data["self.ValueUnmodifiableObjectWarnings"])
        self.ValueVerifyCollationCompatibility.set(self.open_profile_data["self.ValueVerifyCollationCompatibility"])
        self.ValueVerifyDeployment.set(self.open_profile_data["self.ValueVerifyDeployment"])

        self.DoNotDropObjectTypesAggregates.set(self.open_profile_data["self.DoNotDropObjectTypesAggregates"])
        self.DoNotDropObjectTypesApplicationRoles.set(self.open_profile_data["self.DoNotDropObjectTypesApplicationRoles"])
        self.DoNotDropObjectTypesAssemblies.set(self.open_profile_data["self.DoNotDropObjectTypesAssemblies"])
        self.DoNotDropObjectTypesAsymmetricKeys.set(self.open_profile_data["self.DoNotDropObjectTypesAsymmetricKeys"])
        self.DoNotDropObjectTypesBrokerPriorities.set(self.open_profile_data["self.DoNotDropObjectTypesBrokerPriorities"])
        self.DoNotDropObjectTypesCertificates.set(self.open_profile_data["self.DoNotDropObjectTypesCertificates"])
        self.DoNotDropObjectTypesContracts.set(self.open_profile_data["self.DoNotDropObjectTypesContracts"])
        self.DoNotDropObjectTypesDatabaseRoles.set(self.open_profile_data["self.DoNotDropObjectTypesDatabaseRoles"])
        self.DoNotDropObjectTypesDatabaseTriggers.set(self.open_profile_data["self.DoNotDropObjectTypesDatabaseTriggers"])
        self.DoNotDropObjectTypesDefaults.set(self.open_profile_data["self.DoNotDropObjectTypesDefaults"])
        self.DoNotDropObjectTypesExtendedProperties.set(self.open_profile_data["self.DoNotDropObjectTypesExtendedProperties"])
        self.DoNotDropObjectTypesFilegroups.set(self.open_profile_data["self.DoNotDropObjectTypesFilegroups"])
        self.DoNotDropObjectTypesFileTables.set(self.open_profile_data["self.DoNotDropObjectTypesFileTables"])
        self.DoNotDropObjectTypesFullTextCatalogs.set(self.open_profile_data["self.DoNotDropObjectTypesFullTextCatalogs"])
        self.DoNotDropObjectTypesFullTextStoplists.set(self.open_profile_data["self.DoNotDropObjectTypesFullTextStoplists"])
        self.DoNotDropObjectTypesMessageTypes.set(self.open_profile_data["self.DoNotDropObjectTypesMessageTypes"])
        self.DoNotDropObjectTypesPartitionFunctions.set(self.open_profile_data["self.DoNotDropObjectTypesPartitionFunctions"])
        self.DoNotDropObjectTypesPartitionSchemes.set(self.open_profile_data["self.DoNotDropObjectTypesPartitionSchemes"])
        self.DoNotDropObjectTypesPermissions.set(self.open_profile_data["self.DoNotDropObjectTypesPermissions"])
        self.DoNotDropObjectTypesQueues.set(self.open_profile_data["self.DoNotDropObjectTypesQueues"])
        self.DoNotDropObjectTypesRemoteServiceBindings.set(self.open_profile_data["self.DoNotDropObjectTypesRemoteServiceBindings"])
        self.DoNotDropObjectTypesRoleMembership.set(self.open_profile_data["self.DoNotDropObjectTypesRoleMembership"])
        self.DoNotDropObjectTypesRules.set(self.open_profile_data["self.DoNotDropObjectTypesRules"])
        self.DoNotDropObjectTypesScalarValuedFunctions.set(self.open_profile_data["self.DoNotDropObjectTypesScalarValuedFunctions"])
        self.DoNotDropObjectTypesSearchPropertyLists.set(self.open_profile_data["self.DoNotDropObjectTypesSearchPropertyLists"])
        self.DoNotDropObjectTypesSequences.set(self.open_profile_data["self.DoNotDropObjectTypesSequences"])
        self.DoNotDropObjectTypesServices.set(self.open_profile_data["self.DoNotDropObjectTypesServices"])
        self.DoNotDropObjectTypesSignatures.set(self.open_profile_data["self.DoNotDropObjectTypesSignatures"])
        self.DoNotDropObjectTypesStoredProcedures.set(self.open_profile_data["self.DoNotDropObjectTypesStoredProcedures"])
        self.DoNotDropObjectTypesSymmetricKeys.set(self.open_profile_data["self.DoNotDropObjectTypesSymmetricKeys"])
        self.DoNotDropObjectTypesSynonyms.set(self.open_profile_data["self.DoNotDropObjectTypesSynonyms"])
        self.DoNotDropObjectTypesTables.set(self.open_profile_data["self.DoNotDropObjectTypesTables"])
        self.DoNotDropObjectTypesTableValuedFunctions.set(self.open_profile_data["self.DoNotDropObjectTypesTableValuedFunctions"])
        self.DoNotDropObjectTypesUserDefinedDataTypes.set(self.open_profile_data["self.DoNotDropObjectTypesUserDefinedDataTypes"])
        self.DoNotDropObjectTypesUserDefinedTableTypes.set(self.open_profile_data["self.DoNotDropObjectTypesUserDefinedTableTypes"])
        self.DoNotDropObjectTypesClrUserDefinedTypes.set(self.open_profile_data["self.DoNotDropObjectTypesClrUserDefinedTypes"])
        self.DoNotDropObjectTypesUsers.set(self.open_profile_data["self.DoNotDropObjectTypesUsers"])
        self.DoNotDropObjectTypesViews.set(self.open_profile_data["self.DoNotDropObjectTypesViews"])
        self.DoNotDropObjectTypesXmlSchemaCollections.set(self.open_profile_data["self.DoNotDropObjectTypesXmlSchemaCollections"])
        self.DoNotDropObjectTypesAudits.set(self.open_profile_data["self.DoNotDropObjectTypesAudits"])
        self.DoNotDropObjectTypesCredentials.set(self.open_profile_data["self.DoNotDropObjectTypesCredentials"])
        self.DoNotDropObjectTypesCryptographicProviders.set(self.open_profile_data["self.DoNotDropObjectTypesCryptographicProviders"])
        self.DoNotDropObjectTypesDatabaseAuditSpecifications.set(self.open_profile_data["self.DoNotDropObjectTypesDatabaseAuditSpecifications"])
        self.DoNotDropObjectTypesEndpoints.set(self.open_profile_data["self.DoNotDropObjectTypesEndpoints"])
        self.DoNotDropObjectTypesErrorMessages.set(self.open_profile_data["self.DoNotDropObjectTypesErrorMessages"])
        self.DoNotDropObjectTypesEventNotifications.set(self.open_profile_data["self.DoNotDropObjectTypesEventNotifications"])
        self.DoNotDropObjectTypesEventSessions.set(self.open_profile_data["self.DoNotDropObjectTypesEventSessions"])
        self.DoNotDropObjectTypesLinkedServerLogins.set(self.open_profile_data["self.DoNotDropObjectTypesLinkedServerLogins"])
        self.DoNotDropObjectTypesLinkedServers.set(self.open_profile_data["self.DoNotDropObjectTypesLinkedServers"])
        self.DoNotDropObjectTypesLogins.set(self.open_profile_data["self.DoNotDropObjectTypesLogins"])
        self.DoNotDropObjectTypesRoutes.set(self.open_profile_data["self.DoNotDropObjectTypesRoutes"])
        self.DoNotDropObjectTypesServerAuditSpecifications.set(self.open_profile_data["self.DoNotDropObjectTypesServerAuditSpecifications"])
        self.DoNotDropObjectTypesServerRoleMembership.set(self.open_profile_data["self.DoNotDropObjectTypesServerRoleMembership"])
        self.DoNotDropObjectTypesServerRoles.set(self.open_profile_data["self.DoNotDropObjectTypesServerRoles"])
        self.DoNotDropObjectTypesServerTriggers.set(self.open_profile_data["self.DoNotDropObjectTypesServerTriggers"])

        self.ExcludeObjectTypesAggregates.set(self.open_profile_data["self.ExcludeObjectTypesAggregates"])
        self.ExcludeObjectTypesApplicationRoles.set(self.open_profile_data["self.ExcludeObjectTypesApplicationRoles"])
        self.ExcludeObjectTypesAssemblies.set(self.open_profile_data["self.ExcludeObjectTypesAssemblies"])
        self.ExcludeObjectTypesAsymmetricKeys.set(self.open_profile_data["self.ExcludeObjectTypesAsymmetricKeys"])
        self.ExcludeObjectTypesBrokerPriorities.set(self.open_profile_data["self.ExcludeObjectTypesBrokerPriorities"])
        self.ExcludeObjectTypesCertificates.set(self.open_profile_data["self.ExcludeObjectTypesCertificates"])
        self.ExcludeObjectTypesContracts.set(self.open_profile_data["self.ExcludeObjectTypesContracts"])
        self.ExcludeObjectTypesDatabaseRoles.set(self.open_profile_data["self.ExcludeObjectTypesDatabaseRoles"])
        self.ExcludeObjectTypesDatabaseTriggers.set(self.open_profile_data["self.ExcludeObjectTypesDatabaseTriggers"])
        self.ExcludeObjectTypesDefaults.set(self.open_profile_data["self.ExcludeObjectTypesDefaults"])
        self.ExcludeObjectTypesExtendedProperties.set(self.open_profile_data["self.ExcludeObjectTypesExtendedProperties"])
        self.ExcludeObjectTypesFilegroups.set(self.open_profile_data["self.ExcludeObjectTypesFilegroups"])
        self.ExcludeObjectTypesFileTables.set(self.open_profile_data["self.ExcludeObjectTypesFileTables"])
        self.ExcludeObjectTypesFullTextCatalogs.set(self.open_profile_data["self.ExcludeObjectTypesFullTextCatalogs"])
        self.ExcludeObjectTypesFullTextStoplists.set(self.open_profile_data["self.ExcludeObjectTypesFullTextStoplists"])
        self.ExcludeObjectTypesMessageTypes.set(self.open_profile_data["self.ExcludeObjectTypesMessageTypes"])
        self.ExcludeObjectTypesPartitionFunctions.set(self.open_profile_data["self.ExcludeObjectTypesPartitionFunctions"])
        self.ExcludeObjectTypesPartitionSchemes.set(self.open_profile_data["self.ExcludeObjectTypesPartitionSchemes"])
        self.ExcludeObjectTypesPermissions.set(self.open_profile_data["self.ExcludeObjectTypesPermissions"])
        self.ExcludeObjectTypesQueues.set(self.open_profile_data["self.ExcludeObjectTypesQueues"])
        self.ExcludeObjectTypesRemoteServiceBindings.set(self.open_profile_data["self.ExcludeObjectTypesRemoteServiceBindings"])
        self.ExcludeObjectTypesRoleMembership.set(self.open_profile_data["self.ExcludeObjectTypesRoleMembership"])
        self.ExcludeObjectTypesRules.set(self.open_profile_data["self.ExcludeObjectTypesRules"])
        self.ExcludeObjectTypesScalarValuedFunctions.set(self.open_profile_data["self.ExcludeObjectTypesScalarValuedFunctions"])
        self.ExcludeObjectTypesSearchPropertyLists.set(self.open_profile_data["self.ExcludeObjectTypesSearchPropertyLists"])
        self.ExcludeObjectTypesSequences.set(self.open_profile_data["self.ExcludeObjectTypesSequences"])
        self.ExcludeObjectTypesServices.set(self.open_profile_data["self.ExcludeObjectTypesServices"])
        self.ExcludeObjectTypesSignatures.set(self.open_profile_data["self.ExcludeObjectTypesSignatures"])
        self.ExcludeObjectTypesStoredProcedures.set(self.open_profile_data["self.ExcludeObjectTypesStoredProcedures"])
        self.ExcludeObjectTypesSymmetricKeys.set(self.open_profile_data["self.ExcludeObjectTypesSymmetricKeys"])
        self.ExcludeObjectTypesSynonyms.set(self.open_profile_data["self.ExcludeObjectTypesSynonyms"])
        self.ExcludeObjectTypesTables.set(self.open_profile_data["self.ExcludeObjectTypesTables"])
        self.ExcludeObjectTypesTableValuedFunctions.set(self.open_profile_data["self.ExcludeObjectTypesTableValuedFunctions"])
        self.ExcludeObjectTypesUserDefinedDataTypes.set(self.open_profile_data["self.ExcludeObjectTypesUserDefinedDataTypes"])
        self.ExcludeObjectTypesUserDefinedTableTypes.set(self.open_profile_data["self.ExcludeObjectTypesUserDefinedTableTypes"])
        self.ExcludeObjectTypesClrUserDefinedTypes.set(self.open_profile_data["self.ExcludeObjectTypesClrUserDefinedTypes"])
        self.ExcludeObjectTypesUsers.set(self.open_profile_data["self.ExcludeObjectTypesUsers"])
        self.ExcludeObjectTypesViews.set(self.open_profile_data["self.ExcludeObjectTypesViews"])
        self.ExcludeObjectTypesXmlSchemaCollections.set(self.open_profile_data["self.ExcludeObjectTypesXmlSchemaCollections"])
        self.ExcludeObjectTypesAudits.set(self.open_profile_data["self.ExcludeObjectTypesAudits"])
        self.ExcludeObjectTypesCredentials.set(self.open_profile_data["self.ExcludeObjectTypesCredentials"])
        self.ExcludeObjectTypesCryptographicProviders.set(self.open_profile_data["self.ExcludeObjectTypesCryptographicProviders"])
        self.ExcludeObjectTypesDatabaseAuditSpecifications.set(self.open_profile_data["self.ExcludeObjectTypesDatabaseAuditSpecifications"])
        self.ExcludeObjectTypesEndpoints.set(self.open_profile_data["self.ExcludeObjectTypesEndpoints"])
        self.ExcludeObjectTypesErrorMessages.set(self.open_profile_data["self.ExcludeObjectTypesErrorMessages"])
        self.ExcludeObjectTypesEventNotifications.set(self.open_profile_data["self.ExcludeObjectTypesEventNotifications"])
        self.ExcludeObjectTypesEventSessions.set(self.open_profile_data["self.ExcludeObjectTypesEventSessions"])
        self.ExcludeObjectTypesLinkedServerLogins.set(self.open_profile_data["self.ExcludeObjectTypesLinkedServerLogins"])
        self.ExcludeObjectTypesLinkedServers.set(self.open_profile_data["self.ExcludeObjectTypesLinkedServers"])
        self.ExcludeObjectTypesLogins.set(self.open_profile_data["self.ExcludeObjectTypesLogins"])
        self.ExcludeObjectTypesRoutes.set(self.open_profile_data["self.ExcludeObjectTypesRoutes"])
        self.ExcludeObjectTypesServerAuditSpecifications.set(self.open_profile_data["self.ExcludeObjectTypesServerAuditSpecifications"])
        self.ExcludeObjectTypesServerRoleMembership.set(self.open_profile_data["self.ExcludeObjectTypesServerRoleMembership"])
        self.ExcludeObjectTypesServerRoles.set(self.open_profile_data["self.ExcludeObjectTypesServerRoles"])
        self.ExcludeObjectTypesServerTriggers.set(self.open_profile_data["self.ExcludeObjectTypesServerTriggers"])

        self.SrcCredentials_Visibility()
        self.TrgtCredentials_Visibility()
        self.DplyScroll_Visibility()

        self.EnDisScrAllowDropBlockingAssemblies()
        self.EnDisScrAllowIncompatiblePlatform()
        self.EnDisScrBackupDatabaseBeforeChanges()
        self.EnDisScrBlockOnPossibleDataLoss()
        self.EnDisScrBlockWhenDriftDetected()
        self.EnDisScrCommandTimeout()
        self.EnDisScrCommentOutSetVarDeclarations()
        self.EnDisScrCompareUsingTargetCollation()
        self.EnDisScrCreateNewDatabase()
        self.EnDisScrDeployDatabaseInSingleUserMode()
        self.EnDisScrDisableAndReenableDdlTriggers()
        self.EnDisScrDoNotAlterChangeDataCaptureObjects()
        self.EnDisScrDoNotAlterReplicatedObjects()
        self.EnDisScrDoNotDropObjectTypes()
        self.EnDisScrDropConstraintsNotInSource()
        self.EnDisScrDropDmlTriggersNotInSource()
        self.EnDisScrDropExtendedPropertiesNotInSource()
        self.EnDisScrDropIndexesNotInSource()
        self.EnDisScrDropObjectsNotInSource()
        self.EnDisScrDropPermissionsNotInSource()
        self.EnDisScrDropRoleMembersNotInSource()
        self.EnDisScrExcludeObjectTypes()
        self.EnDisScrGenerateSmartDefaults()
        self.EnDisScrIgnoreAnsiNulls()
        self.EnDisScrIgnoreAuthorizer()
        self.EnDisScrIgnoreColumnCollation()
        self.EnDisScrIgnoreComments()
        self.EnDisScrIgnoreCryptographicProviderFilePath()
        self.EnDisScrIgnoreDdlTriggerOrder()
        self.EnDisScrIgnoreDdlTriggerState()
        self.EnDisScrIgnoreDefaultSchema()
        self.EnDisScrIgnoreDmlTriggerOrder()
        self.EnDisScrIgnoreDmlTriggerState()
        self.EnDisScrIgnoreExtendedProperties()
        self.EnDisScrIgnoreFileAndLogFilePath()
        self.EnDisScrIgnoreFilegroupPlacement()
        self.EnDisScrIgnoreFileSize()
        self.EnDisScrIgnoreFillFactor()
        self.EnDisScrIgnoreFullTextCatalogFilePath()
        self.EnDisScrIgnoreIdentitySeed()
        self.EnDisScrIgnoreIncrement()
        self.EnDisScrIgnoreIndexOptions()
        self.EnDisScrIgnoreIndexPadding()
        self.EnDisScrIgnoreKeywordCasing()
        self.EnDisScrIgnoreLockHintsOnIndexes()
        self.EnDisScrIgnoreLoginSids()
        self.EnDisScrIgnoreNotForReplication()
        self.EnDisScrIgnoreObjectPlacementOnPartitionScheme()
        self.EnDisScrIgnorePartitionSchemes()
        self.EnDisScrIgnorePermissions()
        self.EnDisScrIgnoreQuotedIdentifiers()
        self.EnDisScrIgnoreRoleMembership()
        self.EnDisScrIgnoreRouteLifetime()
        self.EnDisScrIgnoreSemicolonBetweenStatements()
        self.EnDisScrIgnoreTableOptions()
        self.EnDisScrIgnoreUserSettingsObjects()
        self.EnDisScrIgnoreWhitespace()
        self.EnDisScrIgnoreWithNocheckOnCheckConstraints()
        self.EnDisScrIgnoreWithNocheckOnForeignKeys()
        self.EnDisScrIncludeCompositeObjects()
        self.EnDisScrIncludeTransactionalScripts()
        self.EnDisScrNoAlterStatementsToChangeClrTypes()
        self.EnDisScrPopulateFilesOnFilegroups()
        self.EnDisScrRegisterDataTierApplication()
        self.EnDisScrRunDeploymentPlanExecutors()
        self.EnDisScrScriptDatabaseCollation()
        self.EnDisScrScriptDatabaseCompatibility()
        self.EnDisScrScriptDatabaseOptions()
        self.EnDisScrScriptDeployStateChecks()
        self.EnDisScrScriptFileSize()
        self.EnDisScrScriptNewConstraintValidation()
        self.EnDisScrScriptRefreshModule()
        self.EnDisScrStorage()
        self.EnDisScrTreatVerificationErrorsAsWarnings()
        self.EnDisScrUnmodifiableObjectWarnings()
        self.EnDisScrVerifyCollationCompatibility()
        self.EnDisScrVerifyDeployment()



    def compare_and_deploy(self):
        self.Prepare_Queries("CompareDeployButton")

        q = Queue()
        t = Thread(target=self.reader_thread_CompareDeploy, args=[q])
        t.start()
        self.update(q)

        # # self.SPPreDeployment.wait()\
        # t.join()
        #
        #
        #
        # self.SPExtract = Popen(self.CmpExeExtractQuery, stdout=PIPE, stderr=STDOUT)
        # t = Thread(target=self.reader_thread, args=(q, self.SPExtract))
        # t.start()
        # # q = Queue()
        # self.update(q)
        #
        # # self.SPExtract.wait()
        # t.join()
        #
        #
        #
        # self.SPPublish = Popen(self.CmpExePublishQuery, stdout=PIPE, stderr=STDOUT)
        # # q = Queue()
        # t = Thread(target=self.reader_thread, args=(q,self.SPPublish)).start()
        # self.update(q)



        # self.ShellOutputPreDeploymentString = SPPreDeployment.communicate()[0]
        # self.ShellOutputExtractString = SPExtract.communicate()[0]
        # self.ShellOutputPublishString = SPPublish.communicate()[0]

        # self.InformationString = 'Connection Info:\nSource Server: ' + self.SourceServerEntry.get() + '\nSource Database: ' + self.SourceDatabaseEntry.get() + '\nTarget Server: ' + self.TargetServerEntry.get() + '\nTarget Database: ' + self.TargetDatabaseEntry.get()
        # self.InformationLabel["text"] = self.InformationString


    def compare_generate_script(self):
        CompareGenerateWindow = Toplevel(width=700, height=700)
        CompareGenerateWindow.title("Script")
        CompareGenerateWindow.grid()
        self.update_idletasks()

        self.Prepare_Queries("CompareDeployButton")

        self.CompareGenerateText = Text(CompareGenerateWindow, width=130, height=40, wrap=WORD)
        self.CompareGenerateText.grid(row=0, column=1, columnspan=2, sticky=W)

        # SPExtract = subprocess.Popen(self.CmpExeExtractQuery, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # SPExtract.wait()
        #
        # SPGenerate = subprocess.Popen(self.CmpExeScriptQuery, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        q = Queue()
        t = Thread(target=self.reader_thread_GenerateScript, args=[q])
        t.start()
        self.update(q)

        # self.update_idletasks()

        # self.ShellOutputExtractString = SPExtract.communicate()[0]
        # self.ShellOutputScriptString = SPGenerate.communicate()[0]

        # exit_codes = [p.wait() for p in (SPExtract, SPGenerate)]
        #
        # scriptRead = open('CompareDeploy\\temp\\'+self.TargetDatabaseEntry.get()+'.sql','r')

        # with open('CompareDeploy\\temp\\' + self.TargetDatabaseEntry.get() + '.sql', 'r') as f:
        #     CompareGenerateText.insert(END, f.read())
            #
            # self.update_idletasks()

    ################################################################################################
    ################################################################################################
    ################################## DATA MIGRATION ##############################################
    ################################################################################################
    ################################################################################################



    def create_scrollbar_data(self):
        self.ChkVarDataMigration = BooleanVar()

        # Function to ENABLE/DISABLE
        def EnDisScrDataMigration():
            if self.ChkVarDataMigration.get() is True:
                self.DataFrame.grid(row=15, column=0, sticky=W)
                chkDependenciesCheckButton.grid(row=16, column=1, sticky=W)
                GenerateScriptButton.grid(row=17, column=1, sticky=W)
                DeployDataButton.grid(row=18, column=1, sticky=W)

                DataWidgetsFunction()

            else:
                self.DataFrame.grid_forget()
                chkDependenciesCheckButton.grid_forget()
                GenerateScriptButton.grid_forget()
                DeployDataButton.grid_forget()
                chkDependenciesLabel.grid_forget()

        # BUTTON to ENABLE/DISABLE Data Migration
        ChkDataMigration = Checkbutton(self, text="Perform Data Migration", var=self.ChkVarDataMigration, command=EnDisScrDataMigration)
        ChkDataMigration.grid(row=14, column=0, sticky=W)

        # Source Tables List
        self.SourceTables = {}

        # Function to CREATE WIDGETS
        def DataWidgetsFunction():
            # PREPARE Query and GET TABLE NAMES
            GetTableQuery = "sqlcmd -S " + self.SourceServerEntry.get() + " -d " + self.SourceDatabaseEntry.get() + " -Q \"SELECT s.name + '.' + t.name AS table_name FROM sys.tables t JOIN sys.schemas s ON t.schema_id = s.schema_id ORDER BY s.name + '.' + t.name ASC\""
            SPGetTables = subprocess.Popen(GetTableQuery, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            GetTableOutputString = SPGetTables.communicate()[0]

            # print(GetTableQuery)

            # EXTRACT TABLE NAMES ONLY
            self.TablesStringList = re.split(r'\\r\\n', re.sub(r'(\s*)', '', str(GetTableOutputString)))

            # CREATE CHECKBUTTON FOR EACH
            for i in range(2, len(self.TablesStringList) - 3):
                self.sKey = self.TablesStringList[i]
                self.SourceTables[self.sKey] = BooleanVar()
                self.SourceTables[self.sKey].set(False)
                Checkbutton(DataCanvasFrame, text=self.TablesStringList[i], var=self.SourceTables[self.sKey]).grid(row=i - 2, column=0, sticky=W)
                # print("self.substituteGetTables[i]=" ,self.TablesStringList[i], " i=", i, " self.sKey=", self.sKey, " self.SourceTables[self.sKey].get()=",self.SourceTables[self.sKey].get(), "\n")

                # self.x = BooleanVar()
                # self.x.set(True)
                # Checkbutton(DataCanvasFrame, var=self.x, command=self.EnDisScrAllowDropBlockingAssemblies).grid(row=20, column=0, sticky=W)

        self.delimitedRequiredTables = ""
        self.OrderedTables = ""
        self.TableDiffDependenciesOrder = BooleanVar()
        self.TableDiffDependenciesOrder.set("False")

        # FUNCTION on button click to check table dependencies
        def chkRequiredTablesFn():
            for sKey in self.SourceTables.keys():
                if self.SourceTables[sKey].get() == True:
                    self.delimitedRequiredTables += "'" + sKey + "', "

            # print(self.delimitedRequiredTables[:-2])

            GetTableDependenciesQuery = """sqlcmd -S """ + self.SourceServerEntry.get() + """ -d """ + self.SourceDatabaseEntry.get() + """ -Q \"declare @level int      -- Current depth
                   ,@count int
            if object_id ('tempdb..#Tables') is not null
                drop table #Tables

            select s.name + '.' + t.name  as TableName
                  ,t.object_id            as TableID
                  ,0                      as Ordinal
              into #Tables
              from sys.tables t
              join sys.schemas s
                on t.schema_id = s.schema_id
             where not exists
                   (select 1
                      from sys.foreign_keys f
                     where f.parent_object_id = t.object_id)

            set @count = @@rowcount
            set @level = 0

            while @count > 0 begin

                insert #Tables (
                       TableName
                      ,TableID
                      ,Ordinal
                )
                select s.name + '.' + t.name  as TableName
                      ,t.object_id            as TableID
                      ,@level + 1             as Ordinal
                  from sys.tables t
                  join sys.schemas s
                    on s.schema_id = t.schema_id
                 where exists
                       (select 1
                          from sys.foreign_keys f
                          join #Tables tt
                            on f.referenced_object_id = tt.TableID
                           and tt.Ordinal = @level
                           and f.parent_object_id = t.object_id
                           and f.parent_object_id != f.referenced_object_id)

               set @count = @@rowcount
               set @level = @level + 1
            end

            select t.Ordinal
                  ,t.TableID
                  ,'|' + t.TableName AS TableName
              from #Tables t
              join (select TableName     as TableName
                          ,Max (Ordinal) as Ordinal
                      from #Tables
                     group by TableName) tt
                on t.TableName = tt.TableName
               and t.Ordinal = tt.Ordinal
               WHERE t.TableName IN (""" + self.delimitedRequiredTables[:-2] + """)
             order by t.Ordinal asc\""""""

            # print(GetTableDependenciesQuery)
            SPGetTableDependencies = subprocess.Popen(GetTableDependenciesQuery, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            GetTableDependenciesString = SPGetTableDependencies.communicate()[0]

            self.OrderedTables = re.split(r'\\r\\n', re.split(r'OrdinalTableIDTableName', re.sub(r'(\s*)', '', str(GetTableDependenciesString)))[1])
            print("self.OrderedTables=", self.OrderedTables)

        def TableDiffGenerateQuery():
            chkRequiredTablesFn()
            self.save_scripts_directory = filedialog.askdirectory()
            for i in range(2, len(self.OrderedTables) - 3):
                TableDiffInsertQuery = "CompareDeploy\\tablediff -sourceserver " + self.SourceServerEntry.get() + " -sourcedatabase " + self.SourceDatabaseEntry.get() + " -sourceschema " + \
                                       re.split(r'\.', (re.split(r'\|', self.OrderedTables[i])[1]))[0] + " -sourcetable " + re.split(r'\.', (re.split(r'\|', self.OrderedTables[i])[1]))[
                                           1] + " -destinationserver " + self.TargetServerEntry.get() + " -destinationdatabase " + self.TargetDatabaseEntry.get() + " -destinationschema " + \
                                       re.split(r'\.', re.split(r'\|', self.OrderedTables[i])[1])[0] + " -destinationtable " + re.split(r'\.', re.split(r'\|', self.OrderedTables[i])[1])[
                                           1] + " -f \"" + self.save_scripts_directory + "\\" + re.split(r'\|', self.OrderedTables[i])[1] + ".sql\""
                print(TableDiffInsertQuery)
                # TableDiffInsertQuery = "sqlcmd -S " + self.SourceServerEntry.get() + " -d " + self.SourceDatabaseEntry.get() + " -Q \"SELECT s.name + '.' + t.name AS table_name FROM sys.tables t JOIN sys.schemas s ON t.schema_id = s.schema_id ORDER BY s.name + '.' + t.name ASC\""
                SPTableDiffInsert = subprocess.Popen(TableDiffInsertQuery, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                TableDiffInsertString = SPTableDiffInsert.communicate()[0]

                print(re.split(r'\|', self.OrderedTables[i])[1])

        def TableDiffDeployData():
            chkRequiredTablesFn()
            for i in range(2, len(self.OrderedTables) - 3):
                TableDiffInsertQuery = "CompareDeploy\\tablediff -sourceserver " + self.SourceServerEntry.get() + " -sourcedatabase " + self.SourceDatabaseEntry.get() + " -sourceschema " + \
                                       re.split(r'\.', (re.split(r'\|', self.OrderedTables[i])[1]))[0] + " -sourcetable " + re.split(r'\.', (re.split(r'\|', self.OrderedTables[i])[1]))[
                                           1] + " -destinationserver " + self.TargetServerEntry.get() + " -destinationdatabase " + self.TargetDatabaseEntry.get() + " -destinationschema " + \
                                       re.split(r'\.', re.split(r'\|', self.OrderedTables[i])[1])[0] + " -destinationtable " + re.split(r'\.', re.split(r'\|', self.OrderedTables[i])[1])[
                                           1] + " -f CompareDeploy\\temp\\" + re.split(r'\|', self.OrderedTables[i])[1] + ".sql"
                print(TableDiffInsertQuery)
                # TableDiffInsertQuery = "sqlcmd -S " + self.SourceServerEntry.get() + " -d " + self.SourceDatabaseEntry.get() + " -Q \"SELECT s.name + '.' + t.name AS table_name FROM sys.tables t JOIN sys.schemas s ON t.schema_id = s.schema_id ORDER BY s.name + '.' + t.name ASC\""
                SPTableDiffInsert = subprocess.Popen(TableDiffInsertQuery, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                TableDiffInsertString = SPTableDiffInsert.communicate()[0]

                DeployDataQuery = "sqlcmd -S " + self.TargetServerEntry.get() + " -d " + self.TargetDatabaseEntry.get() + " -i CompareDeploy\\temp\\" + re.split(r'\|', self.OrderedTables[i])[
                    1] + ".sql"
                print(DeployDataQuery)
                SPDeployData = subprocess.Popen(DeployDataQuery, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                DeployDataString = SPDeployData.communicate()[0]

                print(re.split(r'\|', self.OrderedTables[i])[1])

        def CheckTableDepFunction():
            if self.TableDiffDependenciesOrder.get() is True:
                chkDependenciesLabel.grid(row=15, column=1, sticky=W)
                print("Hello")
                chkRequiredTablesFn()
                for i in range(2, len(self.OrderedTables) - 3):
                    appendtext = chkDependenciesLabel.cget("text") + '\n' + re.split(r'\|', self.OrderedTables[i])[1]
                    chkDependenciesLabel.configure(text=appendtext)
                    print(re.split(r'\|', self.OrderedTables[i])[1])
            else:
                chkDependenciesLabel.grid_forget()
                chkDependenciesLabel.configure(text="Dependencies: \n")

        # BUTTON to trigger check table dependencies and FUNCTION it calls above it
        chkDependenciesCheckButton = Checkbutton(self, text="Check Table Dependencies", var=self.TableDiffDependenciesOrder, command=CheckTableDepFunction)

        GenerateScriptButton = Button(self, text="Generate Data Migration Script", command=TableDiffGenerateQuery)

        DeployDataButton = Button(self, text="Compare & Migrate data", command=TableDiffDeployData)

        chkDependenciesLabel = Label(self, text="Dependencies: \n", justify=LEFT)

        # self.SourceTables["dbo.test1"].set(False)
        # Checkbutton(DataCanvasFrame, text=self.substituteGetTables[i], var=self.SourceTables[self.sKey]).grid(row=i - 2, column=0, sticky=W)
        # print(self.SourceTables[self.TablesStringList[2]].get(), self.TablesStringList[2])
        #
        # for machine in SourceTables:
        #     SourceTables[machine] = Variable()
        #     l = Checkbutton(DataCanvasFrame, text=machine, var=SourceTables[machine])
        #     l.pack()

        # temp = substituteGetTables[2]
        # print("value=",SourceTables[temp].get())

        # temp=substituteGetTables[2]
        # print(substituteGetTables[2], SourceTables[temp])
        # SourceTables[temp]=True
        # print(substituteGetTables[2], SourceTables[temp].get())
        # print(sub)
        # print(GetTableQuery)
        # print(len(sub))

        # Checkbuttons, Labels and option menus #################################
        #########################################################################


        def DataCanvasFunction(event):
            DataCanvas.configure(scrollregion=DataCanvas.bbox("all"), width=300, height=300)

        self.DataFrame = Frame(self, relief=GROOVE, width=100, height=100, bd=1)
        # self.DataFrame.grid(row=15, column=0, sticky=W)

        DataCanvas = Canvas(self.DataFrame)
        DataCanvasFrame = Frame(DataCanvas)
        DataScrollbar = Scrollbar(self.DataFrame, orient="vertical", command=DataCanvas.yview)
        DataCanvas.configure(yscrollcommand=DataScrollbar.set)

        DataScrollbar.pack(side="right", fill="y")
        DataCanvas.pack(side="left")
        DataCanvas.create_window((0, 0), window=DataCanvasFrame, anchor='nw')
        DataCanvasFrame.bind("<Configure>", DataCanvasFunction)

    def reader_thread_CompareDeploy(self, q):
        """Read subprocess output and put it into the queue."""
        self.SPPreDeployment = Popen(self.CmpExePreDeploymentQuery, stdout=PIPE, stderr=STDOUT)
        for line in iter(self.SPPreDeployment.stdout.readline, b''):
            q.put(line)
        print('done reading')
        self.SPPreDeployment.wait()

        self.SPExtract = Popen(self.CmpExeExtractQuery, stdout=PIPE, stderr=STDOUT)
        for line in iter(self.SPExtract.stdout.readline, b''):
            q.put(line)
        print('done reading')
        self.SPExtract.wait()

        self.SPPublish = Popen(self.CmpExePublishQuery, stdout=PIPE, stderr=STDOUT)
        for line in iter(self.SPPublish.stdout.readline, b''):
            q.put(line)
        print('done reading')
        self.SPPublish.wait()

    def reader_thread_GenerateScript(self, q):
        self.SPExtract = Popen(self.CmpExeExtractQuery, stdout=PIPE, stderr=STDOUT)
        for line in iter(self.SPExtract.stdout.readline, b''):
            q.put(line)
        print('done reading')
        self.SPExtract.wait()

        self.SPGenerate = Popen(self.CmpExeScriptQuery, stdout=PIPE, stderr=STDOUT)
        for line in iter(self.SPGenerate.stdout.readline, b''):
            q.put(line)
        print('done reading')

        with open('CompareDeploy\\temp\\' + self.TargetDatabaseEntry.get() + '.sql', 'r') as f:
            self.CompareGenerateText.insert(END, f.read())


    def update(self, q):
        """Update GUI with items from the queue."""
        # read no more than 10000 lines, use deque to discard lines except the last one,
        for line in deque(islice(iter_except(q.get_nowait, Empty), 10000), maxlen=1):
            if line is None:
                return  # stop updating
            else:
                self.ShellOutputText.insert(END, line)
                self.ShellOutputText.see(END)
                # newline = self._var.get() + '\n' + (re.sub(r'\\r\\n', '', str(line))[:-1])[2:]
                # self._var.set(newline)  # update GUI

        self.after(40, self.update, q)  # schedule next update

    def stop(self, PopenProcess):
        """Stop subprocess and quit GUI."""
        print('stoping')
        PopenProcess.terminate()  # tell the subprocess to exit

        # kill subprocess if it hasn't exited after a countdown
        def kill_after(countdown):
            if PopenProcess.poll() is None:  # subprocess hasn't exited yet
                countdown -= 1
                if countdown < 0:  # do kill
                    print('killing')
                    PopenProcess.kill()  # more likely to kill on *nix
                else:
                    self.after(1000, kill_after, countdown)
                    return  # continue countdown in a second
            # clean up
            PopenProcess.stdout.close()  # close fd
            PopenProcess.wait()  # wait for the subprocess' exit
            self.destroy()  # exit GUI

        kill_after(countdown=5)


root = Tk()
root.iconbitmap(default='M.ico')
root.title("Compare and Deploy SQL Server database")
root.geometry("1150x900")
app = Application(root)
root.mainloop()
