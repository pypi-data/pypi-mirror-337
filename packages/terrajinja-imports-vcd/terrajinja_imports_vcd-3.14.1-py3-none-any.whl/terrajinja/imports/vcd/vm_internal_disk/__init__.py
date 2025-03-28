'''
# `vcd_vm_internal_disk`

Refer to the Terraform Registry for docs: [`vcd_vm_internal_disk`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk).
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


class VmInternalDiskA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmInternalDisk.VmInternalDiskA",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk vcd_vm_internal_disk}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bus_number: jsii.Number,
        bus_type: builtins.str,
        size_in_mb: jsii.Number,
        unit_number: jsii.Number,
        vapp_name: builtins.str,
        vm_name: builtins.str,
        allow_vm_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        storage_profile: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk vcd_vm_internal_disk} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bus_number: The number of the SCSI or IDE controller itself. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#bus_number VmInternalDiskA#bus_number}
        :param bus_type: The type of disk controller. Possible values: ide, parallel( LSI Logic Parallel SCSI), sas(LSI Logic SAS (SCSI)), paravirtual(Paravirtual (SCSI)), sata, nvme Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#bus_type VmInternalDiskA#bus_type}
        :param size_in_mb: The size of the disk in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#size_in_mb VmInternalDiskA#size_in_mb}
        :param unit_number: The device number on the SCSI or IDE controller of the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#unit_number VmInternalDiskA#unit_number}
        :param vapp_name: The vApp this VM internal disk belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vapp_name VmInternalDiskA#vapp_name}
        :param vm_name: VM in vApp in which internal disk is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vm_name VmInternalDiskA#vm_name}
        :param allow_vm_reboot: Powers off VM when changing any attribute of an IDE disk or unit/bus number of other disk types, after the change is complete VM is powered back on. Without this setting enabled, such changes on a powered-on VM would fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#allow_vm_reboot VmInternalDiskA#allow_vm_reboot}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#id VmInternalDiskA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iops: Specifies the IOPS for the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#iops VmInternalDiskA#iops}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#org VmInternalDiskA#org}
        :param storage_profile: Storage profile to override the VM default one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#storage_profile VmInternalDiskA#storage_profile}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vdc VmInternalDiskA#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac86803d0b0485cf0b91593b957d662c6e957d4b752010fb9a72cc8911848619)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VmInternalDiskAConfig(
            bus_number=bus_number,
            bus_type=bus_type,
            size_in_mb=size_in_mb,
            unit_number=unit_number,
            vapp_name=vapp_name,
            vm_name=vm_name,
            allow_vm_reboot=allow_vm_reboot,
            id=id,
            iops=iops,
            org=org,
            storage_profile=storage_profile,
            vdc=vdc,
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
        '''Generates CDKTF code for importing a VmInternalDiskA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VmInternalDiskA to import.
        :param import_from_id: The id of the existing VmInternalDiskA that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VmInternalDiskA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff52aef7861dbb420d49fa4b969b14dc4b62ca6373e1efbb0d4912577e2912fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllowVmReboot")
    def reset_allow_vm_reboot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowVmReboot", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIops")
    def reset_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIops", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetStorageProfile")
    def reset_storage_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageProfile", []))

    @jsii.member(jsii_name="resetVdc")
    def reset_vdc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdc", []))

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
    @jsii.member(jsii_name="thinProvisioned")
    def thin_provisioned(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "thinProvisioned"))

    @builtins.property
    @jsii.member(jsii_name="allowVmRebootInput")
    def allow_vm_reboot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowVmRebootInput"))

    @builtins.property
    @jsii.member(jsii_name="busNumberInput")
    def bus_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "busNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="busTypeInput")
    def bus_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "busTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iopsInput")
    def iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iopsInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInMbInput")
    def size_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileInput")
    def storage_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="unitNumberInput")
    def unit_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unitNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="vappNameInput")
    def vapp_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vappNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="vmNameInput")
    def vm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="allowVmReboot")
    def allow_vm_reboot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowVmReboot"))

    @allow_vm_reboot.setter
    def allow_vm_reboot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd5e90f32b0fe3565ffeb640a8398d62262e1968993d6bed2dacf45db966170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowVmReboot", value)

    @builtins.property
    @jsii.member(jsii_name="busNumber")
    def bus_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "busNumber"))

    @bus_number.setter
    def bus_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f56b3cf81359da953fd8ca8f655f87088ad891e703a7cb7bb03bbf6e74aadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busNumber", value)

    @builtins.property
    @jsii.member(jsii_name="busType")
    def bus_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "busType"))

    @bus_type.setter
    def bus_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fc8c04f922a20adc3648285b3b0be21e02cf6465515ceeb35a4429acf6989a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busType", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38339a49e11dfe889dc298d2377b0fc9146c7998ddd2580753ce831e0ff72ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @iops.setter
    def iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f581070910356f1eb79e25159aa1198f522eb78ae5a20001e0a5f5057c92db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41899a351c3b0490d3e24ef3f385345e3da815856e9a683bcc838055b5664870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="sizeInMb")
    def size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInMb"))

    @size_in_mb.setter
    def size_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4627db0050fc051482c2458ba65b4fd383ae57444b7881655faf172a862879e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInMb", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfile"))

    @storage_profile.setter
    def storage_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4931f624bdc794bdd1ac7bd070ddfe5ff62d4303c0c6b961259b57ec5b974989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfile", value)

    @builtins.property
    @jsii.member(jsii_name="unitNumber")
    def unit_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unitNumber"))

    @unit_number.setter
    def unit_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f704aeb23f4386573c6b04a7223837070d11aacb7b8a182c40d00c3e8ad1e270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unitNumber", value)

    @builtins.property
    @jsii.member(jsii_name="vappName")
    def vapp_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappName"))

    @vapp_name.setter
    def vapp_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cca51070480cd36a1537ba2dcaa8398b57dec639475f7002b030eab7f0ef98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappName", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb46f3604adae9e066838a0415876b16c8387c2c12e90419e30b2aed09d70179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)

    @builtins.property
    @jsii.member(jsii_name="vmName")
    def vm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmName"))

    @vm_name.setter
    def vm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faccea6f054b3da25186952c119bfdf6b53e5e2cac248633e77ca77a0dc1d523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmName", value)


