'''
# `vcd_network_isolated_v2`

Refer to the Terraform Registry for docs: [`vcd_network_isolated_v2`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2).
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


class NetworkIsolatedV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2 vcd_network_isolated_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        gateway: builtins.str,
        name: builtins.str,
        prefix_length: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        dual_stack_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_vlan_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        is_shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2MetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        org: typing.Optional[builtins.str] = None,
        owner_id: typing.Optional[builtins.str] = None,
        secondary_gateway: typing.Optional[builtins.str] = None,
        secondary_prefix_length: typing.Optional[builtins.str] = None,
        secondary_static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2SecondaryStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2StaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2 vcd_network_isolated_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param gateway: Gateway IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#gateway NetworkIsolatedV2#gateway}
        :param name: Network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#name NetworkIsolatedV2#name}
        :param prefix_length: Network prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#prefix_length NetworkIsolatedV2#prefix_length}
        :param description: Network description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#description NetworkIsolatedV2#description}
        :param dns1: DNS server 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns1 NetworkIsolatedV2#dns1}
        :param dns2: DNS server 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns2 NetworkIsolatedV2#dns2}
        :param dns_suffix: DNS suffix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns_suffix NetworkIsolatedV2#dns_suffix}
        :param dual_stack_enabled: Boolean value if Dual-Stack mode should be enabled (default ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dual_stack_enabled NetworkIsolatedV2#dual_stack_enabled}
        :param guest_vlan_allowed: True if network allows guest VLAN tagging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#guest_vlan_allowed NetworkIsolatedV2#guest_vlan_allowed}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#id NetworkIsolatedV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_shared: NSX-V only - share this network with other VDCs in this organization. Default - false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#is_shared NetworkIsolatedV2#is_shared}
        :param metadata: Key value map of metadata to assign to this network. Key and value can be any string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#metadata NetworkIsolatedV2#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#metadata_entry NetworkIsolatedV2#metadata_entry}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#org NetworkIsolatedV2#org}
        :param owner_id: ID of VDC or VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#owner_id NetworkIsolatedV2#owner_id}
        :param secondary_gateway: Secondary gateway (can only be IPv6 and requires enabled Dual Stack mode). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_gateway NetworkIsolatedV2#secondary_gateway}
        :param secondary_prefix_length: Secondary prefix (can only be IPv6 and requires enabled Dual Stack mode). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_prefix_length NetworkIsolatedV2#secondary_prefix_length}
        :param secondary_static_ip_pool: secondary_static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_static_ip_pool NetworkIsolatedV2#secondary_static_ip_pool}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#static_ip_pool NetworkIsolatedV2#static_ip_pool}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#vdc NetworkIsolatedV2#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f852a4459dc474abf98d8cd4f39b2ddf0d76e50d44d4aa449989316360dec6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkIsolatedV2Config(
            gateway=gateway,
            name=name,
            prefix_length=prefix_length,
            description=description,
            dns1=dns1,
            dns2=dns2,
            dns_suffix=dns_suffix,
            dual_stack_enabled=dual_stack_enabled,
            guest_vlan_allowed=guest_vlan_allowed,
            id=id,
            is_shared=is_shared,
            metadata=metadata,
            metadata_entry=metadata_entry,
            org=org,
            owner_id=owner_id,
            secondary_gateway=secondary_gateway,
            secondary_prefix_length=secondary_prefix_length,
            secondary_static_ip_pool=secondary_static_ip_pool,
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
        '''Generates CDKTF code for importing a NetworkIsolatedV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkIsolatedV2 to import.
        :param import_from_id: The id of the existing NetworkIsolatedV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkIsolatedV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec06712aa797a711f3c6837866b25e6ea49f0068b80103ce4fde5535f8411932)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2MetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fa9bf40f772f90786bfe48b54dd984b511057f731026ddbfe6b1b156760d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="putSecondaryStaticIpPool")
    def put_secondary_static_ip_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2SecondaryStaticIpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b0156ad5489ab2f2a4126e48a8adbf23be22767bbc4934db1ef013ca6fe364e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondaryStaticIpPool", [value]))

    @jsii.member(jsii_name="putStaticIpPool")
    def put_static_ip_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2StaticIpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d745c7bded5d92ed2d5da9e941acb13e4fe6f2aab29aabb1434ebda9d9143f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStaticIpPool", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDns1")
    def reset_dns1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns1", []))

    @jsii.member(jsii_name="resetDns2")
    def reset_dns2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns2", []))

    @jsii.member(jsii_name="resetDnsSuffix")
    def reset_dns_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsSuffix", []))

    @jsii.member(jsii_name="resetDualStackEnabled")
    def reset_dual_stack_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDualStackEnabled", []))

    @jsii.member(jsii_name="resetGuestVlanAllowed")
    def reset_guest_vlan_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestVlanAllowed", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsShared")
    def reset_is_shared(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsShared", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataEntry")
    def reset_metadata_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataEntry", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOwnerId")
    def reset_owner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnerId", []))

    @jsii.member(jsii_name="resetSecondaryGateway")
    def reset_secondary_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryGateway", []))

    @jsii.member(jsii_name="resetSecondaryPrefixLength")
    def reset_secondary_prefix_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryPrefixLength", []))

    @jsii.member(jsii_name="resetSecondaryStaticIpPool")
    def reset_secondary_static_ip_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryStaticIpPool", []))

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
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "NetworkIsolatedV2MetadataEntryList":
        return typing.cast("NetworkIsolatedV2MetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="secondaryStaticIpPool")
    def secondary_static_ip_pool(self) -> "NetworkIsolatedV2SecondaryStaticIpPoolList":
        return typing.cast("NetworkIsolatedV2SecondaryStaticIpPoolList", jsii.get(self, "secondaryStaticIpPool"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPool")
    def static_ip_pool(self) -> "NetworkIsolatedV2StaticIpPoolList":
        return typing.cast("NetworkIsolatedV2StaticIpPoolList", jsii.get(self, "staticIpPool"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="dualStackEnabledInput")
    def dual_stack_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dualStackEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="guestVlanAllowedInput")
    def guest_vlan_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "guestVlanAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isSharedInput")
    def is_shared_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSharedInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntryInput")
    def metadata_entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2MetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2MetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

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
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerIdInput")
    def owner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryGatewayInput")
    def secondary_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryPrefixLengthInput")
    def secondary_prefix_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryPrefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryStaticIpPoolInput")
    def secondary_static_ip_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2SecondaryStaticIpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2SecondaryStaticIpPool"]]], jsii.get(self, "secondaryStaticIpPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPoolInput")
    def static_ip_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2StaticIpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2StaticIpPool"]]], jsii.get(self, "staticIpPoolInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8e9ede1234982374877b961fcb79dfe9bef66895604d6bc2cc42f21c7e5d6888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="dns1")
    def dns1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns1"))

    @dns1.setter
    def dns1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7331106f8827fae1c7d425f98ff7c5c8a085d4d0a95a0eb5e2aa01de642f55fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns1", value)

    @builtins.property
    @jsii.member(jsii_name="dns2")
    def dns2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns2"))

    @dns2.setter
    def dns2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7334f265fd26d3591aa8d3c7e293caf4c9bf0a2d63a682ecc1d2fa4b17348cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns2", value)

    @builtins.property
    @jsii.member(jsii_name="dnsSuffix")
    def dns_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsSuffix"))

    @dns_suffix.setter
    def dns_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02471c72291eaadc56cc2648af6e5a05ac3615d22efc2d893420ab206ccda58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="dualStackEnabled")
    def dual_stack_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dualStackEnabled"))

    @dual_stack_enabled.setter
    def dual_stack_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5dc43d0585f1993bb12fbd78b0e5c66eec33a24b72b7ebd88213306a1b1c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dualStackEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579207fae143be4e230ba2446008dad05c46640433a9f010ce42227b20d31698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="guestVlanAllowed")
    def guest_vlan_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "guestVlanAllowed"))

    @guest_vlan_allowed.setter
    def guest_vlan_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0343c7679f1fef339fc1498c0ea56da974987a4e88d4c8edb6b61299cb5a843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestVlanAllowed", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ddd5e74954521ba657ca6a6fbe6ac67fb9c453d0311bed9c9aa3b2eac72e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isShared")
    def is_shared(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isShared"))

    @is_shared.setter
    def is_shared(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73faa63adff6f5f3b5a9988d2e34e0a5bceb6d536892bab02c8f8c22c40efbd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isShared", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72962ca40531d691acc7522fd2f5754156f4e028a3be2516cd2065d9c59753c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff97e6d9f4f589f1b6978e783aaf4e5e56e87287389ae75ec09a874a1f1b1681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4c22588ea5fdb5b3ffd262f98848e548ed37a5fde9c02b1ccbd23db936f942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="ownerId")
    def owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerId"))

    @owner_id.setter
    def owner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b09c5bdf0357aa44b44c473778bde392956ae7fa775e4edd968fa18aac5cd8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerId", value)

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9236db10d0453d873a417d0e26deccd57472bdd9c29ab87b80499549ad34471d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="secondaryGateway")
    def secondary_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryGateway"))

    @secondary_gateway.setter
    def secondary_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb72eecfc55b6ed2267f2ed350c577a24f5e0b052857851d13527e26bef1ff65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryGateway", value)

    @builtins.property
    @jsii.member(jsii_name="secondaryPrefixLength")
    def secondary_prefix_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryPrefixLength"))

    @secondary_prefix_length.setter
    def secondary_prefix_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d8047722fdeacab78d7d264d4698d7ef4902143a5350f0100deea109ce2d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryPrefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bedb74a0c7a9daeb3dd4d0b9509c63fb52e1dd834b6b13c3a7a69aa3384976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "gateway": "gateway",
        "name": "name",
        "prefix_length": "prefixLength",
        "description": "description",
        "dns1": "dns1",
        "dns2": "dns2",
        "dns_suffix": "dnsSuffix",
        "dual_stack_enabled": "dualStackEnabled",
        "guest_vlan_allowed": "guestVlanAllowed",
        "id": "id",
        "is_shared": "isShared",
        "metadata": "metadata",
        "metadata_entry": "metadataEntry",
        "org": "org",
        "owner_id": "ownerId",
        "secondary_gateway": "secondaryGateway",
        "secondary_prefix_length": "secondaryPrefixLength",
        "secondary_static_ip_pool": "secondaryStaticIpPool",
        "static_ip_pool": "staticIpPool",
        "vdc": "vdc",
    },
)
class NetworkIsolatedV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gateway: builtins.str,
        name: builtins.str,
        prefix_length: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        dual_stack_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_vlan_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        is_shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2MetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        org: typing.Optional[builtins.str] = None,
        owner_id: typing.Optional[builtins.str] = None,
        secondary_gateway: typing.Optional[builtins.str] = None,
        secondary_prefix_length: typing.Optional[builtins.str] = None,
        secondary_static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2SecondaryStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkIsolatedV2StaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param gateway: Gateway IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#gateway NetworkIsolatedV2#gateway}
        :param name: Network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#name NetworkIsolatedV2#name}
        :param prefix_length: Network prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#prefix_length NetworkIsolatedV2#prefix_length}
        :param description: Network description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#description NetworkIsolatedV2#description}
        :param dns1: DNS server 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns1 NetworkIsolatedV2#dns1}
        :param dns2: DNS server 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns2 NetworkIsolatedV2#dns2}
        :param dns_suffix: DNS suffix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns_suffix NetworkIsolatedV2#dns_suffix}
        :param dual_stack_enabled: Boolean value if Dual-Stack mode should be enabled (default ``false``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dual_stack_enabled NetworkIsolatedV2#dual_stack_enabled}
        :param guest_vlan_allowed: True if network allows guest VLAN tagging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#guest_vlan_allowed NetworkIsolatedV2#guest_vlan_allowed}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#id NetworkIsolatedV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_shared: NSX-V only - share this network with other VDCs in this organization. Default - false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#is_shared NetworkIsolatedV2#is_shared}
        :param metadata: Key value map of metadata to assign to this network. Key and value can be any string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#metadata NetworkIsolatedV2#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#metadata_entry NetworkIsolatedV2#metadata_entry}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#org NetworkIsolatedV2#org}
        :param owner_id: ID of VDC or VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#owner_id NetworkIsolatedV2#owner_id}
        :param secondary_gateway: Secondary gateway (can only be IPv6 and requires enabled Dual Stack mode). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_gateway NetworkIsolatedV2#secondary_gateway}
        :param secondary_prefix_length: Secondary prefix (can only be IPv6 and requires enabled Dual Stack mode). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_prefix_length NetworkIsolatedV2#secondary_prefix_length}
        :param secondary_static_ip_pool: secondary_static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_static_ip_pool NetworkIsolatedV2#secondary_static_ip_pool}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#static_ip_pool NetworkIsolatedV2#static_ip_pool}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#vdc NetworkIsolatedV2#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b865fbfdc4eae1a6aaff6785db15b6298e782edcf29eeec5628db1d241efe0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dns1", value=dns1, expected_type=type_hints["dns1"])
            check_type(argname="argument dns2", value=dns2, expected_type=type_hints["dns2"])
            check_type(argname="argument dns_suffix", value=dns_suffix, expected_type=type_hints["dns_suffix"])
            check_type(argname="argument dual_stack_enabled", value=dual_stack_enabled, expected_type=type_hints["dual_stack_enabled"])
            check_type(argname="argument guest_vlan_allowed", value=guest_vlan_allowed, expected_type=type_hints["guest_vlan_allowed"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_shared", value=is_shared, expected_type=type_hints["is_shared"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_entry", value=metadata_entry, expected_type=type_hints["metadata_entry"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
            check_type(argname="argument secondary_gateway", value=secondary_gateway, expected_type=type_hints["secondary_gateway"])
            check_type(argname="argument secondary_prefix_length", value=secondary_prefix_length, expected_type=type_hints["secondary_prefix_length"])
            check_type(argname="argument secondary_static_ip_pool", value=secondary_static_ip_pool, expected_type=type_hints["secondary_static_ip_pool"])
            check_type(argname="argument static_ip_pool", value=static_ip_pool, expected_type=type_hints["static_ip_pool"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway": gateway,
            "name": name,
            "prefix_length": prefix_length,
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
        if dns1 is not None:
            self._values["dns1"] = dns1
        if dns2 is not None:
            self._values["dns2"] = dns2
        if dns_suffix is not None:
            self._values["dns_suffix"] = dns_suffix
        if dual_stack_enabled is not None:
            self._values["dual_stack_enabled"] = dual_stack_enabled
        if guest_vlan_allowed is not None:
            self._values["guest_vlan_allowed"] = guest_vlan_allowed
        if id is not None:
            self._values["id"] = id
        if is_shared is not None:
            self._values["is_shared"] = is_shared
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_entry is not None:
            self._values["metadata_entry"] = metadata_entry
        if org is not None:
            self._values["org"] = org
        if owner_id is not None:
            self._values["owner_id"] = owner_id
        if secondary_gateway is not None:
            self._values["secondary_gateway"] = secondary_gateway
        if secondary_prefix_length is not None:
            self._values["secondary_prefix_length"] = secondary_prefix_length
        if secondary_static_ip_pool is not None:
            self._values["secondary_static_ip_pool"] = secondary_static_ip_pool
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
    def gateway(self) -> builtins.str:
        '''Gateway IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#gateway NetworkIsolatedV2#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#name NetworkIsolatedV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_length(self) -> jsii.Number:
        '''Network prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#prefix_length NetworkIsolatedV2#prefix_length}
        '''
        result = self._values.get("prefix_length")
        assert result is not None, "Required property 'prefix_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Network description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#description NetworkIsolatedV2#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns1(self) -> typing.Optional[builtins.str]:
        '''DNS server 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns1 NetworkIsolatedV2#dns1}
        '''
        result = self._values.get("dns1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns2(self) -> typing.Optional[builtins.str]:
        '''DNS server 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns2 NetworkIsolatedV2#dns2}
        '''
        result = self._values.get("dns2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_suffix(self) -> typing.Optional[builtins.str]:
        '''DNS suffix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dns_suffix NetworkIsolatedV2#dns_suffix}
        '''
        result = self._values.get("dns_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dual_stack_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean value if Dual-Stack mode should be enabled (default ``false``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#dual_stack_enabled NetworkIsolatedV2#dual_stack_enabled}
        '''
        result = self._values.get("dual_stack_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def guest_vlan_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if network allows guest VLAN tagging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#guest_vlan_allowed NetworkIsolatedV2#guest_vlan_allowed}
        '''
        result = self._values.get("guest_vlan_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#id NetworkIsolatedV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_shared(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''NSX-V only - share this network with other VDCs in this organization. Default - false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#is_shared NetworkIsolatedV2#is_shared}
        '''
        result = self._values.get("is_shared")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key value map of metadata to assign to this network. Key and value can be any string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#metadata NetworkIsolatedV2#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2MetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#metadata_entry NetworkIsolatedV2#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2MetadataEntry"]]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#org NetworkIsolatedV2#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_id(self) -> typing.Optional[builtins.str]:
        '''ID of VDC or VDC Group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#owner_id NetworkIsolatedV2#owner_id}
        '''
        result = self._values.get("owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_gateway(self) -> typing.Optional[builtins.str]:
        '''Secondary gateway (can only be IPv6 and requires enabled Dual Stack mode).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_gateway NetworkIsolatedV2#secondary_gateway}
        '''
        result = self._values.get("secondary_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_prefix_length(self) -> typing.Optional[builtins.str]:
        '''Secondary prefix (can only be IPv6 and requires enabled Dual Stack mode).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_prefix_length NetworkIsolatedV2#secondary_prefix_length}
        '''
        result = self._values.get("secondary_prefix_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_static_ip_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2SecondaryStaticIpPool"]]]:
        '''secondary_static_ip_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#secondary_static_ip_pool NetworkIsolatedV2#secondary_static_ip_pool}
        '''
        result = self._values.get("secondary_static_ip_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2SecondaryStaticIpPool"]]], result)

    @builtins.property
    def static_ip_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2StaticIpPool"]]]:
        '''static_ip_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#static_ip_pool NetworkIsolatedV2#static_ip_pool}
        '''
        result = self._values.get("static_ip_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkIsolatedV2StaticIpPool"]]], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#vdc NetworkIsolatedV2#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIsolatedV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2MetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "is_system": "isSystem",
        "key": "key",
        "type": "type",
        "user_access": "userAccess",
        "value": "value",
    },
)
class NetworkIsolatedV2MetadataEntry:
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
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#is_system NetworkIsolatedV2#is_system}
        :param key: Key of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#key NetworkIsolatedV2#key}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#type NetworkIsolatedV2#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#user_access NetworkIsolatedV2#user_access}
        :param value: Value of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#value NetworkIsolatedV2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c26cc4a143e1cf7cecad4d6d9440d1e4c0b900b9c37a0cbc40dc86d61c224e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#is_system NetworkIsolatedV2#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#key NetworkIsolatedV2#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#type NetworkIsolatedV2#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#user_access NetworkIsolatedV2#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#value NetworkIsolatedV2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIsolatedV2MetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkIsolatedV2MetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2MetadataEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c111da4bca5915a7ab3f4727a744896dc8dee17a6fc05fd405f88c2d5afa8ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkIsolatedV2MetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687d923a9c4513d9ed0062ba6ac4d13ae2a006d6f63d1cd8a861ffcd47e5f355)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkIsolatedV2MetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632971619e9c848e873806f651b696b3084287037fd463d9ca5290ab4d7c932d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58c5e22dc6b7dffddf79348a0adf333ff4c31e9b1c6603f816722f2b3ed5ed1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e70f119be444c8eae8073d2be4d2fa7a8e6b24822b9bcddfd48d26a83f99d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2MetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2MetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2MetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54523a529255d19973356ab79bbd6ee5a243cbeaad7831439e2edb9274a63be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkIsolatedV2MetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2MetadataEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__865896923f4be458af2cc9271fc819fea3bca3744fdba5decd4759cb416d8238)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6b01cea3d36dda916cf67c57652b7bca6b1256ceaaa0813d744496f62b9aaee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68f1adf04b70f26040d4f5a54581ced90d5c4c255d9dd9487a7c0f01d8f2d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d408ecebdaa2a049ff3cb59a4f3bcec9758338c45904545836cb6dc5914b336b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d438a38d9bf440313b1300ec1be00e31b5b1c004411ba3ab6461e264a2fccae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bdf44d3901692301f65223dec669ec386dadc350f8aac9bc024f67ea079a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2MetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2MetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2MetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__339a58e3d70d53b93c06de5066d97c7e631e9976920e4483201eac147ccbd687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2SecondaryStaticIpPool",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class NetworkIsolatedV2SecondaryStaticIpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: End address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#end_address NetworkIsolatedV2#end_address}
        :param start_address: Start address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#start_address NetworkIsolatedV2#start_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d16f7b090b1edcf13c0707ec00ea3238320a6131255aa2efc4b7c6a7a59cfc7)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''End address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#end_address NetworkIsolatedV2#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Start address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#start_address NetworkIsolatedV2#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIsolatedV2SecondaryStaticIpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkIsolatedV2SecondaryStaticIpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2SecondaryStaticIpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34256f304c77f14d41471c6af7b44e24fad047a297502a439a47e4aeffc09f41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkIsolatedV2SecondaryStaticIpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598c491a00ddae3bd2201e32c74489312fc528a3c6b3601e9b14fc21bf5324d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkIsolatedV2SecondaryStaticIpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a47f1b94599b2c86def721818fe97c687d785c7cd065368bb2584590ac5911)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecda1cf9891a1f4fe0ed5928317cf9b0c36c9ca8c8feaee3d7c5b068094f5fbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__074bc20da5cdacdfb0130913847edafb5ea22568f8ba439992820ee21c32e960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2SecondaryStaticIpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2SecondaryStaticIpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2SecondaryStaticIpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a927d1d59ac310c68cbcaac6d82be7286522afc5be34704ff95eeacfdd1ad619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkIsolatedV2SecondaryStaticIpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2SecondaryStaticIpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab9ae5c9f2e6f38beffc788ad3f1da7a9597cbf6568884d394bda6750ba6ead)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92a5c11d2b97afe363652515e9d75076cd0c4fdb410721a5d02a7be60eb900e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c238b133f004be5f90e77adfc94837f2f5089543676e056336ecdefe184c627f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2SecondaryStaticIpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2SecondaryStaticIpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2SecondaryStaticIpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b77d338e6c132ced66a64489f5637dae50d9ccc6fbd34cea671bc008960b0a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2StaticIpPool",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class NetworkIsolatedV2StaticIpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: End address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#end_address NetworkIsolatedV2#end_address}
        :param start_address: Start address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#start_address NetworkIsolatedV2#start_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0d891b9b18a85faed9f935538a85f903ab157059330fb767b2f4f1ace6c69d)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''End address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#end_address NetworkIsolatedV2#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Start address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_isolated_v2#start_address NetworkIsolatedV2#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkIsolatedV2StaticIpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkIsolatedV2StaticIpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2StaticIpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__938879f6549f554c464a6129c75df528605d5a35fe6fd449c248c8608648fadb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkIsolatedV2StaticIpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5483bec6b57fbf491e09abee7d3a4baed3d3e1d283b10b06a7667aaf54e04c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkIsolatedV2StaticIpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852b0547ce80c2d3661b19b1182b6fbce728be119707195d68023f63ebfa604e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a6d6343de2f8f0a7a4a664b336888f92fc790b72226d3b77ccb0f44d219e1a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e463b41deaf5abb232f25143c1b3f578dedfa82f4c7082af4c22a8b3364c0bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2StaticIpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2StaticIpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2StaticIpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a139d7dcdb7509381bf9d301d732bd3eebbb33e286d27dbf28e896888905002b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkIsolatedV2StaticIpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkIsolatedV2.NetworkIsolatedV2StaticIpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f39a0a9ed9176811461b56ecb45eb395fa9567aef1a29bd47307cb3b1bb1fe02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f6426aa1631516d4fe880fc7c5806c10b59547cb9f5be13536bc26380f0c427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394d95f26e41d425dc4a63b15a2cc8b79e4dac66047b8de8ca2b6b8342865a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2StaticIpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2StaticIpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2StaticIpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53fcb41c06e61f4b74432833b6058e76fd315cf185d58b100e1e7a4d6a9f5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NetworkIsolatedV2",
    "NetworkIsolatedV2Config",
    "NetworkIsolatedV2MetadataEntry",
    "NetworkIsolatedV2MetadataEntryList",
    "NetworkIsolatedV2MetadataEntryOutputReference",
    "NetworkIsolatedV2SecondaryStaticIpPool",
    "NetworkIsolatedV2SecondaryStaticIpPoolList",
    "NetworkIsolatedV2SecondaryStaticIpPoolOutputReference",
    "NetworkIsolatedV2StaticIpPool",
    "NetworkIsolatedV2StaticIpPoolList",
    "NetworkIsolatedV2StaticIpPoolOutputReference",
]

