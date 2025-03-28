'''
# `vcd_nsxt_distributed_firewall_rule`

Refer to the Terraform Registry for docs: [`vcd_nsxt_distributed_firewall_rule`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule).
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


class NsxtDistributedFirewallRuleA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtDistributedFirewallRule.NsxtDistributedFirewallRuleA",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule vcd_nsxt_distributed_firewall_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        name: builtins.str,
        vdc_group_id: builtins.str,
        above_rule_id: typing.Optional[builtins.str] = None,
        app_port_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        destination_groups_excluded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        direction: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_context_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        org: typing.Optional[builtins.str] = None,
        source_groups_excluded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule vcd_nsxt_distributed_firewall_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: Defines if the rule should 'ALLOW', 'DROP', 'REJECT' matching traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#action NsxtDistributedFirewallRuleA#action}
        :param name: Firewall Rule name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#name NsxtDistributedFirewallRuleA#name}
        :param vdc_group_id: ID of VDC Group for Distributed Firewall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#vdc_group_id NsxtDistributedFirewallRuleA#vdc_group_id}
        :param above_rule_id: An optional firewall rule ID, to put new rule above during creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#above_rule_id NsxtDistributedFirewallRuleA#above_rule_id}
        :param app_port_profile_ids: A set of Application Port Profile IDs. Leaving it empty means 'Any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#app_port_profile_ids NsxtDistributedFirewallRuleA#app_port_profile_ids}
        :param comment: Comment that is shown next to rule in UI (VCD 10.3.2+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#comment NsxtDistributedFirewallRuleA#comment}
        :param description: Description is not shown in UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#description NsxtDistributedFirewallRuleA#description}
        :param destination_groups_excluded: Reverses firewall matching for to match all except Destinations Groups specified in 'destination_ids' (VCD 10.3.2+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#destination_groups_excluded NsxtDistributedFirewallRuleA#destination_groups_excluded}
        :param destination_ids: A set of Destination Firewall Group IDs (IP Sets or Security Groups). Leaving it empty means 'Any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#destination_ids NsxtDistributedFirewallRuleA#destination_ids}
        :param direction: Direction on which Firewall Rule applies (one of 'IN', 'OUT', 'IN_OUT'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#direction NsxtDistributedFirewallRuleA#direction}
        :param enabled: Defined if Firewall Rule is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#enabled NsxtDistributedFirewallRuleA#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#id NsxtDistributedFirewallRuleA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_protocol: Firewall Rule Protocol (one of 'IPV4', 'IPV6', 'IPV4_IPV6'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#ip_protocol NsxtDistributedFirewallRuleA#ip_protocol}
        :param logging: Defines if matching traffic should be logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#logging NsxtDistributedFirewallRuleA#logging}
        :param network_context_profile_ids: A set of Network Context Profile IDs. Leaving it empty means 'Any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#network_context_profile_ids NsxtDistributedFirewallRuleA#network_context_profile_ids}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#org NsxtDistributedFirewallRuleA#org}
        :param source_groups_excluded: Reverses firewall matching for to match all except Source Groups specified in 'source_ids' (VCD 10.3.2+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#source_groups_excluded NsxtDistributedFirewallRuleA#source_groups_excluded}
        :param source_ids: A set of Source Firewall Group IDs (IP Sets or Security Groups). Leaving it empty means 'Any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#source_ids NsxtDistributedFirewallRuleA#source_ids}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b34bd49b7bf03c5d0b96965deda0f36199ca29a70373ece34dd1c3f4ac07f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtDistributedFirewallRuleAConfig(
            action=action,
            name=name,
            vdc_group_id=vdc_group_id,
            above_rule_id=above_rule_id,
            app_port_profile_ids=app_port_profile_ids,
            comment=comment,
            description=description,
            destination_groups_excluded=destination_groups_excluded,
            destination_ids=destination_ids,
            direction=direction,
            enabled=enabled,
            id=id,
            ip_protocol=ip_protocol,
            logging=logging,
            network_context_profile_ids=network_context_profile_ids,
            org=org,
            source_groups_excluded=source_groups_excluded,
            source_ids=source_ids,
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
        '''Generates CDKTF code for importing a NsxtDistributedFirewallRuleA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtDistributedFirewallRuleA to import.
        :param import_from_id: The id of the existing NsxtDistributedFirewallRuleA that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtDistributedFirewallRuleA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163e986bca2f7f2383cc197a7bb9bc4a83abc9114bb597cf94dbbf1b25484aae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAboveRuleId")
    def reset_above_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAboveRuleId", []))

    @jsii.member(jsii_name="resetAppPortProfileIds")
    def reset_app_port_profile_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppPortProfileIds", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDestinationGroupsExcluded")
    def reset_destination_groups_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationGroupsExcluded", []))

    @jsii.member(jsii_name="resetDestinationIds")
    def reset_destination_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationIds", []))

    @jsii.member(jsii_name="resetDirection")
    def reset_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirection", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpProtocol")
    def reset_ip_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpProtocol", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetNetworkContextProfileIds")
    def reset_network_context_profile_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkContextProfileIds", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetSourceGroupsExcluded")
    def reset_source_groups_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceGroupsExcluded", []))

    @jsii.member(jsii_name="resetSourceIds")
    def reset_source_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceIds", []))

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
    @jsii.member(jsii_name="aboveRuleIdInput")
    def above_rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aboveRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="appPortProfileIdsInput")
    def app_port_profile_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "appPortProfileIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationGroupsExcludedInput")
    def destination_groups_excluded_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "destinationGroupsExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationIdsInput")
    def destination_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

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
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

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
    @jsii.member(jsii_name="networkContextProfileIdsInput")
    def network_context_profile_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkContextProfileIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceGroupsExcludedInput")
    def source_groups_excluded_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sourceGroupsExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIdsInput")
    def source_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcGroupIdInput")
    def vdc_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="aboveRuleId")
    def above_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aboveRuleId"))

    @above_rule_id.setter
    def above_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64170430cc184ee55cebe194074deaf65af208abaeafbd1561e41645cda02d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aboveRuleId", value)

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703b0159c553f0dcdf999f8191e10bab4634511c451a0dad21beb17738c7e077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="appPortProfileIds")
    def app_port_profile_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "appPortProfileIds"))

    @app_port_profile_ids.setter
    def app_port_profile_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80c5972df6f7861c7e081294cd36e8ba46ce98c2fade298605b17f9eab3b865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appPortProfileIds", value)

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93fca64325be34f1b954258609934443642a747ec03237bbe1af08c6c91ef1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1b6e96e2f1a340d0e83980f345f392bd291fe496207f511b19413697b5e2ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="destinationGroupsExcluded")
    def destination_groups_excluded(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "destinationGroupsExcluded"))

    @destination_groups_excluded.setter
    def destination_groups_excluded(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c014354be5aa349dfbb63ed241507cb623f553b0db989e87a3e9442d6b7b2ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationGroupsExcluded", value)

    @builtins.property
    @jsii.member(jsii_name="destinationIds")
    def destination_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationIds"))

    @destination_ids.setter
    def destination_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b778de9469e02ae30a237afd6c07a547cac9c0b41f9101ef5d3d8a5e904545cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationIds", value)

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a7678ae86bd20373cd14e19cf1b9a5248cf268416a2bd8ef4900ea989a40fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__f44b5ef360b0eda05b5d54c8599d1a3691b39b467cc12ea04b7ef50622802b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d964707480df7d7411d874fa69337d47c1da9df003b432f510fac18f39d7fef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243cc48df2e80a1d66a478ffed0fd4dc7dee9e1a932adfe00d98c55b5c5a612e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__155b61055e91d2ea19abf9c03b9ebb125a62476aac4940e162e4090eb70a1dff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50a78664800eba997c3b6f7626b11ad3b653ae075391b5fd04df5adc5d921b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkContextProfileIds")
    def network_context_profile_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkContextProfileIds"))

    @network_context_profile_ids.setter
    def network_context_profile_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f04aa61df4fe554458a1c4ee6d39f55f3a27d822b0495ca9cdbe57164df0ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkContextProfileIds", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9866aa738c6103ad7a8ef141a0b4dc600f5b094ad7958a773df98b60451e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="sourceGroupsExcluded")
    def source_groups_excluded(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sourceGroupsExcluded"))

    @source_groups_excluded.setter
    def source_groups_excluded(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935ec2bef10cb9ff966acdbed4a638aa37a44f84ea64ac2a6189c9f30ea18e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceGroupsExcluded", value)

    @builtins.property
    @jsii.member(jsii_name="sourceIds")
    def source_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIds"))

    @source_ids.setter
    def source_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a75a4127e818863680edb40889a558b6581108abdad1308a851cf259b1ce1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIds", value)

    @builtins.property
    @jsii.member(jsii_name="vdcGroupId")
    def vdc_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcGroupId"))

    @vdc_group_id.setter
    def vdc_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480ab5255b23198c8f6ea012481bcc14f92a02015a47e91c217c144afe177772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdcGroupId", value)


@jsii.data_type(
    jsii_type="vcd.nsxtDistributedFirewallRule.NsxtDistributedFirewallRuleAConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "name": "name",
        "vdc_group_id": "vdcGroupId",
        "above_rule_id": "aboveRuleId",
        "app_port_profile_ids": "appPortProfileIds",
        "comment": "comment",
        "description": "description",
        "destination_groups_excluded": "destinationGroupsExcluded",
        "destination_ids": "destinationIds",
        "direction": "direction",
        "enabled": "enabled",
        "id": "id",
        "ip_protocol": "ipProtocol",
        "logging": "logging",
        "network_context_profile_ids": "networkContextProfileIds",
        "org": "org",
        "source_groups_excluded": "sourceGroupsExcluded",
        "source_ids": "sourceIds",
    },
)
class NsxtDistributedFirewallRuleAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: builtins.str,
        name: builtins.str,
        vdc_group_id: builtins.str,
        above_rule_id: typing.Optional[builtins.str] = None,
        app_port_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        destination_groups_excluded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        direction: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_context_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        org: typing.Optional[builtins.str] = None,
        source_groups_excluded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: Defines if the rule should 'ALLOW', 'DROP', 'REJECT' matching traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#action NsxtDistributedFirewallRuleA#action}
        :param name: Firewall Rule name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#name NsxtDistributedFirewallRuleA#name}
        :param vdc_group_id: ID of VDC Group for Distributed Firewall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#vdc_group_id NsxtDistributedFirewallRuleA#vdc_group_id}
        :param above_rule_id: An optional firewall rule ID, to put new rule above during creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#above_rule_id NsxtDistributedFirewallRuleA#above_rule_id}
        :param app_port_profile_ids: A set of Application Port Profile IDs. Leaving it empty means 'Any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#app_port_profile_ids NsxtDistributedFirewallRuleA#app_port_profile_ids}
        :param comment: Comment that is shown next to rule in UI (VCD 10.3.2+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#comment NsxtDistributedFirewallRuleA#comment}
        :param description: Description is not shown in UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#description NsxtDistributedFirewallRuleA#description}
        :param destination_groups_excluded: Reverses firewall matching for to match all except Destinations Groups specified in 'destination_ids' (VCD 10.3.2+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#destination_groups_excluded NsxtDistributedFirewallRuleA#destination_groups_excluded}
        :param destination_ids: A set of Destination Firewall Group IDs (IP Sets or Security Groups). Leaving it empty means 'Any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#destination_ids NsxtDistributedFirewallRuleA#destination_ids}
        :param direction: Direction on which Firewall Rule applies (one of 'IN', 'OUT', 'IN_OUT'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#direction NsxtDistributedFirewallRuleA#direction}
        :param enabled: Defined if Firewall Rule is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#enabled NsxtDistributedFirewallRuleA#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#id NsxtDistributedFirewallRuleA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_protocol: Firewall Rule Protocol (one of 'IPV4', 'IPV6', 'IPV4_IPV6'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#ip_protocol NsxtDistributedFirewallRuleA#ip_protocol}
        :param logging: Defines if matching traffic should be logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#logging NsxtDistributedFirewallRuleA#logging}
        :param network_context_profile_ids: A set of Network Context Profile IDs. Leaving it empty means 'Any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#network_context_profile_ids NsxtDistributedFirewallRuleA#network_context_profile_ids}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#org NsxtDistributedFirewallRuleA#org}
        :param source_groups_excluded: Reverses firewall matching for to match all except Source Groups specified in 'source_ids' (VCD 10.3.2+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#source_groups_excluded NsxtDistributedFirewallRuleA#source_groups_excluded}
        :param source_ids: A set of Source Firewall Group IDs (IP Sets or Security Groups). Leaving it empty means 'Any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#source_ids NsxtDistributedFirewallRuleA#source_ids}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a87917547c6f08e7624f6f7d8538578faeff380a228d6b3b0aa342b65300cf8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vdc_group_id", value=vdc_group_id, expected_type=type_hints["vdc_group_id"])
            check_type(argname="argument above_rule_id", value=above_rule_id, expected_type=type_hints["above_rule_id"])
            check_type(argname="argument app_port_profile_ids", value=app_port_profile_ids, expected_type=type_hints["app_port_profile_ids"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_groups_excluded", value=destination_groups_excluded, expected_type=type_hints["destination_groups_excluded"])
            check_type(argname="argument destination_ids", value=destination_ids, expected_type=type_hints["destination_ids"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument network_context_profile_ids", value=network_context_profile_ids, expected_type=type_hints["network_context_profile_ids"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument source_groups_excluded", value=source_groups_excluded, expected_type=type_hints["source_groups_excluded"])
            check_type(argname="argument source_ids", value=source_ids, expected_type=type_hints["source_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
            "vdc_group_id": vdc_group_id,
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
        if app_port_profile_ids is not None:
            self._values["app_port_profile_ids"] = app_port_profile_ids
        if comment is not None:
            self._values["comment"] = comment
        if description is not None:
            self._values["description"] = description
        if destination_groups_excluded is not None:
            self._values["destination_groups_excluded"] = destination_groups_excluded
        if destination_ids is not None:
            self._values["destination_ids"] = destination_ids
        if direction is not None:
            self._values["direction"] = direction
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if ip_protocol is not None:
            self._values["ip_protocol"] = ip_protocol
        if logging is not None:
            self._values["logging"] = logging
        if network_context_profile_ids is not None:
            self._values["network_context_profile_ids"] = network_context_profile_ids
        if org is not None:
            self._values["org"] = org
        if source_groups_excluded is not None:
            self._values["source_groups_excluded"] = source_groups_excluded
        if source_ids is not None:
            self._values["source_ids"] = source_ids

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
    def action(self) -> builtins.str:
        '''Defines if the rule should 'ALLOW', 'DROP', 'REJECT' matching traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#action NsxtDistributedFirewallRuleA#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Firewall Rule name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#name NsxtDistributedFirewallRuleA#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vdc_group_id(self) -> builtins.str:
        '''ID of VDC Group for Distributed Firewall.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#vdc_group_id NsxtDistributedFirewallRuleA#vdc_group_id}
        '''
        result = self._values.get("vdc_group_id")
        assert result is not None, "Required property 'vdc_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def above_rule_id(self) -> typing.Optional[builtins.str]:
        '''An optional firewall rule ID, to put new rule above during creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#above_rule_id NsxtDistributedFirewallRuleA#above_rule_id}
        '''
        result = self._values.get("above_rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_port_profile_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of Application Port Profile IDs. Leaving it empty means 'Any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#app_port_profile_ids NsxtDistributedFirewallRuleA#app_port_profile_ids}
        '''
        result = self._values.get("app_port_profile_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Comment that is shown next to rule in UI (VCD 10.3.2+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#comment NsxtDistributedFirewallRuleA#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description is not shown in UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#description NsxtDistributedFirewallRuleA#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_groups_excluded(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Reverses firewall matching for to match all except Destinations Groups specified in 'destination_ids' (VCD 10.3.2+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#destination_groups_excluded NsxtDistributedFirewallRuleA#destination_groups_excluded}
        '''
        result = self._values.get("destination_groups_excluded")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def destination_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of Destination Firewall Group IDs (IP Sets or Security Groups). Leaving it empty means 'Any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#destination_ids NsxtDistributedFirewallRuleA#destination_ids}
        '''
        result = self._values.get("destination_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''Direction on which Firewall Rule applies (one of 'IN', 'OUT', 'IN_OUT').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#direction NsxtDistributedFirewallRuleA#direction}
        '''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defined if Firewall Rule is active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#enabled NsxtDistributedFirewallRuleA#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#id NsxtDistributedFirewallRuleA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_protocol(self) -> typing.Optional[builtins.str]:
        '''Firewall Rule Protocol (one of 'IPV4', 'IPV6', 'IPV4_IPV6').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#ip_protocol NsxtDistributedFirewallRuleA#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines if matching traffic should be logged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#logging NsxtDistributedFirewallRuleA#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_context_profile_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of Network Context Profile IDs. Leaving it empty means 'Any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#network_context_profile_ids NsxtDistributedFirewallRuleA#network_context_profile_ids}
        '''
        result = self._values.get("network_context_profile_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#org NsxtDistributedFirewallRuleA#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_groups_excluded(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Reverses firewall matching for to match all except Source Groups specified in 'source_ids' (VCD 10.3.2+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#source_groups_excluded NsxtDistributedFirewallRuleA#source_groups_excluded}
        '''
        result = self._values.get("source_groups_excluded")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of Source Firewall Group IDs (IP Sets or Security Groups). Leaving it empty means 'Any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_distributed_firewall_rule#source_ids NsxtDistributedFirewallRuleA#source_ids}
        '''
        result = self._values.get("source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtDistributedFirewallRuleAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NsxtDistributedFirewallRuleA",
    "NsxtDistributedFirewallRuleAConfig",
]

publication.publish()

def _typecheckingstub__c9b34bd49b7bf03c5d0b96965deda0f36199ca29a70373ece34dd1c3f4ac07f6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    name: builtins.str,
    vdc_group_id: builtins.str,
    above_rule_id: typing.Optional[builtins.str] = None,
    app_port_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    destination_groups_excluded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    direction: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_context_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    org: typing.Optional[builtins.str] = None,
    source_groups_excluded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__163e986bca2f7f2383cc197a7bb9bc4a83abc9114bb597cf94dbbf1b25484aae(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64170430cc184ee55cebe194074deaf65af208abaeafbd1561e41645cda02d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703b0159c553f0dcdf999f8191e10bab4634511c451a0dad21beb17738c7e077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80c5972df6f7861c7e081294cd36e8ba46ce98c2fade298605b17f9eab3b865(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93fca64325be34f1b954258609934443642a747ec03237bbe1af08c6c91ef1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1b6e96e2f1a340d0e83980f345f392bd291fe496207f511b19413697b5e2ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c014354be5aa349dfbb63ed241507cb623f553b0db989e87a3e9442d6b7b2ec2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b778de9469e02ae30a237afd6c07a547cac9c0b41f9101ef5d3d8a5e904545cb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a7678ae86bd20373cd14e19cf1b9a5248cf268416a2bd8ef4900ea989a40fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44b5ef360b0eda05b5d54c8599d1a3691b39b467cc12ea04b7ef50622802b11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d964707480df7d7411d874fa69337d47c1da9df003b432f510fac18f39d7fef2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243cc48df2e80a1d66a478ffed0fd4dc7dee9e1a932adfe00d98c55b5c5a612e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155b61055e91d2ea19abf9c03b9ebb125a62476aac4940e162e4090eb70a1dff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50a78664800eba997c3b6f7626b11ad3b653ae075391b5fd04df5adc5d921b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f04aa61df4fe554458a1c4ee6d39f55f3a27d822b0495ca9cdbe57164df0ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9866aa738c6103ad7a8ef141a0b4dc600f5b094ad7958a773df98b60451e85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935ec2bef10cb9ff966acdbed4a638aa37a44f84ea64ac2a6189c9f30ea18e74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a75a4127e818863680edb40889a558b6581108abdad1308a851cf259b1ce1d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480ab5255b23198c8f6ea012481bcc14f92a02015a47e91c217c144afe177772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a87917547c6f08e7624f6f7d8538578faeff380a228d6b3b0aa342b65300cf8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    name: builtins.str,
    vdc_group_id: builtins.str,
    above_rule_id: typing.Optional[builtins.str] = None,
    app_port_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    destination_groups_excluded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    direction: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_context_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    org: typing.Optional[builtins.str] = None,
    source_groups_excluded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
