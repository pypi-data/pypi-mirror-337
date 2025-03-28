'''
# `vcd_edgegateway_vpn`

Refer to the Terraform Registry for docs: [`vcd_edgegateway_vpn`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn).
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


class EdgegatewayVpn(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegatewayVpn.EdgegatewayVpn",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn vcd_edgegateway_vpn}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway: builtins.str,
        encryption_protocol: builtins.str,
        local_id: builtins.str,
        local_ip_address: builtins.str,
        mtu: jsii.Number,
        name: builtins.str,
        peer_id: builtins.str,
        peer_ip_address: builtins.str,
        shared_secret: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_subnets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayVpnLocalSubnets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        org: typing.Optional[builtins.str] = None,
        peer_subnets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayVpnPeerSubnets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn vcd_edgegateway_vpn} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#edge_gateway EdgegatewayVpn#edge_gateway}.
        :param encryption_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#encryption_protocol EdgegatewayVpn#encryption_protocol}.
        :param local_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_id EdgegatewayVpn#local_id}.
        :param local_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_ip_address EdgegatewayVpn#local_ip_address}.
        :param mtu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#mtu EdgegatewayVpn#mtu}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#name EdgegatewayVpn#name}.
        :param peer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_id EdgegatewayVpn#peer_id}.
        :param peer_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_ip_address EdgegatewayVpn#peer_ip_address}.
        :param shared_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#shared_secret EdgegatewayVpn#shared_secret}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#description EdgegatewayVpn#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#id EdgegatewayVpn#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_subnets: local_subnets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnets EdgegatewayVpn#local_subnets}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#org EdgegatewayVpn#org}
        :param peer_subnets: peer_subnets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnets EdgegatewayVpn#peer_subnets}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#vdc EdgegatewayVpn#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c556155f7dac2cc3f566220cce146dc18c626d92781209579da1e53cdced3e66)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EdgegatewayVpnConfig(
            edge_gateway=edge_gateway,
            encryption_protocol=encryption_protocol,
            local_id=local_id,
            local_ip_address=local_ip_address,
            mtu=mtu,
            name=name,
            peer_id=peer_id,
            peer_ip_address=peer_ip_address,
            shared_secret=shared_secret,
            description=description,
            id=id,
            local_subnets=local_subnets,
            org=org,
            peer_subnets=peer_subnets,
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
        '''Generates CDKTF code for importing a EdgegatewayVpn resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EdgegatewayVpn to import.
        :param import_from_id: The id of the existing EdgegatewayVpn that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EdgegatewayVpn to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5bb614c706b0577a51d0727d635588d5ee496c1f6b2ebb972e4498ef601164)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLocalSubnets")
    def put_local_subnets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayVpnLocalSubnets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67238aae2658e3d865022343ad8c9125e92f3f1c15ac87c02d207cd0c009051b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocalSubnets", [value]))

    @jsii.member(jsii_name="putPeerSubnets")
    def put_peer_subnets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayVpnPeerSubnets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ea74e96af1bb5c78516cd4e2a71d5cbb1caf0652526f8e552dd2bad1c98d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPeerSubnets", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocalSubnets")
    def reset_local_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSubnets", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetPeerSubnets")
    def reset_peer_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerSubnets", []))

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
    @jsii.member(jsii_name="localSubnets")
    def local_subnets(self) -> "EdgegatewayVpnLocalSubnetsList":
        return typing.cast("EdgegatewayVpnLocalSubnetsList", jsii.get(self, "localSubnets"))

    @builtins.property
    @jsii.member(jsii_name="peerSubnets")
    def peer_subnets(self) -> "EdgegatewayVpnPeerSubnetsList":
        return typing.cast("EdgegatewayVpnPeerSubnetsList", jsii.get(self, "peerSubnets"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayInput")
    def edge_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionProtocolInput")
    def encryption_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localIdInput")
    def local_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIdInput"))

    @builtins.property
    @jsii.member(jsii_name="localIpAddressInput")
    def local_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="localSubnetsInput")
    def local_subnets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayVpnLocalSubnets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayVpnLocalSubnets"]]], jsii.get(self, "localSubnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="mtuInput")
    def mtu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mtuInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIdInput")
    def peer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIpAddressInput")
    def peer_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="peerSubnetsInput")
    def peer_subnets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayVpnPeerSubnets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayVpnPeerSubnets"]]], jsii.get(self, "peerSubnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedSecretInput")
    def shared_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac2006d6eb1854810e852d59fc61fe0ffd53883b7f4fb0292b2d6cc078d7218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGateway")
    def edge_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGateway"))

    @edge_gateway.setter
    def edge_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4eec9ec7e73d7a79a0cb4ed09d103c3048e16cae230c8d5e01ed987bb386ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGateway", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionProtocol")
    def encryption_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionProtocol"))

    @encryption_protocol.setter
    def encryption_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d46e6ce464ce82c4895cd610dca694c7181cb32af87b535b57562d3b1cdc29c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c038bfb5a054e0c14a80f52367578779dadaa3be988380f362f1d84bc05b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="localId")
    def local_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localId"))

    @local_id.setter
    def local_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c959cf2317cda9324d7e4981da7b22359093174396ecb7944950d735087ff66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localId", value)

    @builtins.property
    @jsii.member(jsii_name="localIpAddress")
    def local_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localIpAddress"))

    @local_ip_address.setter
    def local_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50dc797363b64e337ddb630bc34404898edd4ca17cef3fea147a3cf2726ecff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b40f4b6c9003897962ccb323f38e32eb697292f6f6a1d4713ede2f02dc1df369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30813e2216bf14f6e9d868a4b180f549f5454b8e250926edc12c196d8d014863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f5b3b9f4977bc7ec9273be49900a6db070a5b6d6c1bc298a8cfb9bf15b4e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="peerId")
    def peer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerId"))

    @peer_id.setter
    def peer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ed196a448d3f4bf157de54804c8cc0385aca5230702b84dc46dc4d57bc65e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerId", value)

    @builtins.property
    @jsii.member(jsii_name="peerIpAddress")
    def peer_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpAddress"))

    @peer_ip_address.setter
    def peer_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e41381fce766fb5d50241832588a2ea7f194586021d7c6b09bf405573f7a7b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="sharedSecret")
    def shared_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedSecret"))

    @shared_secret.setter
    def shared_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdfb310353ef6358af0880e8c7b404bb6e51d6d703592ba74077b877b53f7be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedSecret", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0c02818912073578037a8cf8505b7e7c660adf54d0e258f67e953353ba8e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.edgegatewayVpn.EdgegatewayVpnConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "edge_gateway": "edgeGateway",
        "encryption_protocol": "encryptionProtocol",
        "local_id": "localId",
        "local_ip_address": "localIpAddress",
        "mtu": "mtu",
        "name": "name",
        "peer_id": "peerId",
        "peer_ip_address": "peerIpAddress",
        "shared_secret": "sharedSecret",
        "description": "description",
        "id": "id",
        "local_subnets": "localSubnets",
        "org": "org",
        "peer_subnets": "peerSubnets",
        "vdc": "vdc",
    },
)
class EdgegatewayVpnConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        edge_gateway: builtins.str,
        encryption_protocol: builtins.str,
        local_id: builtins.str,
        local_ip_address: builtins.str,
        mtu: jsii.Number,
        name: builtins.str,
        peer_id: builtins.str,
        peer_ip_address: builtins.str,
        shared_secret: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_subnets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayVpnLocalSubnets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        org: typing.Optional[builtins.str] = None,
        peer_subnets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgegatewayVpnPeerSubnets", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param edge_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#edge_gateway EdgegatewayVpn#edge_gateway}.
        :param encryption_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#encryption_protocol EdgegatewayVpn#encryption_protocol}.
        :param local_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_id EdgegatewayVpn#local_id}.
        :param local_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_ip_address EdgegatewayVpn#local_ip_address}.
        :param mtu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#mtu EdgegatewayVpn#mtu}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#name EdgegatewayVpn#name}.
        :param peer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_id EdgegatewayVpn#peer_id}.
        :param peer_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_ip_address EdgegatewayVpn#peer_ip_address}.
        :param shared_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#shared_secret EdgegatewayVpn#shared_secret}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#description EdgegatewayVpn#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#id EdgegatewayVpn#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_subnets: local_subnets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnets EdgegatewayVpn#local_subnets}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#org EdgegatewayVpn#org}
        :param peer_subnets: peer_subnets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnets EdgegatewayVpn#peer_subnets}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#vdc EdgegatewayVpn#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076602975836bda2d0f8d2df4d8c64445b6af728b2fe5384704444626d5fb5d0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway", value=edge_gateway, expected_type=type_hints["edge_gateway"])
            check_type(argname="argument encryption_protocol", value=encryption_protocol, expected_type=type_hints["encryption_protocol"])
            check_type(argname="argument local_id", value=local_id, expected_type=type_hints["local_id"])
            check_type(argname="argument local_ip_address", value=local_ip_address, expected_type=type_hints["local_ip_address"])
            check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument peer_id", value=peer_id, expected_type=type_hints["peer_id"])
            check_type(argname="argument peer_ip_address", value=peer_ip_address, expected_type=type_hints["peer_ip_address"])
            check_type(argname="argument shared_secret", value=shared_secret, expected_type=type_hints["shared_secret"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local_subnets", value=local_subnets, expected_type=type_hints["local_subnets"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument peer_subnets", value=peer_subnets, expected_type=type_hints["peer_subnets"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway": edge_gateway,
            "encryption_protocol": encryption_protocol,
            "local_id": local_id,
            "local_ip_address": local_ip_address,
            "mtu": mtu,
            "name": name,
            "peer_id": peer_id,
            "peer_ip_address": peer_ip_address,
            "shared_secret": shared_secret,
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
        if id is not None:
            self._values["id"] = id
        if local_subnets is not None:
            self._values["local_subnets"] = local_subnets
        if org is not None:
            self._values["org"] = org
        if peer_subnets is not None:
            self._values["peer_subnets"] = peer_subnets
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
    def edge_gateway(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#edge_gateway EdgegatewayVpn#edge_gateway}.'''
        result = self._values.get("edge_gateway")
        assert result is not None, "Required property 'edge_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#encryption_protocol EdgegatewayVpn#encryption_protocol}.'''
        result = self._values.get("encryption_protocol")
        assert result is not None, "Required property 'encryption_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_id EdgegatewayVpn#local_id}.'''
        result = self._values.get("local_id")
        assert result is not None, "Required property 'local_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_ip_address EdgegatewayVpn#local_ip_address}.'''
        result = self._values.get("local_ip_address")
        assert result is not None, "Required property 'local_ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mtu(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#mtu EdgegatewayVpn#mtu}.'''
        result = self._values.get("mtu")
        assert result is not None, "Required property 'mtu' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#name EdgegatewayVpn#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_id EdgegatewayVpn#peer_id}.'''
        result = self._values.get("peer_id")
        assert result is not None, "Required property 'peer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_ip_address EdgegatewayVpn#peer_ip_address}.'''
        result = self._values.get("peer_ip_address")
        assert result is not None, "Required property 'peer_ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shared_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#shared_secret EdgegatewayVpn#shared_secret}.'''
        result = self._values.get("shared_secret")
        assert result is not None, "Required property 'shared_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#description EdgegatewayVpn#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#id EdgegatewayVpn#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_subnets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayVpnLocalSubnets"]]]:
        '''local_subnets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnets EdgegatewayVpn#local_subnets}
        '''
        result = self._values.get("local_subnets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayVpnLocalSubnets"]]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#org EdgegatewayVpn#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_subnets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayVpnPeerSubnets"]]]:
        '''peer_subnets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnets EdgegatewayVpn#peer_subnets}
        '''
        result = self._values.get("peer_subnets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgegatewayVpnPeerSubnets"]]], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#vdc EdgegatewayVpn#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgegatewayVpnConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.edgegatewayVpn.EdgegatewayVpnLocalSubnets",
    jsii_struct_bases=[],
    name_mapping={
        "local_subnet_gateway": "localSubnetGateway",
        "local_subnet_mask": "localSubnetMask",
        "local_subnet_name": "localSubnetName",
    },
)
class EdgegatewayVpnLocalSubnets:
    def __init__(
        self,
        *,
        local_subnet_gateway: builtins.str,
        local_subnet_mask: builtins.str,
        local_subnet_name: builtins.str,
    ) -> None:
        '''
        :param local_subnet_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnet_gateway EdgegatewayVpn#local_subnet_gateway}.
        :param local_subnet_mask: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnet_mask EdgegatewayVpn#local_subnet_mask}.
        :param local_subnet_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnet_name EdgegatewayVpn#local_subnet_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d497d76530da662f3bc87bdc6a1260da5405196b988735d60672ea9e8a7d538b)
            check_type(argname="argument local_subnet_gateway", value=local_subnet_gateway, expected_type=type_hints["local_subnet_gateway"])
            check_type(argname="argument local_subnet_mask", value=local_subnet_mask, expected_type=type_hints["local_subnet_mask"])
            check_type(argname="argument local_subnet_name", value=local_subnet_name, expected_type=type_hints["local_subnet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_subnet_gateway": local_subnet_gateway,
            "local_subnet_mask": local_subnet_mask,
            "local_subnet_name": local_subnet_name,
        }

    @builtins.property
    def local_subnet_gateway(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnet_gateway EdgegatewayVpn#local_subnet_gateway}.'''
        result = self._values.get("local_subnet_gateway")
        assert result is not None, "Required property 'local_subnet_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_subnet_mask(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnet_mask EdgegatewayVpn#local_subnet_mask}.'''
        result = self._values.get("local_subnet_mask")
        assert result is not None, "Required property 'local_subnet_mask' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_subnet_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#local_subnet_name EdgegatewayVpn#local_subnet_name}.'''
        result = self._values.get("local_subnet_name")
        assert result is not None, "Required property 'local_subnet_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgegatewayVpnLocalSubnets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgegatewayVpnLocalSubnetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegatewayVpn.EdgegatewayVpnLocalSubnetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6aed9dd9d7e25368d69adfdcf227edd266d9be0d44aeed40872e2765336ffe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EdgegatewayVpnLocalSubnetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a8aa05b18ecde584093e0be61abd9cd4784dd5688645871c988036bc8c94eb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EdgegatewayVpnLocalSubnetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cfe37c28c2b0cd7c713a59280e57f1fcb3bdd48f2c99ff6eb5cbcb3cdc7886)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06d596553061bf39be6ca559eef646b5c285aeeda698b0a7b55af3a466a245b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a8dd37d4f0c6cf40eabb8c25ec48ca7c707679dfb16fd5ecbe5c7989564919f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayVpnLocalSubnets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayVpnLocalSubnets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayVpnLocalSubnets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399714c2ee9f7be36171e4c90886cd755015bce2cd3e87953cde9da1f4067ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EdgegatewayVpnLocalSubnetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegatewayVpn.EdgegatewayVpnLocalSubnetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c6a145951af21be3fdb57c3a8a2b967c079d3e408f16471759a8a1258ca3043)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="localSubnetGatewayInput")
    def local_subnet_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localSubnetGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="localSubnetMaskInput")
    def local_subnet_mask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localSubnetMaskInput"))

    @builtins.property
    @jsii.member(jsii_name="localSubnetNameInput")
    def local_subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localSubnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="localSubnetGateway")
    def local_subnet_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSubnetGateway"))

    @local_subnet_gateway.setter
    def local_subnet_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa02aa47d3a540db3e335ac2d1e5d76d6a67c8a8287cac43a87b0d04d1a631d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSubnetGateway", value)

    @builtins.property
    @jsii.member(jsii_name="localSubnetMask")
    def local_subnet_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSubnetMask"))

    @local_subnet_mask.setter
    def local_subnet_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4198cd1d2e641a09235f2d4bdfa8cbd5fd23f66872ab83bd5e4dbaa2e8f0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSubnetMask", value)

    @builtins.property
    @jsii.member(jsii_name="localSubnetName")
    def local_subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSubnetName"))

    @local_subnet_name.setter
    def local_subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c1ab591646c7ce2dd16e93fc9cdb5337dd651312692c053c7865fef4656aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSubnetName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayVpnLocalSubnets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayVpnLocalSubnets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayVpnLocalSubnets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e438a7611df436bf19d433021a0eb8f52182fdfedc697711b2f0f4c8f5b82e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.edgegatewayVpn.EdgegatewayVpnPeerSubnets",
    jsii_struct_bases=[],
    name_mapping={
        "peer_subnet_gateway": "peerSubnetGateway",
        "peer_subnet_mask": "peerSubnetMask",
        "peer_subnet_name": "peerSubnetName",
    },
)
class EdgegatewayVpnPeerSubnets:
    def __init__(
        self,
        *,
        peer_subnet_gateway: builtins.str,
        peer_subnet_mask: builtins.str,
        peer_subnet_name: builtins.str,
    ) -> None:
        '''
        :param peer_subnet_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnet_gateway EdgegatewayVpn#peer_subnet_gateway}.
        :param peer_subnet_mask: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnet_mask EdgegatewayVpn#peer_subnet_mask}.
        :param peer_subnet_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnet_name EdgegatewayVpn#peer_subnet_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2677c0ae71273ee6f5f31da4ccbbf497e96e7b18008e21ebcd60c72eee06650c)
            check_type(argname="argument peer_subnet_gateway", value=peer_subnet_gateway, expected_type=type_hints["peer_subnet_gateway"])
            check_type(argname="argument peer_subnet_mask", value=peer_subnet_mask, expected_type=type_hints["peer_subnet_mask"])
            check_type(argname="argument peer_subnet_name", value=peer_subnet_name, expected_type=type_hints["peer_subnet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peer_subnet_gateway": peer_subnet_gateway,
            "peer_subnet_mask": peer_subnet_mask,
            "peer_subnet_name": peer_subnet_name,
        }

    @builtins.property
    def peer_subnet_gateway(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnet_gateway EdgegatewayVpn#peer_subnet_gateway}.'''
        result = self._values.get("peer_subnet_gateway")
        assert result is not None, "Required property 'peer_subnet_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_subnet_mask(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnet_mask EdgegatewayVpn#peer_subnet_mask}.'''
        result = self._values.get("peer_subnet_mask")
        assert result is not None, "Required property 'peer_subnet_mask' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_subnet_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/edgegateway_vpn#peer_subnet_name EdgegatewayVpn#peer_subnet_name}.'''
        result = self._values.get("peer_subnet_name")
        assert result is not None, "Required property 'peer_subnet_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgegatewayVpnPeerSubnets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgegatewayVpnPeerSubnetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegatewayVpn.EdgegatewayVpnPeerSubnetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8285a1e647a2edbeb582acd776fadd410861c8bc1c8151608c84dd462b89751d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EdgegatewayVpnPeerSubnetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c55e12d8074f8bef3c34baeff67088b79d3887018e309167617cfae3fa8dacd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EdgegatewayVpnPeerSubnetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0423bb4103a9342315936d4c99946ae657b34041c13dd4e94312efd4766610c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c3e6bf31eda8af35ea5ec618f05d860f5fb872119b4bc1b936357e329e924d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__583cf2d85018b47ed19c1f32cbc40026e9a613946838598c66e0e2def48faa54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayVpnPeerSubnets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayVpnPeerSubnets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayVpnPeerSubnets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15b7ed8fa8f2e5f745f1c04536a87571f81ef08d24f2434acb9b65504a181ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EdgegatewayVpnPeerSubnetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.edgegatewayVpn.EdgegatewayVpnPeerSubnetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae0642f6baed529e9a6e6425af94d1a8e5b0ed767c8dd97df24efeb15edd6c4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="peerSubnetGatewayInput")
    def peer_subnet_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerSubnetGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="peerSubnetMaskInput")
    def peer_subnet_mask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerSubnetMaskInput"))

    @builtins.property
    @jsii.member(jsii_name="peerSubnetNameInput")
    def peer_subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerSubnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerSubnetGateway")
    def peer_subnet_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerSubnetGateway"))

    @peer_subnet_gateway.setter
    def peer_subnet_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a90c2230833dd3af0f8d374494e44a061870fdfd308f9eafd9fb821ab270f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerSubnetGateway", value)

    @builtins.property
    @jsii.member(jsii_name="peerSubnetMask")
    def peer_subnet_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerSubnetMask"))

    @peer_subnet_mask.setter
    def peer_subnet_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e262b91238a412ee3b7f2123201bc0f8625608f19ddde72f71fa75154e0b209a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerSubnetMask", value)

    @builtins.property
    @jsii.member(jsii_name="peerSubnetName")
    def peer_subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerSubnetName"))

    @peer_subnet_name.setter
    def peer_subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0b37bb0d222baf766a1e5d5d562f2cb42312b045c93589f5f4c6f026dd665d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerSubnetName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayVpnPeerSubnets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayVpnPeerSubnets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayVpnPeerSubnets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da7cf2b8ad0fcf9884e536ca35ab2a2a8f437df45b7b3e5efe588abb18df5ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "EdgegatewayVpn",
    "EdgegatewayVpnConfig",
    "EdgegatewayVpnLocalSubnets",
    "EdgegatewayVpnLocalSubnetsList",
    "EdgegatewayVpnLocalSubnetsOutputReference",
    "EdgegatewayVpnPeerSubnets",
    "EdgegatewayVpnPeerSubnetsList",
    "EdgegatewayVpnPeerSubnetsOutputReference",
]

