'''
# `vcd_nsxt_alb_service_engine_group`

Refer to the Terraform Registry for docs: [`vcd_nsxt_alb_service_engine_group`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group).
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


class NsxtAlbServiceEngineGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbServiceEngineGroup.NsxtAlbServiceEngineGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group vcd_nsxt_alb_service_engine_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        alb_cloud_id: builtins.str,
        importable_service_engine_group_name: builtins.str,
        name: builtins.str,
        reservation_model: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        overallocated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supported_feature_set: typing.Optional[builtins.str] = None,
        sync_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group vcd_nsxt_alb_service_engine_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alb_cloud_id: NSX-T ALB backing Cloud ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#alb_cloud_id NsxtAlbServiceEngineGroup#alb_cloud_id}
        :param importable_service_engine_group_name: NSX-T ALB Importable Service Engine Group Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#importable_service_engine_group_name NsxtAlbServiceEngineGroup#importable_service_engine_group_name}
        :param name: NSX-T ALB Service Engine Group name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#name NsxtAlbServiceEngineGroup#name}
        :param reservation_model: NSX-T ALB Service Engine Group reservation model. One of 'DEDICATED', 'SHARED'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#reservation_model NsxtAlbServiceEngineGroup#reservation_model}
        :param description: NSX-T ALB Service Engine Group description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#description NsxtAlbServiceEngineGroup#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#id NsxtAlbServiceEngineGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param overallocated: Boolean value that shows if virtual services are overallocated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#overallocated NsxtAlbServiceEngineGroup#overallocated}
        :param supported_feature_set: Feature set for this ALB Service Engine Group. One of 'STANDARD', 'PREMIUM'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#supported_feature_set NsxtAlbServiceEngineGroup#supported_feature_set}
        :param sync_on_refresh: Boolean value that shows if sync should be performed on every refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#sync_on_refresh NsxtAlbServiceEngineGroup#sync_on_refresh}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78155293664f0efa62c2f9d36ea465d562e7f06a3cb9e09a113728e57fcc8452)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtAlbServiceEngineGroupConfig(
            alb_cloud_id=alb_cloud_id,
            importable_service_engine_group_name=importable_service_engine_group_name,
            name=name,
            reservation_model=reservation_model,
            description=description,
            id=id,
            overallocated=overallocated,
            supported_feature_set=supported_feature_set,
            sync_on_refresh=sync_on_refresh,
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
        '''Generates CDKTF code for importing a NsxtAlbServiceEngineGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtAlbServiceEngineGroup to import.
        :param import_from_id: The id of the existing NsxtAlbServiceEngineGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtAlbServiceEngineGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e87370640c0527e201ce252869a9f177d3f9a3a891b4895f92c38c8be9aa1f)
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

    @jsii.member(jsii_name="resetOverallocated")
    def reset_overallocated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverallocated", []))

    @jsii.member(jsii_name="resetSupportedFeatureSet")
    def reset_supported_feature_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportedFeatureSet", []))

    @jsii.member(jsii_name="resetSyncOnRefresh")
    def reset_sync_on_refresh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncOnRefresh", []))

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
    @jsii.member(jsii_name="deployedVirtualServices")
    def deployed_virtual_services(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deployedVirtualServices"))

    @builtins.property
    @jsii.member(jsii_name="haMode")
    def ha_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haMode"))

    @builtins.property
    @jsii.member(jsii_name="maxVirtualServices")
    def max_virtual_services(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxVirtualServices"))

    @builtins.property
    @jsii.member(jsii_name="reservedVirtualServices")
    def reserved_virtual_services(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reservedVirtualServices"))

    @builtins.property
    @jsii.member(jsii_name="albCloudIdInput")
    def alb_cloud_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "albCloudIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importableServiceEngineGroupNameInput")
    def importable_service_engine_group_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importableServiceEngineGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overallocatedInput")
    def overallocated_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overallocatedInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationModelInput")
    def reservation_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservationModelInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedFeatureSetInput")
    def supported_feature_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportedFeatureSetInput"))

    @builtins.property
    @jsii.member(jsii_name="syncOnRefreshInput")
    def sync_on_refresh_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncOnRefreshInput"))

    @builtins.property
    @jsii.member(jsii_name="albCloudId")
    def alb_cloud_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "albCloudId"))

    @alb_cloud_id.setter
    def alb_cloud_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9fb85845018e86c2d99d8a77f7dc19eddc8c2cd1ea3ed06e1c1fad007a12f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "albCloudId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221841989608cdf07c598c30d5dc0d21fef572ae692492753699618665292ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ccdc2cb794126595c258781a3244df060f8d91dab3318d13eaf1bbe19fbc2aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="importableServiceEngineGroupName")
    def importable_service_engine_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importableServiceEngineGroupName"))

    @importable_service_engine_group_name.setter
    def importable_service_engine_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f29d58f7c3ab021415032d6db0abde31522c4deed9cf450ca9816c420dba7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importableServiceEngineGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2326061900014ed97e12c342415319c8923a6ae7aa106db08bdbdeb383eca568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="overallocated")
    def overallocated(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overallocated"))

    @overallocated.setter
    def overallocated(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40c37d0e021d93628f04d0298ebc1871025199d7b90c66f6774cd9b5c8575cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overallocated", value)

    @builtins.property
    @jsii.member(jsii_name="reservationModel")
    def reservation_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationModel"))

    @reservation_model.setter
    def reservation_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853e3b84aa7d4adf2eaafe2cd9c12106056a5c2ca455bdf25c0fb6721448e3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationModel", value)

    @builtins.property
    @jsii.member(jsii_name="supportedFeatureSet")
    def supported_feature_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportedFeatureSet"))

    @supported_feature_set.setter
    def supported_feature_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5073fa15c93fc20e6501df38b174664043f4c09e5ac0e761b5c0755e4435f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedFeatureSet", value)

    @builtins.property
    @jsii.member(jsii_name="syncOnRefresh")
    def sync_on_refresh(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncOnRefresh"))

    @sync_on_refresh.setter
    def sync_on_refresh(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eed1c7621366b6ef69af0d3d33d99c1810c7faf2cc15015c97307b9122f496d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncOnRefresh", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbServiceEngineGroup.NsxtAlbServiceEngineGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "alb_cloud_id": "albCloudId",
        "importable_service_engine_group_name": "importableServiceEngineGroupName",
        "name": "name",
        "reservation_model": "reservationModel",
        "description": "description",
        "id": "id",
        "overallocated": "overallocated",
        "supported_feature_set": "supportedFeatureSet",
        "sync_on_refresh": "syncOnRefresh",
    },
)
class NsxtAlbServiceEngineGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        alb_cloud_id: builtins.str,
        importable_service_engine_group_name: builtins.str,
        name: builtins.str,
        reservation_model: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        overallocated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supported_feature_set: typing.Optional[builtins.str] = None,
        sync_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param alb_cloud_id: NSX-T ALB backing Cloud ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#alb_cloud_id NsxtAlbServiceEngineGroup#alb_cloud_id}
        :param importable_service_engine_group_name: NSX-T ALB Importable Service Engine Group Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#importable_service_engine_group_name NsxtAlbServiceEngineGroup#importable_service_engine_group_name}
        :param name: NSX-T ALB Service Engine Group name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#name NsxtAlbServiceEngineGroup#name}
        :param reservation_model: NSX-T ALB Service Engine Group reservation model. One of 'DEDICATED', 'SHARED'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#reservation_model NsxtAlbServiceEngineGroup#reservation_model}
        :param description: NSX-T ALB Service Engine Group description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#description NsxtAlbServiceEngineGroup#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#id NsxtAlbServiceEngineGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param overallocated: Boolean value that shows if virtual services are overallocated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#overallocated NsxtAlbServiceEngineGroup#overallocated}
        :param supported_feature_set: Feature set for this ALB Service Engine Group. One of 'STANDARD', 'PREMIUM'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#supported_feature_set NsxtAlbServiceEngineGroup#supported_feature_set}
        :param sync_on_refresh: Boolean value that shows if sync should be performed on every refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#sync_on_refresh NsxtAlbServiceEngineGroup#sync_on_refresh}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34b339959197e4b5e0987f2a56fe3bca56f8643ed1f85180dfa01b9759fc084)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument alb_cloud_id", value=alb_cloud_id, expected_type=type_hints["alb_cloud_id"])
            check_type(argname="argument importable_service_engine_group_name", value=importable_service_engine_group_name, expected_type=type_hints["importable_service_engine_group_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reservation_model", value=reservation_model, expected_type=type_hints["reservation_model"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument overallocated", value=overallocated, expected_type=type_hints["overallocated"])
            check_type(argname="argument supported_feature_set", value=supported_feature_set, expected_type=type_hints["supported_feature_set"])
            check_type(argname="argument sync_on_refresh", value=sync_on_refresh, expected_type=type_hints["sync_on_refresh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alb_cloud_id": alb_cloud_id,
            "importable_service_engine_group_name": importable_service_engine_group_name,
            "name": name,
            "reservation_model": reservation_model,
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
        if overallocated is not None:
            self._values["overallocated"] = overallocated
        if supported_feature_set is not None:
            self._values["supported_feature_set"] = supported_feature_set
        if sync_on_refresh is not None:
            self._values["sync_on_refresh"] = sync_on_refresh

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
    def alb_cloud_id(self) -> builtins.str:
        '''NSX-T ALB backing Cloud ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#alb_cloud_id NsxtAlbServiceEngineGroup#alb_cloud_id}
        '''
        result = self._values.get("alb_cloud_id")
        assert result is not None, "Required property 'alb_cloud_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def importable_service_engine_group_name(self) -> builtins.str:
        '''NSX-T ALB Importable Service Engine Group Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#importable_service_engine_group_name NsxtAlbServiceEngineGroup#importable_service_engine_group_name}
        '''
        result = self._values.get("importable_service_engine_group_name")
        assert result is not None, "Required property 'importable_service_engine_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''NSX-T ALB Service Engine Group name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#name NsxtAlbServiceEngineGroup#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reservation_model(self) -> builtins.str:
        '''NSX-T ALB Service Engine Group reservation model. One of 'DEDICATED', 'SHARED'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#reservation_model NsxtAlbServiceEngineGroup#reservation_model}
        '''
        result = self._values.get("reservation_model")
        assert result is not None, "Required property 'reservation_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''NSX-T ALB Service Engine Group description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#description NsxtAlbServiceEngineGroup#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#id NsxtAlbServiceEngineGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overallocated(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean value that shows if virtual services are overallocated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#overallocated NsxtAlbServiceEngineGroup#overallocated}
        '''
        result = self._values.get("overallocated")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def supported_feature_set(self) -> typing.Optional[builtins.str]:
        '''Feature set for this ALB Service Engine Group. One of 'STANDARD', 'PREMIUM'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#supported_feature_set NsxtAlbServiceEngineGroup#supported_feature_set}
        '''
        result = self._values.get("supported_feature_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_on_refresh(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean value that shows if sync should be performed on every refresh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_service_engine_group#sync_on_refresh NsxtAlbServiceEngineGroup#sync_on_refresh}
        '''
        result = self._values.get("sync_on_refresh")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbServiceEngineGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NsxtAlbServiceEngineGroup",
    "NsxtAlbServiceEngineGroupConfig",
]

publication.publish()

def _typecheckingstub__78155293664f0efa62c2f9d36ea465d562e7f06a3cb9e09a113728e57fcc8452(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    alb_cloud_id: builtins.str,
    importable_service_engine_group_name: builtins.str,
    name: builtins.str,
    reservation_model: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    overallocated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supported_feature_set: typing.Optional[builtins.str] = None,
    sync_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__03e87370640c0527e201ce252869a9f177d3f9a3a891b4895f92c38c8be9aa1f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9fb85845018e86c2d99d8a77f7dc19eddc8c2cd1ea3ed06e1c1fad007a12f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221841989608cdf07c598c30d5dc0d21fef572ae692492753699618665292ca1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccdc2cb794126595c258781a3244df060f8d91dab3318d13eaf1bbe19fbc2aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f29d58f7c3ab021415032d6db0abde31522c4deed9cf450ca9816c420dba7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2326061900014ed97e12c342415319c8923a6ae7aa106db08bdbdeb383eca568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40c37d0e021d93628f04d0298ebc1871025199d7b90c66f6774cd9b5c8575cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853e3b84aa7d4adf2eaafe2cd9c12106056a5c2ca455bdf25c0fb6721448e3ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5073fa15c93fc20e6501df38b174664043f4c09e5ac0e761b5c0755e4435f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eed1c7621366b6ef69af0d3d33d99c1810c7faf2cc15015c97307b9122f496d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34b339959197e4b5e0987f2a56fe3bca56f8643ed1f85180dfa01b9759fc084(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alb_cloud_id: builtins.str,
    importable_service_engine_group_name: builtins.str,
    name: builtins.str,
    reservation_model: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    overallocated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supported_feature_set: typing.Optional[builtins.str] = None,
    sync_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
