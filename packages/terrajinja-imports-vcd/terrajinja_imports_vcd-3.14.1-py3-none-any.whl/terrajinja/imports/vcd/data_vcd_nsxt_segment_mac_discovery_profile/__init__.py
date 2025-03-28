'''
# `data_vcd_nsxt_segment_mac_discovery_profile`

Refer to the Terraform Registry for docs: [`data_vcd_nsxt_segment_mac_discovery_profile`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile).
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


class DataVcdNsxtSegmentMacDiscoveryProfile(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtSegmentMacDiscoveryProfile.DataVcdNsxtSegmentMacDiscoveryProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile vcd_nsxt_segment_mac_discovery_profile}.'''

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
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile vcd_nsxt_segment_mac_discovery_profile} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of Segment MAC Discovery Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#name DataVcdNsxtSegmentMacDiscoveryProfile#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#id DataVcdNsxtSegmentMacDiscoveryProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param nsxt_manager_id: ID of NSX-T Manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#nsxt_manager_id DataVcdNsxtSegmentMacDiscoveryProfile#nsxt_manager_id}
        :param vdc_group_id: ID of VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#vdc_group_id DataVcdNsxtSegmentMacDiscoveryProfile#vdc_group_id}
        :param vdc_id: ID of VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#vdc_id DataVcdNsxtSegmentMacDiscoveryProfile#vdc_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb874550bafa02e31515ce3e6400af017e6b69457472c7ad85797287d28576bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataVcdNsxtSegmentMacDiscoveryProfileConfig(
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
        '''Generates CDKTF code for importing a DataVcdNsxtSegmentMacDiscoveryProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataVcdNsxtSegmentMacDiscoveryProfile to import.
        :param import_from_id: The id of the existing DataVcdNsxtSegmentMacDiscoveryProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataVcdNsxtSegmentMacDiscoveryProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa37f7fb3fc504caf6e979f3a45c90fc06cea79be393750c3f36e18d040b5e5)
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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="isMacChangeEnabled")
    def is_mac_change_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isMacChangeEnabled"))

    @builtins.property
    @jsii.member(jsii_name="isMacLearningEnabled")
    def is_mac_learning_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isMacLearningEnabled"))

    @builtins.property
    @jsii.member(jsii_name="isUnknownUnicastFloodingEnabled")
    def is_unknown_unicast_flooding_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isUnknownUnicastFloodingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="macLearningAgingTime")
    def mac_learning_aging_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "macLearningAgingTime"))

    @builtins.property
    @jsii.member(jsii_name="macLimit")
    def mac_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "macLimit"))

    @builtins.property
    @jsii.member(jsii_name="macPolicy")
    def mac_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macPolicy"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bd55105a9fb4c873b89c577466a5f64839370313b27ba9caabf7eada71c9726a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43c0f3ef16faa63f706a9e3f938241f7fa6e7caee92dd4fe0ee846d80b123f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerId")
    def nsxt_manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nsxtManagerId"))

    @nsxt_manager_id.setter
    def nsxt_manager_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c39bf5280af592be3791c45502e99b8fe42925d0540b78b04c34c2faefa73e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nsxtManagerId", value)

    @builtins.property
    @jsii.member(jsii_name="vdcGroupId")
    def vdc_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcGroupId"))

    @vdc_group_id.setter
    def vdc_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cd914c8500ed7ed90c1ca971bc2bd24aaecee91c7dfc4bbfa43833a4e44436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdcGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="vdcId")
    def vdc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcId"))

    @vdc_id.setter
    def vdc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61491f482ee08a4423b31eaa597f049744438a2cd8bbec70effebbb9622caf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdcId", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtSegmentMacDiscoveryProfile.DataVcdNsxtSegmentMacDiscoveryProfileConfig",
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
class DataVcdNsxtSegmentMacDiscoveryProfileConfig(
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
        :param name: Name of Segment MAC Discovery Profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#name DataVcdNsxtSegmentMacDiscoveryProfile#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#id DataVcdNsxtSegmentMacDiscoveryProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param nsxt_manager_id: ID of NSX-T Manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#nsxt_manager_id DataVcdNsxtSegmentMacDiscoveryProfile#nsxt_manager_id}
        :param vdc_group_id: ID of VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#vdc_group_id DataVcdNsxtSegmentMacDiscoveryProfile#vdc_group_id}
        :param vdc_id: ID of VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#vdc_id DataVcdNsxtSegmentMacDiscoveryProfile#vdc_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b1adcff49c750cab0d9563b849cce141d667df01a7c31868e8bfd1f826c821)
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
        '''Name of Segment MAC Discovery Profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#name DataVcdNsxtSegmentMacDiscoveryProfile#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#id DataVcdNsxtSegmentMacDiscoveryProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nsxt_manager_id(self) -> typing.Optional[builtins.str]:
        '''ID of NSX-T Manager.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#nsxt_manager_id DataVcdNsxtSegmentMacDiscoveryProfile#nsxt_manager_id}
        '''
        result = self._values.get("nsxt_manager_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc_group_id(self) -> typing.Optional[builtins.str]:
        '''ID of VDC Group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#vdc_group_id DataVcdNsxtSegmentMacDiscoveryProfile#vdc_group_id}
        '''
        result = self._values.get("vdc_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc_id(self) -> typing.Optional[builtins.str]:
        '''ID of VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_segment_mac_discovery_profile#vdc_id DataVcdNsxtSegmentMacDiscoveryProfile#vdc_id}
        '''
        result = self._values.get("vdc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtSegmentMacDiscoveryProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataVcdNsxtSegmentMacDiscoveryProfile",
    "DataVcdNsxtSegmentMacDiscoveryProfileConfig",
]

publication.publish()

def _typecheckingstub__eb874550bafa02e31515ce3e6400af017e6b69457472c7ad85797287d28576bd(
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

def _typecheckingstub__3fa37f7fb3fc504caf6e979f3a45c90fc06cea79be393750c3f36e18d040b5e5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd55105a9fb4c873b89c577466a5f64839370313b27ba9caabf7eada71c9726a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43c0f3ef16faa63f706a9e3f938241f7fa6e7caee92dd4fe0ee846d80b123f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c39bf5280af592be3791c45502e99b8fe42925d0540b78b04c34c2faefa73e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cd914c8500ed7ed90c1ca971bc2bd24aaecee91c7dfc4bbfa43833a4e44436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61491f482ee08a4423b31eaa597f049744438a2cd8bbec70effebbb9622caf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b1adcff49c750cab0d9563b849cce141d667df01a7c31868e8bfd1f826c821(
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
