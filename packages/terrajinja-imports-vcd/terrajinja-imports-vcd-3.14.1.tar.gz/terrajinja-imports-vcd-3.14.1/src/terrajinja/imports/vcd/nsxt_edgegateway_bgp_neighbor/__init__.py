'''
# `vcd_nsxt_edgegateway_bgp_neighbor`

Refer to the Terraform Registry for docs: [`vcd_nsxt_edgegateway_bgp_neighbor`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor).
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


class NsxtEdgegatewayBgpNeighbor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayBgpNeighbor.NsxtEdgegatewayBgpNeighbor",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor vcd_nsxt_edgegateway_bgp_neighbor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway_id: builtins.str,
        ip_address: builtins.str,
        remote_as_number: builtins.str,
        allow_as_in: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bfd_dead_multiple: typing.Optional[jsii.Number] = None,
        bfd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bfd_interval: typing.Optional[jsii.Number] = None,
        graceful_restart_mode: typing.Optional[builtins.str] = None,
        hold_down_timer: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        in_filter_ip_prefix_list_id: typing.Optional[builtins.str] = None,
        keep_alive_timer: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        out_filter_ip_prefix_list_id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        route_filtering: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor vcd_nsxt_edgegateway_bgp_neighbor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway_id: Edge gateway ID for BGP Neighbor Configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#edge_gateway_id NsxtEdgegatewayBgpNeighbor#edge_gateway_id}
        :param ip_address: BGP Neighbor IP address (IPv4 or IPv6). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#ip_address NsxtEdgegatewayBgpNeighbor#ip_address}
        :param remote_as_number: Remote Autonomous System (AS) number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#remote_as_number NsxtEdgegatewayBgpNeighbor#remote_as_number}
        :param allow_as_in: A flag indicating whether BGP neighbors can receive routes with same Autonomous System (AS) (default 'false'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#allow_as_in NsxtEdgegatewayBgpNeighbor#allow_as_in}
        :param bfd_dead_multiple: Number of times a heartbeat packet is missed before BFD declares that the neighbor is down. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_dead_multiple NsxtEdgegatewayBgpNeighbor#bfd_dead_multiple}
        :param bfd_enabled: BFD configuration for failure detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_enabled NsxtEdgegatewayBgpNeighbor#bfd_enabled}
        :param bfd_interval: Time interval (in milliseconds) between heartbeat packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_interval NsxtEdgegatewayBgpNeighbor#bfd_interval}
        :param graceful_restart_mode: One of 'DISABLE', 'HELPER_ONLY', 'GRACEFUL_AND_HELPER'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#graceful_restart_mode NsxtEdgegatewayBgpNeighbor#graceful_restart_mode}
        :param hold_down_timer: Time interval (in seconds) before declaring a peer dead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#hold_down_timer NsxtEdgegatewayBgpNeighbor#hold_down_timer}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#id NsxtEdgegatewayBgpNeighbor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_filter_ip_prefix_list_id: An optional IP Prefix List ID for filtering 'IN' direction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#in_filter_ip_prefix_list_id NsxtEdgegatewayBgpNeighbor#in_filter_ip_prefix_list_id}
        :param keep_alive_timer: Time interval (in seconds) between sending keep alive messages to a peer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#keep_alive_timer NsxtEdgegatewayBgpNeighbor#keep_alive_timer}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#org NsxtEdgegatewayBgpNeighbor#org}
        :param out_filter_ip_prefix_list_id: An optional IP Prefix List ID for filtering 'OUT' direction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#out_filter_ip_prefix_list_id NsxtEdgegatewayBgpNeighbor#out_filter_ip_prefix_list_id}
        :param password: Neighbor password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#password NsxtEdgegatewayBgpNeighbor#password}
        :param route_filtering: One of 'DISABLED', 'IPV4', 'IPV6'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#route_filtering NsxtEdgegatewayBgpNeighbor#route_filtering}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab346ee09fadf7627c75fa531c03d05bdb09bd661b8512e224d761ce50c6b6a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtEdgegatewayBgpNeighborConfig(
            edge_gateway_id=edge_gateway_id,
            ip_address=ip_address,
            remote_as_number=remote_as_number,
            allow_as_in=allow_as_in,
            bfd_dead_multiple=bfd_dead_multiple,
            bfd_enabled=bfd_enabled,
            bfd_interval=bfd_interval,
            graceful_restart_mode=graceful_restart_mode,
            hold_down_timer=hold_down_timer,
            id=id,
            in_filter_ip_prefix_list_id=in_filter_ip_prefix_list_id,
            keep_alive_timer=keep_alive_timer,
            org=org,
            out_filter_ip_prefix_list_id=out_filter_ip_prefix_list_id,
            password=password,
            route_filtering=route_filtering,
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
        '''Generates CDKTF code for importing a NsxtEdgegatewayBgpNeighbor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtEdgegatewayBgpNeighbor to import.
        :param import_from_id: The id of the existing NsxtEdgegatewayBgpNeighbor that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtEdgegatewayBgpNeighbor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca87fc8f99e8a3a2a8bf4218e96d74fb9c735321427e8ee65740e1a3375e14f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllowAsIn")
    def reset_allow_as_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAsIn", []))

    @jsii.member(jsii_name="resetBfdDeadMultiple")
    def reset_bfd_dead_multiple(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBfdDeadMultiple", []))

    @jsii.member(jsii_name="resetBfdEnabled")
    def reset_bfd_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBfdEnabled", []))

    @jsii.member(jsii_name="resetBfdInterval")
    def reset_bfd_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBfdInterval", []))

    @jsii.member(jsii_name="resetGracefulRestartMode")
    def reset_graceful_restart_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGracefulRestartMode", []))

    @jsii.member(jsii_name="resetHoldDownTimer")
    def reset_hold_down_timer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoldDownTimer", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInFilterIpPrefixListId")
    def reset_in_filter_ip_prefix_list_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInFilterIpPrefixListId", []))

    @jsii.member(jsii_name="resetKeepAliveTimer")
    def reset_keep_alive_timer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveTimer", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOutFilterIpPrefixListId")
    def reset_out_filter_ip_prefix_list_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutFilterIpPrefixListId", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetRouteFiltering")
    def reset_route_filtering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteFiltering", []))

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
    @jsii.member(jsii_name="allowAsInInput")
    def allow_as_in_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAsInInput"))

    @builtins.property
    @jsii.member(jsii_name="bfdDeadMultipleInput")
    def bfd_dead_multiple_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bfdDeadMultipleInput"))

    @builtins.property
    @jsii.member(jsii_name="bfdEnabledInput")
    def bfd_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bfdEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="bfdIntervalInput")
    def bfd_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bfdIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayIdInput")
    def edge_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gracefulRestartModeInput")
    def graceful_restart_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gracefulRestartModeInput"))

    @builtins.property
    @jsii.member(jsii_name="holdDownTimerInput")
    def hold_down_timer_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "holdDownTimerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inFilterIpPrefixListIdInput")
    def in_filter_ip_prefix_list_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inFilterIpPrefixListIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimerInput")
    def keep_alive_timer_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepAliveTimerInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="outFilterIpPrefixListIdInput")
    def out_filter_ip_prefix_list_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outFilterIpPrefixListIdInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteAsNumberInput")
    def remote_as_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteAsNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="routeFilteringInput")
    def route_filtering_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeFilteringInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAsIn")
    def allow_as_in(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAsIn"))

    @allow_as_in.setter
    def allow_as_in(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f46486121f7fba7258c8f3fa076cbf844945acf869cd94b3006296af12452f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAsIn", value)

    @builtins.property
    @jsii.member(jsii_name="bfdDeadMultiple")
    def bfd_dead_multiple(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bfdDeadMultiple"))

    @bfd_dead_multiple.setter
    def bfd_dead_multiple(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2026d6cc49c10abbe5732ed115f421e309a2cce3e0ad93ca235da9ce3dfc066c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bfdDeadMultiple", value)

    @builtins.property
    @jsii.member(jsii_name="bfdEnabled")
    def bfd_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bfdEnabled"))

    @bfd_enabled.setter
    def bfd_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be9807e37936e053307dcf88a2e3dbfe0938f70087780e7597030c248948f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bfdEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="bfdInterval")
    def bfd_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bfdInterval"))

    @bfd_interval.setter
    def bfd_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe3a9eccf0b107820c4b5b2f2a76971b9227e5a119a4bdd3f97cac06b01003d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bfdInterval", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayId")
    def edge_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGatewayId"))

    @edge_gateway_id.setter
    def edge_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db8816b094d49fb9bab27d6abeba986b2780d57a34ef459ff7201c30b01a88c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGatewayId", value)

    @builtins.property
    @jsii.member(jsii_name="gracefulRestartMode")
    def graceful_restart_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gracefulRestartMode"))

    @graceful_restart_mode.setter
    def graceful_restart_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfff01aa5d327ec76c0d7a8d82eedf53552de4b267f960218c5e79ee10e5d612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gracefulRestartMode", value)

    @builtins.property
    @jsii.member(jsii_name="holdDownTimer")
    def hold_down_timer(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "holdDownTimer"))

    @hold_down_timer.setter
    def hold_down_timer(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3ccae92fbf4db3864ddefa327936182af0a4a7b745cdd119b2f4d9660d9461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "holdDownTimer", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6613a50bef042886a82b0dce26be5763768ecedff596ff9a22c92c0cc37c48c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="inFilterIpPrefixListId")
    def in_filter_ip_prefix_list_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inFilterIpPrefixListId"))

    @in_filter_ip_prefix_list_id.setter
    def in_filter_ip_prefix_list_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4c26a4e2a56e39b7c9784e088647a20486e1767916d43a9fcae16d70ffd3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inFilterIpPrefixListId", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a086ed9085bb631c9586e5b6834235ac2189f46403605d34c55d2423c494b36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimer")
    def keep_alive_timer(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepAliveTimer"))

    @keep_alive_timer.setter
    def keep_alive_timer(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a4e87ed8816a1dd74bf1de8a72d03799cac24c462e58f53c239b9cb47eff06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveTimer", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725c30c0b8c32c2358699ca94aa3effc0c552e20c0dbd80fda2a620fff5c4435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="outFilterIpPrefixListId")
    def out_filter_ip_prefix_list_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outFilterIpPrefixListId"))

    @out_filter_ip_prefix_list_id.setter
    def out_filter_ip_prefix_list_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ec0e9dd1972f4e7077bc29f07312f4b6c49e53b82bf7b93a32b03e4059d2b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outFilterIpPrefixListId", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05832abd5705117326f894c56fd05ddc1bdfd31107b1378de47281fab80d620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="remoteAsNumber")
    def remote_as_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteAsNumber"))

    @remote_as_number.setter
    def remote_as_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6baed4d17e51a2c5732d83c1921260602e5c31f89d2932933be030b162ed2bce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteAsNumber", value)

    @builtins.property
    @jsii.member(jsii_name="routeFiltering")
    def route_filtering(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeFiltering"))

    @route_filtering.setter
    def route_filtering(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731fca3cccaa6984f70443a46c851de808863173eaa071233e98601991182dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeFiltering", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegatewayBgpNeighbor.NsxtEdgegatewayBgpNeighborConfig",
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
        "ip_address": "ipAddress",
        "remote_as_number": "remoteAsNumber",
        "allow_as_in": "allowAsIn",
        "bfd_dead_multiple": "bfdDeadMultiple",
        "bfd_enabled": "bfdEnabled",
        "bfd_interval": "bfdInterval",
        "graceful_restart_mode": "gracefulRestartMode",
        "hold_down_timer": "holdDownTimer",
        "id": "id",
        "in_filter_ip_prefix_list_id": "inFilterIpPrefixListId",
        "keep_alive_timer": "keepAliveTimer",
        "org": "org",
        "out_filter_ip_prefix_list_id": "outFilterIpPrefixListId",
        "password": "password",
        "route_filtering": "routeFiltering",
    },
)
class NsxtEdgegatewayBgpNeighborConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ip_address: builtins.str,
        remote_as_number: builtins.str,
        allow_as_in: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bfd_dead_multiple: typing.Optional[jsii.Number] = None,
        bfd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bfd_interval: typing.Optional[jsii.Number] = None,
        graceful_restart_mode: typing.Optional[builtins.str] = None,
        hold_down_timer: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        in_filter_ip_prefix_list_id: typing.Optional[builtins.str] = None,
        keep_alive_timer: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        out_filter_ip_prefix_list_id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        route_filtering: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param edge_gateway_id: Edge gateway ID for BGP Neighbor Configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#edge_gateway_id NsxtEdgegatewayBgpNeighbor#edge_gateway_id}
        :param ip_address: BGP Neighbor IP address (IPv4 or IPv6). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#ip_address NsxtEdgegatewayBgpNeighbor#ip_address}
        :param remote_as_number: Remote Autonomous System (AS) number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#remote_as_number NsxtEdgegatewayBgpNeighbor#remote_as_number}
        :param allow_as_in: A flag indicating whether BGP neighbors can receive routes with same Autonomous System (AS) (default 'false'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#allow_as_in NsxtEdgegatewayBgpNeighbor#allow_as_in}
        :param bfd_dead_multiple: Number of times a heartbeat packet is missed before BFD declares that the neighbor is down. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_dead_multiple NsxtEdgegatewayBgpNeighbor#bfd_dead_multiple}
        :param bfd_enabled: BFD configuration for failure detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_enabled NsxtEdgegatewayBgpNeighbor#bfd_enabled}
        :param bfd_interval: Time interval (in milliseconds) between heartbeat packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_interval NsxtEdgegatewayBgpNeighbor#bfd_interval}
        :param graceful_restart_mode: One of 'DISABLE', 'HELPER_ONLY', 'GRACEFUL_AND_HELPER'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#graceful_restart_mode NsxtEdgegatewayBgpNeighbor#graceful_restart_mode}
        :param hold_down_timer: Time interval (in seconds) before declaring a peer dead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#hold_down_timer NsxtEdgegatewayBgpNeighbor#hold_down_timer}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#id NsxtEdgegatewayBgpNeighbor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_filter_ip_prefix_list_id: An optional IP Prefix List ID for filtering 'IN' direction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#in_filter_ip_prefix_list_id NsxtEdgegatewayBgpNeighbor#in_filter_ip_prefix_list_id}
        :param keep_alive_timer: Time interval (in seconds) between sending keep alive messages to a peer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#keep_alive_timer NsxtEdgegatewayBgpNeighbor#keep_alive_timer}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#org NsxtEdgegatewayBgpNeighbor#org}
        :param out_filter_ip_prefix_list_id: An optional IP Prefix List ID for filtering 'OUT' direction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#out_filter_ip_prefix_list_id NsxtEdgegatewayBgpNeighbor#out_filter_ip_prefix_list_id}
        :param password: Neighbor password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#password NsxtEdgegatewayBgpNeighbor#password}
        :param route_filtering: One of 'DISABLED', 'IPV4', 'IPV6'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#route_filtering NsxtEdgegatewayBgpNeighbor#route_filtering}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06665145c5db8b93f761cec68150c11c97d51c561920f9400222968edb9becb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway_id", value=edge_gateway_id, expected_type=type_hints["edge_gateway_id"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument remote_as_number", value=remote_as_number, expected_type=type_hints["remote_as_number"])
            check_type(argname="argument allow_as_in", value=allow_as_in, expected_type=type_hints["allow_as_in"])
            check_type(argname="argument bfd_dead_multiple", value=bfd_dead_multiple, expected_type=type_hints["bfd_dead_multiple"])
            check_type(argname="argument bfd_enabled", value=bfd_enabled, expected_type=type_hints["bfd_enabled"])
            check_type(argname="argument bfd_interval", value=bfd_interval, expected_type=type_hints["bfd_interval"])
            check_type(argname="argument graceful_restart_mode", value=graceful_restart_mode, expected_type=type_hints["graceful_restart_mode"])
            check_type(argname="argument hold_down_timer", value=hold_down_timer, expected_type=type_hints["hold_down_timer"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument in_filter_ip_prefix_list_id", value=in_filter_ip_prefix_list_id, expected_type=type_hints["in_filter_ip_prefix_list_id"])
            check_type(argname="argument keep_alive_timer", value=keep_alive_timer, expected_type=type_hints["keep_alive_timer"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument out_filter_ip_prefix_list_id", value=out_filter_ip_prefix_list_id, expected_type=type_hints["out_filter_ip_prefix_list_id"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument route_filtering", value=route_filtering, expected_type=type_hints["route_filtering"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway_id": edge_gateway_id,
            "ip_address": ip_address,
            "remote_as_number": remote_as_number,
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
        if allow_as_in is not None:
            self._values["allow_as_in"] = allow_as_in
        if bfd_dead_multiple is not None:
            self._values["bfd_dead_multiple"] = bfd_dead_multiple
        if bfd_enabled is not None:
            self._values["bfd_enabled"] = bfd_enabled
        if bfd_interval is not None:
            self._values["bfd_interval"] = bfd_interval
        if graceful_restart_mode is not None:
            self._values["graceful_restart_mode"] = graceful_restart_mode
        if hold_down_timer is not None:
            self._values["hold_down_timer"] = hold_down_timer
        if id is not None:
            self._values["id"] = id
        if in_filter_ip_prefix_list_id is not None:
            self._values["in_filter_ip_prefix_list_id"] = in_filter_ip_prefix_list_id
        if keep_alive_timer is not None:
            self._values["keep_alive_timer"] = keep_alive_timer
        if org is not None:
            self._values["org"] = org
        if out_filter_ip_prefix_list_id is not None:
            self._values["out_filter_ip_prefix_list_id"] = out_filter_ip_prefix_list_id
        if password is not None:
            self._values["password"] = password
        if route_filtering is not None:
            self._values["route_filtering"] = route_filtering

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
        '''Edge gateway ID for BGP Neighbor Configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#edge_gateway_id NsxtEdgegatewayBgpNeighbor#edge_gateway_id}
        '''
        result = self._values.get("edge_gateway_id")
        assert result is not None, "Required property 'edge_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''BGP Neighbor IP address (IPv4 or IPv6).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#ip_address NsxtEdgegatewayBgpNeighbor#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_as_number(self) -> builtins.str:
        '''Remote Autonomous System (AS) number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#remote_as_number NsxtEdgegatewayBgpNeighbor#remote_as_number}
        '''
        result = self._values.get("remote_as_number")
        assert result is not None, "Required property 'remote_as_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_as_in(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag indicating whether BGP neighbors can receive routes with same Autonomous System (AS) (default 'false').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#allow_as_in NsxtEdgegatewayBgpNeighbor#allow_as_in}
        '''
        result = self._values.get("allow_as_in")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bfd_dead_multiple(self) -> typing.Optional[jsii.Number]:
        '''Number of times a heartbeat packet is missed before BFD declares that the neighbor is down.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_dead_multiple NsxtEdgegatewayBgpNeighbor#bfd_dead_multiple}
        '''
        result = self._values.get("bfd_dead_multiple")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bfd_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''BFD configuration for failure detection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_enabled NsxtEdgegatewayBgpNeighbor#bfd_enabled}
        '''
        result = self._values.get("bfd_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bfd_interval(self) -> typing.Optional[jsii.Number]:
        '''Time interval (in milliseconds) between heartbeat packets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#bfd_interval NsxtEdgegatewayBgpNeighbor#bfd_interval}
        '''
        result = self._values.get("bfd_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def graceful_restart_mode(self) -> typing.Optional[builtins.str]:
        '''One of 'DISABLE', 'HELPER_ONLY', 'GRACEFUL_AND_HELPER'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#graceful_restart_mode NsxtEdgegatewayBgpNeighbor#graceful_restart_mode}
        '''
        result = self._values.get("graceful_restart_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hold_down_timer(self) -> typing.Optional[jsii.Number]:
        '''Time interval (in seconds) before declaring a peer dead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#hold_down_timer NsxtEdgegatewayBgpNeighbor#hold_down_timer}
        '''
        result = self._values.get("hold_down_timer")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#id NsxtEdgegatewayBgpNeighbor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_filter_ip_prefix_list_id(self) -> typing.Optional[builtins.str]:
        '''An optional IP Prefix List ID for filtering 'IN' direction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#in_filter_ip_prefix_list_id NsxtEdgegatewayBgpNeighbor#in_filter_ip_prefix_list_id}
        '''
        result = self._values.get("in_filter_ip_prefix_list_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_alive_timer(self) -> typing.Optional[jsii.Number]:
        '''Time interval (in seconds) between sending keep alive messages to a peer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#keep_alive_timer NsxtEdgegatewayBgpNeighbor#keep_alive_timer}
        '''
        result = self._values.get("keep_alive_timer")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#org NsxtEdgegatewayBgpNeighbor#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def out_filter_ip_prefix_list_id(self) -> typing.Optional[builtins.str]:
        '''An optional IP Prefix List ID for filtering 'OUT' direction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#out_filter_ip_prefix_list_id NsxtEdgegatewayBgpNeighbor#out_filter_ip_prefix_list_id}
        '''
        result = self._values.get("out_filter_ip_prefix_list_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Neighbor password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#password NsxtEdgegatewayBgpNeighbor#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_filtering(self) -> typing.Optional[builtins.str]:
        '''One of 'DISABLED', 'IPV4', 'IPV6'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_neighbor#route_filtering NsxtEdgegatewayBgpNeighbor#route_filtering}
        '''
        result = self._values.get("route_filtering")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayBgpNeighborConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NsxtEdgegatewayBgpNeighbor",
    "NsxtEdgegatewayBgpNeighborConfig",
]

publication.publish()

def _typecheckingstub__ab346ee09fadf7627c75fa531c03d05bdb09bd661b8512e224d761ce50c6b6a5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway_id: builtins.str,
    ip_address: builtins.str,
    remote_as_number: builtins.str,
    allow_as_in: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bfd_dead_multiple: typing.Optional[jsii.Number] = None,
    bfd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bfd_interval: typing.Optional[jsii.Number] = None,
    graceful_restart_mode: typing.Optional[builtins.str] = None,
    hold_down_timer: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    in_filter_ip_prefix_list_id: typing.Optional[builtins.str] = None,
    keep_alive_timer: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    out_filter_ip_prefix_list_id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    route_filtering: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ca87fc8f99e8a3a2a8bf4218e96d74fb9c735321427e8ee65740e1a3375e14f1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f46486121f7fba7258c8f3fa076cbf844945acf869cd94b3006296af12452f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2026d6cc49c10abbe5732ed115f421e309a2cce3e0ad93ca235da9ce3dfc066c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be9807e37936e053307dcf88a2e3dbfe0938f70087780e7597030c248948f51(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe3a9eccf0b107820c4b5b2f2a76971b9227e5a119a4bdd3f97cac06b01003d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db8816b094d49fb9bab27d6abeba986b2780d57a34ef459ff7201c30b01a88c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfff01aa5d327ec76c0d7a8d82eedf53552de4b267f960218c5e79ee10e5d612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3ccae92fbf4db3864ddefa327936182af0a4a7b745cdd119b2f4d9660d9461(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6613a50bef042886a82b0dce26be5763768ecedff596ff9a22c92c0cc37c48c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4c26a4e2a56e39b7c9784e088647a20486e1767916d43a9fcae16d70ffd3d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a086ed9085bb631c9586e5b6834235ac2189f46403605d34c55d2423c494b36c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a4e87ed8816a1dd74bf1de8a72d03799cac24c462e58f53c239b9cb47eff06(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725c30c0b8c32c2358699ca94aa3effc0c552e20c0dbd80fda2a620fff5c4435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ec0e9dd1972f4e7077bc29f07312f4b6c49e53b82bf7b93a32b03e4059d2b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05832abd5705117326f894c56fd05ddc1bdfd31107b1378de47281fab80d620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6baed4d17e51a2c5732d83c1921260602e5c31f89d2932933be030b162ed2bce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731fca3cccaa6984f70443a46c851de808863173eaa071233e98601991182dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06665145c5db8b93f761cec68150c11c97d51c561920f9400222968edb9becb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway_id: builtins.str,
    ip_address: builtins.str,
    remote_as_number: builtins.str,
    allow_as_in: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bfd_dead_multiple: typing.Optional[jsii.Number] = None,
    bfd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bfd_interval: typing.Optional[jsii.Number] = None,
    graceful_restart_mode: typing.Optional[builtins.str] = None,
    hold_down_timer: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    in_filter_ip_prefix_list_id: typing.Optional[builtins.str] = None,
    keep_alive_timer: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    out_filter_ip_prefix_list_id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    route_filtering: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
