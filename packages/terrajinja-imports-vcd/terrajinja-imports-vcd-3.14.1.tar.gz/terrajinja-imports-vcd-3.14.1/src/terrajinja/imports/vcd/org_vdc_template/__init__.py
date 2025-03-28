'''
# `vcd_org_vdc_template`

Refer to the Terraform Registry for docs: [`vcd_org_vdc_template`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template).
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


class OrgVdcTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template vcd_org_vdc_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        allocation_model: builtins.str,
        compute_configuration: typing.Union["OrgVdcTemplateComputeConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        provider_vdc: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcTemplateProviderVdc", typing.Dict[builtins.str, typing.Any]]]],
        storage_profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcTemplateStorageProfile", typing.Dict[builtins.str, typing.Any]]]],
        tenant_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        edge_gateway: typing.Optional[typing.Union["OrgVdcTemplateEdgeGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_fast_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_thin_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        network_pool_id: typing.Optional[builtins.str] = None,
        nic_quota: typing.Optional[jsii.Number] = None,
        provisioned_network_quota: typing.Optional[jsii.Number] = None,
        readable_by_org_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tenant_description: typing.Optional[builtins.str] = None,
        vm_quota: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template vcd_org_vdc_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param allocation_model: Allocation model that the VDCs instantiated from this template will use. Must be one of: 'AllocationVApp', 'AllocationPool', 'ReservationPool' or 'Flex' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#allocation_model OrgVdcTemplate#allocation_model}
        :param compute_configuration: compute_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#compute_configuration OrgVdcTemplate#compute_configuration}
        :param name: Name of the VDC Template as seen by the System administrator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#name OrgVdcTemplate#name}
        :param provider_vdc: provider_vdc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#provider_vdc OrgVdcTemplate#provider_vdc}
        :param storage_profile: storage_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#storage_profile OrgVdcTemplate#storage_profile}
        :param tenant_name: Name of the VDC Template as seen by the tenants (organizations). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#tenant_name OrgVdcTemplate#tenant_name}
        :param description: Description of the VDC Template as seen by the System administrator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#description OrgVdcTemplate#description}
        :param edge_gateway: edge_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#edge_gateway OrgVdcTemplate#edge_gateway}
        :param enable_fast_provisioning: If 'true', the VDCs instantiated from this template will have Fast provisioning enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#enable_fast_provisioning OrgVdcTemplate#enable_fast_provisioning}
        :param enable_thin_provisioning: If 'true', the VDCs instantiated from this template will have Thin provisioning enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#enable_thin_provisioning OrgVdcTemplate#enable_thin_provisioning}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#id OrgVdcTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_pool_id: If set, specifies the Network pool for the instantiated VDCs. Otherwise, it is automatically chosen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#network_pool_id OrgVdcTemplate#network_pool_id}
        :param nic_quota: Quota for the NICs of the instantiated VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#nic_quota OrgVdcTemplate#nic_quota}
        :param provisioned_network_quota: Quota for the provisioned networks of the instantiated VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#provisioned_network_quota OrgVdcTemplate#provisioned_network_quota}
        :param readable_by_org_ids: IDs of the Organizations that will be able to view and instantiate this VDC template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#readable_by_org_ids OrgVdcTemplate#readable_by_org_ids}
        :param tenant_description: Description of the VDC Template as seen by the tenants (organizations). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#tenant_description OrgVdcTemplate#tenant_description}
        :param vm_quota: Quota for the VMs of the instantiated VDCs. 0 means unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#vm_quota OrgVdcTemplate#vm_quota}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e68d8f298a6183539c7a8eb83fd836ba27b9694a7f429e08075fe61c679cfc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrgVdcTemplateConfig(
            allocation_model=allocation_model,
            compute_configuration=compute_configuration,
            name=name,
            provider_vdc=provider_vdc,
            storage_profile=storage_profile,
            tenant_name=tenant_name,
            description=description,
            edge_gateway=edge_gateway,
            enable_fast_provisioning=enable_fast_provisioning,
            enable_thin_provisioning=enable_thin_provisioning,
            id=id,
            network_pool_id=network_pool_id,
            nic_quota=nic_quota,
            provisioned_network_quota=provisioned_network_quota,
            readable_by_org_ids=readable_by_org_ids,
            tenant_description=tenant_description,
            vm_quota=vm_quota,
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
        '''Generates CDKTF code for importing a OrgVdcTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrgVdcTemplate to import.
        :param import_from_id: The id of the existing OrgVdcTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrgVdcTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62deb087bc340246451045ab540e92cc1787143ec35499121bc4e9637167d78d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putComputeConfiguration")
    def put_compute_configuration(
        self,
        *,
        cpu_allocated: typing.Optional[jsii.Number] = None,
        cpu_guaranteed: typing.Optional[jsii.Number] = None,
        cpu_limit: typing.Optional[jsii.Number] = None,
        cpu_speed: typing.Optional[jsii.Number] = None,
        elasticity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_vm_memory_overhead: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_allocated: typing.Optional[jsii.Number] = None,
        memory_guaranteed: typing.Optional[jsii.Number] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_allocated: AllocationPool, ReservationPool, Flex: The maximum amount of CPU, in MHz, available to the VMs running within the VDC that is instantiated from this template. Minimum is 256MHz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_allocated OrgVdcTemplate#cpu_allocated}
        :param cpu_guaranteed: AllocationVApp, AllocationPool, Flex: The percentage of the CPU guaranteed to be available to VMs running within the VDC instantiated from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_guaranteed OrgVdcTemplate#cpu_guaranteed}
        :param cpu_limit: AllocationVApp, ReservationPool, Flex: The limit amount of CPU, in MHz, of the VDC that is instantiated from this template. Minimum is 256MHz. 0 means unlimited Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_limit OrgVdcTemplate#cpu_limit}
        :param cpu_speed: AllocationVApp, AllocationPool, Flex: Specifies the clock frequency, in MHz, for any virtual CPU that is allocated to a VM. Minimum is 256MHz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_speed OrgVdcTemplate#cpu_speed}
        :param elasticity: Flex only: True if compute capacity can grow or shrink based on demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#elasticity OrgVdcTemplate#elasticity}
        :param include_vm_memory_overhead: Flex only: True if the instantiated VDC includes memory overhead into its accounting for admission control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#include_vm_memory_overhead OrgVdcTemplate#include_vm_memory_overhead}
        :param memory_allocated: AllocationPool, ReservationPool, Flex: The maximum amount of Memory, in MB, available to the VMs running within the VDC that is instantiated from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_allocated OrgVdcTemplate#memory_allocated}
        :param memory_guaranteed: AllocationVApp, AllocationPool, Flex: The percentage of the Memory guaranteed to be available to VMs running within the VDC instantiated from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_guaranteed OrgVdcTemplate#memory_guaranteed}
        :param memory_limit: AllocationVApp, ReservationPool, Flex: The limit amount of Memory, in MB, of the VDC that is instantiated from this template. Minimum is 1024MB. 0 means unlimited Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_limit OrgVdcTemplate#memory_limit}
        '''
        value = OrgVdcTemplateComputeConfiguration(
            cpu_allocated=cpu_allocated,
            cpu_guaranteed=cpu_guaranteed,
            cpu_limit=cpu_limit,
            cpu_speed=cpu_speed,
            elasticity=elasticity,
            include_vm_memory_overhead=include_vm_memory_overhead,
            memory_allocated=memory_allocated,
            memory_guaranteed=memory_guaranteed,
            memory_limit=memory_limit,
        )

        return typing.cast(None, jsii.invoke(self, "putComputeConfiguration", [value]))

    @jsii.member(jsii_name="putEdgeGateway")
    def put_edge_gateway(
        self,
        *,
        name: builtins.str,
        routed_network_gateway_cidr: builtins.str,
        routed_network_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        ip_allocation_count: typing.Optional[jsii.Number] = None,
        routed_network_description: typing.Optional[builtins.str] = None,
        static_ip_pool: typing.Optional[typing.Union["OrgVdcTemplateEdgeGatewayStaticIpPool", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#name OrgVdcTemplate#name}
        :param routed_network_gateway_cidr: CIDR of the Edge Gateway for the created routed network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_gateway_cidr OrgVdcTemplate#routed_network_gateway_cidr}
        :param routed_network_name: Name of the routed network to create with the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_name OrgVdcTemplate#routed_network_name}
        :param description: Description of the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#description OrgVdcTemplate#description}
        :param ip_allocation_count: Allocated IPs for the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#ip_allocation_count OrgVdcTemplate#ip_allocation_count}
        :param routed_network_description: Description of the routed network to create with the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_description OrgVdcTemplate#routed_network_description}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#static_ip_pool OrgVdcTemplate#static_ip_pool}
        '''
        value = OrgVdcTemplateEdgeGateway(
            name=name,
            routed_network_gateway_cidr=routed_network_gateway_cidr,
            routed_network_name=routed_network_name,
            description=description,
            ip_allocation_count=ip_allocation_count,
            routed_network_description=routed_network_description,
            static_ip_pool=static_ip_pool,
        )

        return typing.cast(None, jsii.invoke(self, "putEdgeGateway", [value]))

    @jsii.member(jsii_name="putProviderVdc")
    def put_provider_vdc(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcTemplateProviderVdc", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad8b7fce3acda2ab35ce37ef2823cfc0990a50e18f684fb7a9ea51c838d4961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProviderVdc", [value]))

    @jsii.member(jsii_name="putStorageProfile")
    def put_storage_profile(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcTemplateStorageProfile", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67bedaae0d354ee291afe1270888c97c7700b0eb594080c04293d31dd7541c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageProfile", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEdgeGateway")
    def reset_edge_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeGateway", []))

    @jsii.member(jsii_name="resetEnableFastProvisioning")
    def reset_enable_fast_provisioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableFastProvisioning", []))

    @jsii.member(jsii_name="resetEnableThinProvisioning")
    def reset_enable_thin_provisioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableThinProvisioning", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworkPoolId")
    def reset_network_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPoolId", []))

    @jsii.member(jsii_name="resetNicQuota")
    def reset_nic_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNicQuota", []))

    @jsii.member(jsii_name="resetProvisionedNetworkQuota")
    def reset_provisioned_network_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedNetworkQuota", []))

    @jsii.member(jsii_name="resetReadableByOrgIds")
    def reset_readable_by_org_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadableByOrgIds", []))

    @jsii.member(jsii_name="resetTenantDescription")
    def reset_tenant_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantDescription", []))

    @jsii.member(jsii_name="resetVmQuota")
    def reset_vm_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmQuota", []))

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
    @jsii.member(jsii_name="computeConfiguration")
    def compute_configuration(
        self,
    ) -> "OrgVdcTemplateComputeConfigurationOutputReference":
        return typing.cast("OrgVdcTemplateComputeConfigurationOutputReference", jsii.get(self, "computeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="edgeGateway")
    def edge_gateway(self) -> "OrgVdcTemplateEdgeGatewayOutputReference":
        return typing.cast("OrgVdcTemplateEdgeGatewayOutputReference", jsii.get(self, "edgeGateway"))

    @builtins.property
    @jsii.member(jsii_name="providerVdc")
    def provider_vdc(self) -> "OrgVdcTemplateProviderVdcList":
        return typing.cast("OrgVdcTemplateProviderVdcList", jsii.get(self, "providerVdc"))

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> "OrgVdcTemplateStorageProfileList":
        return typing.cast("OrgVdcTemplateStorageProfileList", jsii.get(self, "storageProfile"))

    @builtins.property
    @jsii.member(jsii_name="allocationModelInput")
    def allocation_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocationModelInput"))

    @builtins.property
    @jsii.member(jsii_name="computeConfigurationInput")
    def compute_configuration_input(
        self,
    ) -> typing.Optional["OrgVdcTemplateComputeConfiguration"]:
        return typing.cast(typing.Optional["OrgVdcTemplateComputeConfiguration"], jsii.get(self, "computeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayInput")
    def edge_gateway_input(self) -> typing.Optional["OrgVdcTemplateEdgeGateway"]:
        return typing.cast(typing.Optional["OrgVdcTemplateEdgeGateway"], jsii.get(self, "edgeGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="enableFastProvisioningInput")
    def enable_fast_provisioning_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableFastProvisioningInput"))

    @builtins.property
    @jsii.member(jsii_name="enableThinProvisioningInput")
    def enable_thin_provisioning_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableThinProvisioningInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPoolIdInput")
    def network_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nicQuotaInput")
    def nic_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nicQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="providerVdcInput")
    def provider_vdc_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcTemplateProviderVdc"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcTemplateProviderVdc"]]], jsii.get(self, "providerVdcInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedNetworkQuotaInput")
    def provisioned_network_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedNetworkQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="readableByOrgIdsInput")
    def readable_by_org_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "readableByOrgIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileInput")
    def storage_profile_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcTemplateStorageProfile"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcTemplateStorageProfile"]]], jsii.get(self, "storageProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantDescriptionInput")
    def tenant_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantNameInput")
    def tenant_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vmQuotaInput")
    def vm_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="allocationModel")
    def allocation_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocationModel"))

    @allocation_model.setter
    def allocation_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68483bc7cc0da51f01845969bfdf54f7c72f658367fe3ed9ab8593b70568d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocationModel", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d96b27fcd02a40bd8f09831d14014058c856f0d468522906a8ebc27f54a8342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__c770e793786f562346029f1f2d40034507e603e917eb879431d25de6f46489e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFastProvisioning", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__03b9fcd6b273b615e79b49ecd8aab36482678a214cef9ae4a279dbbeafb11dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableThinProvisioning", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0386159b795efd09d8b808ed495a0d724248adf47c46a19c8074121282f345b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608906e6020beaaa956c7332eafa293ccc8079564d655dcb7eed0ac6d952221b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkPoolId")
    def network_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPoolId"))

    @network_pool_id.setter
    def network_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eafad9f0eba2d76dd2b1d22138635b8684f3896cb949b4189ce1ef49de330c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="nicQuota")
    def nic_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nicQuota"))

    @nic_quota.setter
    def nic_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc1e1850a25d70de79f8357072a9870dd837eb8c34bc922b18ab8489f8104a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicQuota", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedNetworkQuota")
    def provisioned_network_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedNetworkQuota"))

    @provisioned_network_quota.setter
    def provisioned_network_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879af79272383d428ba9204c8c6234736b6f1ac5b37cc6b429c268452267fb8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedNetworkQuota", value)

    @builtins.property
    @jsii.member(jsii_name="readableByOrgIds")
    def readable_by_org_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "readableByOrgIds"))

    @readable_by_org_ids.setter
    def readable_by_org_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7215639aad0be26e25737fff1d17664d29ef800227471a4692c77f62c15b49ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readableByOrgIds", value)

    @builtins.property
    @jsii.member(jsii_name="tenantDescription")
    def tenant_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantDescription"))

    @tenant_description.setter
    def tenant_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db0074b2f63bbb8a3f34382a5b1a104dac094be0ae64502958fce2007017ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantDescription", value)

    @builtins.property
    @jsii.member(jsii_name="tenantName")
    def tenant_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantName"))

    @tenant_name.setter
    def tenant_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b17b720bc8b3413d4aa99603641bcc6066cb0752e3aa7f8e10cf7658f1de4a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantName", value)

    @builtins.property
    @jsii.member(jsii_name="vmQuota")
    def vm_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmQuota"))

    @vm_quota.setter
    def vm_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec163ebd228a7099edce3012ac8147caaad554dbd666fc4a16337106dfe36b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmQuota", value)


