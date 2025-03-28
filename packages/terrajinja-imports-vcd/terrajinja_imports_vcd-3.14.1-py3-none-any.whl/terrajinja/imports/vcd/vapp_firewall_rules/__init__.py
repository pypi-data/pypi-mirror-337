'''
# `vcd_vapp_firewall_rules`

Refer to the Terraform Registry for docs: [`vcd_vapp_firewall_rules`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules).
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


class VappFirewallRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappFirewallRules.VappFirewallRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules vcd_vapp_firewall_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_action: builtins.str,
        network_id: builtins.str,
        vapp_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        log_default_action: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappFirewallRulesRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules vcd_vapp_firewall_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_action: Specifies what to do should none of the rules match. Either ``allow`` or ``drop``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#default_action VappFirewallRules#default_action}
        :param network_id: vApp network identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#network_id VappFirewallRules#network_id}
        :param vapp_id: vApp identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#vapp_id VappFirewallRules#vapp_id}
        :param enabled: Enable or disable firewall service. Default is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#enabled VappFirewallRules#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#id VappFirewallRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_default_action: Flag to enable logging for default action. Default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#log_default_action VappFirewallRules#log_default_action}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#org VappFirewallRules#org}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#rule VappFirewallRules#rule}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#vdc VappFirewallRules#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85e688bc0f4b4d74e6dcd1af41d8a0b1d3023ab5422b6cac2cf07324e3ce58d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VappFirewallRulesConfig(
            default_action=default_action,
            network_id=network_id,
            vapp_id=vapp_id,
            enabled=enabled,
            id=id,
            log_default_action=log_default_action,
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
        '''Generates CDKTF code for importing a VappFirewallRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VappFirewallRules to import.
        :param import_from_id: The id of the existing VappFirewallRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VappFirewallRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a261fbe7decc09e6918ff41fc0171ab6c78ff41f7ac3f68dbb5264b9446bc79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappFirewallRulesRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4601934c93e5f507b66dc554a52232b66d09d2ec664cd1cee008cac2878406fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogDefaultAction")
    def reset_log_default_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDefaultAction", []))

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
    def rule(self) -> "VappFirewallRulesRuleList":
        return typing.cast("VappFirewallRulesRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionInput")
    def default_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logDefaultActionInput")
    def log_default_action_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logDefaultActionInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappFirewallRulesRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappFirewallRulesRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="vappIdInput")
    def vapp_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vappIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAction")
    def default_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda4feb18b69645a0d021a373d44b1944b38ce92803206c6854f520acc95a3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAction", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__8458e4bf8b0ae83c4941f3b54a56d2c21c3b5c62cc5d577e571783c5eed6f24b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17f70a9f119b6e47275bffc2954dbe99a50f4aa4b575dad657846a8a6e0142a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="logDefaultAction")
    def log_default_action(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logDefaultAction"))

    @log_default_action.setter
    def log_default_action(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09dd31b6da05fc4620c36ff3a9a45dc82025d57b56a0f0b3204a19e2e79fd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDefaultAction", value)

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3196406852683f15df88f2fed3404bea7d9434b58a1552b487cfc0d92a801a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a40c3845f2ca4472386cbeb412fead69e56345ce118b14cd04260b1b1fbd64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="vappId")
    def vapp_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappId"))

    @vapp_id.setter
    def vapp_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5ad0b17e5cdb00dc22159a2fd35851b0a1a8c76517fb8951588be7bef27817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappId", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0808d696c8d27c4a1beaa73a367e043be7d286b66dd3f8161393bb183a359b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.vappFirewallRules.VappFirewallRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_action": "defaultAction",
        "network_id": "networkId",
        "vapp_id": "vappId",
        "enabled": "enabled",
        "id": "id",
        "log_default_action": "logDefaultAction",
        "org": "org",
        "rule": "rule",
        "vdc": "vdc",
    },
)
class VappFirewallRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_action: builtins.str,
        network_id: builtins.str,
        vapp_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        log_default_action: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappFirewallRulesRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param default_action: Specifies what to do should none of the rules match. Either ``allow`` or ``drop``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#default_action VappFirewallRules#default_action}
        :param network_id: vApp network identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#network_id VappFirewallRules#network_id}
        :param vapp_id: vApp identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#vapp_id VappFirewallRules#vapp_id}
        :param enabled: Enable or disable firewall service. Default is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#enabled VappFirewallRules#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#id VappFirewallRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_default_action: Flag to enable logging for default action. Default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#log_default_action VappFirewallRules#log_default_action}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#org VappFirewallRules#org}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#rule VappFirewallRules#rule}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#vdc VappFirewallRules#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d402f8af2b7e9bffa51d138ab880edad18f6bcac9bceb9edb970c2cce95707)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument vapp_id", value=vapp_id, expected_type=type_hints["vapp_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_default_action", value=log_default_action, expected_type=type_hints["log_default_action"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
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
        if id is not None:
            self._values["id"] = id
        if log_default_action is not None:
            self._values["log_default_action"] = log_default_action
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
    def default_action(self) -> builtins.str:
        '''Specifies what to do should none of the rules match. Either ``allow`` or ``drop``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#default_action VappFirewallRules#default_action}
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_id(self) -> builtins.str:
        '''vApp network identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#network_id VappFirewallRules#network_id}
        '''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vapp_id(self) -> builtins.str:
        '''vApp identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#vapp_id VappFirewallRules#vapp_id}
        '''
        result = self._values.get("vapp_id")
        assert result is not None, "Required property 'vapp_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable firewall service. Default is ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#enabled VappFirewallRules#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#id VappFirewallRules#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_default_action(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag to enable logging for default action. Default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#log_default_action VappFirewallRules#log_default_action}
        '''
        result = self._values.get("log_default_action")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#org VappFirewallRules#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappFirewallRulesRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#rule VappFirewallRules#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappFirewallRulesRule"]]], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#vdc VappFirewallRules#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappFirewallRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.vappFirewallRules.VappFirewallRulesRule",
    jsii_struct_bases=[],
    name_mapping={
        "destination_ip": "destinationIp",
        "destination_port": "destinationPort",
        "destination_vm_id": "destinationVmId",
        "destination_vm_ip_type": "destinationVmIpType",
        "destination_vm_nic_id": "destinationVmNicId",
        "enabled": "enabled",
        "enable_logging": "enableLogging",
        "name": "name",
        "policy": "policy",
        "protocol": "protocol",
        "source_ip": "sourceIp",
        "source_port": "sourcePort",
        "source_vm_id": "sourceVmId",
        "source_vm_ip_type": "sourceVmIpType",
        "source_vm_nic_id": "sourceVmNicId",
    },
)
class VappFirewallRulesRule:
    def __init__(
        self,
        *,
        destination_ip: typing.Optional[builtins.str] = None,
        destination_port: typing.Optional[builtins.str] = None,
        destination_vm_id: typing.Optional[builtins.str] = None,
        destination_vm_ip_type: typing.Optional[builtins.str] = None,
        destination_vm_nic_id: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        source_ip: typing.Optional[builtins.str] = None,
        source_port: typing.Optional[builtins.str] = None,
        source_vm_id: typing.Optional[builtins.str] = None,
        source_vm_ip_type: typing.Optional[builtins.str] = None,
        source_vm_nic_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param destination_ip: Destination IP address to which the rule applies. A value of ``Any`` matches any IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_ip VappFirewallRules#destination_ip}
        :param destination_port: Destination port to which this rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_port VappFirewallRules#destination_port}
        :param destination_vm_id: Destination VM identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_vm_id VappFirewallRules#destination_vm_id}
        :param destination_vm_ip_type: The value can be one of: ``assigned`` - assigned internal IP will be automatically chosen. ``NAT``: NATed external IP will be automatically chosen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_vm_ip_type VappFirewallRules#destination_vm_ip_type}
        :param destination_vm_nic_id: Destination VM NIC ID to which this rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_vm_nic_id VappFirewallRules#destination_vm_nic_id}
        :param enabled: 'true' value will enable firewall rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#enabled VappFirewallRules#enabled}
        :param enable_logging: 'true' value will enable rule logging. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#enable_logging VappFirewallRules#enable_logging}
        :param name: Rule name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#name VappFirewallRules#name}
        :param policy: One of: ``drop`` (drop packets that match the rule), ``allow`` (allow packets that match the rule to pass through the firewall). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#policy VappFirewallRules#policy}
        :param protocol: Specify the protocols to which the rule should be applied. One of: ``any``, ``icmp``, ``tcp``, ``udp``, ``tcp&udp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#protocol VappFirewallRules#protocol}
        :param source_ip: Source IP address to which the rule applies. A value of ``Any`` matches any IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_ip VappFirewallRules#source_ip}
        :param source_port: Source port to which this rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_port VappFirewallRules#source_port}
        :param source_vm_id: Source VM identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_vm_id VappFirewallRules#source_vm_id}
        :param source_vm_ip_type: The value can be one of: ``assigned`` - assigned internal IP will be automatically chosen. ``NAT``: NATed external IP will be automatically chosen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_vm_ip_type VappFirewallRules#source_vm_ip_type}
        :param source_vm_nic_id: Source VM NIC ID to which this rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_vm_nic_id VappFirewallRules#source_vm_nic_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b70be0bf1ceaae0a932746617c0f51bf4792da654bddfecc8fd92ca794f7dad)
            check_type(argname="argument destination_ip", value=destination_ip, expected_type=type_hints["destination_ip"])
            check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
            check_type(argname="argument destination_vm_id", value=destination_vm_id, expected_type=type_hints["destination_vm_id"])
            check_type(argname="argument destination_vm_ip_type", value=destination_vm_ip_type, expected_type=type_hints["destination_vm_ip_type"])
            check_type(argname="argument destination_vm_nic_id", value=destination_vm_nic_id, expected_type=type_hints["destination_vm_nic_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument source_ip", value=source_ip, expected_type=type_hints["source_ip"])
            check_type(argname="argument source_port", value=source_port, expected_type=type_hints["source_port"])
            check_type(argname="argument source_vm_id", value=source_vm_id, expected_type=type_hints["source_vm_id"])
            check_type(argname="argument source_vm_ip_type", value=source_vm_ip_type, expected_type=type_hints["source_vm_ip_type"])
            check_type(argname="argument source_vm_nic_id", value=source_vm_nic_id, expected_type=type_hints["source_vm_nic_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_ip is not None:
            self._values["destination_ip"] = destination_ip
        if destination_port is not None:
            self._values["destination_port"] = destination_port
        if destination_vm_id is not None:
            self._values["destination_vm_id"] = destination_vm_id
        if destination_vm_ip_type is not None:
            self._values["destination_vm_ip_type"] = destination_vm_ip_type
        if destination_vm_nic_id is not None:
            self._values["destination_vm_nic_id"] = destination_vm_nic_id
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if protocol is not None:
            self._values["protocol"] = protocol
        if source_ip is not None:
            self._values["source_ip"] = source_ip
        if source_port is not None:
            self._values["source_port"] = source_port
        if source_vm_id is not None:
            self._values["source_vm_id"] = source_vm_id
        if source_vm_ip_type is not None:
            self._values["source_vm_ip_type"] = source_vm_ip_type
        if source_vm_nic_id is not None:
            self._values["source_vm_nic_id"] = source_vm_nic_id

    @builtins.property
    def destination_ip(self) -> typing.Optional[builtins.str]:
        '''Destination IP address to which the rule applies. A value of ``Any`` matches any IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_ip VappFirewallRules#destination_ip}
        '''
        result = self._values.get("destination_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_port(self) -> typing.Optional[builtins.str]:
        '''Destination port to which this rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_port VappFirewallRules#destination_port}
        '''
        result = self._values.get("destination_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_vm_id(self) -> typing.Optional[builtins.str]:
        '''Destination VM identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_vm_id VappFirewallRules#destination_vm_id}
        '''
        result = self._values.get("destination_vm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_vm_ip_type(self) -> typing.Optional[builtins.str]:
        '''The value can be one of: ``assigned`` - assigned internal IP will be automatically chosen.

        ``NAT``: NATed external IP will be automatically chosen.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_vm_ip_type VappFirewallRules#destination_vm_ip_type}
        '''
        result = self._values.get("destination_vm_ip_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_vm_nic_id(self) -> typing.Optional[jsii.Number]:
        '''Destination VM NIC ID to which this rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#destination_vm_nic_id VappFirewallRules#destination_vm_nic_id}
        '''
        result = self._values.get("destination_vm_nic_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        ''''true' value will enable firewall rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#enabled VappFirewallRules#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        ''''true' value will enable rule logging. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#enable_logging VappFirewallRules#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Rule name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#name VappFirewallRules#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''One of: ``drop`` (drop packets that match the rule), ``allow`` (allow packets that match the rule to pass through the firewall).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#policy VappFirewallRules#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Specify the protocols to which the rule should be applied. One of: ``any``, ``icmp``, ``tcp``, ``udp``, ``tcp&udp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#protocol VappFirewallRules#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_ip(self) -> typing.Optional[builtins.str]:
        '''Source IP address to which the rule applies. A value of ``Any`` matches any IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_ip VappFirewallRules#source_ip}
        '''
        result = self._values.get("source_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_port(self) -> typing.Optional[builtins.str]:
        '''Source port to which this rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_port VappFirewallRules#source_port}
        '''
        result = self._values.get("source_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_vm_id(self) -> typing.Optional[builtins.str]:
        '''Source VM identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_vm_id VappFirewallRules#source_vm_id}
        '''
        result = self._values.get("source_vm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_vm_ip_type(self) -> typing.Optional[builtins.str]:
        '''The value can be one of: ``assigned`` - assigned internal IP will be automatically chosen.

        ``NAT``: NATed external IP will be automatically chosen.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_vm_ip_type VappFirewallRules#source_vm_ip_type}
        '''
        result = self._values.get("source_vm_ip_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_vm_nic_id(self) -> typing.Optional[jsii.Number]:
        '''Source VM NIC ID to which this rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_firewall_rules#source_vm_nic_id VappFirewallRules#source_vm_nic_id}
        '''
        result = self._values.get("source_vm_nic_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappFirewallRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappFirewallRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappFirewallRules.VappFirewallRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13eb9eacc9613fc49a002396a977ae45a8515506885294501c102eb339c10e03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappFirewallRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9db346f7449b6ee556f571df56bda6ad7bde59dbb76a1bbd27acd2a32195b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappFirewallRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0b3f6168ae808b13b33b08d582cb30b5cf2a1059137673b133313d8e4153eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c71c1d3716be0c60a4eeea27736e94de40af7d78ad7a250e1671b954e7508bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a3dab058ab086a351a15c962669158367fc8c3c21a86804e3a68bc2673adbf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappFirewallRulesRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappFirewallRulesRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappFirewallRulesRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41356535a22a644a02b5327c81e560d90b3697e2d36fe4fd3a06576b4e68a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappFirewallRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappFirewallRules.VappFirewallRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60a7cd297214bd8e2c96798622596bfc8eebf43fca582872f2b13108018df425)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDestinationIp")
    def reset_destination_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationIp", []))

    @jsii.member(jsii_name="resetDestinationPort")
    def reset_destination_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPort", []))

    @jsii.member(jsii_name="resetDestinationVmId")
    def reset_destination_vm_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationVmId", []))

    @jsii.member(jsii_name="resetDestinationVmIpType")
    def reset_destination_vm_ip_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationVmIpType", []))

    @jsii.member(jsii_name="resetDestinationVmNicId")
    def reset_destination_vm_nic_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationVmNicId", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnableLogging")
    def reset_enable_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLogging", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetSourceIp")
    def reset_source_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceIp", []))

    @jsii.member(jsii_name="resetSourcePort")
    def reset_source_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcePort", []))

    @jsii.member(jsii_name="resetSourceVmId")
    def reset_source_vm_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceVmId", []))

    @jsii.member(jsii_name="resetSourceVmIpType")
    def reset_source_vm_ip_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceVmIpType", []))

    @jsii.member(jsii_name="resetSourceVmNicId")
    def reset_source_vm_nic_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceVmNicId", []))

    @builtins.property
    @jsii.member(jsii_name="destinationIpInput")
    def destination_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationIpInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPortInput")
    def destination_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPortInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationVmIdInput")
    def destination_vm_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationVmIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationVmIpTypeInput")
    def destination_vm_ip_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationVmIpTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationVmNicIdInput")
    def destination_vm_nic_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "destinationVmNicIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLoggingInput")
    def enable_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpInput")
    def source_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIpInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePortInput")
    def source_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcePortInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVmIdInput")
    def source_vm_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVmIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVmIpTypeInput")
    def source_vm_ip_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVmIpTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceVmNicIdInput")
    def source_vm_nic_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sourceVmNicIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationIp")
    def destination_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationIp"))

    @destination_ip.setter
    def destination_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddce7f111558111400cebeec6ea2e12b0f9d1f02c7a8b83b195916f08f18ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationIp", value)

    @builtins.property
    @jsii.member(jsii_name="destinationPort")
    def destination_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPort"))

    @destination_port.setter
    def destination_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d785001f2f920a5d6977b50a7043f1ba2811ecfc2f625e35e8f59415943322d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPort", value)

    @builtins.property
    @jsii.member(jsii_name="destinationVmId")
    def destination_vm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationVmId"))

    @destination_vm_id.setter
    def destination_vm_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb7865bcaa47971fcd3f6d3461d77ec057ee5e84ed6092a5fdc9b5de3555ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationVmId", value)

    @builtins.property
    @jsii.member(jsii_name="destinationVmIpType")
    def destination_vm_ip_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationVmIpType"))

    @destination_vm_ip_type.setter
    def destination_vm_ip_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904dbb2545645854c5945ace62256eef9b047533a699133d766474528c560f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationVmIpType", value)

    @builtins.property
    @jsii.member(jsii_name="destinationVmNicId")
    def destination_vm_nic_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "destinationVmNicId"))

    @destination_vm_nic_id.setter
    def destination_vm_nic_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5073e9f3805477f0afa997706d0cfae837da2bb4c0d0cf4cceff24126792730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationVmNicId", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__fad1e256fcafa8e5ebfbe93a849c0ff776c60d70f3411780131cb54de0f9f376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLogging"))

    @enable_logging.setter
    def enable_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b8c1df6ef5310c99a50abb37abdf5cd116e3a9d3b0eb3765e847ffb380cb35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf18630f261d9c9b6cfc09e0aaf0c3216a780ad4ff4339ecb8baf5ceaeec87f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44545760fd7f4f52515ee5c97843fe787e329ed4f849d2c20f663066c9054d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65a218f3173d8a480397b55291f1435c34a413d20f7a93341d2c539d058e711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="sourceIp")
    def source_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceIp"))

    @source_ip.setter
    def source_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0649e17c807945dffd62943306f7ff5cb2733c9550fd4de07a8011a9f0d2ff20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIp", value)

    @builtins.property
    @jsii.member(jsii_name="sourcePort")
    def source_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcePort"))

    @source_port.setter
    def source_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15624769f7121e4780a6a8c2f7d919c53afeff04684c12af567b03df00e46f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePort", value)

    @builtins.property
    @jsii.member(jsii_name="sourceVmId")
    def source_vm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVmId"))

    @source_vm_id.setter
    def source_vm_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f148ede13a86ab88e22c934b3b6c25454087292e2b2ef61e5acc5b4ce69ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVmId", value)

    @builtins.property
    @jsii.member(jsii_name="sourceVmIpType")
    def source_vm_ip_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVmIpType"))

    @source_vm_ip_type.setter
    def source_vm_ip_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74199cb1a0be0967b3022e6d1ed3329abf643f55d2f3296f2272c97947639698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVmIpType", value)

    @builtins.property
    @jsii.member(jsii_name="sourceVmNicId")
    def source_vm_nic_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sourceVmNicId"))

    @source_vm_nic_id.setter
    def source_vm_nic_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d300148e93b73646fc4c0fe88786b669439d7256a0a461a38c7c8432c64dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVmNicId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappFirewallRulesRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappFirewallRulesRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappFirewallRulesRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b33fc8f71528b9e921958f18fddccd1b587053a5868eca1ee66a3c3884e1a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VappFirewallRules",
    "VappFirewallRulesConfig",
    "VappFirewallRulesRule",
    "VappFirewallRulesRuleList",
    "VappFirewallRulesRuleOutputReference",
]

publication.publish()

def _typecheckingstub__f85e688bc0f4b4d74e6dcd1af41d8a0b1d3023ab5422b6cac2cf07324e3ce58d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_action: builtins.str,
    network_id: builtins.str,
    vapp_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    log_default_action: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappFirewallRulesRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__6a261fbe7decc09e6918ff41fc0171ab6c78ff41f7ac3f68dbb5264b9446bc79(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4601934c93e5f507b66dc554a52232b66d09d2ec664cd1cee008cac2878406fe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappFirewallRulesRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda4feb18b69645a0d021a373d44b1944b38ce92803206c6854f520acc95a3df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8458e4bf8b0ae83c4941f3b54a56d2c21c3b5c62cc5d577e571783c5eed6f24b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17f70a9f119b6e47275bffc2954dbe99a50f4aa4b575dad657846a8a6e0142a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09dd31b6da05fc4620c36ff3a9a45dc82025d57b56a0f0b3204a19e2e79fd16(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3196406852683f15df88f2fed3404bea7d9434b58a1552b487cfc0d92a801a51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a40c3845f2ca4472386cbeb412fead69e56345ce118b14cd04260b1b1fbd64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5ad0b17e5cdb00dc22159a2fd35851b0a1a8c76517fb8951588be7bef27817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0808d696c8d27c4a1beaa73a367e043be7d286b66dd3f8161393bb183a359b88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d402f8af2b7e9bffa51d138ab880edad18f6bcac9bceb9edb970c2cce95707(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_action: builtins.str,
    network_id: builtins.str,
    vapp_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    log_default_action: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappFirewallRulesRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b70be0bf1ceaae0a932746617c0f51bf4792da654bddfecc8fd92ca794f7dad(
    *,
    destination_ip: typing.Optional[builtins.str] = None,
    destination_port: typing.Optional[builtins.str] = None,
    destination_vm_id: typing.Optional[builtins.str] = None,
    destination_vm_ip_type: typing.Optional[builtins.str] = None,
    destination_vm_nic_id: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    source_ip: typing.Optional[builtins.str] = None,
    source_port: typing.Optional[builtins.str] = None,
    source_vm_id: typing.Optional[builtins.str] = None,
    source_vm_ip_type: typing.Optional[builtins.str] = None,
    source_vm_nic_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13eb9eacc9613fc49a002396a977ae45a8515506885294501c102eb339c10e03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9db346f7449b6ee556f571df56bda6ad7bde59dbb76a1bbd27acd2a32195b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0b3f6168ae808b13b33b08d582cb30b5cf2a1059137673b133313d8e4153eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c71c1d3716be0c60a4eeea27736e94de40af7d78ad7a250e1671b954e7508bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3dab058ab086a351a15c962669158367fc8c3c21a86804e3a68bc2673adbf9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41356535a22a644a02b5327c81e560d90b3697e2d36fe4fd3a06576b4e68a94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappFirewallRulesRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a7cd297214bd8e2c96798622596bfc8eebf43fca582872f2b13108018df425(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddce7f111558111400cebeec6ea2e12b0f9d1f02c7a8b83b195916f08f18ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d785001f2f920a5d6977b50a7043f1ba2811ecfc2f625e35e8f59415943322d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb7865bcaa47971fcd3f6d3461d77ec057ee5e84ed6092a5fdc9b5de3555ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904dbb2545645854c5945ace62256eef9b047533a699133d766474528c560f81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5073e9f3805477f0afa997706d0cfae837da2bb4c0d0cf4cceff24126792730(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad1e256fcafa8e5ebfbe93a849c0ff776c60d70f3411780131cb54de0f9f376(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b8c1df6ef5310c99a50abb37abdf5cd116e3a9d3b0eb3765e847ffb380cb35(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf18630f261d9c9b6cfc09e0aaf0c3216a780ad4ff4339ecb8baf5ceaeec87f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44545760fd7f4f52515ee5c97843fe787e329ed4f849d2c20f663066c9054d2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65a218f3173d8a480397b55291f1435c34a413d20f7a93341d2c539d058e711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0649e17c807945dffd62943306f7ff5cb2733c9550fd4de07a8011a9f0d2ff20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15624769f7121e4780a6a8c2f7d919c53afeff04684c12af567b03df00e46f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f148ede13a86ab88e22c934b3b6c25454087292e2b2ef61e5acc5b4ce69ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74199cb1a0be0967b3022e6d1ed3329abf643f55d2f3296f2272c97947639698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d300148e93b73646fc4c0fe88786b669439d7256a0a461a38c7c8432c64dac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b33fc8f71528b9e921958f18fddccd1b587053a5868eca1ee66a3c3884e1a27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappFirewallRulesRule]],
) -> None:
    """Type checking stubs"""
    pass
