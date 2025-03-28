'''
# `vcd_edgegateway`

Refer to the Terraform Registry for docs: [`vcd_edgegateway`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway).
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


class Edgegateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegateway.Edgegateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway vcd_edgegateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        configuration: builtins.str,
        external_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayExternalNetwork", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        distributed_routing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fips_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fw_default_rule_action: typing.Optional[builtins.str] = None,
        fw_default_rule_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fw_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lb_acceleration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_loglevel: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        use_default_route_for_dns_relay: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway vcd_edgegateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param configuration: Configuration of the vShield edge VM for this gateway. One of: compact, full ("Large"), full4 ("Quad Large"), x-large. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#configuration Edgegateway#configuration}
        :param external_network: external_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#external_network Edgegateway#external_network}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#name Edgegateway#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#description Edgegateway#description}.
        :param distributed_routing: Enable distributed routing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#distributed_routing Edgegateway#distributed_routing}
        :param fips_mode_enabled: Enable FIPS mode. FIPS mode turns on the cipher suites that comply with FIPS. (False by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fips_mode_enabled Edgegateway#fips_mode_enabled}
        :param fw_default_rule_action: 'accept' or 'deny'. Default 'deny'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_default_rule_action Edgegateway#fw_default_rule_action}
        :param fw_default_rule_logging_enabled: Enable logging for default rule. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_default_rule_logging_enabled Edgegateway#fw_default_rule_logging_enabled}
        :param fw_enabled: Enable firewall. Default 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_enabled Edgegateway#fw_enabled}
        :param ha_enabled: Enable high availability on this edge gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#ha_enabled Edgegateway#ha_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#id Edgegateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lb_acceleration_enabled: Enable load balancer acceleration. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_acceleration_enabled Edgegateway#lb_acceleration_enabled}
        :param lb_enabled: Enable load balancing. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_enabled Edgegateway#lb_enabled}
        :param lb_logging_enabled: Enable load balancer logging. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_logging_enabled Edgegateway#lb_logging_enabled}
        :param lb_loglevel: Log level. One of 'emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug'. ('info' by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_loglevel Edgegateway#lb_loglevel}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#org Edgegateway#org}
        :param use_default_route_for_dns_relay: If true, default gateway will be used for the edge gateways' default routing and DNS forwarding.(False by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#use_default_route_for_dns_relay Edgegateway#use_default_route_for_dns_relay}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#vdc Edgegateway#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c57953c7ef8514d497bc97d05c6ed98f8729720f1fe9c2b75dd1334e710083)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EdgegatewayConfig(
            configuration=configuration,
            external_network=external_network,
            name=name,
            description=description,
            distributed_routing=distributed_routing,
            fips_mode_enabled=fips_mode_enabled,
            fw_default_rule_action=fw_default_rule_action,
            fw_default_rule_logging_enabled=fw_default_rule_logging_enabled,
            fw_enabled=fw_enabled,
            ha_enabled=ha_enabled,
            id=id,
            lb_acceleration_enabled=lb_acceleration_enabled,
            lb_enabled=lb_enabled,
            lb_logging_enabled=lb_logging_enabled,
            lb_loglevel=lb_loglevel,
            org=org,
            use_default_route_for_dns_relay=use_default_route_for_dns_relay,
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
        '''Generates CDKTF code for importing a Edgegateway resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Edgegateway to import.
        :param import_from_id: The id of the existing Edgegateway that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Edgegateway to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e70d3b6e13b669fd6d62e05dc11aad7d84f64a5c10a812b4531186c9589630d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExternalNetwork")
    def put_external_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayExternalNetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56cc06ef77ed1d4cc2dd8756b1eabcbdd3a70ad2677ba0359bb28d33700367b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExternalNetwork", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDistributedRouting")
    def reset_distributed_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistributedRouting", []))

    @jsii.member(jsii_name="resetFipsModeEnabled")
    def reset_fips_mode_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFipsModeEnabled", []))

    @jsii.member(jsii_name="resetFwDefaultRuleAction")
    def reset_fw_default_rule_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFwDefaultRuleAction", []))

    @jsii.member(jsii_name="resetFwDefaultRuleLoggingEnabled")
    def reset_fw_default_rule_logging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFwDefaultRuleLoggingEnabled", []))

    @jsii.member(jsii_name="resetFwEnabled")
    def reset_fw_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFwEnabled", []))

    @jsii.member(jsii_name="resetHaEnabled")
    def reset_ha_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaEnabled", []))

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

    @jsii.member(jsii_name="resetUseDefaultRouteForDnsRelay")
    def reset_use_default_route_for_dns_relay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseDefaultRouteForDnsRelay", []))

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
    @jsii.member(jsii_name="defaultExternalNetworkIp")
    def default_external_network_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultExternalNetworkIp"))

    @builtins.property
    @jsii.member(jsii_name="externalNetwork")
    def external_network(self) -> "EdgegatewayExternalNetworkList":
        return typing.cast("EdgegatewayExternalNetworkList", jsii.get(self, "externalNetwork"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkIps")
    def external_network_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalNetworkIps"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="distributedRoutingInput")
    def distributed_routing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "distributedRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkInput")
    def external_network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetwork"]]], jsii.get(self, "externalNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="fipsModeEnabledInput")
    def fips_mode_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fipsModeEnabledInput"))

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
    @jsii.member(jsii_name="haEnabledInput")
    def ha_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "haEnabledInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="useDefaultRouteForDnsRelayInput")
    def use_default_route_for_dns_relay_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useDefaultRouteForDnsRelayInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7818634732d05f771efbbc3a4805c4900ee29da3c9f5a176c6461bb158e28378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce9914bd0033a829481c61c659b0fbd3a0ae5ba4f6dab8bde7dcf457130edcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="distributedRouting")
    def distributed_routing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "distributedRouting"))

    @distributed_routing.setter
    def distributed_routing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2382864093f5800be8e64e238784627740d0b6027b13b8c515c033d9d8c7d656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributedRouting", value)

    @builtins.property
    @jsii.member(jsii_name="fipsModeEnabled")
    def fips_mode_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fipsModeEnabled"))

    @fips_mode_enabled.setter
    def fips_mode_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb6a8bf99d96ddb7946777e8e64b52d2e544253b6211442df5170e60d9e607f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fipsModeEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="fwDefaultRuleAction")
    def fw_default_rule_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fwDefaultRuleAction"))

    @fw_default_rule_action.setter
    def fw_default_rule_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671b54f094739937d1bc69ed6c6c72bbc412cce9cd3734be4d24887004743959)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d11b7c9004ded0eddd45a2dcc28b170c7b669026360209e7f0f0e3446d1b3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1b28ece75903da0cbb58a3103866625f92a0f742937de0d090373f4435e33bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fwEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="haEnabled")
    def ha_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "haEnabled"))

    @ha_enabled.setter
    def ha_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef6b755194a2663d19d4bfd9d4c37e0cf2caa25559853308f92b35f904f25d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c9b383bd5ae7bff916e35c904946c1d0c46ded73b3762ad3c6bde306586f1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be316d58cae0d28186a21328542e0553df13e2413d491b539c1bb88f4109f139)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b55dfd86ad2fc4c141bc07a7757d84c77ff4417c0ed14c4f791df4c0e48e5dbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfdd492953134d720ce049ab7282519d0d917ea3b813931db7d10b7b54b8b54f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbLoggingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="lbLoglevel")
    def lb_loglevel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lbLoglevel"))

    @lb_loglevel.setter
    def lb_loglevel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b61b65b069af466d7e62a2eb6790584c5ffbaf1ad4441d2cf8a689e5ce00fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbLoglevel", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7ddd7fd087657befef6fa165c56ed4bd44f940f38a3c9e995a87b2d6e7310f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0dbcb41108768d75536bb1a8cdafe615418ba990e99bb5d59117da26a41dd8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="useDefaultRouteForDnsRelay")
    def use_default_route_for_dns_relay(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useDefaultRouteForDnsRelay"))

    @use_default_route_for_dns_relay.setter
    def use_default_route_for_dns_relay(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64cb93b38eb438e2be3aff835a156043a147db35970b0fa52842c25c7ac611e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDefaultRouteForDnsRelay", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57b9fd4cf9512bcfdc6c932e3abd8a43dca5efb5cdab2f5d6776d8810e17c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.edgegateway.EdgegatewayConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "configuration": "configuration",
        "external_network": "externalNetwork",
        "name": "name",
        "description": "description",
        "distributed_routing": "distributedRouting",
        "fips_mode_enabled": "fipsModeEnabled",
        "fw_default_rule_action": "fwDefaultRuleAction",
        "fw_default_rule_logging_enabled": "fwDefaultRuleLoggingEnabled",
        "fw_enabled": "fwEnabled",
        "ha_enabled": "haEnabled",
        "id": "id",
        "lb_acceleration_enabled": "lbAccelerationEnabled",
        "lb_enabled": "lbEnabled",
        "lb_logging_enabled": "lbLoggingEnabled",
        "lb_loglevel": "lbLoglevel",
        "org": "org",
        "use_default_route_for_dns_relay": "useDefaultRouteForDnsRelay",
        "vdc": "vdc",
    },
)
class EdgegatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        configuration: builtins.str,
        external_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayExternalNetwork", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        distributed_routing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fips_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fw_default_rule_action: typing.Optional[builtins.str] = None,
        fw_default_rule_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fw_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lb_acceleration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lb_loglevel: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        use_default_route_for_dns_relay: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param configuration: Configuration of the vShield edge VM for this gateway. One of: compact, full ("Large"), full4 ("Quad Large"), x-large. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#configuration Edgegateway#configuration}
        :param external_network: external_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#external_network Edgegateway#external_network}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#name Edgegateway#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#description Edgegateway#description}.
        :param distributed_routing: Enable distributed routing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#distributed_routing Edgegateway#distributed_routing}
        :param fips_mode_enabled: Enable FIPS mode. FIPS mode turns on the cipher suites that comply with FIPS. (False by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fips_mode_enabled Edgegateway#fips_mode_enabled}
        :param fw_default_rule_action: 'accept' or 'deny'. Default 'deny'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_default_rule_action Edgegateway#fw_default_rule_action}
        :param fw_default_rule_logging_enabled: Enable logging for default rule. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_default_rule_logging_enabled Edgegateway#fw_default_rule_logging_enabled}
        :param fw_enabled: Enable firewall. Default 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_enabled Edgegateway#fw_enabled}
        :param ha_enabled: Enable high availability on this edge gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#ha_enabled Edgegateway#ha_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#id Edgegateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lb_acceleration_enabled: Enable load balancer acceleration. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_acceleration_enabled Edgegateway#lb_acceleration_enabled}
        :param lb_enabled: Enable load balancing. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_enabled Edgegateway#lb_enabled}
        :param lb_logging_enabled: Enable load balancer logging. (Disabled by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_logging_enabled Edgegateway#lb_logging_enabled}
        :param lb_loglevel: Log level. One of 'emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug'. ('info' by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_loglevel Edgegateway#lb_loglevel}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#org Edgegateway#org}
        :param use_default_route_for_dns_relay: If true, default gateway will be used for the edge gateways' default routing and DNS forwarding.(False by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#use_default_route_for_dns_relay Edgegateway#use_default_route_for_dns_relay}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#vdc Edgegateway#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb02f2a2a8f83474d4461958dc9ab0a86aaf3bad800b98219a3d2c190e5c854)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument external_network", value=external_network, expected_type=type_hints["external_network"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument distributed_routing", value=distributed_routing, expected_type=type_hints["distributed_routing"])
            check_type(argname="argument fips_mode_enabled", value=fips_mode_enabled, expected_type=type_hints["fips_mode_enabled"])
            check_type(argname="argument fw_default_rule_action", value=fw_default_rule_action, expected_type=type_hints["fw_default_rule_action"])
            check_type(argname="argument fw_default_rule_logging_enabled", value=fw_default_rule_logging_enabled, expected_type=type_hints["fw_default_rule_logging_enabled"])
            check_type(argname="argument fw_enabled", value=fw_enabled, expected_type=type_hints["fw_enabled"])
            check_type(argname="argument ha_enabled", value=ha_enabled, expected_type=type_hints["ha_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lb_acceleration_enabled", value=lb_acceleration_enabled, expected_type=type_hints["lb_acceleration_enabled"])
            check_type(argname="argument lb_enabled", value=lb_enabled, expected_type=type_hints["lb_enabled"])
            check_type(argname="argument lb_logging_enabled", value=lb_logging_enabled, expected_type=type_hints["lb_logging_enabled"])
            check_type(argname="argument lb_loglevel", value=lb_loglevel, expected_type=type_hints["lb_loglevel"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument use_default_route_for_dns_relay", value=use_default_route_for_dns_relay, expected_type=type_hints["use_default_route_for_dns_relay"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
            "external_network": external_network,
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
        if description is not None:
            self._values["description"] = description
        if distributed_routing is not None:
            self._values["distributed_routing"] = distributed_routing
        if fips_mode_enabled is not None:
            self._values["fips_mode_enabled"] = fips_mode_enabled
        if fw_default_rule_action is not None:
            self._values["fw_default_rule_action"] = fw_default_rule_action
        if fw_default_rule_logging_enabled is not None:
            self._values["fw_default_rule_logging_enabled"] = fw_default_rule_logging_enabled
        if fw_enabled is not None:
            self._values["fw_enabled"] = fw_enabled
        if ha_enabled is not None:
            self._values["ha_enabled"] = ha_enabled
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
        if use_default_route_for_dns_relay is not None:
            self._values["use_default_route_for_dns_relay"] = use_default_route_for_dns_relay
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
    def configuration(self) -> builtins.str:
        '''Configuration of the vShield edge VM for this gateway. One of: compact, full ("Large"), full4 ("Quad Large"), x-large.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#configuration Edgegateway#configuration}
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_network(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetwork"]]:
        '''external_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#external_network Edgegateway#external_network}
        '''
        result = self._values.get("external_network")
        assert result is not None, "Required property 'external_network' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetwork"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#name Edgegateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#description Edgegateway#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distributed_routing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable distributed routing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#distributed_routing Edgegateway#distributed_routing}
        '''
        result = self._values.get("distributed_routing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fips_mode_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable FIPS mode. FIPS mode turns on the cipher suites that comply with FIPS. (False by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fips_mode_enabled Edgegateway#fips_mode_enabled}
        '''
        result = self._values.get("fips_mode_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fw_default_rule_action(self) -> typing.Optional[builtins.str]:
        ''''accept' or 'deny'. Default 'deny'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_default_rule_action Edgegateway#fw_default_rule_action}
        '''
        result = self._values.get("fw_default_rule_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fw_default_rule_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable logging for default rule. Default 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_default_rule_logging_enabled Edgegateway#fw_default_rule_logging_enabled}
        '''
        result = self._values.get("fw_default_rule_logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fw_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable firewall. Default 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#fw_enabled Edgegateway#fw_enabled}
        '''
        result = self._values.get("fw_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ha_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable high availability on this edge gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#ha_enabled Edgegateway#ha_enabled}
        '''
        result = self._values.get("ha_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#id Edgegateway#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_acceleration_enabled Edgegateway#lb_acceleration_enabled}
        '''
        result = self._values.get("lb_acceleration_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lb_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable load balancing. (Disabled by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_enabled Edgegateway#lb_enabled}
        '''
        result = self._values.get("lb_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lb_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable load balancer logging. (Disabled by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_logging_enabled Edgegateway#lb_logging_enabled}
        '''
        result = self._values.get("lb_logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lb_loglevel(self) -> typing.Optional[builtins.str]:
        '''Log level. One of 'emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug'. ('info' by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#lb_loglevel Edgegateway#lb_loglevel}
        '''
        result = self._values.get("lb_loglevel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#org Edgegateway#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_default_route_for_dns_relay(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, default gateway will be used for the edge gateways' default routing and DNS forwarding.(False by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#use_default_route_for_dns_relay Edgegateway#use_default_route_for_dns_relay}
        '''
        result = self._values.get("use_default_route_for_dns_relay")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#vdc Edgegateway#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgegatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "enable_rate_limit": "enableRateLimit",
        "incoming_rate_limit": "incomingRateLimit",
        "outgoing_rate_limit": "outgoingRateLimit",
        "subnet": "subnet",
    },
)
class EdgegatewayExternalNetwork:
    def __init__(
        self,
        *,
        name: builtins.str,
        enable_rate_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        incoming_rate_limit: typing.Optional[jsii.Number] = None,
        outgoing_rate_limit: typing.Optional[jsii.Number] = None,
        subnet: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayExternalNetworkSubnet", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: External network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#name Edgegateway#name}
        :param enable_rate_limit: Enable rate limiting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#enable_rate_limit Edgegateway#enable_rate_limit}
        :param incoming_rate_limit: Incoming rate limit (Mbps). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#incoming_rate_limit Edgegateway#incoming_rate_limit}
        :param outgoing_rate_limit: Outgoing rate limit (Mbps). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#outgoing_rate_limit Edgegateway#outgoing_rate_limit}
        :param subnet: subnet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#subnet Edgegateway#subnet}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75f0cc895e10062c23b1ebd2f73d48c5b963448da216a42f41e5bad4acd4cbf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument enable_rate_limit", value=enable_rate_limit, expected_type=type_hints["enable_rate_limit"])
            check_type(argname="argument incoming_rate_limit", value=incoming_rate_limit, expected_type=type_hints["incoming_rate_limit"])
            check_type(argname="argument outgoing_rate_limit", value=outgoing_rate_limit, expected_type=type_hints["outgoing_rate_limit"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if enable_rate_limit is not None:
            self._values["enable_rate_limit"] = enable_rate_limit
        if incoming_rate_limit is not None:
            self._values["incoming_rate_limit"] = incoming_rate_limit
        if outgoing_rate_limit is not None:
            self._values["outgoing_rate_limit"] = outgoing_rate_limit
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def name(self) -> builtins.str:
        '''External network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#name Edgegateway#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_rate_limit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable rate limiting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#enable_rate_limit Edgegateway#enable_rate_limit}
        '''
        result = self._values.get("enable_rate_limit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def incoming_rate_limit(self) -> typing.Optional[jsii.Number]:
        '''Incoming rate limit (Mbps).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#incoming_rate_limit Edgegateway#incoming_rate_limit}
        '''
        result = self._values.get("incoming_rate_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def outgoing_rate_limit(self) -> typing.Optional[jsii.Number]:
        '''Outgoing rate limit (Mbps).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#outgoing_rate_limit Edgegateway#outgoing_rate_limit}
        '''
        result = self._values.get("outgoing_rate_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def subnet(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetworkSubnet"]]]:
        '''subnet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#subnet Edgegateway#subnet}
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetworkSubnet"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgegatewayExternalNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgegatewayExternalNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19a3e8df56c246f58baa3560ec9e321cc20293ecc1ab59232f6e9a9e272a40c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EdgegatewayExternalNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4aa45169e57defae555d4640ba57bcbd0c25539c1bc4f6d3144f31497ad6c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EdgegatewayExternalNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7470ce8cdf60c121d2479d0c659b3e8a9f898f37565a50c7c35b41b7e39109)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf3d6cf9380156ec8e62e88fac03f195c90063e8a4d0e13b95fe30ee51f41d2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bb841ee1546d13ea06d512a3eecebbde6967a5e01aa1e346b0344a7e45ae3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d396837957eccc617c378c04c08842f5cf720a9603f455e74d51c3ea7dd3911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EdgegatewayExternalNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c86a9e85f6742fb2cb29ff79e4ab9de076424a2e6c9db0e03e31b3bb840fa2bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSubnet")
    def put_subnet(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayExternalNetworkSubnet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e0534a0a75fdf263132cda42e7fb2f42429c5200363c8f059f2f0adff00060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubnet", [value]))

    @jsii.member(jsii_name="resetEnableRateLimit")
    def reset_enable_rate_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRateLimit", []))

    @jsii.member(jsii_name="resetIncomingRateLimit")
    def reset_incoming_rate_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncomingRateLimit", []))

    @jsii.member(jsii_name="resetOutgoingRateLimit")
    def reset_outgoing_rate_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutgoingRateLimit", []))

    @jsii.member(jsii_name="resetSubnet")
    def reset_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnet", []))

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> "EdgegatewayExternalNetworkSubnetList":
        return typing.cast("EdgegatewayExternalNetworkSubnetList", jsii.get(self, "subnet"))

    @builtins.property
    @jsii.member(jsii_name="enableRateLimitInput")
    def enable_rate_limit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="incomingRateLimitInput")
    def incoming_rate_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "incomingRateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outgoingRateLimitInput")
    def outgoing_rate_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "outgoingRateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetInput")
    def subnet_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetworkSubnet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetworkSubnet"]]], jsii.get(self, "subnetInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRateLimit")
    def enable_rate_limit(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRateLimit"))

    @enable_rate_limit.setter
    def enable_rate_limit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f781f4c12da3fd6c78bb8bcfb412bb74afbd723b145ae3e84a92fa02067780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRateLimit", value)

    @builtins.property
    @jsii.member(jsii_name="incomingRateLimit")
    def incoming_rate_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "incomingRateLimit"))

    @incoming_rate_limit.setter
    def incoming_rate_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4bc83b4d5b51f91048bb5e81a42346ee3d6d35fb3d1627fe95f0b31fcbcfd5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "incomingRateLimit", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800fcf4a9b3508c1b32924bfa4458c73538cd805ecec51360bbf1f14042d29ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="outgoingRateLimit")
    def outgoing_rate_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "outgoingRateLimit"))

    @outgoing_rate_limit.setter
    def outgoing_rate_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b238ff4534c71f1539328ceb2fd5c158cf4d6d1489c1f78ecaa995e071e9958f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outgoingRateLimit", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5332743e22543f05f86e76b069cc0f685bb59b8f6bffb271a4a5b4a23e8f7136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetworkSubnet",
    jsii_struct_bases=[],
    name_mapping={
        "gateway": "gateway",
        "netmask": "netmask",
        "ip_address": "ipAddress",
        "suballocate_pool": "suballocatePool",
        "use_for_default_route": "useForDefaultRoute",
    },
)
class EdgegatewayExternalNetworkSubnet:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        netmask: builtins.str,
        ip_address: typing.Optional[builtins.str] = None,
        suballocate_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayExternalNetworkSubnetSuballocatePool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        use_for_default_route: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param gateway: Gateway address for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#gateway Edgegateway#gateway}
        :param netmask: Netmask address for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#netmask Edgegateway#netmask}
        :param ip_address: IP address on the edge gateway - will be auto-assigned if not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#ip_address Edgegateway#ip_address}
        :param suballocate_pool: suballocate_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#suballocate_pool Edgegateway#suballocate_pool}
        :param use_for_default_route: Defines if this subnet should be used as default gateway for edge. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#use_for_default_route Edgegateway#use_for_default_route}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cfd71dad10d1b437bb7817040510fa7394b095c365f5afddcba2c25525b9cd3)
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument suballocate_pool", value=suballocate_pool, expected_type=type_hints["suballocate_pool"])
            check_type(argname="argument use_for_default_route", value=use_for_default_route, expected_type=type_hints["use_for_default_route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway": gateway,
            "netmask": netmask,
        }
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if suballocate_pool is not None:
            self._values["suballocate_pool"] = suballocate_pool
        if use_for_default_route is not None:
            self._values["use_for_default_route"] = use_for_default_route

    @builtins.property
    def gateway(self) -> builtins.str:
        '''Gateway address for a subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#gateway Edgegateway#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def netmask(self) -> builtins.str:
        '''Netmask address for a subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#netmask Edgegateway#netmask}
        '''
        result = self._values.get("netmask")
        assert result is not None, "Required property 'netmask' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''IP address on the edge gateway - will be auto-assigned if not defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#ip_address Edgegateway#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suballocate_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetworkSubnetSuballocatePool"]]]:
        '''suballocate_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#suballocate_pool Edgegateway#suballocate_pool}
        '''
        result = self._values.get("suballocate_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetworkSubnetSuballocatePool"]]], result)

    @builtins.property
    def use_for_default_route(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines if this subnet should be used as default gateway for edge.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#use_for_default_route Edgegateway#use_for_default_route}
        '''
        result = self._values.get("use_for_default_route")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgegatewayExternalNetworkSubnet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgegatewayExternalNetworkSubnetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetworkSubnetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cdf6472e45395a3eab0d4568edffc7d69b2dae33ca5106910a5cbbfef365f5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EdgegatewayExternalNetworkSubnetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa2ab5602661dd466396e2b915e92c864f6d1a73040deb4acfe3e7f45520746)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EdgegatewayExternalNetworkSubnetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510a109837608dd962209c47bda398d17dce06e384f4800856ca01eb29d03701)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52b790c11ee544af27ff2243b472b55ee64d52f4ae17614874cd769c28a52832)
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
            type_hints = typing.get_type_hints(_typecheckingstub__801aea15b98a07f2abe0d438f5a48418e5c31cb4c28efb7be5e6f99100137103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetworkSubnet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetworkSubnet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetworkSubnet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83fac20c2e5638ddf9ff148c53823f94a8616160e92b5f26869799a10aa0ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EdgegatewayExternalNetworkSubnetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetworkSubnetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__463aa5b42227b9148f59843e9ae32f98d20edd9ac86d89e4c5c3ded661a7f75d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSuballocatePool")
    def put_suballocate_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayExternalNetworkSubnetSuballocatePool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f550cc7b3d7d28640b66d5246e8007aa8de52e53346e4c89066305f8244a8d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSuballocatePool", [value]))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetSuballocatePool")
    def reset_suballocate_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuballocatePool", []))

    @jsii.member(jsii_name="resetUseForDefaultRoute")
    def reset_use_for_default_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseForDefaultRoute", []))

    @builtins.property
    @jsii.member(jsii_name="suballocatePool")
    def suballocate_pool(self) -> "EdgegatewayExternalNetworkSubnetSuballocatePoolList":
        return typing.cast("EdgegatewayExternalNetworkSubnetSuballocatePoolList", jsii.get(self, "suballocatePool"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="netmaskInput")
    def netmask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netmaskInput"))

    @builtins.property
    @jsii.member(jsii_name="suballocatePoolInput")
    def suballocate_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetworkSubnetSuballocatePool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayExternalNetworkSubnetSuballocatePool"]]], jsii.get(self, "suballocatePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="useForDefaultRouteInput")
    def use_for_default_route_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useForDefaultRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce55d7eef148fbf0cdacfed0ee97e842d27580a530ed67e84e3a0ee91e14aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efd192014d7d7d4216063a0f7bfb19363e5f82f2af498e5c1f5743f93b708a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5396c598c837886ec8dc8bf6a640b586ca2c3029c88824c1f3f176d589de6e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="useForDefaultRoute")
    def use_for_default_route(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useForDefaultRoute"))

    @use_for_default_route.setter
    def use_for_default_route(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b87679f87e8737cd83ce14b144c76f3e8c66e31799099808c8fa18951c3f3a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useForDefaultRoute", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetworkSubnet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetworkSubnet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetworkSubnet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716915bfe2c04fbc244cc02357154b2da52a95b1ec13b8c1d664c9cb6505666d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetworkSubnetSuballocatePool",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class EdgegatewayExternalNetworkSubnetSuballocatePool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#end_address Edgegateway#end_address}.
        :param start_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#start_address Edgegateway#start_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8c82e0cb353af573f9e39d97031ac21d2f41eb568a20d743bbe54a910f25f4)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#end_address Edgegateway#end_address}.'''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway#start_address Edgegateway#start_address}.'''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgegatewayExternalNetworkSubnetSuballocatePool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgegatewayExternalNetworkSubnetSuballocatePoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetworkSubnetSuballocatePoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fba8a11390d2eb578f548f7b7eaed3adfdda18ecc3b4230e53976fa9c1b62f4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EdgegatewayExternalNetworkSubnetSuballocatePoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ee3f7d18aae4d63529a83d13aa2d0495921711bb13ebcc67289a6fe386633d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EdgegatewayExternalNetworkSubnetSuballocatePoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36948d88276b7e4859548347c18627b229cd562dee697b4f946da1435a73e1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93df2895111aa57c4a1db920e223e48fe5315966ca499f1afa7f08ac293dfa37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cea291bcbf38ee934ac7e9f5297cb56724fca9283464f338051d07af17adc15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetworkSubnetSuballocatePool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetworkSubnetSuballocatePool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetworkSubnetSuballocatePool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64962454d481870f4275f0ce1c3b54f6dbd56b6b7243437ae854005ee38abc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EdgegatewayExternalNetworkSubnetSuballocatePoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegateway.EdgegatewayExternalNetworkSubnetSuballocatePoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5823fe32c442e2db937c3bb48f7e0eee4e028a624071845f28ff1f18b1f0c0d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endAddressInput")
    def end_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="startAddressInput")
    def start_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="endAddress")
    def end_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endAddress"))

    @end_address.setter
    def end_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5926d9ce46df7fcb4bd72dfe3ad27bc0ff13d075f6ee4955b64488fc30ffb2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8326dc6e59398ffa000c43547b1b5f0dfdfcd2880220bd4112223969d29265ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetworkSubnetSuballocatePool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetworkSubnetSuballocatePool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetworkSubnetSuballocatePool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45917a8b638fe1e8871fce845e7f60dd6273b957bbbbed7b0d90fafba218487f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Edgegateway",
    "EdgegatewayConfig",
    "EdgegatewayExternalNetwork",
    "EdgegatewayExternalNetworkList",
    "EdgegatewayExternalNetworkOutputReference",
    "EdgegatewayExternalNetworkSubnet",
    "EdgegatewayExternalNetworkSubnetList",
    "EdgegatewayExternalNetworkSubnetOutputReference",
    "EdgegatewayExternalNetworkSubnetSuballocatePool",
    "EdgegatewayExternalNetworkSubnetSuballocatePoolList",
    "EdgegatewayExternalNetworkSubnetSuballocatePoolOutputReference",
]

publication.publish()

def _typecheckingstub__94c57953c7ef8514d497bc97d05c6ed98f8729720f1fe9c2b75dd1334e710083(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    configuration: builtins.str,
    external_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayExternalNetwork, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    distributed_routing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fips_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fw_default_rule_action: typing.Optional[builtins.str] = None,
    fw_default_rule_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fw_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lb_acceleration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_loglevel: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    use_default_route_for_dns_relay: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__5e70d3b6e13b669fd6d62e05dc11aad7d84f64a5c10a812b4531186c9589630d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56cc06ef77ed1d4cc2dd8756b1eabcbdd3a70ad2677ba0359bb28d33700367b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayExternalNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7818634732d05f771efbbc3a4805c4900ee29da3c9f5a176c6461bb158e28378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce9914bd0033a829481c61c659b0fbd3a0ae5ba4f6dab8bde7dcf457130edcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2382864093f5800be8e64e238784627740d0b6027b13b8c515c033d9d8c7d656(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb6a8bf99d96ddb7946777e8e64b52d2e544253b6211442df5170e60d9e607f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671b54f094739937d1bc69ed6c6c72bbc412cce9cd3734be4d24887004743959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d11b7c9004ded0eddd45a2dcc28b170c7b669026360209e7f0f0e3446d1b3a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b28ece75903da0cbb58a3103866625f92a0f742937de0d090373f4435e33bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef6b755194a2663d19d4bfd9d4c37e0cf2caa25559853308f92b35f904f25d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c9b383bd5ae7bff916e35c904946c1d0c46ded73b3762ad3c6bde306586f1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be316d58cae0d28186a21328542e0553df13e2413d491b539c1bb88f4109f139(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55dfd86ad2fc4c141bc07a7757d84c77ff4417c0ed14c4f791df4c0e48e5dbc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfdd492953134d720ce049ab7282519d0d917ea3b813931db7d10b7b54b8b54f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b61b65b069af466d7e62a2eb6790584c5ffbaf1ad4441d2cf8a689e5ce00fa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7ddd7fd087657befef6fa165c56ed4bd44f940f38a3c9e995a87b2d6e7310f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dbcb41108768d75536bb1a8cdafe615418ba990e99bb5d59117da26a41dd8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64cb93b38eb438e2be3aff835a156043a147db35970b0fa52842c25c7ac611e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57b9fd4cf9512bcfdc6c932e3abd8a43dca5efb5cdab2f5d6776d8810e17c7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb02f2a2a8f83474d4461958dc9ab0a86aaf3bad800b98219a3d2c190e5c854(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    configuration: builtins.str,
    external_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayExternalNetwork, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    distributed_routing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fips_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fw_default_rule_action: typing.Optional[builtins.str] = None,
    fw_default_rule_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fw_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lb_acceleration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lb_loglevel: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    use_default_route_for_dns_relay: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75f0cc895e10062c23b1ebd2f73d48c5b963448da216a42f41e5bad4acd4cbf(
    *,
    name: builtins.str,
    enable_rate_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    incoming_rate_limit: typing.Optional[jsii.Number] = None,
    outgoing_rate_limit: typing.Optional[jsii.Number] = None,
    subnet: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayExternalNetworkSubnet, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19a3e8df56c246f58baa3560ec9e321cc20293ecc1ab59232f6e9a9e272a40c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4aa45169e57defae555d4640ba57bcbd0c25539c1bc4f6d3144f31497ad6c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7470ce8cdf60c121d2479d0c659b3e8a9f898f37565a50c7c35b41b7e39109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3d6cf9380156ec8e62e88fac03f195c90063e8a4d0e13b95fe30ee51f41d2a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb841ee1546d13ea06d512a3eecebbde6967a5e01aa1e346b0344a7e45ae3be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d396837957eccc617c378c04c08842f5cf720a9603f455e74d51c3ea7dd3911(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86a9e85f6742fb2cb29ff79e4ab9de076424a2e6c9db0e03e31b3bb840fa2bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e0534a0a75fdf263132cda42e7fb2f42429c5200363c8f059f2f0adff00060(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayExternalNetworkSubnet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f781f4c12da3fd6c78bb8bcfb412bb74afbd723b145ae3e84a92fa02067780(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bc83b4d5b51f91048bb5e81a42346ee3d6d35fb3d1627fe95f0b31fcbcfd5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800fcf4a9b3508c1b32924bfa4458c73538cd805ecec51360bbf1f14042d29ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b238ff4534c71f1539328ceb2fd5c158cf4d6d1489c1f78ecaa995e071e9958f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5332743e22543f05f86e76b069cc0f685bb59b8f6bffb271a4a5b4a23e8f7136(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cfd71dad10d1b437bb7817040510fa7394b095c365f5afddcba2c25525b9cd3(
    *,
    gateway: builtins.str,
    netmask: builtins.str,
    ip_address: typing.Optional[builtins.str] = None,
    suballocate_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayExternalNetworkSubnetSuballocatePool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    use_for_default_route: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdf6472e45395a3eab0d4568edffc7d69b2dae33ca5106910a5cbbfef365f5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa2ab5602661dd466396e2b915e92c864f6d1a73040deb4acfe3e7f45520746(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510a109837608dd962209c47bda398d17dce06e384f4800856ca01eb29d03701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b790c11ee544af27ff2243b472b55ee64d52f4ae17614874cd769c28a52832(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801aea15b98a07f2abe0d438f5a48418e5c31cb4c28efb7be5e6f99100137103(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83fac20c2e5638ddf9ff148c53823f94a8616160e92b5f26869799a10aa0ec5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetworkSubnet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463aa5b42227b9148f59843e9ae32f98d20edd9ac86d89e4c5c3ded661a7f75d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f550cc7b3d7d28640b66d5246e8007aa8de52e53346e4c89066305f8244a8d01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayExternalNetworkSubnetSuballocatePool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce55d7eef148fbf0cdacfed0ee97e842d27580a530ed67e84e3a0ee91e14aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efd192014d7d7d4216063a0f7bfb19363e5f82f2af498e5c1f5743f93b708a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5396c598c837886ec8dc8bf6a640b586ca2c3029c88824c1f3f176d589de6e02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b87679f87e8737cd83ce14b144c76f3e8c66e31799099808c8fa18951c3f3a8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716915bfe2c04fbc244cc02357154b2da52a95b1ec13b8c1d664c9cb6505666d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetworkSubnet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8c82e0cb353af573f9e39d97031ac21d2f41eb568a20d743bbe54a910f25f4(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba8a11390d2eb578f548f7b7eaed3adfdda18ecc3b4230e53976fa9c1b62f4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ee3f7d18aae4d63529a83d13aa2d0495921711bb13ebcc67289a6fe386633d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36948d88276b7e4859548347c18627b229cd562dee697b4f946da1435a73e1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93df2895111aa57c4a1db920e223e48fe5315966ca499f1afa7f08ac293dfa37(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cea291bcbf38ee934ac7e9f5297cb56724fca9283464f338051d07af17adc15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64962454d481870f4275f0ce1c3b54f6dbd56b6b7243437ae854005ee38abc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayExternalNetworkSubnetSuballocatePool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5823fe32c442e2db937c3bb48f7e0eee4e028a624071845f28ff1f18b1f0c0d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5926d9ce46df7fcb4bd72dfe3ad27bc0ff13d075f6ee4955b64488fc30ffb2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8326dc6e59398ffa000c43547b1b5f0dfdfcd2880220bd4112223969d29265ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45917a8b638fe1e8871fce845e7f60dd6273b957bbbbed7b0d90fafba218487f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayExternalNetworkSubnetSuballocatePool]],
) -> None:
    """Type checking stubs"""
    pass