@jsii.data_type(
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateComputeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_allocated": "cpuAllocated",
        "cpu_guaranteed": "cpuGuaranteed",
        "cpu_limit": "cpuLimit",
        "cpu_speed": "cpuSpeed",
        "elasticity": "elasticity",
        "include_vm_memory_overhead": "includeVmMemoryOverhead",
        "memory_allocated": "memoryAllocated",
        "memory_guaranteed": "memoryGuaranteed",
        "memory_limit": "memoryLimit",
    },
)
class OrgVdcTemplateComputeConfiguration:
    def __init__(
        self,
        *,
        cpu_allocated: typing.Optional[jsii.Number] = None,
        cpu_guaranteed: typing.Optional[jsii.Number] = None,
        cpu_limit: typing.Optional[jsii.Number] = None,
        cpu_speed: typing.Optional[jsii.Number] = None,
        elasticity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_vm_memory_overhead: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_allocated: typing.Optional[jsii.Number] = None,
        memory_guaranteed: typing.Optional[jsii.Number] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_allocated: AllocationPool, ReservationPool, Flex: The maximum amount of CPU, in MHz, available to the VMs running within the VDC that is instantiated from this template. Minimum is 256MHz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_allocated OrgVdcTemplate#cpu_allocated}
        :param cpu_guaranteed: AllocationVApp, AllocationPool, Flex: The percentage of the CPU guaranteed to be available to VMs running within the VDC instantiated from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_guaranteed OrgVdcTemplate#cpu_guaranteed}
        :param cpu_limit: AllocationVApp, ReservationPool, Flex: The limit amount of CPU, in MHz, of the VDC that is instantiated from this template. Minimum is 256MHz. 0 means unlimited Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_limit OrgVdcTemplate#cpu_limit}
        :param cpu_speed: AllocationVApp, AllocationPool, Flex: Specifies the clock frequency, in MHz, for any virtual CPU that is allocated to a VM. Minimum is 256MHz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_speed OrgVdcTemplate#cpu_speed}
        :param elasticity: Flex only: True if compute capacity can grow or shrink based on demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#elasticity OrgVdcTemplate#elasticity}
        :param include_vm_memory_overhead: Flex only: True if the instantiated VDC includes memory overhead into its accounting for admission control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#include_vm_memory_overhead OrgVdcTemplate#include_vm_memory_overhead}
        :param memory_allocated: AllocationPool, ReservationPool, Flex: The maximum amount of Memory, in MB, available to the VMs running within the VDC that is instantiated from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_allocated OrgVdcTemplate#memory_allocated}
        :param memory_guaranteed: AllocationVApp, AllocationPool, Flex: The percentage of the Memory guaranteed to be available to VMs running within the VDC instantiated from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_guaranteed OrgVdcTemplate#memory_guaranteed}
        :param memory_limit: AllocationVApp, ReservationPool, Flex: The limit amount of Memory, in MB, of the VDC that is instantiated from this template. Minimum is 1024MB. 0 means unlimited Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_limit OrgVdcTemplate#memory_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27133e1d33f3e9530579a849870026e252978f425f3a40d77742e7ad2c49e310)
            check_type(argname="argument cpu_allocated", value=cpu_allocated, expected_type=type_hints["cpu_allocated"])
            check_type(argname="argument cpu_guaranteed", value=cpu_guaranteed, expected_type=type_hints["cpu_guaranteed"])
            check_type(argname="argument cpu_limit", value=cpu_limit, expected_type=type_hints["cpu_limit"])
            check_type(argname="argument cpu_speed", value=cpu_speed, expected_type=type_hints["cpu_speed"])
            check_type(argname="argument elasticity", value=elasticity, expected_type=type_hints["elasticity"])
            check_type(argname="argument include_vm_memory_overhead", value=include_vm_memory_overhead, expected_type=type_hints["include_vm_memory_overhead"])
            check_type(argname="argument memory_allocated", value=memory_allocated, expected_type=type_hints["memory_allocated"])
            check_type(argname="argument memory_guaranteed", value=memory_guaranteed, expected_type=type_hints["memory_guaranteed"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_allocated is not None:
            self._values["cpu_allocated"] = cpu_allocated
        if cpu_guaranteed is not None:
            self._values["cpu_guaranteed"] = cpu_guaranteed
        if cpu_limit is not None:
            self._values["cpu_limit"] = cpu_limit
        if cpu_speed is not None:
            self._values["cpu_speed"] = cpu_speed
        if elasticity is not None:
            self._values["elasticity"] = elasticity
        if include_vm_memory_overhead is not None:
            self._values["include_vm_memory_overhead"] = include_vm_memory_overhead
        if memory_allocated is not None:
            self._values["memory_allocated"] = memory_allocated
        if memory_guaranteed is not None:
            self._values["memory_guaranteed"] = memory_guaranteed
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit

    @builtins.property
    def cpu_allocated(self) -> typing.Optional[jsii.Number]:
        '''AllocationPool, ReservationPool, Flex: The maximum amount of CPU, in MHz, available to the VMs running within the VDC that is instantiated from this template.

        Minimum is 256MHz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_allocated OrgVdcTemplate#cpu_allocated}
        '''
        result = self._values.get("cpu_allocated")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_guaranteed(self) -> typing.Optional[jsii.Number]:
        '''AllocationVApp, AllocationPool, Flex: The percentage of the CPU guaranteed to be available to VMs running within the VDC instantiated from this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_guaranteed OrgVdcTemplate#cpu_guaranteed}
        '''
        result = self._values.get("cpu_guaranteed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_limit(self) -> typing.Optional[jsii.Number]:
        '''AllocationVApp, ReservationPool, Flex: The limit amount of CPU, in MHz, of the VDC that is instantiated from this template.

        Minimum is 256MHz. 0 means unlimited

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_limit OrgVdcTemplate#cpu_limit}
        '''
        result = self._values.get("cpu_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_speed(self) -> typing.Optional[jsii.Number]:
        '''AllocationVApp, AllocationPool, Flex: Specifies the clock frequency, in MHz, for any virtual CPU that is allocated to a VM.

        Minimum is 256MHz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#cpu_speed OrgVdcTemplate#cpu_speed}
        '''
        result = self._values.get("cpu_speed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def elasticity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flex only: True if compute capacity can grow or shrink based on demand.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#elasticity OrgVdcTemplate#elasticity}
        '''
        result = self._values.get("elasticity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_vm_memory_overhead(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flex only: True if the instantiated VDC includes memory overhead into its accounting for admission control.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#include_vm_memory_overhead OrgVdcTemplate#include_vm_memory_overhead}
        '''
        result = self._values.get("include_vm_memory_overhead")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def memory_allocated(self) -> typing.Optional[jsii.Number]:
        '''AllocationPool, ReservationPool, Flex: The maximum amount of Memory, in MB, available to the VMs running within the VDC that is instantiated from this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_allocated OrgVdcTemplate#memory_allocated}
        '''
        result = self._values.get("memory_allocated")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_guaranteed(self) -> typing.Optional[jsii.Number]:
        '''AllocationVApp, AllocationPool, Flex: The percentage of the Memory guaranteed to be available to VMs running within the VDC instantiated from this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_guaranteed OrgVdcTemplate#memory_guaranteed}
        '''
        result = self._values.get("memory_guaranteed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''AllocationVApp, ReservationPool, Flex: The limit amount of Memory, in MB, of the VDC that is instantiated from this template.

        Minimum is 1024MB. 0 means unlimited

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#memory_limit OrgVdcTemplate#memory_limit}
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcTemplateComputeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcTemplateComputeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateComputeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9476ab5847839762e517b8cb58e22aac0f20df7f4baa725a5ba64ab4b820866d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuAllocated")
    def reset_cpu_allocated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuAllocated", []))

    @jsii.member(jsii_name="resetCpuGuaranteed")
    def reset_cpu_guaranteed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuGuaranteed", []))

    @jsii.member(jsii_name="resetCpuLimit")
    def reset_cpu_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuLimit", []))

    @jsii.member(jsii_name="resetCpuSpeed")
    def reset_cpu_speed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuSpeed", []))

    @jsii.member(jsii_name="resetElasticity")
    def reset_elasticity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticity", []))

    @jsii.member(jsii_name="resetIncludeVmMemoryOverhead")
    def reset_include_vm_memory_overhead(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeVmMemoryOverhead", []))

    @jsii.member(jsii_name="resetMemoryAllocated")
    def reset_memory_allocated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryAllocated", []))

    @jsii.member(jsii_name="resetMemoryGuaranteed")
    def reset_memory_guaranteed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryGuaranteed", []))

    @jsii.member(jsii_name="resetMemoryLimit")
    def reset_memory_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryLimit", []))

    @builtins.property
    @jsii.member(jsii_name="cpuAllocatedInput")
    def cpu_allocated_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuAllocatedInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuGuaranteedInput")
    def cpu_guaranteed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuGuaranteedInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuLimitInput")
    def cpu_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSpeedInput")
    def cpu_speed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuSpeedInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticityInput")
    def elasticity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "elasticityInput"))

    @builtins.property
    @jsii.member(jsii_name="includeVmMemoryOverheadInput")
    def include_vm_memory_overhead_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeVmMemoryOverheadInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryAllocatedInput")
    def memory_allocated_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryAllocatedInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGuaranteedInput")
    def memory_guaranteed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryGuaranteedInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryLimitInput")
    def memory_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuAllocated")
    def cpu_allocated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuAllocated"))

    @cpu_allocated.setter
    def cpu_allocated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6916a2a052735a09b6abe7d8f268b2fb853627bacb3182590519e578532aebab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuAllocated", value)

    @builtins.property
    @jsii.member(jsii_name="cpuGuaranteed")
    def cpu_guaranteed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuGuaranteed"))

    @cpu_guaranteed.setter
    def cpu_guaranteed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0db1cbf865d42e0faa0aba97aa65c104bfa81e98019e3769db2828986a91dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuGuaranteed", value)

    @builtins.property
    @jsii.member(jsii_name="cpuLimit")
    def cpu_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuLimit"))

    @cpu_limit.setter
    def cpu_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749f28456d91ada251902319aed97dd500845d98489cee1399b976a0e74abb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuLimit", value)

    @builtins.property
    @jsii.member(jsii_name="cpuSpeed")
    def cpu_speed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuSpeed"))

    @cpu_speed.setter
    def cpu_speed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48df4bf12eb660bc46fc2c96684379aa2468a427bb76312f341baad3ce64970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuSpeed", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__88b101d718cea5981516978c1ebad960764e0285a0b42ca759db2a79635076c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticity", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__a50dd46defc2dafe56087ff6e6c8e77e0413d664d2b5198b1e6f39f9b1ad7a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeVmMemoryOverhead", value)

    @builtins.property
    @jsii.member(jsii_name="memoryAllocated")
    def memory_allocated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryAllocated"))

    @memory_allocated.setter
    def memory_allocated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85eda36c191759c1045e6f931efb1643cd15a35da3eba280d8cff2a27ae783f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryAllocated", value)

    @builtins.property
    @jsii.member(jsii_name="memoryGuaranteed")
    def memory_guaranteed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGuaranteed"))

    @memory_guaranteed.setter
    def memory_guaranteed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07c3bcd964b106d805e691d0d7c37195379ab303a1091b6eb0cced82ebdb45b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGuaranteed", value)

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryLimit"))

    @memory_limit.setter
    def memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3c57f5df0b38c98040f9e2c97c131227f9c9cabd39cdfdd102b4fb65402607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryLimit", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgVdcTemplateComputeConfiguration]:
        return typing.cast(typing.Optional[OrgVdcTemplateComputeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgVdcTemplateComputeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22af6783b6c6486e3d19e74abb8a18ab50c1a595f3a027901ae6e39aed178467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateConfig",
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
        "compute_configuration": "computeConfiguration",
        "name": "name",
        "provider_vdc": "providerVdc",
        "storage_profile": "storageProfile",
        "tenant_name": "tenantName",
        "description": "description",
        "edge_gateway": "edgeGateway",
        "enable_fast_provisioning": "enableFastProvisioning",
        "enable_thin_provisioning": "enableThinProvisioning",
        "id": "id",
        "network_pool_id": "networkPoolId",
        "nic_quota": "nicQuota",
        "provisioned_network_quota": "provisionedNetworkQuota",
        "readable_by_org_ids": "readableByOrgIds",
        "tenant_description": "tenantDescription",
        "vm_quota": "vmQuota",
    },
)
class OrgVdcTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        compute_configuration: typing.Union[OrgVdcTemplateComputeConfiguration, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        provider_vdc: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcTemplateProviderVdc", typing.Dict[builtins.str, typing.Any]]]],
        storage_profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgVdcTemplateStorageProfile", typing.Dict[builtins.str, typing.Any]]]],
        tenant_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        edge_gateway: typing.Optional[typing.Union["OrgVdcTemplateEdgeGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_fast_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_thin_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        network_pool_id: typing.Optional[builtins.str] = None,
        nic_quota: typing.Optional[jsii.Number] = None,
        provisioned_network_quota: typing.Optional[jsii.Number] = None,
        readable_by_org_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tenant_description: typing.Optional[builtins.str] = None,
        vm_quota: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param allocation_model: Allocation model that the VDCs instantiated from this template will use. Must be one of: 'AllocationVApp', 'AllocationPool', 'ReservationPool' or 'Flex' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#allocation_model OrgVdcTemplate#allocation_model}
        :param compute_configuration: compute_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#compute_configuration OrgVdcTemplate#compute_configuration}
        :param name: Name of the VDC Template as seen by the System administrator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#name OrgVdcTemplate#name}
        :param provider_vdc: provider_vdc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#provider_vdc OrgVdcTemplate#provider_vdc}
        :param storage_profile: storage_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#storage_profile OrgVdcTemplate#storage_profile}
        :param tenant_name: Name of the VDC Template as seen by the tenants (organizations). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#tenant_name OrgVdcTemplate#tenant_name}
        :param description: Description of the VDC Template as seen by the System administrator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#description OrgVdcTemplate#description}
        :param edge_gateway: edge_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#edge_gateway OrgVdcTemplate#edge_gateway}
        :param enable_fast_provisioning: If 'true', the VDCs instantiated from this template will have Fast provisioning enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#enable_fast_provisioning OrgVdcTemplate#enable_fast_provisioning}
        :param enable_thin_provisioning: If 'true', the VDCs instantiated from this template will have Thin provisioning enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#enable_thin_provisioning OrgVdcTemplate#enable_thin_provisioning}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#id OrgVdcTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_pool_id: If set, specifies the Network pool for the instantiated VDCs. Otherwise, it is automatically chosen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#network_pool_id OrgVdcTemplate#network_pool_id}
        :param nic_quota: Quota for the NICs of the instantiated VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#nic_quota OrgVdcTemplate#nic_quota}
        :param provisioned_network_quota: Quota for the provisioned networks of the instantiated VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#provisioned_network_quota OrgVdcTemplate#provisioned_network_quota}
        :param readable_by_org_ids: IDs of the Organizations that will be able to view and instantiate this VDC template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#readable_by_org_ids OrgVdcTemplate#readable_by_org_ids}
        :param tenant_description: Description of the VDC Template as seen by the tenants (organizations). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#tenant_description OrgVdcTemplate#tenant_description}
        :param vm_quota: Quota for the VMs of the instantiated VDCs. 0 means unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#vm_quota OrgVdcTemplate#vm_quota}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(compute_configuration, dict):
            compute_configuration = OrgVdcTemplateComputeConfiguration(**compute_configuration)
        if isinstance(edge_gateway, dict):
            edge_gateway = OrgVdcTemplateEdgeGateway(**edge_gateway)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a54fa899038074c744dbecb75bfecc6dadf8a099fc8629c7807f7de92369d5e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument allocation_model", value=allocation_model, expected_type=type_hints["allocation_model"])
            check_type(argname="argument compute_configuration", value=compute_configuration, expected_type=type_hints["compute_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider_vdc", value=provider_vdc, expected_type=type_hints["provider_vdc"])
            check_type(argname="argument storage_profile", value=storage_profile, expected_type=type_hints["storage_profile"])
            check_type(argname="argument tenant_name", value=tenant_name, expected_type=type_hints["tenant_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_gateway", value=edge_gateway, expected_type=type_hints["edge_gateway"])
            check_type(argname="argument enable_fast_provisioning", value=enable_fast_provisioning, expected_type=type_hints["enable_fast_provisioning"])
            check_type(argname="argument enable_thin_provisioning", value=enable_thin_provisioning, expected_type=type_hints["enable_thin_provisioning"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_pool_id", value=network_pool_id, expected_type=type_hints["network_pool_id"])
            check_type(argname="argument nic_quota", value=nic_quota, expected_type=type_hints["nic_quota"])
            check_type(argname="argument provisioned_network_quota", value=provisioned_network_quota, expected_type=type_hints["provisioned_network_quota"])
            check_type(argname="argument readable_by_org_ids", value=readable_by_org_ids, expected_type=type_hints["readable_by_org_ids"])
            check_type(argname="argument tenant_description", value=tenant_description, expected_type=type_hints["tenant_description"])
            check_type(argname="argument vm_quota", value=vm_quota, expected_type=type_hints["vm_quota"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocation_model": allocation_model,
            "compute_configuration": compute_configuration,
            "name": name,
            "provider_vdc": provider_vdc,
            "storage_profile": storage_profile,
            "tenant_name": tenant_name,
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
        if edge_gateway is not None:
            self._values["edge_gateway"] = edge_gateway
        if enable_fast_provisioning is not None:
            self._values["enable_fast_provisioning"] = enable_fast_provisioning
        if enable_thin_provisioning is not None:
            self._values["enable_thin_provisioning"] = enable_thin_provisioning
        if id is not None:
            self._values["id"] = id
        if network_pool_id is not None:
            self._values["network_pool_id"] = network_pool_id
        if nic_quota is not None:
            self._values["nic_quota"] = nic_quota
        if provisioned_network_quota is not None:
            self._values["provisioned_network_quota"] = provisioned_network_quota
        if readable_by_org_ids is not None:
            self._values["readable_by_org_ids"] = readable_by_org_ids
        if tenant_description is not None:
            self._values["tenant_description"] = tenant_description
        if vm_quota is not None:
            self._values["vm_quota"] = vm_quota

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
        '''Allocation model that the VDCs instantiated from this template will use.

        Must be one of: 'AllocationVApp', 'AllocationPool', 'ReservationPool' or 'Flex'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#allocation_model OrgVdcTemplate#allocation_model}
        '''
        result = self._values.get("allocation_model")
        assert result is not None, "Required property 'allocation_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_configuration(self) -> OrgVdcTemplateComputeConfiguration:
        '''compute_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#compute_configuration OrgVdcTemplate#compute_configuration}
        '''
        result = self._values.get("compute_configuration")
        assert result is not None, "Required property 'compute_configuration' is missing"
        return typing.cast(OrgVdcTemplateComputeConfiguration, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the VDC Template as seen by the System administrator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#name OrgVdcTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_vdc(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcTemplateProviderVdc"]]:
        '''provider_vdc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#provider_vdc OrgVdcTemplate#provider_vdc}
        '''
        result = self._values.get("provider_vdc")
        assert result is not None, "Required property 'provider_vdc' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcTemplateProviderVdc"]], result)

    @builtins.property
    def storage_profile(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcTemplateStorageProfile"]]:
        '''storage_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#storage_profile OrgVdcTemplate#storage_profile}
        '''
        result = self._values.get("storage_profile")
        assert result is not None, "Required property 'storage_profile' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgVdcTemplateStorageProfile"]], result)

    @builtins.property
    def tenant_name(self) -> builtins.str:
        '''Name of the VDC Template as seen by the tenants (organizations).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#tenant_name OrgVdcTemplate#tenant_name}
        '''
        result = self._values.get("tenant_name")
        assert result is not None, "Required property 'tenant_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the VDC Template as seen by the System administrator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#description OrgVdcTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_gateway(self) -> typing.Optional["OrgVdcTemplateEdgeGateway"]:
        '''edge_gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#edge_gateway OrgVdcTemplate#edge_gateway}
        '''
        result = self._values.get("edge_gateway")
        return typing.cast(typing.Optional["OrgVdcTemplateEdgeGateway"], result)

    @builtins.property
    def enable_fast_provisioning(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', the VDCs instantiated from this template will have Fast provisioning enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#enable_fast_provisioning OrgVdcTemplate#enable_fast_provisioning}
        '''
        result = self._values.get("enable_fast_provisioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_thin_provisioning(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', the VDCs instantiated from this template will have Thin provisioning enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#enable_thin_provisioning OrgVdcTemplate#enable_thin_provisioning}
        '''
        result = self._values.get("enable_thin_provisioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#id OrgVdcTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_pool_id(self) -> typing.Optional[builtins.str]:
        '''If set, specifies the Network pool for the instantiated VDCs. Otherwise, it is automatically chosen.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#network_pool_id OrgVdcTemplate#network_pool_id}
        '''
        result = self._values.get("network_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_quota(self) -> typing.Optional[jsii.Number]:
        '''Quota for the NICs of the instantiated VDCs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#nic_quota OrgVdcTemplate#nic_quota}
        '''
        result = self._values.get("nic_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_network_quota(self) -> typing.Optional[jsii.Number]:
        '''Quota for the provisioned networks of the instantiated VDCs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#provisioned_network_quota OrgVdcTemplate#provisioned_network_quota}
        '''
        result = self._values.get("provisioned_network_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def readable_by_org_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IDs of the Organizations that will be able to view and instantiate this VDC template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#readable_by_org_ids OrgVdcTemplate#readable_by_org_ids}
        '''
        result = self._values.get("readable_by_org_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tenant_description(self) -> typing.Optional[builtins.str]:
        '''Description of the VDC Template as seen by the tenants (organizations).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#tenant_description OrgVdcTemplate#tenant_description}
        '''
        result = self._values.get("tenant_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_quota(self) -> typing.Optional[jsii.Number]:
        '''Quota for the VMs of the instantiated VDCs. 0 means unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#vm_quota OrgVdcTemplate#vm_quota}
        '''
        result = self._values.get("vm_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateEdgeGateway",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "routed_network_gateway_cidr": "routedNetworkGatewayCidr",
        "routed_network_name": "routedNetworkName",
        "description": "description",
        "ip_allocation_count": "ipAllocationCount",
        "routed_network_description": "routedNetworkDescription",
        "static_ip_pool": "staticIpPool",
    },
)
class OrgVdcTemplateEdgeGateway:
    def __init__(
        self,
        *,
        name: builtins.str,
        routed_network_gateway_cidr: builtins.str,
        routed_network_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        ip_allocation_count: typing.Optional[jsii.Number] = None,
        routed_network_description: typing.Optional[builtins.str] = None,
        static_ip_pool: typing.Optional[typing.Union["OrgVdcTemplateEdgeGatewayStaticIpPool", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#name OrgVdcTemplate#name}
        :param routed_network_gateway_cidr: CIDR of the Edge Gateway for the created routed network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_gateway_cidr OrgVdcTemplate#routed_network_gateway_cidr}
        :param routed_network_name: Name of the routed network to create with the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_name OrgVdcTemplate#routed_network_name}
        :param description: Description of the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#description OrgVdcTemplate#description}
        :param ip_allocation_count: Allocated IPs for the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#ip_allocation_count OrgVdcTemplate#ip_allocation_count}
        :param routed_network_description: Description of the routed network to create with the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_description OrgVdcTemplate#routed_network_description}
        :param static_ip_pool: static_ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#static_ip_pool OrgVdcTemplate#static_ip_pool}
        '''
        if isinstance(static_ip_pool, dict):
            static_ip_pool = OrgVdcTemplateEdgeGatewayStaticIpPool(**static_ip_pool)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7678fa92c99ac5639d19491a1db0a00b52612625dd302005060fa746c0d3d96c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument routed_network_gateway_cidr", value=routed_network_gateway_cidr, expected_type=type_hints["routed_network_gateway_cidr"])
            check_type(argname="argument routed_network_name", value=routed_network_name, expected_type=type_hints["routed_network_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ip_allocation_count", value=ip_allocation_count, expected_type=type_hints["ip_allocation_count"])
            check_type(argname="argument routed_network_description", value=routed_network_description, expected_type=type_hints["routed_network_description"])
            check_type(argname="argument static_ip_pool", value=static_ip_pool, expected_type=type_hints["static_ip_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "routed_network_gateway_cidr": routed_network_gateway_cidr,
            "routed_network_name": routed_network_name,
        }
        if description is not None:
            self._values["description"] = description
        if ip_allocation_count is not None:
            self._values["ip_allocation_count"] = ip_allocation_count
        if routed_network_description is not None:
            self._values["routed_network_description"] = routed_network_description
        if static_ip_pool is not None:
            self._values["static_ip_pool"] = static_ip_pool

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#name OrgVdcTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routed_network_gateway_cidr(self) -> builtins.str:
        '''CIDR of the Edge Gateway for the created routed network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_gateway_cidr OrgVdcTemplate#routed_network_gateway_cidr}
        '''
        result = self._values.get("routed_network_gateway_cidr")
        assert result is not None, "Required property 'routed_network_gateway_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routed_network_name(self) -> builtins.str:
        '''Name of the routed network to create with the Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_name OrgVdcTemplate#routed_network_name}
        '''
        result = self._values.get("routed_network_name")
        assert result is not None, "Required property 'routed_network_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#description OrgVdcTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_allocation_count(self) -> typing.Optional[jsii.Number]:
        '''Allocated IPs for the Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#ip_allocation_count OrgVdcTemplate#ip_allocation_count}
        '''
        result = self._values.get("ip_allocation_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def routed_network_description(self) -> typing.Optional[builtins.str]:
        '''Description of the routed network to create with the Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#routed_network_description OrgVdcTemplate#routed_network_description}
        '''
        result = self._values.get("routed_network_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_ip_pool(
        self,
    ) -> typing.Optional["OrgVdcTemplateEdgeGatewayStaticIpPool"]:
        '''static_ip_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#static_ip_pool OrgVdcTemplate#static_ip_pool}
        '''
        result = self._values.get("static_ip_pool")
        return typing.cast(typing.Optional["OrgVdcTemplateEdgeGatewayStaticIpPool"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcTemplateEdgeGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcTemplateEdgeGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateEdgeGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ae99ad63cee79b2a2c74ba88f4f515eb35a25df87c86e8ac62bbe51095cb766)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStaticIpPool")
    def put_static_ip_pool(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: End address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#end_address OrgVdcTemplate#end_address}
        :param start_address: Start address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#start_address OrgVdcTemplate#start_address}
        '''
        value = OrgVdcTemplateEdgeGatewayStaticIpPool(
            end_address=end_address, start_address=start_address
        )

        return typing.cast(None, jsii.invoke(self, "putStaticIpPool", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetIpAllocationCount")
    def reset_ip_allocation_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAllocationCount", []))

    @jsii.member(jsii_name="resetRoutedNetworkDescription")
    def reset_routed_network_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutedNetworkDescription", []))

    @jsii.member(jsii_name="resetStaticIpPool")
    def reset_static_ip_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticIpPool", []))

    @builtins.property
    @jsii.member(jsii_name="staticIpPool")
    def static_ip_pool(self) -> "OrgVdcTemplateEdgeGatewayStaticIpPoolOutputReference":
        return typing.cast("OrgVdcTemplateEdgeGatewayStaticIpPoolOutputReference", jsii.get(self, "staticIpPool"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAllocationCountInput")
    def ip_allocation_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ipAllocationCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="routedNetworkDescriptionInput")
    def routed_network_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routedNetworkDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="routedNetworkGatewayCidrInput")
    def routed_network_gateway_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routedNetworkGatewayCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="routedNetworkNameInput")
    def routed_network_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routedNetworkNameInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpPoolInput")
    def static_ip_pool_input(
        self,
    ) -> typing.Optional["OrgVdcTemplateEdgeGatewayStaticIpPool"]:
        return typing.cast(typing.Optional["OrgVdcTemplateEdgeGatewayStaticIpPool"], jsii.get(self, "staticIpPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8e186adba2c0fc88396f62da62abe696c532aa3bdd0e707db970625ac45295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="ipAllocationCount")
    def ip_allocation_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ipAllocationCount"))

    @ip_allocation_count.setter
    def ip_allocation_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10cc375471b1198a09adee5190ee1004d2848058d749f2582969f67fcb598675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAllocationCount", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42fd438ddb388c6819714c0caca84081bf8fb1b56f68bed2d024987887025c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="routedNetworkDescription")
    def routed_network_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routedNetworkDescription"))

    @routed_network_description.setter
    def routed_network_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19689d46969bf42577eaee15310b8014e1f52df802d2f343d304febac0db9a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routedNetworkDescription", value)

    @builtins.property
    @jsii.member(jsii_name="routedNetworkGatewayCidr")
    def routed_network_gateway_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routedNetworkGatewayCidr"))

    @routed_network_gateway_cidr.setter
    def routed_network_gateway_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d1543954e3a0df62c334140c03c74f19536945eb76e9c893f551f913e4675d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routedNetworkGatewayCidr", value)

    @builtins.property
    @jsii.member(jsii_name="routedNetworkName")
    def routed_network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routedNetworkName"))

    @routed_network_name.setter
    def routed_network_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6f05840a92a299313facfabfb23db5b5009d026d8d8d3fcd927cc4aac31173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routedNetworkName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgVdcTemplateEdgeGateway]:
        return typing.cast(typing.Optional[OrgVdcTemplateEdgeGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgVdcTemplateEdgeGateway]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbabcb7311c75c8fe3d3afd248ea8c463ddd0b6b1fe8ba8f012f6a7ff3e1f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateEdgeGatewayStaticIpPool",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class OrgVdcTemplateEdgeGatewayStaticIpPool:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: End address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#end_address OrgVdcTemplate#end_address}
        :param start_address: Start address of the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#start_address OrgVdcTemplate#start_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15427aac38b04c0102e7ad155ef7f62d455393378c9cc548e1ab25de60d38291)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''End address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#end_address OrgVdcTemplate#end_address}
        '''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Start address of the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#start_address OrgVdcTemplate#start_address}
        '''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcTemplateEdgeGatewayStaticIpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcTemplateEdgeGatewayStaticIpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateEdgeGatewayStaticIpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9b15cdbd2518690724a37ea10f16ca4454c8b4344a85b03ba65fddfab817443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endAddressInput")
    def end_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="startAddressInput")
    def start_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="endAddress")
    def end_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endAddress"))

    @end_address.setter
    def end_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2e051415c8bba4bf9c5c232fb88a4354503b8a44309672a9e4a08c048e074e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c27b7e8ae1b5950720e9b68e12d28ba8f88997948492ced6338e15e03b2b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgVdcTemplateEdgeGatewayStaticIpPool]:
        return typing.cast(typing.Optional[OrgVdcTemplateEdgeGatewayStaticIpPool], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgVdcTemplateEdgeGatewayStaticIpPool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12384520ea015da93c4fa20fb86d1fb31276cda046e18ce175e8bf4f72879106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateProviderVdc",
    jsii_struct_bases=[],
    name_mapping={
        "external_network_id": "externalNetworkId",
        "id": "id",
        "gateway_edge_cluster_id": "gatewayEdgeClusterId",
        "services_edge_cluster_id": "servicesEdgeClusterId",
    },
)
class OrgVdcTemplateProviderVdc:
    def __init__(
        self,
        *,
        external_network_id: builtins.str,
        id: builtins.str,
        gateway_edge_cluster_id: typing.Optional[builtins.str] = None,
        services_edge_cluster_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_network_id: ID of the External network that the VDCs instantiated from this template will use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#external_network_id OrgVdcTemplate#external_network_id}
        :param id: ID of Provider VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#id OrgVdcTemplate#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param gateway_edge_cluster_id: ID of the Edge Cluster that the VDCs instantiated from this template will use with the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#gateway_edge_cluster_id OrgVdcTemplate#gateway_edge_cluster_id}
        :param services_edge_cluster_id: ID of the Edge Cluster that the VDCs instantiated from this template will use for services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#services_edge_cluster_id OrgVdcTemplate#services_edge_cluster_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088a82c7d470e014333ebd6a33f55980c76a600672f4233694d843839f3b99d2)
            check_type(argname="argument external_network_id", value=external_network_id, expected_type=type_hints["external_network_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument gateway_edge_cluster_id", value=gateway_edge_cluster_id, expected_type=type_hints["gateway_edge_cluster_id"])
            check_type(argname="argument services_edge_cluster_id", value=services_edge_cluster_id, expected_type=type_hints["services_edge_cluster_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "external_network_id": external_network_id,
            "id": id,
        }
        if gateway_edge_cluster_id is not None:
            self._values["gateway_edge_cluster_id"] = gateway_edge_cluster_id
        if services_edge_cluster_id is not None:
            self._values["services_edge_cluster_id"] = services_edge_cluster_id

    @builtins.property
    def external_network_id(self) -> builtins.str:
        '''ID of the External network that the VDCs instantiated from this template will use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#external_network_id OrgVdcTemplate#external_network_id}
        '''
        result = self._values.get("external_network_id")
        assert result is not None, "Required property 'external_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''ID of Provider VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#id OrgVdcTemplate#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway_edge_cluster_id(self) -> typing.Optional[builtins.str]:
        '''ID of the Edge Cluster that the VDCs instantiated from this template will use with the Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#gateway_edge_cluster_id OrgVdcTemplate#gateway_edge_cluster_id}
        '''
        result = self._values.get("gateway_edge_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def services_edge_cluster_id(self) -> typing.Optional[builtins.str]:
        '''ID of the Edge Cluster that the VDCs instantiated from this template will use for services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#services_edge_cluster_id OrgVdcTemplate#services_edge_cluster_id}
        '''
        result = self._values.get("services_edge_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcTemplateProviderVdc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcTemplateProviderVdcList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateProviderVdcList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f031a7627a113516c606c771fe791ec486be7342f42d89d94de2670b130ade1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrgVdcTemplateProviderVdcOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9bf77cc2a907643506c9690b94a0296964db29e9eb615c098a5dcb70628da1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrgVdcTemplateProviderVdcOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f49b18e8ec95d930e9b6327682ce1e051bf0595aed9cc326065c5730272340)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bbd63ebc7272dd688716f528985c6519f0b39b35b37e73fd46b4bf19cd64413)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c1e037a1b1fa7b2deb883ed9e8904e0aa28f3c68230b7fdf82e57daf0ed706f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcTemplateProviderVdc]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcTemplateProviderVdc]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcTemplateProviderVdc]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8c853986fb84baf57ad3c61ddc92df3ccd81064a1f376a65e2f921f33d3fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrgVdcTemplateProviderVdcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateProviderVdcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b51b3249913402c6661b41acc0d62b6962af4b3ea043fc40c49fe64ae61202ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGatewayEdgeClusterId")
    def reset_gateway_edge_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayEdgeClusterId", []))

    @jsii.member(jsii_name="resetServicesEdgeClusterId")
    def reset_services_edge_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicesEdgeClusterId", []))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkIdInput")
    def external_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayEdgeClusterIdInput")
    def gateway_edge_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayEdgeClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesEdgeClusterIdInput")
    def services_edge_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicesEdgeClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkId")
    def external_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalNetworkId"))

    @external_network_id.setter
    def external_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f7ae334ac025c60d20d13c126effaf90193d6c2e3f67102e28c522a4e24974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="gatewayEdgeClusterId")
    def gateway_edge_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayEdgeClusterId"))

    @gateway_edge_cluster_id.setter
    def gateway_edge_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a16ed5af54bea129f9aaebd93cf5da24a7cb6b1657fb60969dbfa28d0c49be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayEdgeClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b425e57ae35c06ea6a152c9d7cff9c9bcac3c9d00fad6e6b5bf2bc212917f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="servicesEdgeClusterId")
    def services_edge_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicesEdgeClusterId"))

    @services_edge_cluster_id.setter
    def services_edge_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__451773149f4b560aff4e398535f5a0e7a2ab7ca1094e24b5766d93252170e425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesEdgeClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcTemplateProviderVdc]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcTemplateProviderVdc]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcTemplateProviderVdc]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b380be9b5299c8e74111ae82a929480538b91a639e9c8bfbcaef1f169ca8a7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateStorageProfile",
    jsii_struct_bases=[],
    name_mapping={"default": "default", "limit": "limit", "name": "name"},
)
class OrgVdcTemplateStorageProfile:
    def __init__(
        self,
        *,
        default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        limit: jsii.Number,
        name: builtins.str,
    ) -> None:
        '''
        :param default: True if this is default storage profile for the VDCs instantiated from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#default OrgVdcTemplate#default}
        :param limit: Storage limit for the VDCs instantiated from this template, in Megabytes. 0 means unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#limit OrgVdcTemplate#limit}
        :param name: Name of Provider VDC storage profile to use for the VDCs instantiated from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#name OrgVdcTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5e2bf8b54b3a89bfdb040e0d760aa03d12af8d6da38330059755b3c3210eb5)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default": default,
            "limit": limit,
            "name": name,
        }

    @builtins.property
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''True if this is default storage profile for the VDCs instantiated from this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#default OrgVdcTemplate#default}
        '''
        result = self._values.get("default")
        assert result is not None, "Required property 'default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def limit(self) -> jsii.Number:
        '''Storage limit for the VDCs instantiated from this template, in Megabytes. 0 means unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#limit OrgVdcTemplate#limit}
        '''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of Provider VDC storage profile to use for the VDCs instantiated from this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_template#name OrgVdcTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcTemplateStorageProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgVdcTemplateStorageProfileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateStorageProfileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffe4d3d2d6549d41e31341b7c0bcb918f37ef02e8cf5ad87443182b73903258d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrgVdcTemplateStorageProfileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de2decf4eb3d591b2179b339f31f2af40b047ace2e34d3104c283a4eb9ffcae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrgVdcTemplateStorageProfileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1f93b15593f22544b7c3e5329d66248360a4855eebef8fd934d23461635a02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cefe20ca42e605934331b2fadbd613b07308f51d74c6113be1d1a170c9579a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a16312def982bfe470df2d62659ea88da1f565b41b2fecdc5f8f87c0472de9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcTemplateStorageProfile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcTemplateStorageProfile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcTemplateStorageProfile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33fef3ef3516275d62e2c712bfc1db55c7209467ea8fae9a82ddc9a666a8abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrgVdcTemplateStorageProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcTemplate.OrgVdcTemplateStorageProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdddd05d526e8ec0f8dc3b95707cb5b94cbb9d7761046083deeda9dfb18086cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__10c25fd6feb7f839f3b8e979551b03400d74492126b05664eca353168e4abaac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc93c8d8702110715ec4989703cb33858d9120abed1bbfe18ca2f277e2823e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea82568f58e221ec20fd4a462ea178743d10a8d2c1cffaafd0d1120a3b52d3e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcTemplateStorageProfile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcTemplateStorageProfile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcTemplateStorageProfile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2bb57618c86cce81653f1b88e39e00c3cec4f7af79718acdf4d8d660df60af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OrgVdcTemplate",
    "OrgVdcTemplateComputeConfiguration",
    "OrgVdcTemplateComputeConfigurationOutputReference",
    "OrgVdcTemplateConfig",
    "OrgVdcTemplateEdgeGateway",
    "OrgVdcTemplateEdgeGatewayOutputReference",
    "OrgVdcTemplateEdgeGatewayStaticIpPool",
    "OrgVdcTemplateEdgeGatewayStaticIpPoolOutputReference",
    "OrgVdcTemplateProviderVdc",
    "OrgVdcTemplateProviderVdcList",
    "OrgVdcTemplateProviderVdcOutputReference",
    "OrgVdcTemplateStorageProfile",
    "OrgVdcTemplateStorageProfileList",
    "OrgVdcTemplateStorageProfileOutputReference",
]

publication.publish()

def _typecheckingstub__57e68d8f298a6183539c7a8eb83fd836ba27b9694a7f429e08075fe61c679cfc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    allocation_model: builtins.str,
    compute_configuration: typing.Union[OrgVdcTemplateComputeConfiguration, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    provider_vdc: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcTemplateProviderVdc, typing.Dict[builtins.str, typing.Any]]]],
    storage_profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcTemplateStorageProfile, typing.Dict[builtins.str, typing.Any]]]],
    tenant_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    edge_gateway: typing.Optional[typing.Union[OrgVdcTemplateEdgeGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_fast_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_thin_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    network_pool_id: typing.Optional[builtins.str] = None,
    nic_quota: typing.Optional[jsii.Number] = None,
    provisioned_network_quota: typing.Optional[jsii.Number] = None,
    readable_by_org_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tenant_description: typing.Optional[builtins.str] = None,
    vm_quota: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__62deb087bc340246451045ab540e92cc1787143ec35499121bc4e9637167d78d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad8b7fce3acda2ab35ce37ef2823cfc0990a50e18f684fb7a9ea51c838d4961(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcTemplateProviderVdc, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67bedaae0d354ee291afe1270888c97c7700b0eb594080c04293d31dd7541c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcTemplateStorageProfile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68483bc7cc0da51f01845969bfdf54f7c72f658367fe3ed9ab8593b70568d3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d96b27fcd02a40bd8f09831d14014058c856f0d468522906a8ebc27f54a8342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c770e793786f562346029f1f2d40034507e603e917eb879431d25de6f46489e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b9fcd6b273b615e79b49ecd8aab36482678a214cef9ae4a279dbbeafb11dac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0386159b795efd09d8b808ed495a0d724248adf47c46a19c8074121282f345b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608906e6020beaaa956c7332eafa293ccc8079564d655dcb7eed0ac6d952221b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eafad9f0eba2d76dd2b1d22138635b8684f3896cb949b4189ce1ef49de330c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc1e1850a25d70de79f8357072a9870dd837eb8c34bc922b18ab8489f8104a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879af79272383d428ba9204c8c6234736b6f1ac5b37cc6b429c268452267fb8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7215639aad0be26e25737fff1d17664d29ef800227471a4692c77f62c15b49ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db0074b2f63bbb8a3f34382a5b1a104dac094be0ae64502958fce2007017ae5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17b720bc8b3413d4aa99603641bcc6066cb0752e3aa7f8e10cf7658f1de4a0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec163ebd228a7099edce3012ac8147caaad554dbd666fc4a16337106dfe36b8c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27133e1d33f3e9530579a849870026e252978f425f3a40d77742e7ad2c49e310(
    *,
    cpu_allocated: typing.Optional[jsii.Number] = None,
    cpu_guaranteed: typing.Optional[jsii.Number] = None,
    cpu_limit: typing.Optional[jsii.Number] = None,
    cpu_speed: typing.Optional[jsii.Number] = None,
    elasticity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_vm_memory_overhead: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_allocated: typing.Optional[jsii.Number] = None,
    memory_guaranteed: typing.Optional[jsii.Number] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9476ab5847839762e517b8cb58e22aac0f20df7f4baa725a5ba64ab4b820866d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6916a2a052735a09b6abe7d8f268b2fb853627bacb3182590519e578532aebab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0db1cbf865d42e0faa0aba97aa65c104bfa81e98019e3769db2828986a91dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749f28456d91ada251902319aed97dd500845d98489cee1399b976a0e74abb9f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48df4bf12eb660bc46fc2c96684379aa2468a427bb76312f341baad3ce64970(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b101d718cea5981516978c1ebad960764e0285a0b42ca759db2a79635076c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50dd46defc2dafe56087ff6e6c8e77e0413d664d2b5198b1e6f39f9b1ad7a9f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85eda36c191759c1045e6f931efb1643cd15a35da3eba280d8cff2a27ae783f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07c3bcd964b106d805e691d0d7c37195379ab303a1091b6eb0cced82ebdb45b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3c57f5df0b38c98040f9e2c97c131227f9c9cabd39cdfdd102b4fb65402607(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22af6783b6c6486e3d19e74abb8a18ab50c1a595f3a027901ae6e39aed178467(
    value: typing.Optional[OrgVdcTemplateComputeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a54fa899038074c744dbecb75bfecc6dadf8a099fc8629c7807f7de92369d5e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allocation_model: builtins.str,
    compute_configuration: typing.Union[OrgVdcTemplateComputeConfiguration, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    provider_vdc: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcTemplateProviderVdc, typing.Dict[builtins.str, typing.Any]]]],
    storage_profile: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgVdcTemplateStorageProfile, typing.Dict[builtins.str, typing.Any]]]],
    tenant_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    edge_gateway: typing.Optional[typing.Union[OrgVdcTemplateEdgeGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_fast_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_thin_provisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    network_pool_id: typing.Optional[builtins.str] = None,
    nic_quota: typing.Optional[jsii.Number] = None,
    provisioned_network_quota: typing.Optional[jsii.Number] = None,
    readable_by_org_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tenant_description: typing.Optional[builtins.str] = None,
    vm_quota: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7678fa92c99ac5639d19491a1db0a00b52612625dd302005060fa746c0d3d96c(
    *,
    name: builtins.str,
    routed_network_gateway_cidr: builtins.str,
    routed_network_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    ip_allocation_count: typing.Optional[jsii.Number] = None,
    routed_network_description: typing.Optional[builtins.str] = None,
    static_ip_pool: typing.Optional[typing.Union[OrgVdcTemplateEdgeGatewayStaticIpPool, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae99ad63cee79b2a2c74ba88f4f515eb35a25df87c86e8ac62bbe51095cb766(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8e186adba2c0fc88396f62da62abe696c532aa3bdd0e707db970625ac45295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cc375471b1198a09adee5190ee1004d2848058d749f2582969f67fcb598675(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fd438ddb388c6819714c0caca84081bf8fb1b56f68bed2d024987887025c6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19689d46969bf42577eaee15310b8014e1f52df802d2f343d304febac0db9a67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d1543954e3a0df62c334140c03c74f19536945eb76e9c893f551f913e4675d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6f05840a92a299313facfabfb23db5b5009d026d8d8d3fcd927cc4aac31173(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbabcb7311c75c8fe3d3afd248ea8c463ddd0b6b1fe8ba8f012f6a7ff3e1f78(
    value: typing.Optional[OrgVdcTemplateEdgeGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15427aac38b04c0102e7ad155ef7f62d455393378c9cc548e1ab25de60d38291(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b15cdbd2518690724a37ea10f16ca4454c8b4344a85b03ba65fddfab817443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2e051415c8bba4bf9c5c232fb88a4354503b8a44309672a9e4a08c048e074e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c27b7e8ae1b5950720e9b68e12d28ba8f88997948492ced6338e15e03b2b32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12384520ea015da93c4fa20fb86d1fb31276cda046e18ce175e8bf4f72879106(
    value: typing.Optional[OrgVdcTemplateEdgeGatewayStaticIpPool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088a82c7d470e014333ebd6a33f55980c76a600672f4233694d843839f3b99d2(
    *,
    external_network_id: builtins.str,
    id: builtins.str,
    gateway_edge_cluster_id: typing.Optional[builtins.str] = None,
    services_edge_cluster_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f031a7627a113516c606c771fe791ec486be7342f42d89d94de2670b130ade1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9bf77cc2a907643506c9690b94a0296964db29e9eb615c098a5dcb70628da1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f49b18e8ec95d930e9b6327682ce1e051bf0595aed9cc326065c5730272340(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbd63ebc7272dd688716f528985c6519f0b39b35b37e73fd46b4bf19cd64413(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1e037a1b1fa7b2deb883ed9e8904e0aa28f3c68230b7fdf82e57daf0ed706f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8c853986fb84baf57ad3c61ddc92df3ccd81064a1f376a65e2f921f33d3fd9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcTemplateProviderVdc]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51b3249913402c6661b41acc0d62b6962af4b3ea043fc40c49fe64ae61202ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f7ae334ac025c60d20d13c126effaf90193d6c2e3f67102e28c522a4e24974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a16ed5af54bea129f9aaebd93cf5da24a7cb6b1657fb60969dbfa28d0c49be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b425e57ae35c06ea6a152c9d7cff9c9bcac3c9d00fad6e6b5bf2bc212917f5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451773149f4b560aff4e398535f5a0e7a2ab7ca1094e24b5766d93252170e425(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b380be9b5299c8e74111ae82a929480538b91a639e9c8bfbcaef1f169ca8a7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcTemplateProviderVdc]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5e2bf8b54b3a89bfdb040e0d760aa03d12af8d6da38330059755b3c3210eb5(
    *,
    default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    limit: jsii.Number,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe4d3d2d6549d41e31341b7c0bcb918f37ef02e8cf5ad87443182b73903258d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de2decf4eb3d591b2179b339f31f2af40b047ace2e34d3104c283a4eb9ffcae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1f93b15593f22544b7c3e5329d66248360a4855eebef8fd934d23461635a02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cefe20ca42e605934331b2fadbd613b07308f51d74c6113be1d1a170c9579a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16312def982bfe470df2d62659ea88da1f565b41b2fecdc5f8f87c0472de9f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33fef3ef3516275d62e2c712bfc1db55c7209467ea8fae9a82ddc9a666a8abf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgVdcTemplateStorageProfile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdddd05d526e8ec0f8dc3b95707cb5b94cbb9d7761046083deeda9dfb18086cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c25fd6feb7f839f3b8e979551b03400d74492126b05664eca353168e4abaac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc93c8d8702110715ec4989703cb33858d9120abed1bbfe18ca2f277e2823e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea82568f58e221ec20fd4a462ea178743d10a8d2c1cffaafd0d1120a3b52d3e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bb57618c86cce81653f1b88e39e00c3cec4f7af79718acdf4d8d660df60af7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgVdcTemplateStorageProfile]],
) -> None:
    """Type checking stubs"""
    pass
