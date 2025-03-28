'''
# `vcd_org_vdc`

Refer to the Terraform Registry for docs: [`vcd_org_vdc`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc).
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


class OrgVdc(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdc.OrgVdc",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc vcd_org_vdc}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        allocation_model: builtins.str,
        compute_capacity: typing.Union["OrgVdcComputeCapacity", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        provider_vdc_name: builtins.str,
        storage_profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcStorageProfile", typing.Dict[builtins.str, typing.Any]]]],
        allow_over_commit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_guaranteed: typing.Optional[jsii.Number] = None,
        cpu_speed: typing.Optional[jsii.Number] = None,
        default_compute_policy_id: typing.Optional[builtins.str] = None,
        default_vm_sizing_policy_id: typing.Optional[builtins.str] = None,
        delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_cluster_id: typing.Optional[builtins.str] = None,
        elasticity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_fast_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_nsxv_distributed_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_thin_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vm_discovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        include_vm_memory_overhead: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_guaranteed: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_pool_name: typing.Optional[builtins.str] = None,
        network_quota: typing.Optional[jsii.Number] = None,
        nic_quota: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        vm_placement_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_quota: typing.Optional[jsii.Number] = None,
        vm_sizing_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_vgpu_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc vcd_org_vdc} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param allocation_model: The allocation model used by this VDC; must be one of {AllocationVApp, AllocationPool, ReservationPool, Flex}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocation_model OrgVdc#allocation_model}
        :param compute_capacity: compute_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#compute_capacity OrgVdc#compute_capacity}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#name OrgVdc#name}.
        :param provider_vdc_name: A reference to the Provider VDC from which this organization VDC is provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#provider_vdc_name OrgVdc#provider_vdc_name}
        :param storage_profile: storage_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#storage_profile OrgVdc#storage_profile}
        :param allow_over_commit: Set to false to disallow creation of the VDC if the AllocationModel is AllocationPool or ReservationPool and the ComputeCapacity you specified is greater than what the backing Provider VDC can supply. Default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allow_over_commit OrgVdc#allow_over_commit}
        :param cpu_guaranteed: Percentage of allocated CPU resources guaranteed to vApps deployed in this VDC. For example, if this value is 0.75, then 75% of allocated resources are guaranteed. Required when AllocationModel is AllocationVApp or AllocationPool. If the element is empty, vCD sets a value Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu_guaranteed OrgVdc#cpu_guaranteed}
        :param cpu_speed: Specifies the clock frequency, in Megahertz, for any virtual CPU that is allocated to a VM. A VM with 2 vCPUs will consume twice as much of this value. Ignored for ReservationPool. Required when AllocationModel is AllocationVApp or AllocationPool, and may not be less than 256 MHz. Defaults to 1000 MHz if the element is empty or missing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu_speed OrgVdc#cpu_speed}
        :param default_compute_policy_id: ID of default Compute policy for this VDC, which can be a VM Sizing Policy, VM Placement Policy or vGPU Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#default_compute_policy_id OrgVdc#default_compute_policy_id}
        :param default_vm_sizing_policy_id: ID of default VM Compute policy, which can be a VM Sizing Policy, VM Placement Policy or vGPU Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#default_vm_sizing_policy_id OrgVdc#default_vm_sizing_policy_id}
        :param delete_force: When destroying use delete_force=True to remove a VDC and any objects it contains, regardless of their state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#delete_force OrgVdc#delete_force}
        :param delete_recursive: When destroying use delete_recursive=True to remove the VDC and any objects it contains that are in a state that normally allows removal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#delete_recursive OrgVdc#delete_recursive}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#description OrgVdc#description}.
        :param edge_cluster_id: ID of NSX-T Edge Cluster (provider vApp networking services and DHCP capability for Isolated networks). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#edge_cluster_id OrgVdc#edge_cluster_id}
        :param elasticity: Set to true to indicate if the Flex VDC is to be elastic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#elasticity OrgVdc#elasticity}
        :param enabled: True if this VDC is enabled for use by the organization VDCs. Default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enabled OrgVdc#enabled}
        :param enable_fast_provisioning: Request for fast provisioning. Request will be honored only if the underlying datas tore supports it. Fast provisioning can reduce the time it takes to create virtual machines by using vSphere linked clones. If you disable fast provisioning, all provisioning operations will result in full clones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_fast_provisioning OrgVdc#enable_fast_provisioning}
        :param enable_nsxv_distributed_firewall: Set to true to enable distributed firewall - Only applies to NSX-V VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_nsxv_distributed_firewall OrgVdc#enable_nsxv_distributed_firewall}
        :param enable_thin_provisioning: Boolean to request thin provisioning. Request will be honored only if the underlying datastore supports it. Thin provisioning saves storage space by committing it on demand. This allows over-allocation of storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_thin_provisioning OrgVdc#enable_thin_provisioning}
        :param enable_vm_discovery: True if discovery of vCenter VMs is enabled for resource pools backing this VDC. If left unspecified, the actual behaviour depends on enablement at the organization level and at the system level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_vm_discovery OrgVdc#enable_vm_discovery}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#id OrgVdc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_vm_memory_overhead: Set to true to indicate if the Flex VDC is to include memory overhead into its accounting for admission control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#include_vm_memory_overhead OrgVdc#include_vm_memory_overhead}
        :param memory_guaranteed: Percentage of allocated memory resources guaranteed to vApps deployed in this VDC. For example, if this value is 0.75, then 75% of allocated resources are guaranteed. Required when AllocationModel is AllocationVApp or AllocationPool. When Allocation model is AllocationPool minimum value is 0.2. If the element is empty, vCD sets a value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#memory_guaranteed OrgVdc#memory_guaranteed}
        :param metadata: Key and value pairs for Org VDC metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#metadata OrgVdc#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#metadata_entry OrgVdc#metadata_entry}
        :param network_pool_name: The name of a network pool in the Provider VDC. Required if this VDC will contain routed or isolated networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#network_pool_name OrgVdc#network_pool_name}
        :param network_quota: Maximum number of network objects that can be deployed in this VDC. Defaults to 0, which means no networks can be deployed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#network_quota OrgVdc#network_quota}
        :param nic_quota: Maximum number of virtual NICs allowed in this VDC. Defaults to 0, which specifies an unlimited number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#nic_quota OrgVdc#nic_quota}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#org OrgVdc#org}
        :param vm_placement_policy_ids: Set of VM Placement Policy IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_placement_policy_ids OrgVdc#vm_placement_policy_ids}
        :param vm_quota: The maximum number of VMs that can be created in this VDC. Includes deployed and undeployed VMs in vApps and vApp templates. Defaults to 0, which specifies an unlimited number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_quota OrgVdc#vm_quota}
        :param vm_sizing_policy_ids: Set of VM Sizing Policy IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_sizing_policy_ids OrgVdc#vm_sizing_policy_ids}
        :param vm_vgpu_policy_ids: Set of VM vGPU Policy IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_vgpu_policy_ids OrgVdc#vm_vgpu_policy_ids}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c35e61e4f0e28e6364694bfea726476c4b575eed184e7b8c72e84398879565c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrgVdcConfig(
            allocation_model=allocation_model,
            compute_capacity=compute_capacity,
            name=name,
            provider_vdc_name=provider_vdc_name,
            storage_profile=storage_profile,
            allow_over_commit=allow_over_commit,
            cpu_guaranteed=cpu_guaranteed,
            cpu_speed=cpu_speed,
            default_compute_policy_id=default_compute_policy_id,
            default_vm_sizing_policy_id=default_vm_sizing_policy_id,
            delete_force=delete_force,
            delete_recursive=delete_recursive,
            description=description,
            edge_cluster_id=edge_cluster_id,
            elasticity=elasticity,
            enabled=enabled,
            enable_fast_provisioning=enable_fast_provisioning,
            enable_nsxv_distributed_firewall=enable_nsxv_distributed_firewall,
            enable_thin_provisioning=enable_thin_provisioning,
            enable_vm_discovery=enable_vm_discovery,
            id=id,
            include_vm_memory_overhead=include_vm_memory_overhead,
            memory_guaranteed=memory_guaranteed,
            metadata=metadata,
            metadata_entry=metadata_entry,
            network_pool_name=network_pool_name,
            network_quota=network_quota,
            nic_quota=nic_quota,
            org=org,
            vm_placement_policy_ids=vm_placement_policy_ids,
            vm_quota=vm_quota,
            vm_sizing_policy_ids=vm_sizing_policy_ids,
            vm_vgpu_policy_ids=vm_vgpu_policy_ids,
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
        '''Generates CDKTF code for importing a OrgVdc resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrgVdc to import.
        :param import_from_id: The id of the existing OrgVdc that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrgVdc to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c310db164f12b2d35ae0268f99ef042b9063cb6bae162b08c31fc1e94b6fd0b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putComputeCapacity")
    def put_compute_capacity(
        self,
        *,
        cpu: typing.Union["OrgVdcComputeCapacityCpu", typing.Dict[builtins.str, typing.Any]],
        memory: typing.Union["OrgVdcComputeCapacityMemory", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cpu: cpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu OrgVdc#cpu}
        :param memory: memory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#memory OrgVdc#memory}
        '''
        value = OrgVdcComputeCapacity(cpu=cpu, memory=memory)

        return typing.cast(None, jsii.invoke(self, "putComputeCapacity", [value]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcMetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6875a284aaae890fca1805ad800469e356b27d297510e301ef40d8e98db4944b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="putStorageProfile")
    def put_storage_profile(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcStorageProfile", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f25b96499a0849580fbdb1bed13fa885493854fa204e67cc6905b0c763d6293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageProfile", [value]))

    @jsii.member(jsii_name="resetAllowOverCommit")
    def reset_allow_over_commit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowOverCommit", []))

    @jsii.member(jsii_name="resetCpuGuaranteed")
    def reset_cpu_guaranteed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuGuaranteed", []))

    @jsii.member(jsii_name="resetCpuSpeed")
    def reset_cpu_speed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuSpeed", []))

    @jsii.member(jsii_name="resetDefaultComputePolicyId")
    def reset_default_compute_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultComputePolicyId", []))

    @jsii.member(jsii_name="resetDefaultVmSizingPolicyId")
    def reset_default_vm_sizing_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultVmSizingPolicyId", []))

    @jsii.member(jsii_name="resetDeleteForce")
    def reset_delete_force(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteForce", []))

    @jsii.member(jsii_name="resetDeleteRecursive")
    def reset_delete_recursive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRecursive", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEdgeClusterId")
    def reset_edge_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeClusterId", []))

    @jsii.member(jsii_name="resetElasticity")
    def reset_elasticity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticity", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnableFastProvisioning")
    def reset_enable_fast_provisioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableFastProvisioning", []))

    @jsii.member(jsii_name="resetEnableNsxvDistributedFirewall")
    def reset_enable_nsxv_distributed_firewall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNsxvDistributedFirewall", []))

    @jsii.member(jsii_name="resetEnableThinProvisioning")
    def reset_enable_thin_provisioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableThinProvisioning", []))

    @jsii.member(jsii_name="resetEnableVmDiscovery")
    def reset_enable_vm_discovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableVmDiscovery", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeVmMemoryOverhead")
    def reset_include_vm_memory_overhead(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeVmMemoryOverhead", []))

    @jsii.member(jsii_name="resetMemoryGuaranteed")
    def reset_memory_guaranteed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryGuaranteed", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataEntry")
    def reset_metadata_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataEntry", []))

    @jsii.member(jsii_name="resetNetworkPoolName")
    def reset_network_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPoolName", []))

    @jsii.member(jsii_name="resetNetworkQuota")
    def reset_network_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkQuota", []))

    @jsii.member(jsii_name="resetNicQuota")
    def reset_nic_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNicQuota", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetVmPlacementPolicyIds")
    def reset_vm_placement_policy_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmPlacementPolicyIds", []))

    @jsii.member(jsii_name="resetVmQuota")
    def reset_vm_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmQuota", []))

    @jsii.member(jsii_name="resetVmSizingPolicyIds")
    def reset_vm_sizing_policy_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSizingPolicyIds", []))

    @jsii.member(jsii_name="resetVmVgpuPolicyIds")
    def reset_vm_vgpu_policy_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmVgpuPolicyIds", []))

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
    @jsii.member(jsii_name="computeCapacity")
    def compute_capacity(self) -> "OrgVdcComputeCapacityOutputReference":
        return typing.cast("OrgVdcComputeCapacityOutputReference", jsii.get(self, "computeCapacity"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "OrgVdcMetadataEntryList":
        return typing.cast("OrgVdcMetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> "OrgVdcStorageProfileList":
        return typing.cast("OrgVdcStorageProfileList", jsii.get(self, "storageProfile"))

    @builtins.property
    @jsii.member(jsii_name="allocationModelInput")
    def allocation_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocationModelInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOverCommitInput")
    def allow_over_commit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowOverCommitInput"))

    @builtins.property
    @jsii.member(jsii_name="computeCapacityInput")
    def compute_capacity_input(self) -> typing.Optional["OrgVdcComputeCapacity"]:
        return typing.cast(typing.Optional["OrgVdcComputeCapacity"], jsii.get(self, "computeCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuGuaranteedInput")
    def cpu_guaranteed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuGuaranteedInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSpeedInput")
    def cpu_speed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuSpeedInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultComputePolicyIdInput")
    def default_compute_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultComputePolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultVmSizingPolicyIdInput")
    def default_vm_sizing_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultVmSizingPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteForceInput")
    def delete_force_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteForceInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRecursiveInput")
    def delete_recursive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteRecursiveInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeClusterIdInput")
    def edge_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticityInput")
    def elasticity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "elasticityInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableFastProvisioningInput")
    def enable_fast_provisioning_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableFastProvisioningInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNsxvDistributedFirewallInput")
    def enable_nsxv_distributed_firewall_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNsxvDistributedFirewallInput"))

    @builtins.property
    @jsii.member(jsii_name="enableThinProvisioningInput")
    def enable_thin_provisioning_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableThinProvisioningInput"))

    @builtins.property
    @jsii.member(jsii_name="enableVmDiscoveryInput")
    def enable_vm_discovery_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableVmDiscoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeVmMemoryOverheadInput")
    def include_vm_memory_overhead_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeVmMemoryOverheadInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGuaranteedInput")
    def memory_guaranteed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryGuaranteedInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntryInput")
    def metadata_entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcMetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcMetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPoolNameInput")
    def network_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkQuotaInput")
    def network_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "networkQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="nicQuotaInput")
    def nic_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nicQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="providerVdcNameInput")
    def provider_vdc_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerVdcNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileInput")
    def storage_profile_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcStorageProfile"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcStorageProfile"]]], jsii.get(self, "storageProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="vmPlacementPolicyIdsInput")
    def vm_placement_policy_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vmPlacementPolicyIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmQuotaInput")
    def vm_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizingPolicyIdsInput")
    def vm_sizing_policy_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vmSizingPolicyIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmVgpuPolicyIdsInput")
    def vm_vgpu_policy_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vmVgpuPolicyIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="allocationModel")
    def allocation_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocationModel"))

    @allocation_model.setter
    def allocation_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149121f19a57508741d190edb32119e0822b1ff055b213f97a1331e091964623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocationModel", value)

    @builtins.property
    @jsii.member(jsii_name="allowOverCommit")
    def allow_over_commit(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowOverCommit"))

    @allow_over_commit.setter
    def allow_over_commit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa194b018f2b1266a89e943c4b0399c96566e46c1623d1016b10a53b2dbdc405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOverCommit", value)

    @builtins.property
    @jsii.member(jsii_name="cpuGuaranteed")
    def cpu_guaranteed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuGuaranteed"))

    @cpu_guaranteed.setter
    def cpu_guaranteed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ccd9fa7f89ae6120f5ecd1a5cb94a3e5b54f6d4a1bc75694bdabe13669959d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuGuaranteed", value)

    @builtins.property
    @jsii.member(jsii_name="cpuSpeed")
    def cpu_speed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuSpeed"))

    @cpu_speed.setter
    def cpu_speed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d2113ee0bd27bbb2790c183e2b64c4b24d9b8849852bbb459f09068b850f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuSpeed", value)

    @builtins.property
    @jsii.member(jsii_name="defaultComputePolicyId")
    def default_compute_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultComputePolicyId"))

    @default_compute_policy_id.setter
    def default_compute_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a5e7ed405c64a519a13a6ced1ac57ed73072933b87ac6033e617f4fef6c186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultComputePolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="defaultVmSizingPolicyId")
    def default_vm_sizing_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultVmSizingPolicyId"))

    @default_vm_sizing_policy_id.setter
    def default_vm_sizing_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466ed11bcea7f40a5ebb21c96bd28e281511e10f4df3c0d0d5b0b38b30c279ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultVmSizingPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="deleteForce")
    def delete_force(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteForce"))

    @delete_force.setter
    def delete_force(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6848f0796681257fec77c329ef4ca5b21b4ae1409570ea625077815d76dcd39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteForce", value)

    @builtins.property
    @jsii.member(jsii_name="deleteRecursive")
    def delete_recursive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteRecursive"))

    @delete_recursive.setter
    def delete_recursive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696c2df69ac7f470241e9988161920bfb857d04ae17d6f2bd93423bc840f70ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRecursive", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6c4ed56913858cf786cb5333b90e63695bf96b1081969a1a823f058d5827f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edgeClusterId")
    def edge_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeClusterId"))

    @edge_cluster_id.setter
    def edge_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa8a8652313bfb3d86da3cc7d110fdc07557a46d729f2671719929b81b128a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="elasticity")
    def elasticity(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "elasticity"))

    @elasticity.setter
    def elasticity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d790308ba418c6347dd4b851daa998cf77befd93abe03e48939a9eef116721a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticity", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4894ac21ce55aec4abddc160548ee8682cada9560d8ee14dd6a39bfddc28be99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="enableFastProvisioning")
    def enable_fast_provisioning(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableFastProvisioning"))

    @enable_fast_provisioning.setter
    def enable_fast_provisioning(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf6ec12f2f2b7033d964b4405019d744aab689511af0342d543d488c7074611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFastProvisioning", value)

    @builtins.property
    @jsii.member(jsii_name="enableNsxvDistributedFirewall")
    def enable_nsxv_distributed_firewall(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNsxvDistributedFirewall"))

    @enable_nsxv_distributed_firewall.setter
    def enable_nsxv_distributed_firewall(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d4a592bc0d930bcf84306ab904b9b9d8b5ad704f23876320ee9181df2f8622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNsxvDistributedFirewall", value)

    @builtins.property
    @jsii.member(jsii_name="enableThinProvisioning")
    def enable_thin_provisioning(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableThinProvisioning"))

    @enable_thin_provisioning.setter
    def enable_thin_provisioning(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90624658e8e62f3b3cd7567d159d6b019c94d2ac87d3763d2c4c1b6460fc228d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableThinProvisioning", value)

    @builtins.property
    @jsii.member(jsii_name="enableVmDiscovery")
    def enable_vm_discovery(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableVmDiscovery"))

    @enable_vm_discovery.setter
    def enable_vm_discovery(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff802fdb34a23817fb8d1181b6b86100d715923d1bb58677e2f87c28455a10a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVmDiscovery", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee2a87da4a8245f771821dbe6f104606dd41d5f8a451cb7ebb7d9a1d2291375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="includeVmMemoryOverhead")
    def include_vm_memory_overhead(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeVmMemoryOverhead"))

    @include_vm_memory_overhead.setter
    def include_vm_memory_overhead(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9853c67986448f800576f7d7798fa87e97b30f2003da2403d7a28ae820448ba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeVmMemoryOverhead", value)

    @builtins.property
    @jsii.member(jsii_name="memoryGuaranteed")
    def memory_guaranteed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGuaranteed"))

    @memory_guaranteed.setter
    def memory_guaranteed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f6fa73e7827c4635104559fc9cbdb820cc8513a7ce22e99957af7b9b9ba4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGuaranteed", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8af76f77d88ccbf028287dc75ca15ecfdc0359b52578e789177bbc9de0b493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed9fcc6851d05db8bfcb8b807d8c098fc38c4007a18597a92f9f2eb72829557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkPoolName")
    def network_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPoolName"))

    @network_pool_name.setter
    def network_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5811e34b35bc1b93b8202ef73e38029bb19fc91d0f39709e1fa425b344456935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPoolName", value)

    @builtins.property
    @jsii.member(jsii_name="networkQuota")
    def network_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "networkQuota"))

    @network_quota.setter
    def network_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6faa4a0f9b8d5ed947c58350e5e821f0ca1d0c58ed75ec78d618ff45badc8717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkQuota", value)

    @builtins.property
    @jsii.member(jsii_name="nicQuota")
    def nic_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nicQuota"))

    @nic_quota.setter
    def nic_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2048e6c541cedabc6ce6f3bc2e7387088793638d422f3ab97004a00bfc40e0a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicQuota", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab57527fbf546cf8d9211c57bd5f66869d91cf3bd2d5b8179dff2a0b5a19ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="providerVdcName")
    def provider_vdc_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerVdcName"))

    @provider_vdc_name.setter
    def provider_vdc_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771534735b5eed8f7aace67319effd17856411554a42eeb31e0aa08aba1b692c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerVdcName", value)

    @builtins.property
    @jsii.member(jsii_name="vmPlacementPolicyIds")
    def vm_placement_policy_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vmPlacementPolicyIds"))

    @vm_placement_policy_ids.setter
    def vm_placement_policy_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef034795490846f113a5b6b467200f56c974d28538a47991992b3349c4b01ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmPlacementPolicyIds", value)

    @builtins.property
    @jsii.member(jsii_name="vmQuota")
    def vm_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmQuota"))

    @vm_quota.setter
    def vm_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a474260d8980de604365afd1671fba240ba190cc08991b5309779178d0b8542b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmQuota", value)

    @builtins.property
    @jsii.member(jsii_name="vmSizingPolicyIds")
    def vm_sizing_policy_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vmSizingPolicyIds"))

    @vm_sizing_policy_ids.setter
    def vm_sizing_policy_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff65603138ce466e3b7aa0b143d22c422660ac0914557f25c5f74eb7f5adb8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSizingPolicyIds", value)

    @builtins.property
    @jsii.member(jsii_name="vmVgpuPolicyIds")
    def vm_vgpu_policy_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vmVgpuPolicyIds"))

    @vm_vgpu_policy_ids.setter
    def vm_vgpu_policy_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09dc170fc06e0700bd02517ad4cbf3c5748e360be7a1646d58e75ac21127c8a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmVgpuPolicyIds", value)


@jsii.data_type(
    jsii_type="vcd.orgVdc.OrgVdcComputeCapacity",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class OrgVdcComputeCapacity:
    def __init__(
        self,
        *,
        cpu: typing.Union["OrgVdcComputeCapacityCpu", typing.Dict[builtins.str, typing.Any]],
        memory: typing.Union["OrgVdcComputeCapacityMemory", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cpu: cpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu OrgVdc#cpu}
        :param memory: memory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#memory OrgVdc#memory}
        '''
        if isinstance(cpu, dict):
            cpu = OrgVdcComputeCapacityCpu(**cpu)
        if isinstance(memory, dict):
            memory = OrgVdcComputeCapacityMemory(**memory)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1118a1c401c3d3c9b3b3c70e5bc6fa2312112b4a957af350457c488b8628c95e)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "memory": memory,
        }

    @builtins.property
    def cpu(self) -> "OrgVdcComputeCapacityCpu":
        '''cpu block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu OrgVdc#cpu}
        '''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast("OrgVdcComputeCapacityCpu", result)

    @builtins.property
    def memory(self) -> "OrgVdcComputeCapacityMemory":
        '''memory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#memory OrgVdc#memory}
        '''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast("OrgVdcComputeCapacityMemory", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcComputeCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.orgVdc.OrgVdcComputeCapacityCpu",
    jsii_struct_bases=[],
    name_mapping={"allocated": "allocated", "limit": "limit"},
)
class OrgVdcComputeCapacityCpu:
    def __init__(
        self,
        *,
        allocated: typing.Optional[jsii.Number] = None,
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allocated: Capacity that is committed to be available. Value in MB or MHz. Used with AllocationPool (Allocation pool) and ReservationPool (Reservation pool). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocated OrgVdc#allocated}
        :param limit: Capacity limit relative to the value specified for Allocation. It must not be less than that value. If it is greater than that value, it implies over provisioning. A value of 0 specifies unlimited units. Value in MB or MHz. Used with AllocationVApp (Pay as you go). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#limit OrgVdc#limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb1b5d4bd04c9370fcd7ced1fbbbdb1bc3d603ff3c0b178810568a0b3f4a365)
            check_type(argname="argument allocated", value=allocated, expected_type=type_hints["allocated"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated is not None:
            self._values["allocated"] = allocated
        if limit is not None:
            self._values["limit"] = limit

    @builtins.property
    def allocated(self) -> typing.Optional[jsii.Number]:
        '''Capacity that is committed to be available.

        Value in MB or MHz. Used with AllocationPool (Allocation pool) and ReservationPool (Reservation pool).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocated OrgVdc#allocated}
        '''
        result = self._values.get("allocated")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''Capacity limit relative to the value specified for Allocation.

        It must not be less than that value. If it is greater than that value, it implies over provisioning. A value of 0 specifies unlimited units. Value in MB or MHz. Used with AllocationVApp (Pay as you go).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#limit OrgVdc#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcComputeCapacityCpu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcComputeCapacityCpuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdc.OrgVdcComputeCapacityCpuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3141df366328664c9d4800d2c05b639ad8c196ebe9fae41ba3a3fcc43308b14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllocated")
    def reset_allocated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocated", []))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @builtins.property
    @jsii.member(jsii_name="reserved")
    def reserved(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reserved"))

    @builtins.property
    @jsii.member(jsii_name="used")
    def used(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "used"))

    @builtins.property
    @jsii.member(jsii_name="allocatedInput")
    def allocated_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocatedInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="allocated")
    def allocated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocated"))

    @allocated.setter
    def allocated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92daa6c984398533f685e797c69a19c58b8f179ec7c67166c633cadf20e719d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocated", value)

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b23045a5bc7742b195042a48f89c2e6f77b7c16651407d1a8bac16c2703375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgVdcComputeCapacityCpu]:
        return typing.cast(typing.Optional[OrgVdcComputeCapacityCpu], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgVdcComputeCapacityCpu]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426e07869031d9be5459259f8c3e8f8970cfbb1ef61ca4f14f7d40456eae3ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgVdc.OrgVdcComputeCapacityMemory",
    jsii_struct_bases=[],
    name_mapping={"allocated": "allocated", "limit": "limit"},
)
class OrgVdcComputeCapacityMemory:
    def __init__(
        self,
        *,
        allocated: typing.Optional[jsii.Number] = None,
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allocated: Capacity that is committed to be available. Value in MB or MHz. Used with AllocationPool (Allocation pool) and ReservationPool (Reservation pool). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocated OrgVdc#allocated}
        :param limit: Capacity limit relative to the value specified for Allocation. It must not be less than that value. If it is greater than that value, it implies over provisioning. A value of 0 specifies unlimited units. Value in MB or MHz. Used with AllocationVApp (Pay as you go). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#limit OrgVdc#limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f20d50a59dd827ac355639e649263996bacbf7f0b2f7f8db730b2a6acaad2c8)
            check_type(argname="argument allocated", value=allocated, expected_type=type_hints["allocated"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated is not None:
            self._values["allocated"] = allocated
        if limit is not None:
            self._values["limit"] = limit

    @builtins.property
    def allocated(self) -> typing.Optional[jsii.Number]:
        '''Capacity that is committed to be available.

        Value in MB or MHz. Used with AllocationPool (Allocation pool) and ReservationPool (Reservation pool).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocated OrgVdc#allocated}
        '''
        result = self._values.get("allocated")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''Capacity limit relative to the value specified for Allocation.

        It must not be less than that value. If it is greater than that value, it implies over provisioning. A value of 0 specifies unlimited units. Value in MB or MHz. Used with AllocationVApp (Pay as you go).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#limit OrgVdc#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcComputeCapacityMemory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcComputeCapacityMemoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdc.OrgVdcComputeCapacityMemoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ef27acf75114d3e2738adad346a0e131a7ee1fe9d411e408fae967dceb261d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllocated")
    def reset_allocated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocated", []))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @builtins.property
    @jsii.member(jsii_name="reserved")
    def reserved(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reserved"))

    @builtins.property
    @jsii.member(jsii_name="used")
    def used(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "used"))

    @builtins.property
    @jsii.member(jsii_name="allocatedInput")
    def allocated_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocatedInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="allocated")
    def allocated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocated"))

    @allocated.setter
    def allocated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c54deb69822d41a80f3ff4fa9c7e38b08faf8267e3ea92c6df0a656505ddb98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocated", value)

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1adcab172895deb53b7a4b9141aec095d29476a9777bed1df4cc216ad819ce2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgVdcComputeCapacityMemory]:
        return typing.cast(typing.Optional[OrgVdcComputeCapacityMemory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgVdcComputeCapacityMemory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d29440dc1e934b4241f209bc5ae9dad600906a6bf40186575ce326349beca8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrgVdcComputeCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdc.OrgVdcComputeCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be1631843f22d803acbf2c79e7de1b94154e60769d1fb8b1fdae5b1a2d6b9ae5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCpu")
    def put_cpu(
        self,
        *,
        allocated: typing.Optional[jsii.Number] = None,
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allocated: Capacity that is committed to be available. Value in MB or MHz. Used with AllocationPool (Allocation pool) and ReservationPool (Reservation pool). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocated OrgVdc#allocated}
        :param limit: Capacity limit relative to the value specified for Allocation. It must not be less than that value. If it is greater than that value, it implies over provisioning. A value of 0 specifies unlimited units. Value in MB or MHz. Used with AllocationVApp (Pay as you go). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#limit OrgVdc#limit}
        '''
        value = OrgVdcComputeCapacityCpu(allocated=allocated, limit=limit)

        return typing.cast(None, jsii.invoke(self, "putCpu", [value]))

    @jsii.member(jsii_name="putMemory")
    def put_memory(
        self,
        *,
        allocated: typing.Optional[jsii.Number] = None,
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allocated: Capacity that is committed to be available. Value in MB or MHz. Used with AllocationPool (Allocation pool) and ReservationPool (Reservation pool). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocated OrgVdc#allocated}
        :param limit: Capacity limit relative to the value specified for Allocation. It must not be less than that value. If it is greater than that value, it implies over provisioning. A value of 0 specifies unlimited units. Value in MB or MHz. Used with AllocationVApp (Pay as you go). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#limit OrgVdc#limit}
        '''
        value = OrgVdcComputeCapacityMemory(allocated=allocated, limit=limit)

        return typing.cast(None, jsii.invoke(self, "putMemory", [value]))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> OrgVdcComputeCapacityCpuOutputReference:
        return typing.cast(OrgVdcComputeCapacityCpuOutputReference, jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> OrgVdcComputeCapacityMemoryOutputReference:
        return typing.cast(OrgVdcComputeCapacityMemoryOutputReference, jsii.get(self, "memory"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[OrgVdcComputeCapacityCpu]:
        return typing.cast(typing.Optional[OrgVdcComputeCapacityCpu], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[OrgVdcComputeCapacityMemory]:
        return typing.cast(typing.Optional[OrgVdcComputeCapacityMemory], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgVdcComputeCapacity]:
        return typing.cast(typing.Optional[OrgVdcComputeCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgVdcComputeCapacity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5839e41b51f6c3b8505ef2854b496c64efbc4733f6dac8382c6b8636166272c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgVdc.OrgVdcConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "allocation_model": "allocationModel",
        "compute_capacity": "computeCapacity",
        "name": "name",
        "provider_vdc_name": "providerVdcName",
        "storage_profile": "storageProfile",
        "allow_over_commit": "allowOverCommit",
        "cpu_guaranteed": "cpuGuaranteed",
        "cpu_speed": "cpuSpeed",
        "default_compute_policy_id": "defaultComputePolicyId",
        "default_vm_sizing_policy_id": "defaultVmSizingPolicyId",
        "delete_force": "deleteForce",
        "delete_recursive": "deleteRecursive",
        "description": "description",
        "edge_cluster_id": "edgeClusterId",
        "elasticity": "elasticity",
        "enabled": "enabled",
        "enable_fast_provisioning": "enableFastProvisioning",
        "enable_nsxv_distributed_firewall": "enableNsxvDistributedFirewall",
        "enable_thin_provisioning": "enableThinProvisioning",
        "enable_vm_discovery": "enableVmDiscovery",
        "id": "id",
        "include_vm_memory_overhead": "includeVmMemoryOverhead",
        "memory_guaranteed": "memoryGuaranteed",
        "metadata": "metadata",
        "metadata_entry": "metadataEntry",
        "network_pool_name": "networkPoolName",
        "network_quota": "networkQuota",
        "nic_quota": "nicQuota",
        "org": "org",
        "vm_placement_policy_ids": "vmPlacementPolicyIds",
        "vm_quota": "vmQuota",
        "vm_sizing_policy_ids": "vmSizingPolicyIds",
        "vm_vgpu_policy_ids": "vmVgpuPolicyIds",
    },
)
class OrgVdcConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allocation_model: builtins.str,
        compute_capacity: typing.Union[OrgVdcComputeCapacity, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        provider_vdc_name: builtins.str,
        storage_profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcStorageProfile", typing.Dict[builtins.str, typing.Any]]]],
        allow_over_commit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_guaranteed: typing.Optional[jsii.Number] = None,
        cpu_speed: typing.Optional[jsii.Number] = None,
        default_compute_policy_id: typing.Optional[builtins.str] = None,
        default_vm_sizing_policy_id: typing.Optional[builtins.str] = None,
        delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_cluster_id: typing.Optional[builtins.str] = None,
        elasticity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_fast_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_nsxv_distributed_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_thin_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vm_discovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        include_vm_memory_overhead: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_guaranteed: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_pool_name: typing.Optional[builtins.str] = None,
        network_quota: typing.Optional[jsii.Number] = None,
        nic_quota: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        vm_placement_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_quota: typing.Optional[jsii.Number] = None,
        vm_sizing_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_vgpu_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param allocation_model: The allocation model used by this VDC; must be one of {AllocationVApp, AllocationPool, ReservationPool, Flex}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocation_model OrgVdc#allocation_model}
        :param compute_capacity: compute_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#compute_capacity OrgVdc#compute_capacity}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#name OrgVdc#name}.
        :param provider_vdc_name: A reference to the Provider VDC from which this organization VDC is provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#provider_vdc_name OrgVdc#provider_vdc_name}
        :param storage_profile: storage_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#storage_profile OrgVdc#storage_profile}
        :param allow_over_commit: Set to false to disallow creation of the VDC if the AllocationModel is AllocationPool or ReservationPool and the ComputeCapacity you specified is greater than what the backing Provider VDC can supply. Default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allow_over_commit OrgVdc#allow_over_commit}
        :param cpu_guaranteed: Percentage of allocated CPU resources guaranteed to vApps deployed in this VDC. For example, if this value is 0.75, then 75% of allocated resources are guaranteed. Required when AllocationModel is AllocationVApp or AllocationPool. If the element is empty, vCD sets a value Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu_guaranteed OrgVdc#cpu_guaranteed}
        :param cpu_speed: Specifies the clock frequency, in Megahertz, for any virtual CPU that is allocated to a VM. A VM with 2 vCPUs will consume twice as much of this value. Ignored for ReservationPool. Required when AllocationModel is AllocationVApp or AllocationPool, and may not be less than 256 MHz. Defaults to 1000 MHz if the element is empty or missing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu_speed OrgVdc#cpu_speed}
        :param default_compute_policy_id: ID of default Compute policy for this VDC, which can be a VM Sizing Policy, VM Placement Policy or vGPU Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#default_compute_policy_id OrgVdc#default_compute_policy_id}
        :param default_vm_sizing_policy_id: ID of default VM Compute policy, which can be a VM Sizing Policy, VM Placement Policy or vGPU Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#default_vm_sizing_policy_id OrgVdc#default_vm_sizing_policy_id}
        :param delete_force: When destroying use delete_force=True to remove a VDC and any objects it contains, regardless of their state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#delete_force OrgVdc#delete_force}
        :param delete_recursive: When destroying use delete_recursive=True to remove the VDC and any objects it contains that are in a state that normally allows removal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#delete_recursive OrgVdc#delete_recursive}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#description OrgVdc#description}.
        :param edge_cluster_id: ID of NSX-T Edge Cluster (provider vApp networking services and DHCP capability for Isolated networks). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#edge_cluster_id OrgVdc#edge_cluster_id}
        :param elasticity: Set to true to indicate if the Flex VDC is to be elastic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#elasticity OrgVdc#elasticity}
        :param enabled: True if this VDC is enabled for use by the organization VDCs. Default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enabled OrgVdc#enabled}
        :param enable_fast_provisioning: Request for fast provisioning. Request will be honored only if the underlying datas tore supports it. Fast provisioning can reduce the time it takes to create virtual machines by using vSphere linked clones. If you disable fast provisioning, all provisioning operations will result in full clones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_fast_provisioning OrgVdc#enable_fast_provisioning}
        :param enable_nsxv_distributed_firewall: Set to true to enable distributed firewall - Only applies to NSX-V VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_nsxv_distributed_firewall OrgVdc#enable_nsxv_distributed_firewall}
        :param enable_thin_provisioning: Boolean to request thin provisioning. Request will be honored only if the underlying datastore supports it. Thin provisioning saves storage space by committing it on demand. This allows over-allocation of storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_thin_provisioning OrgVdc#enable_thin_provisioning}
        :param enable_vm_discovery: True if discovery of vCenter VMs is enabled for resource pools backing this VDC. If left unspecified, the actual behaviour depends on enablement at the organization level and at the system level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_vm_discovery OrgVdc#enable_vm_discovery}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#id OrgVdc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_vm_memory_overhead: Set to true to indicate if the Flex VDC is to include memory overhead into its accounting for admission control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#include_vm_memory_overhead OrgVdc#include_vm_memory_overhead}
        :param memory_guaranteed: Percentage of allocated memory resources guaranteed to vApps deployed in this VDC. For example, if this value is 0.75, then 75% of allocated resources are guaranteed. Required when AllocationModel is AllocationVApp or AllocationPool. When Allocation model is AllocationPool minimum value is 0.2. If the element is empty, vCD sets a value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#memory_guaranteed OrgVdc#memory_guaranteed}
        :param metadata: Key and value pairs for Org VDC metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#metadata OrgVdc#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#metadata_entry OrgVdc#metadata_entry}
        :param network_pool_name: The name of a network pool in the Provider VDC. Required if this VDC will contain routed or isolated networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#network_pool_name OrgVdc#network_pool_name}
        :param network_quota: Maximum number of network objects that can be deployed in this VDC. Defaults to 0, which means no networks can be deployed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#network_quota OrgVdc#network_quota}
        :param nic_quota: Maximum number of virtual NICs allowed in this VDC. Defaults to 0, which specifies an unlimited number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#nic_quota OrgVdc#nic_quota}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#org OrgVdc#org}
        :param vm_placement_policy_ids: Set of VM Placement Policy IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_placement_policy_ids OrgVdc#vm_placement_policy_ids}
        :param vm_quota: The maximum number of VMs that can be created in this VDC. Includes deployed and undeployed VMs in vApps and vApp templates. Defaults to 0, which specifies an unlimited number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_quota OrgVdc#vm_quota}
        :param vm_sizing_policy_ids: Set of VM Sizing Policy IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_sizing_policy_ids OrgVdc#vm_sizing_policy_ids}
        :param vm_vgpu_policy_ids: Set of VM vGPU Policy IDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_vgpu_policy_ids OrgVdc#vm_vgpu_policy_ids}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(compute_capacity, dict):
            compute_capacity = OrgVdcComputeCapacity(**compute_capacity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a99ba475e9412bf13760b38208401291c7102abc341f2cd0375d0e8967c89d7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument allocation_model", value=allocation_model, expected_type=type_hints["allocation_model"])
            check_type(argname="argument compute_capacity", value=compute_capacity, expected_type=type_hints["compute_capacity"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider_vdc_name", value=provider_vdc_name, expected_type=type_hints["provider_vdc_name"])
            check_type(argname="argument storage_profile", value=storage_profile, expected_type=type_hints["storage_profile"])
            check_type(argname="argument allow_over_commit", value=allow_over_commit, expected_type=type_hints["allow_over_commit"])
            check_type(argname="argument cpu_guaranteed", value=cpu_guaranteed, expected_type=type_hints["cpu_guaranteed"])
            check_type(argname="argument cpu_speed", value=cpu_speed, expected_type=type_hints["cpu_speed"])
            check_type(argname="argument default_compute_policy_id", value=default_compute_policy_id, expected_type=type_hints["default_compute_policy_id"])
            check_type(argname="argument default_vm_sizing_policy_id", value=default_vm_sizing_policy_id, expected_type=type_hints["default_vm_sizing_policy_id"])
            check_type(argname="argument delete_force", value=delete_force, expected_type=type_hints["delete_force"])
            check_type(argname="argument delete_recursive", value=delete_recursive, expected_type=type_hints["delete_recursive"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_cluster_id", value=edge_cluster_id, expected_type=type_hints["edge_cluster_id"])
            check_type(argname="argument elasticity", value=elasticity, expected_type=type_hints["elasticity"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_fast_provisioning", value=enable_fast_provisioning, expected_type=type_hints["enable_fast_provisioning"])
            check_type(argname="argument enable_nsxv_distributed_firewall", value=enable_nsxv_distributed_firewall, expected_type=type_hints["enable_nsxv_distributed_firewall"])
            check_type(argname="argument enable_thin_provisioning", value=enable_thin_provisioning, expected_type=type_hints["enable_thin_provisioning"])
            check_type(argname="argument enable_vm_discovery", value=enable_vm_discovery, expected_type=type_hints["enable_vm_discovery"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_vm_memory_overhead", value=include_vm_memory_overhead, expected_type=type_hints["include_vm_memory_overhead"])
            check_type(argname="argument memory_guaranteed", value=memory_guaranteed, expected_type=type_hints["memory_guaranteed"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_entry", value=metadata_entry, expected_type=type_hints["metadata_entry"])
            check_type(argname="argument network_pool_name", value=network_pool_name, expected_type=type_hints["network_pool_name"])
            check_type(argname="argument network_quota", value=network_quota, expected_type=type_hints["network_quota"])
            check_type(argname="argument nic_quota", value=nic_quota, expected_type=type_hints["nic_quota"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument vm_placement_policy_ids", value=vm_placement_policy_ids, expected_type=type_hints["vm_placement_policy_ids"])
            check_type(argname="argument vm_quota", value=vm_quota, expected_type=type_hints["vm_quota"])
            check_type(argname="argument vm_sizing_policy_ids", value=vm_sizing_policy_ids, expected_type=type_hints["vm_sizing_policy_ids"])
            check_type(argname="argument vm_vgpu_policy_ids", value=vm_vgpu_policy_ids, expected_type=type_hints["vm_vgpu_policy_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocation_model": allocation_model,
            "compute_capacity": compute_capacity,
            "name": name,
            "provider_vdc_name": provider_vdc_name,
            "storage_profile": storage_profile,
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
        if allow_over_commit is not None:
            self._values["allow_over_commit"] = allow_over_commit
        if cpu_guaranteed is not None:
            self._values["cpu_guaranteed"] = cpu_guaranteed
        if cpu_speed is not None:
            self._values["cpu_speed"] = cpu_speed
        if default_compute_policy_id is not None:
            self._values["default_compute_policy_id"] = default_compute_policy_id
        if default_vm_sizing_policy_id is not None:
            self._values["default_vm_sizing_policy_id"] = default_vm_sizing_policy_id
        if delete_force is not None:
            self._values["delete_force"] = delete_force
        if delete_recursive is not None:
            self._values["delete_recursive"] = delete_recursive
        if description is not None:
            self._values["description"] = description
        if edge_cluster_id is not None:
            self._values["edge_cluster_id"] = edge_cluster_id
        if elasticity is not None:
            self._values["elasticity"] = elasticity
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_fast_provisioning is not None:
            self._values["enable_fast_provisioning"] = enable_fast_provisioning
        if enable_nsxv_distributed_firewall is not None:
            self._values["enable_nsxv_distributed_firewall"] = enable_nsxv_distributed_firewall
        if enable_thin_provisioning is not None:
            self._values["enable_thin_provisioning"] = enable_thin_provisioning
        if enable_vm_discovery is not None:
            self._values["enable_vm_discovery"] = enable_vm_discovery
        if id is not None:
            self._values["id"] = id
        if include_vm_memory_overhead is not None:
            self._values["include_vm_memory_overhead"] = include_vm_memory_overhead
        if memory_guaranteed is not None:
            self._values["memory_guaranteed"] = memory_guaranteed
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_entry is not None:
            self._values["metadata_entry"] = metadata_entry
        if network_pool_name is not None:
            self._values["network_pool_name"] = network_pool_name
        if network_quota is not None:
            self._values["network_quota"] = network_quota
        if nic_quota is not None:
            self._values["nic_quota"] = nic_quota
        if org is not None:
            self._values["org"] = org
        if vm_placement_policy_ids is not None:
            self._values["vm_placement_policy_ids"] = vm_placement_policy_ids
        if vm_quota is not None:
            self._values["vm_quota"] = vm_quota
        if vm_sizing_policy_ids is not None:
            self._values["vm_sizing_policy_ids"] = vm_sizing_policy_ids
        if vm_vgpu_policy_ids is not None:
            self._values["vm_vgpu_policy_ids"] = vm_vgpu_policy_ids

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
    def allocation_model(self) -> builtins.str:
        '''The allocation model used by this VDC; must be one of {AllocationVApp, AllocationPool, ReservationPool, Flex}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allocation_model OrgVdc#allocation_model}
        '''
        result = self._values.get("allocation_model")
        assert result is not None, "Required property 'allocation_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_capacity(self) -> OrgVdcComputeCapacity:
        '''compute_capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#compute_capacity OrgVdc#compute_capacity}
        '''
        result = self._values.get("compute_capacity")
        assert result is not None, "Required property 'compute_capacity' is missing"
        return typing.cast(OrgVdcComputeCapacity, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#name OrgVdc#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_vdc_name(self) -> builtins.str:
        '''A reference to the Provider VDC from which this organization VDC is provisioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#provider_vdc_name OrgVdc#provider_vdc_name}
        '''
        result = self._values.get("provider_vdc_name")
        assert result is not None, "Required property 'provider_vdc_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_profile(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcStorageProfile"]]:
        '''storage_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#storage_profile OrgVdc#storage_profile}
        '''
        result = self._values.get("storage_profile")
        assert result is not None, "Required property 'storage_profile' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcStorageProfile"]], result)

    @builtins.property
    def allow_over_commit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to false to disallow creation of the VDC if the AllocationModel is AllocationPool or ReservationPool and the ComputeCapacity you specified is greater than what the backing Provider VDC can supply.

        Default is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#allow_over_commit OrgVdc#allow_over_commit}
        '''
        result = self._values.get("allow_over_commit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_guaranteed(self) -> typing.Optional[jsii.Number]:
        '''Percentage of allocated CPU resources guaranteed to vApps deployed in this VDC.

        For example, if this value is 0.75, then 75% of allocated resources are guaranteed. Required when AllocationModel is AllocationVApp or AllocationPool. If the element is empty, vCD sets a value

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu_guaranteed OrgVdc#cpu_guaranteed}
        '''
        result = self._values.get("cpu_guaranteed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_speed(self) -> typing.Optional[jsii.Number]:
        '''Specifies the clock frequency, in Megahertz, for any virtual CPU that is allocated to a VM.

        A VM with 2 vCPUs will consume twice as much of this value. Ignored for ReservationPool. Required when AllocationModel is AllocationVApp or AllocationPool, and may not be less than 256 MHz. Defaults to 1000 MHz if the element is empty or missing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#cpu_speed OrgVdc#cpu_speed}
        '''
        result = self._values.get("cpu_speed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_compute_policy_id(self) -> typing.Optional[builtins.str]:
        '''ID of default Compute policy for this VDC, which can be a VM Sizing Policy, VM Placement Policy or vGPU Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#default_compute_policy_id OrgVdc#default_compute_policy_id}
        '''
        result = self._values.get("default_compute_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_vm_sizing_policy_id(self) -> typing.Optional[builtins.str]:
        '''ID of default VM Compute policy, which can be a VM Sizing Policy, VM Placement Policy or vGPU Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#default_vm_sizing_policy_id OrgVdc#default_vm_sizing_policy_id}
        '''
        result = self._values.get("default_vm_sizing_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When destroying use delete_force=True to remove a VDC and any objects it contains, regardless of their state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#delete_force OrgVdc#delete_force}
        '''
        result = self._values.get("delete_force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_recursive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When destroying use delete_recursive=True to remove the VDC and any objects it contains that are in a state that normally allows removal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#delete_recursive OrgVdc#delete_recursive}
        '''
        result = self._values.get("delete_recursive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#description OrgVdc#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_cluster_id(self) -> typing.Optional[builtins.str]:
        '''ID of NSX-T Edge Cluster (provider vApp networking services and DHCP capability for Isolated networks).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#edge_cluster_id OrgVdc#edge_cluster_id}
        '''
        result = self._values.get("edge_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to indicate if the Flex VDC is to be elastic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#elasticity OrgVdc#elasticity}
        '''
        result = self._values.get("elasticity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if this VDC is enabled for use by the organization VDCs. Default is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enabled OrgVdc#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_fast_provisioning(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Request for fast provisioning.

        Request will be honored only if the underlying datas tore supports it. Fast provisioning can reduce the time it takes to create virtual machines by using vSphere linked clones. If you disable fast provisioning, all provisioning operations will result in full clones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_fast_provisioning OrgVdc#enable_fast_provisioning}
        '''
        result = self._values.get("enable_fast_provisioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_nsxv_distributed_firewall(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to enable distributed firewall - Only applies to NSX-V VDCs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_nsxv_distributed_firewall OrgVdc#enable_nsxv_distributed_firewall}
        '''
        result = self._values.get("enable_nsxv_distributed_firewall")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_thin_provisioning(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean to request thin provisioning.

        Request will be honored only if the underlying datastore supports it. Thin provisioning saves storage space by committing it on demand. This allows over-allocation of storage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_thin_provisioning OrgVdc#enable_thin_provisioning}
        '''
        result = self._values.get("enable_thin_provisioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vm_discovery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if discovery of vCenter VMs is enabled for resource pools backing this VDC.

        If left unspecified, the actual behaviour depends on enablement at the organization level and at the system level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enable_vm_discovery OrgVdc#enable_vm_discovery}
        '''
        result = self._values.get("enable_vm_discovery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#id OrgVdc#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_vm_memory_overhead(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to indicate if the Flex VDC is to include memory overhead into its accounting for admission control.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#include_vm_memory_overhead OrgVdc#include_vm_memory_overhead}
        '''
        result = self._values.get("include_vm_memory_overhead")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def memory_guaranteed(self) -> typing.Optional[jsii.Number]:
        '''Percentage of allocated memory resources guaranteed to vApps deployed in this VDC.

        For example, if this value is 0.75, then 75% of allocated resources are guaranteed. Required when AllocationModel is AllocationVApp or AllocationPool. When Allocation model is AllocationPool minimum value is 0.2. If the element is empty, vCD sets a value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#memory_guaranteed OrgVdc#memory_guaranteed}
        '''
        result = self._values.get("memory_guaranteed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key and value pairs for Org VDC metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#metadata OrgVdc#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcMetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#metadata_entry OrgVdc#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcMetadataEntry"]]], result)

    @builtins.property
    def network_pool_name(self) -> typing.Optional[builtins.str]:
        '''The name of a network pool in the Provider VDC.

        Required if this VDC will contain routed or isolated networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#network_pool_name OrgVdc#network_pool_name}
        '''
        result = self._values.get("network_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_quota(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of network objects that can be deployed in this VDC.

        Defaults to 0, which means no networks can be deployed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#network_quota OrgVdc#network_quota}
        '''
        result = self._values.get("network_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nic_quota(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of virtual NICs allowed in this VDC. Defaults to 0, which specifies an unlimited number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#nic_quota OrgVdc#nic_quota}
        '''
        result = self._values.get("nic_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#org OrgVdc#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_placement_policy_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of VM Placement Policy IDs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_placement_policy_ids OrgVdc#vm_placement_policy_ids}
        '''
        result = self._values.get("vm_placement_policy_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vm_quota(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of VMs that can be created in this VDC.

        Includes deployed and undeployed VMs in vApps and vApp templates. Defaults to 0, which specifies an unlimited number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_quota OrgVdc#vm_quota}
        '''
        result = self._values.get("vm_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vm_sizing_policy_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of VM Sizing Policy IDs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_sizing_policy_ids OrgVdc#vm_sizing_policy_ids}
        '''
        result = self._values.get("vm_sizing_policy_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vm_vgpu_policy_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of VM vGPU Policy IDs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#vm_vgpu_policy_ids OrgVdc#vm_vgpu_policy_ids}
        '''
        result = self._values.get("vm_vgpu_policy_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.orgVdc.OrgVdcMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "is_system": "isSystem",
        "key": "key",
        "type": "type",
        "user_access": "userAccess",
        "value": "value",
    },
)
class OrgVdcMetadataEntry:
    def __init__(
        self,
        *,
        is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user_access: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#is_system OrgVdc#is_system}
        :param key: Key of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#key OrgVdc#key}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#type OrgVdc#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#user_access OrgVdc#user_access}
        :param value: Value of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#value OrgVdc#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f71667db8d2f565cf19277b9b8818be4d945b0ba94970763a222d3c58b33f7f)
            check_type(argname="argument is_system", value=is_system, expected_type=type_hints["is_system"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_access", value=user_access, expected_type=type_hints["user_access"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_system is not None:
            self._values["is_system"] = is_system
        if key is not None:
            self._values["key"] = key
        if type is not None:
            self._values["type"] = type
        if user_access is not None:
            self._values["user_access"] = user_access
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_system(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#is_system OrgVdc#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#key OrgVdc#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#type OrgVdc#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#user_access OrgVdc#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#value OrgVdc#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcMetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdc.OrgVdcMetadataEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d0fbd2808a1442ad0f635ba5de013dc7e83d9a81dfb425952b004f218d67c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrgVdcMetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9882ba70ac4b888225c60ad702d3c9c2da5e3a7805bc79822db75605e9602aed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrgVdcMetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c72ac7dbd3b12f4b82d997e77e699c5c2da0c1fbb3218c68610c85a356c1b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b669a3e6532fed36a8f82a5b3a3ff36d7c4a6b78891bb7f251808d3cae38d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96a192ae4a27f09a6f158a03ff15ec98bc743b95bbc8845ffed14e7b2bd3bc00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcMetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcMetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcMetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a529327d9d2e053c8485f938450359617eb0912f8cce1cdbadc02330529f0777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrgVdcMetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdc.OrgVdcMetadataEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e79da1b78029952026f5531e394f10df748b470a7d9f0390835585009b059d18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsSystem")
    def reset_is_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSystem", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserAccess")
    def reset_user_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAccess", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dcff38e8e62cdcaf2775d215c337130438da6d3584551c0c76f94edab1fca97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21bcc4036bcb0e0509be93c7e0e2432b7dae6f96548f4707c95a37bed7e75e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5303adfa2cd93ab06dc2d37b7feade6ac45c8ef74828d6dc7c2edb27ce8910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0a7fa5c5914adc8e30f55e14729adb963eef032a964a7534669fcf38489ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6550a38ad0d4e6287b3dc43ebbbfe02effc1bdbb03b856a50096773fc363f3e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcMetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcMetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcMetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3c8ff7da035b504266c11b8026ae3abf11d666778d5b1d6506c1fb5d693c77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgVdc.OrgVdcStorageProfile",
    jsii_struct_bases=[],
    name_mapping={
        "default": "default",
        "limit": "limit",
        "name": "name",
        "enabled": "enabled",
    },
)
class OrgVdcStorageProfile:
    def __init__(
        self,
        *,
        default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        limit: jsii.Number,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param default: True if this is default storage profile for this VDC. The default storage profile is used when an object that can specify a storage profile is created with no storage profile specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#default OrgVdc#default}
        :param limit: Maximum number of MB allocated for this storage profile. A value of 0 specifies unlimited MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#limit OrgVdc#limit}
        :param name: Name of Provider VDC storage profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#name OrgVdc#name}
        :param enabled: True if this storage profile is enabled for use in the VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enabled OrgVdc#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea6525bfa09420498f91e6d35efc08cecf2b3c2f68c31ad2c4bdbdb7800a128)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default": default,
            "limit": limit,
            "name": name,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''True if this is default storage profile for this VDC.

        The default storage profile is used when an object that can specify a storage profile is created with no storage profile specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#default OrgVdc#default}
        '''
        result = self._values.get("default")
        assert result is not None, "Required property 'default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def limit(self) -> jsii.Number:
        '''Maximum number of MB allocated for this storage profile. A value of 0 specifies unlimited MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#limit OrgVdc#limit}
        '''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of Provider VDC storage profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#name OrgVdc#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if this storage profile is enabled for use in the VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc#enabled OrgVdc#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcStorageProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcStorageProfileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdc.OrgVdcStorageProfileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3416efcdf9ad92880d07fd2044a92b7565696679bd0930fb3896f31587b21443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrgVdcStorageProfileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d927cd2cd06ebe4fbec228a63e7629b94ddc7aaecc7010fd93f7d25ab37cd2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrgVdcStorageProfileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e73ecd00dab158d9ea0d7383abf533519ae94a8735ed74bf521cd350dba48a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f31cfb7b02fdcdc40627a78ff679bd8445a2dc98fbe933ab589bca6d6c048c94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf60ae050f682fd463fc07de3c59b98e11fa946bbfd8401a5ddcf188be93bb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcStorageProfile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcStorageProfile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcStorageProfile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8580ba4c0a19c9c73db3570f89263deaf48514008183c8348efde313965d2795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrgVdcStorageProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdc.OrgVdcStorageProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81ce85193273d9be76bb1b4a4089255c28c390db5f885371ca7c175f42a22627)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="storageUsedInMb")
    def storage_used_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageUsedInMb"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cccf70caa4ff48d100cdb43ca71bf80e716aaf6cc51497442ab209c1c285d8a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e335200ee0e055b9120e7b80f7adc9dcb3871a0797acf256bc9156181ffdba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a891c169254ae14227b1a628585b04060cbd363b411d7f0f12279c0ddbbdae79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52e3d46d977c399901330cd212d46fdfa85c4c11b0997ca04472aaeb9488b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcStorageProfile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcStorageProfile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcStorageProfile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b82105971a7c89aace553e00cbe0ff12d744a8ced790a31d267aa6e6b93015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OrgVdc",
    "OrgVdcComputeCapacity",
    "OrgVdcComputeCapacityCpu",
    "OrgVdcComputeCapacityCpuOutputReference",
    "OrgVdcComputeCapacityMemory",
    "OrgVdcComputeCapacityMemoryOutputReference",
    "OrgVdcComputeCapacityOutputReference",
    "OrgVdcConfig",
    "OrgVdcMetadataEntry",
    "OrgVdcMetadataEntryList",
    "OrgVdcMetadataEntryOutputReference",
    "OrgVdcStorageProfile",
    "OrgVdcStorageProfileList",
    "OrgVdcStorageProfileOutputReference",
]

publication.publish()

def _typecheckingstub__6c35e61e4f0e28e6364694bfea726476c4b575eed184e7b8c72e84398879565c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    allocation_model: builtins.str,
    compute_capacity: typing.Union[OrgVdcComputeCapacity, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    provider_vdc_name: builtins.str,
    storage_profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcStorageProfile, typing.Dict[builtins.str, typing.Any]]]],
    allow_over_commit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_guaranteed: typing.Optional[jsii.Number] = None,
    cpu_speed: typing.Optional[jsii.Number] = None,
    default_compute_policy_id: typing.Optional[builtins.str] = None,
    default_vm_sizing_policy_id: typing.Optional[builtins.str] = None,
    delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_cluster_id: typing.Optional[builtins.str] = None,
    elasticity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_fast_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_nsxv_distributed_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_thin_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vm_discovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    include_vm_memory_overhead: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_guaranteed: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_pool_name: typing.Optional[builtins.str] = None,
    network_quota: typing.Optional[jsii.Number] = None,
    nic_quota: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    vm_placement_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_quota: typing.Optional[jsii.Number] = None,
    vm_sizing_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_vgpu_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__c310db164f12b2d35ae0268f99ef042b9063cb6bae162b08c31fc1e94b6fd0b8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6875a284aaae890fca1805ad800469e356b27d297510e301ef40d8e98db4944b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcMetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f25b96499a0849580fbdb1bed13fa885493854fa204e67cc6905b0c763d6293(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcStorageProfile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149121f19a57508741d190edb32119e0822b1ff055b213f97a1331e091964623(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa194b018f2b1266a89e943c4b0399c96566e46c1623d1016b10a53b2dbdc405(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ccd9fa7f89ae6120f5ecd1a5cb94a3e5b54f6d4a1bc75694bdabe13669959d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d2113ee0bd27bbb2790c183e2b64c4b24d9b8849852bbb459f09068b850f7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a5e7ed405c64a519a13a6ced1ac57ed73072933b87ac6033e617f4fef6c186(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466ed11bcea7f40a5ebb21c96bd28e281511e10f4df3c0d0d5b0b38b30c279ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6848f0796681257fec77c329ef4ca5b21b4ae1409570ea625077815d76dcd39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696c2df69ac7f470241e9988161920bfb857d04ae17d6f2bd93423bc840f70ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6c4ed56913858cf786cb5333b90e63695bf96b1081969a1a823f058d5827f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa8a8652313bfb3d86da3cc7d110fdc07557a46d729f2671719929b81b128a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d790308ba418c6347dd4b851daa998cf77befd93abe03e48939a9eef116721a8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4894ac21ce55aec4abddc160548ee8682cada9560d8ee14dd6a39bfddc28be99(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf6ec12f2f2b7033d964b4405019d744aab689511af0342d543d488c7074611(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d4a592bc0d930bcf84306ab904b9b9d8b5ad704f23876320ee9181df2f8622(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90624658e8e62f3b3cd7567d159d6b019c94d2ac87d3763d2c4c1b6460fc228d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff802fdb34a23817fb8d1181b6b86100d715923d1bb58677e2f87c28455a10a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee2a87da4a8245f771821dbe6f104606dd41d5f8a451cb7ebb7d9a1d2291375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9853c67986448f800576f7d7798fa87e97b30f2003da2403d7a28ae820448ba6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f6fa73e7827c4635104559fc9cbdb820cc8513a7ce22e99957af7b9b9ba4f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8af76f77d88ccbf028287dc75ca15ecfdc0359b52578e789177bbc9de0b493(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed9fcc6851d05db8bfcb8b807d8c098fc38c4007a18597a92f9f2eb72829557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5811e34b35bc1b93b8202ef73e38029bb19fc91d0f39709e1fa425b344456935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6faa4a0f9b8d5ed947c58350e5e821f0ca1d0c58ed75ec78d618ff45badc8717(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2048e6c541cedabc6ce6f3bc2e7387088793638d422f3ab97004a00bfc40e0a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab57527fbf546cf8d9211c57bd5f66869d91cf3bd2d5b8179dff2a0b5a19ddb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771534735b5eed8f7aace67319effd17856411554a42eeb31e0aa08aba1b692c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef034795490846f113a5b6b467200f56c974d28538a47991992b3349c4b01ff0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a474260d8980de604365afd1671fba240ba190cc08991b5309779178d0b8542b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff65603138ce466e3b7aa0b143d22c422660ac0914557f25c5f74eb7f5adb8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09dc170fc06e0700bd02517ad4cbf3c5748e360be7a1646d58e75ac21127c8a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1118a1c401c3d3c9b3b3c70e5bc6fa2312112b4a957af350457c488b8628c95e(
    *,
    cpu: typing.Union[OrgVdcComputeCapacityCpu, typing.Dict[builtins.str, typing.Any]],
    memory: typing.Union[OrgVdcComputeCapacityMemory, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb1b5d4bd04c9370fcd7ced1fbbbdb1bc3d603ff3c0b178810568a0b3f4a365(
    *,
    allocated: typing.Optional[jsii.Number] = None,
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3141df366328664c9d4800d2c05b639ad8c196ebe9fae41ba3a3fcc43308b14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92daa6c984398533f685e797c69a19c58b8f179ec7c67166c633cadf20e719d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b23045a5bc7742b195042a48f89c2e6f77b7c16651407d1a8bac16c2703375(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426e07869031d9be5459259f8c3e8f8970cfbb1ef61ca4f14f7d40456eae3ee4(
    value: typing.Optional[OrgVdcComputeCapacityCpu],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f20d50a59dd827ac355639e649263996bacbf7f0b2f7f8db730b2a6acaad2c8(
    *,
    allocated: typing.Optional[jsii.Number] = None,
    limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef27acf75114d3e2738adad346a0e131a7ee1fe9d411e408fae967dceb261d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c54deb69822d41a80f3ff4fa9c7e38b08faf8267e3ea92c6df0a656505ddb98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1adcab172895deb53b7a4b9141aec095d29476a9777bed1df4cc216ad819ce2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d29440dc1e934b4241f209bc5ae9dad600906a6bf40186575ce326349beca8c(
    value: typing.Optional[OrgVdcComputeCapacityMemory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1631843f22d803acbf2c79e7de1b94154e60769d1fb8b1fdae5b1a2d6b9ae5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5839e41b51f6c3b8505ef2854b496c64efbc4733f6dac8382c6b8636166272c4(
    value: typing.Optional[OrgVdcComputeCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a99ba475e9412bf13760b38208401291c7102abc341f2cd0375d0e8967c89d7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allocation_model: builtins.str,
    compute_capacity: typing.Union[OrgVdcComputeCapacity, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    provider_vdc_name: builtins.str,
    storage_profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcStorageProfile, typing.Dict[builtins.str, typing.Any]]]],
    allow_over_commit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_guaranteed: typing.Optional[jsii.Number] = None,
    cpu_speed: typing.Optional[jsii.Number] = None,
    default_compute_policy_id: typing.Optional[builtins.str] = None,
    default_vm_sizing_policy_id: typing.Optional[builtins.str] = None,
    delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_cluster_id: typing.Optional[builtins.str] = None,
    elasticity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_fast_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_nsxv_distributed_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_thin_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vm_discovery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    include_vm_memory_overhead: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_guaranteed: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_pool_name: typing.Optional[builtins.str] = None,
    network_quota: typing.Optional[jsii.Number] = None,
    nic_quota: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    vm_placement_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_quota: typing.Optional[jsii.Number] = None,
    vm_sizing_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_vgpu_policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f71667db8d2f565cf19277b9b8818be4d945b0ba94970763a222d3c58b33f7f(
    *,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d0fbd2808a1442ad0f635ba5de013dc7e83d9a81dfb425952b004f218d67c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9882ba70ac4b888225c60ad702d3c9c2da5e3a7805bc79822db75605e9602aed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c72ac7dbd3b12f4b82d997e77e699c5c2da0c1fbb3218c68610c85a356c1b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b669a3e6532fed36a8f82a5b3a3ff36d7c4a6b78891bb7f251808d3cae38d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a192ae4a27f09a6f158a03ff15ec98bc743b95bbc8845ffed14e7b2bd3bc00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a529327d9d2e053c8485f938450359617eb0912f8cce1cdbadc02330529f0777(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcMetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79da1b78029952026f5531e394f10df748b470a7d9f0390835585009b059d18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcff38e8e62cdcaf2775d215c337130438da6d3584551c0c76f94edab1fca97d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21bcc4036bcb0e0509be93c7e0e2432b7dae6f96548f4707c95a37bed7e75e5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5303adfa2cd93ab06dc2d37b7feade6ac45c8ef74828d6dc7c2edb27ce8910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0a7fa5c5914adc8e30f55e14729adb963eef032a964a7534669fcf38489ee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6550a38ad0d4e6287b3dc43ebbbfe02effc1bdbb03b856a50096773fc363f3e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3c8ff7da035b504266c11b8026ae3abf11d666778d5b1d6506c1fb5d693c77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcMetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea6525bfa09420498f91e6d35efc08cecf2b3c2f68c31ad2c4bdbdb7800a128(
    *,
    default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    limit: jsii.Number,
    name: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3416efcdf9ad92880d07fd2044a92b7565696679bd0930fb3896f31587b21443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d927cd2cd06ebe4fbec228a63e7629b94ddc7aaecc7010fd93f7d25ab37cd2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e73ecd00dab158d9ea0d7383abf533519ae94a8735ed74bf521cd350dba48a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31cfb7b02fdcdc40627a78ff679bd8445a2dc98fbe933ab589bca6d6c048c94(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf60ae050f682fd463fc07de3c59b98e11fa946bbfd8401a5ddcf188be93bb52(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8580ba4c0a19c9c73db3570f89263deaf48514008183c8348efde313965d2795(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcStorageProfile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ce85193273d9be76bb1b4a4089255c28c390db5f885371ca7c175f42a22627(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cccf70caa4ff48d100cdb43ca71bf80e716aaf6cc51497442ab209c1c285d8a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e335200ee0e055b9120e7b80f7adc9dcb3871a0797acf256bc9156181ffdba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a891c169254ae14227b1a628585b04060cbd363b411d7f0f12279c0ddbbdae79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52e3d46d977c399901330cd212d46fdfa85c4c11b0997ca04472aaeb9488b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b82105971a7c89aace553e00cbe0ff12d744a8ced790a31d267aa6e6b93015(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcStorageProfile]],
) -> None:
    """Type checking stubs"""
    pass
