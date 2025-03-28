'''
# `vcd_provider_vdc`

Refer to the Terraform Registry for docs: [`vcd_provider_vdc`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc).
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


class ProviderVdc(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdc",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc vcd_provider_vdc}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        highest_supported_hardware_version: builtins.str,
        name: builtins.str,
        resource_pool_ids: typing.Sequence[builtins.str],
        storage_profile_names: typing.Sequence[builtins.str],
        vcenter_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProviderVdcMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        nsxt_manager_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc vcd_provider_vdc} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param highest_supported_hardware_version: The highest virtual hardware version supported by this Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#highest_supported_hardware_version ProviderVdc#highest_supported_hardware_version}
        :param name: Name of the Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#name ProviderVdc#name}
        :param resource_pool_ids: Set of IDs of the resource pools backing this provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#resource_pool_ids ProviderVdc#resource_pool_ids}
        :param storage_profile_names: Set of storage profile names used to create this Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#storage_profile_names ProviderVdc#storage_profile_names}
        :param vcenter_id: ID of the vCenter server that provides the resource pools and datastores. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#vcenter_id ProviderVdc#vcenter_id}
        :param description: Optional description of the Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#description ProviderVdc#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#id ProviderVdc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: True if this Provider VDC is enabled and can provide resources to organization VDCs. A Provider VDC is always enabled on creation Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#is_enabled ProviderVdc#is_enabled}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#metadata_entry ProviderVdc#metadata_entry}
        :param network_pool_ids: Set IDs of the network pools used by this Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#network_pool_ids ProviderVdc#network_pool_ids}
        :param nsxt_manager_id: ID of the registered NSX-T Manager that backs networking operations for this Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#nsxt_manager_id ProviderVdc#nsxt_manager_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f067fdf36905bfc1a143cd141678c276298e9e745d470204010800ffd2a1ddde)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProviderVdcConfig(
            highest_supported_hardware_version=highest_supported_hardware_version,
            name=name,
            resource_pool_ids=resource_pool_ids,
            storage_profile_names=storage_profile_names,
            vcenter_id=vcenter_id,
            description=description,
            id=id,
            is_enabled=is_enabled,
            metadata_entry=metadata_entry,
            network_pool_ids=network_pool_ids,
            nsxt_manager_id=nsxt_manager_id,
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
        '''Generates CDKTF code for importing a ProviderVdc resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProviderVdc to import.
        :param import_from_id: The id of the existing ProviderVdc that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProviderVdc to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d157f0d8513fa8129ff70da3651e05f9d695c6c2a4582e45e9dd7d78e657ad9f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProviderVdcMetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f90404612b7907a2aeeb2fddc2f95afbeba45d092f027bec07cd6df58ea4bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetMetadataEntry")
    def reset_metadata_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataEntry", []))

    @jsii.member(jsii_name="resetNetworkPoolIds")
    def reset_network_pool_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPoolIds", []))

    @jsii.member(jsii_name="resetNsxtManagerId")
    def reset_nsxt_manager_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNsxtManagerId", []))

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
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "capabilities"))

    @builtins.property
    @jsii.member(jsii_name="computeCapacity")
    def compute_capacity(self) -> "ProviderVdcComputeCapacityList":
        return typing.cast("ProviderVdcComputeCapacityList", jsii.get(self, "computeCapacity"))

    @builtins.property
    @jsii.member(jsii_name="computeProviderScope")
    def compute_provider_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeProviderScope"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkIds")
    def external_network_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalNetworkIds"))

    @builtins.property
    @jsii.member(jsii_name="hostIds")
    def host_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostIds"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "ProviderVdcMetadataEntryList":
        return typing.cast("ProviderVdcMetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storageContainerIds")
    def storage_container_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storageContainerIds"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileIds")
    def storage_profile_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storageProfileIds"))

    @builtins.property
    @jsii.member(jsii_name="universalNetworkPoolId")
    def universal_network_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "universalNetworkPoolId"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="highestSupportedHardwareVersionInput")
    def highest_supported_hardware_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "highestSupportedHardwareVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntryInput")
    def metadata_entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProviderVdcMetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProviderVdcMetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPoolIdsInput")
    def network_pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkPoolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerIdInput")
    def nsxt_manager_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nsxtManagerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoolIdsInput")
    def resource_pool_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcePoolIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileNamesInput")
    def storage_profile_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "storageProfileNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="vcenterIdInput")
    def vcenter_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vcenterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d92e8828153113884a5950374879248f532bcca16f60716af7de2449dca504e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="highestSupportedHardwareVersion")
    def highest_supported_hardware_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "highestSupportedHardwareVersion"))

    @highest_supported_hardware_version.setter
    def highest_supported_hardware_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1626ff7f7f62bb640cc3c2c4634886e1c136f2da5ea836141a1da06efde709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highestSupportedHardwareVersion", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb8911cfe90f511f930a9b86978aabe876da86f481b9b458bbd7b71b3826d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9ea40ff8b8992b59d440a3af1930b11bdfe7d192817b435c64a85f937757f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6803dabae3fb03b45d82278a9b78e403fdfa8bfbf3f6705b090942b5daa3b50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkPoolIds")
    def network_pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkPoolIds"))

    @network_pool_ids.setter
    def network_pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d3639059087af5e98778ebbeaaf63c3bab5b59d4df415c25d85ffaac7599e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPoolIds", value)

    @builtins.property
    @jsii.member(jsii_name="nsxtManagerId")
    def nsxt_manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nsxtManagerId"))

    @nsxt_manager_id.setter
    def nsxt_manager_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f7d66d12dd2abdff6fb32a42bc7188522a2e348fd4949e4bb098e26044be74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nsxtManagerId", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePoolIds")
    def resource_pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePoolIds"))

    @resource_pool_ids.setter
    def resource_pool_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c7f91f50e4a6afc1cd6ec90019269b1b4fdd4a89a07e08ecfeff876ec4d49c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePoolIds", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfileNames")
    def storage_profile_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storageProfileNames"))

    @storage_profile_names.setter
    def storage_profile_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f9ef7b4db4cc3309659bc23b4e6bf224022ed50ab7b62d420658f119e475fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfileNames", value)

    @builtins.property
    @jsii.member(jsii_name="vcenterId")
    def vcenter_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcenterId"))

    @vcenter_id.setter
    def vcenter_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c226ee63276007872eb8cd2ca9e636ac398c6253b1225d674aa8a49964f6e2aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcenterId", value)


