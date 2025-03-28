'''
# `vcd_nsxt_network_dhcp_binding`

Refer to the Terraform Registry for docs: [`vcd_nsxt_network_dhcp_binding`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding).
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


class NsxtNetworkDhcpBinding(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtNetworkDhcpBinding.NsxtNetworkDhcpBinding",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding vcd_nsxt_network_dhcp_binding}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        binding_type: builtins.str,
        ip_address: builtins.str,
        lease_time: jsii.Number,
        mac_address: builtins.str,
        name: builtins.str,
        org_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dhcp_v4_config: typing.Optional[typing.Union["NsxtNetworkDhcpBindingDhcpV4Config", typing.Dict[builtins.str, typing.Any]]] = None,
        dhcp_v6_config: typing.Optional[typing.Union["NsxtNetworkDhcpBindingDhcpV6Config", typing.Dict[builtins.str, typing.Any]]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding vcd_nsxt_network_dhcp_binding} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param binding_type: Binding type 'IPV4' or 'IPV6'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#binding_type NsxtNetworkDhcpBinding#binding_type}
        :param ip_address: IP address of the DHCP binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#ip_address NsxtNetworkDhcpBinding#ip_address}
        :param lease_time: Lease time in seconds. Minimum value is 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#lease_time NsxtNetworkDhcpBinding#lease_time}
        :param mac_address: MAC address of the DHCP binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#mac_address NsxtNetworkDhcpBinding#mac_address}
        :param name: Name of DHCP binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#name NsxtNetworkDhcpBinding#name}
        :param org_network_id: Parent Org VDC network ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#org_network_id NsxtNetworkDhcpBinding#org_network_id}
        :param description: Description of DHCP binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#description NsxtNetworkDhcpBinding#description}
        :param dhcp_v4_config: dhcp_v4_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dhcp_v4_config NsxtNetworkDhcpBinding#dhcp_v4_config}
        :param dhcp_v6_config: dhcp_v6_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dhcp_v6_config NsxtNetworkDhcpBinding#dhcp_v6_config}
        :param dns_servers: The DNS server IPs to be assigned . 2 values maximum. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dns_servers NsxtNetworkDhcpBinding#dns_servers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#id NsxtNetworkDhcpBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#org NsxtNetworkDhcpBinding#org}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87721750ba7bf54126e666bff481a08b3a71fd238326b69b49738fc6b6307151)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtNetworkDhcpBindingConfig(
            binding_type=binding_type,
            ip_address=ip_address,
            lease_time=lease_time,
            mac_address=mac_address,
            name=name,
            org_network_id=org_network_id,
            description=description,
            dhcp_v4_config=dhcp_v4_config,
            dhcp_v6_config=dhcp_v6_config,
            dns_servers=dns_servers,
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
        '''Generates CDKTF code for importing a NsxtNetworkDhcpBinding resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtNetworkDhcpBinding to import.
        :param import_from_id: The id of the existing NsxtNetworkDhcpBinding that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtNetworkDhcpBinding to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66883ee1e5ac67d3dfd0cc538e5f727bbb5652bef016b3eca72584a073c2bc9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDhcpV4Config")
    def put_dhcp_v4_config(
        self,
        *,
        gateway_ip_address: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway_ip_address: IPv4 gateway address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#gateway_ip_address NsxtNetworkDhcpBinding#gateway_ip_address}
        :param hostname: Hostname for the DHCP client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#hostname NsxtNetworkDhcpBinding#hostname}
        '''
        value = NsxtNetworkDhcpBindingDhcpV4Config(
            gateway_ip_address=gateway_ip_address, hostname=hostname
        )

        return typing.cast(None, jsii.invoke(self, "putDhcpV4Config", [value]))

    @jsii.member(jsii_name="putDhcpV6Config")
    def put_dhcp_v6_config(
        self,
        *,
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        sntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param domain_names: Set of domain names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#domain_names NsxtNetworkDhcpBinding#domain_names}
        :param sntp_servers: Set of SNTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#sntp_servers NsxtNetworkDhcpBinding#sntp_servers}
        '''
        value = NsxtNetworkDhcpBindingDhcpV6Config(
            domain_names=domain_names, sntp_servers=sntp_servers
        )

        return typing.cast(None, jsii.invoke(self, "putDhcpV6Config", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDhcpV4Config")
    def reset_dhcp_v4_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcpV4Config", []))

    @jsii.member(jsii_name="resetDhcpV6Config")
    def reset_dhcp_v6_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcpV6Config", []))

    @jsii.member(jsii_name="resetDnsServers")
    def reset_dns_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServers", []))

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
    @jsii.member(jsii_name="dhcpV4Config")
    def dhcp_v4_config(self) -> "NsxtNetworkDhcpBindingDhcpV4ConfigOutputReference":
        return typing.cast("NsxtNetworkDhcpBindingDhcpV4ConfigOutputReference", jsii.get(self, "dhcpV4Config"))

    @builtins.property
    @jsii.member(jsii_name="dhcpV6Config")
    def dhcp_v6_config(self) -> "NsxtNetworkDhcpBindingDhcpV6ConfigOutputReference":
        return typing.cast("NsxtNetworkDhcpBindingDhcpV6ConfigOutputReference", jsii.get(self, "dhcpV6Config"))

    @builtins.property
    @jsii.member(jsii_name="bindingTypeInput")
    def binding_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bindingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpV4ConfigInput")
    def dhcp_v4_config_input(
        self,
    ) -> typing.Optional["NsxtNetworkDhcpBindingDhcpV4Config"]:
        return typing.cast(typing.Optional["NsxtNetworkDhcpBindingDhcpV4Config"], jsii.get(self, "dhcpV4ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpV6ConfigInput")
    def dhcp_v6_config_input(
        self,
    ) -> typing.Optional["NsxtNetworkDhcpBindingDhcpV6Config"]:
        return typing.cast(typing.Optional["NsxtNetworkDhcpBindingDhcpV6Config"], jsii.get(self, "dhcpV6ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServersInput")
    def dns_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsServersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="leaseTimeInput")
    def lease_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "leaseTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="macAddressInput")
    def mac_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="orgNetworkIdInput")
    def org_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bindingType")
    def binding_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bindingType"))

    @binding_type.setter
    def binding_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c531c1e3b7822bd637bfddcb736efd6547a4b84243c9ca370d05546d2a4695d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bindingType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b26f2f11a4dfc570010bf89a16ca3b32d20cfcde65b01252838fa208d0b81b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24861ba6204d3af8a5832a7f08a3ee5b283ab973cf6273fa5eec11460561b8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc218991f108bde408b74a3edb3c75448f2fd09e68d73450df7914dedf73f4bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea3a5f15af41be10adc11cca1cd6ba179d7bf6ef80ca6d0ee61200141122188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="leaseTime")
    def lease_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "leaseTime"))

    @lease_time.setter
    def lease_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fab4f44da05d9ab4ae9037de99a82bf747191cd1a468d37ccefdf111262de7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leaseTime", value)

    @builtins.property
    @jsii.member(jsii_name="macAddress")
    def mac_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macAddress"))

    @mac_address.setter
    def mac_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca05997f12837f8a8e7824fa4f06dd9e247f7ad92895d296312f47a23908c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macAddress", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80f3d4f5e1990c9d2d3a0178b6c5873d8ceae0faaa2834e1c4314f886a9edb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab9622712dae55a933b7d95b04ce9941c3a23646dd1cef9272ad4a3b6a98cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="orgNetworkId")
    def org_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgNetworkId"))

    @org_network_id.setter
    def org_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e10430ae165966727992346fee0d821d2d74d21bd2011b527e5b85f03bd1f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgNetworkId", value)