publication.publish()

def _typecheckingstub__c556155f7dac2cc3f566220cce146dc18c626d92781209579da1e53cdced3e66(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway: builtins.str,
    encryption_protocol: builtins.str,
    local_id: builtins.str,
    local_ip_address: builtins.str,
    mtu: jsii.Number,
    name: builtins.str,
    peer_id: builtins.str,
    peer_ip_address: builtins.str,
    shared_secret: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_subnets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayVpnLocalSubnets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org: typing.Optional[builtins.str] = None,
    peer_subnets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayVpnPeerSubnets, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__2b5bb614c706b0577a51d0727d635588d5ee496c1f6b2ebb972e4498ef601164(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67238aae2658e3d865022343ad8c9125e92f3f1c15ac87c02d207cd0c009051b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayVpnLocalSubnets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ea74e96af1bb5c78516cd4e2a71d5cbb1caf0652526f8e552dd2bad1c98d35(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayVpnPeerSubnets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac2006d6eb1854810e852d59fc61fe0ffd53883b7f4fb0292b2d6cc078d7218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4eec9ec7e73d7a79a0cb4ed09d103c3048e16cae230c8d5e01ed987bb386ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d46e6ce464ce82c4895cd610dca694c7181cb32af87b535b57562d3b1cdc29c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c038bfb5a054e0c14a80f52367578779dadaa3be988380f362f1d84bc05b0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c959cf2317cda9324d7e4981da7b22359093174396ecb7944950d735087ff66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50dc797363b64e337ddb630bc34404898edd4ca17cef3fea147a3cf2726ecff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40f4b6c9003897962ccb323f38e32eb697292f6f6a1d4713ede2f02dc1df369(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30813e2216bf14f6e9d868a4b180f549f5454b8e250926edc12c196d8d014863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f5b3b9f4977bc7ec9273be49900a6db070a5b6d6c1bc298a8cfb9bf15b4e1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ed196a448d3f4bf157de54804c8cc0385aca5230702b84dc46dc4d57bc65e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e41381fce766fb5d50241832588a2ea7f194586021d7c6b09bf405573f7a7b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdfb310353ef6358af0880e8c7b404bb6e51d6d703592ba74077b877b53f7be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0c02818912073578037a8cf8505b7e7c660adf54d0e258f67e953353ba8e92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076602975836bda2d0f8d2df4d8c64445b6af728b2fe5384704444626d5fb5d0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway: builtins.str,
    encryption_protocol: builtins.str,
    local_id: builtins.str,
    local_ip_address: builtins.str,
    mtu: jsii.Number,
    name: builtins.str,
    peer_id: builtins.str,
    peer_ip_address: builtins.str,
    shared_secret: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_subnets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayVpnLocalSubnets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org: typing.Optional[builtins.str] = None,
    peer_subnets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgegatewayVpnPeerSubnets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d497d76530da662f3bc87bdc6a1260da5405196b988735d60672ea9e8a7d538b(
    *,
    local_subnet_gateway: builtins.str,
    local_subnet_mask: builtins.str,
    local_subnet_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6aed9dd9d7e25368d69adfdcf227edd266d9be0d44aeed40872e2765336ffe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a8aa05b18ecde584093e0be61abd9cd4784dd5688645871c988036bc8c94eb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cfe37c28c2b0cd7c713a59280e57f1fcb3bdd48f2c99ff6eb5cbcb3cdc7886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d596553061bf39be6ca559eef646b5c285aeeda698b0a7b55af3a466a245b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8dd37d4f0c6cf40eabb8c25ec48ca7c707679dfb16fd5ecbe5c7989564919f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399714c2ee9f7be36171e4c90886cd755015bce2cd3e87953cde9da1f4067ba8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayVpnLocalSubnets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6a145951af21be3fdb57c3a8a2b967c079d3e408f16471759a8a1258ca3043(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa02aa47d3a540db3e335ac2d1e5d76d6a67c8a8287cac43a87b0d04d1a631d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4198cd1d2e641a09235f2d4bdfa8cbd5fd23f66872ab83bd5e4dbaa2e8f0bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c1ab591646c7ce2dd16e93fc9cdb5337dd651312692c053c7865fef4656aa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e438a7611df436bf19d433021a0eb8f52182fdfedc697711b2f0f4c8f5b82e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayVpnLocalSubnets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2677c0ae71273ee6f5f31da4ccbbf497e96e7b18008e21ebcd60c72eee06650c(
    *,
    peer_subnet_gateway: builtins.str,
    peer_subnet_mask: builtins.str,
    peer_subnet_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8285a1e647a2edbeb582acd776fadd410861c8bc1c8151608c84dd462b89751d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c55e12d8074f8bef3c34baeff67088b79d3887018e309167617cfae3fa8dacd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0423bb4103a9342315936d4c99946ae657b34041c13dd4e94312efd4766610c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3e6bf31eda8af35ea5ec618f05d860f5fb872119b4bc1b936357e329e924d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583cf2d85018b47ed19c1f32cbc40026e9a613946838598c66e0e2def48faa54(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15b7ed8fa8f2e5f745f1c04536a87571f81ef08d24f2434acb9b65504a181ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgegatewayVpnPeerSubnets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0642f6baed529e9a6e6425af94d1a8e5b0ed767c8dd97df24efeb15edd6c4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a90c2230833dd3af0f8d374494e44a061870fdfd308f9eafd9fb821ab270f0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e262b91238a412ee3b7f2123201bc0f8625608f19ddde72f71fa75154e0b209a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0b37bb0d222baf766a1e5d5d562f2cb42312b045c93589f5f4c6f026dd665d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da7cf2b8ad0fcf9884e536ca35ab2a2a8f437df45b7b3e5efe588abb18df5ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgegatewayVpnPeerSubnets]],
) -> None:
    """Type checking stubs"""
    pass