@jsii.data_type(
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacity",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProviderVdcComputeCapacity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderVdcComputeCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacityCpu",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProviderVdcComputeCapacityCpu:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderVdcComputeCapacityCpu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProviderVdcComputeCapacityCpuList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacityCpuList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16d0952b790d4d794929c9815edeb83e219d6a74d015791c86c919f60fb69182)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProviderVdcComputeCapacityCpuOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc64445436123dc00d73ddbb9afeb76b2b72bb029d38ff5991de124cdc808bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProviderVdcComputeCapacityCpuOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21678a12f2ba56f3e2a8af636af4ca51dbe01df90e420ef2cd01c3364483565e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3797757c1ebfef2847e51106c4cdda09f46cd711fd532a58a1b5cf3d13c327d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__719aa7517ce742f5726be1037e9f875fa6a125532fb7c08f89412da9a322a52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ProviderVdcComputeCapacityCpuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacityCpuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b7857b4170c0b5ceca3aa1f4fe767bea8e7730446363e5e38228078bd81f16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allocation")
    def allocation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocation"))

    @builtins.property
    @jsii.member(jsii_name="overhead")
    def overhead(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "overhead"))

    @builtins.property
    @jsii.member(jsii_name="reserved")
    def reserved(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reserved"))

    @builtins.property
    @jsii.member(jsii_name="total")
    def total(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "total"))

    @builtins.property
    @jsii.member(jsii_name="units")
    def units(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "units"))

    @builtins.property
    @jsii.member(jsii_name="used")
    def used(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "used"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProviderVdcComputeCapacityCpu]:
        return typing.cast(typing.Optional[ProviderVdcComputeCapacityCpu], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProviderVdcComputeCapacityCpu],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eca17f75a6f6deb56e67d5e7c4825b8e2bbd95115f5979f33ca9887572b3bce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ProviderVdcComputeCapacityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12197cd0be7423bdb4e9ae6a3d4f4e3a5ecd491f37b1ddfa12dcc781c3c426f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProviderVdcComputeCapacityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68b655bbe520c714a3439cb477c9f1149e475bdb03e680642478d356e226dc2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProviderVdcComputeCapacityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42224ccebc69c0e7f296cd1077c1c4df871de84edd32040a937c8a8533064379)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00441a849da1a40316868f6c25b3be065fbf067049d317742c121559c631f936)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c2e73a9c794a8b6a340e2b43554b789c949c2cb9d9330103d17cc1b76327c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.data_type(
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacityMemory",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProviderVdcComputeCapacityMemory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderVdcComputeCapacityMemory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProviderVdcComputeCapacityMemoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacityMemoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db21e339e0a9e99d77267ca682950e7fd5ba8fadac28da2af88c43968eb7c033)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProviderVdcComputeCapacityMemoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e1cbed952175af324504c5395a71528438e1fbc7da8c2460c7388156149e7b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProviderVdcComputeCapacityMemoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6efd9a628aa2add67ffeda9d7cb3498c1b0507787e22179aac1628a5056501e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e567165f13f9316207142d2119d50ad532531b6ed97d7e2e795acf172f3819ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__513ba36bc424f71dcb5b33704037bc6876dffd49c38dc8726cc706be064f838c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ProviderVdcComputeCapacityMemoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacityMemoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__add9a66b0e35c673d983826985aab5ff55485f75b3de08b368ecd75a8578128f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allocation")
    def allocation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocation"))

    @builtins.property
    @jsii.member(jsii_name="overhead")
    def overhead(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "overhead"))

    @builtins.property
    @jsii.member(jsii_name="reserved")
    def reserved(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reserved"))

    @builtins.property
    @jsii.member(jsii_name="total")
    def total(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "total"))

    @builtins.property
    @jsii.member(jsii_name="units")
    def units(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "units"))

    @builtins.property
    @jsii.member(jsii_name="used")
    def used(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "used"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProviderVdcComputeCapacityMemory]:
        return typing.cast(typing.Optional[ProviderVdcComputeCapacityMemory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProviderVdcComputeCapacityMemory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306c37a832c746578c2aace0be5a6a8b812fe93c747b21e981fc7ce35267ad30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ProviderVdcComputeCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdcComputeCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7933bccdd351f36c0f0585714e08fb64e7d7ad349314f7f02eb661057956f93f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> ProviderVdcComputeCapacityCpuList:
        return typing.cast(ProviderVdcComputeCapacityCpuList, jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="isElastic")
    def is_elastic(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isElastic"))

    @builtins.property
    @jsii.member(jsii_name="isHa")
    def is_ha(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isHa"))

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> ProviderVdcComputeCapacityMemoryList:
        return typing.cast(ProviderVdcComputeCapacityMemoryList, jsii.get(self, "memory"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProviderVdcComputeCapacity]:
        return typing.cast(typing.Optional[ProviderVdcComputeCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProviderVdcComputeCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89fc48123e6643e4c695ab4b5dd1dcf6a604dde3b978e261655d60a072b990f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.providerVdc.ProviderVdcConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "highest_supported_hardware_version": "highestSupportedHardwareVersion",
        "name": "name",
        "resource_pool_ids": "resourcePoolIds",
        "storage_profile_names": "storageProfileNames",
        "vcenter_id": "vcenterId",
        "description": "description",
        "id": "id",
        "is_enabled": "isEnabled",
        "metadata_entry": "metadataEntry",
        "network_pool_ids": "networkPoolIds",
        "nsxt_manager_id": "nsxtManagerId",
    },
)
class ProviderVdcConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        highest_supported_hardware_version: builtins.str,
        name: builtins.str,
        resource_pool_ids: typing.Sequence[builtins.str],
        storage_profile_names: typing.Sequence[builtins.str],
        vcenter_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProviderVdcMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        nsxt_manager_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param highest_supported_hardware_version: The highest virtual hardware version supported by this Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#highest_supported_hardware_version ProviderVdc#highest_supported_hardware_version}
        :param name: Name of the Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#name ProviderVdc#name}
        :param resource_pool_ids: Set of IDs of the resource pools backing this provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#resource_pool_ids ProviderVdc#resource_pool_ids}
        :param storage_profile_names: Set of storage profile names used to create this Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#storage_profile_names ProviderVdc#storage_profile_names}
        :param vcenter_id: ID of the vCenter server that provides the resource pools and datastores. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#vcenter_id ProviderVdc#vcenter_id}
        :param description: Optional description of the Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#description ProviderVdc#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#id ProviderVdc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: True if this Provider VDC is enabled and can provide resources to organization VDCs. A Provider VDC is always enabled on creation Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#is_enabled ProviderVdc#is_enabled}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#metadata_entry ProviderVdc#metadata_entry}
        :param network_pool_ids: Set IDs of the network pools used by this Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#network_pool_ids ProviderVdc#network_pool_ids}
        :param nsxt_manager_id: ID of the registered NSX-T Manager that backs networking operations for this Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#nsxt_manager_id ProviderVdc#nsxt_manager_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc49ff373dfc5518bce56b7973b4eda4d1cd8bbb6e02c19fbc4b8aa4cd73564)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument highest_supported_hardware_version", value=highest_supported_hardware_version, expected_type=type_hints["highest_supported_hardware_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_pool_ids", value=resource_pool_ids, expected_type=type_hints["resource_pool_ids"])
            check_type(argname="argument storage_profile_names", value=storage_profile_names, expected_type=type_hints["storage_profile_names"])
            check_type(argname="argument vcenter_id", value=vcenter_id, expected_type=type_hints["vcenter_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument metadata_entry", value=metadata_entry, expected_type=type_hints["metadata_entry"])
            check_type(argname="argument network_pool_ids", value=network_pool_ids, expected_type=type_hints["network_pool_ids"])
            check_type(argname="argument nsxt_manager_id", value=nsxt_manager_id, expected_type=type_hints["nsxt_manager_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "highest_supported_hardware_version": highest_supported_hardware_version,
            "name": name,
            "resource_pool_ids": resource_pool_ids,
            "storage_profile_names": storage_profile_names,
            "vcenter_id": vcenter_id,
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
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if metadata_entry is not None:
            self._values["metadata_entry"] = metadata_entry
        if network_pool_ids is not None:
            self._values["network_pool_ids"] = network_pool_ids
        if nsxt_manager_id is not None:
            self._values["nsxt_manager_id"] = nsxt_manager_id

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
    def highest_supported_hardware_version(self) -> builtins.str:
        '''The highest virtual hardware version supported by this Provider VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#highest_supported_hardware_version ProviderVdc#highest_supported_hardware_version}
        '''
        result = self._values.get("highest_supported_hardware_version")
        assert result is not None, "Required property 'highest_supported_hardware_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Provider VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#name ProviderVdc#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_pool_ids(self) -> typing.List[builtins.str]:
        '''Set of IDs of the resource pools backing this provider VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#resource_pool_ids ProviderVdc#resource_pool_ids}
        '''
        result = self._values.get("resource_pool_ids")
        assert result is not None, "Required property 'resource_pool_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def storage_profile_names(self) -> typing.List[builtins.str]:
        '''Set of storage profile names used to create this Provider VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#storage_profile_names ProviderVdc#storage_profile_names}
        '''
        result = self._values.get("storage_profile_names")
        assert result is not None, "Required property 'storage_profile_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vcenter_id(self) -> builtins.str:
        '''ID of the vCenter server that provides the resource pools and datastores.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#vcenter_id ProviderVdc#vcenter_id}
        '''
        result = self._values.get("vcenter_id")
        assert result is not None, "Required property 'vcenter_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional description of the Provider VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#description ProviderVdc#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#id ProviderVdc#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if this Provider VDC is enabled and can provide resources to organization VDCs.

        A Provider VDC is always enabled on creation

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#is_enabled ProviderVdc#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProviderVdcMetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#metadata_entry ProviderVdc#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProviderVdcMetadataEntry"]]], result)

    @builtins.property
    def network_pool_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set IDs of the network pools used by this Provider VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#network_pool_ids ProviderVdc#network_pool_ids}
        '''
        result = self._values.get("network_pool_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def nsxt_manager_id(self) -> typing.Optional[builtins.str]:
        '''ID of the registered NSX-T Manager that backs networking operations for this Provider VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#nsxt_manager_id ProviderVdc#nsxt_manager_id}
        '''
        result = self._values.get("nsxt_manager_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderVdcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.providerVdc.ProviderVdcMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "value": "value",
        "is_system": "isSystem",
        "type": "type",
        "user_access": "userAccess",
    },
)
class ProviderVdcMetadataEntry:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: builtins.str,
        is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
        user_access: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key of this metadata entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#key ProviderVdc#key}
        :param value: Value of this metadata entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#value ProviderVdc#value}
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Defaults to false Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#is_system ProviderVdc#is_system}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Defaults to 'MetadataStringValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#type ProviderVdc#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Defaults to 'READWRITE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#user_access ProviderVdc#user_access}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9494690c0baaf69383f213b1ac2e70bb5aa6c71b8b4dbcdcebfc7da0cf94fc)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument is_system", value=is_system, expected_type=type_hints["is_system"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_access", value=user_access, expected_type=type_hints["user_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }
        if is_system is not None:
            self._values["is_system"] = is_system
        if type is not None:
            self._values["type"] = type
        if user_access is not None:
            self._values["user_access"] = user_access

    @builtins.property
    def key(self) -> builtins.str:
        '''Key of this metadata entry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#key ProviderVdc#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of this metadata entry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#value ProviderVdc#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_system(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Domain for this metadata entry.

        true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Defaults to false

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#is_system ProviderVdc#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Defaults to 'MetadataStringValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#type ProviderVdc#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Defaults to 'READWRITE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/provider_vdc#user_access ProviderVdc#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderVdcMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProviderVdcMetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdcMetadataEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9e3e67acdb01f216209b492a09f67b58b4e3414891209309578316191effa43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProviderVdcMetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d7089cfed18059dd2475a9c2b95714cf0b217cd528d3b12a980151abfa985d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProviderVdcMetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5537c38a86da2cf7ce8e44c23377c3d123ae6154f5e8077abfde19a345f1719)
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
            type_hints = typing.get_type_hints(_typecheckingstub__342d3ebf808434ff31047dafbe5017a186541b4af0c8c540bcfa250942ec8c5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c03479ea60c80bb93dd7bcfdd7fe7d9bd6b4fc1f5c96531e496cb792ab7bc95b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProviderVdcMetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProviderVdcMetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProviderVdcMetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0134edc4f191513c8445f68f67e5d956b60df67af19f6e4be032209b5bbd5a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ProviderVdcMetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.providerVdc.ProviderVdcMetadataEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9e9d74070e23ceba689ea2bc2db376dfb7c8f22cfbf36d3996da50b50d7c623)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsSystem")
    def reset_is_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSystem", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserAccess")
    def reset_user_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAccess", []))

    @builtins.property
    @jsii.member(jsii_name="isSystemInput")
    def is_system_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userAccessInput")
    def user_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isSystem")
    def is_system(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSystem"))

    @is_system.setter
    def is_system(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e0d34411a4787fb4e79c81fd02eaae8969f9f2ac6a29171b5886e6955ad572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a1982d87c1d4fc058f6b8fb34e3069c44da7fa7649c015a25d99e5f7a6c981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20555210f6d739177ae408e9cf41495e0ac2e7702ad3f250afeaaab4fb4ca1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21077e0d59034138900fb87a9595d33df9fd469d5efdb932f70952036cb201e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35fbc059b51a8380d37d674c30b6e4b4f5f10eccb1e00ee012d1fa3ddea36849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProviderVdcMetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProviderVdcMetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProviderVdcMetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5a84c16c7b87733fcf7239e845f5d25f2da2960351d825e076cb3c5a29c55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ProviderVdc",
    "ProviderVdcComputeCapacity",
    "ProviderVdcComputeCapacityCpu",
    "ProviderVdcComputeCapacityCpuList",
    "ProviderVdcComputeCapacityCpuOutputReference",
    "ProviderVdcComputeCapacityList",
    "ProviderVdcComputeCapacityMemory",
    "ProviderVdcComputeCapacityMemoryList",
    "ProviderVdcComputeCapacityMemoryOutputReference",
    "ProviderVdcComputeCapacityOutputReference",
    "ProviderVdcConfig",
    "ProviderVdcMetadataEntry",
    "ProviderVdcMetadataEntryList",
    "ProviderVdcMetadataEntryOutputReference",
]

publication.publish()

def _typecheckingstub__f067fdf36905bfc1a143cd141678c276298e9e745d470204010800ffd2a1ddde(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    highest_supported_hardware_version: builtins.str,
    name: builtins.str,
    resource_pool_ids: typing.Sequence[builtins.str],
    storage_profile_names: typing.Sequence[builtins.str],
    vcenter_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProviderVdcMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    nsxt_manager_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d157f0d8513fa8129ff70da3651e05f9d695c6c2a4582e45e9dd7d78e657ad9f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f90404612b7907a2aeeb2fddc2f95afbeba45d092f027bec07cd6df58ea4bfe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProviderVdcMetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d92e8828153113884a5950374879248f532bcca16f60716af7de2449dca504e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1626ff7f7f62bb640cc3c2c4634886e1c136f2da5ea836141a1da06efde709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb8911cfe90f511f930a9b86978aabe876da86f481b9b458bbd7b71b3826d4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9ea40ff8b8992b59d440a3af1930b11bdfe7d192817b435c64a85f937757f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6803dabae3fb03b45d82278a9b78e403fdfa8bfbf3f6705b090942b5daa3b50b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d3639059087af5e98778ebbeaaf63c3bab5b59d4df415c25d85ffaac7599e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f7d66d12dd2abdff6fb32a42bc7188522a2e348fd4949e4bb098e26044be74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c7f91f50e4a6afc1cd6ec90019269b1b4fdd4a89a07e08ecfeff876ec4d49c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f9ef7b4db4cc3309659bc23b4e6bf224022ed50ab7b62d420658f119e475fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c226ee63276007872eb8cd2ca9e636ac398c6253b1225d674aa8a49964f6e2aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d0952b790d4d794929c9815edeb83e219d6a74d015791c86c919f60fb69182(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc64445436123dc00d73ddbb9afeb76b2b72bb029d38ff5991de124cdc808bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21678a12f2ba56f3e2a8af636af4ca51dbe01df90e420ef2cd01c3364483565e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3797757c1ebfef2847e51106c4cdda09f46cd711fd532a58a1b5cf3d13c327d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719aa7517ce742f5726be1037e9f875fa6a125532fb7c08f89412da9a322a52a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b7857b4170c0b5ceca3aa1f4fe767bea8e7730446363e5e38228078bd81f16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eca17f75a6f6deb56e67d5e7c4825b8e2bbd95115f5979f33ca9887572b3bce(
    value: typing.Optional[ProviderVdcComputeCapacityCpu],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12197cd0be7423bdb4e9ae6a3d4f4e3a5ecd491f37b1ddfa12dcc781c3c426f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68b655bbe520c714a3439cb477c9f1149e475bdb03e680642478d356e226dc2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42224ccebc69c0e7f296cd1077c1c4df871de84edd32040a937c8a8533064379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00441a849da1a40316868f6c25b3be065fbf067049d317742c121559c631f936(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2e73a9c794a8b6a340e2b43554b789c949c2cb9d9330103d17cc1b76327c2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db21e339e0a9e99d77267ca682950e7fd5ba8fadac28da2af88c43968eb7c033(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e1cbed952175af324504c5395a71528438e1fbc7da8c2460c7388156149e7b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6efd9a628aa2add67ffeda9d7cb3498c1b0507787e22179aac1628a5056501e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e567165f13f9316207142d2119d50ad532531b6ed97d7e2e795acf172f3819ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513ba36bc424f71dcb5b33704037bc6876dffd49c38dc8726cc706be064f838c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add9a66b0e35c673d983826985aab5ff55485f75b3de08b368ecd75a8578128f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306c37a832c746578c2aace0be5a6a8b812fe93c747b21e981fc7ce35267ad30(
    value: typing.Optional[ProviderVdcComputeCapacityMemory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7933bccdd351f36c0f0585714e08fb64e7d7ad349314f7f02eb661057956f93f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fc48123e6643e4c695ab4b5dd1dcf6a604dde3b978e261655d60a072b990f5(
    value: typing.Optional[ProviderVdcComputeCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc49ff373dfc5518bce56b7973b4eda4d1cd8bbb6e02c19fbc4b8aa4cd73564(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    highest_supported_hardware_version: builtins.str,
    name: builtins.str,
    resource_pool_ids: typing.Sequence[builtins.str],
    storage_profile_names: typing.Sequence[builtins.str],
    vcenter_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProviderVdcMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_pool_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    nsxt_manager_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9494690c0baaf69383f213b1ac2e70bb5aa6c71b8b4dbcdcebfc7da0cf94fc(
    *,
    key: builtins.str,
    value: builtins.str,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e3e67acdb01f216209b492a09f67b58b4e3414891209309578316191effa43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d7089cfed18059dd2475a9c2b95714cf0b217cd528d3b12a980151abfa985d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5537c38a86da2cf7ce8e44c23377c3d123ae6154f5e8077abfde19a345f1719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342d3ebf808434ff31047dafbe5017a186541b4af0c8c540bcfa250942ec8c5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03479ea60c80bb93dd7bcfdd7fe7d9bd6b4fc1f5c96531e496cb792ab7bc95b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0134edc4f191513c8445f68f67e5d956b60df67af19f6e4be032209b5bbd5a50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProviderVdcMetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e9d74070e23ceba689ea2bc2db376dfb7c8f22cfbf36d3996da50b50d7c623(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e0d34411a4787fb4e79c81fd02eaae8969f9f2ac6a29171b5886e6955ad572(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a1982d87c1d4fc058f6b8fb34e3069c44da7fa7649c015a25d99e5f7a6c981(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20555210f6d739177ae408e9cf41495e0ac2e7702ad3f250afeaaab4fb4ca1d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21077e0d59034138900fb87a9595d33df9fd469d5efdb932f70952036cb201e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fbc059b51a8380d37d674c30b6e4b4f5f10eccb1e00ee012d1fa3ddea36849(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5a84c16c7b87733fcf7239e845f5d25f2da2960351d825e076cb3c5a29c55a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProviderVdcMetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass
