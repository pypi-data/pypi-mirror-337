'''
# `vcd_nsxv_dhcp_relay`

Refer to the Terraform Registry for docs: [`vcd_nsxv_dhcp_relay`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay).
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


class NsxvDhcpRelay(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvDhcpRelay.NsxvDhcpRelay",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay vcd_nsxv_dhcp_relay}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway: builtins.str,
        relay_agent: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxvDhcpRelayRelayAgent", typing.Dict[builtins.str, typing.Any]]]],
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay vcd_nsxv_dhcp_relay} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway: Edge gateway name for DHCP relay settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#edge_gateway NsxvDhcpRelay#edge_gateway}
        :param relay_agent: relay_agent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#relay_agent NsxvDhcpRelay#relay_agent}
        :param domain_names: A set of IP domain names of DHCP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#domain_names NsxvDhcpRelay#domain_names}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#id NsxvDhcpRelay#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_addresses: A set of IP address of DHCP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#ip_addresses NsxvDhcpRelay#ip_addresses}
        :param ip_sets: A set of IP set names which consist DHCP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#ip_sets NsxvDhcpRelay#ip_sets}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#org NsxvDhcpRelay#org}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#vdc NsxvDhcpRelay#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22323c177dfbcf43e9f79236dea8727ad2a48d245ce0e405775245223f5890fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxvDhcpRelayConfig(
            edge_gateway=edge_gateway,
            relay_agent=relay_agent,
            domain_names=domain_names,
            id=id,
            ip_addresses=ip_addresses,
            ip_sets=ip_sets,
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
        '''Generates CDKTF code for importing a NsxvDhcpRelay resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxvDhcpRelay to import.
        :param import_from_id: The id of the existing NsxvDhcpRelay that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxvDhcpRelay to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e25a7fda6df373d80e2a88c20d4ba6c68149a742426ee6d2e1222fd096a9190)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRelayAgent")
    def put_relay_agent(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxvDhcpRelayRelayAgent", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24eb70ce3110b5552096c861bb36655081e77aafad779a5053175620669eb991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRelayAgent", [value]))

    @jsii.member(jsii_name="resetDomainNames")
    def reset_domain_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainNames", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAddresses")
    def reset_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddresses", []))

    @jsii.member(jsii_name="resetIpSets")
    def reset_ip_sets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpSets", []))

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
    @jsii.member(jsii_name="relayAgent")
    def relay_agent(self) -> "NsxvDhcpRelayRelayAgentList":
        return typing.cast("NsxvDhcpRelayRelayAgentList", jsii.get(self, "relayAgent"))

    @builtins.property
    @jsii.member(jsii_name="domainNamesInput")
    def domain_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayInput")
    def edge_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSetsInput")
    def ip_sets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipSetsInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="relayAgentInput")
    def relay_agent_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxvDhcpRelayRelayAgent"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxvDhcpRelayRelayAgent"]]], jsii.get(self, "relayAgentInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNames")
    def domain_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainNames"))

    @domain_names.setter
    def domain_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4636ca6f64b5b3afb4c861892034e20965db73de964d0e28d652303db475ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNames", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGateway")
    def edge_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGateway"))

    @edge_gateway.setter
    def edge_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0db861c1549ab0dfecf1854834deb648d1de232c61f65bf1e93c50fc87dacd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGateway", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc1e9bfc99af2073ab8c839f2d6f38dab61ff952948bed21249234e1eaab3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77eee9133193dc7b9131892d80be624792fb114119dfb80258634db28117711e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="ipSets")
    def ip_sets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipSets"))

    @ip_sets.setter
    def ip_sets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6b8e652bfe39273a6d4ac54352dc0918c3d38f54372044e8de857e040c7bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSets", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b4fad4349689faa37b662c536fb16823e481fe83fdee93dda9c2378623c87d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54f47c6e818e48f26779bdac6af8f272995eb05d8c724f47be8b1dc46db3914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.nsxvDhcpRelay.NsxvDhcpRelayConfig",
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
        "relay_agent": "relayAgent",
        "domain_names": "domainNames",
        "id": "id",
        "ip_addresses": "ipAddresses",
        "ip_sets": "ipSets",
        "org": "org",
        "vdc": "vdc",
    },
)
class NsxvDhcpRelayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        relay_agent: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxvDhcpRelayRelayAgent", typing.Dict[builtins.str, typing.Any]]]],
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        :param edge_gateway: Edge gateway name for DHCP relay settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#edge_gateway NsxvDhcpRelay#edge_gateway}
        :param relay_agent: relay_agent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#relay_agent NsxvDhcpRelay#relay_agent}
        :param domain_names: A set of IP domain names of DHCP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#domain_names NsxvDhcpRelay#domain_names}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#id NsxvDhcpRelay#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_addresses: A set of IP address of DHCP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#ip_addresses NsxvDhcpRelay#ip_addresses}
        :param ip_sets: A set of IP set names which consist DHCP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#ip_sets NsxvDhcpRelay#ip_sets}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#org NsxvDhcpRelay#org}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#vdc NsxvDhcpRelay#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5340ba4900a66bc0833c8a608b87cebdb33e0d32ea0da6b803d8854207258cef)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway", value=edge_gateway, expected_type=type_hints["edge_gateway"])
            check_type(argname="argument relay_agent", value=relay_agent, expected_type=type_hints["relay_agent"])
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument ip_sets", value=ip_sets, expected_type=type_hints["ip_sets"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway": edge_gateway,
            "relay_agent": relay_agent,
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
        if domain_names is not None:
            self._values["domain_names"] = domain_names
        if id is not None:
            self._values["id"] = id
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if ip_sets is not None:
            self._values["ip_sets"] = ip_sets
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
    def edge_gateway(self) -> builtins.str:
        '''Edge gateway name for DHCP relay settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#edge_gateway NsxvDhcpRelay#edge_gateway}
        '''
        result = self._values.get("edge_gateway")
        assert result is not None, "Required property 'edge_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def relay_agent(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxvDhcpRelayRelayAgent"]]:
        '''relay_agent block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#relay_agent NsxvDhcpRelay#relay_agent}
        '''
        result = self._values.get("relay_agent")
        assert result is not None, "Required property 'relay_agent' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxvDhcpRelayRelayAgent"]], result)

    @builtins.property
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of IP domain names of DHCP servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#domain_names NsxvDhcpRelay#domain_names}
        '''
        result = self._values.get("domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#id NsxvDhcpRelay#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of IP address of DHCP servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#ip_addresses NsxvDhcpRelay#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_sets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of IP set names which consist DHCP servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#ip_sets NsxvDhcpRelay#ip_sets}
        '''
        result = self._values.get("ip_sets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#org NsxvDhcpRelay#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#vdc NsxvDhcpRelay#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxvDhcpRelayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxvDhcpRelay.NsxvDhcpRelayRelayAgent",
    jsii_struct_bases=[],
    name_mapping={
        "network_name": "networkName",
        "gateway_ip_address": "gatewayIpAddress",
    },
)
class NsxvDhcpRelayRelayAgent:
    def __init__(
        self,
        *,
        network_name: builtins.str,
        gateway_ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_name: Org network which is to be used for relaying DHCP message to specified servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#network_name NsxvDhcpRelay#network_name}
        :param gateway_ip_address: Optional gateway IP address of org network which is to be used for relaying DHCP message to specified servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#gateway_ip_address NsxvDhcpRelay#gateway_ip_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00e61636a5b8089db7a51520a22f07ca56b287109d847347984e58fa285faab)
            check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
            check_type(argname="argument gateway_ip_address", value=gateway_ip_address, expected_type=type_hints["gateway_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_name": network_name,
        }
        if gateway_ip_address is not None:
            self._values["gateway_ip_address"] = gateway_ip_address

    @builtins.property
    def network_name(self) -> builtins.str:
        '''Org network which is to be used for relaying DHCP message to specified servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#network_name NsxvDhcpRelay#network_name}
        '''
        result = self._values.get("network_name")
        assert result is not None, "Required property 'network_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway_ip_address(self) -> typing.Optional[builtins.str]:
        '''Optional gateway IP address of org network which is to be used for relaying DHCP message to specified servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dhcp_relay#gateway_ip_address NsxvDhcpRelay#gateway_ip_address}
        '''
        result = self._values.get("gateway_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxvDhcpRelayRelayAgent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxvDhcpRelayRelayAgentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvDhcpRelay.NsxvDhcpRelayRelayAgentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02235e4fa5b26a4c1a9ad5fa566decbba9b08e94ecb5a7e33131bfcfd63a6076)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NsxvDhcpRelayRelayAgentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b0bef8bc1d34a6a3c6c644f02fd692628df053f1bb3a567d7f7a60659667fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxvDhcpRelayRelayAgentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f8deb1c890d79b670a87abb0a53f166438b4f0dec2d1c83195b3936b19b221)
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
            type_hints = typing.get_type_hints(_typecheckingstub__970b70e06fd2ff237f7fcf6fc76d5d8970253883503016c8d20486851b2c1a84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fc3d30933bf9072bc4532e861c7f17ae9484f6c882e400975b1f7c91c27d9b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxvDhcpRelayRelayAgent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxvDhcpRelayRelayAgent]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxvDhcpRelayRelayAgent]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b421186e93069314703118d4505d4625de5d84fef352526f93179866dfb8964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxvDhcpRelayRelayAgentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvDhcpRelay.NsxvDhcpRelayRelayAgentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef0ea13230056210ae5ff6754c2e9a5cd118afe918c7b47107da85cf239ff072)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGatewayIpAddress")
    def reset_gateway_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayIpAddress", []))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpAddressInput")
    def gateway_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkNameInput")
    def network_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpAddress")
    def gateway_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayIpAddress"))

    @gateway_ip_address.setter
    def gateway_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ce5c9764ab6b94f63e3a2cb590417a79c25958b77d289121f56b5a4d32c4da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="networkName")
    def network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkName"))

    @network_name.setter
    def network_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48dadb7a344af5455c9314a01b8bd8441586fa1b8f548754e34d6f08a5f0d9e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxvDhcpRelayRelayAgent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxvDhcpRelayRelayAgent]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxvDhcpRelayRelayAgent]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4019992c9e7523b035c35c96577046544489b9ccd62c477a2249b4a9d42048e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxvDhcpRelay",
    "NsxvDhcpRelayConfig",
    "NsxvDhcpRelayRelayAgent",
    "NsxvDhcpRelayRelayAgentList",
    "NsxvDhcpRelayRelayAgentOutputReference",
]

