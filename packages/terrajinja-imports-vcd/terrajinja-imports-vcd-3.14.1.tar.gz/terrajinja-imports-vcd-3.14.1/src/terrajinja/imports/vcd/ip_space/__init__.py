'''
# `vcd_ip_space`

Refer to the Terraform Registry for docs: [`vcd_ip_space`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space).
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


class IpSpace(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.ipSpace.IpSpace",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space vcd_ip_space}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        internal_scope: typing.Sequence[builtins.str],
        name: builtins.str,
        type: builtins.str,
        default_firewall_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_no_snat_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_snat_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        external_scope: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_prefix: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IpSpaceIpPrefix", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IpSpaceIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_range_quota: typing.Optional[builtins.str] = None,
        org_id: typing.Optional[builtins.str] = None,
        route_advertisement_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space vcd_ip_space} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param internal_scope: A set of internal scope IPs in CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#internal_scope IpSpace#internal_scope}
        :param name: Name of IP space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#name IpSpace#name}
        :param type: Type of IP space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#type IpSpace#type}
        :param default_firewall_rule_creation_enabled: Flag exposing whether default firewall rule creation should be enabled (VCD 10.5.0+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_firewall_rule_creation_enabled IpSpace#default_firewall_rule_creation_enabled}
        :param default_no_snat_rule_creation_enabled: Flag whether NO SNAT rule creation should be enabled (VCD 10.5.0+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_no_snat_rule_creation_enabled IpSpace#default_no_snat_rule_creation_enabled}
        :param default_snat_rule_creation_enabled: Flag whether SNAT rule creation should be enabled (VCD 10.5.0+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_snat_rule_creation_enabled IpSpace#default_snat_rule_creation_enabled}
        :param description: Description of IP space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#description IpSpace#description}
        :param external_scope: External scope in CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#external_scope IpSpace#external_scope}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#id IpSpace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_prefix: ip_prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_prefix IpSpace#ip_prefix}
        :param ip_range: ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_range IpSpace#ip_range}
        :param ip_range_quota: IP ranges quota. '-1' - unlimited, '0' - no quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_range_quota IpSpace#ip_range_quota}
        :param org_id: Org ID for 'SHARED' IP spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#org_id IpSpace#org_id}
        :param route_advertisement_enabled: Flag whether route advertisement should be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#route_advertisement_enabled IpSpace#route_advertisement_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0beed98015746587fdf2ffa4138d904efc1c9f7b9ecdc4cd1abefe36619ff1a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IpSpaceConfig(
            internal_scope=internal_scope,
            name=name,
            type=type,
            default_firewall_rule_creation_enabled=default_firewall_rule_creation_enabled,
            default_no_snat_rule_creation_enabled=default_no_snat_rule_creation_enabled,
            default_snat_rule_creation_enabled=default_snat_rule_creation_enabled,
            description=description,
            external_scope=external_scope,
            id=id,
            ip_prefix=ip_prefix,
            ip_range=ip_range,
            ip_range_quota=ip_range_quota,
            org_id=org_id,
            route_advertisement_enabled=route_advertisement_enabled,
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
        '''Generates CDKTF code for importing a IpSpace resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IpSpace to import.
        :param import_from_id: The id of the existing IpSpace that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IpSpace to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c041278bf197e11ac0e1d39b127aab8c50b3d3e3ea15a0088a149a82487c5a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIpPrefix")
    def put_ip_prefix(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IpSpaceIpPrefix", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbfe72d1706bae62f16e96febfa2fce2826e78751636d2f20f3787e0763690a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpPrefix", [value]))

    @jsii.member(jsii_name="putIpRange")
    def put_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IpSpaceIpRange", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c52ec972d006b36c13cadd8d9a3632025091cae23b902fa9881e06657619bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpRange", [value]))

    @jsii.member(jsii_name="resetDefaultFirewallRuleCreationEnabled")
    def reset_default_firewall_rule_creation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultFirewallRuleCreationEnabled", []))

    @jsii.member(jsii_name="resetDefaultNoSnatRuleCreationEnabled")
    def reset_default_no_snat_rule_creation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultNoSnatRuleCreationEnabled", []))

    @jsii.member(jsii_name="resetDefaultSnatRuleCreationEnabled")
    def reset_default_snat_rule_creation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSnatRuleCreationEnabled", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExternalScope")
    def reset_external_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalScope", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpPrefix")
    def reset_ip_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpPrefix", []))

    @jsii.member(jsii_name="resetIpRange")
    def reset_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRange", []))

    @jsii.member(jsii_name="resetIpRangeQuota")
    def reset_ip_range_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRangeQuota", []))

    @jsii.member(jsii_name="resetOrgId")
    def reset_org_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgId", []))

    @jsii.member(jsii_name="resetRouteAdvertisementEnabled")
    def reset_route_advertisement_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteAdvertisementEnabled", []))

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
    def ip_prefix(self) -> "IpSpaceIpPrefixList":
        return typing.cast("IpSpaceIpPrefixList", jsii.get(self, "ipPrefix"))

    @builtins.property
    @jsii.member(jsii_name="ipRange")
    def ip_range(self) -> "IpSpaceIpRangeList":
        return typing.cast("IpSpaceIpRangeList", jsii.get(self, "ipRange"))

    @builtins.property
    @jsii.member(jsii_name="defaultFirewallRuleCreationEnabledInput")
    def default_firewall_rule_creation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultFirewallRuleCreationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultNoSnatRuleCreationEnabledInput")
    def default_no_snat_rule_creation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultNoSnatRuleCreationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSnatRuleCreationEnabledInput")
    def default_snat_rule_creation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultSnatRuleCreationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="externalScopeInput")
    def external_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="internalScopeInput")
    def internal_scope_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "internalScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipPrefixInput")
    def ip_prefix_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpPrefix"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpPrefix"]]], jsii.get(self, "ipPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRangeInput")
    def ip_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpRange"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpRange"]]], jsii.get(self, "ipRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRangeQuotaInput")
    def ip_range_quota_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipRangeQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="routeAdvertisementEnabledInput")
    def route_advertisement_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "routeAdvertisementEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultFirewallRuleCreationEnabled")
    def default_firewall_rule_creation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultFirewallRuleCreationEnabled"))

    @default_firewall_rule_creation_enabled.setter
    def default_firewall_rule_creation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3d695466b097e18e0c820ad38b354aa09ed371007fad846cf352e372539a2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultFirewallRuleCreationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="defaultNoSnatRuleCreationEnabled")
    def default_no_snat_rule_creation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultNoSnatRuleCreationEnabled"))

    @default_no_snat_rule_creation_enabled.setter
    def default_no_snat_rule_creation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5829e02eea55e167aeeb4033af55f1d838b98c778e5ab0db8b2b049f5954d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultNoSnatRuleCreationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="defaultSnatRuleCreationEnabled")
    def default_snat_rule_creation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultSnatRuleCreationEnabled"))

    @default_snat_rule_creation_enabled.setter
    def default_snat_rule_creation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3dd1c5284d823149f79ef3a39ba6216e5a40067c20b79dcfab45c12a7f06117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSnatRuleCreationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702bc4a1e2c7cf107a869326c3bd44d53259d7008caa8326567f8e13cb862b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="externalScope")
    def external_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalScope"))

    @external_scope.setter
    def external_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3ecc57e7fd8152367a65c04f13a5db75caa4ac4939a735af2186b2c2abe072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalScope", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef611653b2afea39d1fe55705c8aa157e9d3e20e7d406d63b39ae4718be8a396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="internalScope")
    def internal_scope(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "internalScope"))

    @internal_scope.setter
    def internal_scope(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2893a8c1c8d67cd7ec3b6c96e3ae23667e8452f93fbdcb62a8e8f1754fb21992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalScope", value)

    @builtins.property
    @jsii.member(jsii_name="ipRangeQuota")
    def ip_range_quota(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipRangeQuota"))

    @ip_range_quota.setter
    def ip_range_quota(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4966b242b345c07648c9ea83d7eb6e8ac0bbd27e2e02f605c755f5f8bea26f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRangeQuota", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1875a810a3b639720720f2388597cb50ff61f61fb53138a450f8b2f6f120b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb438c1da2d415571748d5cc816b55a63684ac32767150c6db39bf2a2749d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value)

    @builtins.property
    @jsii.member(jsii_name="routeAdvertisementEnabled")
    def route_advertisement_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "routeAdvertisementEnabled"))

    @route_advertisement_enabled.setter
    def route_advertisement_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb63572b09a5164f5201df9904338a863912da7fd4cc7d96d0f5edeae7512f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeAdvertisementEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ddd21d724d41555f52bf850170a8c4ef265d95cfc500ac66e9fa8b68378114b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="vcd.ipSpace.IpSpaceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "internal_scope": "internalScope",
        "name": "name",
        "type": "type",
        "default_firewall_rule_creation_enabled": "defaultFirewallRuleCreationEnabled",
        "default_no_snat_rule_creation_enabled": "defaultNoSnatRuleCreationEnabled",
        "default_snat_rule_creation_enabled": "defaultSnatRuleCreationEnabled",
        "description": "description",
        "external_scope": "externalScope",
        "id": "id",
        "ip_prefix": "ipPrefix",
        "ip_range": "ipRange",
        "ip_range_quota": "ipRangeQuota",
        "org_id": "orgId",
        "route_advertisement_enabled": "routeAdvertisementEnabled",
    },
)
class IpSpaceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        internal_scope: typing.Sequence[builtins.str],
        name: builtins.str,
        type: builtins.str,
        default_firewall_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_no_snat_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_snat_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        external_scope: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_prefix: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IpSpaceIpPrefix", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IpSpaceIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_range_quota: typing.Optional[builtins.str] = None,
        org_id: typing.Optional[builtins.str] = None,
        route_advertisement_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param internal_scope: A set of internal scope IPs in CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#internal_scope IpSpace#internal_scope}
        :param name: Name of IP space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#name IpSpace#name}
        :param type: Type of IP space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#type IpSpace#type}
        :param default_firewall_rule_creation_enabled: Flag exposing whether default firewall rule creation should be enabled (VCD 10.5.0+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_firewall_rule_creation_enabled IpSpace#default_firewall_rule_creation_enabled}
        :param default_no_snat_rule_creation_enabled: Flag whether NO SNAT rule creation should be enabled (VCD 10.5.0+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_no_snat_rule_creation_enabled IpSpace#default_no_snat_rule_creation_enabled}
        :param default_snat_rule_creation_enabled: Flag whether SNAT rule creation should be enabled (VCD 10.5.0+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_snat_rule_creation_enabled IpSpace#default_snat_rule_creation_enabled}
        :param description: Description of IP space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#description IpSpace#description}
        :param external_scope: External scope in CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#external_scope IpSpace#external_scope}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#id IpSpace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_prefix: ip_prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_prefix IpSpace#ip_prefix}
        :param ip_range: ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_range IpSpace#ip_range}
        :param ip_range_quota: IP ranges quota. '-1' - unlimited, '0' - no quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_range_quota IpSpace#ip_range_quota}
        :param org_id: Org ID for 'SHARED' IP spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#org_id IpSpace#org_id}
        :param route_advertisement_enabled: Flag whether route advertisement should be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#route_advertisement_enabled IpSpace#route_advertisement_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2171e48ac2fa4a25a933538dcdd505bc2891997d5e886385ab13c8c6e6e81d68)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument internal_scope", value=internal_scope, expected_type=type_hints["internal_scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument default_firewall_rule_creation_enabled", value=default_firewall_rule_creation_enabled, expected_type=type_hints["default_firewall_rule_creation_enabled"])
            check_type(argname="argument default_no_snat_rule_creation_enabled", value=default_no_snat_rule_creation_enabled, expected_type=type_hints["default_no_snat_rule_creation_enabled"])
            check_type(argname="argument default_snat_rule_creation_enabled", value=default_snat_rule_creation_enabled, expected_type=type_hints["default_snat_rule_creation_enabled"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_scope", value=external_scope, expected_type=type_hints["external_scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_prefix", value=ip_prefix, expected_type=type_hints["ip_prefix"])
            check_type(argname="argument ip_range", value=ip_range, expected_type=type_hints["ip_range"])
            check_type(argname="argument ip_range_quota", value=ip_range_quota, expected_type=type_hints["ip_range_quota"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument route_advertisement_enabled", value=route_advertisement_enabled, expected_type=type_hints["route_advertisement_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "internal_scope": internal_scope,
            "name": name,
            "type": type,
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
        if default_firewall_rule_creation_enabled is not None:
            self._values["default_firewall_rule_creation_enabled"] = default_firewall_rule_creation_enabled
        if default_no_snat_rule_creation_enabled is not None:
            self._values["default_no_snat_rule_creation_enabled"] = default_no_snat_rule_creation_enabled
        if default_snat_rule_creation_enabled is not None:
            self._values["default_snat_rule_creation_enabled"] = default_snat_rule_creation_enabled
        if description is not None:
            self._values["description"] = description
        if external_scope is not None:
            self._values["external_scope"] = external_scope
        if id is not None:
            self._values["id"] = id
        if ip_prefix is not None:
            self._values["ip_prefix"] = ip_prefix
        if ip_range is not None:
            self._values["ip_range"] = ip_range
        if ip_range_quota is not None:
            self._values["ip_range_quota"] = ip_range_quota
        if org_id is not None:
            self._values["org_id"] = org_id
        if route_advertisement_enabled is not None:
            self._values["route_advertisement_enabled"] = route_advertisement_enabled

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
    def internal_scope(self) -> typing.List[builtins.str]:
        '''A set of internal scope IPs in CIDR format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#internal_scope IpSpace#internal_scope}
        '''
        result = self._values.get("internal_scope")
        assert result is not None, "Required property 'internal_scope' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of IP space.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#name IpSpace#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of IP space.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#type IpSpace#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_firewall_rule_creation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag exposing whether default firewall rule creation should be enabled (VCD 10.5.0+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_firewall_rule_creation_enabled IpSpace#default_firewall_rule_creation_enabled}
        '''
        result = self._values.get("default_firewall_rule_creation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_no_snat_rule_creation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag whether NO SNAT rule creation should be enabled (VCD 10.5.0+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_no_snat_rule_creation_enabled IpSpace#default_no_snat_rule_creation_enabled}
        '''
        result = self._values.get("default_no_snat_rule_creation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_snat_rule_creation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag whether SNAT rule creation should be enabled (VCD 10.5.0+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_snat_rule_creation_enabled IpSpace#default_snat_rule_creation_enabled}
        '''
        result = self._values.get("default_snat_rule_creation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of IP space.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#description IpSpace#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_scope(self) -> typing.Optional[builtins.str]:
        '''External scope in CIDR format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#external_scope IpSpace#external_scope}
        '''
        result = self._values.get("external_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#id IpSpace#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_prefix(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpPrefix"]]]:
        '''ip_prefix block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_prefix IpSpace#ip_prefix}
        '''
        result = self._values.get("ip_prefix")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpPrefix"]]], result)

    @builtins.property
    def ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpRange"]]]:
        '''ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_range IpSpace#ip_range}
        '''
        result = self._values.get("ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpRange"]]], result)

    @builtins.property
    def ip_range_quota(self) -> typing.Optional[builtins.str]:
        '''IP ranges quota. '-1' - unlimited, '0' - no quota.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#ip_range_quota IpSpace#ip_range_quota}
        '''
        result = self._values.get("ip_range_quota")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org_id(self) -> typing.Optional[builtins.str]:
        '''Org ID for 'SHARED' IP spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#org_id IpSpace#org_id}
        '''
        result = self._values.get("org_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_advertisement_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag whether route advertisement should be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#route_advertisement_enabled IpSpace#route_advertisement_enabled}
        '''
        result = self._values.get("route_advertisement_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpSpaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.ipSpace.IpSpaceIpPrefix",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix", "default_quota": "defaultQuota"},
)
class IpSpaceIpPrefix:
    def __init__(
        self,
        *,
        prefix: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IpSpaceIpPrefixPrefix", typing.Dict[builtins.str, typing.Any]]]],
        default_quota: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#prefix IpSpace#prefix}
        :param default_quota: Floating IP quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_quota IpSpace#default_quota}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152c3e6e1badc545656fb679836c8767100742c2f7bbf09b39b166255ebd9046)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument default_quota", value=default_quota, expected_type=type_hints["default_quota"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prefix": prefix,
        }
        if default_quota is not None:
            self._values["default_quota"] = default_quota

    @builtins.property
    def prefix(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpPrefixPrefix"]]:
        '''prefix block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#prefix IpSpace#prefix}
        '''
        result = self._values.get("prefix")
        assert result is not None, "Required property 'prefix' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpPrefixPrefix"]], result)

    @builtins.property
    def default_quota(self) -> typing.Optional[builtins.str]:
        '''Floating IP quota.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#default_quota IpSpace#default_quota}
        '''
        result = self._values.get("default_quota")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpSpaceIpPrefix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IpSpaceIpPrefixList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.ipSpace.IpSpaceIpPrefixList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25a3566d843119515e05a09ab1bb9a8b6e4f744d0bfd379323ac68dd7bdd826b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IpSpaceIpPrefixOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f65a5200cfff2421fa2c78acc0f27c9a46d7fcc5703533c152fd3be599cb2df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IpSpaceIpPrefixOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0661195a5f618d43ac4918911656cab5d0380bb256b78bce8684e0241bc6bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0eabea2bdde0643d7d0e9489472d0a0882f34f647f7a75ff1daadf82cd17d96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b697f2320e530adb9668437a72709ac7b61804416764445ee88e65b7962fe7f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpPrefix]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpPrefix]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpPrefix]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37818dc15fdda8fc46708a49f0be92a53beac8f5bf07e774dc1668bd11f241c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class IpSpaceIpPrefixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.ipSpace.IpSpaceIpPrefixOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be5350a8e36c66ca29bb7e5e6f742efb6fd172e9d27033093bb69627d559a67d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPrefix")
    def put_prefix(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IpSpaceIpPrefixPrefix", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4697f5621d3d6cc700194fa0f011e3eccc3d13b9c54af2d471c78c71a8565036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrefix", [value]))

    @jsii.member(jsii_name="resetDefaultQuota")
    def reset_default_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultQuota", []))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> "IpSpaceIpPrefixPrefixList":
        return typing.cast("IpSpaceIpPrefixPrefixList", jsii.get(self, "prefix"))

    @builtins.property
    @jsii.member(jsii_name="defaultQuotaInput")
    def default_quota_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpPrefixPrefix"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IpSpaceIpPrefixPrefix"]]], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultQuota")
    def default_quota(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultQuota"))

    @default_quota.setter
    def default_quota(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df888eab1756382fcd8b369fd574798f4224c4f5af64f989b7e17234ea1c74df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultQuota", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpPrefix]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpPrefix]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpPrefix]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7734cecd7580af2bf0c5a13db77b4d4bbc7889ac60e284c1f403d2cdfbe519aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.ipSpace.IpSpaceIpPrefixPrefix",
    jsii_struct_bases=[],
    name_mapping={
        "first_ip": "firstIp",
        "prefix_count": "prefixCount",
        "prefix_length": "prefixLength",
    },
)
class IpSpaceIpPrefixPrefix:
    def __init__(
        self,
        *,
        first_ip: builtins.str,
        prefix_count: builtins.str,
        prefix_length: builtins.str,
    ) -> None:
        '''
        :param first_ip: First IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#first_ip IpSpace#first_ip}
        :param prefix_count: Number of prefixes to define. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#prefix_count IpSpace#prefix_count}
        :param prefix_length: Prefix length. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#prefix_length IpSpace#prefix_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42601d6cc4e65448a401c8783d420611b1006f1072b5b8f8d0b3f88918745b8)
            check_type(argname="argument first_ip", value=first_ip, expected_type=type_hints["first_ip"])
            check_type(argname="argument prefix_count", value=prefix_count, expected_type=type_hints["prefix_count"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "first_ip": first_ip,
            "prefix_count": prefix_count,
            "prefix_length": prefix_length,
        }

    @builtins.property
    def first_ip(self) -> builtins.str:
        '''First IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#first_ip IpSpace#first_ip}
        '''
        result = self._values.get("first_ip")
        assert result is not None, "Required property 'first_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_count(self) -> builtins.str:
        '''Number of prefixes to define.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#prefix_count IpSpace#prefix_count}
        '''
        result = self._values.get("prefix_count")
        assert result is not None, "Required property 'prefix_count' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_length(self) -> builtins.str:
        '''Prefix length.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#prefix_length IpSpace#prefix_length}
        '''
        result = self._values.get("prefix_length")
        assert result is not None, "Required property 'prefix_length' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpSpaceIpPrefixPrefix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IpSpaceIpPrefixPrefixList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.ipSpace.IpSpaceIpPrefixPrefixList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d3fe8669429bcf0acd9a6240edf5e37a742bbbd12aca0286c270e4b7106ba9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IpSpaceIpPrefixPrefixOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6791ffc45ad57dca1827ab5312358c9a75148aa63721980a6af4c05745fd2a69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IpSpaceIpPrefixPrefixOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ba22eb826880f199eaee0300aa3cca927b319983834372237b0d11a42c990f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fae70563beeb2f159ff3f2ae41319340cc57032d2b1fc407356e5ac8f5799ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e86abbc57915995d9af7d614bd051acf2583c95c7faf08bd5f1058705a52e4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpPrefixPrefix]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpPrefixPrefix]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpPrefixPrefix]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382c3e41b032fee648146f9694a9e8fbdc0117d64d75091ac8f24f8c93a653f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class IpSpaceIpPrefixPrefixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.ipSpace.IpSpaceIpPrefixPrefixOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c1f6db85407204559e60433d05cf26239e85e8a7576ec5177fb34848052ffc2)
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
    @jsii.member(jsii_name="firstIpInput")
    def first_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstIpInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixCountInput")
    def prefix_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixCountInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="firstIp")
    def first_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstIp"))

    @first_ip.setter
    def first_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6841be2660e931001e54059831c87992aa5a4721a8ffff824f34290c4bd5ba31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstIp", value)

    @builtins.property
    @jsii.member(jsii_name="prefixCount")
    def prefix_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixCount"))

    @prefix_count.setter
    def prefix_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303b7f77b53ad900875e99aef87710af18c08e32e0869c3f188cdfaac87cb4ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixCount", value)

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257404ceff02400949aab0f614bd9deaf51f5a30a74342ca34e753630342998a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpPrefixPrefix]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpPrefixPrefix]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpPrefixPrefix]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5108742ce35d103eef86e6656987431d706c4a0b1211a7b665715efd09a3a19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.ipSpace.IpSpaceIpRange",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class IpSpaceIpRange:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: End address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#end_address IpSpace#end_address}
        :param start_address: Start address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#start_address IpSpace#start_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b18d6498fd2681786dccbb6cb570e503f7e93c047e5806a8022176988fee862)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''End address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#end_address IpSpace#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Start address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/ip_space#start_address IpSpace#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpSpaceIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IpSpaceIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.ipSpace.IpSpaceIpRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d12db90a92faa3e67f1a6a18af7e1851b47abbbde93bcbe15e3d7fb0b1d40a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IpSpaceIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e825bb0ed0b6505677b54da8883ed922bae1394371100ee74d6458a4b69c9d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IpSpaceIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adf01ea591e1e262d479cad648e97d95d83cdc92425e8ee4bc80cd5e02487c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f25ac76e01af003d77b894ba6400b70d9b2a266dd062c9de88d7e55ad1b54343)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15bda59dd2e2bfe54485e6f22b6e12a2d1b61f9fe01293bc2f2045ef8d95f0a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a65e643636160e9a1b0744a4b79a2908a44e84fd73e77d67ce9db1319412cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class IpSpaceIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.ipSpace.IpSpaceIpRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a8355e4fdbe3c156f6153f78403c2f206aab80f2b77ffe78623d2ead40be830)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38dc0c21b9b7c613fd953dcbdc232eb966bc341b1b54a6c2a6b9c50f5889840f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40a90458bd057a5367e1404df3f3c29547423e9196519b94fc5ea49eae6a43b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac9a91d84643bc5cad20be0ded4fc793fade0b76740821109809a92af3b2a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "IpSpace",
    "IpSpaceConfig",
    "IpSpaceIpPrefix",
    "IpSpaceIpPrefixList",
    "IpSpaceIpPrefixOutputReference",
    "IpSpaceIpPrefixPrefix",
    "IpSpaceIpPrefixPrefixList",
    "IpSpaceIpPrefixPrefixOutputReference",
    "IpSpaceIpRange",
    "IpSpaceIpRangeList",
    "IpSpaceIpRangeOutputReference",
]

publication.publish()

def _typecheckingstub__f0beed98015746587fdf2ffa4138d904efc1c9f7b9ecdc4cd1abefe36619ff1a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    internal_scope: typing.Sequence[builtins.str],
    name: builtins.str,
    type: builtins.str,
    default_firewall_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_no_snat_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_snat_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    external_scope: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_prefix: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IpSpaceIpPrefix, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IpSpaceIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_range_quota: typing.Optional[builtins.str] = None,
    org_id: typing.Optional[builtins.str] = None,
    route_advertisement_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__8c041278bf197e11ac0e1d39b127aab8c50b3d3e3ea15a0088a149a82487c5a5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbfe72d1706bae62f16e96febfa2fce2826e78751636d2f20f3787e0763690a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IpSpaceIpPrefix, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c52ec972d006b36c13cadd8d9a3632025091cae23b902fa9881e06657619bd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IpSpaceIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3d695466b097e18e0c820ad38b354aa09ed371007fad846cf352e372539a2f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5829e02eea55e167aeeb4033af55f1d838b98c778e5ab0db8b2b049f5954d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3dd1c5284d823149f79ef3a39ba6216e5a40067c20b79dcfab45c12a7f06117(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702bc4a1e2c7cf107a869326c3bd44d53259d7008caa8326567f8e13cb862b2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3ecc57e7fd8152367a65c04f13a5db75caa4ac4939a735af2186b2c2abe072(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef611653b2afea39d1fe55705c8aa157e9d3e20e7d406d63b39ae4718be8a396(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2893a8c1c8d67cd7ec3b6c96e3ae23667e8452f93fbdcb62a8e8f1754fb21992(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4966b242b345c07648c9ea83d7eb6e8ac0bbd27e2e02f605c755f5f8bea26f5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1875a810a3b639720720f2388597cb50ff61f61fb53138a450f8b2f6f120b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb438c1da2d415571748d5cc816b55a63684ac32767150c6db39bf2a2749d64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb63572b09a5164f5201df9904338a863912da7fd4cc7d96d0f5edeae7512f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddd21d724d41555f52bf850170a8c4ef265d95cfc500ac66e9fa8b68378114b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2171e48ac2fa4a25a933538dcdd505bc2891997d5e886385ab13c8c6e6e81d68(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    internal_scope: typing.Sequence[builtins.str],
    name: builtins.str,
    type: builtins.str,
    default_firewall_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_no_snat_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_snat_rule_creation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    external_scope: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_prefix: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IpSpaceIpPrefix, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IpSpaceIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_range_quota: typing.Optional[builtins.str] = None,
    org_id: typing.Optional[builtins.str] = None,
    route_advertisement_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152c3e6e1badc545656fb679836c8767100742c2f7bbf09b39b166255ebd9046(
    *,
    prefix: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IpSpaceIpPrefixPrefix, typing.Dict[builtins.str, typing.Any]]]],
    default_quota: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a3566d843119515e05a09ab1bb9a8b6e4f744d0bfd379323ac68dd7bdd826b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f65a5200cfff2421fa2c78acc0f27c9a46d7fcc5703533c152fd3be599cb2df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0661195a5f618d43ac4918911656cab5d0380bb256b78bce8684e0241bc6bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0eabea2bdde0643d7d0e9489472d0a0882f34f647f7a75ff1daadf82cd17d96(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b697f2320e530adb9668437a72709ac7b61804416764445ee88e65b7962fe7f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37818dc15fdda8fc46708a49f0be92a53beac8f5bf07e774dc1668bd11f241c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpPrefix]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5350a8e36c66ca29bb7e5e6f742efb6fd172e9d27033093bb69627d559a67d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4697f5621d3d6cc700194fa0f011e3eccc3d13b9c54af2d471c78c71a8565036(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IpSpaceIpPrefixPrefix, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df888eab1756382fcd8b369fd574798f4224c4f5af64f989b7e17234ea1c74df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7734cecd7580af2bf0c5a13db77b4d4bbc7889ac60e284c1f403d2cdfbe519aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpPrefix]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42601d6cc4e65448a401c8783d420611b1006f1072b5b8f8d0b3f88918745b8(
    *,
    first_ip: builtins.str,
    prefix_count: builtins.str,
    prefix_length: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d3fe8669429bcf0acd9a6240edf5e37a742bbbd12aca0286c270e4b7106ba9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6791ffc45ad57dca1827ab5312358c9a75148aa63721980a6af4c05745fd2a69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ba22eb826880f199eaee0300aa3cca927b319983834372237b0d11a42c990f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fae70563beeb2f159ff3f2ae41319340cc57032d2b1fc407356e5ac8f5799ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86abbc57915995d9af7d614bd051acf2583c95c7faf08bd5f1058705a52e4bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382c3e41b032fee648146f9694a9e8fbdc0117d64d75091ac8f24f8c93a653f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpPrefixPrefix]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1f6db85407204559e60433d05cf26239e85e8a7576ec5177fb34848052ffc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6841be2660e931001e54059831c87992aa5a4721a8ffff824f34290c4bd5ba31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303b7f77b53ad900875e99aef87710af18c08e32e0869c3f188cdfaac87cb4ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257404ceff02400949aab0f614bd9deaf51f5a30a74342ca34e753630342998a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5108742ce35d103eef86e6656987431d706c4a0b1211a7b665715efd09a3a19(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpPrefixPrefix]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b18d6498fd2681786dccbb6cb570e503f7e93c047e5806a8022176988fee862(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d12db90a92faa3e67f1a6a18af7e1851b47abbbde93bcbe15e3d7fb0b1d40a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e825bb0ed0b6505677b54da8883ed922bae1394371100ee74d6458a4b69c9d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adf01ea591e1e262d479cad648e97d95d83cdc92425e8ee4bc80cd5e02487c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25ac76e01af003d77b894ba6400b70d9b2a266dd062c9de88d7e55ad1b54343(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bda59dd2e2bfe54485e6f22b6e12a2d1b61f9fe01293bc2f2045ef8d95f0a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a65e643636160e9a1b0744a4b79a2908a44e84fd73e77d67ce9db1319412cd5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IpSpaceIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8355e4fdbe3c156f6153f78403c2f206aab80f2b77ffe78623d2ead40be830(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dc0c21b9b7c613fd953dcbdc232eb966bc341b1b54a6c2a6b9c50f5889840f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40a90458bd057a5367e1404df3f3c29547423e9196519b94fc5ea49eae6a43b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac9a91d84643bc5cad20be0ded4fc793fade0b76740821109809a92af3b2a48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IpSpaceIpRange]],
) -> None:
    """Type checking stubs"""
    pass
