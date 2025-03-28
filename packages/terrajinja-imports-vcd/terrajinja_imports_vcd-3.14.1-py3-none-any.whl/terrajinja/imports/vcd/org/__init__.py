'''
# `vcd_org`

Refer to the Terraform Registry for docs: [`vcd_org`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class Org(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.org.Org",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org vcd_org}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        full_name: builtins.str,
        name: builtins.str,
        account_lockout: typing.Optional[typing.Union["OrgAccountLockout", typing.Dict[builtins.str, typing.Any]]] = None,
        can_publish_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        can_publish_external_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        can_subscribe_external_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delay_after_power_on_seconds: typing.Optional[jsii.Number] = None,
        delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployed_vm_quota: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stored_vm_quota: typing.Optional[jsii.Number] = None,
        vapp_lease: typing.Optional[typing.Union["OrgVappLease", typing.Dict[builtins.str, typing.Any]]] = None,
        vapp_template_lease: typing.Optional[typing.Union["OrgVappTemplateLease", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org vcd_org} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param full_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#full_name Org#full_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#name Org#name}.
        :param account_lockout: account_lockout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#account_lockout Org#account_lockout}
        :param can_publish_catalogs: True if this organization is allowed to share catalogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_publish_catalogs Org#can_publish_catalogs}
        :param can_publish_external_catalogs: True if this organization is allowed to publish external catalogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_publish_external_catalogs Org#can_publish_external_catalogs}
        :param can_subscribe_external_catalogs: True if this organization is allowed to subscribe to external catalogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_subscribe_external_catalogs Org#can_subscribe_external_catalogs}
        :param delay_after_power_on_seconds: Specifies this organization's default for virtual machine boot delay after power on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delay_after_power_on_seconds Org#delay_after_power_on_seconds}
        :param delete_force: When destroying use delete_force=True with delete_recursive=True to remove an org and any objects it contains, regardless of their state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_force Org#delete_force}
        :param delete_recursive: When destroying use delete_recursive=True to remove the org and any objects it contains that are in a state that normally allows removal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_recursive Org#delete_recursive}
        :param deployed_vm_quota: Maximum number of virtual machines that can be deployed simultaneously by a member of this organization. (0 = unlimited). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#deployed_vm_quota Org#deployed_vm_quota}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#description Org#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#id Org#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: True if this organization is enabled (allows login and all other operations). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#is_enabled Org#is_enabled}
        :param metadata: Key value map of metadata to assign to this organization. Key and value can be any string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#metadata Org#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#metadata_entry Org#metadata_entry}
        :param stored_vm_quota: Maximum number of virtual machines in vApps or vApp templates that can be stored in an undeployed state by a member of this organization. (0 = unlimited) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#stored_vm_quota Org#stored_vm_quota}
        :param vapp_lease: vapp_lease block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#vapp_lease Org#vapp_lease}
        :param vapp_template_lease: vapp_template_lease block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#vapp_template_lease Org#vapp_template_lease}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da99ee655f8aadf64750aabe0324f281cb06b3c669b44bd0c0a4f5a09232c114)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrgConfig(
            full_name=full_name,
            name=name,
            account_lockout=account_lockout,
            can_publish_catalogs=can_publish_catalogs,
            can_publish_external_catalogs=can_publish_external_catalogs,
            can_subscribe_external_catalogs=can_subscribe_external_catalogs,
            delay_after_power_on_seconds=delay_after_power_on_seconds,
            delete_force=delete_force,
            delete_recursive=delete_recursive,
            deployed_vm_quota=deployed_vm_quota,
            description=description,
            id=id,
            is_enabled=is_enabled,
            metadata=metadata,
            metadata_entry=metadata_entry,
            stored_vm_quota=stored_vm_quota,
            vapp_lease=vapp_lease,
            vapp_template_lease=vapp_template_lease,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Org resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Org to import.
        :param import_from_id: The id of the existing Org that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Org to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f26adc5a49fcae011de6b0dcee35dbbad13a1ace9c922845fcc51b29df6f6a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccountLockout")
    def put_account_lockout(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        invalid_logins_before_lockout: jsii.Number,
        lockout_interval_minutes: jsii.Number,
    ) -> None:
        '''
        :param enabled: Whether account lockout is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#enabled Org#enabled}
        :param invalid_logins_before_lockout: Number of login attempts that will trigger an account lockout for the given user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#invalid_logins_before_lockout Org#invalid_logins_before_lockout}
        :param lockout_interval_minutes: Once a user is locked out, they will not be able to log back in for this time period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#lockout_interval_minutes Org#lockout_interval_minutes}
        '''
        value = OrgAccountLockout(
            enabled=enabled,
            invalid_logins_before_lockout=invalid_logins_before_lockout,
            lockout_interval_minutes=lockout_interval_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putAccountLockout", [value]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgMetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da05bf8553d40284efe3312a506b7f0095e9447d4550a32d6e45d8aeedcec501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="putVappLease")
    def put_vapp_lease(
        self,
        *,
        delete_on_storage_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        maximum_runtime_lease_in_sec: jsii.Number,
        maximum_storage_lease_in_sec: jsii.Number,
        power_off_on_runtime_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param delete_on_storage_lease_expiration: If true, storage for a vApp is deleted when the vApp's lease expires. If false, the storage is flagged for deletion, but not deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_on_storage_lease_expiration Org#delete_on_storage_lease_expiration}
        :param maximum_runtime_lease_in_sec: How long vApps can run before they are automatically stopped (in seconds). 0 means never expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_runtime_lease_in_sec Org#maximum_runtime_lease_in_sec}
        :param maximum_storage_lease_in_sec: How long stopped vApps are available before being automatically cleaned up (in seconds). 0 means never expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_storage_lease_in_sec Org#maximum_storage_lease_in_sec}
        :param power_off_on_runtime_lease_expiration: When true, vApps are powered off when the runtime lease expires. When false, vApps are suspended when the runtime lease expires Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#power_off_on_runtime_lease_expiration Org#power_off_on_runtime_lease_expiration}
        '''
        value = OrgVappLease(
            delete_on_storage_lease_expiration=delete_on_storage_lease_expiration,
            maximum_runtime_lease_in_sec=maximum_runtime_lease_in_sec,
            maximum_storage_lease_in_sec=maximum_storage_lease_in_sec,
            power_off_on_runtime_lease_expiration=power_off_on_runtime_lease_expiration,
        )

        return typing.cast(None, jsii.invoke(self, "putVappLease", [value]))

    @jsii.member(jsii_name="putVappTemplateLease")
    def put_vapp_template_lease(
        self,
        *,
        delete_on_storage_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        maximum_storage_lease_in_sec: jsii.Number,
    ) -> None:
        '''
        :param delete_on_storage_lease_expiration: If true, storage for a vAppTemplate is deleted when the vAppTemplate lease expires. If false, the storage is flagged for deletion, but not deleted Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_on_storage_lease_expiration Org#delete_on_storage_lease_expiration}
        :param maximum_storage_lease_in_sec: How long vApp templates are available before being automatically cleaned up (in seconds). 0 means never expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_storage_lease_in_sec Org#maximum_storage_lease_in_sec}
        '''
        value = OrgVappTemplateLease(
            delete_on_storage_lease_expiration=delete_on_storage_lease_expiration,
            maximum_storage_lease_in_sec=maximum_storage_lease_in_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putVappTemplateLease", [value]))

    @jsii.member(jsii_name="resetAccountLockout")
    def reset_account_lockout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountLockout", []))

    @jsii.member(jsii_name="resetCanPublishCatalogs")
    def reset_can_publish_catalogs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanPublishCatalogs", []))

    @jsii.member(jsii_name="resetCanPublishExternalCatalogs")
    def reset_can_publish_external_catalogs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanPublishExternalCatalogs", []))

    @jsii.member(jsii_name="resetCanSubscribeExternalCatalogs")
    def reset_can_subscribe_external_catalogs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanSubscribeExternalCatalogs", []))

    @jsii.member(jsii_name="resetDelayAfterPowerOnSeconds")
    def reset_delay_after_power_on_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelayAfterPowerOnSeconds", []))

    @jsii.member(jsii_name="resetDeleteForce")
    def reset_delete_force(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteForce", []))

    @jsii.member(jsii_name="resetDeleteRecursive")
    def reset_delete_recursive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRecursive", []))

    @jsii.member(jsii_name="resetDeployedVmQuota")
    def reset_deployed_vm_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeployedVmQuota", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataEntry")
    def reset_metadata_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataEntry", []))

    @jsii.member(jsii_name="resetStoredVmQuota")
    def reset_stored_vm_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoredVmQuota", []))

    @jsii.member(jsii_name="resetVappLease")
    def reset_vapp_lease(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVappLease", []))

    @jsii.member(jsii_name="resetVappTemplateLease")
    def reset_vapp_template_lease(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVappTemplateLease", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accountLockout")
    def account_lockout(self) -> "OrgAccountLockoutOutputReference":
        return typing.cast("OrgAccountLockoutOutputReference", jsii.get(self, "accountLockout"))

    @builtins.property
    @jsii.member(jsii_name="listOfCatalogs")
    def list_of_catalogs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "listOfCatalogs"))

    @builtins.property
    @jsii.member(jsii_name="listOfVdcs")
    def list_of_vdcs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "listOfVdcs"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "OrgMetadataEntryList":
        return typing.cast("OrgMetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="numberOfCatalogs")
    def number_of_catalogs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfCatalogs"))

    @builtins.property
    @jsii.member(jsii_name="numberOfVdcs")
    def number_of_vdcs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfVdcs"))

    @builtins.property
    @jsii.member(jsii_name="vappLease")
    def vapp_lease(self) -> "OrgVappLeaseOutputReference":
        return typing.cast("OrgVappLeaseOutputReference", jsii.get(self, "vappLease"))

    @builtins.property
    @jsii.member(jsii_name="vappTemplateLease")
    def vapp_template_lease(self) -> "OrgVappTemplateLeaseOutputReference":
        return typing.cast("OrgVappTemplateLeaseOutputReference", jsii.get(self, "vappTemplateLease"))

    @builtins.property
    @jsii.member(jsii_name="accountLockoutInput")
    def account_lockout_input(self) -> typing.Optional["OrgAccountLockout"]:
        return typing.cast(typing.Optional["OrgAccountLockout"], jsii.get(self, "accountLockoutInput"))

    @builtins.property
    @jsii.member(jsii_name="canPublishCatalogsInput")
    def can_publish_catalogs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canPublishCatalogsInput"))

    @builtins.property
    @jsii.member(jsii_name="canPublishExternalCatalogsInput")
    def can_publish_external_catalogs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canPublishExternalCatalogsInput"))

    @builtins.property
    @jsii.member(jsii_name="canSubscribeExternalCatalogsInput")
    def can_subscribe_external_catalogs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canSubscribeExternalCatalogsInput"))

    @builtins.property
    @jsii.member(jsii_name="delayAfterPowerOnSecondsInput")
    def delay_after_power_on_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "delayAfterPowerOnSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteForceInput")
    def delete_force_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteForceInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRecursiveInput")
    def delete_recursive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteRecursiveInput"))

    @builtins.property
    @jsii.member(jsii_name="deployedVmQuotaInput")
    def deployed_vm_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deployedVmQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fullNameInput")
    def full_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntryInput")
    def metadata_entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgMetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgMetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storedVmQuotaInput")
    def stored_vm_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storedVmQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="vappLeaseInput")
    def vapp_lease_input(self) -> typing.Optional["OrgVappLease"]:
        return typing.cast(typing.Optional["OrgVappLease"], jsii.get(self, "vappLeaseInput"))

    @builtins.property
    @jsii.member(jsii_name="vappTemplateLeaseInput")
    def vapp_template_lease_input(self) -> typing.Optional["OrgVappTemplateLease"]:
        return typing.cast(typing.Optional["OrgVappTemplateLease"], jsii.get(self, "vappTemplateLeaseInput"))

    @builtins.property
    @jsii.member(jsii_name="canPublishCatalogs")
    def can_publish_catalogs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canPublishCatalogs"))

    @can_publish_catalogs.setter
    def can_publish_catalogs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394c5233df3baeb6aca66b79093ef78d95ff31c6a9f621f635951e3a64c4df75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canPublishCatalogs", value)

    @builtins.property
    @jsii.member(jsii_name="canPublishExternalCatalogs")
    def can_publish_external_catalogs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canPublishExternalCatalogs"))

    @can_publish_external_catalogs.setter
    def can_publish_external_catalogs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbb90c599fa3fd73a5cc0833782f0ae86fe0adabf19910f917c76fbffee20b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canPublishExternalCatalogs", value)

    @builtins.property
    @jsii.member(jsii_name="canSubscribeExternalCatalogs")
    def can_subscribe_external_catalogs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canSubscribeExternalCatalogs"))

    @can_subscribe_external_catalogs.setter
    def can_subscribe_external_catalogs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd9fc36d1316923f968e3bba5c264fe87fe61c3931ed7f675d221d7d2f927e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canSubscribeExternalCatalogs", value)

    @builtins.property
    @jsii.member(jsii_name="delayAfterPowerOnSeconds")
    def delay_after_power_on_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "delayAfterPowerOnSeconds"))

    @delay_after_power_on_seconds.setter
    def delay_after_power_on_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c933ed2548cb963f1082325cd497cf8766ff99ffa26a05b11de2ad149c2b0c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delayAfterPowerOnSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="deleteForce")
    def delete_force(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteForce"))

    @delete_force.setter
    def delete_force(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f060d64a5146a1f6fce28792ad7a9fa718e4923156eec85abac3795d67a4cebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteForce", value)

    @builtins.property
    @jsii.member(jsii_name="deleteRecursive")
    def delete_recursive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteRecursive"))

    @delete_recursive.setter
    def delete_recursive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2ec11ecb39a2518a91e711de6872cc59f9b6729337733d0428d6d7217f2c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRecursive", value)

    @builtins.property
    @jsii.member(jsii_name="deployedVmQuota")
    def deployed_vm_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deployedVmQuota"))

    @deployed_vm_quota.setter
    def deployed_vm_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19ae47cf0cb674b7f3572ba188582fa9ff86de04cf1118409a5a27f9314b8c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployedVmQuota", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e461bd99563e72331c30568f772e437dd576bc56d4c8cad6e35e6a855420a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullName"))

    @full_name.setter
    def full_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc7e1aae3db18a049d2180ac767595068633748e49427c62b2738d7d97e861a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2eba38c2592c624e26af3e85bac5ef1623f592f6b996f81d5b45aa580cdaa7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9200da0790a65615bfe167c8095097df737769d728763fc7358495cd4e0fa27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83cf513777be540d322d7d596cc54aa16aef727bfd268e7dace93f02c6a27367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c75feb7984e6bcc911aa7ccd75c197d767ed12d660b08b0b4777a09211bcb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="storedVmQuota")
    def stored_vm_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storedVmQuota"))

    @stored_vm_quota.setter
    def stored_vm_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9096202e548f06839692246ee554c8b1b11c8ee067c37ac19051e700a2c54f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storedVmQuota", value)


