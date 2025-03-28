'''
# `data_vcd_vdc_group`

Refer to the Terraform Registry for docs: [`data_vcd_vdc_group`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group).
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


class DataVcdVdcGroup(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdVdcGroup.DataVcdVdcGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group vcd_vdc_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_policy_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        error_message: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_egress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        network_pool_id: typing.Optional[builtins.str] = None,
        network_pool_universal_id: typing.Optional[builtins.str] = None,
        network_provider_type: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        universal_networking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group vcd_vdc_group} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_policy_status: Default Policy Status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#default_policy_status DataVcdVdcGroup#default_policy_status}
        :param description: VDC group description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#description DataVcdVdcGroup#description}
        :param error_message: More detailed error message when VDC group has error status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#error_message DataVcdVdcGroup#error_message}
        :param id: VDC group ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#id DataVcdVdcGroup#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_egress: Status whether local egress is enabled for a universal router belonging to a universal VDC group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#local_egress DataVcdVdcGroup#local_egress}
        :param name: Name of VDC group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#name DataVcdVdcGroup#name}
        :param network_pool_id: ID of used network pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_pool_id DataVcdVdcGroup#network_pool_id}
        :param network_pool_universal_id: The network provider’s universal id that is backing the universal network pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_pool_universal_id DataVcdVdcGroup#network_pool_universal_id}
        :param network_provider_type: Defines the networking provider backing the VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_provider_type DataVcdVdcGroup#network_provider_type}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#org DataVcdVdcGroup#org}
        :param status: The status that the group can be in (e.g. 'SAVING', 'SAVED', 'CONFIGURING', 'REALIZED', 'REALIZATION_FAILED', 'DELETING', 'DELETE_FAILED', 'OBJECT_NOT_FOUND', 'UNCONFIGURED'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#status DataVcdVdcGroup#status}
        :param type: Defines the group as LOCAL or UNIVERSAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#type DataVcdVdcGroup#type}
        :param universal_networking_enabled: True means that a VDC group router has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#universal_networking_enabled DataVcdVdcGroup#universal_networking_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6eb91859e70345ec83d1f16aa3cfa869e08a9d102a1e729028c930a89846d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataVcdVdcGroupConfig(
            default_policy_status=default_policy_status,
            description=description,
            error_message=error_message,
            id=id,
            local_egress=local_egress,
            name=name,
            network_pool_id=network_pool_id,
            network_pool_universal_id=network_pool_universal_id,
            network_provider_type=network_provider_type,
            org=org,
            status=status,
            type=type,
            universal_networking_enabled=universal_networking_enabled,
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
        '''Generates CDKTF code for importing a DataVcdVdcGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataVcdVdcGroup to import.
        :param import_from_id: The id of the existing DataVcdVdcGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataVcdVdcGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802be1c67c0948c3bb2499d10f516f7b9e5e2e297f88d418157f5db1130d02c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDefaultPolicyStatus")
    def reset_default_policy_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPolicyStatus", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetErrorMessage")
    def reset_error_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorMessage", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocalEgress")
    def reset_local_egress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalEgress", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNetworkPoolId")
    def reset_network_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPoolId", []))

    @jsii.member(jsii_name="resetNetworkPoolUniversalId")
    def reset_network_pool_universal_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPoolUniversalId", []))

    @jsii.member(jsii_name="resetNetworkProviderType")
    def reset_network_provider_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkProviderType", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUniversalNetworkingEnabled")
    def reset_universal_networking_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniversalNetworkingEnabled", []))

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
    @jsii.member(jsii_name="dfwEnabled")
    def dfw_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "dfwEnabled"))

    @builtins.property
    @jsii.member(jsii_name="participatingOrgVdcs")
    def participating_org_vdcs(self) -> "DataVcdVdcGroupParticipatingOrgVdcsList":
        return typing.cast("DataVcdVdcGroupParticipatingOrgVdcsList", jsii.get(self, "participatingOrgVdcs"))

    @builtins.property
    @jsii.member(jsii_name="defaultPolicyStatusInput")
    def default_policy_status_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultPolicyStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="errorMessageInput")
    def error_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localEgressInput")
    def local_egress_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localEgressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPoolIdInput")
    def network_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPoolUniversalIdInput")
    def network_pool_universal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPoolUniversalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="networkProviderTypeInput")
    def network_provider_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkProviderTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="universalNetworkingEnabledInput")
    def universal_networking_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "universalNetworkingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPolicyStatus")
    def default_policy_status(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultPolicyStatus"))

    @default_policy_status.setter
    def default_policy_status(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f905e30a86ad044b8f44a43049f500c2d000e39b17f77cbf4abfa9634d4b8c6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPolicyStatus", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4a4889c21e0c0a55599e228ea817231eb339105a4c3b1f773a7a7bafe7d0e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @error_message.setter
    def error_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236dd6c91d7c1e7700b1ad8651602af9d8acd13ed7bef3e82e79189a93db3e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorMessage", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56465ef0895dd486b3085a6b4d10687bbbc06fb8cff083e00fe8b0a177b5e176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="localEgress")
    def local_egress(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "localEgress"))

    @local_egress.setter
    def local_egress(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a23f757d1763665e6bfd9df5acad4616575971450eab1dd52612491b343e52c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localEgress", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32db89b2685f2f32f6d3259692526b21f8f66863f87809e67cde4e07ca2a6b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkPoolId")
    def network_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPoolId"))

    @network_pool_id.setter
    def network_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8544056ecfea932d04fa71016e155976c29d2560fa05989b272b70e606e1ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="networkPoolUniversalId")
    def network_pool_universal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPoolUniversalId"))

    @network_pool_universal_id.setter
    def network_pool_universal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b238f50e54965fb4bbe1e868d279b2a4672a1c7c78ea1a1db324083ab624c621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPoolUniversalId", value)

    @builtins.property
    @jsii.member(jsii_name="networkProviderType")
    def network_provider_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkProviderType"))

    @network_provider_type.setter
    def network_provider_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08eec335b731a3207cceb200dd5ef0618a7ab8853c9175cd6d76ebf4081e487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkProviderType", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd38e69ffc62df6b32c5d28bc9d7d3441ed3c281610a6d9aa934234300751a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135ba7212930b8cf7cabc8a67460e6f8d356b9a08f9ba41f9be20ef099374cbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b6a77e98bc15f492357390f4847327b5ca41c5d283856ddc89d477baca8d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="universalNetworkingEnabled")
    def universal_networking_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "universalNetworkingEnabled"))

    @universal_networking_enabled.setter
    def universal_networking_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be7356bbc3296b16b2230924eddd8b7791288e1ecc50a3e4c265c14ea9f41c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "universalNetworkingEnabled", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdVdcGroup.DataVcdVdcGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_policy_status": "defaultPolicyStatus",
        "description": "description",
        "error_message": "errorMessage",
        "id": "id",
        "local_egress": "localEgress",
        "name": "name",
        "network_pool_id": "networkPoolId",
        "network_pool_universal_id": "networkPoolUniversalId",
        "network_provider_type": "networkProviderType",
        "org": "org",
        "status": "status",
        "type": "type",
        "universal_networking_enabled": "universalNetworkingEnabled",
    },
)
class DataVcdVdcGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_policy_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        error_message: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_egress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        network_pool_id: typing.Optional[builtins.str] = None,
        network_pool_universal_id: typing.Optional[builtins.str] = None,
        network_provider_type: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        universal_networking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_policy_status: Default Policy Status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#default_policy_status DataVcdVdcGroup#default_policy_status}
        :param description: VDC group description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#description DataVcdVdcGroup#description}
        :param error_message: More detailed error message when VDC group has error status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#error_message DataVcdVdcGroup#error_message}
        :param id: VDC group ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#id DataVcdVdcGroup#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_egress: Status whether local egress is enabled for a universal router belonging to a universal VDC group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#local_egress DataVcdVdcGroup#local_egress}
        :param name: Name of VDC group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#name DataVcdVdcGroup#name}
        :param network_pool_id: ID of used network pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_pool_id DataVcdVdcGroup#network_pool_id}
        :param network_pool_universal_id: The network provider’s universal id that is backing the universal network pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_pool_universal_id DataVcdVdcGroup#network_pool_universal_id}
        :param network_provider_type: Defines the networking provider backing the VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_provider_type DataVcdVdcGroup#network_provider_type}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#org DataVcdVdcGroup#org}
        :param status: The status that the group can be in (e.g. 'SAVING', 'SAVED', 'CONFIGURING', 'REALIZED', 'REALIZATION_FAILED', 'DELETING', 'DELETE_FAILED', 'OBJECT_NOT_FOUND', 'UNCONFIGURED'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#status DataVcdVdcGroup#status}
        :param type: Defines the group as LOCAL or UNIVERSAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#type DataVcdVdcGroup#type}
        :param universal_networking_enabled: True means that a VDC group router has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#universal_networking_enabled DataVcdVdcGroup#universal_networking_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7f745c6f34022c2f38ecb913cf1bd87ba66e6a7ffd62daefd402ae6f05bd7c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_policy_status", value=default_policy_status, expected_type=type_hints["default_policy_status"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local_egress", value=local_egress, expected_type=type_hints["local_egress"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_pool_id", value=network_pool_id, expected_type=type_hints["network_pool_id"])
            check_type(argname="argument network_pool_universal_id", value=network_pool_universal_id, expected_type=type_hints["network_pool_universal_id"])
            check_type(argname="argument network_provider_type", value=network_provider_type, expected_type=type_hints["network_provider_type"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument universal_networking_enabled", value=universal_networking_enabled, expected_type=type_hints["universal_networking_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if default_policy_status is not None:
            self._values["default_policy_status"] = default_policy_status
        if description is not None:
            self._values["description"] = description
        if error_message is not None:
            self._values["error_message"] = error_message
        if id is not None:
            self._values["id"] = id
        if local_egress is not None:
            self._values["local_egress"] = local_egress
        if name is not None:
            self._values["name"] = name
        if network_pool_id is not None:
            self._values["network_pool_id"] = network_pool_id
        if network_pool_universal_id is not None:
            self._values["network_pool_universal_id"] = network_pool_universal_id
        if network_provider_type is not None:
            self._values["network_provider_type"] = network_provider_type
        if org is not None:
            self._values["org"] = org
        if status is not None:
            self._values["status"] = status
        if type is not None:
            self._values["type"] = type
        if universal_networking_enabled is not None:
            self._values["universal_networking_enabled"] = universal_networking_enabled

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
    def default_policy_status(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Default Policy Status.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#default_policy_status DataVcdVdcGroup#default_policy_status}
        '''
        result = self._values.get("default_policy_status")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''VDC group description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#description DataVcdVdcGroup#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_message(self) -> typing.Optional[builtins.str]:
        '''More detailed error message when VDC group has error status.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#error_message DataVcdVdcGroup#error_message}
        '''
        result = self._values.get("error_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''VDC group ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#id DataVcdVdcGroup#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_egress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Status whether local egress is enabled for a universal router belonging to a universal VDC group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#local_egress DataVcdVdcGroup#local_egress}
        '''
        result = self._values.get("local_egress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of VDC group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#name DataVcdVdcGroup#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_pool_id(self) -> typing.Optional[builtins.str]:
        '''ID of used network pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_pool_id DataVcdVdcGroup#network_pool_id}
        '''
        result = self._values.get("network_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_pool_universal_id(self) -> typing.Optional[builtins.str]:
        '''The network provider’s universal id that is backing the universal network pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_pool_universal_id DataVcdVdcGroup#network_pool_universal_id}
        '''
        result = self._values.get("network_pool_universal_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_provider_type(self) -> typing.Optional[builtins.str]:
        '''Defines the networking provider backing the VDC Group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#network_provider_type DataVcdVdcGroup#network_provider_type}
        '''
        result = self._values.get("network_provider_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#org DataVcdVdcGroup#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status that the group can be in (e.g. 'SAVING', 'SAVED', 'CONFIGURING', 'REALIZED', 'REALIZATION_FAILED', 'DELETING', 'DELETE_FAILED', 'OBJECT_NOT_FOUND', 'UNCONFIGURED').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#status DataVcdVdcGroup#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Defines the group as LOCAL or UNIVERSAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#type DataVcdVdcGroup#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def universal_networking_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True means that a VDC group router has been created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/vdc_group#universal_networking_enabled DataVcdVdcGroup#universal_networking_enabled}
        '''
        result = self._values.get("universal_networking_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdVdcGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.dataVcdVdcGroup.DataVcdVdcGroupParticipatingOrgVdcs",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdVdcGroupParticipatingOrgVdcs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdVdcGroupParticipatingOrgVdcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdVdcGroupParticipatingOrgVdcsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdVdcGroup.DataVcdVdcGroupParticipatingOrgVdcsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__594edf71940088ebf31406ced951c774a37fd43b5ab3d292862872c1aeaaf2d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdVdcGroupParticipatingOrgVdcsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baabd6e269cfea76c6921cbba962b4e7175531a1dcc888ca48d2da9a1436ac4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdVdcGroupParticipatingOrgVdcsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf40d9bf5b7361af554538adf8d169098706eef8a25dc51d9f71ede2685148d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b535cea05f81f91b83f3c413d11657251d3417f3f5ea2949c2e1df7008e074c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57fc2b3464a577b591227ae822deab22377ec7cc4406d722cac100b42b0f78bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdVdcGroupParticipatingOrgVdcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdVdcGroup.DataVcdVdcGroupParticipatingOrgVdcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17967df1cd660b04d9c888753698b7a78bff223d8f494bac951dc3a44df5e468)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="faultDomainTag")
    def fault_domain_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faultDomainTag"))

    @builtins.property
    @jsii.member(jsii_name="isRemoteOrg")
    def is_remote_org(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isRemoteOrg"))

    @builtins.property
    @jsii.member(jsii_name="networkProviderScope")
    def network_provider_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkProviderScope"))

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @builtins.property
    @jsii.member(jsii_name="orgName")
    def org_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgName"))

    @builtins.property
    @jsii.member(jsii_name="siteId")
    def site_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "siteId"))

    @builtins.property
    @jsii.member(jsii_name="siteName")
    def site_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "siteName"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="vdcId")
    def vdc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcId"))

    @builtins.property
    @jsii.member(jsii_name="vdcName")
    def vdc_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataVcdVdcGroupParticipatingOrgVdcs]:
        return typing.cast(typing.Optional[DataVcdVdcGroupParticipatingOrgVdcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdVdcGroupParticipatingOrgVdcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b329fef56260e128694c1abd28d971776ef95ce08b6fb6181f1ff5a1d99ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataVcdVdcGroup",
    "DataVcdVdcGroupConfig",
    "DataVcdVdcGroupParticipatingOrgVdcs",
    "DataVcdVdcGroupParticipatingOrgVdcsList",
    "DataVcdVdcGroupParticipatingOrgVdcsOutputReference",
]

publication.publish()

def _typecheckingstub__0d6eb91859e70345ec83d1f16aa3cfa869e08a9d102a1e729028c930a89846d0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_policy_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    error_message: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_egress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    network_pool_id: typing.Optional[builtins.str] = None,
    network_pool_universal_id: typing.Optional[builtins.str] = None,
    network_provider_type: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    universal_networking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__802be1c67c0948c3bb2499d10f516f7b9e5e2e297f88d418157f5db1130d02c3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f905e30a86ad044b8f44a43049f500c2d000e39b17f77cbf4abfa9634d4b8c6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4a4889c21e0c0a55599e228ea817231eb339105a4c3b1f773a7a7bafe7d0e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236dd6c91d7c1e7700b1ad8651602af9d8acd13ed7bef3e82e79189a93db3e55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56465ef0895dd486b3085a6b4d10687bbbc06fb8cff083e00fe8b0a177b5e176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a23f757d1763665e6bfd9df5acad4616575971450eab1dd52612491b343e52c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32db89b2685f2f32f6d3259692526b21f8f66863f87809e67cde4e07ca2a6b82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8544056ecfea932d04fa71016e155976c29d2560fa05989b272b70e606e1ce1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b238f50e54965fb4bbe1e868d279b2a4672a1c7c78ea1a1db324083ab624c621(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08eec335b731a3207cceb200dd5ef0618a7ab8853c9175cd6d76ebf4081e487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd38e69ffc62df6b32c5d28bc9d7d3441ed3c281610a6d9aa934234300751a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135ba7212930b8cf7cabc8a67460e6f8d356b9a08f9ba41f9be20ef099374cbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b6a77e98bc15f492357390f4847327b5ca41c5d283856ddc89d477baca8d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be7356bbc3296b16b2230924eddd8b7791288e1ecc50a3e4c265c14ea9f41c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7f745c6f34022c2f38ecb913cf1bd87ba66e6a7ffd62daefd402ae6f05bd7c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_policy_status: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    error_message: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_egress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    network_pool_id: typing.Optional[builtins.str] = None,
    network_pool_universal_id: typing.Optional[builtins.str] = None,
    network_provider_type: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    universal_networking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594edf71940088ebf31406ced951c774a37fd43b5ab3d292862872c1aeaaf2d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baabd6e269cfea76c6921cbba962b4e7175531a1dcc888ca48d2da9a1436ac4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf40d9bf5b7361af554538adf8d169098706eef8a25dc51d9f71ede2685148d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b535cea05f81f91b83f3c413d11657251d3417f3f5ea2949c2e1df7008e074c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fc2b3464a577b591227ae822deab22377ec7cc4406d722cac100b42b0f78bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17967df1cd660b04d9c888753698b7a78bff223d8f494bac951dc3a44df5e468(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b329fef56260e128694c1abd28d971776ef95ce08b6fb6181f1ff5a1d99ae1(
    value: typing.Optional[DataVcdVdcGroupParticipatingOrgVdcs],
) -> None:
    """Type checking stubs"""
    pass
