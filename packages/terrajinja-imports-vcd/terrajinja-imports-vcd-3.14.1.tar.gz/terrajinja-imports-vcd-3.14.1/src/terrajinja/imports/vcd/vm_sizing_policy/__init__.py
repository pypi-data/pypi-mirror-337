'''
# `vcd_vm_sizing_policy`

Refer to the Terraform Registry for docs: [`vcd_vm_sizing_policy`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy).
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


class VmSizingPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmSizingPolicy.VmSizingPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy vcd_vm_sizing_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        cpu: typing.Optional[typing.Union["VmSizingPolicyCpu", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        memory: typing.Optional[typing.Union["VmSizingPolicyMemory", typing.Dict[builtins.str, typing.Any]]] = None,
        org: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy vcd_vm_sizing_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#name VmSizingPolicy#name}.
        :param cpu: cpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#cpu VmSizingPolicy#cpu}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#description VmSizingPolicy#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#id VmSizingPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param memory: memory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#memory VmSizingPolicy#memory}
        :param org: The name of organization to use - Deprecated and unneeded: will be ignored if used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#org VmSizingPolicy#org}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d04a9a851d3f0539d587aeb8600fd818b849aece243143e8751811ddc029b1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VmSizingPolicyConfig(
            name=name,
            cpu=cpu,
            description=description,
            id=id,
            memory=memory,
            org=org,
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
        '''Generates CDKTF code for importing a VmSizingPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VmSizingPolicy to import.
        :param import_from_id: The id of the existing VmSizingPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VmSizingPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03194269aa90e17c884bc635c8085313f3bba21bcd4fbbfd841cd4c73d03d986)
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
        :param cores_per_socket: The number of cores per socket for a VM. This is a VM hardware configuration. The number of vCPUs that is defined in the VM sizing policy must be divisible by the number of cores per socket. If the number of vCPUs is not divisible by the number of cores per socket, the number of cores per socket becomes invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#cores_per_socket VmSizingPolicy#cores_per_socket}
        :param count: Defines the number of vCPUs configured for a VM. This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, this count becomes the configured number of vCPUs for the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#count VmSizingPolicy#count}
        :param limit_in_mhz: Defines the CPU limit in MHz for a VM. If not defined in the VDC compute policy, CPU limit is equal to the vCPU speed multiplied by the number of vCPUs. -1 means unlimited Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#limit_in_mhz VmSizingPolicy#limit_in_mhz}
        :param reservation_guarantee: Defines how much of the CPU resources of a VM are reserved. The allocated CPU for a VM equals the number of vCPUs times the vCPU speed in MHz. The value of the attribute ranges between 0 and one. Value of 0 CPU reservation guarantee defines no CPU reservation. Value of 1 defines 100% of CPU reserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#reservation_guarantee VmSizingPolicy#reservation_guarantee}
        :param shares: Defines the number of CPU shares for a VM. Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of CPU as another VM, it is entitled to consume twice as much CPU when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#shares VmSizingPolicy#shares}
        :param speed_in_mhz: Defines the vCPU speed of a core in MHz. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#speed_in_mhz VmSizingPolicy#speed_in_mhz}
        '''
        value = VmSizingPolicyCpu(
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
        :param limit_in_mb: Defines the memory limit in MB for a VM. If not defined in the VM sizing policy, memory limit is equal to the allocated memory for the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#limit_in_mb VmSizingPolicy#limit_in_mb}
        :param reservation_guarantee: Defines the reserved amount of memory that is configured for a VM. The value of the attribute ranges between 0 and one. Value of 0 memory reservation guarantee defines no memory reservation. Value of 1 defines 100% of memory reserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#reservation_guarantee VmSizingPolicy#reservation_guarantee}
        :param shares: Defines the number of memory shares for a VM. Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of memory as another VM, it is entitled to consume twice as much memory when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#shares VmSizingPolicy#shares}
        :param size_in_mb: Defines the memory configured for a VM in MB. This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, the VM receives the amount of memory defined by this attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#size_in_mb VmSizingPolicy#size_in_mb}
        '''
        value = VmSizingPolicyMemory(
            limit_in_mb=limit_in_mb,
            reservation_guarantee=reservation_guarantee,
            shares=shares,
            size_in_mb=size_in_mb,
        )

        return typing.cast(None, jsii.invoke(self, "putMemory", [value]))

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

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

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
    def cpu(self) -> "VmSizingPolicyCpuOutputReference":
        return typing.cast("VmSizingPolicyCpuOutputReference", jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> "VmSizingPolicyMemoryOutputReference":
        return typing.cast("VmSizingPolicyMemoryOutputReference", jsii.get(self, "memory"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional["VmSizingPolicyCpu"]:
        return typing.cast(typing.Optional["VmSizingPolicyCpu"], jsii.get(self, "cpuInput"))

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
    def memory_input(self) -> typing.Optional["VmSizingPolicyMemory"]:
        return typing.cast(typing.Optional["VmSizingPolicyMemory"], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4e7b1027ded4d294b7bd5ac6e7af5ed71cc04ea5ee27ec56ea29c1339c71fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb978163b204fcd8dfed094bf7912d479d7ec58b0a40f6e08c669843919da0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4056f3b364187231256ae6b15ab73dbd70313631731f3ed1f013e8d7d6fef70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d33c4c5c293374d8dbdfa1bc9a4ea0d0678941f5432fe68108f5ff6e73a2866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)


@jsii.data_type(
    jsii_type="vcd.vmSizingPolicy.VmSizingPolicyConfig",
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
        "cpu": "cpu",
        "description": "description",
        "id": "id",
        "memory": "memory",
        "org": "org",
    },
)
class VmSizingPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cpu: typing.Optional[typing.Union["VmSizingPolicyCpu", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        memory: typing.Optional[typing.Union["VmSizingPolicyMemory", typing.Dict[builtins.str, typing.Any]]] = None,
        org: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#name VmSizingPolicy#name}.
        :param cpu: cpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#cpu VmSizingPolicy#cpu}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#description VmSizingPolicy#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#id VmSizingPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param memory: memory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#memory VmSizingPolicy#memory}
        :param org: The name of organization to use - Deprecated and unneeded: will be ignored if used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#org VmSizingPolicy#org}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cpu, dict):
            cpu = VmSizingPolicyCpu(**cpu)
        if isinstance(memory, dict):
            memory = VmSizingPolicyMemory(**memory)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3c505a17fffdc36ef9755a457f4df45725373985195fd68d267a723428a764)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
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
        if cpu is not None:
            self._values["cpu"] = cpu
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if memory is not None:
            self._values["memory"] = memory
        if org is not None:
            self._values["org"] = org

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#name VmSizingPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cpu(self) -> typing.Optional["VmSizingPolicyCpu"]:
        '''cpu block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#cpu VmSizingPolicy#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional["VmSizingPolicyCpu"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#description VmSizingPolicy#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#id VmSizingPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional["VmSizingPolicyMemory"]:
        '''memory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#memory VmSizingPolicy#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional["VmSizingPolicyMemory"], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use - Deprecated and unneeded: will be ignored if used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#org VmSizingPolicy#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmSizingPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.vmSizingPolicy.VmSizingPolicyCpu",
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
class VmSizingPolicyCpu:
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
        :param cores_per_socket: The number of cores per socket for a VM. This is a VM hardware configuration. The number of vCPUs that is defined in the VM sizing policy must be divisible by the number of cores per socket. If the number of vCPUs is not divisible by the number of cores per socket, the number of cores per socket becomes invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#cores_per_socket VmSizingPolicy#cores_per_socket}
        :param count: Defines the number of vCPUs configured for a VM. This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, this count becomes the configured number of vCPUs for the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#count VmSizingPolicy#count}
        :param limit_in_mhz: Defines the CPU limit in MHz for a VM. If not defined in the VDC compute policy, CPU limit is equal to the vCPU speed multiplied by the number of vCPUs. -1 means unlimited Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#limit_in_mhz VmSizingPolicy#limit_in_mhz}
        :param reservation_guarantee: Defines how much of the CPU resources of a VM are reserved. The allocated CPU for a VM equals the number of vCPUs times the vCPU speed in MHz. The value of the attribute ranges between 0 and one. Value of 0 CPU reservation guarantee defines no CPU reservation. Value of 1 defines 100% of CPU reserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#reservation_guarantee VmSizingPolicy#reservation_guarantee}
        :param shares: Defines the number of CPU shares for a VM. Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of CPU as another VM, it is entitled to consume twice as much CPU when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#shares VmSizingPolicy#shares}
        :param speed_in_mhz: Defines the vCPU speed of a core in MHz. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#speed_in_mhz VmSizingPolicy#speed_in_mhz}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67277b82e6d1e5a1252fa1754c2d73f2fd7ebaff215650aa0a518ee6909f00f7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#cores_per_socket VmSizingPolicy#cores_per_socket}
        '''
        result = self._values.get("cores_per_socket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def count(self) -> typing.Optional[builtins.str]:
        '''Defines the number of vCPUs configured for a VM.

        This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, this count becomes the configured number of vCPUs for the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#count VmSizingPolicy#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit_in_mhz(self) -> typing.Optional[builtins.str]:
        '''Defines the CPU limit in MHz for a VM.

        If not defined in the VDC compute policy, CPU limit is equal to the vCPU speed multiplied by the number of vCPUs. -1 means unlimited

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#limit_in_mhz VmSizingPolicy#limit_in_mhz}
        '''
        result = self._values.get("limit_in_mhz")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_guarantee(self) -> typing.Optional[builtins.str]:
        '''Defines how much of the CPU resources of a VM are reserved.

        The allocated CPU for a VM equals the number of vCPUs times the vCPU speed in MHz. The value of the attribute ranges between 0 and one. Value of 0 CPU reservation guarantee defines no CPU reservation. Value of 1 defines 100% of CPU reserved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#reservation_guarantee VmSizingPolicy#reservation_guarantee}
        '''
        result = self._values.get("reservation_guarantee")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shares(self) -> typing.Optional[builtins.str]:
        '''Defines the number of CPU shares for a VM.

        Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of CPU as another VM, it is entitled to consume twice as much CPU when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#shares VmSizingPolicy#shares}
        '''
        result = self._values.get("shares")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def speed_in_mhz(self) -> typing.Optional[builtins.str]:
        '''Defines the vCPU speed of a core in MHz.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#speed_in_mhz VmSizingPolicy#speed_in_mhz}
        '''
        result = self._values.get("speed_in_mhz")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmSizingPolicyCpu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmSizingPolicyCpuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmSizingPolicy.VmSizingPolicyCpuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a170b5f232f8f4d4b814df802f134033acc79ad81cd399e32aad91977d4ec8a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62ac20953c12e8fcef73305d001e4f47cd5edf4e95a47364f15dff2c10a3903f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coresPerSocket", value)

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "count"))

    @count.setter
    def count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc1001c946252d9b3deea35cf208b84bedf223f6cfd05a5d77c962fdea1c3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="limitInMhz")
    def limit_in_mhz(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limitInMhz"))

    @limit_in_mhz.setter
    def limit_in_mhz(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f58bdc83ed1e35e2c0034c0c90f861c9818280e3a831063cf2fd6a58983a385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitInMhz", value)

    @builtins.property
    @jsii.member(jsii_name="reservationGuarantee")
    def reservation_guarantee(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationGuarantee"))

    @reservation_guarantee.setter
    def reservation_guarantee(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580bf95d481017a845e5516937b833fe624ee461d3e82c89a8726cb85aeba76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationGuarantee", value)

    @builtins.property
    @jsii.member(jsii_name="shares")
    def shares(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shares"))

    @shares.setter
    def shares(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0749e0d65fd0bd46e885909b58b3920be476b5f2da840f34199a83a6c98cf975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shares", value)

    @builtins.property
    @jsii.member(jsii_name="speedInMhz")
    def speed_in_mhz(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "speedInMhz"))

    @speed_in_mhz.setter
    def speed_in_mhz(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd891f69699817aadad25baa17839e696e7e243695f97068bc55928aa50315f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speedInMhz", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmSizingPolicyCpu]:
        return typing.cast(typing.Optional[VmSizingPolicyCpu], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmSizingPolicyCpu]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade6043540a66a7c17c19afc10d0fba596208aeb0124bd8601255ead8ea6a38b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vmSizingPolicy.VmSizingPolicyMemory",
    jsii_struct_bases=[],
    name_mapping={
        "limit_in_mb": "limitInMb",
        "reservation_guarantee": "reservationGuarantee",
        "shares": "shares",
        "size_in_mb": "sizeInMb",
    },
)
class VmSizingPolicyMemory:
    def __init__(
        self,
        *,
        limit_in_mb: typing.Optional[builtins.str] = None,
        reservation_guarantee: typing.Optional[builtins.str] = None,
        shares: typing.Optional[builtins.str] = None,
        size_in_mb: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param limit_in_mb: Defines the memory limit in MB for a VM. If not defined in the VM sizing policy, memory limit is equal to the allocated memory for the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#limit_in_mb VmSizingPolicy#limit_in_mb}
        :param reservation_guarantee: Defines the reserved amount of memory that is configured for a VM. The value of the attribute ranges between 0 and one. Value of 0 memory reservation guarantee defines no memory reservation. Value of 1 defines 100% of memory reserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#reservation_guarantee VmSizingPolicy#reservation_guarantee}
        :param shares: Defines the number of memory shares for a VM. Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of memory as another VM, it is entitled to consume twice as much memory when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#shares VmSizingPolicy#shares}
        :param size_in_mb: Defines the memory configured for a VM in MB. This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, the VM receives the amount of memory defined by this attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#size_in_mb VmSizingPolicy#size_in_mb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d894109019bcd8b4408ac73ce9fff80cbac3f74e6e5fadcdae38de1187a75e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#limit_in_mb VmSizingPolicy#limit_in_mb}
        '''
        result = self._values.get("limit_in_mb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_guarantee(self) -> typing.Optional[builtins.str]:
        '''Defines the reserved amount of memory that is configured for a VM.

        The value of the attribute ranges between 0 and one. Value of 0 memory reservation guarantee defines no memory reservation. Value of 1 defines 100% of memory reserved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#reservation_guarantee VmSizingPolicy#reservation_guarantee}
        '''
        result = self._values.get("reservation_guarantee")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shares(self) -> typing.Optional[builtins.str]:
        '''Defines the number of memory shares for a VM.

        Shares specify the relative importance of a VM within a virtual data center. If a VM has twice as many shares of memory as another VM, it is entitled to consume twice as much memory when these two virtual machines are competing for resources. If not defined in the VDC compute policy, normal shares are applied to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#shares VmSizingPolicy#shares}
        '''
        result = self._values.get("shares")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_in_mb(self) -> typing.Optional[builtins.str]:
        '''Defines the memory configured for a VM in MB.

        This is a VM hardware configuration. When a tenant assigns the VM sizing policy to a VM, the VM receives the amount of memory defined by this attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm_sizing_policy#size_in_mb VmSizingPolicy#size_in_mb}
        '''
        result = self._values.get("size_in_mb")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmSizingPolicyMemory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmSizingPolicyMemoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vmSizingPolicy.VmSizingPolicyMemoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__967e50dead98dd01a09519afeff537f5a922441213f87ff41a40eee294994006)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97a153190a9fb2c6e5f37b6f031169727b14d629589be6c32ad807726d71497b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitInMb", value)

    @builtins.property
    @jsii.member(jsii_name="reservationGuarantee")
    def reservation_guarantee(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationGuarantee"))

    @reservation_guarantee.setter
    def reservation_guarantee(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d7d8085384045a28592d1b404d98d194a6ceb4ea15f77d9a06ea5c7590330f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationGuarantee", value)

    @builtins.property
    @jsii.member(jsii_name="shares")
    def shares(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shares"))

    @shares.setter
    def shares(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202e43f7ddfb5a2a8ca7f5b4b9eed2f0de660b7165be924a1e2ca0b43d506696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shares", value)

    @builtins.property
    @jsii.member(jsii_name="sizeInMb")
    def size_in_mb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeInMb"))

    @size_in_mb.setter
    def size_in_mb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb84968d9608144a57aab35991b3008cfc602814863df88ec19ad3b3167e936e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInMb", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmSizingPolicyMemory]:
        return typing.cast(typing.Optional[VmSizingPolicyMemory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmSizingPolicyMemory]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506b2023cfa763034c3fe7bdb8864299e0993f8e8441f1131fc7d9909c38d3f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VmSizingPolicy",
    "VmSizingPolicyConfig",
    "VmSizingPolicyCpu",
    "VmSizingPolicyCpuOutputReference",
    "VmSizingPolicyMemory",
    "VmSizingPolicyMemoryOutputReference",
]

publication.publish()

def _typecheckingstub__8d04a9a851d3f0539d587aeb8600fd818b849aece243143e8751811ddc029b1b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    cpu: typing.Optional[typing.Union[VmSizingPolicyCpu, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    memory: typing.Optional[typing.Union[VmSizingPolicyMemory, typing.Dict[builtins.str, typing.Any]]] = None,
    org: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__03194269aa90e17c884bc635c8085313f3bba21bcd4fbbfd841cd4c73d03d986(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4e7b1027ded4d294b7bd5ac6e7af5ed71cc04ea5ee27ec56ea29c1339c71fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb978163b204fcd8dfed094bf7912d479d7ec58b0a40f6e08c669843919da0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4056f3b364187231256ae6b15ab73dbd70313631731f3ed1f013e8d7d6fef70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d33c4c5c293374d8dbdfa1bc9a4ea0d0678941f5432fe68108f5ff6e73a2866(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3c505a17fffdc36ef9755a457f4df45725373985195fd68d267a723428a764(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    cpu: typing.Optional[typing.Union[VmSizingPolicyCpu, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    memory: typing.Optional[typing.Union[VmSizingPolicyMemory, typing.Dict[builtins.str, typing.Any]]] = None,
    org: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67277b82e6d1e5a1252fa1754c2d73f2fd7ebaff215650aa0a518ee6909f00f7(
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

def _typecheckingstub__a170b5f232f8f4d4b814df802f134033acc79ad81cd399e32aad91977d4ec8a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ac20953c12e8fcef73305d001e4f47cd5edf4e95a47364f15dff2c10a3903f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc1001c946252d9b3deea35cf208b84bedf223f6cfd05a5d77c962fdea1c3d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f58bdc83ed1e35e2c0034c0c90f861c9818280e3a831063cf2fd6a58983a385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580bf95d481017a845e5516937b833fe624ee461d3e82c89a8726cb85aeba76d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0749e0d65fd0bd46e885909b58b3920be476b5f2da840f34199a83a6c98cf975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd891f69699817aadad25baa17839e696e7e243695f97068bc55928aa50315f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade6043540a66a7c17c19afc10d0fba596208aeb0124bd8601255ead8ea6a38b(
    value: typing.Optional[VmSizingPolicyCpu],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d894109019bcd8b4408ac73ce9fff80cbac3f74e6e5fadcdae38de1187a75e(
    *,
    limit_in_mb: typing.Optional[builtins.str] = None,
    reservation_guarantee: typing.Optional[builtins.str] = None,
    shares: typing.Optional[builtins.str] = None,
    size_in_mb: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967e50dead98dd01a09519afeff537f5a922441213f87ff41a40eee294994006(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a153190a9fb2c6e5f37b6f031169727b14d629589be6c32ad807726d71497b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d7d8085384045a28592d1b404d98d194a6ceb4ea15f77d9a06ea5c7590330f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202e43f7ddfb5a2a8ca7f5b4b9eed2f0de660b7165be924a1e2ca0b43d506696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb84968d9608144a57aab35991b3008cfc602814863df88ec19ad3b3167e936e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506b2023cfa763034c3fe7bdb8864299e0993f8e8441f1131fc7d9909c38d3f3(
    value: typing.Optional[VmSizingPolicyMemory],
) -> None:
    """Type checking stubs"""
    pass
