'''
# `vcd_nsxt_network_segment_profile`

Refer to the Terraform Registry for docs: [`vcd_nsxt_network_segment_profile`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile).
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


class NsxtNetworkSegmentProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtNetworkSegmentProfile.NsxtNetworkSegmentProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile vcd_nsxt_network_segment_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        org_network_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        ip_discovery_profile_id: typing.Optional[builtins.str] = None,
        mac_discovery_profile_id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        qos_profile_id: typing.Optional[builtins.str] = None,
        segment_profile_template_id: typing.Optional[builtins.str] = None,
        segment_security_profile_id: typing.Optional[builtins.str] = None,
        spoof_guard_profile_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile vcd_nsxt_network_segment_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param org_network_id: ID of the Organization Network that will have the segment profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#org_network_id NsxtNetworkSegmentProfile#org_network_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#id NsxtNetworkSegmentProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_discovery_profile_id: NSX-T IP Discovery Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#ip_discovery_profile_id NsxtNetworkSegmentProfile#ip_discovery_profile_id}
        :param mac_discovery_profile_id: NSX-T Mac Discovery Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#mac_discovery_profile_id NsxtNetworkSegmentProfile#mac_discovery_profile_id}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#org NsxtNetworkSegmentProfile#org}
        :param qos_profile_id: NSX-T QoS Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#qos_profile_id NsxtNetworkSegmentProfile#qos_profile_id}
        :param segment_profile_template_id: Segment Profile Template ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#segment_profile_template_id NsxtNetworkSegmentProfile#segment_profile_template_id}
        :param segment_security_profile_id: NSX-T Segment Security Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#segment_security_profile_id NsxtNetworkSegmentProfile#segment_security_profile_id}
        :param spoof_guard_profile_id: NSX-T Spoof Guard Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#spoof_guard_profile_id NsxtNetworkSegmentProfile#spoof_guard_profile_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe3c72315a6cf76d4cb5f6dc65e8962db1eb27dbf56b07dc6697d8efaf6e661)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtNetworkSegmentProfileConfig(
            org_network_id=org_network_id,
            id=id,
            ip_discovery_profile_id=ip_discovery_profile_id,
            mac_discovery_profile_id=mac_discovery_profile_id,
            org=org,
            qos_profile_id=qos_profile_id,
            segment_profile_template_id=segment_profile_template_id,
            segment_security_profile_id=segment_security_profile_id,
            spoof_guard_profile_id=spoof_guard_profile_id,
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
        '''Generates CDKTF code for importing a NsxtNetworkSegmentProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtNetworkSegmentProfile to import.
        :param import_from_id: The id of the existing NsxtNetworkSegmentProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtNetworkSegmentProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a60370d7f26141f6ec743badcc1e30e9f05e1fbe79b788a309963a0d1a3444)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpDiscoveryProfileId")
    def reset_ip_discovery_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpDiscoveryProfileId", []))

    @jsii.member(jsii_name="resetMacDiscoveryProfileId")
    def reset_mac_discovery_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacDiscoveryProfileId", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetQosProfileId")
    def reset_qos_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQosProfileId", []))

    @jsii.member(jsii_name="resetSegmentProfileTemplateId")
    def reset_segment_profile_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegmentProfileTemplateId", []))

    @jsii.member(jsii_name="resetSegmentSecurityProfileId")
    def reset_segment_security_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegmentSecurityProfileId", []))

    @jsii.member(jsii_name="resetSpoofGuardProfileId")
    def reset_spoof_guard_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpoofGuardProfileId", []))

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
    @jsii.member(jsii_name="segmentProfileTemplateName")
    def segment_profile_template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segmentProfileTemplateName"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipDiscoveryProfileIdInput")
    def ip_discovery_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipDiscoveryProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="macDiscoveryProfileIdInput")
    def mac_discovery_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macDiscoveryProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="orgNetworkIdInput")
    def org_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="qosProfileIdInput")
    def qos_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qosProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentProfileTemplateIdInput")
    def segment_profile_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "segmentProfileTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentSecurityProfileIdInput")
    def segment_security_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "segmentSecurityProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="spoofGuardProfileIdInput")
    def spoof_guard_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spoofGuardProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc02e9f1ae1d53f1cddffc9b66ab408484f2f1cf192d440225ab2f15feeb642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipDiscoveryProfileId")
    def ip_discovery_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipDiscoveryProfileId"))

    @ip_discovery_profile_id.setter
    def ip_discovery_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3077fd80fabd7694bbc40e488c7597aadf0bb688e0941f850c5ec3014134ed3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipDiscoveryProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="macDiscoveryProfileId")
    def mac_discovery_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macDiscoveryProfileId"))

    @mac_discovery_profile_id.setter
    def mac_discovery_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca946bc6581d59600986d2789eda619fc9b2522061bb30d85d461debba3c1c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macDiscoveryProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb2ae98b0088ba0214efedd2adb4b7c5b9e609f9386e297af3f8507a8a81928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="orgNetworkId")
    def org_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgNetworkId"))

    @org_network_id.setter
    def org_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee81a640fdd026f7711920cb7e8c7891615c6c34a555ea0abd7b2b5f8a19d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="qosProfileId")
    def qos_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qosProfileId"))

    @qos_profile_id.setter
    def qos_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e27dd28523f25d3813f13f96877f9e2624d948bbf12c20778ec6cb2b9cf691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qosProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="segmentProfileTemplateId")
    def segment_profile_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segmentProfileTemplateId"))

    @segment_profile_template_id.setter
    def segment_profile_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ecb83407c04a255ca32ceb26dd69f56b4abf717122d364115bcb5ec2327804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentProfileTemplateId", value)

    @builtins.property
    @jsii.member(jsii_name="segmentSecurityProfileId")
    def segment_security_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segmentSecurityProfileId"))

    @segment_security_profile_id.setter
    def segment_security_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82ada73636528a5b093e4807a920e842871161be6079ccf5e2c3e558327b5a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentSecurityProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="spoofGuardProfileId")
    def spoof_guard_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spoofGuardProfileId"))

    @spoof_guard_profile_id.setter
    def spoof_guard_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6998d6e616ca3e27a3dd918590b820f6863d7e9e0fff25cfd3d5d7479ad64b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spoofGuardProfileId", value)


