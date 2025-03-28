'''
# `vcd_nsxt_edgegateway_bgp_ip_prefix_list`

Refer to the Terraform Registry for docs: [`vcd_nsxt_edgegateway_bgp_ip_prefix_list`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list).
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


class NsxtEdgegatewayBgpIpPrefixList(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayBgpIpPrefixList.NsxtEdgegatewayBgpIpPrefixList",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list vcd_nsxt_edgegateway_bgp_ip_prefix_list}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway_id: builtins.str,
        ip_prefix: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayBgpIpPrefixListIpPrefix", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list vcd_nsxt_edgegateway_bgp_ip_prefix_list} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway_id: Edge gateway ID for BGP IP Prefix List Configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#edge_gateway_id NsxtEdgegatewayBgpIpPrefixList#edge_gateway_id}
        :param ip_prefix: ip_prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#ip_prefix NsxtEdgegatewayBgpIpPrefixList#ip_prefix}
        :param name: BGP IP Prefix List name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#name NsxtEdgegatewayBgpIpPrefixList#name}
        :param description: BGP IP Prefix List description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#description NsxtEdgegatewayBgpIpPrefixList#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#id NsxtEdgegatewayBgpIpPrefixList#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#org NsxtEdgegatewayBgpIpPrefixList#org}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544e777acf293ab0e8ea9c7d2a3bdca6dbac34a62876d3c65675ce2596e411b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtEdgegatewayBgpIpPrefixListConfig(
            edge_gateway_id=edge_gateway_id,
            ip_prefix=ip_prefix,
            name=name,
            description=description,
            id=id,
            org=org,
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
        '''Generates CDKTF code for importing a NsxtEdgegatewayBgpIpPrefixList resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtEdgegatewayBgpIpPrefixList to import.
        :param import_from_id: The id of the existing NsxtEdgegatewayBgpIpPrefixList that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtEdgegatewayBgpIpPrefixList to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa07f85076217288f89fbd476b53a80b9bdcb1041a763aad6f731f350f883159)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIpPrefix")
    def put_ip_prefix(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayBgpIpPrefixListIpPrefix", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7253e5d3e4460feda5179acc7fcd0f4a1ab6efd1b3c009aa417b6bcfa6d037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpPrefix", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

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
    @jsii.member(jsii_name="ipPrefix")
    def ip_prefix(self) -> "NsxtEdgegatewayBgpIpPrefixListIpPrefixList":
        return typing.cast("NsxtEdgegatewayBgpIpPrefixListIpPrefixList", jsii.get(self, "ipPrefix"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayIdInput")
    def edge_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipPrefixInput")
    def ip_prefix_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayBgpIpPrefixListIpPrefix"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayBgpIpPrefixListIpPrefix"]]], jsii.get(self, "ipPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1893830720afcebe47db54b0173b4858f261962c0af41da87be9ad4a8f44187a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayId")
    def edge_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGatewayId"))

    @edge_gateway_id.setter
    def edge_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8804532dd405e4844e68e85bf483d9a1a66267515c24c3e1bd9205ea951357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGatewayId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de8c85a0c3b4df717790ce7e995f76f66a55f1b5947ce55f8ab654e4596b0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39048324a5964e587bfec820a553c039a43f25372b50f63918c27651258787c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd1d05b3decfe5bc6a859a6f8b7aeb3b044dcbe344f8635b8eda17444bd5667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegatewayBgpIpPrefixList.NsxtEdgegatewayBgpIpPrefixListConfig",
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
        "ip_prefix": "ipPrefix",
        "name": "name",
        "description": "description",
        "id": "id",
        "org": "org",
    },
)
class NsxtEdgegatewayBgpIpPrefixListConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ip_prefix: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayBgpIpPrefixListIpPrefix", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param edge_gateway_id: Edge gateway ID for BGP IP Prefix List Configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#edge_gateway_id NsxtEdgegatewayBgpIpPrefixList#edge_gateway_id}
        :param ip_prefix: ip_prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#ip_prefix NsxtEdgegatewayBgpIpPrefixList#ip_prefix}
        :param name: BGP IP Prefix List name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#name NsxtEdgegatewayBgpIpPrefixList#name}
        :param description: BGP IP Prefix List description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#description NsxtEdgegatewayBgpIpPrefixList#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#id NsxtEdgegatewayBgpIpPrefixList#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#org NsxtEdgegatewayBgpIpPrefixList#org}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f6ae982f0573616201b47bb51a3825a720ee4e693b13c9bba7a3d775d82080)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway_id", value=edge_gateway_id, expected_type=type_hints["edge_gateway_id"])
            check_type(argname="argument ip_prefix", value=ip_prefix, expected_type=type_hints["ip_prefix"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway_id": edge_gateway_id,
            "ip_prefix": ip_prefix,
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
        if id is not None:
            self._values["id"] = id
        if org is not None:
            self._values["org"] = org

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
        '''Edge gateway ID for BGP IP Prefix List Configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#edge_gateway_id NsxtEdgegatewayBgpIpPrefixList#edge_gateway_id}
        '''
        result = self._values.get("edge_gateway_id")
        assert result is not None, "Required property 'edge_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_prefix(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayBgpIpPrefixListIpPrefix"]]:
        '''ip_prefix block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#ip_prefix NsxtEdgegatewayBgpIpPrefixList#ip_prefix}
        '''
        result = self._values.get("ip_prefix")
        assert result is not None, "Required property 'ip_prefix' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayBgpIpPrefixListIpPrefix"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''BGP IP Prefix List name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#name NsxtEdgegatewayBgpIpPrefixList#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''BGP IP Prefix List description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#description NsxtEdgegatewayBgpIpPrefixList#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#id NsxtEdgegatewayBgpIpPrefixList#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#org NsxtEdgegatewayBgpIpPrefixList#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayBgpIpPrefixListConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegatewayBgpIpPrefixList.NsxtEdgegatewayBgpIpPrefixListIpPrefix",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "network": "network",
        "greater_than_or_equal_to": "greaterThanOrEqualTo",
        "less_than_or_equal_to": "lessThanOrEqualTo",
    },
)
class NsxtEdgegatewayBgpIpPrefixListIpPrefix:
    def __init__(
        self,
        *,
        action: builtins.str,
        network: builtins.str,
        greater_than_or_equal_to: typing.Optional[jsii.Number] = None,
        less_than_or_equal_to: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action: Action 'PERMIT' or 'DENY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#action NsxtEdgegatewayBgpIpPrefixList#action}
        :param network: Network in CIDR notation (e.g. '192.168.100.0/24', '2001:db8::/48'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#network NsxtEdgegatewayBgpIpPrefixList#network}
        :param greater_than_or_equal_to: Greater than or equal to subnet mask. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#greater_than_or_equal_to NsxtEdgegatewayBgpIpPrefixList#greater_than_or_equal_to}
        :param less_than_or_equal_to: Less than or equal to subnet mask. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#less_than_or_equal_to NsxtEdgegatewayBgpIpPrefixList#less_than_or_equal_to}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bb1c3be504487a40a35876339269a822c554c46e0a37359120b674d0a7c7c8)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument greater_than_or_equal_to", value=greater_than_or_equal_to, expected_type=type_hints["greater_than_or_equal_to"])
            check_type(argname="argument less_than_or_equal_to", value=less_than_or_equal_to, expected_type=type_hints["less_than_or_equal_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "network": network,
        }
        if greater_than_or_equal_to is not None:
            self._values["greater_than_or_equal_to"] = greater_than_or_equal_to
        if less_than_or_equal_to is not None:
            self._values["less_than_or_equal_to"] = less_than_or_equal_to

    @builtins.property
    def action(self) -> builtins.str:
        '''Action 'PERMIT' or 'DENY'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#action NsxtEdgegatewayBgpIpPrefixList#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''Network in CIDR notation (e.g. '192.168.100.0/24', '2001:db8::/48').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#network NsxtEdgegatewayBgpIpPrefixList#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def greater_than_or_equal_to(self) -> typing.Optional[jsii.Number]:
        '''Greater than or equal to subnet mask.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#greater_than_or_equal_to NsxtEdgegatewayBgpIpPrefixList#greater_than_or_equal_to}
        '''
        result = self._values.get("greater_than_or_equal_to")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def less_than_or_equal_to(self) -> typing.Optional[jsii.Number]:
        '''Less than or equal to subnet mask.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway_bgp_ip_prefix_list#less_than_or_equal_to NsxtEdgegatewayBgpIpPrefixList#less_than_or_equal_to}
        '''
        result = self._values.get("less_than_or_equal_to")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayBgpIpPrefixListIpPrefix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtEdgegatewayBgpIpPrefixListIpPrefixList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayBgpIpPrefixList.NsxtEdgegatewayBgpIpPrefixListIpPrefixList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4f599406281ceb974bd1210c62ab1b15175545573bf614c842d14c82e95f1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtEdgegatewayBgpIpPrefixListIpPrefixOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1572071ee6c5a1731166167f3c57acddf59a4824b312966aa11061d9b136b0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtEdgegatewayBgpIpPrefixListIpPrefixOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9140b4019b63a6df99a41605c297449c2dfb64c4f16029075a3433879e8f49b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca536600fd19b78ef7411d6229c64399d7e1e96edf1bc4c692622f89c10a0762)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abc4500551b10ed7580bc9bc94de5bbf90e1f26e10450482220f4d750688a18d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayBgpIpPrefixListIpPrefix]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayBgpIpPrefixListIpPrefix]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayBgpIpPrefixListIpPrefix]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009b0221b573f90f91bd4b093f3cbd06d4ca902d1afdc404899a356214cf9fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewayBgpIpPrefixListIpPrefixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegatewayBgpIpPrefixList.NsxtEdgegatewayBgpIpPrefixListIpPrefixOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f4af165c56bf1b6541d896472eb48894aaa6e646803919946e7e92b716ab245)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGreaterThanOrEqualTo")
    def reset_greater_than_or_equal_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGreaterThanOrEqualTo", []))

    @jsii.member(jsii_name="resetLessThanOrEqualTo")
    def reset_less_than_or_equal_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLessThanOrEqualTo", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="greaterThanOrEqualToInput")
    def greater_than_or_equal_to_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "greaterThanOrEqualToInput"))

    @builtins.property
    @jsii.member(jsii_name="lessThanOrEqualToInput")
    def less_than_or_equal_to_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lessThanOrEqualToInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5c5fe041529968666c0ba22908eb4f37e5060c9d0f42987ff9a295cf15934c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="greaterThanOrEqualTo")
    def greater_than_or_equal_to(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "greaterThanOrEqualTo"))

    @greater_than_or_equal_to.setter
    def greater_than_or_equal_to(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7c760bf2ceee247e81566450684d70f46ce603ca3a1fb61386f62226401d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "greaterThanOrEqualTo", value)

    @builtins.property
    @jsii.member(jsii_name="lessThanOrEqualTo")
    def less_than_or_equal_to(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lessThanOrEqualTo"))

    @less_than_or_equal_to.setter
    def less_than_or_equal_to(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0930767a0369e741cde90b90343fa880888d4de3803c29db01c54cfef58094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lessThanOrEqualTo", value)

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670d00dfb1809cad882e6026c3b6b6834113d09465d7df89cdfa709f5da268e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayBgpIpPrefixListIpPrefix]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayBgpIpPrefixListIpPrefix]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayBgpIpPrefixListIpPrefix]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896ca0dc40338e5773a8b74b8397cfecd00a55e9b4f21ec79f5db076313082f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtEdgegatewayBgpIpPrefixList",
    "NsxtEdgegatewayBgpIpPrefixListConfig",
    "NsxtEdgegatewayBgpIpPrefixListIpPrefix",
    "NsxtEdgegatewayBgpIpPrefixListIpPrefixList",
    "NsxtEdgegatewayBgpIpPrefixListIpPrefixOutputReference",
]

publication.publish()

def _typecheckingstub__544e777acf293ab0e8ea9c7d2a3bdca6dbac34a62876d3c65675ce2596e411b5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway_id: builtins.str,
    ip_prefix: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayBgpIpPrefixListIpPrefix, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__aa07f85076217288f89fbd476b53a80b9bdcb1041a763aad6f731f350f883159(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7253e5d3e4460feda5179acc7fcd0f4a1ab6efd1b3c009aa417b6bcfa6d037(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayBgpIpPrefixListIpPrefix, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1893830720afcebe47db54b0173b4858f261962c0af41da87be9ad4a8f44187a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8804532dd405e4844e68e85bf483d9a1a66267515c24c3e1bd9205ea951357(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de8c85a0c3b4df717790ce7e995f76f66a55f1b5947ce55f8ab654e4596b0ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39048324a5964e587bfec820a553c039a43f25372b50f63918c27651258787c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd1d05b3decfe5bc6a859a6f8b7aeb3b044dcbe344f8635b8eda17444bd5667(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f6ae982f0573616201b47bb51a3825a720ee4e693b13c9bba7a3d775d82080(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway_id: builtins.str,
    ip_prefix: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayBgpIpPrefixListIpPrefix, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bb1c3be504487a40a35876339269a822c554c46e0a37359120b674d0a7c7c8(
    *,
    action: builtins.str,
    network: builtins.str,
    greater_than_or_equal_to: typing.Optional[jsii.Number] = None,
    less_than_or_equal_to: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4f599406281ceb974bd1210c62ab1b15175545573bf614c842d14c82e95f1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1572071ee6c5a1731166167f3c57acddf59a4824b312966aa11061d9b136b0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9140b4019b63a6df99a41605c297449c2dfb64c4f16029075a3433879e8f49b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca536600fd19b78ef7411d6229c64399d7e1e96edf1bc4c692622f89c10a0762(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc4500551b10ed7580bc9bc94de5bbf90e1f26e10450482220f4d750688a18d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009b0221b573f90f91bd4b093f3cbd06d4ca902d1afdc404899a356214cf9fbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayBgpIpPrefixListIpPrefix]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4af165c56bf1b6541d896472eb48894aaa6e646803919946e7e92b716ab245(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5c5fe041529968666c0ba22908eb4f37e5060c9d0f42987ff9a295cf15934c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7c760bf2ceee247e81566450684d70f46ce603ca3a1fb61386f62226401d88(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0930767a0369e741cde90b90343fa880888d4de3803c29db01c54cfef58094(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670d00dfb1809cad882e6026c3b6b6834113d09465d7df89cdfa709f5da268e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896ca0dc40338e5773a8b74b8397cfecd00a55e9b4f21ec79f5db076313082f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayBgpIpPrefixListIpPrefix]],
) -> None:
    """Type checking stubs"""
    pass