publication.publish()

def _typecheckingstub__4f852a4459dc474abf98d8cd4f39b2ddf0d76e50d44d4aa449989316360dec6f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    gateway: builtins.str,
    name: builtins.str,
    prefix_length: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    dual_stack_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_vlan_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    is_shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2MetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org: typing.Optional[builtins.str] = None,
    owner_id: typing.Optional[builtins.str] = None,
    secondary_gateway: typing.Optional[builtins.str] = None,
    secondary_prefix_length: typing.Optional[builtins.str] = None,
    secondary_static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2SecondaryStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2StaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__ec06712aa797a711f3c6837866b25e6ea49f0068b80103ce4fde5535f8411932(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fa9bf40f772f90786bfe48b54dd984b511057f731026ddbfe6b1b156760d5c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2MetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0156ad5489ab2f2a4126e48a8adbf23be22767bbc4934db1ef013ca6fe364e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2SecondaryStaticIpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d745c7bded5d92ed2d5da9e941acb13e4fe6f2aab29aabb1434ebda9d9143f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2StaticIpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9ede1234982374877b961fcb79dfe9bef66895604d6bc2cc42f21c7e5d6888(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7331106f8827fae1c7d425f98ff7c5c8a085d4d0a95a0eb5e2aa01de642f55fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7334f265fd26d3591aa8d3c7e293caf4c9bf0a2d63a682ecc1d2fa4b17348cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02471c72291eaadc56cc2648af6e5a05ac3615d22efc2d893420ab206ccda58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5dc43d0585f1993bb12fbd78b0e5c66eec33a24b72b7ebd88213306a1b1c71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579207fae143be4e230ba2446008dad05c46640433a9f010ce42227b20d31698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0343c7679f1fef339fc1498c0ea56da974987a4e88d4c8edb6b61299cb5a843(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ddd5e74954521ba657ca6a6fbe6ac67fb9c453d0311bed9c9aa3b2eac72e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73faa63adff6f5f3b5a9988d2e34e0a5bceb6d536892bab02c8f8c22c40efbd8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72962ca40531d691acc7522fd2f5754156f4e028a3be2516cd2065d9c59753c1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff97e6d9f4f589f1b6978e783aaf4e5e56e87287389ae75ec09a874a1f1b1681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4c22588ea5fdb5b3ffd262f98848e548ed37a5fde9c02b1ccbd23db936f942(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b09c5bdf0357aa44b44c473778bde392956ae7fa775e4edd968fa18aac5cd8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9236db10d0453d873a417d0e26deccd57472bdd9c29ab87b80499549ad34471d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb72eecfc55b6ed2267f2ed350c577a24f5e0b052857851d13527e26bef1ff65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d8047722fdeacab78d7d264d4698d7ef4902143a5350f0100deea109ce2d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bedb74a0c7a9daeb3dd4d0b9509c63fb52e1dd834b6b13c3a7a69aa3384976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b865fbfdc4eae1a6aaff6785db15b6298e782edcf29eeec5628db1d241efe0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gateway: builtins.str,
    name: builtins.str,
    prefix_length: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    dual_stack_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_vlan_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    is_shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2MetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org: typing.Optional[builtins.str] = None,
    owner_id: typing.Optional[builtins.str] = None,
    secondary_gateway: typing.Optional[builtins.str] = None,
    secondary_prefix_length: typing.Optional[builtins.str] = None,
    secondary_static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2SecondaryStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkIsolatedV2StaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c26cc4a143e1cf7cecad4d6d9440d1e4c0b900b9c37a0cbc40dc86d61c224e(
    *,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c111da4bca5915a7ab3f4727a744896dc8dee17a6fc05fd405f88c2d5afa8ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687d923a9c4513d9ed0062ba6ac4d13ae2a006d6f63d1cd8a861ffcd47e5f355(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632971619e9c848e873806f651b696b3084287037fd463d9ca5290ab4d7c932d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c5e22dc6b7dffddf79348a0adf333ff4c31e9b1c6603f816722f2b3ed5ed1a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e70f119be444c8eae8073d2be4d2fa7a8e6b24822b9bcddfd48d26a83f99d74(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54523a529255d19973356ab79bbd6ee5a243cbeaad7831439e2edb9274a63be7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2MetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865896923f4be458af2cc9271fc819fea3bca3744fdba5decd4759cb416d8238(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b01cea3d36dda916cf67c57652b7bca6b1256ceaaa0813d744496f62b9aaee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68f1adf04b70f26040d4f5a54581ced90d5c4c255d9dd9487a7c0f01d8f2d4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d408ecebdaa2a049ff3cb59a4f3bcec9758338c45904545836cb6dc5914b336b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d438a38d9bf440313b1300ec1be00e31b5b1c004411ba3ab6461e264a2fccae1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bdf44d3901692301f65223dec669ec386dadc350f8aac9bc024f67ea079a41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339a58e3d70d53b93c06de5066d97c7e631e9976920e4483201eac147ccbd687(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2MetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d16f7b090b1edcf13c0707ec00ea3238320a6131255aa2efc4b7c6a7a59cfc7(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34256f304c77f14d41471c6af7b44e24fad047a297502a439a47e4aeffc09f41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598c491a00ddae3bd2201e32c74489312fc528a3c6b3601e9b14fc21bf5324d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a47f1b94599b2c86def721818fe97c687d785c7cd065368bb2584590ac5911(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecda1cf9891a1f4fe0ed5928317cf9b0c36c9ca8c8feaee3d7c5b068094f5fbf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074bc20da5cdacdfb0130913847edafb5ea22568f8ba439992820ee21c32e960(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a927d1d59ac310c68cbcaac6d82be7286522afc5be34704ff95eeacfdd1ad619(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2SecondaryStaticIpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab9ae5c9f2e6f38beffc788ad3f1da7a9597cbf6568884d394bda6750ba6ead(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a5c11d2b97afe363652515e9d75076cd0c4fdb410721a5d02a7be60eb900e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c238b133f004be5f90e77adfc94837f2f5089543676e056336ecdefe184c627f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b77d338e6c132ced66a64489f5637dae50d9ccc6fbd34cea671bc008960b0a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2SecondaryStaticIpPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0d891b9b18a85faed9f935538a85f903ab157059330fb767b2f4f1ace6c69d(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938879f6549f554c464a6129c75df528605d5a35fe6fd449c248c8608648fadb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5483bec6b57fbf491e09abee7d3a4baed3d3e1d283b10b06a7667aaf54e04c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852b0547ce80c2d3661b19b1182b6fbce728be119707195d68023f63ebfa604e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6d6343de2f8f0a7a4a664b336888f92fc790b72226d3b77ccb0f44d219e1a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e463b41deaf5abb232f25143c1b3f578dedfa82f4c7082af4c22a8b3364c0bff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a139d7dcdb7509381bf9d301d732bd3eebbb33e286d27dbf28e896888905002b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkIsolatedV2StaticIpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39a0a9ed9176811461b56ecb45eb395fa9567aef1a29bd47307cb3b1bb1fe02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6426aa1631516d4fe880fc7c5806c10b59547cb9f5be13536bc26380f0c427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394d95f26e41d425dc4a63b15a2cc8b79e4dac66047b8de8ca2b6b8342865a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53fcb41c06e61f4b74432833b6058e76fd315cf185d58b100e1e7a4d6a9f5b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkIsolatedV2StaticIpPool]],
) -> None:
    """Type checking stubs"""
    pass