@jsii.data_type(
    jsii_type="vcd.org.OrgAccountLockout",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "invalid_logins_before_lockout": "invalidLoginsBeforeLockout",
        "lockout_interval_minutes": "lockoutIntervalMinutes",
    },
)
class OrgAccountLockout:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        invalid_logins_before_lockout: jsii.Number,
        lockout_interval_minutes: jsii.Number,
    ) -> None:
        '''
        :param enabled: Whether account lockout is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#enabled Org#enabled}
        :param invalid_logins_before_lockout: Number of login attempts that will trigger an account lockout for the given user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#invalid_logins_before_lockout Org#invalid_logins_before_lockout}
        :param lockout_interval_minutes: Once a user is locked out, they will not be able to log back in for this time period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#lockout_interval_minutes Org#lockout_interval_minutes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b4cec623c2deb70371386077bc8775f53f0bef5011ff834c7bd35268fb6964)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument invalid_logins_before_lockout", value=invalid_logins_before_lockout, expected_type=type_hints["invalid_logins_before_lockout"])
            check_type(argname="argument lockout_interval_minutes", value=lockout_interval_minutes, expected_type=type_hints["lockout_interval_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "invalid_logins_before_lockout": invalid_logins_before_lockout,
            "lockout_interval_minutes": lockout_interval_minutes,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether account lockout is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#enabled Org#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def invalid_logins_before_lockout(self) -> jsii.Number:
        '''Number of login attempts that will trigger an account lockout for the given user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#invalid_logins_before_lockout Org#invalid_logins_before_lockout}
        '''
        result = self._values.get("invalid_logins_before_lockout")
        assert result is not None, "Required property 'invalid_logins_before_lockout' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def lockout_interval_minutes(self) -> jsii.Number:
        '''Once a user is locked out, they will not be able to log back in for this time period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#lockout_interval_minutes Org#lockout_interval_minutes}
        '''
        result = self._values.get("lockout_interval_minutes")
        assert result is not None, "Required property 'lockout_interval_minutes' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgAccountLockout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgAccountLockoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.org.OrgAccountLockoutOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0df8d533b6d2bfdda94abbc7ac1b21e86595ccec39b866eddda30c2f08ebc7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="invalidLoginsBeforeLockoutInput")
    def invalid_logins_before_lockout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "invalidLoginsBeforeLockoutInput"))

    @builtins.property
    @jsii.member(jsii_name="lockoutIntervalMinutesInput")
    def lockout_interval_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lockoutIntervalMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc821692eafa7a0aae555e759acc673276b573d5ed46ca95964271b660a2071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="invalidLoginsBeforeLockout")
    def invalid_logins_before_lockout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "invalidLoginsBeforeLockout"))

    @invalid_logins_before_lockout.setter
    def invalid_logins_before_lockout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12a05a9d38fcf9c04ae518152d883e53b1e8bca93f1b5371ffedf1751c4ff5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invalidLoginsBeforeLockout", value)

    @builtins.property
    @jsii.member(jsii_name="lockoutIntervalMinutes")
    def lockout_interval_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockoutIntervalMinutes"))

    @lockout_interval_minutes.setter
    def lockout_interval_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44e53b41590fb5ac01a2b9d0d68663aba1e18b2e08ed25051eb0d56a9791520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockoutIntervalMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgAccountLockout]:
        return typing.cast(typing.Optional[OrgAccountLockout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgAccountLockout]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676772fbf12efc807de2e12a6093b4ce813b52efdd3d7bdf5415b7a617186a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.org.OrgConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "full_name": "fullName",
        "name": "name",
        "account_lockout": "accountLockout",
        "can_publish_catalogs": "canPublishCatalogs",
        "can_publish_external_catalogs": "canPublishExternalCatalogs",
        "can_subscribe_external_catalogs": "canSubscribeExternalCatalogs",
        "delay_after_power_on_seconds": "delayAfterPowerOnSeconds",
        "delete_force": "deleteForce",
        "delete_recursive": "deleteRecursive",
        "deployed_vm_quota": "deployedVmQuota",
        "description": "description",
        "id": "id",
        "is_enabled": "isEnabled",
        "metadata": "metadata",
        "metadata_entry": "metadataEntry",
        "stored_vm_quota": "storedVmQuota",
        "vapp_lease": "vappLease",
        "vapp_template_lease": "vappTemplateLease",
    },
)
class OrgConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        full_name: builtins.str,
        name: builtins.str,
        account_lockout: typing.Optional[typing.Union[OrgAccountLockout, typing.Dict[builtins.str, typing.Any]]] = None,
        can_publish_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        can_publish_external_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        can_subscribe_external_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delay_after_power_on_seconds: typing.Optional[jsii.Number] = None,
        delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployed_vm_quota: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stored_vm_quota: typing.Optional[jsii.Number] = None,
        vapp_lease: typing.Optional[typing.Union["OrgVappLease", typing.Dict[builtins.str, typing.Any]]] = None,
        vapp_template_lease: typing.Optional[typing.Union["OrgVappTemplateLease", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param full_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#full_name Org#full_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#name Org#name}.
        :param account_lockout: account_lockout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#account_lockout Org#account_lockout}
        :param can_publish_catalogs: True if this organization is allowed to share catalogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_publish_catalogs Org#can_publish_catalogs}
        :param can_publish_external_catalogs: True if this organization is allowed to publish external catalogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_publish_external_catalogs Org#can_publish_external_catalogs}
        :param can_subscribe_external_catalogs: True if this organization is allowed to subscribe to external catalogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_subscribe_external_catalogs Org#can_subscribe_external_catalogs}
        :param delay_after_power_on_seconds: Specifies this organization's default for virtual machine boot delay after power on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delay_after_power_on_seconds Org#delay_after_power_on_seconds}
        :param delete_force: When destroying use delete_force=True with delete_recursive=True to remove an org and any objects it contains, regardless of their state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_force Org#delete_force}
        :param delete_recursive: When destroying use delete_recursive=True to remove the org and any objects it contains that are in a state that normally allows removal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_recursive Org#delete_recursive}
        :param deployed_vm_quota: Maximum number of virtual machines that can be deployed simultaneously by a member of this organization. (0 = unlimited). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#deployed_vm_quota Org#deployed_vm_quota}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#description Org#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#id Org#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: True if this organization is enabled (allows login and all other operations). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#is_enabled Org#is_enabled}
        :param metadata: Key value map of metadata to assign to this organization. Key and value can be any string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#metadata Org#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#metadata_entry Org#metadata_entry}
        :param stored_vm_quota: Maximum number of virtual machines in vApps or vApp templates that can be stored in an undeployed state by a member of this organization. (0 = unlimited) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#stored_vm_quota Org#stored_vm_quota}
        :param vapp_lease: vapp_lease block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#vapp_lease Org#vapp_lease}
        :param vapp_template_lease: vapp_template_lease block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#vapp_template_lease Org#vapp_template_lease}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(account_lockout, dict):
            account_lockout = OrgAccountLockout(**account_lockout)
        if isinstance(vapp_lease, dict):
            vapp_lease = OrgVappLease(**vapp_lease)
        if isinstance(vapp_template_lease, dict):
            vapp_template_lease = OrgVappTemplateLease(**vapp_template_lease)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d1b665c99e15fc1fe19b7dcda30c72ced7d4b2df970f66d7282506ec0c9865)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument full_name", value=full_name, expected_type=type_hints["full_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument account_lockout", value=account_lockout, expected_type=type_hints["account_lockout"])
            check_type(argname="argument can_publish_catalogs", value=can_publish_catalogs, expected_type=type_hints["can_publish_catalogs"])
            check_type(argname="argument can_publish_external_catalogs", value=can_publish_external_catalogs, expected_type=type_hints["can_publish_external_catalogs"])
            check_type(argname="argument can_subscribe_external_catalogs", value=can_subscribe_external_catalogs, expected_type=type_hints["can_subscribe_external_catalogs"])
            check_type(argname="argument delay_after_power_on_seconds", value=delay_after_power_on_seconds, expected_type=type_hints["delay_after_power_on_seconds"])
            check_type(argname="argument delete_force", value=delete_force, expected_type=type_hints["delete_force"])
            check_type(argname="argument delete_recursive", value=delete_recursive, expected_type=type_hints["delete_recursive"])
            check_type(argname="argument deployed_vm_quota", value=deployed_vm_quota, expected_type=type_hints["deployed_vm_quota"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_entry", value=metadata_entry, expected_type=type_hints["metadata_entry"])
            check_type(argname="argument stored_vm_quota", value=stored_vm_quota, expected_type=type_hints["stored_vm_quota"])
            check_type(argname="argument vapp_lease", value=vapp_lease, expected_type=type_hints["vapp_lease"])
            check_type(argname="argument vapp_template_lease", value=vapp_template_lease, expected_type=type_hints["vapp_template_lease"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "full_name": full_name,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if account_lockout is not None:
            self._values["account_lockout"] = account_lockout
        if can_publish_catalogs is not None:
            self._values["can_publish_catalogs"] = can_publish_catalogs
        if can_publish_external_catalogs is not None:
            self._values["can_publish_external_catalogs"] = can_publish_external_catalogs
        if can_subscribe_external_catalogs is not None:
            self._values["can_subscribe_external_catalogs"] = can_subscribe_external_catalogs
        if delay_after_power_on_seconds is not None:
            self._values["delay_after_power_on_seconds"] = delay_after_power_on_seconds
        if delete_force is not None:
            self._values["delete_force"] = delete_force
        if delete_recursive is not None:
            self._values["delete_recursive"] = delete_recursive
        if deployed_vm_quota is not None:
            self._values["deployed_vm_quota"] = deployed_vm_quota
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_entry is not None:
            self._values["metadata_entry"] = metadata_entry
        if stored_vm_quota is not None:
            self._values["stored_vm_quota"] = stored_vm_quota
        if vapp_lease is not None:
            self._values["vapp_lease"] = vapp_lease
        if vapp_template_lease is not None:
            self._values["vapp_template_lease"] = vapp_template_lease

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def full_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#full_name Org#full_name}.'''
        result = self._values.get("full_name")
        assert result is not None, "Required property 'full_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#name Org#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_lockout(self) -> typing.Optional[OrgAccountLockout]:
        '''account_lockout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#account_lockout Org#account_lockout}
        '''
        result = self._values.get("account_lockout")
        return typing.cast(typing.Optional[OrgAccountLockout], result)

    @builtins.property
    def can_publish_catalogs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if this organization is allowed to share catalogs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_publish_catalogs Org#can_publish_catalogs}
        '''
        result = self._values.get("can_publish_catalogs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def can_publish_external_catalogs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if this organization is allowed to publish external catalogs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_publish_external_catalogs Org#can_publish_external_catalogs}
        '''
        result = self._values.get("can_publish_external_catalogs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def can_subscribe_external_catalogs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if this organization is allowed to subscribe to external catalogs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#can_subscribe_external_catalogs Org#can_subscribe_external_catalogs}
        '''
        result = self._values.get("can_subscribe_external_catalogs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delay_after_power_on_seconds(self) -> typing.Optional[jsii.Number]:
        '''Specifies this organization's default for virtual machine boot delay after power on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delay_after_power_on_seconds Org#delay_after_power_on_seconds}
        '''
        result = self._values.get("delay_after_power_on_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When destroying use delete_force=True with delete_recursive=True to remove an org and any objects it contains, regardless of their state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_force Org#delete_force}
        '''
        result = self._values.get("delete_force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_recursive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When destroying use delete_recursive=True to remove the org and any objects it contains that are in a state that normally allows removal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_recursive Org#delete_recursive}
        '''
        result = self._values.get("delete_recursive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deployed_vm_quota(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of virtual machines that can be deployed simultaneously by a member of this organization. (0 = unlimited).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#deployed_vm_quota Org#deployed_vm_quota}
        '''
        result = self._values.get("deployed_vm_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#description Org#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#id Org#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if this organization is enabled (allows login and all other operations).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#is_enabled Org#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key value map of metadata to assign to this organization. Key and value can be any string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#metadata Org#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgMetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#metadata_entry Org#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgMetadataEntry"]]], result)

    @builtins.property
    def stored_vm_quota(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of virtual machines in vApps or vApp templates that can be stored in an undeployed state by a member of this organization.

        (0 = unlimited)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#stored_vm_quota Org#stored_vm_quota}
        '''
        result = self._values.get("stored_vm_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vapp_lease(self) -> typing.Optional["OrgVappLease"]:
        '''vapp_lease block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#vapp_lease Org#vapp_lease}
        '''
        result = self._values.get("vapp_lease")
        return typing.cast(typing.Optional["OrgVappLease"], result)

    @builtins.property
    def vapp_template_lease(self) -> typing.Optional["OrgVappTemplateLease"]:
        '''vapp_template_lease block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#vapp_template_lease Org#vapp_template_lease}
        '''
        result = self._values.get("vapp_template_lease")
        return typing.cast(typing.Optional["OrgVappTemplateLease"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.org.OrgMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "is_system": "isSystem",
        "key": "key",
        "type": "type",
        "user_access": "userAccess",
        "value": "value",
    },
)
class OrgMetadataEntry:
    def __init__(
        self,
        *,
        is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user_access: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#is_system Org#is_system}
        :param key: Key of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#key Org#key}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#type Org#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#user_access Org#user_access}
        :param value: Value of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#value Org#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea5d45fda5b015f66cb9c92a16b50f5c5d073404082fafa27841b6710a5c02a)
            check_type(argname="argument is_system", value=is_system, expected_type=type_hints["is_system"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_access", value=user_access, expected_type=type_hints["user_access"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_system is not None:
            self._values["is_system"] = is_system
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if user_access is not None:
            self._values["user_access"] = user_access
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_system(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#is_system Org#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#key Org#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#type Org#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#user_access Org#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#value Org#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgMetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.org.OrgMetadataEntryList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34ab83bc6a896c302e0b83ee452798b238c6646d57d5d060ff3335cde5e39ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrgMetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c6935b9965ae858fdfb4d4b3ef77b6d0e6f41b0615079747ff3e9989e45d63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrgMetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dece60e3a2d2c93337af0fbb0df50a23120057e153eb8201f240525bf17788e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b879335dfb07abadc96bffb0c3b1843d4379fdf6bb3e35813d3d9e9021876008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419b0b738c9f9d9916a92de095e3692f0a6f407d3e4837f2d3a6737b3f9c2e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgMetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgMetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgMetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3740630763ef9b2bd0354340e7236806361607432f4a8b45fed8303574d1424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrgMetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.org.OrgMetadataEntryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e589d0d6b9865a68aed9a403dcf001ae8221a4a9effc473a903449fc07a41f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsSystem")
    def reset_is_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSystem", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserAccess")
    def reset_user_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAccess", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="isSystemInput")
    def is_system_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userAccessInput")
    def user_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isSystem")
    def is_system(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSystem"))

    @is_system.setter
    def is_system(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47fa2e5be302590bf11943e670973b87f932bc819fea07aa799ea5a6667363b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe7e03ba834dfb7d727044bce7261bbdafaf44c9c3849fef553df1e26a8a81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076ffb727f9ad7f78a354e036985f82d8684769ad442b83e71ecb7d233aacc40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41df05e86f5d727b1a385e6bb403cc6395866379da9012e00cabb6ba0ee0a0d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb2db3c9cdeb5cde99c13f50f09a6a79eac1753daf8d9949c62564e8a812d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgMetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgMetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgMetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__badb775c217aa4dee888102fb6cdfe60caf670fab37d9f6a69437e707be85925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.org.OrgVappLease",
    jsii_struct_bases=[],
    name_mapping={
        "delete_on_storage_lease_expiration": "deleteOnStorageLeaseExpiration",
        "maximum_runtime_lease_in_sec": "maximumRuntimeLeaseInSec",
        "maximum_storage_lease_in_sec": "maximumStorageLeaseInSec",
        "power_off_on_runtime_lease_expiration": "powerOffOnRuntimeLeaseExpiration",
    },
)
class OrgVappLease:
    def __init__(
        self,
        *,
        delete_on_storage_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        maximum_runtime_lease_in_sec: jsii.Number,
        maximum_storage_lease_in_sec: jsii.Number,
        power_off_on_runtime_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param delete_on_storage_lease_expiration: If true, storage for a vApp is deleted when the vApp's lease expires. If false, the storage is flagged for deletion, but not deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_on_storage_lease_expiration Org#delete_on_storage_lease_expiration}
        :param maximum_runtime_lease_in_sec: How long vApps can run before they are automatically stopped (in seconds). 0 means never expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_runtime_lease_in_sec Org#maximum_runtime_lease_in_sec}
        :param maximum_storage_lease_in_sec: How long stopped vApps are available before being automatically cleaned up (in seconds). 0 means never expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_storage_lease_in_sec Org#maximum_storage_lease_in_sec}
        :param power_off_on_runtime_lease_expiration: When true, vApps are powered off when the runtime lease expires. When false, vApps are suspended when the runtime lease expires Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#power_off_on_runtime_lease_expiration Org#power_off_on_runtime_lease_expiration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297c3602592bfde8ae613de5699c260cad392f93579b933f68753b6447750caa)
            check_type(argname="argument delete_on_storage_lease_expiration", value=delete_on_storage_lease_expiration, expected_type=type_hints["delete_on_storage_lease_expiration"])
            check_type(argname="argument maximum_runtime_lease_in_sec", value=maximum_runtime_lease_in_sec, expected_type=type_hints["maximum_runtime_lease_in_sec"])
            check_type(argname="argument maximum_storage_lease_in_sec", value=maximum_storage_lease_in_sec, expected_type=type_hints["maximum_storage_lease_in_sec"])
            check_type(argname="argument power_off_on_runtime_lease_expiration", value=power_off_on_runtime_lease_expiration, expected_type=type_hints["power_off_on_runtime_lease_expiration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delete_on_storage_lease_expiration": delete_on_storage_lease_expiration,
            "maximum_runtime_lease_in_sec": maximum_runtime_lease_in_sec,
            "maximum_storage_lease_in_sec": maximum_storage_lease_in_sec,
            "power_off_on_runtime_lease_expiration": power_off_on_runtime_lease_expiration,
        }

    @builtins.property
    def delete_on_storage_lease_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, storage for a vApp is deleted when the vApp's lease expires.

        If false, the storage is flagged for deletion, but not deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_on_storage_lease_expiration Org#delete_on_storage_lease_expiration}
        '''
        result = self._values.get("delete_on_storage_lease_expiration")
        assert result is not None, "Required property 'delete_on_storage_lease_expiration' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def maximum_runtime_lease_in_sec(self) -> jsii.Number:
        '''How long vApps can run before they are automatically stopped (in seconds). 0 means never expires.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_runtime_lease_in_sec Org#maximum_runtime_lease_in_sec}
        '''
        result = self._values.get("maximum_runtime_lease_in_sec")
        assert result is not None, "Required property 'maximum_runtime_lease_in_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def maximum_storage_lease_in_sec(self) -> jsii.Number:
        '''How long stopped vApps are available before being automatically cleaned up (in seconds). 0 means never expires.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_storage_lease_in_sec Org#maximum_storage_lease_in_sec}
        '''
        result = self._values.get("maximum_storage_lease_in_sec")
        assert result is not None, "Required property 'maximum_storage_lease_in_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def power_off_on_runtime_lease_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, vApps are powered off when the runtime lease expires.

        When false, vApps are suspended when the runtime lease expires

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#power_off_on_runtime_lease_expiration Org#power_off_on_runtime_lease_expiration}
        '''
        result = self._values.get("power_off_on_runtime_lease_expiration")
        assert result is not None, "Required property 'power_off_on_runtime_lease_expiration' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVappLease(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVappLeaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.org.OrgVappLeaseOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20777be09208973702543382392ff7587a13e74d78198cf8756047168e9b401e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="deleteOnStorageLeaseExpirationInput")
    def delete_on_storage_lease_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteOnStorageLeaseExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRuntimeLeaseInSecInput")
    def maximum_runtime_lease_in_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRuntimeLeaseInSecInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumStorageLeaseInSecInput")
    def maximum_storage_lease_in_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumStorageLeaseInSecInput"))

    @builtins.property
    @jsii.member(jsii_name="powerOffOnRuntimeLeaseExpirationInput")
    def power_off_on_runtime_lease_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "powerOffOnRuntimeLeaseExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteOnStorageLeaseExpiration")
    def delete_on_storage_lease_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteOnStorageLeaseExpiration"))

    @delete_on_storage_lease_expiration.setter
    def delete_on_storage_lease_expiration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b684577ab5d7a533683d4331024e172fa622680b1b47b87644920ef0da8e8979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteOnStorageLeaseExpiration", value)

    @builtins.property
    @jsii.member(jsii_name="maximumRuntimeLeaseInSec")
    def maximum_runtime_lease_in_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRuntimeLeaseInSec"))

    @maximum_runtime_lease_in_sec.setter
    def maximum_runtime_lease_in_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba6ea31bfe7b5caddc3806435991f665020714fc00fd19ece29f0983f18d6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRuntimeLeaseInSec", value)

    @builtins.property
    @jsii.member(jsii_name="maximumStorageLeaseInSec")
    def maximum_storage_lease_in_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumStorageLeaseInSec"))

    @maximum_storage_lease_in_sec.setter
    def maximum_storage_lease_in_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb536641dbc5cc979d533c6fc6a87e72b82c8e4a32c115ead83d6894accc29f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumStorageLeaseInSec", value)

    @builtins.property
    @jsii.member(jsii_name="powerOffOnRuntimeLeaseExpiration")
    def power_off_on_runtime_lease_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "powerOffOnRuntimeLeaseExpiration"))

    @power_off_on_runtime_lease_expiration.setter
    def power_off_on_runtime_lease_expiration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba38dac64458ec0c63f18983cec847074b5a93f28e830fa1897f6f5cdb56d8c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "powerOffOnRuntimeLeaseExpiration", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgVappLease]:
        return typing.cast(typing.Optional[OrgVappLease], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgVappLease]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2311beb7794d465875d8c1d5a048ad642333155305aaedc03b8964057c2f68c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.org.OrgVappTemplateLease",
    jsii_struct_bases=[],
    name_mapping={
        "delete_on_storage_lease_expiration": "deleteOnStorageLeaseExpiration",
        "maximum_storage_lease_in_sec": "maximumStorageLeaseInSec",
    },
)
class OrgVappTemplateLease:
    def __init__(
        self,
        *,
        delete_on_storage_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        maximum_storage_lease_in_sec: jsii.Number,
    ) -> None:
        '''
        :param delete_on_storage_lease_expiration: If true, storage for a vAppTemplate is deleted when the vAppTemplate lease expires. If false, the storage is flagged for deletion, but not deleted Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_on_storage_lease_expiration Org#delete_on_storage_lease_expiration}
        :param maximum_storage_lease_in_sec: How long vApp templates are available before being automatically cleaned up (in seconds). 0 means never expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_storage_lease_in_sec Org#maximum_storage_lease_in_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5f8a1ddab798b135aa18b2877e3a6d7b9eed7b171aa0c73ca3285047182302)
            check_type(argname="argument delete_on_storage_lease_expiration", value=delete_on_storage_lease_expiration, expected_type=type_hints["delete_on_storage_lease_expiration"])
            check_type(argname="argument maximum_storage_lease_in_sec", value=maximum_storage_lease_in_sec, expected_type=type_hints["maximum_storage_lease_in_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delete_on_storage_lease_expiration": delete_on_storage_lease_expiration,
            "maximum_storage_lease_in_sec": maximum_storage_lease_in_sec,
        }

    @builtins.property
    def delete_on_storage_lease_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, storage for a vAppTemplate is deleted when the vAppTemplate lease expires.

        If false, the storage is flagged for deletion, but not deleted

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#delete_on_storage_lease_expiration Org#delete_on_storage_lease_expiration}
        '''
        result = self._values.get("delete_on_storage_lease_expiration")
        assert result is not None, "Required property 'delete_on_storage_lease_expiration' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def maximum_storage_lease_in_sec(self) -> jsii.Number:
        '''How long vApp templates are available before being automatically cleaned up (in seconds). 0 means never expires.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org#maximum_storage_lease_in_sec Org#maximum_storage_lease_in_sec}
        '''
        result = self._values.get("maximum_storage_lease_in_sec")
        assert result is not None, "Required property 'maximum_storage_lease_in_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVappTemplateLease(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVappTemplateLeaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.org.OrgVappTemplateLeaseOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1474d950941939e97a5ef2b838a8fde597a32399d28576bdfb3fb025912b41b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="deleteOnStorageLeaseExpirationInput")
    def delete_on_storage_lease_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteOnStorageLeaseExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumStorageLeaseInSecInput")
    def maximum_storage_lease_in_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumStorageLeaseInSecInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteOnStorageLeaseExpiration")
    def delete_on_storage_lease_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteOnStorageLeaseExpiration"))

    @delete_on_storage_lease_expiration.setter
    def delete_on_storage_lease_expiration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bceb8858f25865d73831548e5599e63aafddf03589c142e12aa33eced53fd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteOnStorageLeaseExpiration", value)

    @builtins.property
    @jsii.member(jsii_name="maximumStorageLeaseInSec")
    def maximum_storage_lease_in_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumStorageLeaseInSec"))

    @maximum_storage_lease_in_sec.setter
    def maximum_storage_lease_in_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06d6ab927d19b6a14ffecd28e8b95f49d6a816fb5a81dc8f4ec071b9f5c6ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumStorageLeaseInSec", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgVappTemplateLease]:
        return typing.cast(typing.Optional[OrgVappTemplateLease], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgVappTemplateLease]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c0e91b3cc2ffc6abeb870355d7dcd29ab6136c493d26dfa0e09b1bb6a8de64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Org",
    "OrgAccountLockout",
    "OrgAccountLockoutOutputReference",
    "OrgConfig",
    "OrgMetadataEntry",
    "OrgMetadataEntryList",
    "OrgMetadataEntryOutputReference",
    "OrgVappLease",
    "OrgVappLeaseOutputReference",
    "OrgVappTemplateLease",
    "OrgVappTemplateLeaseOutputReference",
]

publication.publish()

def _typecheckingstub__da99ee655f8aadf64750aabe0324f281cb06b3c669b44bd0c0a4f5a09232c114(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    full_name: builtins.str,
    name: builtins.str,
    account_lockout: typing.Optional[typing.Union[OrgAccountLockout, typing.Dict[builtins.str, typing.Any]]] = None,
    can_publish_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    can_publish_external_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    can_subscribe_external_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delay_after_power_on_seconds: typing.Optional[jsii.Number] = None,
    delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployed_vm_quota: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stored_vm_quota: typing.Optional[jsii.Number] = None,
    vapp_lease: typing.Optional[typing.Union[OrgVappLease, typing.Dict[builtins.str, typing.Any]]] = None,
    vapp_template_lease: typing.Optional[typing.Union[OrgVappTemplateLease, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f26adc5a49fcae011de6b0dcee35dbbad13a1ace9c922845fcc51b29df6f6a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da05bf8553d40284efe3312a506b7f0095e9447d4550a32d6e45d8aeedcec501(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgMetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394c5233df3baeb6aca66b79093ef78d95ff31c6a9f621f635951e3a64c4df75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbb90c599fa3fd73a5cc0833782f0ae86fe0adabf19910f917c76fbffee20b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9fc36d1316923f968e3bba5c264fe87fe61c3931ed7f675d221d7d2f927e1e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c933ed2548cb963f1082325cd497cf8766ff99ffa26a05b11de2ad149c2b0c71(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f060d64a5146a1f6fce28792ad7a9fa718e4923156eec85abac3795d67a4cebb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2ec11ecb39a2518a91e711de6872cc59f9b6729337733d0428d6d7217f2c0b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19ae47cf0cb674b7f3572ba188582fa9ff86de04cf1118409a5a27f9314b8c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e461bd99563e72331c30568f772e437dd576bc56d4c8cad6e35e6a855420a1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc7e1aae3db18a049d2180ac767595068633748e49427c62b2738d7d97e861a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2eba38c2592c624e26af3e85bac5ef1623f592f6b996f81d5b45aa580cdaa7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9200da0790a65615bfe167c8095097df737769d728763fc7358495cd4e0fa27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83cf513777be540d322d7d596cc54aa16aef727bfd268e7dace93f02c6a27367(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c75feb7984e6bcc911aa7ccd75c197d767ed12d660b08b0b4777a09211bcb53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9096202e548f06839692246ee554c8b1b11c8ee067c37ac19051e700a2c54f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b4cec623c2deb70371386077bc8775f53f0bef5011ff834c7bd35268fb6964(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    invalid_logins_before_lockout: jsii.Number,
    lockout_interval_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0df8d533b6d2bfdda94abbc7ac1b21e86595ccec39b866eddda30c2f08ebc7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc821692eafa7a0aae555e759acc673276b573d5ed46ca95964271b660a2071(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12a05a9d38fcf9c04ae518152d883e53b1e8bca93f1b5371ffedf1751c4ff5b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44e53b41590fb5ac01a2b9d0d68663aba1e18b2e08ed25051eb0d56a9791520(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676772fbf12efc807de2e12a6093b4ce813b52efdd3d7bdf5415b7a617186a38(
    value: typing.Optional[OrgAccountLockout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d1b665c99e15fc1fe19b7dcda30c72ced7d4b2df970f66d7282506ec0c9865(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    full_name: builtins.str,
    name: builtins.str,
    account_lockout: typing.Optional[typing.Union[OrgAccountLockout, typing.Dict[builtins.str, typing.Any]]] = None,
    can_publish_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    can_publish_external_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    can_subscribe_external_catalogs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delay_after_power_on_seconds: typing.Optional[jsii.Number] = None,
    delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployed_vm_quota: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stored_vm_quota: typing.Optional[jsii.Number] = None,
    vapp_lease: typing.Optional[typing.Union[OrgVappLease, typing.Dict[builtins.str, typing.Any]]] = None,
    vapp_template_lease: typing.Optional[typing.Union[OrgVappTemplateLease, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea5d45fda5b015f66cb9c92a16b50f5c5d073404082fafa27841b6710a5c02a(
    *,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34ab83bc6a896c302e0b83ee452798b238c6646d57d5d060ff3335cde5e39ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c6935b9965ae858fdfb4d4b3ef77b6d0e6f41b0615079747ff3e9989e45d63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dece60e3a2d2c93337af0fbb0df50a23120057e153eb8201f240525bf17788e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b879335dfb07abadc96bffb0c3b1843d4379fdf6bb3e35813d3d9e9021876008(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419b0b738c9f9d9916a92de095e3692f0a6f407d3e4837f2d3a6737b3f9c2e8b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3740630763ef9b2bd0354340e7236806361607432f4a8b45fed8303574d1424(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgMetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e589d0d6b9865a68aed9a403dcf001ae8221a4a9effc473a903449fc07a41f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47fa2e5be302590bf11943e670973b87f932bc819fea07aa799ea5a6667363b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe7e03ba834dfb7d727044bce7261bbdafaf44c9c3849fef553df1e26a8a81e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076ffb727f9ad7f78a354e036985f82d8684769ad442b83e71ecb7d233aacc40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41df05e86f5d727b1a385e6bb403cc6395866379da9012e00cabb6ba0ee0a0d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb2db3c9cdeb5cde99c13f50f09a6a79eac1753daf8d9949c62564e8a812d93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__badb775c217aa4dee888102fb6cdfe60caf670fab37d9f6a69437e707be85925(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgMetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297c3602592bfde8ae613de5699c260cad392f93579b933f68753b6447750caa(
    *,
    delete_on_storage_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    maximum_runtime_lease_in_sec: jsii.Number,
    maximum_storage_lease_in_sec: jsii.Number,
    power_off_on_runtime_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20777be09208973702543382392ff7587a13e74d78198cf8756047168e9b401e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b684577ab5d7a533683d4331024e172fa622680b1b47b87644920ef0da8e8979(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba6ea31bfe7b5caddc3806435991f665020714fc00fd19ece29f0983f18d6ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb536641dbc5cc979d533c6fc6a87e72b82c8e4a32c115ead83d6894accc29f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba38dac64458ec0c63f18983cec847074b5a93f28e830fa1897f6f5cdb56d8c4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2311beb7794d465875d8c1d5a048ad642333155305aaedc03b8964057c2f68c0(
    value: typing.Optional[OrgVappLease],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5f8a1ddab798b135aa18b2877e3a6d7b9eed7b171aa0c73ca3285047182302(
    *,
    delete_on_storage_lease_expiration: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    maximum_storage_lease_in_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1474d950941939e97a5ef2b838a8fde597a32399d28576bdfb3fb025912b41b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bceb8858f25865d73831548e5599e63aafddf03589c142e12aa33eced53fd71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06d6ab927d19b6a14ffecd28e8b95f49d6a816fb5a81dc8f4ec071b9f5c6ce8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c0e91b3cc2ffc6abeb870355d7dcd29ab6136c493d26dfa0e09b1bb6a8de64(
    value: typing.Optional[OrgVappTemplateLease],
) -> None:
    """Type checking stubs"""
    pass