publication.publish()

def _typecheckingstub__22323c177dfbcf43e9f79236dea8727ad2a48d245ce0e405775245223f5890fc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway: builtins.str,
    relay_agent: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxvDhcpRelayRelayAgent, typing.Dict[builtins.str, typing.Any]]]],
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__5e25a7fda6df373d80e2a88c20d4ba6c68149a742426ee6d2e1222fd096a9190(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24eb70ce3110b5552096c861bb36655081e77aafad779a5053175620669eb991(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxvDhcpRelayRelayAgent, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4636ca6f64b5b3afb4c861892034e20965db73de964d0e28d652303db475ad8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0db861c1549ab0dfecf1854834deb648d1de232c61f65bf1e93c50fc87dacd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc1e9bfc99af2073ab8c839f2d6f38dab61ff952948bed21249234e1eaab3ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77eee9133193dc7b9131892d80be624792fb114119dfb80258634db28117711e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6b8e652bfe39273a6d4ac54352dc0918c3d38f54372044e8de857e040c7bf6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b4fad4349689faa37b662c536fb16823e481fe83fdee93dda9c2378623c87d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54f47c6e818e48f26779bdac6af8f272995eb05d8c724f47be8b1dc46db3914(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5340ba4900a66bc0833c8a608b87cebdb33e0d32ea0da6b803d8854207258cef(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway: builtins.str,
    relay_agent: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxvDhcpRelayRelayAgent, typing.Dict[builtins.str, typing.Any]]]],
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_sets: typing.Optional[typing.Sequence[builtins.str]] = None,
    org: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00e61636a5b8089db7a51520a22f07ca56b287109d847347984e58fa285faab(
    *,
    network_name: builtins.str,
    gateway_ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02235e4fa5b26a4c1a9ad5fa566decbba9b08e94ecb5a7e33131bfcfd63a6076(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b0bef8bc1d34a6a3c6c644f02fd692628df053f1bb3a567d7f7a60659667fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f8deb1c890d79b670a87abb0a53f166438b4f0dec2d1c83195b3936b19b221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970b70e06fd2ff237f7fcf6fc76d5d8970253883503016c8d20486851b2c1a84(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc3d30933bf9072bc4532e861c7f17ae9484f6c882e400975b1f7c91c27d9b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b421186e93069314703118d4505d4625de5d84fef352526f93179866dfb8964(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxvDhcpRelayRelayAgent]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0ea13230056210ae5ff6754c2e9a5cd118afe918c7b47107da85cf239ff072(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ce5c9764ab6b94f63e3a2cb590417a79c25958b77d289121f56b5a4d32c4da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48dadb7a344af5455c9314a01b8bd8441586fa1b8f548754e34d6f08a5f0d9e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4019992c9e7523b035c35c96577046544489b9ccd62c477a2249b4a9d42048e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxvDhcpRelayRelayAgent]],
) -> None:
    """Type checking stubs"""
    pass
