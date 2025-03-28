'''
# `vcd_nsxt_edgegateway_dns`

Refer to the Terraform Registry for docs: [`vcd_nsxt_edgegateway_dns`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns).
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


class NsxtEdgegatewayDns(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayDns.NsxtEdgegatewayDns",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns vcd_nsxt_edgegateway_dns}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_forwarder_zone: typing.Union["NsxtEdgegatewayDnsDefaultForwarderZone", typing.Dict[builtins.str, typing.Any]],
        edge_gateway_id: builtins.str,
        conditional_forwarder_zone: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayDnsConditionalForwarderZone", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        listener_ip: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        snat_rule_ip_address: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns vcd_nsxt_edgegateway_dns} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_forwarder_zone: default_forwarder_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#default_forwarder_zone NsxtEdgegatewayDns#default_forwarder_zone}
        :param edge_gateway_id: Edge gateway ID for DNS configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#edge_gateway_id NsxtEdgegatewayDns#edge_gateway_id}
        :param conditional_forwarder_zone: conditional_forwarder_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#conditional_forwarder_zone NsxtEdgegatewayDns#conditional_forwarder_zone}
        :param enabled: Status of the DNS Forwarder. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#enabled NsxtEdgegatewayDns#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#id NsxtEdgegatewayDns#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param listener_ip: IP on which the DNS forwarder listens.Can be modified only if the Edge Gateway has a dedicated external network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#listener_ip NsxtEdgegatewayDns#listener_ip}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#org NsxtEdgegatewayDns#org}
        :param snat_rule_ip_address: The external IP address of the SNAT rule. Can be modified only if the Edge Gateway's external network is using IP spaces. (VCD 10.5.0+) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#snat_rule_ip_address NsxtEdgegatewayDns#snat_rule_ip_address}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfca2c5656f60cbb6d1d6072e74ed1ba3134b9baa56b659045dc8e8fdf6e9c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtEdgegatewayDnsConfig(
            default_forwarder_zone=default_forwarder_zone,
            edge_gateway_id=edge_gateway_id,
            conditional_forwarder_zone=conditional_forwarder_zone,
            enabled=enabled,
            id=id,
            listener_ip=listener_ip,
            org=org,
            snat_rule_ip_address=snat_rule_ip_address,
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
        '''Generates CDKTF code for importing a NsxtEdgegatewayDns resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtEdgegatewayDns to import.
        :param import_from_id: The id of the existing NsxtEdgegatewayDns that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtEdgegatewayDns to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f282c7ac068f7460e5f6c774957b7cb11b33707f0e5de133791956261bfa3c53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConditionalForwarderZone")
    def put_conditional_forwarder_zone(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayDnsConditionalForwarderZone", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7243d5c3a815927450ae4cfd1c79300696e0d88b1bff6fcd39f156c09242f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditionalForwarderZone", [value]))

    @jsii.member(jsii_name="putDefaultForwarderZone")
    def put_default_forwarder_zone(
        self,
        *,
        name: builtins.str,
        upstream_servers: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Name of the forwarder zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#name NsxtEdgegatewayDns#name}
        :param upstream_servers: Servers to which DNS requests should be forwarded to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#upstream_servers NsxtEdgegatewayDns#upstream_servers}
        '''
        value = NsxtEdgegatewayDnsDefaultForwarderZone(
            name=name, upstream_servers=upstream_servers
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultForwarderZone", [value]))

    @jsii.member(jsii_name="resetConditionalForwarderZone")
    def reset_conditional_forwarder_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionalForwarderZone", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetListenerIp")
    def reset_listener_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetListenerIp", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetSnatRuleIpAddress")
    def reset_snat_rule_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnatRuleIpAddress", []))

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
    @jsii.member(jsii_name="conditionalForwarderZone")
    def conditional_forwarder_zone(
        self,
    ) -> "NsxtEdgegatewayDnsConditionalForwarderZoneList":
        return typing.cast("NsxtEdgegatewayDnsConditionalForwarderZoneList", jsii.get(self, "conditionalForwarderZone"))

    @builtins.property
    @jsii.member(jsii_name="defaultForwarderZone")
    def default_forwarder_zone(
        self,
    ) -> "NsxtEdgegatewayDnsDefaultForwarderZoneOutputReference":
        return typing.cast("NsxtEdgegatewayDnsDefaultForwarderZoneOutputReference", jsii.get(self, "defaultForwarderZone"))

    @builtins.property
    @jsii.member(jsii_name="snatRuleEnabled")
    def snat_rule_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "snatRuleEnabled"))

    @builtins.property
    @jsii.member(jsii_name="conditionalForwarderZoneInput")
    def conditional_forwarder_zone_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayDnsConditionalForwarderZone"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayDnsConditionalForwarderZone"]]], jsii.get(self, "conditionalForwarderZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultForwarderZoneInput")
    def default_forwarder_zone_input(
        self,
    ) -> typing.Optional["NsxtEdgegatewayDnsDefaultForwarderZone"]:
        return typing.cast(typing.Optional["NsxtEdgegatewayDnsDefaultForwarderZone"], jsii.get(self, "defaultForwarderZoneInput"))

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
    @jsii.member(jsii_name="listenerIpInput")
    def listener_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listenerIpInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="snatRuleIpAddressInput")
    def snat_rule_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snatRuleIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayId")
    def edge_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGatewayId"))

    @edge_gateway_id.setter
    def edge_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0994c532f8961190ec6723926d9cd1a1df3e520610b8f747e92d284da0d2e545)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b529158f7eb6c3c2c6200fbe2822d48310493ef64a03fb1bcd6ee2a57751d2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33edcfeac1e08eece6bd080b65a83244dceb0c7e0c06d7f6723b4445005d3bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="listenerIp")
    def listener_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listenerIp"))

    @listener_ip.setter
    def listener_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2d53a711d4b62c8bf8d7d7dca058ce570de016226d284e0bb2acf93ed59016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerIp", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2e5e5403d2819c6d427579452aa46809439622d4fb23c636745d2a3ff99b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="snatRuleIpAddress")
    def snat_rule_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snatRuleIpAddress"))

    @snat_rule_ip_address.setter
    def snat_rule_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdf606337998d1d4335f3285002566a442be3f73dc86cf98d5e278b9470b290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snatRuleIpAddress", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegatewayDns.NsxtEdgegatewayDnsConditionalForwarderZone",
    jsii_struct_bases=[],
    name_mapping={
        "domain_names": "domainNames",
        "name": "name",
        "upstream_servers": "upstreamServers",
    },
)
class NsxtEdgegatewayDnsConditionalForwarderZone:
    def __init__(
        self,
        *,
        domain_names: typing.Sequence[builtins.str],
        name: builtins.str,
        upstream_servers: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param domain_names: Set of domain names on which conditional forwarding is based. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#domain_names NsxtEdgegatewayDns#domain_names}
        :param name: Name of the forwarder zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#name NsxtEdgegatewayDns#name}
        :param upstream_servers: Servers to which DNS requests should be forwarded to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#upstream_servers NsxtEdgegatewayDns#upstream_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7279997183562440665b88132bdf73d6fb2e8446f7f2ea80275193bca5e727)
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument upstream_servers", value=upstream_servers, expected_type=type_hints["upstream_servers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_names": domain_names,
            "name": name,
            "upstream_servers": upstream_servers,
        }

    @builtins.property
    def domain_names(self) -> typing.List[builtins.str]:
        '''Set of domain names on which conditional forwarding is based.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#domain_names NsxtEdgegatewayDns#domain_names}
        '''
        result = self._values.get("domain_names")
        assert result is not None, "Required property 'domain_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the forwarder zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#name NsxtEdgegatewayDns#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def upstream_servers(self) -> typing.List[builtins.str]:
        '''Servers to which DNS requests should be forwarded to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#upstream_servers NsxtEdgegatewayDns#upstream_servers}
        '''
        result = self._values.get("upstream_servers")
        assert result is not None, "Required property 'upstream_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayDnsConditionalForwarderZone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtEdgegatewayDnsConditionalForwarderZoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayDns.NsxtEdgegatewayDnsConditionalForwarderZoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6210d7dafc0af50dc16fb479652fb306545b2302d8bbbf8cb4373b465e5a3e83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtEdgegatewayDnsConditionalForwarderZoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7794cc2d3f67557684c4c033049455d83e0321d6538209b4802d57b1e83d9d5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtEdgegatewayDnsConditionalForwarderZoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d381322ec71d28a6eedc687aeb06b1ea0f5d40735291d2d587b58b8d2ddf42b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c926420b76a13e0cb31cc70a12a2dd1a8251bb513b64d632ba2a52d2625e295)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f93d3b4b6e81a3ac97568fa5cb94319160a808c6bca8ee232ac3304418bb0dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayDnsConditionalForwarderZone]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayDnsConditionalForwarderZone]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayDnsConditionalForwarderZone]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648acc178f9e9f8eb1675293e9c42d014d472090a3b84ca60a5026ee23fb0cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewayDnsConditionalForwarderZoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayDns.NsxtEdgegatewayDnsConditionalForwarderZoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99ed2415d82567a0cf9c38c5c695b8d27fa392b3aafcfc946bbb840bb3659965)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="domainNamesInput")
    def domain_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="upstreamServersInput")
    def upstream_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "upstreamServersInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNames")
    def domain_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainNames"))

    @domain_names.setter
    def domain_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f724f3cbface154d0d4f6148703e11d749a4cd08e3ec8c536fb1efdbde1cfc42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNames", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1f0c3718c20af55e8ce5b91d851bdcca1c33f972ffc16911605ba9c19f71ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="upstreamServers")
    def upstream_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "upstreamServers"))

    @upstream_servers.setter
    def upstream_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48641a435bf595ee0b32406ad84e1146c743812be4fc62a0ce01f9f3c6b0853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upstreamServers", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayDnsConditionalForwarderZone]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayDnsConditionalForwarderZone]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayDnsConditionalForwarderZone]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f733fee616347bf1acbb8b42bdd82d68781d06e8997899b05d95cf234ae112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegatewayDns.NsxtEdgegatewayDnsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_forwarder_zone": "defaultForwarderZone",
        "edge_gateway_id": "edgeGatewayId",
        "conditional_forwarder_zone": "conditionalForwarderZone",
        "enabled": "enabled",
        "id": "id",
        "listener_ip": "listenerIp",
        "org": "org",
        "snat_rule_ip_address": "snatRuleIpAddress",
    },
)
class NsxtEdgegatewayDnsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_forwarder_zone: typing.Union["NsxtEdgegatewayDnsDefaultForwarderZone", typing.Dict[builtins.str, typing.Any]],
        edge_gateway_id: builtins.str,
        conditional_forwarder_zone: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayDnsConditionalForwarderZone, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        listener_ip: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        snat_rule_ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_forwarder_zone: default_forwarder_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#default_forwarder_zone NsxtEdgegatewayDns#default_forwarder_zone}
        :param edge_gateway_id: Edge gateway ID for DNS configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#edge_gateway_id NsxtEdgegatewayDns#edge_gateway_id}
        :param conditional_forwarder_zone: conditional_forwarder_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#conditional_forwarder_zone NsxtEdgegatewayDns#conditional_forwarder_zone}
        :param enabled: Status of the DNS Forwarder. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#enabled NsxtEdgegatewayDns#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#id NsxtEdgegatewayDns#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param listener_ip: IP on which the DNS forwarder listens.Can be modified only if the Edge Gateway has a dedicated external network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#listener_ip NsxtEdgegatewayDns#listener_ip}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#org NsxtEdgegatewayDns#org}
        :param snat_rule_ip_address: The external IP address of the SNAT rule. Can be modified only if the Edge Gateway's external network is using IP spaces. (VCD 10.5.0+) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#snat_rule_ip_address NsxtEdgegatewayDns#snat_rule_ip_address}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_forwarder_zone, dict):
            default_forwarder_zone = NsxtEdgegatewayDnsDefaultForwarderZone(**default_forwarder_zone)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d757986cb7caa2acaa9369a7410176a47b764ba1952d9fc0b07de73fad2129)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_forwarder_zone", value=default_forwarder_zone, expected_type=type_hints["default_forwarder_zone"])
            check_type(argname="argument edge_gateway_id", value=edge_gateway_id, expected_type=type_hints["edge_gateway_id"])
            check_type(argname="argument conditional_forwarder_zone", value=conditional_forwarder_zone, expected_type=type_hints["conditional_forwarder_zone"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument listener_ip", value=listener_ip, expected_type=type_hints["listener_ip"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument snat_rule_ip_address", value=snat_rule_ip_address, expected_type=type_hints["snat_rule_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_forwarder_zone": default_forwarder_zone,
            "edge_gateway_id": edge_gateway_id,
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
        if conditional_forwarder_zone is not None:
            self._values["conditional_forwarder_zone"] = conditional_forwarder_zone
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if listener_ip is not None:
            self._values["listener_ip"] = listener_ip
        if org is not None:
            self._values["org"] = org
        if snat_rule_ip_address is not None:
            self._values["snat_rule_ip_address"] = snat_rule_ip_address

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
    def default_forwarder_zone(self) -> "NsxtEdgegatewayDnsDefaultForwarderZone":
        '''default_forwarder_zone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#default_forwarder_zone NsxtEdgegatewayDns#default_forwarder_zone}
        '''
        result = self._values.get("default_forwarder_zone")
        assert result is not None, "Required property 'default_forwarder_zone' is missing"
        return typing.cast("NsxtEdgegatewayDnsDefaultForwarderZone", result)

    @builtins.property
    def edge_gateway_id(self) -> builtins.str:
        '''Edge gateway ID for DNS configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#edge_gateway_id NsxtEdgegatewayDns#edge_gateway_id}
        '''
        result = self._values.get("edge_gateway_id")
        assert result is not None, "Required property 'edge_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def conditional_forwarder_zone(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayDnsConditionalForwarderZone]]]:
        '''conditional_forwarder_zone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#conditional_forwarder_zone NsxtEdgegatewayDns#conditional_forwarder_zone}
        '''
        result = self._values.get("conditional_forwarder_zone")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayDnsConditionalForwarderZone]]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Status of the DNS Forwarder. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#enabled NsxtEdgegatewayDns#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#id NsxtEdgegatewayDns#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def listener_ip(self) -> typing.Optional[builtins.str]:
        '''IP on which the DNS forwarder listens.Can be modified only if the Edge Gateway has a dedicated external network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#listener_ip NsxtEdgegatewayDns#listener_ip}
        '''
        result = self._values.get("listener_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#org NsxtEdgegatewayDns#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snat_rule_ip_address(self) -> typing.Optional[builtins.str]:
        '''The external IP address of the SNAT rule.

        Can be modified only if the Edge Gateway's external network is using IP spaces. (VCD 10.5.0+)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#snat_rule_ip_address NsxtEdgegatewayDns#snat_rule_ip_address}
        '''
        result = self._values.get("snat_rule_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayDnsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegatewayDns.NsxtEdgegatewayDnsDefaultForwarderZone",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "upstream_servers": "upstreamServers"},
)
class NsxtEdgegatewayDnsDefaultForwarderZone:
    def __init__(
        self,
        *,
        name: builtins.str,
        upstream_servers: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Name of the forwarder zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#name NsxtEdgegatewayDns#name}
        :param upstream_servers: Servers to which DNS requests should be forwarded to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#upstream_servers NsxtEdgegatewayDns#upstream_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8919a2fb9e9da03d0d23d1d1c2ceacbabf88bcd453c8045d471c347e1ec279)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument upstream_servers", value=upstream_servers, expected_type=type_hints["upstream_servers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "upstream_servers": upstream_servers,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the forwarder zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#name NsxtEdgegatewayDns#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def upstream_servers(self) -> typing.List[builtins.str]:
        '''Servers to which DNS requests should be forwarded to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_dns#upstream_servers NsxtEdgegatewayDns#upstream_servers}
        '''
        result = self._values.get("upstream_servers")
        assert result is not None, "Required property 'upstream_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayDnsDefaultForwarderZone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtEdgegatewayDnsDefaultForwarderZoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayDns.NsxtEdgegatewayDnsDefaultForwarderZoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fe5ca636c883cf6c89358e64338db9e53d09f502ef77be624b951c7ab1d5cc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="upstreamServersInput")
    def upstream_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "upstreamServersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274cb4a2d6a23542a3ef10b8bd0efd090e33f146cfa1718de98614d339def2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="upstreamServers")
    def upstream_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "upstreamServers"))

    @upstream_servers.setter
    def upstream_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc84f02d3a24146c967ff72dcc2b4936ac74537dff0f45aeb8ac66278b1141b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upstreamServers", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NsxtEdgegatewayDnsDefaultForwarderZone]:
        return typing.cast(typing.Optional[NsxtEdgegatewayDnsDefaultForwarderZone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtEdgegatewayDnsDefaultForwarderZone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19272db2763ffa33be106e1375c17ddba7103398a2e91b936cd54bb054546e08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtEdgegatewayDns",
    "NsxtEdgegatewayDnsConditionalForwarderZone",
    "NsxtEdgegatewayDnsConditionalForwarderZoneList",
    "NsxtEdgegatewayDnsConditionalForwarderZoneOutputReference",
    "NsxtEdgegatewayDnsConfig",
    "NsxtEdgegatewayDnsDefaultForwarderZone",
    "NsxtEdgegatewayDnsDefaultForwarderZoneOutputReference",
]

publication.publish()

def _typecheckingstub__2dfca2c5656f60cbb6d1d6072e74ed1ba3134b9baa56b659045dc8e8fdf6e9c7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_forwarder_zone: typing.Union[NsxtEdgegatewayDnsDefaultForwarderZone, typing.Dict[builtins.str, typing.Any]],
    edge_gateway_id: builtins.str,
    conditional_forwarder_zone: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayDnsConditionalForwarderZone, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    listener_ip: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    snat_rule_ip_address: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__f282c7ac068f7460e5f6c774957b7cb11b33707f0e5de133791956261bfa3c53(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7243d5c3a815927450ae4cfd1c79300696e0d88b1bff6fcd39f156c09242f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayDnsConditionalForwarderZone, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0994c532f8961190ec6723926d9cd1a1df3e520610b8f747e92d284da0d2e545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b529158f7eb6c3c2c6200fbe2822d48310493ef64a03fb1bcd6ee2a57751d2ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33edcfeac1e08eece6bd080b65a83244dceb0c7e0c06d7f6723b4445005d3bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2d53a711d4b62c8bf8d7d7dca058ce570de016226d284e0bb2acf93ed59016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2e5e5403d2819c6d427579452aa46809439622d4fb23c636745d2a3ff99b3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdf606337998d1d4335f3285002566a442be3f73dc86cf98d5e278b9470b290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7279997183562440665b88132bdf73d6fb2e8446f7f2ea80275193bca5e727(
    *,
    domain_names: typing.Sequence[builtins.str],
    name: builtins.str,
    upstream_servers: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6210d7dafc0af50dc16fb479652fb306545b2302d8bbbf8cb4373b465e5a3e83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7794cc2d3f67557684c4c033049455d83e0321d6538209b4802d57b1e83d9d5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d381322ec71d28a6eedc687aeb06b1ea0f5d40735291d2d587b58b8d2ddf42b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c926420b76a13e0cb31cc70a12a2dd1a8251bb513b64d632ba2a52d2625e295(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93d3b4b6e81a3ac97568fa5cb94319160a808c6bca8ee232ac3304418bb0dc7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648acc178f9e9f8eb1675293e9c42d014d472090a3b84ca60a5026ee23fb0cf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayDnsConditionalForwarderZone]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ed2415d82567a0cf9c38c5c695b8d27fa392b3aafcfc946bbb840bb3659965(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f724f3cbface154d0d4f6148703e11d749a4cd08e3ec8c536fb1efdbde1cfc42(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1f0c3718c20af55e8ce5b91d851bdcca1c33f972ffc16911605ba9c19f71ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48641a435bf595ee0b32406ad84e1146c743812be4fc62a0ce01f9f3c6b0853(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f733fee616347bf1acbb8b42bdd82d68781d06e8997899b05d95cf234ae112(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayDnsConditionalForwarderZone]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d757986cb7caa2acaa9369a7410176a47b764ba1952d9fc0b07de73fad2129(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_forwarder_zone: typing.Union[NsxtEdgegatewayDnsDefaultForwarderZone, typing.Dict[builtins.str, typing.Any]],
    edge_gateway_id: builtins.str,
    conditional_forwarder_zone: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayDnsConditionalForwarderZone, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    listener_ip: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    snat_rule_ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8919a2fb9e9da03d0d23d1d1c2ceacbabf88bcd453c8045d471c347e1ec279(
    *,
    name: builtins.str,
    upstream_servers: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe5ca636c883cf6c89358e64338db9e53d09f502ef77be624b951c7ab1d5cc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274cb4a2d6a23542a3ef10b8bd0efd090e33f146cfa1718de98614d339def2e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc84f02d3a24146c967ff72dcc2b4936ac74537dff0f45aeb8ac66278b1141b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19272db2763ffa33be106e1375c17ddba7103398a2e91b936cd54bb054546e08(
    value: typing.Optional[NsxtEdgegatewayDnsDefaultForwarderZone],
) -> None:
    """Type checking stubs"""
    pass
