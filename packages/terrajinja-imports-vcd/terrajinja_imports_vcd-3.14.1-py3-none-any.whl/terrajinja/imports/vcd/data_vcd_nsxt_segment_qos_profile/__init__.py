'''
# `data_vcd_nsxt_segment_qos_profile`

Refer to the Terraform Registry for docs: [`data_vcd_nsxt_segment_qos_profile`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile).
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


class DataVcdNsxtSegmentQosProfile(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtSegmentQosProfile.DataVcdNsxtSegmentQosProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile vcd_nsxt_segment_qos_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        nsxt_manager_id: typing.Optional[builtins.str] = None,
        vdc_group_id: typing.Optional[builtins.str] = None,
        vdc_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile vcd_nsxt_segment_qos_profile} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of Segment QoS Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#name DataVcdNsxtSegmentQosProfile#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#id DataVcdNsxtSegmentQosProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param nsxt_manager_id: ID of NSX-T Manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#nsxt_manager_id DataVcdNsxtSegmentQosProfile#nsxt_manager_id}
        :param vdc_group_id: ID of VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#vdc_group_id DataVcdNsxtSegmentQosProfile#vdc_group_id}
        :param vdc_id: ID of VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#vdc_id DataVcdNsxtSegmentQosProfile#vdc_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85105da6f12a254def6cb89f9a50f5ee9f870666e1742b230ae9dff3d1cd0ea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataVcdNsxtSegmentQosProfileConfig(
            name=name,
            id=id,
            nsxt_manager_id=nsxt_manager_id,
            vdc_group_id=vdc_group_id,
            vdc_id=vdc_id,
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
        '''Generates CDKTF code for importing a DataVcdNsxtSegmentQosProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataVcdNsxtSegmentQosProfile to import.
        :param import_from_id: The id of the existing DataVcdNsxtSegmentQosProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataVcdNsxtSegmentQosProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ea9a05810177c49fec87435780893ce4b80288052ddc3497a26b9ec72a4643)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNsxtManagerId")
    def reset_nsxt_manager_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNsxtManagerId", []))

    @jsii.member(jsii_name="resetVdcGroupId")
    def reset_vdc_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdcGroupId", []))

    @jsii.member(jsii_name="resetVdcId")
    def reset_vdc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdcId", []))

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
    @jsii.member(jsii_name="classOfService")
    def class_of_service(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "classOfService"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="dscpPriority")
    def dscp_priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dscpPriority"))

    @builtins.property
    @jsii.member(jsii_name="dscpTrustMode")
    def dscp_trust_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dscpTrustMode"))

    @builtins.property
    @jsii.member(jsii_name="egressRateLimiterAvgBandwidth")
    def egress_rate_limiter_avg_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "egressRateLimiterAvgBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="egressRateLimiterBurstSize")
    def egress_rate_limiter_burst_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "egressRateLimiterBurstSize"))

    @builtins.property
    @jsii.member(jsii_name="egressRateLimiterPeakBandwidth")
    def egress_rate_limiter_peak_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "egressRateLimiterPeakBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="ingressBroadcastRateLimiterAvgBandwidth")
    def ingress_broadcast_rate_limiter_avg_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressBroadcastRateLimiterAvgBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="ingressBroadcastRateLimiterBurstSize")
    def ingress_broadcast_rate_limiter_burst_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressBroadcastRateLimiterBurstSize"))

    @builtins.property
    @jsii.member(jsii_name="ingressBroadcastRateLimiterPeakBandwidth")
    def ingress_broadcast_rate_limiter_peak_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressBroadcastRateLimiterPeakBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="ingressRateLimiterAvgBandwidth")
    def ingress_rate_limiter_avg_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressRateLimiterAvgBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="ingressRateLimiterBurstSize")
    def ingress_rate_limiter_burst_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressRateLimiterBurstSize"))

    @builtins.property
    @jsii.member(jsii_name="ingressRateLimiterPeakBandwidth")
    def ingress_rate_limiter_peak_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressRateLimiterPeakBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerIdInput")
    def nsxt_manager_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nsxtManagerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcGroupIdInput")
    def vdc_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcIdInput")
    def vdc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb8d09c4857b0481a95ca2934fbbbec60407ba5ad07b71b7f4f53ee923d9c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e948679d5b49f3deed9cb49b57cea9b576ca3638aa440e5f94655fb81db7863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerId")
    def nsxt_manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nsxtManagerId"))

    @nsxt_manager_id.setter
    def nsxt_manager_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718787b7ce7917e9f7adcbaa94f60b3a18a3d325b25e721a6a6e28876ce64bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nsxtManagerId", value)

    @builtins.property
    @jsii.member(jsii_name="vdcGroupId")
    def vdc_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcGroupId"))

    @vdc_group_id.setter
    def vdc_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2021c6bd68cdcd1ea7319fe1adfb868aad9e1ba0ff319ec7c5221e14417a63e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdcGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="vdcId")
    def vdc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcId"))

    @vdc_id.setter
    def vdc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a067b3979c86eff5f88939be85b702f570d88a2d9d07b5ad90bf5fa8e2b48922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdcId", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtSegmentQosProfile.DataVcdNsxtSegmentQosProfileConfig",
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
        "id": "id",
        "nsxt_manager_id": "nsxtManagerId",
        "vdc_group_id": "vdcGroupId",
        "vdc_id": "vdcId",
    },
)
class DataVcdNsxtSegmentQosProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        nsxt_manager_id: typing.Optional[builtins.str] = None,
        vdc_group_id: typing.Optional[builtins.str] = None,
        vdc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of Segment QoS Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#name DataVcdNsxtSegmentQosProfile#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#id DataVcdNsxtSegmentQosProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param nsxt_manager_id: ID of NSX-T Manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#nsxt_manager_id DataVcdNsxtSegmentQosProfile#nsxt_manager_id}
        :param vdc_group_id: ID of VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#vdc_group_id DataVcdNsxtSegmentQosProfile#vdc_group_id}
        :param vdc_id: ID of VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#vdc_id DataVcdNsxtSegmentQosProfile#vdc_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77793f0df4bf1585a356e7f82a42a2eea77bb890f91738a7a05d255d1d0ae6bd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument nsxt_manager_id", value=nsxt_manager_id, expected_type=type_hints["nsxt_manager_id"])
            check_type(argname="argument vdc_group_id", value=vdc_group_id, expected_type=type_hints["vdc_group_id"])
            check_type(argname="argument vdc_id", value=vdc_id, expected_type=type_hints["vdc_id"])
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
        if id is not None:
            self._values["id"] = id
        if nsxt_manager_id is not None:
            self._values["nsxt_manager_id"] = nsxt_manager_id
        if vdc_group_id is not None:
            self._values["vdc_group_id"] = vdc_group_id
        if vdc_id is not None:
            self._values["vdc_id"] = vdc_id

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
        '''Name of Segment QoS Profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#name DataVcdNsxtSegmentQosProfile#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#id DataVcdNsxtSegmentQosProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nsxt_manager_id(self) -> typing.Optional[builtins.str]:
        '''ID of NSX-T Manager.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#nsxt_manager_id DataVcdNsxtSegmentQosProfile#nsxt_manager_id}
        '''
        result = self._values.get("nsxt_manager_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc_group_id(self) -> typing.Optional[builtins.str]:
        '''ID of VDC Group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#vdc_group_id DataVcdNsxtSegmentQosProfile#vdc_group_id}
        '''
        result = self._values.get("vdc_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc_id(self) -> typing.Optional[builtins.str]:
        '''ID of VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_qos_profile#vdc_id DataVcdNsxtSegmentQosProfile#vdc_id}
        '''
        result = self._values.get("vdc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtSegmentQosProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataVcdNsxtSegmentQosProfile",
    "DataVcdNsxtSegmentQosProfileConfig",
]

publication.publish()

def _typecheckingstub__f85105da6f12a254def6cb89f9a50f5ee9f870666e1742b230ae9dff3d1cd0ea(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    nsxt_manager_id: typing.Optional[builtins.str] = None,
    vdc_group_id: typing.Optional[builtins.str] = None,
    vdc_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__26ea9a05810177c49fec87435780893ce4b80288052ddc3497a26b9ec72a4643(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb8d09c4857b0481a95ca2934fbbbec60407ba5ad07b71b7f4f53ee923d9c3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e948679d5b49f3deed9cb49b57cea9b576ca3638aa440e5f94655fb81db7863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718787b7ce7917e9f7adcbaa94f60b3a18a3d325b25e721a6a6e28876ce64bea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2021c6bd68cdcd1ea7319fe1adfb868aad9e1ba0ff319ec7c5221e14417a63e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a067b3979c86eff5f88939be85b702f570d88a2d9d07b5ad90bf5fa8e2b48922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77793f0df4bf1585a356e7f82a42a2eea77bb890f91738a7a05d255d1d0ae6bd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    nsxt_manager_id: typing.Optional[builtins.str] = None,
    vdc_group_id: typing.Optional[builtins.str] = None,
    vdc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
