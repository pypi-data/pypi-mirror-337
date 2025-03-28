'''
# `vcd_nsxt_nat_rule`

Refer to the Terraform Registry for docs: [`vcd_nsxt_nat_rule`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule).
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


class NsxtNatRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtNatRule.NsxtNatRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule vcd_nsxt_nat_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway_id: builtins.str,
        name: builtins.str,
        rule_type: builtins.str,
        app_port_profile_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        dnat_external_port: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_address: typing.Optional[builtins.str] = None,
        firewall_match: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        internal_address: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        snat_destination_address: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule vcd_nsxt_nat_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway_id: Edge gateway name in which NAT Rule is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#edge_gateway_id NsxtNatRule#edge_gateway_id}
        :param name: Name of NAT rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#name NsxtNatRule#name}
        :param rule_type: Rule type - one of 'DNAT', 'NO_DNAT', 'SNAT', 'NO_SNAT', 'REFLEXIVE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#rule_type NsxtNatRule#rule_type}
        :param app_port_profile_id: Application Port Profile to apply for this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#app_port_profile_id NsxtNatRule#app_port_profile_id}
        :param description: Description of NAT rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#description NsxtNatRule#description}
        :param dnat_external_port: For DNAT only. Enter a port into which the DNAT rule is translating for the packets inbound to the virtual machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#dnat_external_port NsxtNatRule#dnat_external_port}
        :param enabled: Enables or disables this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#enabled NsxtNatRule#enabled}
        :param external_address: IP address or CIDR of external network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#external_address NsxtNatRule#external_address}
        :param firewall_match: VCD 10.2.2+ Determines how the firewall matches the address during NATing if firewall stage is not skipped. One of 'MATCH_INTERNAL_ADDRESS', 'MATCH_EXTERNAL_ADDRESS', 'BYPASS'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#firewall_match NsxtNatRule#firewall_match}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#id NsxtNatRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internal_address: IP address or CIDR of the virtual machines for which you are configuring NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#internal_address NsxtNatRule#internal_address}
        :param logging: Enable logging when this rule is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#logging NsxtNatRule#logging}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#org NsxtNatRule#org}
        :param priority: VCD 10.2.2+ If an address has multiple NAT rules, the rule with the highest priority is applied. A lower value means a higher precedence for this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#priority NsxtNatRule#priority}
        :param snat_destination_address: For SNAT only. If you want the rule to apply only for traffic to a specific domain, enter an IP address for this domain or an IP address range in CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#snat_destination_address NsxtNatRule#snat_destination_address}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#vdc NsxtNatRule#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab8c47b4c13229117fef7ebc910ef942886d11a6c7225b17c4e2b05fa452950)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtNatRuleConfig(
            edge_gateway_id=edge_gateway_id,
            name=name,
            rule_type=rule_type,
            app_port_profile_id=app_port_profile_id,
            description=description,
            dnat_external_port=dnat_external_port,
            enabled=enabled,
            external_address=external_address,
            firewall_match=firewall_match,
            id=id,
            internal_address=internal_address,
            logging=logging,
            org=org,
            priority=priority,
            snat_destination_address=snat_destination_address,
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
        '''Generates CDKTF code for importing a NsxtNatRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtNatRule to import.
        :param import_from_id: The id of the existing NsxtNatRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtNatRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0a642bec525a0fee304f57e39e88214be4fddcd678e473a1b6b3012227b551)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAppPortProfileId")
    def reset_app_port_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppPortProfileId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDnatExternalPort")
    def reset_dnat_external_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnatExternalPort", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetExternalAddress")
    def reset_external_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAddress", []))

    @jsii.member(jsii_name="resetFirewallMatch")
    def reset_firewall_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewallMatch", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInternalAddress")
    def reset_internal_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalAddress", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetSnatDestinationAddress")
    def reset_snat_destination_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnatDestinationAddress", []))

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
    @jsii.member(jsii_name="appPortProfileIdInput")
    def app_port_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appPortProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dnatExternalPortInput")
    def dnat_external_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnatExternalPortInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayIdInput")
    def edge_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAddressInput")
    def external_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallMatchInput")
    def firewall_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="internalAddressInput")
    def internal_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleTypeInput")
    def rule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="snatDestinationAddressInput")
    def snat_destination_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snatDestinationAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="appPortProfileId")
    def app_port_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appPortProfileId"))

    @app_port_profile_id.setter
    def app_port_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665a67d7c68ca6afbff216090ce605cc0ac81d50e9ba4c8e60cf5cdcc943b00e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appPortProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11cc685bb54e7e6c0ec9a514cff4652d59adeb2ec830c421323955422f9d4418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="dnatExternalPort")
    def dnat_external_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnatExternalPort"))

    @dnat_external_port.setter
    def dnat_external_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a717909a3a221e7cff5f27da8fdef012fbb341e47c861b475ea155a32e48e221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnatExternalPort", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayId")
    def edge_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGatewayId"))

    @edge_gateway_id.setter
    def edge_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135d81f7e16d690357d31058c85b8c5c060a517ea3def08e70b745ad937a41a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGatewayId", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__73c1461b06a0c23c11998da002a8a67501123f5f81077b5e77b15e261f374151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="externalAddress")
    def external_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAddress"))

    @external_address.setter
    def external_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e964c1590d9a6d67fb65359a516cf5e808a63ee99f621355b4d29e359e35f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAddress", value)

    @builtins.property
    @jsii.member(jsii_name="firewallMatch")
    def firewall_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallMatch"))

    @firewall_match.setter
    def firewall_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf6c044bc8bdc5f96a922fa2fb3c3ba18b68e7b5609439ae0ebf0ac8749dfc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallMatch", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2ade3ba815ec94a8acbcc88a28064d43a16c1681d333d7fe0c584ee91a752a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="internalAddress")
    def internal_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalAddress"))

    @internal_address.setter
    def internal_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5223474810d324d72bee3eb5e7ab9f8fb51aa8aa370a32f129d88ccdd01d8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalAddress", value)

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logging"))

    @logging.setter
    def logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5558ea41734a22839469c2a722c8145dfa8fc3ff2bf9737bfae333367897dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0920d6ab34587b1224ef7336ddf9ff78bf8282922de125b505255a9e9ea687b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8307eb390de5309b1d341ddb19dec71ec23361a52992e5db216888637a9b0d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b805c513c5bcd209d4949de8590660d09a185ebd5eebb52d0ed3ec8fe2bccfda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ece886e4192b3e401c10c9574cb02aa8a4781b20446fd36321b2f8c03e872a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="snatDestinationAddress")
    def snat_destination_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snatDestinationAddress"))

    @snat_destination_address.setter
    def snat_destination_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3ad9a92686b97f52de88177fcf516ab6834d72106e737f240b190bc4357fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snatDestinationAddress", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c486c04d9045e5916f6e6a19823d29e18a82504704a664d66f99ecea5c3c3b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.nsxtNatRule.NsxtNatRuleConfig",
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
        "name": "name",
        "rule_type": "ruleType",
        "app_port_profile_id": "appPortProfileId",
        "description": "description",
        "dnat_external_port": "dnatExternalPort",
        "enabled": "enabled",
        "external_address": "externalAddress",
        "firewall_match": "firewallMatch",
        "id": "id",
        "internal_address": "internalAddress",
        "logging": "logging",
        "org": "org",
        "priority": "priority",
        "snat_destination_address": "snatDestinationAddress",
        "vdc": "vdc",
    },
)
class NsxtNatRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        edge_gateway_id: builtins.str,
        name: builtins.str,
        rule_type: builtins.str,
        app_port_profile_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        dnat_external_port: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_address: typing.Optional[builtins.str] = None,
        firewall_match: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        internal_address: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        snat_destination_address: typing.Optional[builtins.str] = None,
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
        :param edge_gateway_id: Edge gateway name in which NAT Rule is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#edge_gateway_id NsxtNatRule#edge_gateway_id}
        :param name: Name of NAT rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#name NsxtNatRule#name}
        :param rule_type: Rule type - one of 'DNAT', 'NO_DNAT', 'SNAT', 'NO_SNAT', 'REFLEXIVE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#rule_type NsxtNatRule#rule_type}
        :param app_port_profile_id: Application Port Profile to apply for this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#app_port_profile_id NsxtNatRule#app_port_profile_id}
        :param description: Description of NAT rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#description NsxtNatRule#description}
        :param dnat_external_port: For DNAT only. Enter a port into which the DNAT rule is translating for the packets inbound to the virtual machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#dnat_external_port NsxtNatRule#dnat_external_port}
        :param enabled: Enables or disables this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#enabled NsxtNatRule#enabled}
        :param external_address: IP address or CIDR of external network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#external_address NsxtNatRule#external_address}
        :param firewall_match: VCD 10.2.2+ Determines how the firewall matches the address during NATing if firewall stage is not skipped. One of 'MATCH_INTERNAL_ADDRESS', 'MATCH_EXTERNAL_ADDRESS', 'BYPASS'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#firewall_match NsxtNatRule#firewall_match}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#id NsxtNatRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internal_address: IP address or CIDR of the virtual machines for which you are configuring NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#internal_address NsxtNatRule#internal_address}
        :param logging: Enable logging when this rule is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#logging NsxtNatRule#logging}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#org NsxtNatRule#org}
        :param priority: VCD 10.2.2+ If an address has multiple NAT rules, the rule with the highest priority is applied. A lower value means a higher precedence for this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#priority NsxtNatRule#priority}
        :param snat_destination_address: For SNAT only. If you want the rule to apply only for traffic to a specific domain, enter an IP address for this domain or an IP address range in CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#snat_destination_address NsxtNatRule#snat_destination_address}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#vdc NsxtNatRule#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711bad87ef97c00a5d45875bc617d51352bf2c9ad0c89f927ee0768b252162e5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway_id", value=edge_gateway_id, expected_type=type_hints["edge_gateway_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule_type", value=rule_type, expected_type=type_hints["rule_type"])
            check_type(argname="argument app_port_profile_id", value=app_port_profile_id, expected_type=type_hints["app_port_profile_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dnat_external_port", value=dnat_external_port, expected_type=type_hints["dnat_external_port"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument external_address", value=external_address, expected_type=type_hints["external_address"])
            check_type(argname="argument firewall_match", value=firewall_match, expected_type=type_hints["firewall_match"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument internal_address", value=internal_address, expected_type=type_hints["internal_address"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument snat_destination_address", value=snat_destination_address, expected_type=type_hints["snat_destination_address"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway_id": edge_gateway_id,
            "name": name,
            "rule_type": rule_type,
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
        if app_port_profile_id is not None:
            self._values["app_port_profile_id"] = app_port_profile_id
        if description is not None:
            self._values["description"] = description
        if dnat_external_port is not None:
            self._values["dnat_external_port"] = dnat_external_port
        if enabled is not None:
            self._values["enabled"] = enabled
        if external_address is not None:
            self._values["external_address"] = external_address
        if firewall_match is not None:
            self._values["firewall_match"] = firewall_match
        if id is not None:
            self._values["id"] = id
        if internal_address is not None:
            self._values["internal_address"] = internal_address
        if logging is not None:
            self._values["logging"] = logging
        if org is not None:
            self._values["org"] = org
        if priority is not None:
            self._values["priority"] = priority
        if snat_destination_address is not None:
            self._values["snat_destination_address"] = snat_destination_address
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
    def edge_gateway_id(self) -> builtins.str:
        '''Edge gateway name in which NAT Rule is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#edge_gateway_id NsxtNatRule#edge_gateway_id}
        '''
        result = self._values.get("edge_gateway_id")
        assert result is not None, "Required property 'edge_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of NAT rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#name NsxtNatRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_type(self) -> builtins.str:
        '''Rule type - one of 'DNAT', 'NO_DNAT', 'SNAT', 'NO_SNAT', 'REFLEXIVE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#rule_type NsxtNatRule#rule_type}
        '''
        result = self._values.get("rule_type")
        assert result is not None, "Required property 'rule_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_port_profile_id(self) -> typing.Optional[builtins.str]:
        '''Application Port Profile to apply for this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#app_port_profile_id NsxtNatRule#app_port_profile_id}
        '''
        result = self._values.get("app_port_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of NAT rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#description NsxtNatRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dnat_external_port(self) -> typing.Optional[builtins.str]:
        '''For DNAT only.

        Enter a port into which the DNAT rule is translating for the packets inbound to the virtual machines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#dnat_external_port NsxtNatRule#dnat_external_port}
        '''
        result = self._values.get("dnat_external_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables or disables this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#enabled NsxtNatRule#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_address(self) -> typing.Optional[builtins.str]:
        '''IP address or CIDR of external network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#external_address NsxtNatRule#external_address}
        '''
        result = self._values.get("external_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_match(self) -> typing.Optional[builtins.str]:
        '''VCD 10.2.2+ Determines how the firewall matches the address during NATing if firewall stage is not skipped. One of 'MATCH_INTERNAL_ADDRESS', 'MATCH_EXTERNAL_ADDRESS', 'BYPASS'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#firewall_match NsxtNatRule#firewall_match}
        '''
        result = self._values.get("firewall_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#id NsxtNatRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_address(self) -> typing.Optional[builtins.str]:
        '''IP address or CIDR of the virtual machines for which you are configuring NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#internal_address NsxtNatRule#internal_address}
        '''
        result = self._values.get("internal_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable logging when this rule is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#logging NsxtNatRule#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#org NsxtNatRule#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''VCD 10.2.2+ If an address has multiple NAT rules, the rule with the highest priority is applied. A lower value means a higher precedence for this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#priority NsxtNatRule#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snat_destination_address(self) -> typing.Optional[builtins.str]:
        '''For SNAT only.

        If you want the rule to apply only for traffic to a specific domain, enter an IP address for this domain or an IP address range in CIDR format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#snat_destination_address NsxtNatRule#snat_destination_address}
        '''
        result = self._values.get("snat_destination_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_nat_rule#vdc NsxtNatRule#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtNatRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NsxtNatRule",
    "NsxtNatRuleConfig",
]

publication.publish()

def _typecheckingstub__9ab8c47b4c13229117fef7ebc910ef942886d11a6c7225b17c4e2b05fa452950(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway_id: builtins.str,
    name: builtins.str,
    rule_type: builtins.str,
    app_port_profile_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    dnat_external_port: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_address: typing.Optional[builtins.str] = None,
    firewall_match: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    internal_address: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    snat_destination_address: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6c0a642bec525a0fee304f57e39e88214be4fddcd678e473a1b6b3012227b551(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665a67d7c68ca6afbff216090ce605cc0ac81d50e9ba4c8e60cf5cdcc943b00e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11cc685bb54e7e6c0ec9a514cff4652d59adeb2ec830c421323955422f9d4418(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a717909a3a221e7cff5f27da8fdef012fbb341e47c861b475ea155a32e48e221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135d81f7e16d690357d31058c85b8c5c060a517ea3def08e70b745ad937a41a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c1461b06a0c23c11998da002a8a67501123f5f81077b5e77b15e261f374151(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e964c1590d9a6d67fb65359a516cf5e808a63ee99f621355b4d29e359e35f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf6c044bc8bdc5f96a922fa2fb3c3ba18b68e7b5609439ae0ebf0ac8749dfc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2ade3ba815ec94a8acbcc88a28064d43a16c1681d333d7fe0c584ee91a752a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5223474810d324d72bee3eb5e7ab9f8fb51aa8aa370a32f129d88ccdd01d8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5558ea41734a22839469c2a722c8145dfa8fc3ff2bf9737bfae333367897dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0920d6ab34587b1224ef7336ddf9ff78bf8282922de125b505255a9e9ea687b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8307eb390de5309b1d341ddb19dec71ec23361a52992e5db216888637a9b0d77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b805c513c5bcd209d4949de8590660d09a185ebd5eebb52d0ed3ec8fe2bccfda(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ece886e4192b3e401c10c9574cb02aa8a4781b20446fd36321b2f8c03e872a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3ad9a92686b97f52de88177fcf516ab6834d72106e737f240b190bc4357fc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c486c04d9045e5916f6e6a19823d29e18a82504704a664d66f99ecea5c3c3b59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711bad87ef97c00a5d45875bc617d51352bf2c9ad0c89f927ee0768b252162e5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway_id: builtins.str,
    name: builtins.str,
    rule_type: builtins.str,
    app_port_profile_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    dnat_external_port: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_address: typing.Optional[builtins.str] = None,
    firewall_match: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    internal_address: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    snat_destination_address: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
