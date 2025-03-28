'''
# `vcd_vapp_nat_rules`

Refer to the Terraform Registry for docs: [`vcd_vapp_nat_rules`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules).
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


class VappNatRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappNatRules.VappNatRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules vcd_vapp_nat_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        nat_type: builtins.str,
        network_id: builtins.str,
        vapp_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ip_masquerade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNatRulesRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules vcd_vapp_nat_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param nat_type: One of: ``ipTranslation`` (use IP translation), ``portForwarding`` (use port forwarding). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#nat_type VappNatRules#nat_type}
        :param network_id: vApp network identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#network_id VappNatRules#network_id}
        :param vapp_id: vApp identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vapp_id VappNatRules#vapp_id}
        :param enabled: Enable or disable NAT service. Default is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#enabled VappNatRules#enabled}
        :param enable_ip_masquerade: When enabled translates a virtual machine's private, internal IP address to a public IP address for outbound traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#enable_ip_masquerade VappNatRules#enable_ip_masquerade}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#id VappNatRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#org VappNatRules#org}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#rule VappNatRules#rule}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vdc VappNatRules#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9ffa76038f3005fa7b8df79583f1f7120fd1fcc122d266601308fc92054b1c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VappNatRulesConfig(
            nat_type=nat_type,
            network_id=network_id,
            vapp_id=vapp_id,
            enabled=enabled,
            enable_ip_masquerade=enable_ip_masquerade,
            id=id,
            org=org,
            rule=rule,
            vdc=vdc,
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
        '''Generates CDKTF code for importing a VappNatRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VappNatRules to import.
        :param import_from_id: The id of the existing VappNatRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VappNatRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652cc3b2d454be02868269f96dec8f2807a672b00f35b1d3fbec26dc710797d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNatRulesRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7afcf83d85ec71056196add783f207f75c038fe47a1803ebbf9e7850491456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnableIpMasquerade")
    def reset_enable_ip_masquerade(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIpMasquerade", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @jsii.member(jsii_name="resetVdc")
    def reset_vdc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdc", []))

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
    @jsii.member(jsii_name="rule")
    def rule(self) -> "VappNatRulesRuleList":
        return typing.cast("VappNatRulesRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIpMasqueradeInput")
    def enable_ip_masquerade_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIpMasqueradeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="natTypeInput")
    def nat_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "natTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNatRulesRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNatRulesRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="vappIdInput")
    def vapp_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vappIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2522327d7e4dad551e2f6032e1af401ba0cbe815d5ebbd1c2ab1ae2c3c219190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="enableIpMasquerade")
    def enable_ip_masquerade(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIpMasquerade"))

    @enable_ip_masquerade.setter
    def enable_ip_masquerade(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f11f054ba13d125f54932421a7113517efb9ed4bda67e9f1bbbe58ef193691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpMasquerade", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3d9d42dc8e5468f4cbb97b43b2d466d5fc54ccf74b5d9313748d0a6d71227b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="natType")
    def nat_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natType"))

    @nat_type.setter
    def nat_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6692aa2b00093e0abe63d604975053cf6e6864b6dc803643e2c836db3235a404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natType", value)

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40be8651db24aafa0c58a4f9ec3a2cc3167614448c9d12cde5bc9522b8fb619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eaa245834afc349e746e16771db869fe7f97a8bcd9bf7a8e076b02cb51900a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="vappId")
    def vapp_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappId"))

    @vapp_id.setter
    def vapp_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414a24ad7cad628b63ac3a2ea5ccd621f9d752d7213028c1e5113247bb0b863a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappId", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2428cdf45d5671750bd5f4051fadbccf0ff858d845f3212f43d6f14127d8197a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.vappNatRules.VappNatRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "nat_type": "natType",
        "network_id": "networkId",
        "vapp_id": "vappId",
        "enabled": "enabled",
        "enable_ip_masquerade": "enableIpMasquerade",
        "id": "id",
        "org": "org",
        "rule": "rule",
        "vdc": "vdc",
    },
)
class VappNatRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        nat_type: builtins.str,
        network_id: builtins.str,
        vapp_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ip_masquerade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNatRulesRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vdc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param nat_type: One of: ``ipTranslation`` (use IP translation), ``portForwarding`` (use port forwarding). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#nat_type VappNatRules#nat_type}
        :param network_id: vApp network identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#network_id VappNatRules#network_id}
        :param vapp_id: vApp identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vapp_id VappNatRules#vapp_id}
        :param enabled: Enable or disable NAT service. Default is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#enabled VappNatRules#enabled}
        :param enable_ip_masquerade: When enabled translates a virtual machine's private, internal IP address to a public IP address for outbound traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#enable_ip_masquerade VappNatRules#enable_ip_masquerade}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#id VappNatRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#org VappNatRules#org}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#rule VappNatRules#rule}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vdc VappNatRules#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ae5a914ed14f6c2e76e78c89a620e9f423f740fb77e9d288f16b0dabfa500c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument nat_type", value=nat_type, expected_type=type_hints["nat_type"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument vapp_id", value=vapp_id, expected_type=type_hints["vapp_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_ip_masquerade", value=enable_ip_masquerade, expected_type=type_hints["enable_ip_masquerade"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "nat_type": nat_type,
            "network_id": network_id,
            "vapp_id": vapp_id,
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
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_ip_masquerade is not None:
            self._values["enable_ip_masquerade"] = enable_ip_masquerade
        if id is not None:
            self._values["id"] = id
        if org is not None:
            self._values["org"] = org
        if rule is not None:
            self._values["rule"] = rule
        if vdc is not None:
            self._values["vdc"] = vdc

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
    def nat_type(self) -> builtins.str:
        '''One of: ``ipTranslation`` (use IP translation), ``portForwarding`` (use port forwarding).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#nat_type VappNatRules#nat_type}
        '''
        result = self._values.get("nat_type")
        assert result is not None, "Required property 'nat_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_id(self) -> builtins.str:
        '''vApp network identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#network_id VappNatRules#network_id}
        '''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vapp_id(self) -> builtins.str:
        '''vApp identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vapp_id VappNatRules#vapp_id}
        '''
        result = self._values.get("vapp_id")
        assert result is not None, "Required property 'vapp_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable NAT service. Default is ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#enabled VappNatRules#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_ip_masquerade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled translates a virtual machine's private, internal IP address to a public IP address for outbound traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#enable_ip_masquerade VappNatRules#enable_ip_masquerade}
        '''
        result = self._values.get("enable_ip_masquerade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#id VappNatRules#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#org VappNatRules#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNatRulesRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#rule VappNatRules#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNatRulesRule"]]], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vdc VappNatRules#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappNatRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.vappNatRules.VappNatRulesRule",
    jsii_struct_bases=[],
    name_mapping={
        "vm_id": "vmId",
        "vm_nic_id": "vmNicId",
        "external_ip": "externalIp",
        "external_port": "externalPort",
        "forward_to_port": "forwardToPort",
        "mapping_mode": "mappingMode",
        "protocol": "protocol",
    },
)
class VappNatRulesRule:
    def __init__(
        self,
        *,
        vm_id: builtins.str,
        vm_nic_id: jsii.Number,
        external_ip: typing.Optional[builtins.str] = None,
        external_port: typing.Optional[jsii.Number] = None,
        forward_to_port: typing.Optional[jsii.Number] = None,
        mapping_mode: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vm_id: VM to which this rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vm_id VappNatRules#vm_id}
        :param vm_nic_id: VM NIC ID to which this rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vm_nic_id VappNatRules#vm_nic_id}
        :param external_ip: External IP address to forward to or External IP address to map to VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#external_ip VappNatRules#external_ip}
        :param external_port: External port to forward. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#external_port VappNatRules#external_port}
        :param forward_to_port: Internal port to forward. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#forward_to_port VappNatRules#forward_to_port}
        :param mapping_mode: Mapping mode. One of: ``automatic``, ``manual``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#mapping_mode VappNatRules#mapping_mode}
        :param protocol: Protocol to forward. One of: ``TCP`` (forward TCP packets), ``UDP`` (forward UDP packets), ``TCP_UDP`` (forward TCP and UDP packets). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#protocol VappNatRules#protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622a550165448dcc8fd52bd055c8920ef32349bc7d4b1de46ee49d29e466ebf1)
            check_type(argname="argument vm_id", value=vm_id, expected_type=type_hints["vm_id"])
            check_type(argname="argument vm_nic_id", value=vm_nic_id, expected_type=type_hints["vm_nic_id"])
            check_type(argname="argument external_ip", value=external_ip, expected_type=type_hints["external_ip"])
            check_type(argname="argument external_port", value=external_port, expected_type=type_hints["external_port"])
            check_type(argname="argument forward_to_port", value=forward_to_port, expected_type=type_hints["forward_to_port"])
            check_type(argname="argument mapping_mode", value=mapping_mode, expected_type=type_hints["mapping_mode"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vm_id": vm_id,
            "vm_nic_id": vm_nic_id,
        }
        if external_ip is not None:
            self._values["external_ip"] = external_ip
        if external_port is not None:
            self._values["external_port"] = external_port
        if forward_to_port is not None:
            self._values["forward_to_port"] = forward_to_port
        if mapping_mode is not None:
            self._values["mapping_mode"] = mapping_mode
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def vm_id(self) -> builtins.str:
        '''VM to which this rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vm_id VappNatRules#vm_id}
        '''
        result = self._values.get("vm_id")
        assert result is not None, "Required property 'vm_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_nic_id(self) -> jsii.Number:
        '''VM NIC ID to which this rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#vm_nic_id VappNatRules#vm_nic_id}
        '''
        result = self._values.get("vm_nic_id")
        assert result is not None, "Required property 'vm_nic_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def external_ip(self) -> typing.Optional[builtins.str]:
        '''External IP address to forward to or External IP address to map to VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#external_ip VappNatRules#external_ip}
        '''
        result = self._values.get("external_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_port(self) -> typing.Optional[jsii.Number]:
        '''External port to forward.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#external_port VappNatRules#external_port}
        '''
        result = self._values.get("external_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def forward_to_port(self) -> typing.Optional[jsii.Number]:
        '''Internal port to forward.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#forward_to_port VappNatRules#forward_to_port}
        '''
        result = self._values.get("forward_to_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mapping_mode(self) -> typing.Optional[builtins.str]:
        '''Mapping mode. One of: ``automatic``, ``manual``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#mapping_mode VappNatRules#mapping_mode}
        '''
        result = self._values.get("mapping_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Protocol to forward. One of: ``TCP`` (forward TCP packets), ``UDP`` (forward UDP packets), ``TCP_UDP`` (forward TCP and UDP packets).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_nat_rules#protocol VappNatRules#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappNatRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappNatRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappNatRules.VappNatRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4ed8a416bf84d82b43d5862fda16a3d55843943dec621b7369d17cc8faeaac9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappNatRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b773635f8f9645f5836b166ed7435730d21c1b72bfa0b9520d917ae7c3da1e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappNatRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc24780bdb2c1b960114a8c20224895c8b37acbf092e03e23f7cd6fb3845b31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01a20ab1a233280f0a3b5a5783309353e7892d89047574453ba7231c7ca1a1eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54d95f2946c8ba3ab2fd07b7fb15d7f22cab84a29fc3963d4fe9011c11379ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNatRulesRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNatRulesRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNatRulesRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d7b17743a7b1d430db9a8407f4b800b01d0260dc01fe2f9e2a63548bd3cbb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappNatRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappNatRules.VappNatRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__410cb19ab77ee18f591cf9c86813e2ba00794b50b3e4a74c31a750eb6800566f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExternalIp")
    def reset_external_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalIp", []))

    @jsii.member(jsii_name="resetExternalPort")
    def reset_external_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalPort", []))

    @jsii.member(jsii_name="resetForwardToPort")
    def reset_forward_to_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardToPort", []))

    @jsii.member(jsii_name="resetMappingMode")
    def reset_mapping_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingMode", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="externalIpInput")
    def external_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="externalPortInput")
    def external_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalPortInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardToPortInput")
    def forward_to_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "forwardToPortInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingModeInput")
    def mapping_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="vmIdInput")
    def vm_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vmNicIdInput")
    def vm_nic_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmNicIdInput"))

    @builtins.property
    @jsii.member(jsii_name="externalIp")
    def external_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIp"))

    @external_ip.setter
    def external_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e05a9239b07af0285902be14353b9fb9291179d74b4d24976e41e0cd540aa23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIp", value)

    @builtins.property
    @jsii.member(jsii_name="externalPort")
    def external_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalPort"))

    @external_port.setter
    def external_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c9d45386c7e383a4dd1e763cb3611975f601ccfc638ff312c5bf33981047b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalPort", value)

    @builtins.property
    @jsii.member(jsii_name="forwardToPort")
    def forward_to_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "forwardToPort"))

    @forward_to_port.setter
    def forward_to_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1e143c8d5f95738a840e454794b330070eea4f101ecc5271cdb833384ae5ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardToPort", value)

    @builtins.property
    @jsii.member(jsii_name="mappingMode")
    def mapping_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mappingMode"))

    @mapping_mode.setter
    def mapping_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb36e13f79f00c97011436e722635db8e31fe684e58f9b374ba93578bba979c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappingMode", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ad0fb39b2a61766d1dd4edfda3d3f465244493fbf0c9cf5881c95476bcd064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="vmId")
    def vm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmId"))

    @vm_id.setter
    def vm_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630be4fc77f209e75f467b7ee59eec5f8074ed676cd382f9b60ace83d687d73b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmId", value)

    @builtins.property
    @jsii.member(jsii_name="vmNicId")
    def vm_nic_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmNicId"))

    @vm_nic_id.setter
    def vm_nic_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44360c8fde140150db8fbc1b3efd0958118158cf892bf2e5ab154dd6a50c6dcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmNicId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNatRulesRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNatRulesRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNatRulesRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6c09761ecc9b35d08332692f155d86e41cfb651041bf25b447e4a45640edfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VappNatRules",
    "VappNatRulesConfig",
    "VappNatRulesRule",
    "VappNatRulesRuleList",
    "VappNatRulesRuleOutputReference",
]

publication.publish()

def _typecheckingstub__0d9ffa76038f3005fa7b8df79583f1f7120fd1fcc122d266601308fc92054b1c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    nat_type: builtins.str,
    network_id: builtins.str,
    vapp_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ip_masquerade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNatRulesRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vdc: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__652cc3b2d454be02868269f96dec8f2807a672b00f35b1d3fbec26dc710797d2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7afcf83d85ec71056196add783f207f75c038fe47a1803ebbf9e7850491456(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNatRulesRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2522327d7e4dad551e2f6032e1af401ba0cbe815d5ebbd1c2ab1ae2c3c219190(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f11f054ba13d125f54932421a7113517efb9ed4bda67e9f1bbbe58ef193691(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3d9d42dc8e5468f4cbb97b43b2d466d5fc54ccf74b5d9313748d0a6d71227b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6692aa2b00093e0abe63d604975053cf6e6864b6dc803643e2c836db3235a404(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40be8651db24aafa0c58a4f9ec3a2cc3167614448c9d12cde5bc9522b8fb619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eaa245834afc349e746e16771db869fe7f97a8bcd9bf7a8e076b02cb51900a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414a24ad7cad628b63ac3a2ea5ccd621f9d752d7213028c1e5113247bb0b863a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2428cdf45d5671750bd5f4051fadbccf0ff858d845f3212f43d6f14127d8197a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ae5a914ed14f6c2e76e78c89a620e9f423f740fb77e9d288f16b0dabfa500c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nat_type: builtins.str,
    network_id: builtins.str,
    vapp_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ip_masquerade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNatRulesRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622a550165448dcc8fd52bd055c8920ef32349bc7d4b1de46ee49d29e466ebf1(
    *,
    vm_id: builtins.str,
    vm_nic_id: jsii.Number,
    external_ip: typing.Optional[builtins.str] = None,
    external_port: typing.Optional[jsii.Number] = None,
    forward_to_port: typing.Optional[jsii.Number] = None,
    mapping_mode: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ed8a416bf84d82b43d5862fda16a3d55843943dec621b7369d17cc8faeaac9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b773635f8f9645f5836b166ed7435730d21c1b72bfa0b9520d917ae7c3da1e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc24780bdb2c1b960114a8c20224895c8b37acbf092e03e23f7cd6fb3845b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a20ab1a233280f0a3b5a5783309353e7892d89047574453ba7231c7ca1a1eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d95f2946c8ba3ab2fd07b7fb15d7f22cab84a29fc3963d4fe9011c11379ab0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d7b17743a7b1d430db9a8407f4b800b01d0260dc01fe2f9e2a63548bd3cbb6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNatRulesRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410cb19ab77ee18f591cf9c86813e2ba00794b50b3e4a74c31a750eb6800566f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e05a9239b07af0285902be14353b9fb9291179d74b4d24976e41e0cd540aa23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c9d45386c7e383a4dd1e763cb3611975f601ccfc638ff312c5bf33981047b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1e143c8d5f95738a840e454794b330070eea4f101ecc5271cdb833384ae5ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb36e13f79f00c97011436e722635db8e31fe684e58f9b374ba93578bba979c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ad0fb39b2a61766d1dd4edfda3d3f465244493fbf0c9cf5881c95476bcd064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630be4fc77f209e75f467b7ee59eec5f8074ed676cd382f9b60ace83d687d73b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44360c8fde140150db8fbc1b3efd0958118158cf892bf2e5ab154dd6a50c6dcb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6c09761ecc9b35d08332692f155d86e41cfb651041bf25b447e4a45640edfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNatRulesRule]],
) -> None:
    """Type checking stubs"""
    pass
