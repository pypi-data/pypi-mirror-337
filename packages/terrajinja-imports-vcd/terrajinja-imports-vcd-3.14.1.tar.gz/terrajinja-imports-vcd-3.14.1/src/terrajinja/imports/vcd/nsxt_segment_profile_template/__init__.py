'''
# `vcd_nsxt_segment_profile_template`

Refer to the Terraform Registry for docs: [`vcd_nsxt_segment_profile_template`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template).
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


class NsxtSegmentProfileTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtSegmentProfileTemplate.NsxtSegmentProfileTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template vcd_nsxt_segment_profile_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        nsxt_manager_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_discovery_profile_id: typing.Optional[builtins.str] = None,
        mac_discovery_profile_id: typing.Optional[builtins.str] = None,
        qos_profile_id: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template vcd_nsxt_segment_profile_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of Segment Profile Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#name NsxtSegmentProfileTemplate#name}
        :param nsxt_manager_id: NSX-T Manager ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#nsxt_manager_id NsxtSegmentProfileTemplate#nsxt_manager_id}
        :param description: Description of Segment Profile Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#description NsxtSegmentProfileTemplate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#id NsxtSegmentProfileTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_discovery_profile_id: Segment IP Discovery Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#ip_discovery_profile_id NsxtSegmentProfileTemplate#ip_discovery_profile_id}
        :param mac_discovery_profile_id: Segment MAC Discovery Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#mac_discovery_profile_id NsxtSegmentProfileTemplate#mac_discovery_profile_id}
        :param qos_profile_id: Segment QoS Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#qos_profile_id NsxtSegmentProfileTemplate#qos_profile_id}
        :param segment_security_profile_id: Segment Security Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#segment_security_profile_id NsxtSegmentProfileTemplate#segment_security_profile_id}
        :param spoof_guard_profile_id: Segment Spoof Guard Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#spoof_guard_profile_id NsxtSegmentProfileTemplate#spoof_guard_profile_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a2ec3031b497e9c8a5441c45c3ec554cd0c5c16db9020cbf0e99b3935c81ea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtSegmentProfileTemplateConfig(
            name=name,
            nsxt_manager_id=nsxt_manager_id,
            description=description,
            id=id,
            ip_discovery_profile_id=ip_discovery_profile_id,
            mac_discovery_profile_id=mac_discovery_profile_id,
            qos_profile_id=qos_profile_id,
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
        '''Generates CDKTF code for importing a NsxtSegmentProfileTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtSegmentProfileTemplate to import.
        :param import_from_id: The id of the existing NsxtSegmentProfileTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtSegmentProfileTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec54a9c091298335650a9fab7a0ec4b4201b44a04b73c6d4e51930926184503a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpDiscoveryProfileId")
    def reset_ip_discovery_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpDiscoveryProfileId", []))

    @jsii.member(jsii_name="resetMacDiscoveryProfileId")
    def reset_mac_discovery_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacDiscoveryProfileId", []))

    @jsii.member(jsii_name="resetQosProfileId")
    def reset_qos_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQosProfileId", []))

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
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerIdInput")
    def nsxt_manager_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nsxtManagerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="qosProfileIdInput")
    def qos_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qosProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentSecurityProfileIdInput")
    def segment_security_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "segmentSecurityProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="spoofGuardProfileIdInput")
    def spoof_guard_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spoofGuardProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8405b686de8c2783d413937614241246c46c3e9ba137679c62e4bca562e947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f765f3c6d7a0d546cc776a094bf7663c12c30fcab426b38c62a1d2815b4f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipDiscoveryProfileId")
    def ip_discovery_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipDiscoveryProfileId"))

    @ip_discovery_profile_id.setter
    def ip_discovery_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a74e8e037bd3345a5c0578d1023808e8b95e853de94cd1bd99be34b9a6932e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipDiscoveryProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="macDiscoveryProfileId")
    def mac_discovery_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macDiscoveryProfileId"))

    @mac_discovery_profile_id.setter
    def mac_discovery_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da2db62ac4ebc162102fbb998e308e746d3d5ce6db82dde5035064bfbb02672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macDiscoveryProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951bd66bbbfe9e7c4f68bce8ba59171ea6e7777b6361093ef925c4bdd074cb4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerId")
    def nsxt_manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nsxtManagerId"))

    @nsxt_manager_id.setter
    def nsxt_manager_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8955762c56ccc121944878f65a0f46f6d094abb437efbf4649e9498126957555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nsxtManagerId", value)

    @builtins.property
    @jsii.member(jsii_name="qosProfileId")
    def qos_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qosProfileId"))

    @qos_profile_id.setter
    def qos_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57dc7c55faf84bb2bad68005f8fc75f85fa0c6165edd79f112c65a1ac3dff879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qosProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="segmentSecurityProfileId")
    def segment_security_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segmentSecurityProfileId"))

    @segment_security_profile_id.setter
    def segment_security_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565d394412dfd61db00116b8ab1afff159e28fdecc4b5fbea625a3b41364d726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentSecurityProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="spoofGuardProfileId")
    def spoof_guard_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spoofGuardProfileId"))

    @spoof_guard_profile_id.setter
    def spoof_guard_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8122d1cabb5611ada736203fd69e43a66fdedc62ae6733d9e61cc96a71af22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spoofGuardProfileId", value)


