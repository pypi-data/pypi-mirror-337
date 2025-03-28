'''
# `vcd_nsxv_firewall_rule`

Refer to the Terraform Registry for docs: [`vcd_nsxv_firewall_rule`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule).
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


class NsxvFirewallRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule vcd_nsxv_firewall_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination: typing.Union["NsxvFirewallRuleDestination", typing.Dict[builtins.str, typing.Any]],
        edge_gateway: builtins.str,
        service: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxvFirewallRuleService", typing.Dict[builtins.str, typing.Any]]]],
        source: typing.Union["NsxvFirewallRuleSource", typing.Dict[builtins.str, typing.Any]],
        above_rule_id: typing.Optional[builtins.str] = None,
        action: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        rule_tag: typing.Optional[jsii.Number] = None,
        rule_type: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule vcd_nsxv_firewall_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#destination NsxvFirewallRule#destination}
        :param edge_gateway: Edge gateway name in which Firewall Rule is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#edge_gateway NsxvFirewallRule#edge_gateway}
        :param service: service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#service NsxvFirewallRule#service}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#source NsxvFirewallRule#source}
        :param above_rule_id: This firewall rule will be inserted above the referred one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#above_rule_id NsxvFirewallRule#above_rule_id}
        :param action: 'accept' or 'deny'. Default 'accept'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#action NsxvFirewallRule#action}
        :param enabled: Whether the rule should be enabled. Default 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#enabled NsxvFirewallRule#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#id NsxvFirewallRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_enabled: Whether logging should be enabled for this rule. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#logging_enabled NsxvFirewallRule#logging_enabled}
        :param name: Firewall rule name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#name NsxvFirewallRule#name}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org NsxvFirewallRule#org}
        :param rule_tag: Optional. Allows to set custom rule tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#rule_tag NsxvFirewallRule#rule_tag}
        :param rule_type: Read only. Possible values 'user', 'internal_high'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#rule_type NsxvFirewallRule#rule_type}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vdc NsxvFirewallRule#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeece478c7f2e329d74dbc4c68876b93e9a1d009ac203a63e90de1753fcbd56a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxvFirewallRuleConfig(
            destination=destination,
            edge_gateway=edge_gateway,
            service=service,
            source=source,
            above_rule_id=above_rule_id,
            action=action,
            enabled=enabled,
            id=id,
            logging_enabled=logging_enabled,
            name=name,
            org=org,
            rule_tag=rule_tag,
            rule_type=rule_type,
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
        '''Generates CDKTF code for importing a NsxvFirewallRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxvFirewallRule to import.
        :param import_from_id: The id of the existing NsxvFirewallRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxvFirewallRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904514826a73af81052bc971cece1ccbd82b35d8402d029dd3db0960efc94a40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        exclude: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gateway_interfaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
        org_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude: Rule is applied to traffic going to any destinations except for the excluded destination. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#exclude NsxvFirewallRule#exclude}
        :param gateway_interfaces: 'vse', 'internal', 'external' or network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#gateway_interfaces NsxvFirewallRule#gateway_interfaces}
        :param ip_addresses: IP address, CIDR, an IP range, or the keyword 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_addresses NsxvFirewallRule#ip_addresses}
        :param ip_sets: Set of IP set names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_sets NsxvFirewallRule#ip_sets}
        :param org_networks: Set of org network names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org_networks NsxvFirewallRule#org_networks}
        :param vm_ids: Set of VM IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vm_ids NsxvFirewallRule#vm_ids}
        '''
        value = NsxvFirewallRuleDestination(
            exclude=exclude,
            gateway_interfaces=gateway_interfaces,
            ip_addresses=ip_addresses,
            ip_sets=ip_sets,
            org_networks=org_networks,
            vm_ids=vm_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="putService")
    def put_service(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxvFirewallRuleService", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b652ff4f32a8b269d07148b8fd437776c3d8fab802d74820772ddd0f327847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putService", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        exclude: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gateway_interfaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
        org_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude: Rule is applied to traffic coming from all sources except for the excluded source. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#exclude NsxvFirewallRule#exclude}
        :param gateway_interfaces: 'vse', 'internal', 'external' or network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#gateway_interfaces NsxvFirewallRule#gateway_interfaces}
        :param ip_addresses: IP address, CIDR, an IP range, or the keyword 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_addresses NsxvFirewallRule#ip_addresses}
        :param ip_sets: Set of IP set names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_sets NsxvFirewallRule#ip_sets}
        :param org_networks: Set of org network names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org_networks NsxvFirewallRule#org_networks}
        :param vm_ids: Set of VM IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vm_ids NsxvFirewallRule#vm_ids}
        '''
        value = NsxvFirewallRuleSource(
            exclude=exclude,
            gateway_interfaces=gateway_interfaces,
            ip_addresses=ip_addresses,
            ip_sets=ip_sets,
            org_networks=org_networks,
            vm_ids=vm_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetAboveRuleId")
    def reset_above_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAboveRuleId", []))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingEnabled")
    def reset_logging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetRuleTag")
    def reset_rule_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleTag", []))

    @jsii.member(jsii_name="resetRuleType")
    def reset_rule_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleType", []))

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
    @jsii.member(jsii_name="destination")
    def destination(self) -> "NsxvFirewallRuleDestinationOutputReference":
        return typing.cast("NsxvFirewallRuleDestinationOutputReference", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "NsxvFirewallRuleServiceList":
        return typing.cast("NsxvFirewallRuleServiceList", jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "NsxvFirewallRuleSourceOutputReference":
        return typing.cast("NsxvFirewallRuleSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="aboveRuleIdInput")
    def above_rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aboveRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional["NsxvFirewallRuleDestination"]:
        return typing.cast(typing.Optional["NsxvFirewallRuleDestination"], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayInput")
    def edge_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayInput"))

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
    @jsii.member(jsii_name="loggingEnabledInput")
    def logging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleTagInput")
    def rule_tag_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleTagInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleTypeInput")
    def rule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxvFirewallRuleService"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxvFirewallRuleService"]]], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["NsxvFirewallRuleSource"]:
        return typing.cast(typing.Optional["NsxvFirewallRuleSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="aboveRuleId")
    def above_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aboveRuleId"))

    @above_rule_id.setter
    def above_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dbd185ae2752ec9dfeda7fd0a953a04fbf6188e5839dcd1beb2fe14671f7e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aboveRuleId", value)

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7afc9e692d989bb18054d56787771257509cf4a7de7d77ca79e825c15eda53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGateway")
    def edge_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGateway"))

    @edge_gateway.setter
    def edge_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90055a6736f0a6bccf23ba446987d85522a2497760481aeb3444d00a400c9291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGateway", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__191f82b9185dd7aa5d2ad75fe26fdc88e548c241f966322dc7a652ed249b7761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02215c0e0c60435cfed6c7c57162933fafb7d9a458c5996c258d7daf6c0b9443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="loggingEnabled")
    def logging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "loggingEnabled"))

    @logging_enabled.setter
    def logging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775e5d68ecd42af15915b4bdae46d9fc7630a94317220b7ffada465e083743e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c33060d3bf1591732d2e6278ff50340c6c534e8c283ada2817d22bf82541940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01cb04f25da79ef2592e1dc43755fa5c7a008d4131253c87c88d38ecaee8a16e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="ruleTag")
    def rule_tag(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleTag"))

    @rule_tag.setter
    def rule_tag(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c87912789b43235a06b570605495697a09862bcf250dc87118e29fd9c790c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleTag", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5815d72a2428f0ed73d00fbead3c32045cbb6256cc7bd5348699fb8b71602d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b60bb1b340bca1bb45d4ed50a268bcbdec500990372bdd62af72ea7dec7901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination": "destination",
        "edge_gateway": "edgeGateway",
        "service": "service",
        "source": "source",
        "above_rule_id": "aboveRuleId",
        "action": "action",
        "enabled": "enabled",
        "id": "id",
        "logging_enabled": "loggingEnabled",
        "name": "name",
        "org": "org",
        "rule_tag": "ruleTag",
        "rule_type": "ruleType",
        "vdc": "vdc",
    },
)
class NsxvFirewallRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination: typing.Union["NsxvFirewallRuleDestination", typing.Dict[builtins.str, typing.Any]],
        edge_gateway: builtins.str,
        service: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxvFirewallRuleService", typing.Dict[builtins.str, typing.Any]]]],
        source: typing.Union["NsxvFirewallRuleSource", typing.Dict[builtins.str, typing.Any]],
        above_rule_id: typing.Optional[builtins.str] = None,
        action: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        rule_tag: typing.Optional[jsii.Number] = None,
        rule_type: typing.Optional[builtins.str] = None,
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
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#destination NsxvFirewallRule#destination}
        :param edge_gateway: Edge gateway name in which Firewall Rule is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#edge_gateway NsxvFirewallRule#edge_gateway}
        :param service: service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#service NsxvFirewallRule#service}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#source NsxvFirewallRule#source}
        :param above_rule_id: This firewall rule will be inserted above the referred one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#above_rule_id NsxvFirewallRule#above_rule_id}
        :param action: 'accept' or 'deny'. Default 'accept'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#action NsxvFirewallRule#action}
        :param enabled: Whether the rule should be enabled. Default 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#enabled NsxvFirewallRule#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#id NsxvFirewallRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_enabled: Whether logging should be enabled for this rule. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#logging_enabled NsxvFirewallRule#logging_enabled}
        :param name: Firewall rule name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#name NsxvFirewallRule#name}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org NsxvFirewallRule#org}
        :param rule_tag: Optional. Allows to set custom rule tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#rule_tag NsxvFirewallRule#rule_tag}
        :param rule_type: Read only. Possible values 'user', 'internal_high'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#rule_type NsxvFirewallRule#rule_type}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vdc NsxvFirewallRule#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination, dict):
            destination = NsxvFirewallRuleDestination(**destination)
        if isinstance(source, dict):
            source = NsxvFirewallRuleSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22067aecfe3c2abbba31557ce8eedd12bad45b4cc86e3c1d49f3e3e0d1bab672)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument edge_gateway", value=edge_gateway, expected_type=type_hints["edge_gateway"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument above_rule_id", value=above_rule_id, expected_type=type_hints["above_rule_id"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_enabled", value=logging_enabled, expected_type=type_hints["logging_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument rule_tag", value=rule_tag, expected_type=type_hints["rule_tag"])
            check_type(argname="argument rule_type", value=rule_type, expected_type=type_hints["rule_type"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "edge_gateway": edge_gateway,
            "service": service,
            "source": source,
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
        if above_rule_id is not None:
            self._values["above_rule_id"] = above_rule_id
        if action is not None:
            self._values["action"] = action
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if logging_enabled is not None:
            self._values["logging_enabled"] = logging_enabled
        if name is not None:
            self._values["name"] = name
        if org is not None:
            self._values["org"] = org
        if rule_tag is not None:
            self._values["rule_tag"] = rule_tag
        if rule_type is not None:
            self._values["rule_type"] = rule_type
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
    def destination(self) -> "NsxvFirewallRuleDestination":
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#destination NsxvFirewallRule#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("NsxvFirewallRuleDestination", result)

    @builtins.property
    def edge_gateway(self) -> builtins.str:
        '''Edge gateway name in which Firewall Rule is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#edge_gateway NsxvFirewallRule#edge_gateway}
        '''
        result = self._values.get("edge_gateway")
        assert result is not None, "Required property 'edge_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxvFirewallRuleService"]]:
        '''service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#service NsxvFirewallRule#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxvFirewallRuleService"]], result)

    @builtins.property
    def source(self) -> "NsxvFirewallRuleSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#source NsxvFirewallRule#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("NsxvFirewallRuleSource", result)

    @builtins.property
    def above_rule_id(self) -> typing.Optional[builtins.str]:
        '''This firewall rule will be inserted above the referred one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#above_rule_id NsxvFirewallRule#above_rule_id}
        '''
        result = self._values.get("above_rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        ''''accept' or 'deny'. Default 'accept'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#action NsxvFirewallRule#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the rule should be enabled. Default 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#enabled NsxvFirewallRule#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#id NsxvFirewallRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether logging should be enabled for this rule. Default 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#logging_enabled NsxvFirewallRule#logging_enabled}
        '''
        result = self._values.get("logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Firewall rule name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#name NsxvFirewallRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org NsxvFirewallRule#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_tag(self) -> typing.Optional[jsii.Number]:
        '''Optional. Allows to set custom rule tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#rule_tag NsxvFirewallRule#rule_tag}
        '''
        result = self._values.get("rule_tag")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_type(self) -> typing.Optional[builtins.str]:
        '''Read only. Possible values 'user', 'internal_high'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#rule_type NsxvFirewallRule#rule_type}
        '''
        result = self._values.get("rule_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vdc NsxvFirewallRule#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxvFirewallRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRuleDestination",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "gateway_interfaces": "gatewayInterfaces",
        "ip_addresses": "ipAddresses",
        "ip_sets": "ipSets",
        "org_networks": "orgNetworks",
        "vm_ids": "vmIds",
    },
)
class NsxvFirewallRuleDestination:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gateway_interfaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
        org_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude: Rule is applied to traffic going to any destinations except for the excluded destination. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#exclude NsxvFirewallRule#exclude}
        :param gateway_interfaces: 'vse', 'internal', 'external' or network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#gateway_interfaces NsxvFirewallRule#gateway_interfaces}
        :param ip_addresses: IP address, CIDR, an IP range, or the keyword 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_addresses NsxvFirewallRule#ip_addresses}
        :param ip_sets: Set of IP set names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_sets NsxvFirewallRule#ip_sets}
        :param org_networks: Set of org network names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org_networks NsxvFirewallRule#org_networks}
        :param vm_ids: Set of VM IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vm_ids NsxvFirewallRule#vm_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bac3c5ce82c13183ea4e8b2dbad5a53d16c41c4d0fffbf10b1bb15a88cfabde)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument gateway_interfaces", value=gateway_interfaces, expected_type=type_hints["gateway_interfaces"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument ip_sets", value=ip_sets, expected_type=type_hints["ip_sets"])
            check_type(argname="argument org_networks", value=org_networks, expected_type=type_hints["org_networks"])
            check_type(argname="argument vm_ids", value=vm_ids, expected_type=type_hints["vm_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if gateway_interfaces is not None:
            self._values["gateway_interfaces"] = gateway_interfaces
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if ip_sets is not None:
            self._values["ip_sets"] = ip_sets
        if org_networks is not None:
            self._values["org_networks"] = org_networks
        if vm_ids is not None:
            self._values["vm_ids"] = vm_ids

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Rule is applied to traffic going to any destinations except for the excluded destination. Default 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#exclude NsxvFirewallRule#exclude}
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gateway_interfaces(self) -> typing.Optional[typing.List[builtins.str]]:
        ''''vse', 'internal', 'external' or network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#gateway_interfaces NsxvFirewallRule#gateway_interfaces}
        '''
        result = self._values.get("gateway_interfaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP address, CIDR, an IP range, or the keyword 'any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_addresses NsxvFirewallRule#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_sets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of IP set names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_sets NsxvFirewallRule#ip_sets}
        '''
        result = self._values.get("ip_sets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def org_networks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of org network names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org_networks NsxvFirewallRule#org_networks}
        '''
        result = self._values.get("org_networks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vm_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of VM IDs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vm_ids NsxvFirewallRule#vm_ids}
        '''
        result = self._values.get("vm_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxvFirewallRuleDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxvFirewallRuleDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRuleDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b84ce763cdace292381975f24da00f4f4b0011709a0f11fd6376aa005d64ed9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExclude")
    def reset_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclude", []))

    @jsii.member(jsii_name="resetGatewayInterfaces")
    def reset_gateway_interfaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayInterfaces", []))

    @jsii.member(jsii_name="resetIpAddresses")
    def reset_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddresses", []))

    @jsii.member(jsii_name="resetIpSets")
    def reset_ip_sets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpSets", []))

    @jsii.member(jsii_name="resetOrgNetworks")
    def reset_org_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgNetworks", []))

    @jsii.member(jsii_name="resetVmIds")
    def reset_vm_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmIds", []))

    @builtins.property
    @jsii.member(jsii_name="excludeInput")
    def exclude_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInterfacesInput")
    def gateway_interfaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gatewayInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSetsInput")
    def ip_sets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipSetsInput"))

    @builtins.property
    @jsii.member(jsii_name="orgNetworksInput")
    def org_networks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "orgNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="vmIdsInput")
    def vm_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vmIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="exclude")
    def exclude(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "exclude"))

    @exclude.setter
    def exclude(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec94c3d12901ec8eecb627746853918b20ccb01ecd182e6acc72a8ff03c0cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclude", value)

    @builtins.property
    @jsii.member(jsii_name="gatewayInterfaces")
    def gateway_interfaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gatewayInterfaces"))

    @gateway_interfaces.setter
    def gateway_interfaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143d6672a5d3bb23b00d556565195c048be9018f77c0c1d1e0c7a0d0b71cd01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayInterfaces", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb0f0ed0461697613f137fb9f2b32b2c3ed4aa572e9ce6e12bfd0f50d3156d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="ipSets")
    def ip_sets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipSets"))

    @ip_sets.setter
    def ip_sets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72a50ec7286697e104a65ccff1aa3f6a3268397ae1157f5385b1dcff6f14771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSets", value)

    @builtins.property
    @jsii.member(jsii_name="orgNetworks")
    def org_networks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "orgNetworks"))

    @org_networks.setter
    def org_networks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db8fa9cb9b230d478ec692b69edcfda5f75706537876ae171dd77124df59aab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgNetworks", value)

    @builtins.property
    @jsii.member(jsii_name="vmIds")
    def vm_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vmIds"))

    @vm_ids.setter
    def vm_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe89cb51cdfcdb82ef058a46a340dfc6e1c5ab7c21a6b2f01714d0c0e6263d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NsxvFirewallRuleDestination]:
        return typing.cast(typing.Optional[NsxvFirewallRuleDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxvFirewallRuleDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89bea6cb21973fd6963282d25e3c7758bd4e79d8e29a02d404d7fad831619aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRuleService",
    jsii_struct_bases=[],
    name_mapping={"protocol": "protocol", "port": "port", "source_port": "sourcePort"},
)
class NsxvFirewallRuleService:
    def __init__(
        self,
        *,
        protocol: builtins.str,
        port: typing.Optional[builtins.str] = None,
        source_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#protocol NsxvFirewallRule#protocol}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#port NsxvFirewallRule#port}.
        :param source_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#source_port NsxvFirewallRule#source_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef55fc8c414085065228fd8a7e90c8e4437d9f3e3e0a7ed6c3f5a7e5a16b04f)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument source_port", value=source_port, expected_type=type_hints["source_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "protocol": protocol,
        }
        if port is not None:
            self._values["port"] = port
        if source_port is not None:
            self._values["source_port"] = source_port

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#protocol NsxvFirewallRule#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#port NsxvFirewallRule#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#source_port NsxvFirewallRule#source_port}.'''
        result = self._values.get("source_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxvFirewallRuleService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxvFirewallRuleServiceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRuleServiceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4269fe5c19b88230ea6f904936346527aa1dd963b0cededcce47d525dcef24c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NsxvFirewallRuleServiceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39202f26ce3491be22db11346b95446f146cfc0a7831a9881dd87829cbcf0021)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxvFirewallRuleServiceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5928ffd118e765b41f4f571ad11ccde75da00d357f99038e509978125d2d70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0fd36155af96039da77fcfcfd64616a99581d12a850742ff82327cfbb510fd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0769ded38ab61e7e428f04bf72b2b2866df37e8ea92fcfc55db1a21e9f5cd51d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxvFirewallRuleService]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxvFirewallRuleService]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxvFirewallRuleService]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca07c98d21feccbc0f6defc1097371a0218f1238b02c9ccdbb00be926326e81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxvFirewallRuleServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRuleServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1acb16d10647b5a89111a79c62c2d3ed3ce5a93679cd664cb0c32865788e806)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSourcePort")
    def reset_source_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcePort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePortInput")
    def source_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcePortInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea02e5aae340d7cba58d16b834d3022315656b7375be1440c17e3239a2c9e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958cfbe00b835ea10e69bb1d26763dd1dce78cd18f565508305484cac35cc1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="sourcePort")
    def source_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcePort"))

    @source_port.setter
    def source_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc5c4cc35bea0f1d7964ed9c66ce1613f5b52063a8a379cf8b336b450117eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePort", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxvFirewallRuleService]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxvFirewallRuleService]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxvFirewallRuleService]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94977b42f885f18ce9031696c80e0a54c6b71f3a0c746f456f5f7370293dbf3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRuleSource",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "gateway_interfaces": "gatewayInterfaces",
        "ip_addresses": "ipAddresses",
        "ip_sets": "ipSets",
        "org_networks": "orgNetworks",
        "vm_ids": "vmIds",
    },
)
class NsxvFirewallRuleSource:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gateway_interfaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
        org_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude: Rule is applied to traffic coming from all sources except for the excluded source. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#exclude NsxvFirewallRule#exclude}
        :param gateway_interfaces: 'vse', 'internal', 'external' or network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#gateway_interfaces NsxvFirewallRule#gateway_interfaces}
        :param ip_addresses: IP address, CIDR, an IP range, or the keyword 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_addresses NsxvFirewallRule#ip_addresses}
        :param ip_sets: Set of IP set names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_sets NsxvFirewallRule#ip_sets}
        :param org_networks: Set of org network names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org_networks NsxvFirewallRule#org_networks}
        :param vm_ids: Set of VM IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vm_ids NsxvFirewallRule#vm_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5cc69691f148206eff8a349d079edf5dcb81089577e3b02e2c2d5a81503e82)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument gateway_interfaces", value=gateway_interfaces, expected_type=type_hints["gateway_interfaces"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument ip_sets", value=ip_sets, expected_type=type_hints["ip_sets"])
            check_type(argname="argument org_networks", value=org_networks, expected_type=type_hints["org_networks"])
            check_type(argname="argument vm_ids", value=vm_ids, expected_type=type_hints["vm_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if gateway_interfaces is not None:
            self._values["gateway_interfaces"] = gateway_interfaces
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if ip_sets is not None:
            self._values["ip_sets"] = ip_sets
        if org_networks is not None:
            self._values["org_networks"] = org_networks
        if vm_ids is not None:
            self._values["vm_ids"] = vm_ids

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Rule is applied to traffic coming from all sources except for the excluded source. Default 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#exclude NsxvFirewallRule#exclude}
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gateway_interfaces(self) -> typing.Optional[typing.List[builtins.str]]:
        ''''vse', 'internal', 'external' or network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#gateway_interfaces NsxvFirewallRule#gateway_interfaces}
        '''
        result = self._values.get("gateway_interfaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP address, CIDR, an IP range, or the keyword 'any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_addresses NsxvFirewallRule#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_sets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of IP set names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#ip_sets NsxvFirewallRule#ip_sets}
        '''
        result = self._values.get("ip_sets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def org_networks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of org network names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#org_networks NsxvFirewallRule#org_networks}
        '''
        result = self._values.get("org_networks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vm_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of VM IDs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_firewall_rule#vm_ids NsxvFirewallRule#vm_ids}
        '''
        result = self._values.get("vm_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxvFirewallRuleSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxvFirewallRuleSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvFirewallRule.NsxvFirewallRuleSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5f024d343fa44484b739da39e182bffd08489e9bb8b4e5573b9d5f8cb679ceb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExclude")
    def reset_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclude", []))

    @jsii.member(jsii_name="resetGatewayInterfaces")
    def reset_gateway_interfaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayInterfaces", []))

    @jsii.member(jsii_name="resetIpAddresses")
    def reset_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddresses", []))

    @jsii.member(jsii_name="resetIpSets")
    def reset_ip_sets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpSets", []))

    @jsii.member(jsii_name="resetOrgNetworks")
    def reset_org_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgNetworks", []))

    @jsii.member(jsii_name="resetVmIds")
    def reset_vm_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmIds", []))

    @builtins.property
    @jsii.member(jsii_name="excludeInput")
    def exclude_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInterfacesInput")
    def gateway_interfaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gatewayInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSetsInput")
    def ip_sets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipSetsInput"))

    @builtins.property
    @jsii.member(jsii_name="orgNetworksInput")
    def org_networks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "orgNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="vmIdsInput")
    def vm_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vmIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="exclude")
    def exclude(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "exclude"))

    @exclude.setter
    def exclude(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cbd909062b9f809f871cd165f0367ec4deec3b51b1e9226ff074c255d25da55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclude", value)

    @builtins.property
    @jsii.member(jsii_name="gatewayInterfaces")
    def gateway_interfaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gatewayInterfaces"))

    @gateway_interfaces.setter
    def gateway_interfaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2171c4cfefce38479c6d773288e436b28dd549fe9c27a4ad06f5ef2f1db9f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayInterfaces", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3d77b82f182dfbc2b08e0c6327272846c89263221545a07e099f67a05387f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="ipSets")
    def ip_sets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipSets"))

    @ip_sets.setter
    def ip_sets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd528178dac2b9dbcb76b055a2ce08c3d9a3cf7527515365c2a3f5504c14f8e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSets", value)

    @builtins.property
    @jsii.member(jsii_name="orgNetworks")
    def org_networks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "orgNetworks"))

    @org_networks.setter
    def org_networks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92942fbb3a22bdd1e9e813fb17462c71838e5323b1dba3cb64d1e354a7771bdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgNetworks", value)

    @builtins.property
    @jsii.member(jsii_name="vmIds")
    def vm_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vmIds"))

    @vm_ids.setter
    def vm_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd1d10ec88e64bb47ec5d65cffa903759cf016378b485e9ca69c657fae1b9a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NsxvFirewallRuleSource]:
        return typing.cast(typing.Optional[NsxvFirewallRuleSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NsxvFirewallRuleSource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3383f7cab59b6e58a816032cbee7b1ec8c11f150bc419adec6dcba70363b91c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxvFirewallRule",
    "NsxvFirewallRuleConfig",
    "NsxvFirewallRuleDestination",
    "NsxvFirewallRuleDestinationOutputReference",
    "NsxvFirewallRuleService",
    "NsxvFirewallRuleServiceList",
    "NsxvFirewallRuleServiceOutputReference",
    "NsxvFirewallRuleSource",
    "NsxvFirewallRuleSourceOutputReference",
]

publication.publish()

def _typecheckingstub__eeece478c7f2e329d74dbc4c68876b93e9a1d009ac203a63e90de1753fcbd56a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination: typing.Union[NsxvFirewallRuleDestination, typing.Dict[builtins.str, typing.Any]],
    edge_gateway: builtins.str,
    service: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxvFirewallRuleService, typing.Dict[builtins.str, typing.Any]]]],
    source: typing.Union[NsxvFirewallRuleSource, typing.Dict[builtins.str, typing.Any]],
    above_rule_id: typing.Optional[builtins.str] = None,
    action: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    rule_tag: typing.Optional[jsii.Number] = None,
    rule_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__904514826a73af81052bc971cece1ccbd82b35d8402d029dd3db0960efc94a40(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b652ff4f32a8b269d07148b8fd437776c3d8fab802d74820772ddd0f327847(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxvFirewallRuleService, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbd185ae2752ec9dfeda7fd0a953a04fbf6188e5839dcd1beb2fe14671f7e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7afc9e692d989bb18054d56787771257509cf4a7de7d77ca79e825c15eda53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90055a6736f0a6bccf23ba446987d85522a2497760481aeb3444d00a400c9291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191f82b9185dd7aa5d2ad75fe26fdc88e548c241f966322dc7a652ed249b7761(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02215c0e0c60435cfed6c7c57162933fafb7d9a458c5996c258d7daf6c0b9443(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775e5d68ecd42af15915b4bdae46d9fc7630a94317220b7ffada465e083743e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c33060d3bf1591732d2e6278ff50340c6c534e8c283ada2817d22bf82541940(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01cb04f25da79ef2592e1dc43755fa5c7a008d4131253c87c88d38ecaee8a16e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c87912789b43235a06b570605495697a09862bcf250dc87118e29fd9c790c99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5815d72a2428f0ed73d00fbead3c32045cbb6256cc7bd5348699fb8b71602d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b60bb1b340bca1bb45d4ed50a268bcbdec500990372bdd62af72ea7dec7901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22067aecfe3c2abbba31557ce8eedd12bad45b4cc86e3c1d49f3e3e0d1bab672(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination: typing.Union[NsxvFirewallRuleDestination, typing.Dict[builtins.str, typing.Any]],
    edge_gateway: builtins.str,
    service: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxvFirewallRuleService, typing.Dict[builtins.str, typing.Any]]]],
    source: typing.Union[NsxvFirewallRuleSource, typing.Dict[builtins.str, typing.Any]],
    above_rule_id: typing.Optional[builtins.str] = None,
    action: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    rule_tag: typing.Optional[jsii.Number] = None,
    rule_type: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bac3c5ce82c13183ea4e8b2dbad5a53d16c41c4d0fffbf10b1bb15a88cfabde(
    *,
    exclude: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gateway_interfaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
    org_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b84ce763cdace292381975f24da00f4f4b0011709a0f11fd6376aa005d64ed9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec94c3d12901ec8eecb627746853918b20ccb01ecd182e6acc72a8ff03c0cf2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143d6672a5d3bb23b00d556565195c048be9018f77c0c1d1e0c7a0d0b71cd01a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb0f0ed0461697613f137fb9f2b32b2c3ed4aa572e9ce6e12bfd0f50d3156d6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72a50ec7286697e104a65ccff1aa3f6a3268397ae1157f5385b1dcff6f14771(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8fa9cb9b230d478ec692b69edcfda5f75706537876ae171dd77124df59aab0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe89cb51cdfcdb82ef058a46a340dfc6e1c5ab7c21a6b2f01714d0c0e6263d5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89bea6cb21973fd6963282d25e3c7758bd4e79d8e29a02d404d7fad831619aa(
    value: typing.Optional[NsxvFirewallRuleDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef55fc8c414085065228fd8a7e90c8e4437d9f3e3e0a7ed6c3f5a7e5a16b04f(
    *,
    protocol: builtins.str,
    port: typing.Optional[builtins.str] = None,
    source_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4269fe5c19b88230ea6f904936346527aa1dd963b0cededcce47d525dcef24c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39202f26ce3491be22db11346b95446f146cfc0a7831a9881dd87829cbcf0021(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5928ffd118e765b41f4f571ad11ccde75da00d357f99038e509978125d2d70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fd36155af96039da77fcfcfd64616a99581d12a850742ff82327cfbb510fd0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0769ded38ab61e7e428f04bf72b2b2866df37e8ea92fcfc55db1a21e9f5cd51d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca07c98d21feccbc0f6defc1097371a0218f1238b02c9ccdbb00be926326e81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxvFirewallRuleService]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1acb16d10647b5a89111a79c62c2d3ed3ce5a93679cd664cb0c32865788e806(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea02e5aae340d7cba58d16b834d3022315656b7375be1440c17e3239a2c9e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958cfbe00b835ea10e69bb1d26763dd1dce78cd18f565508305484cac35cc1e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc5c4cc35bea0f1d7964ed9c66ce1613f5b52063a8a379cf8b336b450117eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94977b42f885f18ce9031696c80e0a54c6b71f3a0c746f456f5f7370293dbf3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxvFirewallRuleService]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5cc69691f148206eff8a349d079edf5dcb81089577e3b02e2c2d5a81503e82(
    *,
    exclude: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gateway_interfaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
    org_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f024d343fa44484b739da39e182bffd08489e9bb8b4e5573b9d5f8cb679ceb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cbd909062b9f809f871cd165f0367ec4deec3b51b1e9226ff074c255d25da55(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2171c4cfefce38479c6d773288e436b28dd549fe9c27a4ad06f5ef2f1db9f4b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3d77b82f182dfbc2b08e0c6327272846c89263221545a07e099f67a05387f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd528178dac2b9dbcb76b055a2ce08c3d9a3cf7527515365c2a3f5504c14f8e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92942fbb3a22bdd1e9e813fb17462c71838e5323b1dba3cb64d1e354a7771bdb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd1d10ec88e64bb47ec5d65cffa903759cf016378b485e9ca69c657fae1b9a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3383f7cab59b6e58a816032cbee7b1ec8c11f150bc419adec6dcba70363b91c0(
    value: typing.Optional[NsxvFirewallRuleSource],
) -> None:
    """Type checking stubs"""
    pass
