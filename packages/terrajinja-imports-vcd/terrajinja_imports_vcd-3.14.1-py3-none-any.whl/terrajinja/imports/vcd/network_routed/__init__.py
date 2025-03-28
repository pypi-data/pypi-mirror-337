'''
# `vcd_network_routed`

Refer to the Terraform Registry for docs: [`vcd_network_routed`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed).
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


class NetworkRouted(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkRouted.NetworkRouted",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed vcd_network_routed}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedDhcpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        gateway: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        interface_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        netmask: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed vcd_network_routed} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway: The name of the edge gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#edge_gateway NetworkRouted#edge_gateway}
        :param name: A unique name for the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#name NetworkRouted#name}
        :param description: Optional description for the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#description NetworkRouted#description}
        :param dhcp_pool: dhcp_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dhcp_pool NetworkRouted#dhcp_pool}
        :param dns1: First DNS server to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns1 NetworkRouted#dns1}
        :param dns2: Second DNS server to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns2 NetworkRouted#dns2}
        :param dns_suffix: A FQDN for the virtual machines on this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns_suffix NetworkRouted#dns_suffix}
        :param gateway: The gateway of this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#gateway NetworkRouted#gateway}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#id NetworkRouted#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interface_type: Which interface to use (one of ``internal``, ``subinterface``, ``distributed``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#interface_type NetworkRouted#interface_type}
        :param metadata: Key value map of metadata to assign to this network. Key and value can be any string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#metadata NetworkRouted#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#metadata_entry NetworkRouted#metadata_entry}
        :param netmask: The netmask for the new network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#netmask NetworkRouted#netmask}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#org NetworkRouted#org}
        :param shared: Defines if this network is shared between multiple VDCs in the Org. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#shared NetworkRouted#shared}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#static_ip_pool NetworkRouted#static_ip_pool}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#vdc NetworkRouted#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a4940deb0d73b12545099d658363e6a3a2c038b8f6c2ef2dc54be8ef157ed9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkRoutedConfig(
            edge_gateway=edge_gateway,
            name=name,
            description=description,
            dhcp_pool=dhcp_pool,
            dns1=dns1,
            dns2=dns2,
            dns_suffix=dns_suffix,
            gateway=gateway,
            id=id,
            interface_type=interface_type,
            metadata=metadata,
            metadata_entry=metadata_entry,
            netmask=netmask,
            org=org,
            shared=shared,
            static_ip_pool=static_ip_pool,
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
        '''Generates CDKTF code for importing a NetworkRouted resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkRouted to import.
        :param import_from_id: The id of the existing NetworkRouted that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkRouted to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe5b94a8e7be4248d5cc31f10388cc385ea56c3e15cb66cd4cc149fd460d1d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDhcpPool")
    def put_dhcp_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedDhcpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30717aeaed3f360a49877e8cddef3c21c14fa1c5537c3b5c78b57d4673053d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDhcpPool", [value]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedMetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300fa00752609127e12590a25ea62d59cf4edc132620ed08cbeb872e361d7590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="putStaticIpPool")
    def put_static_ip_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedStaticIpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd7da6bbe65c4ed9bb043419354787ef816a7f99a2f0c1bc7914b8b4308b48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStaticIpPool", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDhcpPool")
    def reset_dhcp_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcpPool", []))

    @jsii.member(jsii_name="resetDns1")
    def reset_dns1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns1", []))

    @jsii.member(jsii_name="resetDns2")
    def reset_dns2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns2", []))

    @jsii.member(jsii_name="resetDnsSuffix")
    def reset_dns_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsSuffix", []))

    @jsii.member(jsii_name="resetGateway")
    def reset_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGateway", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInterfaceType")
    def reset_interface_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterfaceType", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataEntry")
    def reset_metadata_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataEntry", []))

    @jsii.member(jsii_name="resetNetmask")
    def reset_netmask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetmask", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetShared")
    def reset_shared(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShared", []))

    @jsii.member(jsii_name="resetStaticIpPool")
    def reset_static_ip_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticIpPool", []))

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
    @jsii.member(jsii_name="dhcpPool")
    def dhcp_pool(self) -> "NetworkRoutedDhcpPoolList":
        return typing.cast("NetworkRoutedDhcpPoolList", jsii.get(self, "dhcpPool"))

    @builtins.property
    @jsii.member(jsii_name="href")
    def href(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "href"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "NetworkRoutedMetadataEntryList":
        return typing.cast("NetworkRoutedMetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPool")
    def static_ip_pool(self) -> "NetworkRoutedStaticIpPoolList":
        return typing.cast("NetworkRoutedStaticIpPoolList", jsii.get(self, "staticIpPool"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpPoolInput")
    def dhcp_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedDhcpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedDhcpPool"]]], jsii.get(self, "dhcpPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="dns1Input")
    def dns1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dns1Input"))

    @builtins.property
    @jsii.member(jsii_name="dns2Input")
    def dns2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dns2Input"))

    @builtins.property
    @jsii.member(jsii_name="dnsSuffixInput")
    def dns_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayInput")
    def edge_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceTypeInput")
    def interface_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntryInput")
    def metadata_entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedMetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedMetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="netmaskInput")
    def netmask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netmaskInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedInput")
    def shared_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sharedInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPoolInput")
    def static_ip_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedStaticIpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedStaticIpPool"]]], jsii.get(self, "staticIpPoolInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f6761b402b1f046aa31e06e8224316a1bead9814ef0fe84b42e411e58ee1d90f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="dns1")
    def dns1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns1"))

    @dns1.setter
    def dns1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bca238ddb19da8b30e6d61104d2c4306ecf822a72f8d4f2652e8feba8240238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns1", value)

    @builtins.property
    @jsii.member(jsii_name="dns2")
    def dns2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns2"))

    @dns2.setter
    def dns2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae478ee69050a71eac714f17d0e1a623dd075a8b73cb120a292eb569c34769e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns2", value)

    @builtins.property
    @jsii.member(jsii_name="dnsSuffix")
    def dns_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsSuffix"))

    @dns_suffix.setter
    def dns_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb9d00d1a8b16bfd91b610e812267696baa900beb01a5c6a166060643693b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGateway")
    def edge_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGateway"))

    @edge_gateway.setter
    def edge_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff705645ffb463a0a1db54bb5fb29fd935a0f7cb288da0ebcb235ed3fba7145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGateway", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80e37b62cffad03be361a534ea05fd9aa3c4ecff8ed03d3bf8a485ed8bbc26d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed0fdfa16c7db49e6af80350c7a9b504545256e0f428b6db5a357c1a6c57b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="interfaceType")
    def interface_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceType"))

    @interface_type.setter
    def interface_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e10c0964ab91642dc344df9ed04d7937bdaa5258c3c5b1d654dc657a383628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceType", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397d188cbd89a7783ebab8d670bb7ccb1bf82e18ed192cc8e75928af622ffdb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78371396a5a74e3e6fcae49c0c20258f484e188ffb0f04f1114ba6b6c8a739d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f452c143825bd04b51da9b5d1dcd0333819611b63c869e8c35d06a4f0b53bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb25f246ec9998c159530096be020d30f871a258d074b2ec0e69b59575782b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="shared")
    def shared(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "shared"))

    @shared.setter
    def shared(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e8c5d4c13c0c432b509f21d285711745defb7b60c7a0d96120069e7a86dce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shared", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57badae24ff41fa1d6f00d8db904212b3ce9948cf3bd30a30356a6b4c060daa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.networkRouted.NetworkRoutedConfig",
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
        "name": "name",
        "description": "description",
        "dhcp_pool": "dhcpPool",
        "dns1": "dns1",
        "dns2": "dns2",
        "dns_suffix": "dnsSuffix",
        "gateway": "gateway",
        "id": "id",
        "interface_type": "interfaceType",
        "metadata": "metadata",
        "metadata_entry": "metadataEntry",
        "netmask": "netmask",
        "org": "org",
        "shared": "shared",
        "static_ip_pool": "staticIpPool",
        "vdc": "vdc",
    },
)
class NetworkRoutedConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedDhcpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        gateway: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        interface_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        netmask: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkRoutedStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param edge_gateway: The name of the edge gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#edge_gateway NetworkRouted#edge_gateway}
        :param name: A unique name for the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#name NetworkRouted#name}
        :param description: Optional description for the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#description NetworkRouted#description}
        :param dhcp_pool: dhcp_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dhcp_pool NetworkRouted#dhcp_pool}
        :param dns1: First DNS server to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns1 NetworkRouted#dns1}
        :param dns2: Second DNS server to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns2 NetworkRouted#dns2}
        :param dns_suffix: A FQDN for the virtual machines on this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns_suffix NetworkRouted#dns_suffix}
        :param gateway: The gateway of this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#gateway NetworkRouted#gateway}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#id NetworkRouted#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interface_type: Which interface to use (one of ``internal``, ``subinterface``, ``distributed``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#interface_type NetworkRouted#interface_type}
        :param metadata: Key value map of metadata to assign to this network. Key and value can be any string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#metadata NetworkRouted#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#metadata_entry NetworkRouted#metadata_entry}
        :param netmask: The netmask for the new network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#netmask NetworkRouted#netmask}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#org NetworkRouted#org}
        :param shared: Defines if this network is shared between multiple VDCs in the Org. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#shared NetworkRouted#shared}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#static_ip_pool NetworkRouted#static_ip_pool}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#vdc NetworkRouted#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0831a555a79947655fd9fb2ec7c458818e13a0ea5822ee9f81e5df52e384d797)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway", value=edge_gateway, expected_type=type_hints["edge_gateway"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dhcp_pool", value=dhcp_pool, expected_type=type_hints["dhcp_pool"])
            check_type(argname="argument dns1", value=dns1, expected_type=type_hints["dns1"])
            check_type(argname="argument dns2", value=dns2, expected_type=type_hints["dns2"])
            check_type(argname="argument dns_suffix", value=dns_suffix, expected_type=type_hints["dns_suffix"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument interface_type", value=interface_type, expected_type=type_hints["interface_type"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_entry", value=metadata_entry, expected_type=type_hints["metadata_entry"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument shared", value=shared, expected_type=type_hints["shared"])
            check_type(argname="argument static_ip_pool", value=static_ip_pool, expected_type=type_hints["static_ip_pool"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway": edge_gateway,
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
        if dhcp_pool is not None:
            self._values["dhcp_pool"] = dhcp_pool
        if dns1 is not None:
            self._values["dns1"] = dns1
        if dns2 is not None:
            self._values["dns2"] = dns2
        if dns_suffix is not None:
            self._values["dns_suffix"] = dns_suffix
        if gateway is not None:
            self._values["gateway"] = gateway
        if id is not None:
            self._values["id"] = id
        if interface_type is not None:
            self._values["interface_type"] = interface_type
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_entry is not None:
            self._values["metadata_entry"] = metadata_entry
        if netmask is not None:
            self._values["netmask"] = netmask
        if org is not None:
            self._values["org"] = org
        if shared is not None:
            self._values["shared"] = shared
        if static_ip_pool is not None:
            self._values["static_ip_pool"] = static_ip_pool
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
        '''The name of the edge gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#edge_gateway NetworkRouted#edge_gateway}
        '''
        result = self._values.get("edge_gateway")
        assert result is not None, "Required property 'edge_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A unique name for the network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#name NetworkRouted#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional description for the network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#description NetworkRouted#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dhcp_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedDhcpPool"]]]:
        '''dhcp_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dhcp_pool NetworkRouted#dhcp_pool}
        '''
        result = self._values.get("dhcp_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedDhcpPool"]]], result)

    @builtins.property
    def dns1(self) -> typing.Optional[builtins.str]:
        '''First DNS server to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns1 NetworkRouted#dns1}
        '''
        result = self._values.get("dns1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns2(self) -> typing.Optional[builtins.str]:
        '''Second DNS server to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns2 NetworkRouted#dns2}
        '''
        result = self._values.get("dns2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_suffix(self) -> typing.Optional[builtins.str]:
        '''A FQDN for the virtual machines on this network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#dns_suffix NetworkRouted#dns_suffix}
        '''
        result = self._values.get("dns_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway(self) -> typing.Optional[builtins.str]:
        '''The gateway of this network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#gateway NetworkRouted#gateway}
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#id NetworkRouted#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface_type(self) -> typing.Optional[builtins.str]:
        '''Which interface to use (one of ``internal``, ``subinterface``, ``distributed``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#interface_type NetworkRouted#interface_type}
        '''
        result = self._values.get("interface_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key value map of metadata to assign to this network. Key and value can be any string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#metadata NetworkRouted#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedMetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#metadata_entry NetworkRouted#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedMetadataEntry"]]], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''The netmask for the new network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#netmask NetworkRouted#netmask}
        '''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#org NetworkRouted#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines if this network is shared between multiple VDCs in the Org.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#shared NetworkRouted#shared}
        '''
        result = self._values.get("shared")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def static_ip_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedStaticIpPool"]]]:
        '''static_ip_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#static_ip_pool NetworkRouted#static_ip_pool}
        '''
        result = self._values.get("static_ip_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkRoutedStaticIpPool"]]], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#vdc NetworkRouted#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkRoutedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.networkRouted.NetworkRoutedDhcpPool",
    jsii_struct_bases=[],
    name_mapping={
        "end_address": "endAddress",
        "start_address": "startAddress",
        "max_lease_time": "maxLeaseTime",
    },
)
class NetworkRoutedDhcpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
        max_lease_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_address: The final address in the IP Range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#end_address NetworkRouted#end_address}
        :param start_address: The first address in the IP Range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#start_address NetworkRouted#start_address}
        :param max_lease_time: The maximum DHCP lease time to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#max_lease_time NetworkRouted#max_lease_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb02dd355e73c65c901e24452dbac463218d12b57f6254384000dedf3c4ae31)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
            check_type(argname="argument max_lease_time", value=max_lease_time, expected_type=type_hints["max_lease_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }
        if max_lease_time is not None:
            self._values["max_lease_time"] = max_lease_time

    @builtins.property
    def end_address(self) -> builtins.str:
        '''The final address in the IP Range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#end_address NetworkRouted#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''The first address in the IP Range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#start_address NetworkRouted#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_lease_time(self) -> typing.Optional[jsii.Number]:
        '''The maximum DHCP lease time to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#max_lease_time NetworkRouted#max_lease_time}
        '''
        result = self._values.get("max_lease_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkRoutedDhcpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkRoutedDhcpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkRouted.NetworkRoutedDhcpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b833eed82322212293dcf645bde291ce2fa4432a00dc8a89013660b8519970a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkRoutedDhcpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d50aba8a1735348f9e9d485f20f1f9bcf9486306152e12491f88775770410d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkRoutedDhcpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25428b90159af28c3554e3286bce446c9b7e0794912464ecbc9fa2f3e755580)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07caa8bee631fe2f0a196e9cbb26262a2c8a76f66076bebf9205063ae54737d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5095a83898afa38cd7fe919438cf037120333c1e58090f76938d6dcbb9fd10f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedDhcpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedDhcpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedDhcpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699f212e839c7ddc426d5c39186f7bb620d7b88aefb1f2feb1b1d3ab77363ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkRoutedDhcpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkRouted.NetworkRoutedDhcpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__678cacc1a896f5a1ac7074df0398a3973a806c7068aabc96a4e8241405b54e5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaxLeaseTime")
    def reset_max_lease_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLeaseTime", []))

    @builtins.property
    @jsii.member(jsii_name="defaultLeaseTime")
    def default_lease_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultLeaseTime"))

    @builtins.property
    @jsii.member(jsii_name="endAddressInput")
    def end_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTimeInput")
    def max_lease_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLeaseTimeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__952832e368ab77f4e05a6d3bb880446ce3fa1e18dfebb2701fa425181f5b582b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTime")
    def max_lease_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLeaseTime"))

    @max_lease_time.setter
    def max_lease_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7650972d719b6345f6ac6a233a2674770298e6ff58a5fbbafa7c96028f91c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLeaseTime", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff58c224123aa0b9bed51f8cb662b4d521582a837ad83553058908186654ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedDhcpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedDhcpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedDhcpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c38f3a963c0ede2ab856eae36399fc515aa4b7ea7edbc2a86b96ea3b8ba18fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkRouted.NetworkRoutedMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "is_system": "isSystem",
        "key": "key",
        "type": "type",
        "user_access": "userAccess",
        "value": "value",
    },
)
class NetworkRoutedMetadataEntry:
    def __init__(
        self,
        *,
        is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user_access: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#is_system NetworkRouted#is_system}
        :param key: Key of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#key NetworkRouted#key}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#type NetworkRouted#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#user_access NetworkRouted#user_access}
        :param value: Value of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#value NetworkRouted#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dcea0e34391882fd2a769e8f3f924eef127ff52931ceee721b3b1518d070926)
            check_type(argname="argument is_system", value=is_system, expected_type=type_hints["is_system"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_access", value=user_access, expected_type=type_hints["user_access"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_system is not None:
            self._values["is_system"] = is_system
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if user_access is not None:
            self._values["user_access"] = user_access
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_system(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#is_system NetworkRouted#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#key NetworkRouted#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#type NetworkRouted#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#user_access NetworkRouted#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#value NetworkRouted#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkRoutedMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkRoutedMetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkRouted.NetworkRoutedMetadataEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dac86579fc064052c7f60a5e284472b520f8b66553d30abf6f1bd6153311ac3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkRoutedMetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4609e49266c9985fb21e52302780661b2a1ae381c45b58cef2e8d92f08250838)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkRoutedMetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535610adeb7ba9788159d7fe8e2c6ca268dc0f9f1e8ed82bd39fa19375372a01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__356074e1daa1e7113209c9cfb02da5bea188c3c8d364300252865076b935dc0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f817bdb7bf37a34a9f06d9186c6855ce644ad303e2baefeb42965f45f100ae58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedMetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedMetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedMetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a72ac3ad0177a76a1b00ae7ff2d4db7d2ed6d3a81ce81398bae2ec143d3904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkRoutedMetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkRouted.NetworkRoutedMetadataEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0c5bca6f2d10e918264e16aa696eac982e2c6d9323a62f279d0f19a9b2816a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsSystem")
    def reset_is_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSystem", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserAccess")
    def reset_user_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAccess", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="isSystemInput")
    def is_system_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userAccessInput")
    def user_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isSystem")
    def is_system(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSystem"))

    @is_system.setter
    def is_system(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bace0a6d043e523040d84eb8d1756c50c03dcaa53dc3ddff8f9a148c1dfb2af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f15ae56584d518447252194470998bcb3689a45bedc774e72d6f96096df607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831e1ccd2cb73a0666b87de9432b334d8bb2ce332a47426c456631624a481ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6bd6fa25c3044b47fe9a0e3d116c75080e7c0486cb9e7dfd0daa29e9bfaa9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2b0d52f95321c3e1fb09da5022f011702b08b5db6e22c6d9b5235b1c000cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedMetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedMetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedMetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb9c3aad05eb2ec0e52785460e80ea7d181ce2c1dbe1e7825b6708f1ebec8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkRouted.NetworkRoutedStaticIpPool",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class NetworkRoutedStaticIpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: The final address in the IP Range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#end_address NetworkRouted#end_address}
        :param start_address: The first address in the IP Range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#start_address NetworkRouted#start_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69d29e13a905eca1f2a571dd8f2e557851162b8c859f70244a26d6111d99c12)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''The final address in the IP Range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#end_address NetworkRouted#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''The first address in the IP Range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_routed#start_address NetworkRouted#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkRoutedStaticIpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkRoutedStaticIpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkRouted.NetworkRoutedStaticIpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0b8f0f94acbe612c8e2c5f0084c2f62d88b6d10c03900c9effbf81c11f2067d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkRoutedStaticIpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee03d66157cfb147997103f076193aa1f51a3c559256012e74fa3692826c3287)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkRoutedStaticIpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85fae18a6105e1f12af9a0f47e56bb83f2ad9e158b798ed55624d83dc490318)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b058cc88ede9c69ddeaadff0d6d80edc912c670fd6ae74b1f7e9ecd1bbf2505)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbbb97ad9ae58e3bb87455a8d01321563b0960d21a248355e8621e77314e18f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedStaticIpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedStaticIpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedStaticIpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ad4d23a7abac0e693018846d2825cd81b385a849dded915bfcb62802ba335c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkRoutedStaticIpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkRouted.NetworkRoutedStaticIpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ce08fb02ba068b197be89bd7ed59f7db2c7b8a2da42781f0b0588344cf2377d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce8e1ca44a772067b440a0a1d9360af8459dd230848f74292c67f75bbeea0817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4293f8e23b552ec3a71c44dfff39e57fe2baa9f5e145caf13826785657ec44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedStaticIpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedStaticIpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedStaticIpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a40c483eb7803eda985014c2dd525f8e7dbf7ca58e157ee2cf6a917d06ca45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NetworkRouted",
    "NetworkRoutedConfig",
    "NetworkRoutedDhcpPool",
    "NetworkRoutedDhcpPoolList",
    "NetworkRoutedDhcpPoolOutputReference",
    "NetworkRoutedMetadataEntry",
    "NetworkRoutedMetadataEntryList",
    "NetworkRoutedMetadataEntryOutputReference",
    "NetworkRoutedStaticIpPool",
    "NetworkRoutedStaticIpPoolList",
    "NetworkRoutedStaticIpPoolOutputReference",
]

publication.publish()

def _typecheckingstub__f8a4940deb0d73b12545099d658363e6a3a2c038b8f6c2ef2dc54be8ef157ed9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedDhcpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    gateway: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    interface_type: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    netmask: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__fbe5b94a8e7be4248d5cc31f10388cc385ea56c3e15cb66cd4cc149fd460d1d9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30717aeaed3f360a49877e8cddef3c21c14fa1c5537c3b5c78b57d4673053d53(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedDhcpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300fa00752609127e12590a25ea62d59cf4edc132620ed08cbeb872e361d7590(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedMetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd7da6bbe65c4ed9bb043419354787ef816a7f99a2f0c1bc7914b8b4308b48f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedStaticIpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6761b402b1f046aa31e06e8224316a1bead9814ef0fe84b42e411e58ee1d90f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bca238ddb19da8b30e6d61104d2c4306ecf822a72f8d4f2652e8feba8240238(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae478ee69050a71eac714f17d0e1a623dd075a8b73cb120a292eb569c34769e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb9d00d1a8b16bfd91b610e812267696baa900beb01a5c6a166060643693b5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff705645ffb463a0a1db54bb5fb29fd935a0f7cb288da0ebcb235ed3fba7145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80e37b62cffad03be361a534ea05fd9aa3c4ecff8ed03d3bf8a485ed8bbc26d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed0fdfa16c7db49e6af80350c7a9b504545256e0f428b6db5a357c1a6c57b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e10c0964ab91642dc344df9ed04d7937bdaa5258c3c5b1d654dc657a383628(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397d188cbd89a7783ebab8d670bb7ccb1bf82e18ed192cc8e75928af622ffdb7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78371396a5a74e3e6fcae49c0c20258f484e188ffb0f04f1114ba6b6c8a739d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f452c143825bd04b51da9b5d1dcd0333819611b63c869e8c35d06a4f0b53bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb25f246ec9998c159530096be020d30f871a258d074b2ec0e69b59575782b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e8c5d4c13c0c432b509f21d285711745defb7b60c7a0d96120069e7a86dce3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57badae24ff41fa1d6f00d8db904212b3ce9948cf3bd30a30356a6b4c060daa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0831a555a79947655fd9fb2ec7c458818e13a0ea5822ee9f81e5df52e384d797(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedDhcpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    gateway: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    interface_type: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    netmask: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkRoutedStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb02dd355e73c65c901e24452dbac463218d12b57f6254384000dedf3c4ae31(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
    max_lease_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b833eed82322212293dcf645bde291ce2fa4432a00dc8a89013660b8519970a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d50aba8a1735348f9e9d485f20f1f9bcf9486306152e12491f88775770410d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25428b90159af28c3554e3286bce446c9b7e0794912464ecbc9fa2f3e755580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07caa8bee631fe2f0a196e9cbb26262a2c8a76f66076bebf9205063ae54737d6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5095a83898afa38cd7fe919438cf037120333c1e58090f76938d6dcbb9fd10f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699f212e839c7ddc426d5c39186f7bb620d7b88aefb1f2feb1b1d3ab77363ece(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedDhcpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678cacc1a896f5a1ac7074df0398a3973a806c7068aabc96a4e8241405b54e5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952832e368ab77f4e05a6d3bb880446ce3fa1e18dfebb2701fa425181f5b582b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7650972d719b6345f6ac6a233a2674770298e6ff58a5fbbafa7c96028f91c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff58c224123aa0b9bed51f8cb662b4d521582a837ad83553058908186654ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c38f3a963c0ede2ab856eae36399fc515aa4b7ea7edbc2a86b96ea3b8ba18fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedDhcpPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcea0e34391882fd2a769e8f3f924eef127ff52931ceee721b3b1518d070926(
    *,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dac86579fc064052c7f60a5e284472b520f8b66553d30abf6f1bd6153311ac3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4609e49266c9985fb21e52302780661b2a1ae381c45b58cef2e8d92f08250838(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535610adeb7ba9788159d7fe8e2c6ca268dc0f9f1e8ed82bd39fa19375372a01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356074e1daa1e7113209c9cfb02da5bea188c3c8d364300252865076b935dc0b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f817bdb7bf37a34a9f06d9186c6855ce644ad303e2baefeb42965f45f100ae58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a72ac3ad0177a76a1b00ae7ff2d4db7d2ed6d3a81ce81398bae2ec143d3904(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedMetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c5bca6f2d10e918264e16aa696eac982e2c6d9323a62f279d0f19a9b2816a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bace0a6d043e523040d84eb8d1756c50c03dcaa53dc3ddff8f9a148c1dfb2af0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f15ae56584d518447252194470998bcb3689a45bedc774e72d6f96096df607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831e1ccd2cb73a0666b87de9432b334d8bb2ce332a47426c456631624a481ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bd6fa25c3044b47fe9a0e3d116c75080e7c0486cb9e7dfd0daa29e9bfaa9df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2b0d52f95321c3e1fb09da5022f011702b08b5db6e22c6d9b5235b1c000cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb9c3aad05eb2ec0e52785460e80ea7d181ce2c1dbe1e7825b6708f1ebec8f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedMetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69d29e13a905eca1f2a571dd8f2e557851162b8c859f70244a26d6111d99c12(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b8f0f94acbe612c8e2c5f0084c2f62d88b6d10c03900c9effbf81c11f2067d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee03d66157cfb147997103f076193aa1f51a3c559256012e74fa3692826c3287(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85fae18a6105e1f12af9a0f47e56bb83f2ad9e158b798ed55624d83dc490318(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b058cc88ede9c69ddeaadff0d6d80edc912c670fd6ae74b1f7e9ecd1bbf2505(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbb97ad9ae58e3bb87455a8d01321563b0960d21a248355e8621e77314e18f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ad4d23a7abac0e693018846d2825cd81b385a849dded915bfcb62802ba335c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkRoutedStaticIpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce08fb02ba068b197be89bd7ed59f7db2c7b8a2da42781f0b0588344cf2377d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8e1ca44a772067b440a0a1d9360af8459dd230848f74292c67f75bbeea0817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4293f8e23b552ec3a71c44dfff39e57fe2baa9f5e145caf13826785657ec44d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a40c483eb7803eda985014c2dd525f8e7dbf7ca58e157ee2cf6a917d06ca45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkRoutedStaticIpPool]],
) -> None:
    """Type checking stubs"""
    pass
