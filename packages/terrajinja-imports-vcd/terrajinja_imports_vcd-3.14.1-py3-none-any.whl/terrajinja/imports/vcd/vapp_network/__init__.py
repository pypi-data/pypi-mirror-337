'''
# `vcd_vapp_network`

Refer to the Terraform Registry for docs: [`vcd_vapp_network`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network).
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


class VappNetwork(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappNetwork.VappNetwork",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network vcd_vapp_network}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        gateway: builtins.str,
        name: builtins.str,
        vapp_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNetworkDhcpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        guest_vlan_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        netmask: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        org_network_name: typing.Optional[builtins.str] = None,
        prefix_length: typing.Optional[builtins.str] = None,
        reboot_vapp_on_removal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retain_ip_mac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNetworkStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network vcd_vapp_network} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param gateway: Gateway of the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#gateway VappNetwork#gateway}
        :param name: vApp network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#name VappNetwork#name}
        :param vapp_name: vApp to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#vapp_name VappNetwork#vapp_name}
        :param description: Optional description for the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#description VappNetwork#description}
        :param dhcp_pool: dhcp_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dhcp_pool VappNetwork#dhcp_pool}
        :param dns1: Primary DNS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns1 VappNetwork#dns1}
        :param dns2: Secondary DNS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns2 VappNetwork#dns2}
        :param dns_suffix: DNS suffix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns_suffix VappNetwork#dns_suffix}
        :param guest_vlan_allowed: True if Network allows guest VLAN tagging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#guest_vlan_allowed VappNetwork#guest_vlan_allowed}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#id VappNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param netmask: Netmask address for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#netmask VappNetwork#netmask}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#org VappNetwork#org}
        :param org_network_name: org network name to which vapp network is connected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#org_network_name VappNetwork#org_network_name}
        :param prefix_length: Prefix length for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#prefix_length VappNetwork#prefix_length}
        :param reboot_vapp_on_removal: Specifies whether the vApp should be rebooted when the vApp network is removed. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#reboot_vapp_on_removal VappNetwork#reboot_vapp_on_removal}
        :param retain_ip_mac_enabled: Specifies whether the network resources such as IP/MAC of router will be retained across deployments. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#retain_ip_mac_enabled VappNetwork#retain_ip_mac_enabled}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#static_ip_pool VappNetwork#static_ip_pool}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#vdc VappNetwork#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f248d929ff91399934bba394434ad89f014850f91ed0184acc3d005bc01916)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VappNetworkConfig(
            gateway=gateway,
            name=name,
            vapp_name=vapp_name,
            description=description,
            dhcp_pool=dhcp_pool,
            dns1=dns1,
            dns2=dns2,
            dns_suffix=dns_suffix,
            guest_vlan_allowed=guest_vlan_allowed,
            id=id,
            netmask=netmask,
            org=org,
            org_network_name=org_network_name,
            prefix_length=prefix_length,
            reboot_vapp_on_removal=reboot_vapp_on_removal,
            retain_ip_mac_enabled=retain_ip_mac_enabled,
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
        '''Generates CDKTF code for importing a VappNetwork resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VappNetwork to import.
        :param import_from_id: The id of the existing VappNetwork that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VappNetwork to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a818194c9f282bf3ebe40c3c5630f8736b664f431f959d0b3cce3e62ceaf163)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDhcpPool")
    def put_dhcp_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNetworkDhcpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5982dcf2e740f25b116f5a65ec66c2b172d725c65450de6fa2a96947975b25e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDhcpPool", [value]))

    @jsii.member(jsii_name="putStaticIpPool")
    def put_static_ip_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNetworkStaticIpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b4b07229e2f3c74b87fbce0f8267b95aebde12df0501a975984c5abbd82fe2)
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

    @jsii.member(jsii_name="resetGuestVlanAllowed")
    def reset_guest_vlan_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestVlanAllowed", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetmask")
    def reset_netmask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetmask", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOrgNetworkName")
    def reset_org_network_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgNetworkName", []))

    @jsii.member(jsii_name="resetPrefixLength")
    def reset_prefix_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixLength", []))

    @jsii.member(jsii_name="resetRebootVappOnRemoval")
    def reset_reboot_vapp_on_removal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRebootVappOnRemoval", []))

    @jsii.member(jsii_name="resetRetainIpMacEnabled")
    def reset_retain_ip_mac_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainIpMacEnabled", []))

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
    def dhcp_pool(self) -> "VappNetworkDhcpPoolList":
        return typing.cast("VappNetworkDhcpPoolList", jsii.get(self, "dhcpPool"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPool")
    def static_ip_pool(self) -> "VappNetworkStaticIpPoolList":
        return typing.cast("VappNetworkStaticIpPoolList", jsii.get(self, "staticIpPool"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpPoolInput")
    def dhcp_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNetworkDhcpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNetworkDhcpPool"]]], jsii.get(self, "dhcpPoolInput"))

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
    @jsii.member(jsii_name="orgNetworkNameInput")
    def org_network_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgNetworkNameInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="rebootVappOnRemovalInput")
    def reboot_vapp_on_removal_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rebootVappOnRemovalInput"))

    @builtins.property
    @jsii.member(jsii_name="retainIpMacEnabledInput")
    def retain_ip_mac_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retainIpMacEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPoolInput")
    def static_ip_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNetworkStaticIpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNetworkStaticIpPool"]]], jsii.get(self, "staticIpPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="vappNameInput")
    def vapp_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vappNameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7df509edc610bd6ad63413c2b76486f9c60fa00c82a72968654bb7c028e976d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="dns1")
    def dns1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns1"))

    @dns1.setter
    def dns1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6635dfbbdc5179191702179da655c86dfffd45f3aa61f3462537290030a9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns1", value)

    @builtins.property
    @jsii.member(jsii_name="dns2")
    def dns2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns2"))

    @dns2.setter
    def dns2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad9f9d639f9b38c34146afce01ec1054c782ac5a0d8f4d9f17e76d3e294b831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns2", value)

    @builtins.property
    @jsii.member(jsii_name="dnsSuffix")
    def dns_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsSuffix"))

    @dns_suffix.setter
    def dns_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656723efecee902b1aeebf66ede1ae5649d6752f9e97c6a59b019ecf4d24467a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f93635b34f97efe498ff325bfa25101a348f0b9835dfa2e3ef2bb28e8c06c4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b63be30be269601ebcaab2efb3faa5c6d62daf8b5dcd4fa01f00aecb0abe4385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestVlanAllowed", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52decdbc2270a517b52eb3b951b48a244cc0052340b4e823542429b86c51af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfff54cc85150e502f87d5b34d7e3614b4b1140f7f932344ff1fc9354bd9805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e7bbb0c86844f192bd133581435e8be47f4ed88ae95b89f846050e7deaeb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39298103f565ba9e027a72d1bcb609ec5a1d93342415a7ad90293fa15eb7303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="orgNetworkName")
    def org_network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgNetworkName"))

    @org_network_name.setter
    def org_network_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ba560a24923a0fd62c4b44a42d9eea5e559d703ea38026f44ed7f3fbb9430c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgNetworkName", value)

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1076495ece8ce94938503ba74db042e0613a192d06ce06bff5ea7b96b5cd9c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="rebootVappOnRemoval")
    def reboot_vapp_on_removal(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rebootVappOnRemoval"))

    @reboot_vapp_on_removal.setter
    def reboot_vapp_on_removal(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73cba45438b8bf0d8a875330b44c2b61725e3b8ba29355239f549425f9c4e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rebootVappOnRemoval", value)

    @builtins.property
    @jsii.member(jsii_name="retainIpMacEnabled")
    def retain_ip_mac_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retainIpMacEnabled"))

    @retain_ip_mac_enabled.setter
    def retain_ip_mac_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c362a5f2cdf1771d323d7cc2b636bf628a1e0f9461c8138416463aae5545218b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainIpMacEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vappName")
    def vapp_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappName"))

    @vapp_name.setter
    def vapp_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c70edfe25d3cebb832efeb221dc919ade19d68cc7b2a4fb5b00345f66272eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappName", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e89450801cc6b9ea984a368e09db3df248ac1fb1b5290b564c015b7a988ddb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.vappNetwork.VappNetworkConfig",
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
        "vapp_name": "vappName",
        "description": "description",
        "dhcp_pool": "dhcpPool",
        "dns1": "dns1",
        "dns2": "dns2",
        "dns_suffix": "dnsSuffix",
        "guest_vlan_allowed": "guestVlanAllowed",
        "id": "id",
        "netmask": "netmask",
        "org": "org",
        "org_network_name": "orgNetworkName",
        "prefix_length": "prefixLength",
        "reboot_vapp_on_removal": "rebootVappOnRemoval",
        "retain_ip_mac_enabled": "retainIpMacEnabled",
        "static_ip_pool": "staticIpPool",
        "vdc": "vdc",
    },
)
class VappNetworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        vapp_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNetworkDhcpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        guest_vlan_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        netmask: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        org_network_name: typing.Optional[builtins.str] = None,
        prefix_length: typing.Optional[builtins.str] = None,
        reboot_vapp_on_removal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retain_ip_mac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappNetworkStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param gateway: Gateway of the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#gateway VappNetwork#gateway}
        :param name: vApp network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#name VappNetwork#name}
        :param vapp_name: vApp to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#vapp_name VappNetwork#vapp_name}
        :param description: Optional description for the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#description VappNetwork#description}
        :param dhcp_pool: dhcp_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dhcp_pool VappNetwork#dhcp_pool}
        :param dns1: Primary DNS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns1 VappNetwork#dns1}
        :param dns2: Secondary DNS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns2 VappNetwork#dns2}
        :param dns_suffix: DNS suffix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns_suffix VappNetwork#dns_suffix}
        :param guest_vlan_allowed: True if Network allows guest VLAN tagging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#guest_vlan_allowed VappNetwork#guest_vlan_allowed}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#id VappNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param netmask: Netmask address for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#netmask VappNetwork#netmask}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#org VappNetwork#org}
        :param org_network_name: org network name to which vapp network is connected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#org_network_name VappNetwork#org_network_name}
        :param prefix_length: Prefix length for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#prefix_length VappNetwork#prefix_length}
        :param reboot_vapp_on_removal: Specifies whether the vApp should be rebooted when the vApp network is removed. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#reboot_vapp_on_removal VappNetwork#reboot_vapp_on_removal}
        :param retain_ip_mac_enabled: Specifies whether the network resources such as IP/MAC of router will be retained across deployments. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#retain_ip_mac_enabled VappNetwork#retain_ip_mac_enabled}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#static_ip_pool VappNetwork#static_ip_pool}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#vdc VappNetwork#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae60f025fb25ddaf839be692fda6dc86c0f8ae375d3c27b3023f4dc18636dbd3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vapp_name", value=vapp_name, expected_type=type_hints["vapp_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dhcp_pool", value=dhcp_pool, expected_type=type_hints["dhcp_pool"])
            check_type(argname="argument dns1", value=dns1, expected_type=type_hints["dns1"])
            check_type(argname="argument dns2", value=dns2, expected_type=type_hints["dns2"])
            check_type(argname="argument dns_suffix", value=dns_suffix, expected_type=type_hints["dns_suffix"])
            check_type(argname="argument guest_vlan_allowed", value=guest_vlan_allowed, expected_type=type_hints["guest_vlan_allowed"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument org_network_name", value=org_network_name, expected_type=type_hints["org_network_name"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
            check_type(argname="argument reboot_vapp_on_removal", value=reboot_vapp_on_removal, expected_type=type_hints["reboot_vapp_on_removal"])
            check_type(argname="argument retain_ip_mac_enabled", value=retain_ip_mac_enabled, expected_type=type_hints["retain_ip_mac_enabled"])
            check_type(argname="argument static_ip_pool", value=static_ip_pool, expected_type=type_hints["static_ip_pool"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway": gateway,
            "name": name,
            "vapp_name": vapp_name,
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
        if guest_vlan_allowed is not None:
            self._values["guest_vlan_allowed"] = guest_vlan_allowed
        if id is not None:
            self._values["id"] = id
        if netmask is not None:
            self._values["netmask"] = netmask
        if org is not None:
            self._values["org"] = org
        if org_network_name is not None:
            self._values["org_network_name"] = org_network_name
        if prefix_length is not None:
            self._values["prefix_length"] = prefix_length
        if reboot_vapp_on_removal is not None:
            self._values["reboot_vapp_on_removal"] = reboot_vapp_on_removal
        if retain_ip_mac_enabled is not None:
            self._values["retain_ip_mac_enabled"] = retain_ip_mac_enabled
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
        '''Gateway of the network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#gateway VappNetwork#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''vApp network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#name VappNetwork#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vapp_name(self) -> builtins.str:
        '''vApp to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#vapp_name VappNetwork#vapp_name}
        '''
        result = self._values.get("vapp_name")
        assert result is not None, "Required property 'vapp_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional description for the network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#description VappNetwork#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dhcp_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNetworkDhcpPool"]]]:
        '''dhcp_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dhcp_pool VappNetwork#dhcp_pool}
        '''
        result = self._values.get("dhcp_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNetworkDhcpPool"]]], result)

    @builtins.property
    def dns1(self) -> typing.Optional[builtins.str]:
        '''Primary DNS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns1 VappNetwork#dns1}
        '''
        result = self._values.get("dns1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns2(self) -> typing.Optional[builtins.str]:
        '''Secondary DNS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns2 VappNetwork#dns2}
        '''
        result = self._values.get("dns2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_suffix(self) -> typing.Optional[builtins.str]:
        '''DNS suffix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#dns_suffix VappNetwork#dns_suffix}
        '''
        result = self._values.get("dns_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_vlan_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if Network allows guest VLAN tagging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#guest_vlan_allowed VappNetwork#guest_vlan_allowed}
        '''
        result = self._values.get("guest_vlan_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#id VappNetwork#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''Netmask address for a subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#netmask VappNetwork#netmask}
        '''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#org VappNetwork#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org_network_name(self) -> typing.Optional[builtins.str]:
        '''org network name to which vapp network is connected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#org_network_name VappNetwork#org_network_name}
        '''
        result = self._values.get("org_network_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_length(self) -> typing.Optional[builtins.str]:
        '''Prefix length for a subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#prefix_length VappNetwork#prefix_length}
        '''
        result = self._values.get("prefix_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reboot_vapp_on_removal(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the vApp should be rebooted when the vApp network is removed. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#reboot_vapp_on_removal VappNetwork#reboot_vapp_on_removal}
        '''
        result = self._values.get("reboot_vapp_on_removal")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retain_ip_mac_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the network resources such as IP/MAC of router will be retained across deployments. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#retain_ip_mac_enabled VappNetwork#retain_ip_mac_enabled}
        '''
        result = self._values.get("retain_ip_mac_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def static_ip_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNetworkStaticIpPool"]]]:
        '''static_ip_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#static_ip_pool VappNetwork#static_ip_pool}
        '''
        result = self._values.get("static_ip_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappNetworkStaticIpPool"]]], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#vdc VappNetwork#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.vappNetwork.VappNetworkDhcpPool",
    jsii_struct_bases=[],
    name_mapping={
        "start_address": "startAddress",
        "default_lease_time": "defaultLeaseTime",
        "enabled": "enabled",
        "end_address": "endAddress",
        "max_lease_time": "maxLeaseTime",
    },
)
class VappNetworkDhcpPool:
    def __init__(
        self,
        *,
        start_address: builtins.str,
        default_lease_time: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_address: typing.Optional[builtins.str] = None,
        max_lease_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#start_address VappNetwork#start_address}.
        :param default_lease_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#default_lease_time VappNetwork#default_lease_time}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#enabled VappNetwork#enabled}.
        :param end_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#end_address VappNetwork#end_address}.
        :param max_lease_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#max_lease_time VappNetwork#max_lease_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25ad092bd2d54bd9690ef1c42008191511df9c5e7848e44fb5d543fd3c82406)
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
            check_type(argname="argument default_lease_time", value=default_lease_time, expected_type=type_hints["default_lease_time"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument max_lease_time", value=max_lease_time, expected_type=type_hints["max_lease_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_address": start_address,
        }
        if default_lease_time is not None:
            self._values["default_lease_time"] = default_lease_time
        if enabled is not None:
            self._values["enabled"] = enabled
        if end_address is not None:
            self._values["end_address"] = end_address
        if max_lease_time is not None:
            self._values["max_lease_time"] = max_lease_time

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#start_address VappNetwork#start_address}.'''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_lease_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#default_lease_time VappNetwork#default_lease_time}.'''
        result = self._values.get("default_lease_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#enabled VappNetwork#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def end_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#end_address VappNetwork#end_address}.'''
        result = self._values.get("end_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_lease_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#max_lease_time VappNetwork#max_lease_time}.'''
        result = self._values.get("max_lease_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappNetworkDhcpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappNetworkDhcpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappNetwork.VappNetworkDhcpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dbb6df9581b6d14e78867aa3eb74684d5e3c00d9f1b7034a2a2e12b2a77ddfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappNetworkDhcpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4948900a40542b81cabd0e075ad169cda9267dd7090377dcdfa477d3e9322e6f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappNetworkDhcpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5523aa4da9ca2719b1548d6ba77971b11ee0c025a3cc7bf8e4e23cb94ece59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__397735d1926aa65797f7cdc32b244ab38104a499e2db8170c7b7533c65dbdd5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40c3994504f5c3db5b3cae6eaac268b49477bfece86a591a1feb712e6d95102c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNetworkDhcpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNetworkDhcpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNetworkDhcpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3f8b4681d7cb3e69151e7ad706e6c170d7b60f39c77ac1d92b83fd9e6a494a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappNetworkDhcpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappNetwork.VappNetworkDhcpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da31cc9d7e4f72559c1e35cad03f3b06567e0634c4d0b3eb2bd64fcb8197f421)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDefaultLeaseTime")
    def reset_default_lease_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLeaseTime", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEndAddress")
    def reset_end_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndAddress", []))

    @jsii.member(jsii_name="resetMaxLeaseTime")
    def reset_max_lease_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLeaseTime", []))

    @builtins.property
    @jsii.member(jsii_name="defaultLeaseTimeInput")
    def default_lease_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultLeaseTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__53986810e923d3d2c43db7b53f34d84f1f5898394c501f24496f7e2c9c1b7609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLeaseTime", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__b03990a315c8557fe2f2fb3ed7a0657744da1e294dc09934e8263a1f8bfe90be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="endAddress")
    def end_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endAddress"))

    @end_address.setter
    def end_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6526a4c0d6367c8655a336e8b0759a282328822523ed9d47bd0271e1a4f5bad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTime")
    def max_lease_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLeaseTime"))

    @max_lease_time.setter
    def max_lease_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbd8208fc81bf59d029314967fa1793f21ca9998bd240b730b30fbc1e62b88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLeaseTime", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b903770b057ba95526c8eac7e32ea8aba2e3eae468e3a66d7feba7a0e19179e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNetworkDhcpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNetworkDhcpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNetworkDhcpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04ab8e54a617e221087338650a6acd973a2f2dac8a2b8e2a85da1b631b9b10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappNetwork.VappNetworkStaticIpPool",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class VappNetworkStaticIpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#end_address VappNetwork#end_address}.
        :param start_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#start_address VappNetwork#start_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc10aee290f7351b7e4c88d4d1b21d091be844ad8ef5e1da405b256fbb883b82)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#end_address VappNetwork#end_address}.'''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_network#start_address VappNetwork#start_address}.'''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappNetworkStaticIpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappNetworkStaticIpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappNetwork.VappNetworkStaticIpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cb816fb0582764795ab29e03f9c05e04b83b911deb449f7d335c6807d6ea767)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappNetworkStaticIpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900d18cbb466e24da46250e421e351e874700384015018ce4926db53fea02383)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappNetworkStaticIpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c6457bfa6771539611c2bbfaf272b3165ca17d6adf0cf2daaba2e6411f32a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9967d5f8f6c2ec5b720b70a56e1a677f4b17f76e45a2f575259a89f3c4a06c3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afbb49745690653f566240e84366153bb620d10eb1c167ed7c9c5c0ad75caefb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNetworkStaticIpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNetworkStaticIpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNetworkStaticIpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6a86efdf6a95304626963e7fad5272a798ae08adb512fb1ce0f8d13f08b0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappNetworkStaticIpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappNetwork.VappNetworkStaticIpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d02ec838238466d051518dd677487f90e77a4f0bc097f2ab89599efd2c861607)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ceaebddafc4d7e68cfff77f24d9abd529885252a7b6622ea4a1a91611489bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f602360c8e6ebf9511554ca74a0515a9250ad5e6478149be0fae4a34de071584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNetworkStaticIpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNetworkStaticIpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNetworkStaticIpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073e2f93e1126bb330bb855887efb3c9360130963a5fc4dd554c60de809bbd9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VappNetwork",
    "VappNetworkConfig",
    "VappNetworkDhcpPool",
    "VappNetworkDhcpPoolList",
    "VappNetworkDhcpPoolOutputReference",
    "VappNetworkStaticIpPool",
    "VappNetworkStaticIpPoolList",
    "VappNetworkStaticIpPoolOutputReference",
]

publication.publish()

def _typecheckingstub__b9f248d929ff91399934bba394434ad89f014850f91ed0184acc3d005bc01916(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    gateway: builtins.str,
    name: builtins.str,
    vapp_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNetworkDhcpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    guest_vlan_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    netmask: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    org_network_name: typing.Optional[builtins.str] = None,
    prefix_length: typing.Optional[builtins.str] = None,
    reboot_vapp_on_removal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retain_ip_mac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNetworkStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__8a818194c9f282bf3ebe40c3c5630f8736b664f431f959d0b3cce3e62ceaf163(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5982dcf2e740f25b116f5a65ec66c2b172d725c65450de6fa2a96947975b25e3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNetworkDhcpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b4b07229e2f3c74b87fbce0f8267b95aebde12df0501a975984c5abbd82fe2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNetworkStaticIpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df509edc610bd6ad63413c2b76486f9c60fa00c82a72968654bb7c028e976d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6635dfbbdc5179191702179da655c86dfffd45f3aa61f3462537290030a9bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad9f9d639f9b38c34146afce01ec1054c782ac5a0d8f4d9f17e76d3e294b831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656723efecee902b1aeebf66ede1ae5649d6752f9e97c6a59b019ecf4d24467a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f93635b34f97efe498ff325bfa25101a348f0b9835dfa2e3ef2bb28e8c06c4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63be30be269601ebcaab2efb3faa5c6d62daf8b5dcd4fa01f00aecb0abe4385(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52decdbc2270a517b52eb3b951b48a244cc0052340b4e823542429b86c51af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfff54cc85150e502f87d5b34d7e3614b4b1140f7f932344ff1fc9354bd9805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e7bbb0c86844f192bd133581435e8be47f4ed88ae95b89f846050e7deaeb5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39298103f565ba9e027a72d1bcb609ec5a1d93342415a7ad90293fa15eb7303(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ba560a24923a0fd62c4b44a42d9eea5e559d703ea38026f44ed7f3fbb9430c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1076495ece8ce94938503ba74db042e0613a192d06ce06bff5ea7b96b5cd9c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73cba45438b8bf0d8a875330b44c2b61725e3b8ba29355239f549425f9c4e8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c362a5f2cdf1771d323d7cc2b636bf628a1e0f9461c8138416463aae5545218b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c70edfe25d3cebb832efeb221dc919ade19d68cc7b2a4fb5b00345f66272eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e89450801cc6b9ea984a368e09db3df248ac1fb1b5290b564c015b7a988ddb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae60f025fb25ddaf839be692fda6dc86c0f8ae375d3c27b3023f4dc18636dbd3(
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
    vapp_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dhcp_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNetworkDhcpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    guest_vlan_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    netmask: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    org_network_name: typing.Optional[builtins.str] = None,
    prefix_length: typing.Optional[builtins.str] = None,
    reboot_vapp_on_removal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retain_ip_mac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappNetworkStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25ad092bd2d54bd9690ef1c42008191511df9c5e7848e44fb5d543fd3c82406(
    *,
    start_address: builtins.str,
    default_lease_time: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_address: typing.Optional[builtins.str] = None,
    max_lease_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbb6df9581b6d14e78867aa3eb74684d5e3c00d9f1b7034a2a2e12b2a77ddfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4948900a40542b81cabd0e075ad169cda9267dd7090377dcdfa477d3e9322e6f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5523aa4da9ca2719b1548d6ba77971b11ee0c025a3cc7bf8e4e23cb94ece59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397735d1926aa65797f7cdc32b244ab38104a499e2db8170c7b7533c65dbdd5c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c3994504f5c3db5b3cae6eaac268b49477bfece86a591a1feb712e6d95102c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3f8b4681d7cb3e69151e7ad706e6c170d7b60f39c77ac1d92b83fd9e6a494a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNetworkDhcpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da31cc9d7e4f72559c1e35cad03f3b06567e0634c4d0b3eb2bd64fcb8197f421(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53986810e923d3d2c43db7b53f34d84f1f5898394c501f24496f7e2c9c1b7609(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03990a315c8557fe2f2fb3ed7a0657744da1e294dc09934e8263a1f8bfe90be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6526a4c0d6367c8655a336e8b0759a282328822523ed9d47bd0271e1a4f5bad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbd8208fc81bf59d029314967fa1793f21ca9998bd240b730b30fbc1e62b88e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b903770b057ba95526c8eac7e32ea8aba2e3eae468e3a66d7feba7a0e19179e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04ab8e54a617e221087338650a6acd973a2f2dac8a2b8e2a85da1b631b9b10d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNetworkDhcpPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc10aee290f7351b7e4c88d4d1b21d091be844ad8ef5e1da405b256fbb883b82(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb816fb0582764795ab29e03f9c05e04b83b911deb449f7d335c6807d6ea767(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900d18cbb466e24da46250e421e351e874700384015018ce4926db53fea02383(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c6457bfa6771539611c2bbfaf272b3165ca17d6adf0cf2daaba2e6411f32a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9967d5f8f6c2ec5b720b70a56e1a677f4b17f76e45a2f575259a89f3c4a06c3c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbb49745690653f566240e84366153bb620d10eb1c167ed7c9c5c0ad75caefb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6a86efdf6a95304626963e7fad5272a798ae08adb512fb1ce0f8d13f08b0aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappNetworkStaticIpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02ec838238466d051518dd677487f90e77a4f0bc097f2ab89599efd2c861607(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ceaebddafc4d7e68cfff77f24d9abd529885252a7b6622ea4a1a91611489bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f602360c8e6ebf9511554ca74a0515a9250ad5e6478149be0fae4a34de071584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073e2f93e1126bb330bb855887efb3c9360130963a5fc4dd554c60de809bbd9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappNetworkStaticIpPool]],
) -> None:
    """Type checking stubs"""
    pass
