'''
# `vcd_external_network_v2`

Refer to the Terraform Registry for docs: [`vcd_external_network_v2`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2).
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


class ExternalNetworkV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2 vcd_external_network_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        dedicated_org_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalNetworkV2IpScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
        nat_and_firewall_service_intention: typing.Optional[builtins.str] = None,
        nsxt_network: typing.Optional[typing.Union["ExternalNetworkV2NsxtNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        route_advertisement_intention: typing.Optional[builtins.str] = None,
        use_ip_spaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsphere_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalNetworkV2VsphereNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2 vcd_external_network_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#name ExternalNetworkV2#name}
        :param dedicated_org_id: Dedicate this External Network to an Org ID (only with IP Spaces, VCD 10.4.1+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dedicated_org_id ExternalNetworkV2#dedicated_org_id}
        :param description: Network description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#description ExternalNetworkV2#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#id ExternalNetworkV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_scope: ip_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#ip_scope ExternalNetworkV2#ip_scope}
        :param nat_and_firewall_service_intention: Defines intentions to configure NAT and Firewall rules (only with IP Spaces, VCD 10.5.1+) One of ``PROVIDER_GATEWAY``,``EDGE_GATEWAY``,``PROVIDER_AND_EDGE_GATEWAY``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nat_and_firewall_service_intention ExternalNetworkV2#nat_and_firewall_service_intention}
        :param nsxt_network: nsxt_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_network ExternalNetworkV2#nsxt_network}
        :param route_advertisement_intention: Defines intentions to configure route advertisement (only with IP Spaces, VCD 10.5.1+) One of ``IP_SPACE_UPLINKS_ADVERTISED_STRICT``,``IP_SPACE_UPLINKS_ADVERTISED_FLEXIBLE``,``ALL_NETWORKS_ADVERTISED``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#route_advertisement_intention ExternalNetworkV2#route_advertisement_intention}
        :param use_ip_spaces: Enables IP Spaces for this network (default 'false'). VCD 10.4.1+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#use_ip_spaces ExternalNetworkV2#use_ip_spaces}
        :param vsphere_network: vsphere_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#vsphere_network ExternalNetworkV2#vsphere_network}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89fa7fe354484d770380726c97f1b0cd699bd9706aafb56f3929533343b1bcd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ExternalNetworkV2Config(
            name=name,
            dedicated_org_id=dedicated_org_id,
            description=description,
            id=id,
            ip_scope=ip_scope,
            nat_and_firewall_service_intention=nat_and_firewall_service_intention,
            nsxt_network=nsxt_network,
            route_advertisement_intention=route_advertisement_intention,
            use_ip_spaces=use_ip_spaces,
            vsphere_network=vsphere_network,
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
        '''Generates CDKTF code for importing a ExternalNetworkV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExternalNetworkV2 to import.
        :param import_from_id: The id of the existing ExternalNetworkV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExternalNetworkV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a93ac2a548e1a87d1aba3860d3c14e8ebf3acf82d195eb1423d1eb24c8c7acc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIpScope")
    def put_ip_scope(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalNetworkV2IpScope", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dabd71e8da5e350a5d6fb40d615b13f11d17c5a37ec9f7b4bd05a8d83592eb0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpScope", [value]))

    @jsii.member(jsii_name="putNsxtNetwork")
    def put_nsxt_network(
        self,
        *,
        nsxt_manager_id: builtins.str,
        nsxt_segment_name: typing.Optional[builtins.str] = None,
        nsxt_tier0_router_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nsxt_manager_id: ID of NSX-T manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_manager_id ExternalNetworkV2#nsxt_manager_id}
        :param nsxt_segment_name: Name of NSX-T segment (for NSX-T segment backed external network). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_segment_name ExternalNetworkV2#nsxt_segment_name}
        :param nsxt_tier0_router_id: ID of NSX-T Tier-0 router (for T0 gateway backed external network). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_tier0_router_id ExternalNetworkV2#nsxt_tier0_router_id}
        '''
        value = ExternalNetworkV2NsxtNetwork(
            nsxt_manager_id=nsxt_manager_id,
            nsxt_segment_name=nsxt_segment_name,
            nsxt_tier0_router_id=nsxt_tier0_router_id,
        )

        return typing.cast(None, jsii.invoke(self, "putNsxtNetwork", [value]))

    @jsii.member(jsii_name="putVsphereNetwork")
    def put_vsphere_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalNetworkV2VsphereNetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20409ac46318e56ee0ef189d62bdb58bb27678b218f7831624f7ac7582d3ffa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVsphereNetwork", [value]))

    @jsii.member(jsii_name="resetDedicatedOrgId")
    def reset_dedicated_org_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedOrgId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpScope")
    def reset_ip_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpScope", []))

    @jsii.member(jsii_name="resetNatAndFirewallServiceIntention")
    def reset_nat_and_firewall_service_intention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNatAndFirewallServiceIntention", []))

    @jsii.member(jsii_name="resetNsxtNetwork")
    def reset_nsxt_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNsxtNetwork", []))

    @jsii.member(jsii_name="resetRouteAdvertisementIntention")
    def reset_route_advertisement_intention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteAdvertisementIntention", []))

    @jsii.member(jsii_name="resetUseIpSpaces")
    def reset_use_ip_spaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseIpSpaces", []))

    @jsii.member(jsii_name="resetVsphereNetwork")
    def reset_vsphere_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsphereNetwork", []))

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
    @jsii.member(jsii_name="ipScope")
    def ip_scope(self) -> "ExternalNetworkV2IpScopeList":
        return typing.cast("ExternalNetworkV2IpScopeList", jsii.get(self, "ipScope"))

    @builtins.property
    @jsii.member(jsii_name="nsxtNetwork")
    def nsxt_network(self) -> "ExternalNetworkV2NsxtNetworkOutputReference":
        return typing.cast("ExternalNetworkV2NsxtNetworkOutputReference", jsii.get(self, "nsxtNetwork"))

    @builtins.property
    @jsii.member(jsii_name="vsphereNetwork")
    def vsphere_network(self) -> "ExternalNetworkV2VsphereNetworkList":
        return typing.cast("ExternalNetworkV2VsphereNetworkList", jsii.get(self, "vsphereNetwork"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedOrgIdInput")
    def dedicated_org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dedicatedOrgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipScopeInput")
    def ip_scope_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2IpScope"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2IpScope"]]], jsii.get(self, "ipScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="natAndFirewallServiceIntentionInput")
    def nat_and_firewall_service_intention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "natAndFirewallServiceIntentionInput"))

    @builtins.property
    @jsii.member(jsii_name="nsxtNetworkInput")
    def nsxt_network_input(self) -> typing.Optional["ExternalNetworkV2NsxtNetwork"]:
        return typing.cast(typing.Optional["ExternalNetworkV2NsxtNetwork"], jsii.get(self, "nsxtNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="routeAdvertisementIntentionInput")
    def route_advertisement_intention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeAdvertisementIntentionInput"))

    @builtins.property
    @jsii.member(jsii_name="useIpSpacesInput")
    def use_ip_spaces_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useIpSpacesInput"))

    @builtins.property
    @jsii.member(jsii_name="vsphereNetworkInput")
    def vsphere_network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2VsphereNetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2VsphereNetwork"]]], jsii.get(self, "vsphereNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedOrgId")
    def dedicated_org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicatedOrgId"))

    @dedicated_org_id.setter
    def dedicated_org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c443daae4d2a65901fa039f3c03d69cc51dfd8d5cb8d8c3fbacf9e737912a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedOrgId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82242c3320e23eb18309de39e12d387ac743e07a2ee0db975911be8a051cd387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0257c9e5ae4e28624d52bf4788b5c771ccce0cd48b767a9ef53ff1ec4e512752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ebd22144b4cc670843d3501dd13a4831c717570d5fa34fc36a1ee81e97e13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="natAndFirewallServiceIntention")
    def nat_and_firewall_service_intention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natAndFirewallServiceIntention"))

    @nat_and_firewall_service_intention.setter
    def nat_and_firewall_service_intention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97512af7fd3e589dfc04eefe6ba86cf9091c903e40a87be1a71fca4422a19f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natAndFirewallServiceIntention", value)

    @builtins.property
    @jsii.member(jsii_name="routeAdvertisementIntention")
    def route_advertisement_intention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeAdvertisementIntention"))

    @route_advertisement_intention.setter
    def route_advertisement_intention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3124541be95d13618b4812387d4095c161e6053089be499750ccb1a22b174d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeAdvertisementIntention", value)

    @builtins.property
    @jsii.member(jsii_name="useIpSpaces")
    def use_ip_spaces(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useIpSpaces"))

    @use_ip_spaces.setter
    def use_ip_spaces(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e1484bcc0b8a1c4d754a75b6fd3cb3b8d43c50e658710ab4e3df4b8f0fe7ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIpSpaces", value)


@jsii.data_type(
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2Config",
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
        "dedicated_org_id": "dedicatedOrgId",
        "description": "description",
        "id": "id",
        "ip_scope": "ipScope",
        "nat_and_firewall_service_intention": "natAndFirewallServiceIntention",
        "nsxt_network": "nsxtNetwork",
        "route_advertisement_intention": "routeAdvertisementIntention",
        "use_ip_spaces": "useIpSpaces",
        "vsphere_network": "vsphereNetwork",
    },
)
class ExternalNetworkV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dedicated_org_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalNetworkV2IpScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
        nat_and_firewall_service_intention: typing.Optional[builtins.str] = None,
        nsxt_network: typing.Optional[typing.Union["ExternalNetworkV2NsxtNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        route_advertisement_intention: typing.Optional[builtins.str] = None,
        use_ip_spaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsphere_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalNetworkV2VsphereNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#name ExternalNetworkV2#name}
        :param dedicated_org_id: Dedicate this External Network to an Org ID (only with IP Spaces, VCD 10.4.1+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dedicated_org_id ExternalNetworkV2#dedicated_org_id}
        :param description: Network description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#description ExternalNetworkV2#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#id ExternalNetworkV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_scope: ip_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#ip_scope ExternalNetworkV2#ip_scope}
        :param nat_and_firewall_service_intention: Defines intentions to configure NAT and Firewall rules (only with IP Spaces, VCD 10.5.1+) One of ``PROVIDER_GATEWAY``,``EDGE_GATEWAY``,``PROVIDER_AND_EDGE_GATEWAY``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nat_and_firewall_service_intention ExternalNetworkV2#nat_and_firewall_service_intention}
        :param nsxt_network: nsxt_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_network ExternalNetworkV2#nsxt_network}
        :param route_advertisement_intention: Defines intentions to configure route advertisement (only with IP Spaces, VCD 10.5.1+) One of ``IP_SPACE_UPLINKS_ADVERTISED_STRICT``,``IP_SPACE_UPLINKS_ADVERTISED_FLEXIBLE``,``ALL_NETWORKS_ADVERTISED``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#route_advertisement_intention ExternalNetworkV2#route_advertisement_intention}
        :param use_ip_spaces: Enables IP Spaces for this network (default 'false'). VCD 10.4.1+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#use_ip_spaces ExternalNetworkV2#use_ip_spaces}
        :param vsphere_network: vsphere_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#vsphere_network ExternalNetworkV2#vsphere_network}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(nsxt_network, dict):
            nsxt_network = ExternalNetworkV2NsxtNetwork(**nsxt_network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb51486c632ac6496980e40833956f1c67f59b84c2a5a1408257394bdf1402bc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dedicated_org_id", value=dedicated_org_id, expected_type=type_hints["dedicated_org_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_scope", value=ip_scope, expected_type=type_hints["ip_scope"])
            check_type(argname="argument nat_and_firewall_service_intention", value=nat_and_firewall_service_intention, expected_type=type_hints["nat_and_firewall_service_intention"])
            check_type(argname="argument nsxt_network", value=nsxt_network, expected_type=type_hints["nsxt_network"])
            check_type(argname="argument route_advertisement_intention", value=route_advertisement_intention, expected_type=type_hints["route_advertisement_intention"])
            check_type(argname="argument use_ip_spaces", value=use_ip_spaces, expected_type=type_hints["use_ip_spaces"])
            check_type(argname="argument vsphere_network", value=vsphere_network, expected_type=type_hints["vsphere_network"])
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
        if dedicated_org_id is not None:
            self._values["dedicated_org_id"] = dedicated_org_id
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ip_scope is not None:
            self._values["ip_scope"] = ip_scope
        if nat_and_firewall_service_intention is not None:
            self._values["nat_and_firewall_service_intention"] = nat_and_firewall_service_intention
        if nsxt_network is not None:
            self._values["nsxt_network"] = nsxt_network
        if route_advertisement_intention is not None:
            self._values["route_advertisement_intention"] = route_advertisement_intention
        if use_ip_spaces is not None:
            self._values["use_ip_spaces"] = use_ip_spaces
        if vsphere_network is not None:
            self._values["vsphere_network"] = vsphere_network

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
        '''Network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#name ExternalNetworkV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dedicated_org_id(self) -> typing.Optional[builtins.str]:
        '''Dedicate this External Network to an Org ID (only with IP Spaces, VCD 10.4.1+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dedicated_org_id ExternalNetworkV2#dedicated_org_id}
        '''
        result = self._values.get("dedicated_org_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Network description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#description ExternalNetworkV2#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#id ExternalNetworkV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_scope(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2IpScope"]]]:
        '''ip_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#ip_scope ExternalNetworkV2#ip_scope}
        '''
        result = self._values.get("ip_scope")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2IpScope"]]], result)

    @builtins.property
    def nat_and_firewall_service_intention(self) -> typing.Optional[builtins.str]:
        '''Defines intentions to configure NAT and Firewall rules (only with IP Spaces, VCD 10.5.1+) One of ``PROVIDER_GATEWAY``,``EDGE_GATEWAY``,``PROVIDER_AND_EDGE_GATEWAY``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nat_and_firewall_service_intention ExternalNetworkV2#nat_and_firewall_service_intention}
        '''
        result = self._values.get("nat_and_firewall_service_intention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nsxt_network(self) -> typing.Optional["ExternalNetworkV2NsxtNetwork"]:
        '''nsxt_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_network ExternalNetworkV2#nsxt_network}
        '''
        result = self._values.get("nsxt_network")
        return typing.cast(typing.Optional["ExternalNetworkV2NsxtNetwork"], result)

    @builtins.property
    def route_advertisement_intention(self) -> typing.Optional[builtins.str]:
        '''Defines intentions to configure route advertisement (only with IP Spaces, VCD 10.5.1+) One of ``IP_SPACE_UPLINKS_ADVERTISED_STRICT``,``IP_SPACE_UPLINKS_ADVERTISED_FLEXIBLE``,``ALL_NETWORKS_ADVERTISED``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#route_advertisement_intention ExternalNetworkV2#route_advertisement_intention}
        '''
        result = self._values.get("route_advertisement_intention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ip_spaces(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables IP Spaces for this network (default 'false'). VCD 10.4.1+.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#use_ip_spaces ExternalNetworkV2#use_ip_spaces}
        '''
        result = self._values.get("use_ip_spaces")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vsphere_network(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2VsphereNetwork"]]]:
        '''vsphere_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#vsphere_network ExternalNetworkV2#vsphere_network}
        '''
        result = self._values.get("vsphere_network")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2VsphereNetwork"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalNetworkV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2IpScope",
    jsii_struct_bases=[],
    name_mapping={
        "gateway": "gateway",
        "prefix_length": "prefixLength",
        "dns1": "dns1",
        "dns2": "dns2",
        "dns_suffix": "dnsSuffix",
        "enabled": "enabled",
        "static_ip_pool": "staticIpPool",
    },
)
class ExternalNetworkV2IpScope:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        prefix_length: jsii.Number,
        dns1: typing.Optional[builtins.str] = None,
        dns2: typing.Optional[builtins.str] = None,
        dns_suffix: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalNetworkV2IpScopeStaticIpPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gateway: Gateway of the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#gateway ExternalNetworkV2#gateway}
        :param prefix_length: Network mask. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#prefix_length ExternalNetworkV2#prefix_length}
        :param dns1: Primary DNS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dns1 ExternalNetworkV2#dns1}
        :param dns2: Secondary DNS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dns2 ExternalNetworkV2#dns2}
        :param dns_suffix: DNS suffix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dns_suffix ExternalNetworkV2#dns_suffix}
        :param enabled: If subnet is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#enabled ExternalNetworkV2#enabled}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#static_ip_pool ExternalNetworkV2#static_ip_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b97c2ce957746ed7a939d42b77e7f4be828098c070b9f81e1ada3bc0e6879b)
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
            check_type(argname="argument dns1", value=dns1, expected_type=type_hints["dns1"])
            check_type(argname="argument dns2", value=dns2, expected_type=type_hints["dns2"])
            check_type(argname="argument dns_suffix", value=dns_suffix, expected_type=type_hints["dns_suffix"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument static_ip_pool", value=static_ip_pool, expected_type=type_hints["static_ip_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway": gateway,
            "prefix_length": prefix_length,
        }
        if dns1 is not None:
            self._values["dns1"] = dns1
        if dns2 is not None:
            self._values["dns2"] = dns2
        if dns_suffix is not None:
            self._values["dns_suffix"] = dns_suffix
        if enabled is not None:
            self._values["enabled"] = enabled
        if static_ip_pool is not None:
            self._values["static_ip_pool"] = static_ip_pool

    @builtins.property
    def gateway(self) -> builtins.str:
        '''Gateway of the network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#gateway ExternalNetworkV2#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_length(self) -> jsii.Number:
        '''Network mask.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#prefix_length ExternalNetworkV2#prefix_length}
        '''
        result = self._values.get("prefix_length")
        assert result is not None, "Required property 'prefix_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def dns1(self) -> typing.Optional[builtins.str]:
        '''Primary DNS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dns1 ExternalNetworkV2#dns1}
        '''
        result = self._values.get("dns1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns2(self) -> typing.Optional[builtins.str]:
        '''Secondary DNS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dns2 ExternalNetworkV2#dns2}
        '''
        result = self._values.get("dns2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_suffix(self) -> typing.Optional[builtins.str]:
        '''DNS suffix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#dns_suffix ExternalNetworkV2#dns_suffix}
        '''
        result = self._values.get("dns_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If subnet is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#enabled ExternalNetworkV2#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def static_ip_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2IpScopeStaticIpPool"]]]:
        '''static_ip_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#static_ip_pool ExternalNetworkV2#static_ip_pool}
        '''
        result = self._values.get("static_ip_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2IpScopeStaticIpPool"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalNetworkV2IpScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalNetworkV2IpScopeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2IpScopeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6d7a4f8b155fb2eb45280a9577a79c20c51533d0d545fc4a1152ff3945cb78c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ExternalNetworkV2IpScopeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64357b8125b895720da07bdb9ddd6b3709754a44034157999dcb80d9dd89e0c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalNetworkV2IpScopeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb575131125861eb7bd4db8dd4c8dba61c4cdc4ada8a09621150ae879b5d73a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93357f62f9da92646b381d991267eb7404a9be85818817771b37d31d02cd99e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d9445125aa6a12569c8ba0d9e4caef15451038a420ae0605eead663cc8c87f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2IpScope]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2IpScope]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2IpScope]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6742e67cb8bf7006a9101ebd1ae10c57256ef44157948db945b2c4c785b644a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ExternalNetworkV2IpScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2IpScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea56982c4769c1b6198709e4b30c7868b91774ee908a3ebc7bcb511afe9f5bd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putStaticIpPool")
    def put_static_ip_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalNetworkV2IpScopeStaticIpPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8709d8dd17e304d3e36d6dd42deb405d2dda46e8a04db249d9a4ec8f29265f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStaticIpPool", [value]))

    @jsii.member(jsii_name="resetDns1")
    def reset_dns1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns1", []))

    @jsii.member(jsii_name="resetDns2")
    def reset_dns2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns2", []))

    @jsii.member(jsii_name="resetDnsSuffix")
    def reset_dns_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsSuffix", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetStaticIpPool")
    def reset_static_ip_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticIpPool", []))

    @builtins.property
    @jsii.member(jsii_name="staticIpPool")
    def static_ip_pool(self) -> "ExternalNetworkV2IpScopeStaticIpPoolList":
        return typing.cast("ExternalNetworkV2IpScopeStaticIpPoolList", jsii.get(self, "staticIpPool"))

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
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPoolInput")
    def static_ip_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2IpScopeStaticIpPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalNetworkV2IpScopeStaticIpPool"]]], jsii.get(self, "staticIpPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="dns1")
    def dns1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns1"))

    @dns1.setter
    def dns1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfce1b3a4631a81b4396d15febc054b962d5e7c5cbe2ffb4afe12971923d83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns1", value)

    @builtins.property
    @jsii.member(jsii_name="dns2")
    def dns2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns2"))

    @dns2.setter
    def dns2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80c383d8b9d8886044ea45cee20ea6c028aff5a7b2edb3041a2391739ba3030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns2", value)

    @builtins.property
    @jsii.member(jsii_name="dnsSuffix")
    def dns_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsSuffix"))

    @dns_suffix.setter
    def dns_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87a6d1f0b7f942f06d290d643f24d58be0b677b6f8a14762636abda032bf3a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSuffix", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__2606b854cbc559b9c1582f6a8598ce2ccda6b94d6b013368314a5d1d3bf2533a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17442fbf9648a78a3dea96ab009b9ab3aa1109e7bb589dbd9b041f053a8be48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb23594468c1e7a35b033cc643125683d2f74cf649a4cf5531df142b1800ad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2IpScope]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2IpScope]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2IpScope]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2a3e612553ab1b2c2b1f20421d903851e21b41d6bc15485eba01be1ca0303f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2IpScopeStaticIpPool",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class ExternalNetworkV2IpScopeStaticIpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: End address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#end_address ExternalNetworkV2#end_address}
        :param start_address: Start address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#start_address ExternalNetworkV2#start_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4d95d63dc56ff3304178a66619a4661e625608d550965493ecff67c7c31233)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''End address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#end_address ExternalNetworkV2#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Start address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#start_address ExternalNetworkV2#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalNetworkV2IpScopeStaticIpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalNetworkV2IpScopeStaticIpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2IpScopeStaticIpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5d9fab2c5a0a34b5d8d96d2c0e747fc11111d7b60d8f2dc0bf493f99aba5f32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalNetworkV2IpScopeStaticIpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38a5b0bf2cf26957d9d540f0e1b1cc33dce75f891eb91a219aa3fb20d51368e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalNetworkV2IpScopeStaticIpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0f08516e3b43198082c3d1847e9751f619a08b10bcd1f120277d71f10a5be6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc2b7e688af9873f41d65634487217c848aee0f38036fb06ffd6020e8a55c03c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d58f5bd0e72f159cbb2cddb36a0fdc74a3249beb441685de1968144d0240d06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2IpScopeStaticIpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2IpScopeStaticIpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2IpScopeStaticIpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a9b58f04537605ef01d082a2a10b08a203aae37795c7f8f47bf4a90769414e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ExternalNetworkV2IpScopeStaticIpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2IpScopeStaticIpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85736dd61f396a2ac791813310240c5b73b1560a72c5153b075223ae3f6ebdc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1554719821fde1d6e198e6dcd4bf8501061a6a249405c21d899b14677d61465b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9792039f7b9bb9502cb5aa68979999f5b92ca64702e0cc33e1914b142d2a3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2IpScopeStaticIpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2IpScopeStaticIpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2IpScopeStaticIpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c9e1e32478a5a65121ef0185f607bddeabc4d69e03e1a0bf919d8a52d92fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2NsxtNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "nsxt_manager_id": "nsxtManagerId",
        "nsxt_segment_name": "nsxtSegmentName",
        "nsxt_tier0_router_id": "nsxtTier0RouterId",
    },
)
class ExternalNetworkV2NsxtNetwork:
    def __init__(
        self,
        *,
        nsxt_manager_id: builtins.str,
        nsxt_segment_name: typing.Optional[builtins.str] = None,
        nsxt_tier0_router_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nsxt_manager_id: ID of NSX-T manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_manager_id ExternalNetworkV2#nsxt_manager_id}
        :param nsxt_segment_name: Name of NSX-T segment (for NSX-T segment backed external network). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_segment_name ExternalNetworkV2#nsxt_segment_name}
        :param nsxt_tier0_router_id: ID of NSX-T Tier-0 router (for T0 gateway backed external network). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_tier0_router_id ExternalNetworkV2#nsxt_tier0_router_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee9ef0ee4ae9ae5bcf4512d2c43d09b56dc2df9322e6bc3ef26a77d62e8ac1f)
            check_type(argname="argument nsxt_manager_id", value=nsxt_manager_id, expected_type=type_hints["nsxt_manager_id"])
            check_type(argname="argument nsxt_segment_name", value=nsxt_segment_name, expected_type=type_hints["nsxt_segment_name"])
            check_type(argname="argument nsxt_tier0_router_id", value=nsxt_tier0_router_id, expected_type=type_hints["nsxt_tier0_router_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "nsxt_manager_id": nsxt_manager_id,
        }
        if nsxt_segment_name is not None:
            self._values["nsxt_segment_name"] = nsxt_segment_name
        if nsxt_tier0_router_id is not None:
            self._values["nsxt_tier0_router_id"] = nsxt_tier0_router_id

    @builtins.property
    def nsxt_manager_id(self) -> builtins.str:
        '''ID of NSX-T manager.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_manager_id ExternalNetworkV2#nsxt_manager_id}
        '''
        result = self._values.get("nsxt_manager_id")
        assert result is not None, "Required property 'nsxt_manager_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nsxt_segment_name(self) -> typing.Optional[builtins.str]:
        '''Name of NSX-T segment (for NSX-T segment backed external network).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_segment_name ExternalNetworkV2#nsxt_segment_name}
        '''
        result = self._values.get("nsxt_segment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nsxt_tier0_router_id(self) -> typing.Optional[builtins.str]:
        '''ID of NSX-T Tier-0 router (for T0 gateway backed external network).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#nsxt_tier0_router_id ExternalNetworkV2#nsxt_tier0_router_id}
        '''
        result = self._values.get("nsxt_tier0_router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalNetworkV2NsxtNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalNetworkV2NsxtNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2NsxtNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee0a9ad841db77dda28a79f3affd76ab721a34fe636b36c4cec667de2bdb1194)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNsxtSegmentName")
    def reset_nsxt_segment_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNsxtSegmentName", []))

    @jsii.member(jsii_name="resetNsxtTier0RouterId")
    def reset_nsxt_tier0_router_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNsxtTier0RouterId", []))

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerIdInput")
    def nsxt_manager_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nsxtManagerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nsxtSegmentNameInput")
    def nsxt_segment_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nsxtSegmentNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nsxtTier0RouterIdInput")
    def nsxt_tier0_router_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nsxtTier0RouterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerId")
    def nsxt_manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nsxtManagerId"))

    @nsxt_manager_id.setter
    def nsxt_manager_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39accb781331e7e6f615c8981e92ff11219b504c48e2381187e9c8f3cbc0e1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nsxtManagerId", value)

    @builtins.property
    @jsii.member(jsii_name="nsxtSegmentName")
    def nsxt_segment_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nsxtSegmentName"))

    @nsxt_segment_name.setter
    def nsxt_segment_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fa069172a47c31838511895824f73c1411b76642e91c16fd3249b73dacc9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nsxtSegmentName", value)

    @builtins.property
    @jsii.member(jsii_name="nsxtTier0RouterId")
    def nsxt_tier0_router_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nsxtTier0RouterId"))

    @nsxt_tier0_router_id.setter
    def nsxt_tier0_router_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fcfc7760995eb7958a6e8cce7571ee3173e97d757bdc5cd976726ff8e54267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nsxtTier0RouterId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExternalNetworkV2NsxtNetwork]:
        return typing.cast(typing.Optional[ExternalNetworkV2NsxtNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalNetworkV2NsxtNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387caced7e1a1df0362cf061bfc8956a4a6537a20e67df1f8790dc757f01f74a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2VsphereNetwork",
    jsii_struct_bases=[],
    name_mapping={"portgroup_id": "portgroupId", "vcenter_id": "vcenterId"},
)
class ExternalNetworkV2VsphereNetwork:
    def __init__(self, *, portgroup_id: builtins.str, vcenter_id: builtins.str) -> None:
        '''
        :param portgroup_id: The name of the port group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#portgroup_id ExternalNetworkV2#portgroup_id}
        :param vcenter_id: The vCenter server name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#vcenter_id ExternalNetworkV2#vcenter_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4a1d8d2b32b808d2282c08c48169da7cc4a6eaeb801a2942b7c1ced3f9c4b7)
            check_type(argname="argument portgroup_id", value=portgroup_id, expected_type=type_hints["portgroup_id"])
            check_type(argname="argument vcenter_id", value=vcenter_id, expected_type=type_hints["vcenter_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portgroup_id": portgroup_id,
            "vcenter_id": vcenter_id,
        }

    @builtins.property
    def portgroup_id(self) -> builtins.str:
        '''The name of the port group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#portgroup_id ExternalNetworkV2#portgroup_id}
        '''
        result = self._values.get("portgroup_id")
        assert result is not None, "Required property 'portgroup_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vcenter_id(self) -> builtins.str:
        '''The vCenter server name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/external_network_v2#vcenter_id ExternalNetworkV2#vcenter_id}
        '''
        result = self._values.get("vcenter_id")
        assert result is not None, "Required property 'vcenter_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalNetworkV2VsphereNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalNetworkV2VsphereNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2VsphereNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25901270e42bba7a3856aaf90c37d39e51742dcee5c775328e1fd1ea06bc62e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalNetworkV2VsphereNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e8eb503d7445c3d1e93a1a4cff22050915235cd11ab9a0ffad46884c550186)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalNetworkV2VsphereNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a588d9cbf11feae46d0bc415e1814ec7c1aaef40fddfc90b4770a6af20ca358)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98eee736c60ea6c3cf9e9efefb79299815126f3d46c7e2e25463b5cf6f658a80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0a69b94f134bde78ec21652f81ba0160c64f0d856cf2755e51fc8005ef6521c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2VsphereNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2VsphereNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2VsphereNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14da8186a87aaf0668caccc9fb6043d2cbdf7f324e62d082d49211d70f3e70e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ExternalNetworkV2VsphereNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.externalNetworkV2.ExternalNetworkV2VsphereNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3f7fc4abc658869281c89460bfb38e74a793bcce02c7726d6817bf27005c07d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="portgroupIdInput")
    def portgroup_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portgroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vcenterIdInput")
    def vcenter_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vcenterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="portgroupId")
    def portgroup_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portgroupId"))

    @portgroup_id.setter
    def portgroup_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0650d3046c8525550250cd5dd37d80ba2f01f57e244433653e14ee723f24e167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portgroupId", value)

    @builtins.property
    @jsii.member(jsii_name="vcenterId")
    def vcenter_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcenterId"))

    @vcenter_id.setter
    def vcenter_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae55f71f9c28dc75a9a5ab9f0bc5cf0428bb134bf7cde386cc43bd39af322d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcenterId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2VsphereNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2VsphereNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2VsphereNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395e50890cb7adc2dfaf6c74938d0ca4303c946e468d7725012547eb30b9fe69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ExternalNetworkV2",
    "ExternalNetworkV2Config",
    "ExternalNetworkV2IpScope",
    "ExternalNetworkV2IpScopeList",
    "ExternalNetworkV2IpScopeOutputReference",
    "ExternalNetworkV2IpScopeStaticIpPool",
    "ExternalNetworkV2IpScopeStaticIpPoolList",
    "ExternalNetworkV2IpScopeStaticIpPoolOutputReference",
    "ExternalNetworkV2NsxtNetwork",
    "ExternalNetworkV2NsxtNetworkOutputReference",
    "ExternalNetworkV2VsphereNetwork",
    "ExternalNetworkV2VsphereNetworkList",
    "ExternalNetworkV2VsphereNetworkOutputReference",
]

publication.publish()

def _typecheckingstub__e89fa7fe354484d770380726c97f1b0cd699bd9706aafb56f3929533343b1bcd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    dedicated_org_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalNetworkV2IpScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nat_and_firewall_service_intention: typing.Optional[builtins.str] = None,
    nsxt_network: typing.Optional[typing.Union[ExternalNetworkV2NsxtNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    route_advertisement_intention: typing.Optional[builtins.str] = None,
    use_ip_spaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsphere_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalNetworkV2VsphereNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__1a93ac2a548e1a87d1aba3860d3c14e8ebf3acf82d195eb1423d1eb24c8c7acc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dabd71e8da5e350a5d6fb40d615b13f11d17c5a37ec9f7b4bd05a8d83592eb0d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalNetworkV2IpScope, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20409ac46318e56ee0ef189d62bdb58bb27678b218f7831624f7ac7582d3ffa5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalNetworkV2VsphereNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c443daae4d2a65901fa039f3c03d69cc51dfd8d5cb8d8c3fbacf9e737912a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82242c3320e23eb18309de39e12d387ac743e07a2ee0db975911be8a051cd387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0257c9e5ae4e28624d52bf4788b5c771ccce0cd48b767a9ef53ff1ec4e512752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ebd22144b4cc670843d3501dd13a4831c717570d5fa34fc36a1ee81e97e13e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97512af7fd3e589dfc04eefe6ba86cf9091c903e40a87be1a71fca4422a19f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3124541be95d13618b4812387d4095c161e6053089be499750ccb1a22b174d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e1484bcc0b8a1c4d754a75b6fd3cb3b8d43c50e658710ab4e3df4b8f0fe7ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb51486c632ac6496980e40833956f1c67f59b84c2a5a1408257394bdf1402bc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    dedicated_org_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalNetworkV2IpScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nat_and_firewall_service_intention: typing.Optional[builtins.str] = None,
    nsxt_network: typing.Optional[typing.Union[ExternalNetworkV2NsxtNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    route_advertisement_intention: typing.Optional[builtins.str] = None,
    use_ip_spaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsphere_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalNetworkV2VsphereNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b97c2ce957746ed7a939d42b77e7f4be828098c070b9f81e1ada3bc0e6879b(
    *,
    gateway: builtins.str,
    prefix_length: jsii.Number,
    dns1: typing.Optional[builtins.str] = None,
    dns2: typing.Optional[builtins.str] = None,
    dns_suffix: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    static_ip_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalNetworkV2IpScopeStaticIpPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d7a4f8b155fb2eb45280a9577a79c20c51533d0d545fc4a1152ff3945cb78c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64357b8125b895720da07bdb9ddd6b3709754a44034157999dcb80d9dd89e0c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb575131125861eb7bd4db8dd4c8dba61c4cdc4ada8a09621150ae879b5d73a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93357f62f9da92646b381d991267eb7404a9be85818817771b37d31d02cd99e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d9445125aa6a12569c8ba0d9e4caef15451038a420ae0605eead663cc8c87f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6742e67cb8bf7006a9101ebd1ae10c57256ef44157948db945b2c4c785b644a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2IpScope]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea56982c4769c1b6198709e4b30c7868b91774ee908a3ebc7bcb511afe9f5bd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8709d8dd17e304d3e36d6dd42deb405d2dda46e8a04db249d9a4ec8f29265f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalNetworkV2IpScopeStaticIpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfce1b3a4631a81b4396d15febc054b962d5e7c5cbe2ffb4afe12971923d83a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80c383d8b9d8886044ea45cee20ea6c028aff5a7b2edb3041a2391739ba3030(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87a6d1f0b7f942f06d290d643f24d58be0b677b6f8a14762636abda032bf3a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2606b854cbc559b9c1582f6a8598ce2ccda6b94d6b013368314a5d1d3bf2533a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17442fbf9648a78a3dea96ab009b9ab3aa1109e7bb589dbd9b041f053a8be48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb23594468c1e7a35b033cc643125683d2f74cf649a4cf5531df142b1800ad2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2a3e612553ab1b2c2b1f20421d903851e21b41d6bc15485eba01be1ca0303f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2IpScope]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4d95d63dc56ff3304178a66619a4661e625608d550965493ecff67c7c31233(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d9fab2c5a0a34b5d8d96d2c0e747fc11111d7b60d8f2dc0bf493f99aba5f32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38a5b0bf2cf26957d9d540f0e1b1cc33dce75f891eb91a219aa3fb20d51368e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0f08516e3b43198082c3d1847e9751f619a08b10bcd1f120277d71f10a5be6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2b7e688af9873f41d65634487217c848aee0f38036fb06ffd6020e8a55c03c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58f5bd0e72f159cbb2cddb36a0fdc74a3249beb441685de1968144d0240d06a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a9b58f04537605ef01d082a2a10b08a203aae37795c7f8f47bf4a90769414e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2IpScopeStaticIpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85736dd61f396a2ac791813310240c5b73b1560a72c5153b075223ae3f6ebdc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1554719821fde1d6e198e6dcd4bf8501061a6a249405c21d899b14677d61465b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9792039f7b9bb9502cb5aa68979999f5b92ca64702e0cc33e1914b142d2a3e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c9e1e32478a5a65121ef0185f607bddeabc4d69e03e1a0bf919d8a52d92fbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2IpScopeStaticIpPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee9ef0ee4ae9ae5bcf4512d2c43d09b56dc2df9322e6bc3ef26a77d62e8ac1f(
    *,
    nsxt_manager_id: builtins.str,
    nsxt_segment_name: typing.Optional[builtins.str] = None,
    nsxt_tier0_router_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0a9ad841db77dda28a79f3affd76ab721a34fe636b36c4cec667de2bdb1194(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39accb781331e7e6f615c8981e92ff11219b504c48e2381187e9c8f3cbc0e1e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fa069172a47c31838511895824f73c1411b76642e91c16fd3249b73dacc9e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fcfc7760995eb7958a6e8cce7571ee3173e97d757bdc5cd976726ff8e54267(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387caced7e1a1df0362cf061bfc8956a4a6537a20e67df1f8790dc757f01f74a(
    value: typing.Optional[ExternalNetworkV2NsxtNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4a1d8d2b32b808d2282c08c48169da7cc4a6eaeb801a2942b7c1ced3f9c4b7(
    *,
    portgroup_id: builtins.str,
    vcenter_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25901270e42bba7a3856aaf90c37d39e51742dcee5c775328e1fd1ea06bc62e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e8eb503d7445c3d1e93a1a4cff22050915235cd11ab9a0ffad46884c550186(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a588d9cbf11feae46d0bc415e1814ec7c1aaef40fddfc90b4770a6af20ca358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98eee736c60ea6c3cf9e9efefb79299815126f3d46c7e2e25463b5cf6f658a80(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a69b94f134bde78ec21652f81ba0160c64f0d856cf2755e51fc8005ef6521c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14da8186a87aaf0668caccc9fb6043d2cbdf7f324e62d082d49211d70f3e70e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalNetworkV2VsphereNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f7fc4abc658869281c89460bfb38e74a793bcce02c7726d6817bf27005c07d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0650d3046c8525550250cd5dd37d80ba2f01f57e244433653e14ee723f24e167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae55f71f9c28dc75a9a5ab9f0bc5cf0428bb134bf7cde386cc43bd39af322d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395e50890cb7adc2dfaf6c74938d0ca4303c946e468d7725012547eb30b9fe69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalNetworkV2VsphereNetwork]],
) -> None:
    """Type checking stubs"""
    pass