@jsii.data_type(
    jsii_type="vcd.nsxtSegmentProfileTemplate.NsxtSegmentProfileTemplateConfig",
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
        "nsxt_manager_id": "nsxtManagerId",
        "description": "description",
        "id": "id",
        "ip_discovery_profile_id": "ipDiscoveryProfileId",
        "mac_discovery_profile_id": "macDiscoveryProfileId",
        "qos_profile_id": "qosProfileId",
        "segment_security_profile_id": "segmentSecurityProfileId",
        "spoof_guard_profile_id": "spoofGuardProfileId",
    },
)
class NsxtSegmentProfileTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        nsxt_manager_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_discovery_profile_id: typing.Optional[builtins.str] = None,
        mac_discovery_profile_id: typing.Optional[builtins.str] = None,
        qos_profile_id: typing.Optional[builtins.str] = None,
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
        :param name: Name of Segment Profile Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#name NsxtSegmentProfileTemplate#name}
        :param nsxt_manager_id: NSX-T Manager ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#nsxt_manager_id NsxtSegmentProfileTemplate#nsxt_manager_id}
        :param description: Description of Segment Profile Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#description NsxtSegmentProfileTemplate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#id NsxtSegmentProfileTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_discovery_profile_id: Segment IP Discovery Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#ip_discovery_profile_id NsxtSegmentProfileTemplate#ip_discovery_profile_id}
        :param mac_discovery_profile_id: Segment MAC Discovery Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#mac_discovery_profile_id NsxtSegmentProfileTemplate#mac_discovery_profile_id}
        :param qos_profile_id: Segment QoS Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#qos_profile_id NsxtSegmentProfileTemplate#qos_profile_id}
        :param segment_security_profile_id: Segment Security Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#segment_security_profile_id NsxtSegmentProfileTemplate#segment_security_profile_id}
        :param spoof_guard_profile_id: Segment Spoof Guard Profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#spoof_guard_profile_id NsxtSegmentProfileTemplate#spoof_guard_profile_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fb5e98aeb6b3611fc0729433985d5f7b3fa1cc9d873caff6951c1e946c2052)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nsxt_manager_id", value=nsxt_manager_id, expected_type=type_hints["nsxt_manager_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_discovery_profile_id", value=ip_discovery_profile_id, expected_type=type_hints["ip_discovery_profile_id"])
            check_type(argname="argument mac_discovery_profile_id", value=mac_discovery_profile_id, expected_type=type_hints["mac_discovery_profile_id"])
            check_type(argname="argument qos_profile_id", value=qos_profile_id, expected_type=type_hints["qos_profile_id"])
            check_type(argname="argument segment_security_profile_id", value=segment_security_profile_id, expected_type=type_hints["segment_security_profile_id"])
            check_type(argname="argument spoof_guard_profile_id", value=spoof_guard_profile_id, expected_type=type_hints["spoof_guard_profile_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "nsxt_manager_id": nsxt_manager_id,
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
        if ip_discovery_profile_id is not None:
            self._values["ip_discovery_profile_id"] = ip_discovery_profile_id
        if mac_discovery_profile_id is not None:
            self._values["mac_discovery_profile_id"] = mac_discovery_profile_id
        if qos_profile_id is not None:
            self._values["qos_profile_id"] = qos_profile_id
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
    def name(self) -> builtins.str:
        '''Name of Segment Profile Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#name NsxtSegmentProfileTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nsxt_manager_id(self) -> builtins.str:
        '''NSX-T Manager ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#nsxt_manager_id NsxtSegmentProfileTemplate#nsxt_manager_id}
        '''
        result = self._values.get("nsxt_manager_id")
        assert result is not None, "Required property 'nsxt_manager_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of Segment Profile Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#description NsxtSegmentProfileTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#id NsxtSegmentProfileTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_discovery_profile_id(self) -> typing.Optional[builtins.str]:
        '''Segment IP Discovery Profile ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#ip_discovery_profile_id NsxtSegmentProfileTemplate#ip_discovery_profile_id}
        '''
        result = self._values.get("ip_discovery_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mac_discovery_profile_id(self) -> typing.Optional[builtins.str]:
        '''Segment MAC Discovery Profile ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#mac_discovery_profile_id NsxtSegmentProfileTemplate#mac_discovery_profile_id}
        '''
        result = self._values.get("mac_discovery_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qos_profile_id(self) -> typing.Optional[builtins.str]:
        '''Segment QoS Profile ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#qos_profile_id NsxtSegmentProfileTemplate#qos_profile_id}
        '''
        result = self._values.get("qos_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_security_profile_id(self) -> typing.Optional[builtins.str]:
        '''Segment Security Profile ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#segment_security_profile_id NsxtSegmentProfileTemplate#segment_security_profile_id}
        '''
        result = self._values.get("segment_security_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spoof_guard_profile_id(self) -> typing.Optional[builtins.str]:
        '''Segment Spoof Guard Profile ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_segment_profile_template#spoof_guard_profile_id NsxtSegmentProfileTemplate#spoof_guard_profile_id}
        '''
        result = self._values.get("spoof_guard_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtSegmentProfileTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NsxtSegmentProfileTemplate",
    "NsxtSegmentProfileTemplateConfig",
]

publication.publish()

def _typecheckingstub__c5a2ec3031b497e9c8a5441c45c3ec554cd0c5c16db9020cbf0e99b3935c81ea(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    nsxt_manager_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_discovery_profile_id: typing.Optional[builtins.str] = None,
    mac_discovery_profile_id: typing.Optional[builtins.str] = None,
    qos_profile_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ec54a9c091298335650a9fab7a0ec4b4201b44a04b73c6d4e51930926184503a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8405b686de8c2783d413937614241246c46c3e9ba137679c62e4bca562e947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f765f3c6d7a0d546cc776a094bf7663c12c30fcab426b38c62a1d2815b4f26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a74e8e037bd3345a5c0578d1023808e8b95e853de94cd1bd99be34b9a6932e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da2db62ac4ebc162102fbb998e308e746d3d5ce6db82dde5035064bfbb02672(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951bd66bbbfe9e7c4f68bce8ba59171ea6e7777b6361093ef925c4bdd074cb4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8955762c56ccc121944878f65a0f46f6d094abb437efbf4649e9498126957555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57dc7c55faf84bb2bad68005f8fc75f85fa0c6165edd79f112c65a1ac3dff879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565d394412dfd61db00116b8ab1afff159e28fdecc4b5fbea625a3b41364d726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8122d1cabb5611ada736203fd69e43a66fdedc62ae6733d9e61cc96a71af22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fb5e98aeb6b3611fc0729433985d5f7b3fa1cc9d873caff6951c1e946c2052(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    nsxt_manager_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_discovery_profile_id: typing.Optional[builtins.str] = None,
    mac_discovery_profile_id: typing.Optional[builtins.str] = None,
    qos_profile_id: typing.Optional[builtins.str] = None,
    segment_security_profile_id: typing.Optional[builtins.str] = None,
    spoof_guard_profile_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