@jsii.data_type(
    jsii_type="vcd.nsxtNetworkSegmentProfile.NsxtNetworkSegmentProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "org_network_id": "orgNetworkId",
        "id": "id",
        "ip_discovery_profile_id": "ipDiscoveryProfileId",
        "mac_discovery_profile_id": "macDiscoveryProfileId",
        "org": "org",
        "qos_profile_id": "qosProfileId",
        "segment_profile_template_id": "segmentProfileTemplateId",
        "segment_security_profile_id": "segmentSecurityProfileId",
        "spoof_guard_profile_id": "spoofGuardProfileId",
    },
)
class NsxtNetworkSegmentProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        org_network_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        ip_discovery_profile_id: typing.Optional[builtins.str] = None,
        mac_discovery_profile_id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        qos_profile_id: typing.Optional[builtins.str] = None,
        segment_profile_template_id: typing.Optional[builtins.str] = None,
        segment_security_profile_id: typing.Optional[builtins.str] = None,
        spoof_guard_profile_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param org_network_id: ID of the Organization Network that will have the segment profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#org_network_id NsxtNetworkSegmentProfile#org_network_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#id NsxtNetworkSegmentProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_discovery_profile_id: NSX-T IP Discovery Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#ip_discovery_profile_id NsxtNetworkSegmentProfile#ip_discovery_profile_id}
        :param mac_discovery_profile_id: NSX-T Mac Discovery Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#mac_discovery_profile_id NsxtNetworkSegmentProfile#mac_discovery_profile_id}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#org NsxtNetworkSegmentProfile#org}
        :param qos_profile_id: NSX-T QoS Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#qos_profile_id NsxtNetworkSegmentProfile#qos_profile_id}
        :param segment_profile_template_id: Segment Profile Template ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#segment_profile_template_id NsxtNetworkSegmentProfile#segment_profile_template_id}
        :param segment_security_profile_id: NSX-T Segment Security Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#segment_security_profile_id NsxtNetworkSegmentProfile#segment_security_profile_id}
        :param spoof_guard_profile_id: NSX-T Spoof Guard Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#spoof_guard_profile_id NsxtNetworkSegmentProfile#spoof_guard_profile_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a81072c61acff5b4388c957066747309b1c4e6689ef0e10abe82851347d700)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument org_network_id", value=org_network_id, expected_type=type_hints["org_network_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_discovery_profile_id", value=ip_discovery_profile_id, expected_type=type_hints["ip_discovery_profile_id"])
            check_type(argname="argument mac_discovery_profile_id", value=mac_discovery_profile_id, expected_type=type_hints["mac_discovery_profile_id"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument qos_profile_id", value=qos_profile_id, expected_type=type_hints["qos_profile_id"])
            check_type(argname="argument segment_profile_template_id", value=segment_profile_template_id, expected_type=type_hints["segment_profile_template_id"])
            check_type(argname="argument segment_security_profile_id", value=segment_security_profile_id, expected_type=type_hints["segment_security_profile_id"])
            check_type(argname="argument spoof_guard_profile_id", value=spoof_guard_profile_id, expected_type=type_hints["spoof_guard_profile_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if id is not None:
            self._values["id"] = id
        if ip_discovery_profile_id is not None:
            self._values["ip_discovery_profile_id"] = ip_discovery_profile_id
        if mac_discovery_profile_id is not None:
            self._values["mac_discovery_profile_id"] = mac_discovery_profile_id
        if org is not None:
            self._values["org"] = org
        if qos_profile_id is not None:
            self._values["qos_profile_id"] = qos_profile_id
        if segment_profile_template_id is not None:
            self._values["segment_profile_template_id"] = segment_profile_template_id
        if segment_security_profile_id is not None:
            self._values["segment_security_profile_id"] = segment_security_profile_id
        if spoof_guard_profile_id is not None:
            self._values["spoof_guard_profile_id"] = spoof_guard_profile_id

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
    def org_network_id(self) -> builtins.str:
        '''ID of the Organization Network that will have the segment profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#org_network_id NsxtNetworkSegmentProfile#org_network_id}
        '''
        result = self._values.get("org_network_id")
        assert result is not None, "Required property 'org_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#id NsxtNetworkSegmentProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_discovery_profile_id(self) -> typing.Optional[builtins.str]:
        '''NSX-T IP Discovery Profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#ip_discovery_profile_id NsxtNetworkSegmentProfile#ip_discovery_profile_id}
        '''
        result = self._values.get("ip_discovery_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mac_discovery_profile_id(self) -> typing.Optional[builtins.str]:
        '''NSX-T Mac Discovery Profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#mac_discovery_profile_id NsxtNetworkSegmentProfile#mac_discovery_profile_id}
        '''
        result = self._values.get("mac_discovery_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#org NsxtNetworkSegmentProfile#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qos_profile_id(self) -> typing.Optional[builtins.str]:
        '''NSX-T QoS Profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#qos_profile_id NsxtNetworkSegmentProfile#qos_profile_id}
        '''
        result = self._values.get("qos_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_profile_template_id(self) -> typing.Optional[builtins.str]:
        '''Segment Profile Template ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#segment_profile_template_id NsxtNetworkSegmentProfile#segment_profile_template_id}
        '''
        result = self._values.get("segment_profile_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_security_profile_id(self) -> typing.Optional[builtins.str]:
        '''NSX-T Segment Security Profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#segment_security_profile_id NsxtNetworkSegmentProfile#segment_security_profile_id}
        '''
        result = self._values.get("segment_security_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spoof_guard_profile_id(self) -> typing.Optional[builtins.str]:
        '''NSX-T Spoof Guard Profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_network_segment_profile#spoof_guard_profile_id NsxtNetworkSegmentProfile#spoof_guard_profile_id}
        '''
        result = self._values.get("spoof_guard_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtNetworkSegmentProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NsxtNetworkSegmentProfile",
    "NsxtNetworkSegmentProfileConfig",
]

publication.publish()

def _typecheckingstub__1fe3c72315a6cf76d4cb5f6dc65e8962db1eb27dbf56b07dc6697d8efaf6e661(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    org_network_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    ip_discovery_profile_id: typing.Optional[builtins.str] = None,
    mac_discovery_profile_id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    qos_profile_id: typing.Optional[builtins.str] = None,
    segment_profile_template_id: typing.Optional[builtins.str] = None,
    segment_security_profile_id: typing.Optional[builtins.str] = None,
    spoof_guard_profile_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__56a60370d7f26141f6ec743badcc1e30e9f05e1fbe79b788a309963a0d1a3444(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc02e9f1ae1d53f1cddffc9b66ab408484f2f1cf192d440225ab2f15feeb642(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3077fd80fabd7694bbc40e488c7597aadf0bb688e0941f850c5ec3014134ed3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca946bc6581d59600986d2789eda619fc9b2522061bb30d85d461debba3c1c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb2ae98b0088ba0214efedd2adb4b7c5b9e609f9386e297af3f8507a8a81928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee81a640fdd026f7711920cb7e8c7891615c6c34a555ea0abd7b2b5f8a19d60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e27dd28523f25d3813f13f96877f9e2624d948bbf12c20778ec6cb2b9cf691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ecb83407c04a255ca32ceb26dd69f56b4abf717122d364115bcb5ec2327804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ada73636528a5b093e4807a920e842871161be6079ccf5e2c3e558327b5a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6998d6e616ca3e27a3dd918590b820f6863d7e9e0fff25cfd3d5d7479ad64b7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a81072c61acff5b4388c957066747309b1c4e6689ef0e10abe82851347d700(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org_network_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    ip_discovery_profile_id: typing.Optional[builtins.str] = None,
    mac_discovery_profile_id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    qos_profile_id: typing.Optional[builtins.str] = None,
    segment_profile_template_id: typing.Optional[builtins.str] = None,
    segment_security_profile_id: typing.Optional[builtins.str] = None,
    spoof_guard_profile_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
