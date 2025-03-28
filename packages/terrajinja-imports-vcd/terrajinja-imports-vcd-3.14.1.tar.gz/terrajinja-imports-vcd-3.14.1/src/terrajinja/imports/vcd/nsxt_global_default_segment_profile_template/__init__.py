'''
# `vcd_nsxt_global_default_segment_profile_template`

Refer to the Terraform Registry for docs: [`vcd_nsxt_global_default_segment_profile_template`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template).
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


class NsxtGlobalDefaultSegmentProfileTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtGlobalDefaultSegmentProfileTemplate.NsxtGlobalDefaultSegmentProfileTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template vcd_nsxt_global_default_segment_profile_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        vapp_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
        vdc_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template vcd_nsxt_global_default_segment_profile_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#id NsxtGlobalDefaultSegmentProfileTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param vapp_networks_default_segment_profile_template_id: Global default NSX-T Segment Profile for vApp networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#vapp_networks_default_segment_profile_template_id NsxtGlobalDefaultSegmentProfileTemplate#vapp_networks_default_segment_profile_template_id}
        :param vdc_networks_default_segment_profile_template_id: Global default NSX-T Segment Profile for Org VDC networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#vdc_networks_default_segment_profile_template_id NsxtGlobalDefaultSegmentProfileTemplate#vdc_networks_default_segment_profile_template_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421a4e734aa29769331852ffa1e30775101e1a50b839473fedc7577b15b87cbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtGlobalDefaultSegmentProfileTemplateConfig(
            id=id,
            vapp_networks_default_segment_profile_template_id=vapp_networks_default_segment_profile_template_id,
            vdc_networks_default_segment_profile_template_id=vdc_networks_default_segment_profile_template_id,
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
        '''Generates CDKTF code for importing a NsxtGlobalDefaultSegmentProfileTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtGlobalDefaultSegmentProfileTemplate to import.
        :param import_from_id: The id of the existing NsxtGlobalDefaultSegmentProfileTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtGlobalDefaultSegmentProfileTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430b80c768f58272d3ffe1bd716b89e670bd9bbddf7eb5cf17a6b2920d69027c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetVappNetworksDefaultSegmentProfileTemplateId")
    def reset_vapp_networks_default_segment_profile_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVappNetworksDefaultSegmentProfileTemplateId", []))

    @jsii.member(jsii_name="resetVdcNetworksDefaultSegmentProfileTemplateId")
    def reset_vdc_networks_default_segment_profile_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdcNetworksDefaultSegmentProfileTemplateId", []))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="vappNetworksDefaultSegmentProfileTemplateIdInput")
    def vapp_networks_default_segment_profile_template_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vappNetworksDefaultSegmentProfileTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcNetworksDefaultSegmentProfileTemplateIdInput")
    def vdc_networks_default_segment_profile_template_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcNetworksDefaultSegmentProfileTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ac46f4e246e810bafffcfcacca8dd9f7ea67f85dc37cb17412ca8881c34d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="vappNetworksDefaultSegmentProfileTemplateId")
    def vapp_networks_default_segment_profile_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappNetworksDefaultSegmentProfileTemplateId"))

    @vapp_networks_default_segment_profile_template_id.setter
    def vapp_networks_default_segment_profile_template_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dbe38c4e6439bcc1d8e22c8ecfa198d8c424158395bf8188027011e9f08eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappNetworksDefaultSegmentProfileTemplateId", value)

    @builtins.property
    @jsii.member(jsii_name="vdcNetworksDefaultSegmentProfileTemplateId")
    def vdc_networks_default_segment_profile_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcNetworksDefaultSegmentProfileTemplateId"))

    @vdc_networks_default_segment_profile_template_id.setter
    def vdc_networks_default_segment_profile_template_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186885c0ad91fb4c3ea9e12f150bab25e84143882d4864134315a126eba8f0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdcNetworksDefaultSegmentProfileTemplateId", value)


@jsii.data_type(
    jsii_type="vcd.nsxtGlobalDefaultSegmentProfileTemplate.NsxtGlobalDefaultSegmentProfileTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "vapp_networks_default_segment_profile_template_id": "vappNetworksDefaultSegmentProfileTemplateId",
        "vdc_networks_default_segment_profile_template_id": "vdcNetworksDefaultSegmentProfileTemplateId",
    },
)
class NsxtGlobalDefaultSegmentProfileTemplateConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        id: typing.Optional[builtins.str] = None,
        vapp_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
        vdc_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#id NsxtGlobalDefaultSegmentProfileTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param vapp_networks_default_segment_profile_template_id: Global default NSX-T Segment Profile for vApp networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#vapp_networks_default_segment_profile_template_id NsxtGlobalDefaultSegmentProfileTemplate#vapp_networks_default_segment_profile_template_id}
        :param vdc_networks_default_segment_profile_template_id: Global default NSX-T Segment Profile for Org VDC networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#vdc_networks_default_segment_profile_template_id NsxtGlobalDefaultSegmentProfileTemplate#vdc_networks_default_segment_profile_template_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0d624ac03d2fb24623edc203015854bc7564f820b7896d88a446a71688faf0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument vapp_networks_default_segment_profile_template_id", value=vapp_networks_default_segment_profile_template_id, expected_type=type_hints["vapp_networks_default_segment_profile_template_id"])
            check_type(argname="argument vdc_networks_default_segment_profile_template_id", value=vdc_networks_default_segment_profile_template_id, expected_type=type_hints["vdc_networks_default_segment_profile_template_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if vapp_networks_default_segment_profile_template_id is not None:
            self._values["vapp_networks_default_segment_profile_template_id"] = vapp_networks_default_segment_profile_template_id
        if vdc_networks_default_segment_profile_template_id is not None:
            self._values["vdc_networks_default_segment_profile_template_id"] = vdc_networks_default_segment_profile_template_id

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#id NsxtGlobalDefaultSegmentProfileTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vapp_networks_default_segment_profile_template_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Global default NSX-T Segment Profile for vApp networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#vapp_networks_default_segment_profile_template_id NsxtGlobalDefaultSegmentProfileTemplate#vapp_networks_default_segment_profile_template_id}
        '''
        result = self._values.get("vapp_networks_default_segment_profile_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc_networks_default_segment_profile_template_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Global default NSX-T Segment Profile for Org VDC networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_global_default_segment_profile_template#vdc_networks_default_segment_profile_template_id NsxtGlobalDefaultSegmentProfileTemplate#vdc_networks_default_segment_profile_template_id}
        '''
        result = self._values.get("vdc_networks_default_segment_profile_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtGlobalDefaultSegmentProfileTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NsxtGlobalDefaultSegmentProfileTemplate",
    "NsxtGlobalDefaultSegmentProfileTemplateConfig",
]

publication.publish()

def _typecheckingstub__421a4e734aa29769331852ffa1e30775101e1a50b839473fedc7577b15b87cbf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    vapp_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
    vdc_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__430b80c768f58272d3ffe1bd716b89e670bd9bbddf7eb5cf17a6b2920d69027c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ac46f4e246e810bafffcfcacca8dd9f7ea67f85dc37cb17412ca8881c34d69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dbe38c4e6439bcc1d8e22c8ecfa198d8c424158395bf8188027011e9f08eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186885c0ad91fb4c3ea9e12f150bab25e84143882d4864134315a126eba8f0f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0d624ac03d2fb24623edc203015854bc7564f820b7896d88a446a71688faf0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    vapp_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
    vdc_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
