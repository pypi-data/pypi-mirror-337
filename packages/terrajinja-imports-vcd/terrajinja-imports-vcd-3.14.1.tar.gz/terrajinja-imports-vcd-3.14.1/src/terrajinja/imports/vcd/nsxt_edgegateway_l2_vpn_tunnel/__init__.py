'''
# `vcd_nsxt_edgegateway_l2_vpn_tunnel`

Refer to the Terraform Registry for docs: [`vcd_nsxt_edgegateway_l2_vpn_tunnel`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel).
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


class NsxtEdgegatewayL2VpnTunnel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayL2VpnTunnel.NsxtEdgegatewayL2VpnTunnel",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel vcd_nsxt_edgegateway_l2_vpn_tunnel}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway_id: builtins.str,
        local_endpoint_ip: builtins.str,
        name: builtins.str,
        remote_endpoint_ip: builtins.str,
        session_mode: builtins.str,
        connector_initiation_mode: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        peer_code: typing.Optional[builtins.str] = None,
        pre_shared_key: typing.Optional[builtins.str] = None,
        stretched_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayL2VpnTunnelStretchedNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tunnel_interface: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel vcd_nsxt_edgegateway_l2_vpn_tunnel} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway_id: Edge Gateway ID for the tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#edge_gateway_id NsxtEdgegatewayL2VpnTunnel#edge_gateway_id}
        :param local_endpoint_ip: Local endpoint IP of the tunnel session, the IP must be sub-allocated to the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#local_endpoint_ip NsxtEdgegatewayL2VpnTunnel#local_endpoint_ip}
        :param name: Name of the L2 VPN Tunnel session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#name NsxtEdgegatewayL2VpnTunnel#name}
        :param remote_endpoint_ip: The IP address of the remote endpoint, which corresponds to the deviceon the remote site terminating the VPN tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#remote_endpoint_ip NsxtEdgegatewayL2VpnTunnel#remote_endpoint_ip}
        :param session_mode: Mode of the tunnel session, must be CLIENT or SERVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#session_mode NsxtEdgegatewayL2VpnTunnel#session_mode}
        :param connector_initiation_mode: Connector initation mode of the session describing how a connection is made. Needs to be set only if ``session_mode`` is set to ``SERVER`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#connector_initiation_mode NsxtEdgegatewayL2VpnTunnel#connector_initiation_mode}
        :param description: Description of the L2 VPN Tunnel session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#description NsxtEdgegatewayL2VpnTunnel#description}
        :param enabled: Status of the L2 VPN Tunnel session. Always set to ``true`` for CLIENT sessions. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#enabled NsxtEdgegatewayL2VpnTunnel#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#id NsxtEdgegatewayL2VpnTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#org NsxtEdgegatewayL2VpnTunnel#org}
        :param peer_code: Base64 encoded string of the full configuration of the tunnel provided by the SERVER session. It is a computed field for SERVER sessions and is a required field for CLIENT sessions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#peer_code NsxtEdgegatewayL2VpnTunnel#peer_code}
        :param pre_shared_key: Pre-shared key used for authentication, needs to be provided only for``SERVER`` sessions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#pre_shared_key NsxtEdgegatewayL2VpnTunnel#pre_shared_key}
        :param stretched_network: stretched_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#stretched_network NsxtEdgegatewayL2VpnTunnel#stretched_network}
        :param tunnel_interface: Network CIDR block over which the session interfaces. Only relevant if ``session_mode`` is set to ``SERVER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#tunnel_interface NsxtEdgegatewayL2VpnTunnel#tunnel_interface}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63205f90586a9997779b1552908f527a7d3d8ab2670e3e0fed0f3c4fa56209e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtEdgegatewayL2VpnTunnelConfig(
            edge_gateway_id=edge_gateway_id,
            local_endpoint_ip=local_endpoint_ip,
            name=name,
            remote_endpoint_ip=remote_endpoint_ip,
            session_mode=session_mode,
            connector_initiation_mode=connector_initiation_mode,
            description=description,
            enabled=enabled,
            id=id,
            org=org,
            peer_code=peer_code,
            pre_shared_key=pre_shared_key,
            stretched_network=stretched_network,
            tunnel_interface=tunnel_interface,
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
        '''Generates CDKTF code for importing a NsxtEdgegatewayL2VpnTunnel resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtEdgegatewayL2VpnTunnel to import.
        :param import_from_id: The id of the existing NsxtEdgegatewayL2VpnTunnel that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtEdgegatewayL2VpnTunnel to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8857ced4c6d2bffcd40af025f9750260b6e7ad65c5482b70a7962ccd3aacdb55)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStretchedNetwork")
    def put_stretched_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayL2VpnTunnelStretchedNetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a02285ab3af0639e1be17f497711ad68f35da2df9a30cefe530945440c20ff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStretchedNetwork", [value]))

    @jsii.member(jsii_name="resetConnectorInitiationMode")
    def reset_connector_initiation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorInitiationMode", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetPeerCode")
    def reset_peer_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerCode", []))

    @jsii.member(jsii_name="resetPreSharedKey")
    def reset_pre_shared_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreSharedKey", []))

    @jsii.member(jsii_name="resetStretchedNetwork")
    def reset_stretched_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStretchedNetwork", []))

    @jsii.member(jsii_name="resetTunnelInterface")
    def reset_tunnel_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelInterface", []))

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
    @jsii.member(jsii_name="stretchedNetwork")
    def stretched_network(self) -> "NsxtEdgegatewayL2VpnTunnelStretchedNetworkList":
        return typing.cast("NsxtEdgegatewayL2VpnTunnelStretchedNetworkList", jsii.get(self, "stretchedNetwork"))

    @builtins.property
    @jsii.member(jsii_name="connectorInitiationModeInput")
    def connector_initiation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorInitiationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localEndpointIpInput")
    def local_endpoint_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localEndpointIpInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="peerCodeInput")
    def peer_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="preSharedKeyInput")
    def pre_shared_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preSharedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteEndpointIpInput")
    def remote_endpoint_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteEndpointIpInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionModeInput")
    def session_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="stretchedNetworkInput")
    def stretched_network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayL2VpnTunnelStretchedNetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayL2VpnTunnelStretchedNetwork"]]], jsii.get(self, "stretchedNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelInterfaceInput")
    def tunnel_interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorInitiationMode")
    def connector_initiation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorInitiationMode"))

    @connector_initiation_mode.setter
    def connector_initiation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12fcde7ab96d4d899ba8527361ea0b4db40c2fe9d0817193cbf08ffe316e3d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorInitiationMode", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0e38dadfbb5a1b9840f0017e2137f628ee621ec85a1e9e639b4281fa0da98d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayId")
    def edge_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGatewayId"))

    @edge_gateway_id.setter
    def edge_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df85576caf6df9724227ce2342de555637d77a719fdca1df4950615e67dedd98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea3ffad1b92ac42bd72bb2cdda1a47a608cb54d52db826688c41b651b44feae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e36772f16f462d051eefd2826d88e07b810fdb6e4eb2f9fd05c88e745e96bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="localEndpointIp")
    def local_endpoint_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localEndpointIp"))

    @local_endpoint_ip.setter
    def local_endpoint_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68364334314625c9f990197a5e07a4a454b39799aca172a214974cb06bb4691c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localEndpointIp", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc55eacdf5c224e4b43c7773a84d440053586323e85490fb872118e5fe4c782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611b15d1eae468249cd0764e441ddc91cd516878d745f36dbd067504a1db4507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="peerCode")
    def peer_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerCode"))

    @peer_code.setter
    def peer_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7cfd07e76acd704233ee9a24ea09e81c141c7b64952ad98813ca9c770cdf6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerCode", value)

    @builtins.property
    @jsii.member(jsii_name="preSharedKey")
    def pre_shared_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preSharedKey"))

    @pre_shared_key.setter
    def pre_shared_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f996485bf4b6c7ecf08c3a0b6cf60ea63c2acd81c714f0f56db4476eb0a575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preSharedKey", value)

    @builtins.property
    @jsii.member(jsii_name="remoteEndpointIp")
    def remote_endpoint_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteEndpointIp"))

    @remote_endpoint_ip.setter
    def remote_endpoint_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf24dee3701c6e21790f032a50581bc4145bf0fdbf104d6d611b634d73b334b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteEndpointIp", value)

    @builtins.property
    @jsii.member(jsii_name="sessionMode")
    def session_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionMode"))

    @session_mode.setter
    def session_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8796928160f91fb562cc5e03eb0b6ff442bccc66e8cfc869831a55414e3aecf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionMode", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelInterface")
    def tunnel_interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelInterface"))

    @tunnel_interface.setter
    def tunnel_interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1a6c1fc0afdaba3899f83ba26efcd96a3642e6f53493a4157e95668d481ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelInterface", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegatewayL2VpnTunnel.NsxtEdgegatewayL2VpnTunnelConfig",
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
        "local_endpoint_ip": "localEndpointIp",
        "name": "name",
        "remote_endpoint_ip": "remoteEndpointIp",
        "session_mode": "sessionMode",
        "connector_initiation_mode": "connectorInitiationMode",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "org": "org",
        "peer_code": "peerCode",
        "pre_shared_key": "preSharedKey",
        "stretched_network": "stretchedNetwork",
        "tunnel_interface": "tunnelInterface",
    },
)
class NsxtEdgegatewayL2VpnTunnelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        local_endpoint_ip: builtins.str,
        name: builtins.str,
        remote_endpoint_ip: builtins.str,
        session_mode: builtins.str,
        connector_initiation_mode: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        peer_code: typing.Optional[builtins.str] = None,
        pre_shared_key: typing.Optional[builtins.str] = None,
        stretched_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayL2VpnTunnelStretchedNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tunnel_interface: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param edge_gateway_id: Edge Gateway ID for the tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#edge_gateway_id NsxtEdgegatewayL2VpnTunnel#edge_gateway_id}
        :param local_endpoint_ip: Local endpoint IP of the tunnel session, the IP must be sub-allocated to the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#local_endpoint_ip NsxtEdgegatewayL2VpnTunnel#local_endpoint_ip}
        :param name: Name of the L2 VPN Tunnel session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#name NsxtEdgegatewayL2VpnTunnel#name}
        :param remote_endpoint_ip: The IP address of the remote endpoint, which corresponds to the deviceon the remote site terminating the VPN tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#remote_endpoint_ip NsxtEdgegatewayL2VpnTunnel#remote_endpoint_ip}
        :param session_mode: Mode of the tunnel session, must be CLIENT or SERVER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#session_mode NsxtEdgegatewayL2VpnTunnel#session_mode}
        :param connector_initiation_mode: Connector initation mode of the session describing how a connection is made. Needs to be set only if ``session_mode`` is set to ``SERVER`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#connector_initiation_mode NsxtEdgegatewayL2VpnTunnel#connector_initiation_mode}
        :param description: Description of the L2 VPN Tunnel session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#description NsxtEdgegatewayL2VpnTunnel#description}
        :param enabled: Status of the L2 VPN Tunnel session. Always set to ``true`` for CLIENT sessions. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#enabled NsxtEdgegatewayL2VpnTunnel#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#id NsxtEdgegatewayL2VpnTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#org NsxtEdgegatewayL2VpnTunnel#org}
        :param peer_code: Base64 encoded string of the full configuration of the tunnel provided by the SERVER session. It is a computed field for SERVER sessions and is a required field for CLIENT sessions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#peer_code NsxtEdgegatewayL2VpnTunnel#peer_code}
        :param pre_shared_key: Pre-shared key used for authentication, needs to be provided only for``SERVER`` sessions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#pre_shared_key NsxtEdgegatewayL2VpnTunnel#pre_shared_key}
        :param stretched_network: stretched_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#stretched_network NsxtEdgegatewayL2VpnTunnel#stretched_network}
        :param tunnel_interface: Network CIDR block over which the session interfaces. Only relevant if ``session_mode`` is set to ``SERVER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#tunnel_interface NsxtEdgegatewayL2VpnTunnel#tunnel_interface}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0999092e9245fa4e4bc9255cbadedadcf208b65d253334960a7c0d99a071730d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway_id", value=edge_gateway_id, expected_type=type_hints["edge_gateway_id"])
            check_type(argname="argument local_endpoint_ip", value=local_endpoint_ip, expected_type=type_hints["local_endpoint_ip"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument remote_endpoint_ip", value=remote_endpoint_ip, expected_type=type_hints["remote_endpoint_ip"])
            check_type(argname="argument session_mode", value=session_mode, expected_type=type_hints["session_mode"])
            check_type(argname="argument connector_initiation_mode", value=connector_initiation_mode, expected_type=type_hints["connector_initiation_mode"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument peer_code", value=peer_code, expected_type=type_hints["peer_code"])
            check_type(argname="argument pre_shared_key", value=pre_shared_key, expected_type=type_hints["pre_shared_key"])
            check_type(argname="argument stretched_network", value=stretched_network, expected_type=type_hints["stretched_network"])
            check_type(argname="argument tunnel_interface", value=tunnel_interface, expected_type=type_hints["tunnel_interface"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway_id": edge_gateway_id,
            "local_endpoint_ip": local_endpoint_ip,
            "name": name,
            "remote_endpoint_ip": remote_endpoint_ip,
            "session_mode": session_mode,
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
        if connector_initiation_mode is not None:
            self._values["connector_initiation_mode"] = connector_initiation_mode
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if org is not None:
            self._values["org"] = org
        if peer_code is not None:
            self._values["peer_code"] = peer_code
        if pre_shared_key is not None:
            self._values["pre_shared_key"] = pre_shared_key
        if stretched_network is not None:
            self._values["stretched_network"] = stretched_network
        if tunnel_interface is not None:
            self._values["tunnel_interface"] = tunnel_interface

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
        '''Edge Gateway ID for the tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#edge_gateway_id NsxtEdgegatewayL2VpnTunnel#edge_gateway_id}
        '''
        result = self._values.get("edge_gateway_id")
        assert result is not None, "Required property 'edge_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_endpoint_ip(self) -> builtins.str:
        '''Local endpoint IP of the tunnel session, the IP must be sub-allocated to the Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#local_endpoint_ip NsxtEdgegatewayL2VpnTunnel#local_endpoint_ip}
        '''
        result = self._values.get("local_endpoint_ip")
        assert result is not None, "Required property 'local_endpoint_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the L2 VPN Tunnel session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#name NsxtEdgegatewayL2VpnTunnel#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_endpoint_ip(self) -> builtins.str:
        '''The IP address of the remote endpoint, which corresponds to the deviceon the remote site terminating the VPN tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#remote_endpoint_ip NsxtEdgegatewayL2VpnTunnel#remote_endpoint_ip}
        '''
        result = self._values.get("remote_endpoint_ip")
        assert result is not None, "Required property 'remote_endpoint_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_mode(self) -> builtins.str:
        '''Mode of the tunnel session, must be CLIENT or SERVER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#session_mode NsxtEdgegatewayL2VpnTunnel#session_mode}
        '''
        result = self._values.get("session_mode")
        assert result is not None, "Required property 'session_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_initiation_mode(self) -> typing.Optional[builtins.str]:
        '''Connector initation mode of the session describing how a connection is made.

        Needs to be set only if ``session_mode`` is set to ``SERVER``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#connector_initiation_mode NsxtEdgegatewayL2VpnTunnel#connector_initiation_mode}
        '''
        result = self._values.get("connector_initiation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the L2 VPN Tunnel session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#description NsxtEdgegatewayL2VpnTunnel#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Status of the L2 VPN Tunnel session. Always set to ``true`` for CLIENT sessions. Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#enabled NsxtEdgegatewayL2VpnTunnel#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#id NsxtEdgegatewayL2VpnTunnel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#org NsxtEdgegatewayL2VpnTunnel#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_code(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded string of the full configuration of the tunnel provided by the SERVER session.

        It is a computed field for SERVER sessions and is a required field for CLIENT sessions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#peer_code NsxtEdgegatewayL2VpnTunnel#peer_code}
        '''
        result = self._values.get("peer_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_shared_key(self) -> typing.Optional[builtins.str]:
        '''Pre-shared key used for authentication, needs to be provided only for``SERVER`` sessions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#pre_shared_key NsxtEdgegatewayL2VpnTunnel#pre_shared_key}
        '''
        result = self._values.get("pre_shared_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stretched_network(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayL2VpnTunnelStretchedNetwork"]]]:
        '''stretched_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#stretched_network NsxtEdgegatewayL2VpnTunnel#stretched_network}
        '''
        result = self._values.get("stretched_network")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayL2VpnTunnelStretchedNetwork"]]], result)

    @builtins.property
    def tunnel_interface(self) -> typing.Optional[builtins.str]:
        '''Network CIDR block over which the session interfaces. Only relevant if ``session_mode`` is set to ``SERVER``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#tunnel_interface NsxtEdgegatewayL2VpnTunnel#tunnel_interface}
        '''
        result = self._values.get("tunnel_interface")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayL2VpnTunnelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegatewayL2VpnTunnel.NsxtEdgegatewayL2VpnTunnelStretchedNetwork",
    jsii_struct_bases=[],
    name_mapping={"network_id": "networkId", "tunnel_id": "tunnelId"},
)
class NsxtEdgegatewayL2VpnTunnelStretchedNetwork:
    def __init__(
        self,
        *,
        network_id: builtins.str,
        tunnel_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param network_id: ID of the Org VDC network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#network_id NsxtEdgegatewayL2VpnTunnel#network_id}
        :param tunnel_id: Tunnel ID of the network for the tunnel. Read-only for ``SERVER`` sessions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#tunnel_id NsxtEdgegatewayL2VpnTunnel#tunnel_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d602db5f9b3ac3d488090aec3125edda153de29dc4e2c5962e8f0925c411cb3a)
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument tunnel_id", value=tunnel_id, expected_type=type_hints["tunnel_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_id": network_id,
        }
        if tunnel_id is not None:
            self._values["tunnel_id"] = tunnel_id

    @builtins.property
    def network_id(self) -> builtins.str:
        '''ID of the Org VDC network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#network_id NsxtEdgegatewayL2VpnTunnel#network_id}
        '''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tunnel_id(self) -> typing.Optional[jsii.Number]:
        '''Tunnel ID of the network for the tunnel. Read-only for ``SERVER`` sessions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_l2_vpn_tunnel#tunnel_id NsxtEdgegatewayL2VpnTunnel#tunnel_id}
        '''
        result = self._values.get("tunnel_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayL2VpnTunnelStretchedNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtEdgegatewayL2VpnTunnelStretchedNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayL2VpnTunnel.NsxtEdgegatewayL2VpnTunnelStretchedNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70ca7599a852ed48d4c6d0cacf7fc6d7b89bd3277a1972c7fb5b56eb527a9607)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtEdgegatewayL2VpnTunnelStretchedNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a187f2272c68151020fba1d8646e4a7a835cb08825b0186ede2ff851000ace)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtEdgegatewayL2VpnTunnelStretchedNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f14ebd8de5e99651eea17a4893451ed8c5051c89d157c10e9e18611a14538424)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aaf0eca1922c03c2a1921aa0c09062d4a4293104502c2d350d507a15e1f3787)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a581b608e4ee76f82b4d65781c167e85058ec09aa70f54fc36e7efd40d9e1eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayL2VpnTunnelStretchedNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayL2VpnTunnelStretchedNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayL2VpnTunnelStretchedNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0761c6db44636323857f72cd2941e2a44cebf6afefb0345d1c1ba9412db75d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewayL2VpnTunnelStretchedNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayL2VpnTunnel.NsxtEdgegatewayL2VpnTunnelStretchedNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bec0ef6d0813319c9cde15da2daa8700b39e8239e0e896d64f3fac829d1c427f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTunnelId")
    def reset_tunnel_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelId", []))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelIdInput")
    def tunnel_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2bd29c560e4af687e4e17fcd5fee4f4067106778d364f3eda5426e4708948d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelId")
    def tunnel_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnelId"))

    @tunnel_id.setter
    def tunnel_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e67e5e1ce22e1561f03224ac55c2fb563e22c636a9552bd942d4acfebcd92c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayL2VpnTunnelStretchedNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayL2VpnTunnelStretchedNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayL2VpnTunnelStretchedNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957da7a6102acd623765b17cc04bee9d09f27fe942deaecf943996be03873826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtEdgegatewayL2VpnTunnel",
    "NsxtEdgegatewayL2VpnTunnelConfig",
    "NsxtEdgegatewayL2VpnTunnelStretchedNetwork",
    "NsxtEdgegatewayL2VpnTunnelStretchedNetworkList",
    "NsxtEdgegatewayL2VpnTunnelStretchedNetworkOutputReference",
]

publication.publish()

def _typecheckingstub__c63205f90586a9997779b1552908f527a7d3d8ab2670e3e0fed0f3c4fa56209e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway_id: builtins.str,
    local_endpoint_ip: builtins.str,
    name: builtins.str,
    remote_endpoint_ip: builtins.str,
    session_mode: builtins.str,
    connector_initiation_mode: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    peer_code: typing.Optional[builtins.str] = None,
    pre_shared_key: typing.Optional[builtins.str] = None,
    stretched_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayL2VpnTunnelStretchedNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tunnel_interface: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8857ced4c6d2bffcd40af025f9750260b6e7ad65c5482b70a7962ccd3aacdb55(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a02285ab3af0639e1be17f497711ad68f35da2df9a30cefe530945440c20ff9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayL2VpnTunnelStretchedNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fcde7ab96d4d899ba8527361ea0b4db40c2fe9d0817193cbf08ffe316e3d42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0e38dadfbb5a1b9840f0017e2137f628ee621ec85a1e9e639b4281fa0da98d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df85576caf6df9724227ce2342de555637d77a719fdca1df4950615e67dedd98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3ffad1b92ac42bd72bb2cdda1a47a608cb54d52db826688c41b651b44feae8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e36772f16f462d051eefd2826d88e07b810fdb6e4eb2f9fd05c88e745e96bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68364334314625c9f990197a5e07a4a454b39799aca172a214974cb06bb4691c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc55eacdf5c224e4b43c7773a84d440053586323e85490fb872118e5fe4c782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611b15d1eae468249cd0764e441ddc91cd516878d745f36dbd067504a1db4507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7cfd07e76acd704233ee9a24ea09e81c141c7b64952ad98813ca9c770cdf6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f996485bf4b6c7ecf08c3a0b6cf60ea63c2acd81c714f0f56db4476eb0a575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf24dee3701c6e21790f032a50581bc4145bf0fdbf104d6d611b634d73b334b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8796928160f91fb562cc5e03eb0b6ff442bccc66e8cfc869831a55414e3aecf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1a6c1fc0afdaba3899f83ba26efcd96a3642e6f53493a4157e95668d481ce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0999092e9245fa4e4bc9255cbadedadcf208b65d253334960a7c0d99a071730d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway_id: builtins.str,
    local_endpoint_ip: builtins.str,
    name: builtins.str,
    remote_endpoint_ip: builtins.str,
    session_mode: builtins.str,
    connector_initiation_mode: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    peer_code: typing.Optional[builtins.str] = None,
    pre_shared_key: typing.Optional[builtins.str] = None,
    stretched_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayL2VpnTunnelStretchedNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tunnel_interface: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d602db5f9b3ac3d488090aec3125edda153de29dc4e2c5962e8f0925c411cb3a(
    *,
    network_id: builtins.str,
    tunnel_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ca7599a852ed48d4c6d0cacf7fc6d7b89bd3277a1972c7fb5b56eb527a9607(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a187f2272c68151020fba1d8646e4a7a835cb08825b0186ede2ff851000ace(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14ebd8de5e99651eea17a4893451ed8c5051c89d157c10e9e18611a14538424(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaf0eca1922c03c2a1921aa0c09062d4a4293104502c2d350d507a15e1f3787(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a581b608e4ee76f82b4d65781c167e85058ec09aa70f54fc36e7efd40d9e1eb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0761c6db44636323857f72cd2941e2a44cebf6afefb0345d1c1ba9412db75d26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayL2VpnTunnelStretchedNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec0ef6d0813319c9cde15da2daa8700b39e8239e0e896d64f3fac829d1c427f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2bd29c560e4af687e4e17fcd5fee4f4067106778d364f3eda5426e4708948d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e67e5e1ce22e1561f03224ac55c2fb563e22c636a9552bd942d4acfebcd92c4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957da7a6102acd623765b17cc04bee9d09f27fe942deaecf943996be03873826(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayL2VpnTunnelStretchedNetwork]],
) -> None:
    """Type checking stubs"""
    pass
