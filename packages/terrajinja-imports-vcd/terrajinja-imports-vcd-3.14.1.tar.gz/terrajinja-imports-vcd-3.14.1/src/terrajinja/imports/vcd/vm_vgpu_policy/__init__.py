'''
# `vcd_vm_vgpu_policy`

Refer to the Terraform Registry for docs: [`vcd_vm_vgpu_policy`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy).
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


class VmVgpuPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy vcd_vm_vgpu_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        vgpu_profile: typing.Union["VmVgpuPolicyVgpuProfile", typing.Dict[builtins.str, typing.Any]],
        cpu: typing.Optional[typing.Union["VmVgpuPolicyCpu", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        memory: typing.Optional[typing.Union["VmVgpuPolicyMemory", typing.Dict[builtins.str, typing.Any]]] = None,
        provider_vdc_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmVgpuPolicyProviderVdcScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy vcd_vm_vgpu_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The unique name of the vGPU policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#name VmVgpuPolicy#name}
        :param vgpu_profile: vgpu_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#vgpu_profile VmVgpuPolicy#vgpu_profile}
        :param cpu: cpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#cpu VmVgpuPolicy#cpu}
        :param description: Description of the vGPU policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#description VmVgpuPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#id VmVgpuPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param memory: memory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#memory VmVgpuPolicy#memory}
        :param provider_vdc_scope: provider_vdc_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#provider_vdc_scope VmVgpuPolicy#provider_vdc_scope}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11af979146faba89505ef77ae9b52d9be9cc39b9b58466a8a942606013f34241)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VmVgpuPolicyConfig(
            name=name,
            vgpu_profile=vgpu_profile,
            cpu=cpu,
            description=description,
            id=id,
            memory=memory,
            provider_vdc_scope=provider_vdc_scope,
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
        '''Generates CDKTF code for importing a VmVgpuPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VmVgpuPolicy to import.
        :param import_from_id: The id of the existing VmVgpuPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VmVgpuPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc81372eea9b4d2cd97911dc682e1c3e7985167b6e72bbdeb79ffc1424b145b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCpu")
    def put_cpu(
        self,
        *,
        cores_per_socket: typing.Optional[builtins.str] = None,
        count: typing.Optional[builtins.str] = None,
        limit_in_mhz: typing.Optional[builtins.str] = None,
        reservation_guarantee: typing.Optional[builtins.str] = None,
        shares: typing.Optional[builtins.str] = None,
        speed_in_mhz: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cores_per_socket: The number of cores per socket for a VM. This is a VM hardware configuration. The number of vCPUs that is defined in the VM sizing policy must be divisible by the number of cores per socket. If the number of vCPUs is not divisible by the number of cores per socket, the number of cores per socket becomes invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#cores_per_socket VmVgpuPolicy#cores_per_socket}
        :param count: Defines the number of vCPUs configured for a VM. This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, this count becomes the configured number of vCPUs for the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#count VmVgpuPolicy#count}
        :param limit_in_mhz: Defines the CPU limit in MHz for a VM. If not defined in the VDC compute policy, CPU limit is equal to the vCPU speed multiplied by the number of vCPUs. -1 means unlimited Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#limit_in_mhz VmVgpuPolicy#limit_in_mhz}
        :param reservation_guarantee: Defines how much of the CPU resources of a VM are reserved. The allocated CPU for a VM equals the number of vCPUs times the vCPU speed in MHz. The value of the attribute ranges between 0 and one. Value of 0 CPU reservation guarantee defines no CPU reservation. Value of 1 defines 100% of CPU reserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#reservation_guarantee VmVgpuPolicy#reservation_guarantee}
        :param shares: Defines the number of CPU shares for a VM. Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of CPU as another VM, it is entitled to consume twice as much CPU when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#shares VmVgpuPolicy#shares}
        :param speed_in_mhz: Defines the vCPU speed of a core in MHz. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#speed_in_mhz VmVgpuPolicy#speed_in_mhz}
        '''
        value = VmVgpuPolicyCpu(
            cores_per_socket=cores_per_socket,
            count=count,
            limit_in_mhz=limit_in_mhz,
            reservation_guarantee=reservation_guarantee,
            shares=shares,
            speed_in_mhz=speed_in_mhz,
        )

        return typing.cast(None, jsii.invoke(self, "putCpu", [value]))

    @jsii.member(jsii_name="putMemory")
    def put_memory(
        self,
        *,
        limit_in_mb: typing.Optional[builtins.str] = None,
        reservation_guarantee: typing.Optional[builtins.str] = None,
        shares: typing.Optional[builtins.str] = None,
        size_in_mb: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param limit_in_mb: Defines the memory limit in MB for a VM. If not defined in the VM sizing policy, memory limit is equal to the allocated memory for the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#limit_in_mb VmVgpuPolicy#limit_in_mb}
        :param reservation_guarantee: Defines the reserved amount of memory that is configured for a VM. The value of the attribute ranges between 0 and one. Value of 0 memory reservation guarantee defines no memory reservation. Value of 1 defines 100% of memory reserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#reservation_guarantee VmVgpuPolicy#reservation_guarantee}
        :param shares: Defines the number of memory shares for a VM. Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of memory as another VM, it is entitled to consume twice as much memory when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#shares VmVgpuPolicy#shares}
        :param size_in_mb: Defines the memory configured for a VM in MB. This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, the VM receives the amount of memory defined by this attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#size_in_mb VmVgpuPolicy#size_in_mb}
        '''
        value = VmVgpuPolicyMemory(
            limit_in_mb=limit_in_mb,
            reservation_guarantee=reservation_guarantee,
            shares=shares,
            size_in_mb=size_in_mb,
        )

        return typing.cast(None, jsii.invoke(self, "putMemory", [value]))

    @jsii.member(jsii_name="putProviderVdcScope")
    def put_provider_vdc_scope(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmVgpuPolicyProviderVdcScope", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171de1c1e4c883f0f807f73d23030264ffbda3a72023caac37ef6a495f99ce1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProviderVdcScope", [value]))

    @jsii.member(jsii_name="putVgpuProfile")
    def put_vgpu_profile(self, *, count: jsii.Number, id: builtins.str) -> None:
        '''
        :param count: Specifies the number of vGPU profiles. Must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#count VmVgpuPolicy#count}
        :param id: The identifier of the vGPU profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#id VmVgpuPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = VmVgpuPolicyVgpuProfile(count=count, id=id)

        return typing.cast(None, jsii.invoke(self, "putVgpuProfile", [value]))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetProviderVdcScope")
    def reset_provider_vdc_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderVdcScope", []))

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
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> "VmVgpuPolicyCpuOutputReference":
        return typing.cast("VmVgpuPolicyCpuOutputReference", jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> "VmVgpuPolicyMemoryOutputReference":
        return typing.cast("VmVgpuPolicyMemoryOutputReference", jsii.get(self, "memory"))

    @builtins.property
    @jsii.member(jsii_name="providerVdcScope")
    def provider_vdc_scope(self) -> "VmVgpuPolicyProviderVdcScopeList":
        return typing.cast("VmVgpuPolicyProviderVdcScopeList", jsii.get(self, "providerVdcScope"))

    @builtins.property
    @jsii.member(jsii_name="vgpuProfile")
    def vgpu_profile(self) -> "VmVgpuPolicyVgpuProfileOutputReference":
        return typing.cast("VmVgpuPolicyVgpuProfileOutputReference", jsii.get(self, "vgpuProfile"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional["VmVgpuPolicyCpu"]:
        return typing.cast(typing.Optional["VmVgpuPolicyCpu"], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional["VmVgpuPolicyMemory"]:
        return typing.cast(typing.Optional["VmVgpuPolicyMemory"], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerVdcScopeInput")
    def provider_vdc_scope_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmVgpuPolicyProviderVdcScope"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmVgpuPolicyProviderVdcScope"]]], jsii.get(self, "providerVdcScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="vgpuProfileInput")
    def vgpu_profile_input(self) -> typing.Optional["VmVgpuPolicyVgpuProfile"]:
        return typing.cast(typing.Optional["VmVgpuPolicyVgpuProfile"], jsii.get(self, "vgpuProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622d4c0b425006dc0e3bf3262c3e65be788217c59f556a3ee8d2f3869708e002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358fed85e2fc509298d957048a94d23a1d723033326c0f3ae251becc31824251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083be0a096e0bbebd96f1ea3409b5602b44e09b105f43ff3e161f0126c2440ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyConfig",
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
        "vgpu_profile": "vgpuProfile",
        "cpu": "cpu",
        "description": "description",
        "id": "id",
        "memory": "memory",
        "provider_vdc_scope": "providerVdcScope",
    },
)
class VmVgpuPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        vgpu_profile: typing.Union["VmVgpuPolicyVgpuProfile", typing.Dict[builtins.str, typing.Any]],
        cpu: typing.Optional[typing.Union["VmVgpuPolicyCpu", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        memory: typing.Optional[typing.Union["VmVgpuPolicyMemory", typing.Dict[builtins.str, typing.Any]]] = None,
        provider_vdc_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmVgpuPolicyProviderVdcScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The unique name of the vGPU policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#name VmVgpuPolicy#name}
        :param vgpu_profile: vgpu_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#vgpu_profile VmVgpuPolicy#vgpu_profile}
        :param cpu: cpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#cpu VmVgpuPolicy#cpu}
        :param description: Description of the vGPU policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#description VmVgpuPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#id VmVgpuPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param memory: memory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#memory VmVgpuPolicy#memory}
        :param provider_vdc_scope: provider_vdc_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#provider_vdc_scope VmVgpuPolicy#provider_vdc_scope}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(vgpu_profile, dict):
            vgpu_profile = VmVgpuPolicyVgpuProfile(**vgpu_profile)
        if isinstance(cpu, dict):
            cpu = VmVgpuPolicyCpu(**cpu)
        if isinstance(memory, dict):
            memory = VmVgpuPolicyMemory(**memory)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac8ec4acef4bc310b71f4fbaeb2ea3e37161f2a9982006a1a87ce3900ad780c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vgpu_profile", value=vgpu_profile, expected_type=type_hints["vgpu_profile"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument provider_vdc_scope", value=provider_vdc_scope, expected_type=type_hints["provider_vdc_scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vgpu_profile": vgpu_profile,
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
        if cpu is not None:
            self._values["cpu"] = cpu
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if memory is not None:
            self._values["memory"] = memory
        if provider_vdc_scope is not None:
            self._values["provider_vdc_scope"] = provider_vdc_scope

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
        '''The unique name of the vGPU policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#name VmVgpuPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vgpu_profile(self) -> "VmVgpuPolicyVgpuProfile":
        '''vgpu_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#vgpu_profile VmVgpuPolicy#vgpu_profile}
        '''
        result = self._values.get("vgpu_profile")
        assert result is not None, "Required property 'vgpu_profile' is missing"
        return typing.cast("VmVgpuPolicyVgpuProfile", result)

    @builtins.property
    def cpu(self) -> typing.Optional["VmVgpuPolicyCpu"]:
        '''cpu block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#cpu VmVgpuPolicy#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional["VmVgpuPolicyCpu"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the vGPU policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#description VmVgpuPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#id VmVgpuPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional["VmVgpuPolicyMemory"]:
        '''memory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#memory VmVgpuPolicy#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional["VmVgpuPolicyMemory"], result)

    @builtins.property
    def provider_vdc_scope(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmVgpuPolicyProviderVdcScope"]]]:
        '''provider_vdc_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#provider_vdc_scope VmVgpuPolicy#provider_vdc_scope}
        '''
        result = self._values.get("provider_vdc_scope")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmVgpuPolicyProviderVdcScope"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmVgpuPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyCpu",
    jsii_struct_bases=[],
    name_mapping={
        "cores_per_socket": "coresPerSocket",
        "count": "count",
        "limit_in_mhz": "limitInMhz",
        "reservation_guarantee": "reservationGuarantee",
        "shares": "shares",
        "speed_in_mhz": "speedInMhz",
    },
)
class VmVgpuPolicyCpu:
    def __init__(
        self,
        *,
        cores_per_socket: typing.Optional[builtins.str] = None,
        count: typing.Optional[builtins.str] = None,
        limit_in_mhz: typing.Optional[builtins.str] = None,
        reservation_guarantee: typing.Optional[builtins.str] = None,
        shares: typing.Optional[builtins.str] = None,
        speed_in_mhz: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cores_per_socket: The number of cores per socket for a VM. This is a VM hardware configuration. The number of vCPUs that is defined in the VM sizing policy must be divisible by the number of cores per socket. If the number of vCPUs is not divisible by the number of cores per socket, the number of cores per socket becomes invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#cores_per_socket VmVgpuPolicy#cores_per_socket}
        :param count: Defines the number of vCPUs configured for a VM. This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, this count becomes the configured number of vCPUs for the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#count VmVgpuPolicy#count}
        :param limit_in_mhz: Defines the CPU limit in MHz for a VM. If not defined in the VDC compute policy, CPU limit is equal to the vCPU speed multiplied by the number of vCPUs. -1 means unlimited Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#limit_in_mhz VmVgpuPolicy#limit_in_mhz}
        :param reservation_guarantee: Defines how much of the CPU resources of a VM are reserved. The allocated CPU for a VM equals the number of vCPUs times the vCPU speed in MHz. The value of the attribute ranges between 0 and one. Value of 0 CPU reservation guarantee defines no CPU reservation. Value of 1 defines 100% of CPU reserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#reservation_guarantee VmVgpuPolicy#reservation_guarantee}
        :param shares: Defines the number of CPU shares for a VM. Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of CPU as another VM, it is entitled to consume twice as much CPU when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#shares VmVgpuPolicy#shares}
        :param speed_in_mhz: Defines the vCPU speed of a core in MHz. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#speed_in_mhz VmVgpuPolicy#speed_in_mhz}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92a12e8959393fc6d4dbaebd40a2b354b36fc1afa9ef2136802592beef44841)
            check_type(argname="argument cores_per_socket", value=cores_per_socket, expected_type=type_hints["cores_per_socket"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument limit_in_mhz", value=limit_in_mhz, expected_type=type_hints["limit_in_mhz"])
            check_type(argname="argument reservation_guarantee", value=reservation_guarantee, expected_type=type_hints["reservation_guarantee"])
            check_type(argname="argument shares", value=shares, expected_type=type_hints["shares"])
            check_type(argname="argument speed_in_mhz", value=speed_in_mhz, expected_type=type_hints["speed_in_mhz"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cores_per_socket is not None:
            self._values["cores_per_socket"] = cores_per_socket
        if count is not None:
            self._values["count"] = count
        if limit_in_mhz is not None:
            self._values["limit_in_mhz"] = limit_in_mhz
        if reservation_guarantee is not None:
            self._values["reservation_guarantee"] = reservation_guarantee
        if shares is not None:
            self._values["shares"] = shares
        if speed_in_mhz is not None:
            self._values["speed_in_mhz"] = speed_in_mhz

    @builtins.property
    def cores_per_socket(self) -> typing.Optional[builtins.str]:
        '''The number of cores per socket for a VM.

        This is a VM hardware configuration. The number of vCPUs that is defined in the VM sizing policy must be divisible by the number of cores per socket. If the number of vCPUs is not divisible by the number of cores per socket, the number of cores per socket becomes invalid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#cores_per_socket VmVgpuPolicy#cores_per_socket}
        '''
        result = self._values.get("cores_per_socket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def count(self) -> typing.Optional[builtins.str]:
        '''Defines the number of vCPUs configured for a VM.

        This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, this count becomes the configured number of vCPUs for the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#count VmVgpuPolicy#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit_in_mhz(self) -> typing.Optional[builtins.str]:
        '''Defines the CPU limit in MHz for a VM.

        If not defined in the VDC compute policy, CPU limit is equal to the vCPU speed multiplied by the number of vCPUs. -1 means unlimited

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#limit_in_mhz VmVgpuPolicy#limit_in_mhz}
        '''
        result = self._values.get("limit_in_mhz")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_guarantee(self) -> typing.Optional[builtins.str]:
        '''Defines how much of the CPU resources of a VM are reserved.

        The allocated CPU for a VM equals the number of vCPUs times the vCPU speed in MHz. The value of the attribute ranges between 0 and one. Value of 0 CPU reservation guarantee defines no CPU reservation. Value of 1 defines 100% of CPU reserved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#reservation_guarantee VmVgpuPolicy#reservation_guarantee}
        '''
        result = self._values.get("reservation_guarantee")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shares(self) -> typing.Optional[builtins.str]:
        '''Defines the number of CPU shares for a VM.

        Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of CPU as another VM, it is entitled to consume twice as much CPU when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#shares VmVgpuPolicy#shares}
        '''
        result = self._values.get("shares")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def speed_in_mhz(self) -> typing.Optional[builtins.str]:
        '''Defines the vCPU speed of a core in MHz.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#speed_in_mhz VmVgpuPolicy#speed_in_mhz}
        '''
        result = self._values.get("speed_in_mhz")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmVgpuPolicyCpu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmVgpuPolicyCpuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyCpuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa1e316a6b99aa8f97f9eaf780f91ac00de2a2589d7bdfe458ddb8ee674fd366)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCoresPerSocket")
    def reset_cores_per_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoresPerSocket", []))

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetLimitInMhz")
    def reset_limit_in_mhz(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimitInMhz", []))

    @jsii.member(jsii_name="resetReservationGuarantee")
    def reset_reservation_guarantee(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationGuarantee", []))

    @jsii.member(jsii_name="resetShares")
    def reset_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShares", []))

    @jsii.member(jsii_name="resetSpeedInMhz")
    def reset_speed_in_mhz(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeedInMhz", []))

    @builtins.property
    @jsii.member(jsii_name="coresPerSocketInput")
    def cores_per_socket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coresPerSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInMhzInput")
    def limit_in_mhz_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "limitInMhzInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationGuaranteeInput")
    def reservation_guarantee_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservationGuaranteeInput"))

    @builtins.property
    @jsii.member(jsii_name="sharesInput")
    def shares_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharesInput"))

    @builtins.property
    @jsii.member(jsii_name="speedInMhzInput")
    def speed_in_mhz_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "speedInMhzInput"))

    @builtins.property
    @jsii.member(jsii_name="coresPerSocket")
    def cores_per_socket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coresPerSocket"))

    @cores_per_socket.setter
    def cores_per_socket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389ed641d8c9ee5e8894303af76bfd53ee418bbd9cfe61066c6dfb184fc3d591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coresPerSocket", value)

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "count"))

    @count.setter
    def count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d4e30fd2c815eed488489ecfcb758eee2891946c5ad03b4177a60f7bfced07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="limitInMhz")
    def limit_in_mhz(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limitInMhz"))

    @limit_in_mhz.setter
    def limit_in_mhz(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b730b5ae1a02aae653a3c766d9533849a5b03865e41f0562dead39cead1b5bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitInMhz", value)

    @builtins.property
    @jsii.member(jsii_name="reservationGuarantee")
    def reservation_guarantee(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationGuarantee"))

    @reservation_guarantee.setter
    def reservation_guarantee(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d194b8db5a7edbf639b69edbedbaff07bf8f5dd3f1cd52e734989dea490e991e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationGuarantee", value)

    @builtins.property
    @jsii.member(jsii_name="shares")
    def shares(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shares"))

    @shares.setter
    def shares(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a8d01ed7d4a3b6d239f3c5fb39b2c5104adec2d1a6ba90d3c8685d8fad8416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shares", value)

    @builtins.property
    @jsii.member(jsii_name="speedInMhz")
    def speed_in_mhz(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "speedInMhz"))

    @speed_in_mhz.setter
    def speed_in_mhz(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1029ffa48a88609686f938dc65cff2071d735446b38d10038f71d5eaab832006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speedInMhz", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmVgpuPolicyCpu]:
        return typing.cast(typing.Optional[VmVgpuPolicyCpu], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmVgpuPolicyCpu]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bd17d8a14bb8eb88c98dc7512b4da5acbddf9c70fbf436bf01ed6413c90c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyMemory",
    jsii_struct_bases=[],
    name_mapping={
        "limit_in_mb": "limitInMb",
        "reservation_guarantee": "reservationGuarantee",
        "shares": "shares",
        "size_in_mb": "sizeInMb",
    },
)
class VmVgpuPolicyMemory:
    def __init__(
        self,
        *,
        limit_in_mb: typing.Optional[builtins.str] = None,
        reservation_guarantee: typing.Optional[builtins.str] = None,
        shares: typing.Optional[builtins.str] = None,
        size_in_mb: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param limit_in_mb: Defines the memory limit in MB for a VM. If not defined in the VM sizing policy, memory limit is equal to the allocated memory for the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#limit_in_mb VmVgpuPolicy#limit_in_mb}
        :param reservation_guarantee: Defines the reserved amount of memory that is configured for a VM. The value of the attribute ranges between 0 and one. Value of 0 memory reservation guarantee defines no memory reservation. Value of 1 defines 100% of memory reserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#reservation_guarantee VmVgpuPolicy#reservation_guarantee}
        :param shares: Defines the number of memory shares for a VM. Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of memory as another VM, it is entitled to consume twice as much memory when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#shares VmVgpuPolicy#shares}
        :param size_in_mb: Defines the memory configured for a VM in MB. This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, the VM receives the amount of memory defined by this attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#size_in_mb VmVgpuPolicy#size_in_mb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9635e4d84ea5821abe51fdba1e1aa8b294425841b161290b656dc62db414487)
            check_type(argname="argument limit_in_mb", value=limit_in_mb, expected_type=type_hints["limit_in_mb"])
            check_type(argname="argument reservation_guarantee", value=reservation_guarantee, expected_type=type_hints["reservation_guarantee"])
            check_type(argname="argument shares", value=shares, expected_type=type_hints["shares"])
            check_type(argname="argument size_in_mb", value=size_in_mb, expected_type=type_hints["size_in_mb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limit_in_mb is not None:
            self._values["limit_in_mb"] = limit_in_mb
        if reservation_guarantee is not None:
            self._values["reservation_guarantee"] = reservation_guarantee
        if shares is not None:
            self._values["shares"] = shares
        if size_in_mb is not None:
            self._values["size_in_mb"] = size_in_mb

    @builtins.property
    def limit_in_mb(self) -> typing.Optional[builtins.str]:
        '''Defines the memory limit in MB for a VM.

        If not defined in the VM sizing policy, memory limit is equal to the allocated memory for the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#limit_in_mb VmVgpuPolicy#limit_in_mb}
        '''
        result = self._values.get("limit_in_mb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_guarantee(self) -> typing.Optional[builtins.str]:
        '''Defines the reserved amount of memory that is configured for a VM.

        The value of the attribute ranges between 0 and one. Value of 0 memory reservation guarantee defines no memory reservation. Value of 1 defines 100% of memory reserved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#reservation_guarantee VmVgpuPolicy#reservation_guarantee}
        '''
        result = self._values.get("reservation_guarantee")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shares(self) -> typing.Optional[builtins.str]:
        '''Defines the number of memory shares for a VM.

        Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of memory as another VM, it is entitled to consume twice as much memory when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#shares VmVgpuPolicy#shares}
        '''
        result = self._values.get("shares")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_in_mb(self) -> typing.Optional[builtins.str]:
        '''Defines the memory configured for a VM in MB.

        This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, the VM receives the amount of memory defined by this attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#size_in_mb VmVgpuPolicy#size_in_mb}
        '''
        result = self._values.get("size_in_mb")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmVgpuPolicyMemory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmVgpuPolicyMemoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyMemoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9e60a5feede1f7b1b16bab4a32ce7dab3767fae002683e51f8fec9e1e8685fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLimitInMb")
    def reset_limit_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimitInMb", []))

    @jsii.member(jsii_name="resetReservationGuarantee")
    def reset_reservation_guarantee(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationGuarantee", []))

    @jsii.member(jsii_name="resetShares")
    def reset_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShares", []))

    @jsii.member(jsii_name="resetSizeInMb")
    def reset_size_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeInMb", []))

    @builtins.property
    @jsii.member(jsii_name="limitInMbInput")
    def limit_in_mb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "limitInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationGuaranteeInput")
    def reservation_guarantee_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservationGuaranteeInput"))

    @builtins.property
    @jsii.member(jsii_name="sharesInput")
    def shares_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharesInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInMbInput")
    def size_in_mb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInMb")
    def limit_in_mb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limitInMb"))

    @limit_in_mb.setter
    def limit_in_mb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cedf208c47ed4a28b0b0c2a8bd77990fca680d9dcf8b1507de2375194abaad9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitInMb", value)

    @builtins.property
    @jsii.member(jsii_name="reservationGuarantee")
    def reservation_guarantee(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationGuarantee"))

    @reservation_guarantee.setter
    def reservation_guarantee(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a23d6eb5c5cd39d4fa81c4cefeddc6f4834a95ab5af9f39ba99cc392b461ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationGuarantee", value)

    @builtins.property
    @jsii.member(jsii_name="shares")
    def shares(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shares"))

    @shares.setter
    def shares(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c55ba8e0fbd2fa8e0cdd610c3c5dc0a05cae5ce70baa60dc5ffc029010f0233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shares", value)

    @builtins.property
    @jsii.member(jsii_name="sizeInMb")
    def size_in_mb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeInMb"))

    @size_in_mb.setter
    def size_in_mb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762532b40197ed270d64b4ccd1c7ba3892109353301929f2eb13d581f8623f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInMb", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmVgpuPolicyMemory]:
        return typing.cast(typing.Optional[VmVgpuPolicyMemory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmVgpuPolicyMemory]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ec8a9d6e65db864baaf2fe7ebb23d83497645b5c6b46a23054110c95a3cfca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyProviderVdcScope",
    jsii_struct_bases=[],
    name_mapping={
        "provider_vdc_id": "providerVdcId",
        "cluster_names": "clusterNames",
        "vm_group_id": "vmGroupId",
    },
)
class VmVgpuPolicyProviderVdcScope:
    def __init__(
        self,
        *,
        provider_vdc_id: builtins.str,
        cluster_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param provider_vdc_id: Identifier for the provider virtual data center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#provider_vdc_id VmVgpuPolicy#provider_vdc_id}
        :param cluster_names: Set of cluster names within the provider virtual data center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#cluster_names VmVgpuPolicy#cluster_names}
        :param vm_group_id: Optional identifier for a VM group within the provider VDC scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#vm_group_id VmVgpuPolicy#vm_group_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa341d40a2d445b0fee64bae767c6d693901160b0ae7a399d6106a7d2d329768)
            check_type(argname="argument provider_vdc_id", value=provider_vdc_id, expected_type=type_hints["provider_vdc_id"])
            check_type(argname="argument cluster_names", value=cluster_names, expected_type=type_hints["cluster_names"])
            check_type(argname="argument vm_group_id", value=vm_group_id, expected_type=type_hints["vm_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_vdc_id": provider_vdc_id,
        }
        if cluster_names is not None:
            self._values["cluster_names"] = cluster_names
        if vm_group_id is not None:
            self._values["vm_group_id"] = vm_group_id

    @builtins.property
    def provider_vdc_id(self) -> builtins.str:
        '''Identifier for the provider virtual data center.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#provider_vdc_id VmVgpuPolicy#provider_vdc_id}
        '''
        result = self._values.get("provider_vdc_id")
        assert result is not None, "Required property 'provider_vdc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of cluster names within the provider virtual data center.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#cluster_names VmVgpuPolicy#cluster_names}
        '''
        result = self._values.get("cluster_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vm_group_id(self) -> typing.Optional[builtins.str]:
        '''Optional identifier for a VM group within the provider VDC scope.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#vm_group_id VmVgpuPolicy#vm_group_id}
        '''
        result = self._values.get("vm_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmVgpuPolicyProviderVdcScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmVgpuPolicyProviderVdcScopeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyProviderVdcScopeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cd3ad8364b0f02a5c92c1c7e27547cd4ac861e02c4311f68b7f3afdbc088484)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmVgpuPolicyProviderVdcScopeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735b378c0814ff209f2108e35a9993294553df150c7d799875643fdbbf68686c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmVgpuPolicyProviderVdcScopeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db706ff8c60e6459e17a9386192b4eddf486c57fd1519e02e9b4f9834e61d226)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a01e4cd6ab2ee930cbe91e81d4136b9f6e7a433270f86f455436150dba1e8143)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b1ac8feb43e3f4ef9e9f5c5fc7d767a5aadf00ec06ee819ff150fa580d2a81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmVgpuPolicyProviderVdcScope]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmVgpuPolicyProviderVdcScope]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmVgpuPolicyProviderVdcScope]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411ba5c40effcf0de7bd552ee1db9662583caafcf3e46b165a6e465f53ce5550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VmVgpuPolicyProviderVdcScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyProviderVdcScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08e78261ae9ba0518e0e5bdffd1515d6d5754ab3791adadee9f3ea9f7bc28d2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetClusterNames")
    def reset_cluster_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterNames", []))

    @jsii.member(jsii_name="resetVmGroupId")
    def reset_vm_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmGroupId", []))

    @builtins.property
    @jsii.member(jsii_name="clusterNamesInput")
    def cluster_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clusterNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="providerVdcIdInput")
    def provider_vdc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerVdcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vmGroupIdInput")
    def vm_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNames")
    def cluster_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterNames"))

    @cluster_names.setter
    def cluster_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0151ac2577d46b7f5bcbb498216d2e44e2d796724a78cf32b3131d1c28187c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterNames", value)

    @builtins.property
    @jsii.member(jsii_name="providerVdcId")
    def provider_vdc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerVdcId"))

    @provider_vdc_id.setter
    def provider_vdc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f460092697eb82b9c82a81865d9ac4925e7f2dfde87c3c8bdcf937e57460741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerVdcId", value)

    @builtins.property
    @jsii.member(jsii_name="vmGroupId")
    def vm_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmGroupId"))

    @vm_group_id.setter
    def vm_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc75e7883328c2eb0a1b8b2bd7632ad84fa90c270d64c24873941927fa5e2569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmVgpuPolicyProviderVdcScope]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmVgpuPolicyProviderVdcScope]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmVgpuPolicyProviderVdcScope]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a61d4f4154e0ccf51a50f3035185b1d2180e4d5f4716bf1a3d87bcd23359c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyVgpuProfile",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "id": "id"},
)
class VmVgpuPolicyVgpuProfile:
    def __init__(self, *, count: jsii.Number, id: builtins.str) -> None:
        '''
        :param count: Specifies the number of vGPU profiles. Must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#count VmVgpuPolicy#count}
        :param id: The identifier of the vGPU profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#id VmVgpuPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2339909d684c249e8656fc09c730866d416985be2a5366612fe39e4778767ec9)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "id": id,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Specifies the number of vGPU profiles. Must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#count VmVgpuPolicy#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The identifier of the vGPU profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_vgpu_policy#id VmVgpuPolicy#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmVgpuPolicyVgpuProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmVgpuPolicyVgpuProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmVgpuPolicy.VmVgpuPolicyVgpuProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1de96c90d4696e6df6f80778440b14c67fc3ce6b0e7b1823caed31b51d8e8613)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0f78f343cd890d02a45069098f130c9f0a6cf727f7dc69bba41dd4cffd1f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc7523d087f732519849fd145abaa2a12df0ada045f4f437523ff9a837a3ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmVgpuPolicyVgpuProfile]:
        return typing.cast(typing.Optional[VmVgpuPolicyVgpuProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmVgpuPolicyVgpuProfile]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608c9f7a8958b7f8193d0bbc394b20c2d27632f3effc3f688c0f1760fcc3000f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VmVgpuPolicy",
    "VmVgpuPolicyConfig",
    "VmVgpuPolicyCpu",
    "VmVgpuPolicyCpuOutputReference",
    "VmVgpuPolicyMemory",
    "VmVgpuPolicyMemoryOutputReference",
    "VmVgpuPolicyProviderVdcScope",
    "VmVgpuPolicyProviderVdcScopeList",
    "VmVgpuPolicyProviderVdcScopeOutputReference",
    "VmVgpuPolicyVgpuProfile",
    "VmVgpuPolicyVgpuProfileOutputReference",
]

publication.publish()

def _typecheckingstub__11af979146faba89505ef77ae9b52d9be9cc39b9b58466a8a942606013f34241(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    vgpu_profile: typing.Union[VmVgpuPolicyVgpuProfile, typing.Dict[builtins.str, typing.Any]],
    cpu: typing.Optional[typing.Union[VmVgpuPolicyCpu, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    memory: typing.Optional[typing.Union[VmVgpuPolicyMemory, typing.Dict[builtins.str, typing.Any]]] = None,
    provider_vdc_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmVgpuPolicyProviderVdcScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__cc81372eea9b4d2cd97911dc682e1c3e7985167b6e72bbdeb79ffc1424b145b6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171de1c1e4c883f0f807f73d23030264ffbda3a72023caac37ef6a495f99ce1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmVgpuPolicyProviderVdcScope, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622d4c0b425006dc0e3bf3262c3e65be788217c59f556a3ee8d2f3869708e002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358fed85e2fc509298d957048a94d23a1d723033326c0f3ae251becc31824251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083be0a096e0bbebd96f1ea3409b5602b44e09b105f43ff3e161f0126c2440ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac8ec4acef4bc310b71f4fbaeb2ea3e37161f2a9982006a1a87ce3900ad780c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    vgpu_profile: typing.Union[VmVgpuPolicyVgpuProfile, typing.Dict[builtins.str, typing.Any]],
    cpu: typing.Optional[typing.Union[VmVgpuPolicyCpu, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    memory: typing.Optional[typing.Union[VmVgpuPolicyMemory, typing.Dict[builtins.str, typing.Any]]] = None,
    provider_vdc_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmVgpuPolicyProviderVdcScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92a12e8959393fc6d4dbaebd40a2b354b36fc1afa9ef2136802592beef44841(
    *,
    cores_per_socket: typing.Optional[builtins.str] = None,
    count: typing.Optional[builtins.str] = None,
    limit_in_mhz: typing.Optional[builtins.str] = None,
    reservation_guarantee: typing.Optional[builtins.str] = None,
    shares: typing.Optional[builtins.str] = None,
    speed_in_mhz: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1e316a6b99aa8f97f9eaf780f91ac00de2a2589d7bdfe458ddb8ee674fd366(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389ed641d8c9ee5e8894303af76bfd53ee418bbd9cfe61066c6dfb184fc3d591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d4e30fd2c815eed488489ecfcb758eee2891946c5ad03b4177a60f7bfced07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b730b5ae1a02aae653a3c766d9533849a5b03865e41f0562dead39cead1b5bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d194b8db5a7edbf639b69edbedbaff07bf8f5dd3f1cd52e734989dea490e991e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a8d01ed7d4a3b6d239f3c5fb39b2c5104adec2d1a6ba90d3c8685d8fad8416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1029ffa48a88609686f938dc65cff2071d735446b38d10038f71d5eaab832006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bd17d8a14bb8eb88c98dc7512b4da5acbddf9c70fbf436bf01ed6413c90c49(
    value: typing.Optional[VmVgpuPolicyCpu],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9635e4d84ea5821abe51fdba1e1aa8b294425841b161290b656dc62db414487(
    *,
    limit_in_mb: typing.Optional[builtins.str] = None,
    reservation_guarantee: typing.Optional[builtins.str] = None,
    shares: typing.Optional[builtins.str] = None,
    size_in_mb: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e60a5feede1f7b1b16bab4a32ce7dab3767fae002683e51f8fec9e1e8685fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cedf208c47ed4a28b0b0c2a8bd77990fca680d9dcf8b1507de2375194abaad9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a23d6eb5c5cd39d4fa81c4cefeddc6f4834a95ab5af9f39ba99cc392b461ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c55ba8e0fbd2fa8e0cdd610c3c5dc0a05cae5ce70baa60dc5ffc029010f0233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762532b40197ed270d64b4ccd1c7ba3892109353301929f2eb13d581f8623f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ec8a9d6e65db864baaf2fe7ebb23d83497645b5c6b46a23054110c95a3cfca(
    value: typing.Optional[VmVgpuPolicyMemory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa341d40a2d445b0fee64bae767c6d693901160b0ae7a399d6106a7d2d329768(
    *,
    provider_vdc_id: builtins.str,
    cluster_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd3ad8364b0f02a5c92c1c7e27547cd4ac861e02c4311f68b7f3afdbc088484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735b378c0814ff209f2108e35a9993294553df150c7d799875643fdbbf68686c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db706ff8c60e6459e17a9386192b4eddf486c57fd1519e02e9b4f9834e61d226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01e4cd6ab2ee930cbe91e81d4136b9f6e7a433270f86f455436150dba1e8143(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1ac8feb43e3f4ef9e9f5c5fc7d767a5aadf00ec06ee819ff150fa580d2a81d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411ba5c40effcf0de7bd552ee1db9662583caafcf3e46b165a6e465f53ce5550(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmVgpuPolicyProviderVdcScope]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e78261ae9ba0518e0e5bdffd1515d6d5754ab3791adadee9f3ea9f7bc28d2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0151ac2577d46b7f5bcbb498216d2e44e2d796724a78cf32b3131d1c28187c81(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f460092697eb82b9c82a81865d9ac4925e7f2dfde87c3c8bdcf937e57460741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc75e7883328c2eb0a1b8b2bd7632ad84fa90c270d64c24873941927fa5e2569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a61d4f4154e0ccf51a50f3035185b1d2180e4d5f4716bf1a3d87bcd23359c03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmVgpuPolicyProviderVdcScope]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2339909d684c249e8656fc09c730866d416985be2a5366612fe39e4778767ec9(
    *,
    count: jsii.Number,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de96c90d4696e6df6f80778440b14c67fc3ce6b0e7b1823caed31b51d8e8613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0f78f343cd890d02a45069098f130c9f0a6cf727f7dc69bba41dd4cffd1f72(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc7523d087f732519849fd145abaa2a12df0ada045f4f437523ff9a837a3ee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608c9f7a8958b7f8193d0bbc394b20c2d27632f3effc3f688c0f1760fcc3000f(
    value: typing.Optional[VmVgpuPolicyVgpuProfile],
) -> None:
    """Type checking stubs"""
    pass
