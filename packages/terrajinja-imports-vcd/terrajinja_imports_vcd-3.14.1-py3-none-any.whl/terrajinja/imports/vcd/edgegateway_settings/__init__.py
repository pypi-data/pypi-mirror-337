'''
# `vcd_edgegateway_settings`

Refer to the Terraform Registry for docs: [`vcd_edgegateway_settings`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings).
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


class EdgegatewaySettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegatewaySettings.EdgegatewaySettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings vcd_edgegateway_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway_id: typing.Optional[builtins.str] = None,
        edge_gateway_name: typing.Optional[builtins.str] = None,
        fw_default_rule_action: typing.Optional[builtins.str] = None,
        fw_default_rule_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fw_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lb_acceleration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_loglevel: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings vcd_edgegateway_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway_id: ID of the edge gateway. Required when 'edge_gateway_name' is not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#edge_gateway_id EdgegatewaySettings#edge_gateway_id}
        :param edge_gateway_name: Name of the edge gateway. Required when 'edge_gateway_id' is not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#edge_gateway_name EdgegatewaySettings#edge_gateway_name}
        :param fw_default_rule_action: 'accept' or 'deny'. Default 'deny'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_default_rule_action EdgegatewaySettings#fw_default_rule_action}
        :param fw_default_rule_logging_enabled: Enable logging for default rule. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_default_rule_logging_enabled EdgegatewaySettings#fw_default_rule_logging_enabled}
        :param fw_enabled: Enable firewall. Default 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_enabled EdgegatewaySettings#fw_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#id EdgegatewaySettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lb_acceleration_enabled: Enable load balancer acceleration. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_acceleration_enabled EdgegatewaySettings#lb_acceleration_enabled}
        :param lb_enabled: Enable load balancing. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_enabled EdgegatewaySettings#lb_enabled}
        :param lb_logging_enabled: Enable load balancer logging. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_logging_enabled EdgegatewaySettings#lb_logging_enabled}
        :param lb_loglevel: Log level. One of 'emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug'. ('info' by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_loglevel EdgegatewaySettings#lb_loglevel}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#org EdgegatewaySettings#org}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#vdc EdgegatewaySettings#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68086ce4155bb9782f0b39a2d9608f20a200776afd992846423602ee16ac5a2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EdgegatewaySettingsConfig(
            edge_gateway_id=edge_gateway_id,
            edge_gateway_name=edge_gateway_name,
            fw_default_rule_action=fw_default_rule_action,
            fw_default_rule_logging_enabled=fw_default_rule_logging_enabled,
            fw_enabled=fw_enabled,
            id=id,
            lb_acceleration_enabled=lb_acceleration_enabled,
            lb_enabled=lb_enabled,
            lb_logging_enabled=lb_logging_enabled,
            lb_loglevel=lb_loglevel,
            org=org,
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
        '''Generates CDKTF code for importing a EdgegatewaySettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EdgegatewaySettings to import.
        :param import_from_id: The id of the existing EdgegatewaySettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EdgegatewaySettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01df67df79ec252fc8646486be6d7cef6f747d6d18c2bcd1080c12a995074839)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetEdgeGatewayId")
    def reset_edge_gateway_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeGatewayId", []))

    @jsii.member(jsii_name="resetEdgeGatewayName")
    def reset_edge_gateway_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeGatewayName", []))

    @jsii.member(jsii_name="resetFwDefaultRuleAction")
    def reset_fw_default_rule_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFwDefaultRuleAction", []))

    @jsii.member(jsii_name="resetFwDefaultRuleLoggingEnabled")
    def reset_fw_default_rule_logging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFwDefaultRuleLoggingEnabled", []))

    @jsii.member(jsii_name="resetFwEnabled")
    def reset_fw_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFwEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLbAccelerationEnabled")
    def reset_lb_acceleration_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLbAccelerationEnabled", []))

    @jsii.member(jsii_name="resetLbEnabled")
    def reset_lb_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLbEnabled", []))

    @jsii.member(jsii_name="resetLbLoggingEnabled")
    def reset_lb_logging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLbLoggingEnabled", []))

    @jsii.member(jsii_name="resetLbLoglevel")
    def reset_lb_loglevel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLbLoglevel", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

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
    @jsii.member(jsii_name="edgeGatewayIdInput")
    def edge_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayNameInput")
    def edge_gateway_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fwDefaultRuleActionInput")
    def fw_default_rule_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fwDefaultRuleActionInput"))

    @builtins.property
    @jsii.member(jsii_name="fwDefaultRuleLoggingEnabledInput")
    def fw_default_rule_logging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fwDefaultRuleLoggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="fwEnabledInput")
    def fw_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fwEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lbAccelerationEnabledInput")
    def lb_acceleration_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lbAccelerationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lbEnabledInput")
    def lb_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lbEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lbLoggingEnabledInput")
    def lb_logging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lbLoggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lbLoglevelInput")
    def lb_loglevel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lbLoglevelInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayId")
    def edge_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGatewayId"))

    @edge_gateway_id.setter
    def edge_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c577ed749aef35519bdcb62889380a70f7e51af58ac4520dba9cf86f87956d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGatewayId", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayName")
    def edge_gateway_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGatewayName"))

    @edge_gateway_name.setter
    def edge_gateway_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d47c6205968d23c811820ba8c7c86c4fb9b8614d8a9cf044b6e0ba74416c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGatewayName", value)

    @builtins.property
    @jsii.member(jsii_name="fwDefaultRuleAction")
    def fw_default_rule_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fwDefaultRuleAction"))

    @fw_default_rule_action.setter
    def fw_default_rule_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d298b5e0e14b0759c0e8129cd8e9497cc8ba94427504189be174764c9a08a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fwDefaultRuleAction", value)

    @builtins.property
    @jsii.member(jsii_name="fwDefaultRuleLoggingEnabled")
    def fw_default_rule_logging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fwDefaultRuleLoggingEnabled"))

    @fw_default_rule_logging_enabled.setter
    def fw_default_rule_logging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8450dca4b3043d3868ef942b48cdcba81f13eb358f458302ff2a0b60045904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fwDefaultRuleLoggingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="fwEnabled")
    def fw_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fwEnabled"))

    @fw_enabled.setter
    def fw_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b927b8f40f608851b471916d60da9b18c09406644d120d279325f2dd8b6d9f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fwEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17dfe21347927359376f2a79b67d77ff474502ab21da37be2fe0103ab5edf49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="lbAccelerationEnabled")
    def lb_acceleration_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lbAccelerationEnabled"))

    @lb_acceleration_enabled.setter
    def lb_acceleration_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5468f3a8850a99eaad9dbae4de6234fc829df4afef92bb4fda6087d21445bed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbAccelerationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="lbEnabled")
    def lb_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lbEnabled"))

    @lb_enabled.setter
    def lb_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb10c4b4510ab7a5f373937e463f0f76ae37a2492bf28d91ec3d9a1e8c50f12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="lbLoggingEnabled")
    def lb_logging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lbLoggingEnabled"))

    @lb_logging_enabled.setter
    def lb_logging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58707392ae48a05034fbd6a79374c2ae5df5357e7a011905586043aa094cefc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbLoggingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="lbLoglevel")
    def lb_loglevel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lbLoglevel"))

    @lb_loglevel.setter
    def lb_loglevel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f858ea8e0d9506a51574de20ab27bd17e22920e484c1011f521dfbae206ebe00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbLoglevel", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54c38a1338d9ef0610719d3193fccbfa15dcfe3431a4ffc5a3c4f35b273528f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d35b111b5e94bf6e6953ac4f75c256c02e6d9dfe9c00106679a292a9479123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.edgegatewaySettings.EdgegatewaySettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "edge_gateway_id": "edgeGatewayId",
        "edge_gateway_name": "edgeGatewayName",
        "fw_default_rule_action": "fwDefaultRuleAction",
        "fw_default_rule_logging_enabled": "fwDefaultRuleLoggingEnabled",
        "fw_enabled": "fwEnabled",
        "id": "id",
        "lb_acceleration_enabled": "lbAccelerationEnabled",
        "lb_enabled": "lbEnabled",
        "lb_logging_enabled": "lbLoggingEnabled",
        "lb_loglevel": "lbLoglevel",
        "org": "org",
        "vdc": "vdc",
    },
)
class EdgegatewaySettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        edge_gateway_id: typing.Optional[builtins.str] = None,
        edge_gateway_name: typing.Optional[builtins.str] = None,
        fw_default_rule_action: typing.Optional[builtins.str] = None,
        fw_default_rule_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fw_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lb_acceleration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_loglevel: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
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
        :param edge_gateway_id: ID of the edge gateway. Required when 'edge_gateway_name' is not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#edge_gateway_id EdgegatewaySettings#edge_gateway_id}
        :param edge_gateway_name: Name of the edge gateway. Required when 'edge_gateway_id' is not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#edge_gateway_name EdgegatewaySettings#edge_gateway_name}
        :param fw_default_rule_action: 'accept' or 'deny'. Default 'deny'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_default_rule_action EdgegatewaySettings#fw_default_rule_action}
        :param fw_default_rule_logging_enabled: Enable logging for default rule. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_default_rule_logging_enabled EdgegatewaySettings#fw_default_rule_logging_enabled}
        :param fw_enabled: Enable firewall. Default 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_enabled EdgegatewaySettings#fw_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#id EdgegatewaySettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lb_acceleration_enabled: Enable load balancer acceleration. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_acceleration_enabled EdgegatewaySettings#lb_acceleration_enabled}
        :param lb_enabled: Enable load balancing. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_enabled EdgegatewaySettings#lb_enabled}
        :param lb_logging_enabled: Enable load balancer logging. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_logging_enabled EdgegatewaySettings#lb_logging_enabled}
        :param lb_loglevel: Log level. One of 'emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug'. ('info' by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_loglevel EdgegatewaySettings#lb_loglevel}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#org EdgegatewaySettings#org}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#vdc EdgegatewaySettings#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90af9e51ac050c238b25ae3691c575dae6be8a78fb12a5fdafe2ff2eec1e7a5d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway_id", value=edge_gateway_id, expected_type=type_hints["edge_gateway_id"])
            check_type(argname="argument edge_gateway_name", value=edge_gateway_name, expected_type=type_hints["edge_gateway_name"])
            check_type(argname="argument fw_default_rule_action", value=fw_default_rule_action, expected_type=type_hints["fw_default_rule_action"])
            check_type(argname="argument fw_default_rule_logging_enabled", value=fw_default_rule_logging_enabled, expected_type=type_hints["fw_default_rule_logging_enabled"])
            check_type(argname="argument fw_enabled", value=fw_enabled, expected_type=type_hints["fw_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lb_acceleration_enabled", value=lb_acceleration_enabled, expected_type=type_hints["lb_acceleration_enabled"])
            check_type(argname="argument lb_enabled", value=lb_enabled, expected_type=type_hints["lb_enabled"])
            check_type(argname="argument lb_logging_enabled", value=lb_logging_enabled, expected_type=type_hints["lb_logging_enabled"])
            check_type(argname="argument lb_loglevel", value=lb_loglevel, expected_type=type_hints["lb_loglevel"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
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
        if edge_gateway_id is not None:
            self._values["edge_gateway_id"] = edge_gateway_id
        if edge_gateway_name is not None:
            self._values["edge_gateway_name"] = edge_gateway_name
        if fw_default_rule_action is not None:
            self._values["fw_default_rule_action"] = fw_default_rule_action
        if fw_default_rule_logging_enabled is not None:
            self._values["fw_default_rule_logging_enabled"] = fw_default_rule_logging_enabled
        if fw_enabled is not None:
            self._values["fw_enabled"] = fw_enabled
        if id is not None:
            self._values["id"] = id
        if lb_acceleration_enabled is not None:
            self._values["lb_acceleration_enabled"] = lb_acceleration_enabled
        if lb_enabled is not None:
            self._values["lb_enabled"] = lb_enabled
        if lb_logging_enabled is not None:
            self._values["lb_logging_enabled"] = lb_logging_enabled
        if lb_loglevel is not None:
            self._values["lb_loglevel"] = lb_loglevel
        if org is not None:
            self._values["org"] = org
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
    def edge_gateway_id(self) -> typing.Optional[builtins.str]:
        '''ID of the edge gateway. Required when 'edge_gateway_name' is not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#edge_gateway_id EdgegatewaySettings#edge_gateway_id}
        '''
        result = self._values.get("edge_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_gateway_name(self) -> typing.Optional[builtins.str]:
        '''Name of the edge gateway. Required when 'edge_gateway_id' is not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#edge_gateway_name EdgegatewaySettings#edge_gateway_name}
        '''
        result = self._values.get("edge_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fw_default_rule_action(self) -> typing.Optional[builtins.str]:
        ''''accept' or 'deny'. Default 'deny'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_default_rule_action EdgegatewaySettings#fw_default_rule_action}
        '''
        result = self._values.get("fw_default_rule_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fw_default_rule_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable logging for default rule. Default 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_default_rule_logging_enabled EdgegatewaySettings#fw_default_rule_logging_enabled}
        '''
        result = self._values.get("fw_default_rule_logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fw_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable firewall. Default 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#fw_enabled EdgegatewaySettings#fw_enabled}
        '''
        result = self._values.get("fw_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#id EdgegatewaySettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lb_acceleration_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable load balancer acceleration. (Disabled by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_acceleration_enabled EdgegatewaySettings#lb_acceleration_enabled}
        '''
        result = self._values.get("lb_acceleration_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lb_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable load balancing. (Disabled by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_enabled EdgegatewaySettings#lb_enabled}
        '''
        result = self._values.get("lb_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lb_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable load balancer logging. (Disabled by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_logging_enabled EdgegatewaySettings#lb_logging_enabled}
        '''
        result = self._values.get("lb_logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lb_loglevel(self) -> typing.Optional[builtins.str]:
        '''Log level. One of 'emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug'. ('info' by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#lb_loglevel EdgegatewaySettings#lb_loglevel}
        '''
        result = self._values.get("lb_loglevel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#org EdgegatewaySettings#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_settings#vdc EdgegatewaySettings#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgegatewaySettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EdgegatewaySettings",
    "EdgegatewaySettingsConfig",
]

publication.publish()

def _typecheckingstub__d68086ce4155bb9782f0b39a2d9608f20a200776afd992846423602ee16ac5a2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway_id: typing.Optional[builtins.str] = None,
    edge_gateway_name: typing.Optional[builtins.str] = None,
    fw_default_rule_action: typing.Optional[builtins.str] = None,
    fw_default_rule_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fw_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lb_acceleration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_loglevel: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__01df67df79ec252fc8646486be6d7cef6f747d6d18c2bcd1080c12a995074839(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c577ed749aef35519bdcb62889380a70f7e51af58ac4520dba9cf86f87956d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d47c6205968d23c811820ba8c7c86c4fb9b8614d8a9cf044b6e0ba74416c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d298b5e0e14b0759c0e8129cd8e9497cc8ba94427504189be174764c9a08a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8450dca4b3043d3868ef942b48cdcba81f13eb358f458302ff2a0b60045904(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b927b8f40f608851b471916d60da9b18c09406644d120d279325f2dd8b6d9f3a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17dfe21347927359376f2a79b67d77ff474502ab21da37be2fe0103ab5edf49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5468f3a8850a99eaad9dbae4de6234fc829df4afef92bb4fda6087d21445bed4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb10c4b4510ab7a5f373937e463f0f76ae37a2492bf28d91ec3d9a1e8c50f12d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58707392ae48a05034fbd6a79374c2ae5df5357e7a011905586043aa094cefc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f858ea8e0d9506a51574de20ab27bd17e22920e484c1011f521dfbae206ebe00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54c38a1338d9ef0610719d3193fccbfa15dcfe3431a4ffc5a3c4f35b273528f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d35b111b5e94bf6e6953ac4f75c256c02e6d9dfe9c00106679a292a9479123(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90af9e51ac050c238b25ae3691c575dae6be8a78fb12a5fdafe2ff2eec1e7a5d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway_id: typing.Optional[builtins.str] = None,
    edge_gateway_name: typing.Optional[builtins.str] = None,
    fw_default_rule_action: typing.Optional[builtins.str] = None,
    fw_default_rule_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fw_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lb_acceleration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_loglevel: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
