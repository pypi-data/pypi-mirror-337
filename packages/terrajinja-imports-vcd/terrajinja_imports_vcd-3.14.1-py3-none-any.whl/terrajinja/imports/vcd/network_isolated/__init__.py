'''
# `vcd_network_isolated`

Refer to the Terraform Registry for docs: [`vcd_network_isolated`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated).
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


class NetworkIsolated(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolated.NetworkIsolated",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated vcd_network_isolated}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedDhcpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        gateway: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        netmask: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated vcd_network_isolated} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A unique name for this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#name NetworkIsolated#name}
        :param description: Optional description for the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#description NetworkIsolated#description}
        :param dhcp_pool: dhcp_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dhcp_pool NetworkIsolated#dhcp_pool}
        :param dns1: First DNS server to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns1 NetworkIsolated#dns1}
        :param dns2: Second DNS server to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns2 NetworkIsolated#dns2}
        :param dns_suffix: A FQDN for the virtual machines on this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns_suffix NetworkIsolated#dns_suffix}
        :param gateway: The gateway for this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#gateway NetworkIsolated#gateway}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#id NetworkIsolated#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Key value map of metadata to assign to this network. Key and value can be any string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#metadata NetworkIsolated#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#metadata_entry NetworkIsolated#metadata_entry}
        :param netmask: The netmask for the new network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#netmask NetworkIsolated#netmask}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#org NetworkIsolated#org}
        :param shared: Defines if this network is shared between multiple VDCs in the Org. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#shared NetworkIsolated#shared}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#static_ip_pool NetworkIsolated#static_ip_pool}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#vdc NetworkIsolated#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12410298f2772bcf3c801595e5af845c1012f6fe3b98f56eef05db9d0e905b55)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkIsolatedConfig(
            name=name,
            description=description,
            dhcp_pool=dhcp_pool,
            dns1=dns1,
            dns2=dns2,
            dns_suffix=dns_suffix,
            gateway=gateway,
            id=id,
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
        '''Generates CDKTF code for importing a NetworkIsolated resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkIsolated to import.
        :param import_from_id: The id of the existing NetworkIsolated that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkIsolated to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638a09d68726c1238f95920f35c407d9ff371720d8c8b04b4b94a0c7fb29fafc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDhcpPool")
    def put_dhcp_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedDhcpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4d11afb0f6ecddd120b58f914a47a75b16f243cd572e147654baefca4a2853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDhcpPool", [value]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedMetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74cab2a97666a80cce2bb22c4fd96de0ba66b67f56de173fb715720a7d03bdc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="putStaticIpPool")
    def put_static_ip_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedStaticIpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7234b2e7708c220e2c11e9cd15a4371a70227347aa46789678fad5710b17aa)
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
    def dhcp_pool(self) -> "NetworkIsolatedDhcpPoolList":
        return typing.cast("NetworkIsolatedDhcpPoolList", jsii.get(self, "dhcpPool"))

    @builtins.property
    @jsii.member(jsii_name="href")
    def href(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "href"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "NetworkIsolatedMetadataEntryList":
        return typing.cast("NetworkIsolatedMetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPool")
    def static_ip_pool(self) -> "NetworkIsolatedStaticIpPoolList":
        return typing.cast("NetworkIsolatedStaticIpPoolList", jsii.get(self, "staticIpPool"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpPoolInput")
    def dhcp_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedDhcpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedDhcpPool"]]], jsii.get(self, "dhcpPoolInput"))

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
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntryInput")
    def metadata_entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedMetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedMetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedStaticIpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedStaticIpPool"]]], jsii.get(self, "staticIpPoolInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__12ae285fb96ee9e304d98da94a58e25cda4079e43bf5ad5f5898fcc37389a281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="dns1")
    def dns1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns1"))

    @dns1.setter
    def dns1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8ca17cb4e7965ee769f3a956cb07bfa6e493bbcb8cdd7232638bcad836cd721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns1", value)

    @builtins.property
    @jsii.member(jsii_name="dns2")
    def dns2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns2"))

    @dns2.setter
    def dns2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72a225ead152f024ecb98fa94fea9aefce6cf847cb261f02865e1e6826d4c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns2", value)

    @builtins.property
    @jsii.member(jsii_name="dnsSuffix")
    def dns_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsSuffix"))

    @dns_suffix.setter
    def dns_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a726bf1b22048af71ac79c374e0ad2e739a6f47275b0747e1d372d045c16e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966b238fde6744e51719fa02d25ee86da6deb7877aec03642c26c4f4e0635095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d0bd1bfcc0f0abf55c76d85cf2deb86158cf40944b4874576b613c08ced897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad04b86a77916619066f419cec9e4b33de2989c36cd1a3d36e0226f814a04525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e48a245345aaad1554dd6a76603a937253339d681b2b9016183492165ce2e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e60e13f69565e3cd593b8ed2b3c02f1b38d102c28a556faf32af719cd5f1f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d636f46604d0201d535dfbc6fd3105b8018d8388a8938ac6f7722d5b3f21dde1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f53f24ce90df44e863d99d73b28d07921cb32853819fa0c35c298f30b2412c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shared", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b703b99090551ec8e28426db9782f9f1d8cd0028edabd3d759b75894358c6eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.networkIsolated.NetworkIsolatedConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "description": "description",
        "dhcp_pool": "dhcpPool",
        "dns1": "dns1",
        "dns2": "dns2",
        "dns_suffix": "dnsSuffix",
        "gateway": "gateway",
        "id": "id",
        "metadata": "metadata",
        "metadata_entry": "metadataEntry",
        "netmask": "netmask",
        "org": "org",
        "shared": "shared",
        "static_ip_pool": "staticIpPool",
        "vdc": "vdc",
    },
)
class NetworkIsolatedConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedDhcpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        gateway: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        netmask: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param name: A unique name for this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#name NetworkIsolated#name}
        :param description: Optional description for the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#description NetworkIsolated#description}
        :param dhcp_pool: dhcp_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dhcp_pool NetworkIsolated#dhcp_pool}
        :param dns1: First DNS server to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns1 NetworkIsolated#dns1}
        :param dns2: Second DNS server to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns2 NetworkIsolated#dns2}
        :param dns_suffix: A FQDN for the virtual machines on this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns_suffix NetworkIsolated#dns_suffix}
        :param gateway: The gateway for this network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#gateway NetworkIsolated#gateway}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#id NetworkIsolated#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Key value map of metadata to assign to this network. Key and value can be any string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#metadata NetworkIsolated#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#metadata_entry NetworkIsolated#metadata_entry}
        :param netmask: The netmask for the new network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#netmask NetworkIsolated#netmask}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#org NetworkIsolated#org}
        :param shared: Defines if this network is shared between multiple VDCs in the Org. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#shared NetworkIsolated#shared}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#static_ip_pool NetworkIsolated#static_ip_pool}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#vdc NetworkIsolated#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114613f68c1be6b5f3c0a1a5fb297b50cc5b12182305b5476c7537b1fc193317)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dhcp_pool", value=dhcp_pool, expected_type=type_hints["dhcp_pool"])
            check_type(argname="argument dns1", value=dns1, expected_type=type_hints["dns1"])
            check_type(argname="argument dns2", value=dns2, expected_type=type_hints["dns2"])
            check_type(argname="argument dns_suffix", value=dns_suffix, expected_type=type_hints["dns_suffix"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_entry", value=metadata_entry, expected_type=type_hints["metadata_entry"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument shared", value=shared, expected_type=type_hints["shared"])
            check_type(argname="argument static_ip_pool", value=static_ip_pool, expected_type=type_hints["static_ip_pool"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
    def name(self) -> builtins.str:
        '''A unique name for this network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#name NetworkIsolated#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional description for the network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#description NetworkIsolated#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dhcp_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedDhcpPool"]]]:
        '''dhcp_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dhcp_pool NetworkIsolated#dhcp_pool}
        '''
        result = self._values.get("dhcp_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedDhcpPool"]]], result)

    @builtins.property
    def dns1(self) -> typing.Optional[builtins.str]:
        '''First DNS server to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns1 NetworkIsolated#dns1}
        '''
        result = self._values.get("dns1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns2(self) -> typing.Optional[builtins.str]:
        '''Second DNS server to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns2 NetworkIsolated#dns2}
        '''
        result = self._values.get("dns2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_suffix(self) -> typing.Optional[builtins.str]:
        '''A FQDN for the virtual machines on this network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#dns_suffix NetworkIsolated#dns_suffix}
        '''
        result = self._values.get("dns_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway(self) -> typing.Optional[builtins.str]:
        '''The gateway for this network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#gateway NetworkIsolated#gateway}
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#id NetworkIsolated#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key value map of metadata to assign to this network. Key and value can be any string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#metadata NetworkIsolated#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedMetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#metadata_entry NetworkIsolated#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedMetadataEntry"]]], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''The netmask for the new network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#netmask NetworkIsolated#netmask}
        '''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#org NetworkIsolated#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines if this network is shared between multiple VDCs in the Org.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#shared NetworkIsolated#shared}
        '''
        result = self._values.get("shared")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def static_ip_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedStaticIpPool"]]]:
        '''static_ip_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#static_ip_pool NetworkIsolated#static_ip_pool}
        '''
        result = self._values.get("static_ip_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedStaticIpPool"]]], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#vdc NetworkIsolated#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIsolatedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.networkIsolated.NetworkIsolatedDhcpPool",
    jsii_struct_bases=[],
    name_mapping={
        "end_address": "endAddress",
        "start_address": "startAddress",
        "default_lease_time": "defaultLeaseTime",
        "max_lease_time": "maxLeaseTime",
    },
)
class NetworkIsolatedDhcpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
        default_lease_time: typing.Optional[jsii.Number] = None,
        max_lease_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_address: The final address in the IP Range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#end_address NetworkIsolated#end_address}
        :param start_address: The first address in the IP Range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#start_address NetworkIsolated#start_address}
        :param default_lease_time: The default DHCP lease time to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#default_lease_time NetworkIsolated#default_lease_time}
        :param max_lease_time: The maximum DHCP lease time to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#max_lease_time NetworkIsolated#max_lease_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36914d56539d500834c6fdc467bb99b3aad47fff0a886a54cccb4bd06da971a5)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
            check_type(argname="argument default_lease_time", value=default_lease_time, expected_type=type_hints["default_lease_time"])
            check_type(argname="argument max_lease_time", value=max_lease_time, expected_type=type_hints["max_lease_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }
        if default_lease_time is not None:
            self._values["default_lease_time"] = default_lease_time
        if max_lease_time is not None:
            self._values["max_lease_time"] = max_lease_time

    @builtins.property
    def end_address(self) -> builtins.str:
        '''The final address in the IP Range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#end_address NetworkIsolated#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''The first address in the IP Range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#start_address NetworkIsolated#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_lease_time(self) -> typing.Optional[jsii.Number]:
        '''The default DHCP lease time to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#default_lease_time NetworkIsolated#default_lease_time}
        '''
        result = self._values.get("default_lease_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_lease_time(self) -> typing.Optional[jsii.Number]:
        '''The maximum DHCP lease time to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#max_lease_time NetworkIsolated#max_lease_time}
        '''
        result = self._values.get("max_lease_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIsolatedDhcpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkIsolatedDhcpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolated.NetworkIsolatedDhcpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f67c2ca96f6fd8a064c29350e6dece34b70db36a177066a39bdc55fd13c9a0e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkIsolatedDhcpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7616360fe8c0a6fe934e954f61994baeb69e51e336f95938bbe5d9b6d37e1b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkIsolatedDhcpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2805235949679a8af23fee9a130c259a908a327e10f75648e71196ccccae211)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55e45ecb7c6490e208ca8467bde93e1f341e12d87e459017df110ed6a8a05122)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7157599561c010d0fe28272f1fec79dbeb83825bab65f572f8e64711f3917552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedDhcpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedDhcpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedDhcpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58dd9df08ed6c7a22dfa0ddde31332f6fbcb14060aeef571b603a425474f5e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkIsolatedDhcpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolated.NetworkIsolatedDhcpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9f5f202442f35d391cd9c1e7d07e77fb1e29a8a18b67a6f3b461104cf1f65e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDefaultLeaseTime")
    def reset_default_lease_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLeaseTime", []))

    @jsii.member(jsii_name="resetMaxLeaseTime")
    def reset_max_lease_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLeaseTime", []))

    @builtins.property
    @jsii.member(jsii_name="defaultLeaseTimeInput")
    def default_lease_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultLeaseTimeInput"))

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
    @jsii.member(jsii_name="defaultLeaseTime")
    def default_lease_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultLeaseTime"))

    @default_lease_time.setter
    def default_lease_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62881a2592f71ec43cfa75b843177bf30c5c6a4d677431e126ae9d7e693e5103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLeaseTime", value)

    @builtins.property
    @jsii.member(jsii_name="endAddress")
    def end_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endAddress"))

    @end_address.setter
    def end_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90b420be1efec47800792e64e8ed111fb268661b3fc6be93205f3e8c45a929f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTime")
    def max_lease_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLeaseTime"))

    @max_lease_time.setter
    def max_lease_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3ab888293e5e15251465d39a3a8710b51092efcdc179d98af39071cd8914d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLeaseTime", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1b353ca546cf0b1a5ecbc3d0fa14e95d2ca4ca253282e4c4f26ac293bc55ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedDhcpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedDhcpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedDhcpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17ee37746fe90ade0c450d820649355a2eb6bd828996f79a24aee0190fba096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkIsolated.NetworkIsolatedMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "is_system": "isSystem",
        "key": "key",
        "type": "type",
        "user_access": "userAccess",
        "value": "value",
    },
)
class NetworkIsolatedMetadataEntry:
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
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#is_system NetworkIsolated#is_system}
        :param key: Key of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#key NetworkIsolated#key}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#type NetworkIsolated#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#user_access NetworkIsolated#user_access}
        :param value: Value of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#value NetworkIsolated#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6046cc49529ed0472bfbd3f0545acf2f925d032decd958d4edc3dc5f44124c80)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#is_system NetworkIsolated#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#key NetworkIsolated#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#type NetworkIsolated#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#user_access NetworkIsolated#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#value NetworkIsolated#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIsolatedMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkIsolatedMetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolated.NetworkIsolatedMetadataEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f85457415ad2507dd0a96c14eb1bb57f895b880936bb02084f5151d530e27f15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkIsolatedMetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d77fb01809def0f64e1bdb652c17951128f2803d1ad4ca574f3d108801c8394)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkIsolatedMetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb07098c21e41c853d2969982e8b8ddd0e40d7ccd7f4561cfa5763bc3046eb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aacebe320e0c033a2881435543d96a6705a3fd8748de278fc93bb9fff3cbcc6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3725ef35626dd8365d7c25637523d208a5a8a507d1c7d70a753f1b54024c2fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedMetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedMetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedMetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ebf72d519b38f97318a57d885048693ea0d5fa1d6c1d69d5211ee38e9dd3e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkIsolatedMetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolated.NetworkIsolatedMetadataEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c71c3cfcc38d4e1e88aff1e44590f246c38b44eec130137c5f89f0b5de7533a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aabb6cf7824afb68a025d6694152a71c2a2715aa36fbd4989902d54cb41596fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8a82d8697b4b275f6f1188231f9ccfc5415f26753370af1b1bfdec1e4c3dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8763799105ec3c4d5cffc0d21901e3a96bff967d8399edcf455aff39acfe9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf0982aaadea9749d4c930aedf1e1bf7727bc5471eb7f6d2497a13315df2086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a116a38c8679dbe29693c615ea7285a8bf6d9e58153dec832812f959dc5591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedMetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedMetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedMetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7305ff4c8c869ddcc7b2aef02b1c6db7e33fae1d52bb1adbd68f48dbbbe07958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkIsolated.NetworkIsolatedStaticIpPool",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class NetworkIsolatedStaticIpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: The final address in the IP Range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#end_address NetworkIsolated#end_address}
        :param start_address: The first address in the IP Range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#start_address NetworkIsolated#start_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5b5ed352f33a496253d1710407270704679bca553fe314da9051bccf0c7dc1)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''The final address in the IP Range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#end_address NetworkIsolated#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''The first address in the IP Range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated#start_address NetworkIsolated#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIsolatedStaticIpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkIsolatedStaticIpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolated.NetworkIsolatedStaticIpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c473067cfadd93a7ca5dca23cc3925dc0cbae0cf8849a6c64d731b59c8a40ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkIsolatedStaticIpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ddfcbbf79043ca5d824711dc2e78a393f9861c504424b5eda1918629460a84)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkIsolatedStaticIpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3e1e39dc9c9b34e157ef0bfc293476d25f3d14883cbc705c2d684a7151ed9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa32d007716e54c84852e656d5fcde0642deba3a2a6f5ffb97345ff3f666bc1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36400a0f6590bfae63083a6284aa297b41b13a4213ab1e792b98b218555008ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedStaticIpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedStaticIpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedStaticIpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8b2ff86ec89b5c30cf91cb9aeeb585d57077033cf60cff6314116fd707298b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkIsolatedStaticIpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolated.NetworkIsolatedStaticIpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__193bb41bc583c8c0b4b2fa09bd760979c5e827be756a636e95d2be98ba7dda2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95b764c255110b746a70b9620fdd6eea087ce190f456b3241fddc886ba888f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4bca6eda7427ec4a169c5974e00a98bf61bb8319500d242610ddd52c8e61cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedStaticIpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedStaticIpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedStaticIpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb930cb3668ca6c2f3c7ac5d9219686b2decb0314db4f65f1cc86158c908912c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NetworkIsolated",
    "NetworkIsolatedConfig",
    "NetworkIsolatedDhcpPool",
    "NetworkIsolatedDhcpPoolList",
    "NetworkIsolatedDhcpPoolOutputReference",
    "NetworkIsolatedMetadataEntry",
    "NetworkIsolatedMetadataEntryList",
    "NetworkIsolatedMetadataEntryOutputReference",
    "NetworkIsolatedStaticIpPool",
    "NetworkIsolatedStaticIpPoolList",
    "NetworkIsolatedStaticIpPoolOutputReference",
]

publication.publish()

def _typecheckingstub__12410298f2772bcf3c801595e5af845c1012f6fe3b98f56eef05db9d0e905b55(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedDhcpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    gateway: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    netmask: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__638a09d68726c1238f95920f35c407d9ff371720d8c8b04b4b94a0c7fb29fafc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4d11afb0f6ecddd120b58f914a47a75b16f243cd572e147654baefca4a2853(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedDhcpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cab2a97666a80cce2bb22c4fd96de0ba66b67f56de173fb715720a7d03bdc3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedMetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7234b2e7708c220e2c11e9cd15a4371a70227347aa46789678fad5710b17aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedStaticIpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ae285fb96ee9e304d98da94a58e25cda4079e43bf5ad5f5898fcc37389a281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ca17cb4e7965ee769f3a956cb07bfa6e493bbcb8cdd7232638bcad836cd721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72a225ead152f024ecb98fa94fea9aefce6cf847cb261f02865e1e6826d4c48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a726bf1b22048af71ac79c374e0ad2e739a6f47275b0747e1d372d045c16e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966b238fde6744e51719fa02d25ee86da6deb7877aec03642c26c4f4e0635095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d0bd1bfcc0f0abf55c76d85cf2deb86158cf40944b4874576b613c08ced897(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad04b86a77916619066f419cec9e4b33de2989c36cd1a3d36e0226f814a04525(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e48a245345aaad1554dd6a76603a937253339d681b2b9016183492165ce2e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e60e13f69565e3cd593b8ed2b3c02f1b38d102c28a556faf32af719cd5f1f0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d636f46604d0201d535dfbc6fd3105b8018d8388a8938ac6f7722d5b3f21dde1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53f24ce90df44e863d99d73b28d07921cb32853819fa0c35c298f30b2412c93(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b703b99090551ec8e28426db9782f9f1d8cd0028edabd3d759b75894358c6eed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114613f68c1be6b5f3c0a1a5fb297b50cc5b12182305b5476c7537b1fc193317(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedDhcpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    gateway: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    netmask: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36914d56539d500834c6fdc467bb99b3aad47fff0a886a54cccb4bd06da971a5(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
    default_lease_time: typing.Optional[jsii.Number] = None,
    max_lease_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67c2ca96f6fd8a064c29350e6dece34b70db36a177066a39bdc55fd13c9a0e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7616360fe8c0a6fe934e954f61994baeb69e51e336f95938bbe5d9b6d37e1b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2805235949679a8af23fee9a130c259a908a327e10f75648e71196ccccae211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e45ecb7c6490e208ca8467bde93e1f341e12d87e459017df110ed6a8a05122(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7157599561c010d0fe28272f1fec79dbeb83825bab65f572f8e64711f3917552(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58dd9df08ed6c7a22dfa0ddde31332f6fbcb14060aeef571b603a425474f5e89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedDhcpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f5f202442f35d391cd9c1e7d07e77fb1e29a8a18b67a6f3b461104cf1f65e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62881a2592f71ec43cfa75b843177bf30c5c6a4d677431e126ae9d7e693e5103(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90b420be1efec47800792e64e8ed111fb268661b3fc6be93205f3e8c45a929f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3ab888293e5e15251465d39a3a8710b51092efcdc179d98af39071cd8914d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1b353ca546cf0b1a5ecbc3d0fa14e95d2ca4ca253282e4c4f26ac293bc55ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17ee37746fe90ade0c450d820649355a2eb6bd828996f79a24aee0190fba096(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedDhcpPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6046cc49529ed0472bfbd3f0545acf2f925d032decd958d4edc3dc5f44124c80(
    *,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85457415ad2507dd0a96c14eb1bb57f895b880936bb02084f5151d530e27f15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d77fb01809def0f64e1bdb652c17951128f2803d1ad4ca574f3d108801c8394(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb07098c21e41c853d2969982e8b8ddd0e40d7ccd7f4561cfa5763bc3046eb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacebe320e0c033a2881435543d96a6705a3fd8748de278fc93bb9fff3cbcc6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3725ef35626dd8365d7c25637523d208a5a8a507d1c7d70a753f1b54024c2fea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ebf72d519b38f97318a57d885048693ea0d5fa1d6c1d69d5211ee38e9dd3e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedMetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c71c3cfcc38d4e1e88aff1e44590f246c38b44eec130137c5f89f0b5de7533a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabb6cf7824afb68a025d6694152a71c2a2715aa36fbd4989902d54cb41596fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8a82d8697b4b275f6f1188231f9ccfc5415f26753370af1b1bfdec1e4c3dcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8763799105ec3c4d5cffc0d21901e3a96bff967d8399edcf455aff39acfe9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf0982aaadea9749d4c930aedf1e1bf7727bc5471eb7f6d2497a13315df2086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a116a38c8679dbe29693c615ea7285a8bf6d9e58153dec832812f959dc5591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7305ff4c8c869ddcc7b2aef02b1c6db7e33fae1d52bb1adbd68f48dbbbe07958(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedMetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5b5ed352f33a496253d1710407270704679bca553fe314da9051bccf0c7dc1(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c473067cfadd93a7ca5dca23cc3925dc0cbae0cf8849a6c64d731b59c8a40ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ddfcbbf79043ca5d824711dc2e78a393f9861c504424b5eda1918629460a84(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3e1e39dc9c9b34e157ef0bfc293476d25f3d14883cbc705c2d684a7151ed9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa32d007716e54c84852e656d5fcde0642deba3a2a6f5ffb97345ff3f666bc1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36400a0f6590bfae63083a6284aa297b41b13a4213ab1e792b98b218555008ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8b2ff86ec89b5c30cf91cb9aeeb585d57077033cf60cff6314116fd707298b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedStaticIpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193bb41bc583c8c0b4b2fa09bd760979c5e827be756a636e95d2be98ba7dda2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b764c255110b746a70b9620fdd6eea087ce190f456b3241fddc886ba888f7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4bca6eda7427ec4a169c5974e00a98bf61bb8319500d242610ddd52c8e61cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb930cb3668ca6c2f3c7ac5d9219686b2decb0314db4f65f1cc86158c908912c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedStaticIpPool]],
) -> None:
    """Type checking stubs"""
    pass