@jsii.data_type(
    jsii_type="vcd.nsxtNetworkDhcpBinding.NsxtNetworkDhcpBindingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "binding_type": "bindingType",
        "ip_address": "ipAddress",
        "lease_time": "leaseTime",
        "mac_address": "macAddress",
        "name": "name",
        "org_network_id": "orgNetworkId",
        "description": "description",
        "dhcp_v4_config": "dhcpV4Config",
        "dhcp_v6_config": "dhcpV6Config",
        "dns_servers": "dnsServers",
        "id": "id",
        "org": "org",
    },
)
class NsxtNetworkDhcpBindingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        binding_type: builtins.str,
        ip_address: builtins.str,
        lease_time: jsii.Number,
        mac_address: builtins.str,
        name: builtins.str,
        org_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dhcp_v4_config: typing.Optional[typing.Union["NsxtNetworkDhcpBindingDhcpV4Config", typing.Dict[builtins.str, typing.Any]]] = None,
        dhcp_v6_config: typing.Optional[typing.Union["NsxtNetworkDhcpBindingDhcpV6Config", typing.Dict[builtins.str, typing.Any]]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        :param binding_type: Binding type 'IPV4' or 'IPV6'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#binding_type NsxtNetworkDhcpBinding#binding_type}
        :param ip_address: IP address of the DHCP binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#ip_address NsxtNetworkDhcpBinding#ip_address}
        :param lease_time: Lease time in seconds. Minimum value is 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#lease_time NsxtNetworkDhcpBinding#lease_time}
        :param mac_address: MAC address of the DHCP binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#mac_address NsxtNetworkDhcpBinding#mac_address}
        :param name: Name of DHCP binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#name NsxtNetworkDhcpBinding#name}
        :param org_network_id: Parent Org VDC network ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#org_network_id NsxtNetworkDhcpBinding#org_network_id}
        :param description: Description of DHCP binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#description NsxtNetworkDhcpBinding#description}
        :param dhcp_v4_config: dhcp_v4_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dhcp_v4_config NsxtNetworkDhcpBinding#dhcp_v4_config}
        :param dhcp_v6_config: dhcp_v6_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dhcp_v6_config NsxtNetworkDhcpBinding#dhcp_v6_config}
        :param dns_servers: The DNS server IPs to be assigned . 2 values maximum. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dns_servers NsxtNetworkDhcpBinding#dns_servers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#id NsxtNetworkDhcpBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#org NsxtNetworkDhcpBinding#org}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dhcp_v4_config, dict):
            dhcp_v4_config = NsxtNetworkDhcpBindingDhcpV4Config(**dhcp_v4_config)
        if isinstance(dhcp_v6_config, dict):
            dhcp_v6_config = NsxtNetworkDhcpBindingDhcpV6Config(**dhcp_v6_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b833ba173b4cfa3dfa81e8f6afc45287ea5d966c68ebf8db93123749d7dbb8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument binding_type", value=binding_type, expected_type=type_hints["binding_type"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument lease_time", value=lease_time, expected_type=type_hints["lease_time"])
            check_type(argname="argument mac_address", value=mac_address, expected_type=type_hints["mac_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument org_network_id", value=org_network_id, expected_type=type_hints["org_network_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dhcp_v4_config", value=dhcp_v4_config, expected_type=type_hints["dhcp_v4_config"])
            check_type(argname="argument dhcp_v6_config", value=dhcp_v6_config, expected_type=type_hints["dhcp_v6_config"])
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "binding_type": binding_type,
            "ip_address": ip_address,
            "lease_time": lease_time,
            "mac_address": mac_address,
            "name": name,
            "org_network_id": org_network_id,
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
        if dhcp_v4_config is not None:
            self._values["dhcp_v4_config"] = dhcp_v4_config
        if dhcp_v6_config is not None:
            self._values["dhcp_v6_config"] = dhcp_v6_config
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
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
    def binding_type(self) -> builtins.str:
        '''Binding type 'IPV4' or 'IPV6'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#binding_type NsxtNetworkDhcpBinding#binding_type}
        '''
        result = self._values.get("binding_type")
        assert result is not None, "Required property 'binding_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''IP address of the DHCP binding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#ip_address NsxtNetworkDhcpBinding#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lease_time(self) -> jsii.Number:
        '''Lease time in seconds. Minimum value is 60 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#lease_time NsxtNetworkDhcpBinding#lease_time}
        '''
        result = self._values.get("lease_time")
        assert result is not None, "Required property 'lease_time' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def mac_address(self) -> builtins.str:
        '''MAC address of the DHCP binding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#mac_address NsxtNetworkDhcpBinding#mac_address}
        '''
        result = self._values.get("mac_address")
        assert result is not None, "Required property 'mac_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of DHCP binding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#name NsxtNetworkDhcpBinding#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_network_id(self) -> builtins.str:
        '''Parent Org VDC network ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#org_network_id NsxtNetworkDhcpBinding#org_network_id}
        '''
        result = self._values.get("org_network_id")
        assert result is not None, "Required property 'org_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of DHCP binding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#description NsxtNetworkDhcpBinding#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dhcp_v4_config(self) -> typing.Optional["NsxtNetworkDhcpBindingDhcpV4Config"]:
        '''dhcp_v4_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dhcp_v4_config NsxtNetworkDhcpBinding#dhcp_v4_config}
        '''
        result = self._values.get("dhcp_v4_config")
        return typing.cast(typing.Optional["NsxtNetworkDhcpBindingDhcpV4Config"], result)

    @builtins.property
    def dhcp_v6_config(self) -> typing.Optional["NsxtNetworkDhcpBindingDhcpV6Config"]:
        '''dhcp_v6_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dhcp_v6_config NsxtNetworkDhcpBinding#dhcp_v6_config}
        '''
        result = self._values.get("dhcp_v6_config")
        return typing.cast(typing.Optional["NsxtNetworkDhcpBindingDhcpV6Config"], result)

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The DNS server IPs to be assigned . 2 values maximum.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#dns_servers NsxtNetworkDhcpBinding#dns_servers}
        '''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#id NsxtNetworkDhcpBinding#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#org NsxtNetworkDhcpBinding#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtNetworkDhcpBindingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtNetworkDhcpBinding.NsxtNetworkDhcpBindingDhcpV4Config",
    jsii_struct_bases=[],
    name_mapping={"gateway_ip_address": "gatewayIpAddress", "hostname": "hostname"},
)
class NsxtNetworkDhcpBindingDhcpV4Config:
    def __init__(
        self,
        *,
        gateway_ip_address: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway_ip_address: IPv4 gateway address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#gateway_ip_address NsxtNetworkDhcpBinding#gateway_ip_address}
        :param hostname: Hostname for the DHCP client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#hostname NsxtNetworkDhcpBinding#hostname}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f7b7952a38130bd30451cdb8153afd994f3dc89f2fa41c2350656448b8c2b0)
            check_type(argname="argument gateway_ip_address", value=gateway_ip_address, expected_type=type_hints["gateway_ip_address"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway_ip_address is not None:
            self._values["gateway_ip_address"] = gateway_ip_address
        if hostname is not None:
            self._values["hostname"] = hostname

    @builtins.property
    def gateway_ip_address(self) -> typing.Optional[builtins.str]:
        '''IPv4 gateway address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#gateway_ip_address NsxtNetworkDhcpBinding#gateway_ip_address}
        '''
        result = self._values.get("gateway_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname for the DHCP client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#hostname NsxtNetworkDhcpBinding#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtNetworkDhcpBindingDhcpV4Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtNetworkDhcpBindingDhcpV4ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtNetworkDhcpBinding.NsxtNetworkDhcpBindingDhcpV4ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76788c70476bf45556e63dc14f8f0924619401998b56e66f50246c73c7b7bbf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGatewayIpAddress")
    def reset_gateway_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayIpAddress", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpAddressInput")
    def gateway_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpAddress")
    def gateway_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayIpAddress"))

    @gateway_ip_address.setter
    def gateway_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa18c8ca1536e0ce4ecd6a3387d6514c4c36d3de8492ebf167f07002051957b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d8853ef4244a37a4e7f9eb401d95472ba48b211c94f1109d8c35d0f93aef76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NsxtNetworkDhcpBindingDhcpV4Config]:
        return typing.cast(typing.Optional[NsxtNetworkDhcpBindingDhcpV4Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtNetworkDhcpBindingDhcpV4Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbb6a465a128a279d2ed80c1ed617e996242f1a8e6fb7892fdece387232b0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtNetworkDhcpBinding.NsxtNetworkDhcpBindingDhcpV6Config",
    jsii_struct_bases=[],
    name_mapping={"domain_names": "domainNames", "sntp_servers": "sntpServers"},
)
class NsxtNetworkDhcpBindingDhcpV6Config:
    def __init__(
        self,
        *,
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        sntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param domain_names: Set of domain names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#domain_names NsxtNetworkDhcpBinding#domain_names}
        :param sntp_servers: Set of SNTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#sntp_servers NsxtNetworkDhcpBinding#sntp_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70bd06e1c43b8397d2607bb76c53c7b876a24b75fa47e1899b8c3bb6d7616ac4)
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            check_type(argname="argument sntp_servers", value=sntp_servers, expected_type=type_hints["sntp_servers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_names is not None:
            self._values["domain_names"] = domain_names
        if sntp_servers is not None:
            self._values["sntp_servers"] = sntp_servers

    @builtins.property
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of domain names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#domain_names NsxtNetworkDhcpBinding#domain_names}
        '''
        result = self._values.get("domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sntp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of SNTP servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_dhcp_binding#sntp_servers NsxtNetworkDhcpBinding#sntp_servers}
        '''
        result = self._values.get("sntp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtNetworkDhcpBindingDhcpV6Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtNetworkDhcpBindingDhcpV6ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtNetworkDhcpBinding.NsxtNetworkDhcpBindingDhcpV6ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eccbf6e0e266e2a92bc229c64ccd7396c5db98edcbe543445587104eb1103084)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDomainNames")
    def reset_domain_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainNames", []))

    @jsii.member(jsii_name="resetSntpServers")
    def reset_sntp_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSntpServers", []))

    @builtins.property
    @jsii.member(jsii_name="domainNamesInput")
    def domain_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="sntpServersInput")
    def sntp_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sntpServersInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNames")
    def domain_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainNames"))

    @domain_names.setter
    def domain_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ab2e999b5fea40ed6a3907c9533d78b5761fcb4872787b56c29ce8ef9d68c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNames", value)

    @builtins.property
    @jsii.member(jsii_name="sntpServers")
    def sntp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sntpServers"))

    @sntp_servers.setter
    def sntp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eec94bb0d7d9fc7d860d321f834da33a8f511a6710f55537b107bd777a298c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sntpServers", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NsxtNetworkDhcpBindingDhcpV6Config]:
        return typing.cast(typing.Optional[NsxtNetworkDhcpBindingDhcpV6Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtNetworkDhcpBindingDhcpV6Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e1230dadc1a199a9eb9de50b0beb096c210ee77b835b030c1815c678c3624c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtNetworkDhcpBinding",
    "NsxtNetworkDhcpBindingConfig",
    "NsxtNetworkDhcpBindingDhcpV4Config",
    "NsxtNetworkDhcpBindingDhcpV4ConfigOutputReference",
    "NsxtNetworkDhcpBindingDhcpV6Config",
    "NsxtNetworkDhcpBindingDhcpV6ConfigOutputReference",
]

publication.publish()

def _typecheckingstub__87721750ba7bf54126e666bff481a08b3a71fd238326b69b49738fc6b6307151(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    binding_type: builtins.str,
    ip_address: builtins.str,
    lease_time: jsii.Number,
    mac_address: builtins.str,
    name: builtins.str,
    org_network_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dhcp_v4_config: typing.Optional[typing.Union[NsxtNetworkDhcpBindingDhcpV4Config, typing.Dict[builtins.str, typing.Any]]] = None,
    dhcp_v6_config: typing.Optional[typing.Union[NsxtNetworkDhcpBindingDhcpV6Config, typing.Dict[builtins.str, typing.Any]]] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__e66883ee1e5ac67d3dfd0cc538e5f727bbb5652bef016b3eca72584a073c2bc9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c531c1e3b7822bd637bfddcb736efd6547a4b84243c9ca370d05546d2a4695d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b26f2f11a4dfc570010bf89a16ca3b32d20cfcde65b01252838fa208d0b81b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24861ba6204d3af8a5832a7f08a3ee5b283ab973cf6273fa5eec11460561b8e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc218991f108bde408b74a3edb3c75448f2fd09e68d73450df7914dedf73f4bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea3a5f15af41be10adc11cca1cd6ba179d7bf6ef80ca6d0ee61200141122188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fab4f44da05d9ab4ae9037de99a82bf747191cd1a468d37ccefdf111262de7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca05997f12837f8a8e7824fa4f06dd9e247f7ad92895d296312f47a23908c06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80f3d4f5e1990c9d2d3a0178b6c5873d8ceae0faaa2834e1c4314f886a9edb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab9622712dae55a933b7d95b04ce9941c3a23646dd1cef9272ad4a3b6a98cc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e10430ae165966727992346fee0d821d2d74d21bd2011b527e5b85f03bd1f2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b833ba173b4cfa3dfa81e8f6afc45287ea5d966c68ebf8db93123749d7dbb8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    binding_type: builtins.str,
    ip_address: builtins.str,
    lease_time: jsii.Number,
    mac_address: builtins.str,
    name: builtins.str,
    org_network_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dhcp_v4_config: typing.Optional[typing.Union[NsxtNetworkDhcpBindingDhcpV4Config, typing.Dict[builtins.str, typing.Any]]] = None,
    dhcp_v6_config: typing.Optional[typing.Union[NsxtNetworkDhcpBindingDhcpV6Config, typing.Dict[builtins.str, typing.Any]]] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f7b7952a38130bd30451cdb8153afd994f3dc89f2fa41c2350656448b8c2b0(
    *,
    gateway_ip_address: typing.Optional[builtins.str] = None,
    hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76788c70476bf45556e63dc14f8f0924619401998b56e66f50246c73c7b7bbf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa18c8ca1536e0ce4ecd6a3387d6514c4c36d3de8492ebf167f07002051957b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d8853ef4244a37a4e7f9eb401d95472ba48b211c94f1109d8c35d0f93aef76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbb6a465a128a279d2ed80c1ed617e996242f1a8e6fb7892fdece387232b0af(
    value: typing.Optional[NsxtNetworkDhcpBindingDhcpV4Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70bd06e1c43b8397d2607bb76c53c7b876a24b75fa47e1899b8c3bb6d7616ac4(
    *,
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    sntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccbf6e0e266e2a92bc229c64ccd7396c5db98edcbe543445587104eb1103084(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ab2e999b5fea40ed6a3907c9533d78b5761fcb4872787b56c29ce8ef9d68c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eec94bb0d7d9fc7d860d321f834da33a8f511a6710f55537b107bd777a298c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e1230dadc1a199a9eb9de50b0beb096c210ee77b835b030c1815c678c3624c(
    value: typing.Optional[NsxtNetworkDhcpBindingDhcpV6Config],
) -> None:
    """Type checking stubs"""
    pass