@jsii.data_type(
    jsii_type="vcd.vmInternalDisk.VmInternalDiskAConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bus_number": "busNumber",
        "bus_type": "busType",
        "size_in_mb": "sizeInMb",
        "unit_number": "unitNumber",
        "vapp_name": "vappName",
        "vm_name": "vmName",
        "allow_vm_reboot": "allowVmReboot",
        "id": "id",
        "iops": "iops",
        "org": "org",
        "storage_profile": "storageProfile",
        "vdc": "vdc",
    },
)
class VmInternalDiskAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bus_number: jsii.Number,
        bus_type: builtins.str,
        size_in_mb: jsii.Number,
        unit_number: jsii.Number,
        vapp_name: builtins.str,
        vm_name: builtins.str,
        allow_vm_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        storage_profile: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bus_number: The number of the SCSI or IDE controller itself. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#bus_number VmInternalDiskA#bus_number}
        :param bus_type: The type of disk controller. Possible values: ide, parallel( LSI Logic Parallel SCSI), sas(LSI Logic SAS (SCSI)), paravirtual(Paravirtual (SCSI)), sata, nvme Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#bus_type VmInternalDiskA#bus_type}
        :param size_in_mb: The size of the disk in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#size_in_mb VmInternalDiskA#size_in_mb}
        :param unit_number: The device number on the SCSI or IDE controller of the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#unit_number VmInternalDiskA#unit_number}
        :param vapp_name: The vApp this VM internal disk belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vapp_name VmInternalDiskA#vapp_name}
        :param vm_name: VM in vApp in which internal disk is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vm_name VmInternalDiskA#vm_name}
        :param allow_vm_reboot: Powers off VM when changing any attribute of an IDE disk or unit/bus number of other disk types, after the change is complete VM is powered back on. Without this setting enabled, such changes on a powered-on VM would fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#allow_vm_reboot VmInternalDiskA#allow_vm_reboot}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#id VmInternalDiskA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iops: Specifies the IOPS for the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#iops VmInternalDiskA#iops}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#org VmInternalDiskA#org}
        :param storage_profile: Storage profile to override the VM default one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#storage_profile VmInternalDiskA#storage_profile}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vdc VmInternalDiskA#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cbb7452e5a6c9e26eb421ffc0d4c08dbe40c3b0eceda8910485343f5acf48f4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bus_number", value=bus_number, expected_type=type_hints["bus_number"])
            check_type(argname="argument bus_type", value=bus_type, expected_type=type_hints["bus_type"])
            check_type(argname="argument size_in_mb", value=size_in_mb, expected_type=type_hints["size_in_mb"])
            check_type(argname="argument unit_number", value=unit_number, expected_type=type_hints["unit_number"])
            check_type(argname="argument vapp_name", value=vapp_name, expected_type=type_hints["vapp_name"])
            check_type(argname="argument vm_name", value=vm_name, expected_type=type_hints["vm_name"])
            check_type(argname="argument allow_vm_reboot", value=allow_vm_reboot, expected_type=type_hints["allow_vm_reboot"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument storage_profile", value=storage_profile, expected_type=type_hints["storage_profile"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bus_number": bus_number,
            "bus_type": bus_type,
            "size_in_mb": size_in_mb,
            "unit_number": unit_number,
            "vapp_name": vapp_name,
            "vm_name": vm_name,
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
        if allow_vm_reboot is not None:
            self._values["allow_vm_reboot"] = allow_vm_reboot
        if id is not None:
            self._values["id"] = id
        if iops is not None:
            self._values["iops"] = iops
        if org is not None:
            self._values["org"] = org
        if storage_profile is not None:
            self._values["storage_profile"] = storage_profile
        if vdc is not None:
            self._values["vdc"] = vdc

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
    def bus_number(self) -> jsii.Number:
        '''The number of the SCSI or IDE controller itself.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#bus_number VmInternalDiskA#bus_number}
        '''
        result = self._values.get("bus_number")
        assert result is not None, "Required property 'bus_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def bus_type(self) -> builtins.str:
        '''The type of disk controller.

        Possible values: ide, parallel( LSI Logic Parallel SCSI), sas(LSI Logic SAS (SCSI)), paravirtual(Paravirtual (SCSI)), sata, nvme

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#bus_type VmInternalDiskA#bus_type}
        '''
        result = self._values.get("bus_type")
        assert result is not None, "Required property 'bus_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size_in_mb(self) -> jsii.Number:
        '''The size of the disk in MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#size_in_mb VmInternalDiskA#size_in_mb}
        '''
        result = self._values.get("size_in_mb")
        assert result is not None, "Required property 'size_in_mb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def unit_number(self) -> jsii.Number:
        '''The device number on the SCSI or IDE controller of the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#unit_number VmInternalDiskA#unit_number}
        '''
        result = self._values.get("unit_number")
        assert result is not None, "Required property 'unit_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vapp_name(self) -> builtins.str:
        '''The vApp this VM internal disk belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vapp_name VmInternalDiskA#vapp_name}
        '''
        result = self._values.get("vapp_name")
        assert result is not None, "Required property 'vapp_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_name(self) -> builtins.str:
        '''VM in vApp in which internal disk is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vm_name VmInternalDiskA#vm_name}
        '''
        result = self._values.get("vm_name")
        assert result is not None, "Required property 'vm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_vm_reboot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Powers off VM when changing any attribute of an IDE disk or unit/bus number of other disk types, after the change is complete VM is powered back on.

        Without this setting enabled, such changes on a powered-on VM would fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#allow_vm_reboot VmInternalDiskA#allow_vm_reboot}
        '''
        result = self._values.get("allow_vm_reboot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#id VmInternalDiskA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''Specifies the IOPS for the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#iops VmInternalDiskA#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#org VmInternalDiskA#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_profile(self) -> typing.Optional[builtins.str]:
        '''Storage profile to override the VM default one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#storage_profile VmInternalDiskA#storage_profile}
        '''
        result = self._values.get("storage_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_internal_disk#vdc VmInternalDiskA#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmInternalDiskAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "VmInternalDiskA",
    "VmInternalDiskAConfig",
]

publication.publish()

def _typecheckingstub__ac86803d0b0485cf0b91593b957d662c6e957d4b752010fb9a72cc8911848619(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bus_number: jsii.Number,
    bus_type: builtins.str,
    size_in_mb: jsii.Number,
    unit_number: jsii.Number,
    vapp_name: builtins.str,
    vm_name: builtins.str,
    allow_vm_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    iops: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    storage_profile: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ff52aef7861dbb420d49fa4b969b14dc4b62ca6373e1efbb0d4912577e2912fc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd5e90f32b0fe3565ffeb640a8398d62262e1968993d6bed2dacf45db966170(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f56b3cf81359da953fd8ca8f655f87088ad891e703a7cb7bb03bbf6e74aadb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fc8c04f922a20adc3648285b3b0be21e02cf6465515ceeb35a4429acf6989a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38339a49e11dfe889dc298d2377b0fc9146c7998ddd2580753ce831e0ff72ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f581070910356f1eb79e25159aa1198f522eb78ae5a20001e0a5f5057c92db7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41899a351c3b0490d3e24ef3f385345e3da815856e9a683bcc838055b5664870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4627db0050fc051482c2458ba65b4fd383ae57444b7881655faf172a862879e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4931f624bdc794bdd1ac7bd070ddfe5ff62d4303c0c6b961259b57ec5b974989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f704aeb23f4386573c6b04a7223837070d11aacb7b8a182c40d00c3e8ad1e270(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cca51070480cd36a1537ba2dcaa8398b57dec639475f7002b030eab7f0ef98b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb46f3604adae9e066838a0415876b16c8387c2c12e90419e30b2aed09d70179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faccea6f054b3da25186952c119bfdf6b53e5e2cac248633e77ca77a0dc1d523(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cbb7452e5a6c9e26eb421ffc0d4c08dbe40c3b0eceda8910485343f5acf48f4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bus_number: jsii.Number,
    bus_type: builtins.str,
    size_in_mb: jsii.Number,
    unit_number: jsii.Number,
    vapp_name: builtins.str,
    vm_name: builtins.str,
    allow_vm_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    iops: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    storage_profile: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
