'''
# `vcd_vapp_vm`

Refer to the Terraform Registry for docs: [`vcd_vapp_vm`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm).
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


class VappVm(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVm",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm vcd_vapp_vm}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        vapp_name: builtins.str,
        accept_all_eulas: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        boot_image: typing.Optional[builtins.str] = None,
        boot_image_id: typing.Optional[builtins.str] = None,
        boot_options: typing.Optional[typing.Union["VappVmBootOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        catalog_name: typing.Optional[builtins.str] = None,
        computer_name: typing.Optional[builtins.str] = None,
        consolidate_disks_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        copy_from_vm_id: typing.Optional[builtins.str] = None,
        cpu_cores: typing.Optional[jsii.Number] = None,
        cpu_hot_add_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_limit: typing.Optional[jsii.Number] = None,
        cpu_priority: typing.Optional[builtins.str] = None,
        cpu_reservation: typing.Optional[jsii.Number] = None,
        cpus: typing.Optional[jsii.Number] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        customization: typing.Optional[typing.Union["VappVmCustomization", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        expose_hardware_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        firmware: typing.Optional[builtins.str] = None,
        guest_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        hardware_version: typing.Optional[builtins.str] = None,
        href: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_hot_add_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        memory_priority: typing.Optional[builtins.str] = None,
        memory_reservation: typing.Optional[jsii.Number] = None,
        memory_shares: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_dhcp_wait_seconds: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        override_template_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmOverrideTemplateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement_policy_id: typing.Optional[builtins.str] = None,
        power_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_update_power_off: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        set_extra_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmSetExtraConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sizing_policy_id: typing.Optional[builtins.str] = None,
        storage_profile: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
        vapp_template_id: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        vm_name_in_template: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm vcd_vapp_vm} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A name for the VM, unique within the vApp. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#name VappVm#name}
        :param vapp_name: The vApp this VM belongs to - Required, unless it is a standalone VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vapp_name VappVm#vapp_name}
        :param accept_all_eulas: Automatically accept EULA if OVA has it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#accept_all_eulas VappVm#accept_all_eulas}
        :param boot_image: Media name to add as boot image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_image VappVm#boot_image}
        :param boot_image_id: The URN of the media to use as boot image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_image_id VappVm#boot_image_id}
        :param boot_options: boot_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_options VappVm#boot_options}
        :param catalog_name: The catalog name in which to find the given vApp Template or media for boot_image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#catalog_name VappVm#catalog_name}
        :param computer_name: Computer name to assign to this virtual machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#computer_name VappVm#computer_name}
        :param consolidate_disks_on_create: Consolidates disks during creation and allows to change disk size using 'override_template_disk' in fast provisioned VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#consolidate_disks_on_create VappVm#consolidate_disks_on_create}
        :param copy_from_vm_id: Source VM that should be copied from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#copy_from_vm_id VappVm#copy_from_vm_id}
        :param cpu_cores: The number of cores per socket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_cores VappVm#cpu_cores}
        :param cpu_hot_add_enabled: True if the virtual machine supports addition of virtual CPUs while powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_hot_add_enabled VappVm#cpu_hot_add_enabled}
        :param cpu_limit: The limit for how much of CPU can be consumed on the underlying virtualization infrastructure. This is only valid when the resource allocation is not unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_limit VappVm#cpu_limit}
        :param cpu_priority: Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_priority VappVm#cpu_priority}
        :param cpu_reservation: The amount of MHz reservation on the underlying virtualization infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_reservation VappVm#cpu_reservation}
        :param cpus: The number of virtual CPUs to allocate to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpus VappVm#cpus}
        :param cpu_shares: Custom priority for the resource. This is a read-only, unless the ``cpu_priority`` is CUSTOM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_shares VappVm#cpu_shares}
        :param customization: customization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#customization VappVm#customization}
        :param description: The VM description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#description VappVm#description}
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#disk VappVm#disk}
        :param expose_hardware_virtualization: Expose hardware-assisted CPU virtualization to guest OS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#expose_hardware_virtualization VappVm#expose_hardware_virtualization}
        :param firmware: Firmware of the VM. Can be either EFI or BIOS, availabilitydepending on the os_type argument. If unset, is set to 'bios' by default. Changing the value when ``power_on`` is set to true, will cause a reboot of the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#firmware VappVm#firmware}
        :param guest_properties: Key/value settings for guest properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#guest_properties VappVm#guest_properties}
        :param hardware_version: Virtual Hardware Version (e.g.``vmx-14``, ``vmx-13``, ``vmx-12``, etc.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#hardware_version VappVm#hardware_version}
        :param href: VM Hyper Reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#href VappVm#href}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#id VappVm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param memory: The amount of RAM (in MB) to allocate to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory VappVm#memory}
        :param memory_hot_add_enabled: True if the virtual machine supports addition of memory while powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_hot_add_enabled VappVm#memory_hot_add_enabled}
        :param memory_limit: The limit for how much of memory can be consumed on the underlying virtualization infrastructure. This is only valid when the resource allocation is not unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_limit VappVm#memory_limit}
        :param memory_priority: Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_priority VappVm#memory_priority}
        :param memory_reservation: The amount of RAM (in MB) reservation on the underlying virtualization infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_reservation VappVm#memory_reservation}
        :param memory_shares: Custom priority for the resource. This is a read-only, unless the ``memory_priority`` is CUSTOM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_shares VappVm#memory_shares}
        :param metadata: Key value map of metadata to assign to this VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#metadata VappVm#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#metadata_entry VappVm#metadata_entry}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#network VappVm#network}
        :param network_dhcp_wait_seconds: Optional number of seconds to try and wait for DHCP IP (valid for 'network' block only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#network_dhcp_wait_seconds VappVm#network_dhcp_wait_seconds}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#org VappVm#org}
        :param os_type: Operating System type. Possible values can be found in documentation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#os_type VappVm#os_type}
        :param override_template_disk: override_template_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#override_template_disk VappVm#override_template_disk}
        :param placement_policy_id: VM placement policy ID. Has to be assigned to Org VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#placement_policy_id VappVm#placement_policy_id}
        :param power_on: A boolean value stating if this VM should be powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#power_on VappVm#power_on}
        :param prevent_update_power_off: True if the update of resource should fail when virtual machine power off needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#prevent_update_power_off VappVm#prevent_update_power_off}
        :param security_tags: Security tags to assign to this VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#security_tags VappVm#security_tags}
        :param set_extra_config: set_extra_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#set_extra_config VappVm#set_extra_config}
        :param sizing_policy_id: VM sizing policy ID. Has to be assigned to Org VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#sizing_policy_id VappVm#sizing_policy_id}
        :param storage_profile: Storage profile to override the default one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#storage_profile VappVm#storage_profile}
        :param template_name: The name of the vApp Template to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#template_name VappVm#template_name}
        :param vapp_template_id: The URN of the vApp Template to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vapp_template_id VappVm#vapp_template_id}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vdc VappVm#vdc}
        :param vm_name_in_template: The name of the VM in vApp Template to use. In cases when vApp template has more than one VM Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vm_name_in_template VappVm#vm_name_in_template}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b761d3283e39573700f0cc2d03f356fc8564c81cb1932738e8b11f9482d3fb98)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VappVmConfig(
            name=name,
            vapp_name=vapp_name,
            accept_all_eulas=accept_all_eulas,
            boot_image=boot_image,
            boot_image_id=boot_image_id,
            boot_options=boot_options,
            catalog_name=catalog_name,
            computer_name=computer_name,
            consolidate_disks_on_create=consolidate_disks_on_create,
            copy_from_vm_id=copy_from_vm_id,
            cpu_cores=cpu_cores,
            cpu_hot_add_enabled=cpu_hot_add_enabled,
            cpu_limit=cpu_limit,
            cpu_priority=cpu_priority,
            cpu_reservation=cpu_reservation,
            cpus=cpus,
            cpu_shares=cpu_shares,
            customization=customization,
            description=description,
            disk=disk,
            expose_hardware_virtualization=expose_hardware_virtualization,
            firmware=firmware,
            guest_properties=guest_properties,
            hardware_version=hardware_version,
            href=href,
            id=id,
            memory=memory,
            memory_hot_add_enabled=memory_hot_add_enabled,
            memory_limit=memory_limit,
            memory_priority=memory_priority,
            memory_reservation=memory_reservation,
            memory_shares=memory_shares,
            metadata=metadata,
            metadata_entry=metadata_entry,
            network=network,
            network_dhcp_wait_seconds=network_dhcp_wait_seconds,
            org=org,
            os_type=os_type,
            override_template_disk=override_template_disk,
            placement_policy_id=placement_policy_id,
            power_on=power_on,
            prevent_update_power_off=prevent_update_power_off,
            security_tags=security_tags,
            set_extra_config=set_extra_config,
            sizing_policy_id=sizing_policy_id,
            storage_profile=storage_profile,
            template_name=template_name,
            vapp_template_id=vapp_template_id,
            vdc=vdc,
            vm_name_in_template=vm_name_in_template,
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
        '''Generates CDKTF code for importing a VappVm resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VappVm to import.
        :param import_from_id: The id of the existing VappVm that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VappVm to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80db4eaf3326c46ee0b456c88a2c413399b7fc0b108495aaf72660c4dc587524)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBootOptions")
    def put_boot_options(
        self,
        *,
        boot_delay: typing.Optional[jsii.Number] = None,
        boot_retry_delay: typing.Optional[jsii.Number] = None,
        boot_retry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        efi_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enter_bios_setup_on_next_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param boot_delay: Number of milliseconds to wait between powering-on and booting the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_delay VappVm#boot_delay}
        :param boot_retry_delay: Delay in milliseconds before a boot retry. Only works if 'boot_retry_enabled' is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_retry_delay VappVm#boot_retry_delay}
        :param boot_retry_enabled: If set to true, a VM that fails to boot will try again after the 'boot_retry_delay' time period has expired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_retry_enabled VappVm#boot_retry_enabled}
        :param efi_secure_boot: If set to true, enables EFI Secure Boot for the VM. Can only be changed when the VM is powered off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#efi_secure_boot VappVm#efi_secure_boot}
        :param enter_bios_setup_on_next_boot: If set to true, the VM will enter BIOS setup on next boot. If a VM is powered on, the field will be set to ``false`` by VCD and Terraform will return a non-empty plan Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#enter_bios_setup_on_next_boot VappVm#enter_bios_setup_on_next_boot}
        '''
        value = VappVmBootOptions(
            boot_delay=boot_delay,
            boot_retry_delay=boot_retry_delay,
            boot_retry_enabled=boot_retry_enabled,
            efi_secure_boot=efi_secure_boot,
            enter_bios_setup_on_next_boot=enter_bios_setup_on_next_boot,
        )

        return typing.cast(None, jsii.invoke(self, "putBootOptions", [value]))

    @jsii.member(jsii_name="putCustomization")
    def put_customization(
        self,
        *,
        admin_password: typing.Optional[builtins.str] = None,
        allow_local_admin_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_generate_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        change_sid: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        initscript: typing.Optional[builtins.str] = None,
        join_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        join_domain_account_ou: typing.Optional[builtins.str] = None,
        join_domain_name: typing.Optional[builtins.str] = None,
        join_domain_password: typing.Optional[builtins.str] = None,
        join_domain_user: typing.Optional[builtins.str] = None,
        join_org_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        must_change_password_on_first_login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        number_of_auto_logons: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param admin_password: Manually specify admin password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#admin_password VappVm#admin_password}
        :param allow_local_admin_password: Allow local administrator password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#allow_local_admin_password VappVm#allow_local_admin_password}
        :param auto_generate_password: Auto generate password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#auto_generate_password VappVm#auto_generate_password}
        :param change_sid: 'true' value will change SID. Applicable only for Windows VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#change_sid VappVm#change_sid}
        :param enabled: 'true' value will enable guest customization. It may occur on first boot or when 'force' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#enabled VappVm#enabled}
        :param force: 'true' value will cause the VM to reboot on every 'apply' operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#force VappVm#force}
        :param initscript: Script to run on initial boot or with customization.force=true set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#initscript VappVm#initscript}
        :param join_domain: Enable this VM to join a domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain VappVm#join_domain}
        :param join_domain_account_ou: Account organizational unit for domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_account_ou VappVm#join_domain_account_ou}
        :param join_domain_name: Custom domain name for join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_name VappVm#join_domain_name}
        :param join_domain_password: Password for custom domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_password VappVm#join_domain_password}
        :param join_domain_user: Username for custom domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_user VappVm#join_domain_user}
        :param join_org_domain: Use organization's domain for joining. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_org_domain VappVm#join_org_domain}
        :param must_change_password_on_first_login: Require Administrator to change password on first login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#must_change_password_on_first_login VappVm#must_change_password_on_first_login}
        :param number_of_auto_logons: Number of times to log on automatically. '0' - disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#number_of_auto_logons VappVm#number_of_auto_logons}
        '''
        value = VappVmCustomization(
            admin_password=admin_password,
            allow_local_admin_password=allow_local_admin_password,
            auto_generate_password=auto_generate_password,
            change_sid=change_sid,
            enabled=enabled,
            force=force,
            initscript=initscript,
            join_domain=join_domain,
            join_domain_account_ou=join_domain_account_ou,
            join_domain_name=join_domain_name,
            join_domain_password=join_domain_password,
            join_domain_user=join_domain_user,
            join_org_domain=join_org_domain,
            must_change_password_on_first_login=must_change_password_on_first_login,
            number_of_auto_logons=number_of_auto_logons,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomization", [value]))

    @jsii.member(jsii_name="putDisk")
    def put_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e67874cbf716ceb441b3873fc4d79db03606f7d8e08224106080165459d1266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisk", [value]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmMetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53cfc4aa6b73f714fc188d711d0015132671ec6d987a06dd4757d53e26ce23a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmNetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cd3fef6979f7e79eedf5841b9a4a4fedbce1123a4acf322181a0a043dd9b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putOverrideTemplateDisk")
    def put_override_template_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmOverrideTemplateDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f045761e24d6995180b90d0a320f44ef2e2a1021cbd138a0aa67a09cbcd51085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOverrideTemplateDisk", [value]))

    @jsii.member(jsii_name="putSetExtraConfig")
    def put_set_extra_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmSetExtraConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13622ae8f2fb177c44317c1dc21376716288b503c63b663b216259de527df7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetExtraConfig", [value]))

    @jsii.member(jsii_name="resetAcceptAllEulas")
    def reset_accept_all_eulas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceptAllEulas", []))

    @jsii.member(jsii_name="resetBootImage")
    def reset_boot_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootImage", []))

    @jsii.member(jsii_name="resetBootImageId")
    def reset_boot_image_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootImageId", []))

    @jsii.member(jsii_name="resetBootOptions")
    def reset_boot_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootOptions", []))

    @jsii.member(jsii_name="resetCatalogName")
    def reset_catalog_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalogName", []))

    @jsii.member(jsii_name="resetComputerName")
    def reset_computer_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputerName", []))

    @jsii.member(jsii_name="resetConsolidateDisksOnCreate")
    def reset_consolidate_disks_on_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsolidateDisksOnCreate", []))

    @jsii.member(jsii_name="resetCopyFromVmId")
    def reset_copy_from_vm_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyFromVmId", []))

    @jsii.member(jsii_name="resetCpuCores")
    def reset_cpu_cores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCores", []))

    @jsii.member(jsii_name="resetCpuHotAddEnabled")
    def reset_cpu_hot_add_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuHotAddEnabled", []))

    @jsii.member(jsii_name="resetCpuLimit")
    def reset_cpu_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuLimit", []))

    @jsii.member(jsii_name="resetCpuPriority")
    def reset_cpu_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuPriority", []))

    @jsii.member(jsii_name="resetCpuReservation")
    def reset_cpu_reservation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuReservation", []))

    @jsii.member(jsii_name="resetCpus")
    def reset_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpus", []))

    @jsii.member(jsii_name="resetCpuShares")
    def reset_cpu_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuShares", []))

    @jsii.member(jsii_name="resetCustomization")
    def reset_customization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomization", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @jsii.member(jsii_name="resetExposeHardwareVirtualization")
    def reset_expose_hardware_virtualization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExposeHardwareVirtualization", []))

    @jsii.member(jsii_name="resetFirmware")
    def reset_firmware(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirmware", []))

    @jsii.member(jsii_name="resetGuestProperties")
    def reset_guest_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestProperties", []))

    @jsii.member(jsii_name="resetHardwareVersion")
    def reset_hardware_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHardwareVersion", []))

    @jsii.member(jsii_name="resetHref")
    def reset_href(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHref", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetMemoryHotAddEnabled")
    def reset_memory_hot_add_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryHotAddEnabled", []))

    @jsii.member(jsii_name="resetMemoryLimit")
    def reset_memory_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryLimit", []))

    @jsii.member(jsii_name="resetMemoryPriority")
    def reset_memory_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryPriority", []))

    @jsii.member(jsii_name="resetMemoryReservation")
    def reset_memory_reservation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryReservation", []))

    @jsii.member(jsii_name="resetMemoryShares")
    def reset_memory_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryShares", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataEntry")
    def reset_metadata_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataEntry", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkDhcpWaitSeconds")
    def reset_network_dhcp_wait_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkDhcpWaitSeconds", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOsType")
    def reset_os_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsType", []))

    @jsii.member(jsii_name="resetOverrideTemplateDisk")
    def reset_override_template_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideTemplateDisk", []))

    @jsii.member(jsii_name="resetPlacementPolicyId")
    def reset_placement_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementPolicyId", []))

    @jsii.member(jsii_name="resetPowerOn")
    def reset_power_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPowerOn", []))

    @jsii.member(jsii_name="resetPreventUpdatePowerOff")
    def reset_prevent_update_power_off(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventUpdatePowerOff", []))

    @jsii.member(jsii_name="resetSecurityTags")
    def reset_security_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityTags", []))

    @jsii.member(jsii_name="resetSetExtraConfig")
    def reset_set_extra_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetExtraConfig", []))

    @jsii.member(jsii_name="resetSizingPolicyId")
    def reset_sizing_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizingPolicyId", []))

    @jsii.member(jsii_name="resetStorageProfile")
    def reset_storage_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageProfile", []))

    @jsii.member(jsii_name="resetTemplateName")
    def reset_template_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateName", []))

    @jsii.member(jsii_name="resetVappTemplateId")
    def reset_vapp_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVappTemplateId", []))

    @jsii.member(jsii_name="resetVdc")
    def reset_vdc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdc", []))

    @jsii.member(jsii_name="resetVmNameInTemplate")
    def reset_vm_name_in_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmNameInTemplate", []))

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
    @jsii.member(jsii_name="bootOptions")
    def boot_options(self) -> "VappVmBootOptionsOutputReference":
        return typing.cast("VappVmBootOptionsOutputReference", jsii.get(self, "bootOptions"))

    @builtins.property
    @jsii.member(jsii_name="customization")
    def customization(self) -> "VappVmCustomizationOutputReference":
        return typing.cast("VappVmCustomizationOutputReference", jsii.get(self, "customization"))

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> "VappVmDiskList":
        return typing.cast("VappVmDiskList", jsii.get(self, "disk"))

    @builtins.property
    @jsii.member(jsii_name="extraConfig")
    def extra_config(self) -> "VappVmExtraConfigList":
        return typing.cast("VappVmExtraConfigList", jsii.get(self, "extraConfig"))

    @builtins.property
    @jsii.member(jsii_name="imported")
    def imported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "imported"))

    @builtins.property
    @jsii.member(jsii_name="inheritedMetadata")
    def inherited_metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "inheritedMetadata"))

    @builtins.property
    @jsii.member(jsii_name="internalDisk")
    def internal_disk(self) -> "VappVmInternalDiskList":
        return typing.cast("VappVmInternalDiskList", jsii.get(self, "internalDisk"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "VappVmMetadataEntryList":
        return typing.cast("VappVmMetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "VappVmNetworkList":
        return typing.cast("VappVmNetworkList", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="overrideTemplateDisk")
    def override_template_disk(self) -> "VappVmOverrideTemplateDiskList":
        return typing.cast("VappVmOverrideTemplateDiskList", jsii.get(self, "overrideTemplateDisk"))

    @builtins.property
    @jsii.member(jsii_name="setExtraConfig")
    def set_extra_config(self) -> "VappVmSetExtraConfigList":
        return typing.cast("VappVmSetExtraConfigList", jsii.get(self, "setExtraConfig"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusText")
    def status_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusText"))

    @builtins.property
    @jsii.member(jsii_name="vappId")
    def vapp_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappId"))

    @builtins.property
    @jsii.member(jsii_name="vmType")
    def vm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmType"))

    @builtins.property
    @jsii.member(jsii_name="acceptAllEulasInput")
    def accept_all_eulas_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceptAllEulasInput"))

    @builtins.property
    @jsii.member(jsii_name="bootImageIdInput")
    def boot_image_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootImageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bootImageInput")
    def boot_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootImageInput"))

    @builtins.property
    @jsii.member(jsii_name="bootOptionsInput")
    def boot_options_input(self) -> typing.Optional["VappVmBootOptions"]:
        return typing.cast(typing.Optional["VappVmBootOptions"], jsii.get(self, "bootOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="catalogNameInput")
    def catalog_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogNameInput"))

    @builtins.property
    @jsii.member(jsii_name="computerNameInput")
    def computer_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="consolidateDisksOnCreateInput")
    def consolidate_disks_on_create_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "consolidateDisksOnCreateInput"))

    @builtins.property
    @jsii.member(jsii_name="copyFromVmIdInput")
    def copy_from_vm_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copyFromVmIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCoresInput")
    def cpu_cores_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCoresInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuHotAddEnabledInput")
    def cpu_hot_add_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cpuHotAddEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuLimitInput")
    def cpu_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuPriorityInput")
    def cpu_priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuPriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuReservationInput")
    def cpu_reservation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuReservationInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSharesInput")
    def cpu_shares_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="cpusInput")
    def cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpusInput"))

    @builtins.property
    @jsii.member(jsii_name="customizationInput")
    def customization_input(self) -> typing.Optional["VappVmCustomization"]:
        return typing.cast(typing.Optional["VappVmCustomization"], jsii.get(self, "customizationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmDisk"]]], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="exposeHardwareVirtualizationInput")
    def expose_hardware_virtualization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "exposeHardwareVirtualizationInput"))

    @builtins.property
    @jsii.member(jsii_name="firmwareInput")
    def firmware_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firmwareInput"))

    @builtins.property
    @jsii.member(jsii_name="guestPropertiesInput")
    def guest_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "guestPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="hardwareVersionInput")
    def hardware_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hardwareVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="hrefInput")
    def href_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hrefInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryHotAddEnabledInput")
    def memory_hot_add_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "memoryHotAddEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryLimitInput")
    def memory_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryPriorityInput")
    def memory_priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryPriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryReservationInput")
    def memory_reservation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryReservationInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySharesInput")
    def memory_shares_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySharesInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntryInput")
    def metadata_entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmMetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmMetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

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
    @jsii.member(jsii_name="networkDhcpWaitSecondsInput")
    def network_dhcp_wait_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "networkDhcpWaitSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmNetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmNetwork"]]], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideTemplateDiskInput")
    def override_template_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmOverrideTemplateDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmOverrideTemplateDisk"]]], jsii.get(self, "overrideTemplateDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="placementPolicyIdInput")
    def placement_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "placementPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="powerOnInput")
    def power_on_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "powerOnInput"))

    @builtins.property
    @jsii.member(jsii_name="preventUpdatePowerOffInput")
    def prevent_update_power_off_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventUpdatePowerOffInput"))

    @builtins.property
    @jsii.member(jsii_name="securityTagsInput")
    def security_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="setExtraConfigInput")
    def set_extra_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmSetExtraConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmSetExtraConfig"]]], jsii.get(self, "setExtraConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyIdInput")
    def sizing_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizingPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileInput")
    def storage_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="templateNameInput")
    def template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vappNameInput")
    def vapp_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vappNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vappTemplateIdInput")
    def vapp_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vappTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="vmNameInTemplateInput")
    def vm_name_in_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmNameInTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="acceptAllEulas")
    def accept_all_eulas(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceptAllEulas"))

    @accept_all_eulas.setter
    def accept_all_eulas(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4392299d19c63d727e2875682bf72ede984bf5b48e25bcb4341310c2c13df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptAllEulas", value)

    @builtins.property
    @jsii.member(jsii_name="bootImage")
    def boot_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootImage"))

    @boot_image.setter
    def boot_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925508e393ac3fa746a7eb516700317cac2db0865ca97589cd9306e548791677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootImage", value)

    @builtins.property
    @jsii.member(jsii_name="bootImageId")
    def boot_image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootImageId"))

    @boot_image_id.setter
    def boot_image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02bee797d6e214bc8bdb05b905017f613bc3338ee60a5601d6fb3556a5e7e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootImageId", value)

    @builtins.property
    @jsii.member(jsii_name="catalogName")
    def catalog_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogName"))

    @catalog_name.setter
    def catalog_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3502768eccaffe0c9b627c40cf4dc83e120b2ae62e1402de974b555f38515f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalogName", value)

    @builtins.property
    @jsii.member(jsii_name="computerName")
    def computer_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computerName"))

    @computer_name.setter
    def computer_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231a4d0933c961e94f29e29d4dd6f6f4f82078c9bc9c6a757aad34d7b5c8db89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computerName", value)

    @builtins.property
    @jsii.member(jsii_name="consolidateDisksOnCreate")
    def consolidate_disks_on_create(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "consolidateDisksOnCreate"))

    @consolidate_disks_on_create.setter
    def consolidate_disks_on_create(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7dee32eb35b7dbc71860ae4abfca1739875a47eb2abc9a86e2b35b3bfef6ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consolidateDisksOnCreate", value)

    @builtins.property
    @jsii.member(jsii_name="copyFromVmId")
    def copy_from_vm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyFromVmId"))

    @copy_from_vm_id.setter
    def copy_from_vm_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64d0d01a029822caebdf3da00dca8ba2e9b9cb7c4cd545b7973e52d06edd7db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyFromVmId", value)

    @builtins.property
    @jsii.member(jsii_name="cpuCores")
    def cpu_cores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCores"))

    @cpu_cores.setter
    def cpu_cores(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2b8dc7b794bf83e1237c401339cacfe05050219a454bf7de8bf7a77f2d9c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCores", value)

    @builtins.property
    @jsii.member(jsii_name="cpuHotAddEnabled")
    def cpu_hot_add_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cpuHotAddEnabled"))

    @cpu_hot_add_enabled.setter
    def cpu_hot_add_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6b40be4f791a6d7f8a5904afecb4b6b2c3996f3ddcc68a98a3bd0fb63be78f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuHotAddEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cpuLimit")
    def cpu_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuLimit"))

    @cpu_limit.setter
    def cpu_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90a95620112768bb43008e835301aa5dfacb050f3246b926d76dfe91df6479f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuLimit", value)

    @builtins.property
    @jsii.member(jsii_name="cpuPriority")
    def cpu_priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuPriority"))

    @cpu_priority.setter
    def cpu_priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1e108f7b019f9d54d02c6822e2a5d4ee40375275727a450b7c5852b0c12990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuPriority", value)

    @builtins.property
    @jsii.member(jsii_name="cpuReservation")
    def cpu_reservation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuReservation"))

    @cpu_reservation.setter
    def cpu_reservation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77458c019284910145482fd73eed4299e0d483d34615f13eaaf0ac93fa37ac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuReservation", value)

    @builtins.property
    @jsii.member(jsii_name="cpus")
    def cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpus"))

    @cpus.setter
    def cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ad1fc0e223fe293ac3d8d830ad84fe7e309683d60a010aeae0ea74379077be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value)

    @builtins.property
    @jsii.member(jsii_name="cpuShares")
    def cpu_shares(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuShares"))

    @cpu_shares.setter
    def cpu_shares(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11c7a7e8c93ab7240f571eae49292bd94ffd8773172df44d10e399a9dba0fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuShares", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a472b1bac4aa1e94f14f93b21c6c3dee70fa1c0dbec5c8a3d41f85d1cde436a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="exposeHardwareVirtualization")
    def expose_hardware_virtualization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "exposeHardwareVirtualization"))

    @expose_hardware_virtualization.setter
    def expose_hardware_virtualization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394818d6c1ee800aac41f9fd6920f4649315932aa219f01e337634ca56bb0d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposeHardwareVirtualization", value)

    @builtins.property
    @jsii.member(jsii_name="firmware")
    def firmware(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firmware"))

    @firmware.setter
    def firmware(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c18e1b7002006a4b8515ae1892c0195a76875e4b82523515af061f3576e3d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firmware", value)

    @builtins.property
    @jsii.member(jsii_name="guestProperties")
    def guest_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "guestProperties"))

    @guest_properties.setter
    def guest_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a489319a9b5c4d226004ff2795ad1b593c000e2f53e89d59de6c738d53208df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestProperties", value)

    @builtins.property
    @jsii.member(jsii_name="hardwareVersion")
    def hardware_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hardwareVersion"))

    @hardware_version.setter
    def hardware_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5b3e592b4eb1368c91f73fb4403bd70810e99bf36b0c0939d1c055f5c72723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hardwareVersion", value)

    @builtins.property
    @jsii.member(jsii_name="href")
    def href(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "href"))

    @href.setter
    def href(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8ff23804e87cd342d58d1ca09d50383e5d496204d50a79b0d482ea2bed947c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "href", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c4acb87a1b9cb834157a5a3c614b59442c3907cf09786388645f597445955e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0157496020119b7ecb146067a27448a214216b220a517751204ba0f3950f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value)

    @builtins.property
    @jsii.member(jsii_name="memoryHotAddEnabled")
    def memory_hot_add_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "memoryHotAddEnabled"))

    @memory_hot_add_enabled.setter
    def memory_hot_add_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e950e021a52182ae0444d46800860bb75f95556afb9bc6513a199cc3cd16c43d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryHotAddEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryLimit"))

    @memory_limit.setter
    def memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542cbbd7962f015092ee3ef944fee41f53478baf95c2a9b62f0956898b7bfbdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryLimit", value)

    @builtins.property
    @jsii.member(jsii_name="memoryPriority")
    def memory_priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memoryPriority"))

    @memory_priority.setter
    def memory_priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531f72707f72912eace0c26e0314b34643d50c84749fa04ba14745ee16ec310d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryPriority", value)

    @builtins.property
    @jsii.member(jsii_name="memoryReservation")
    def memory_reservation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryReservation"))

    @memory_reservation.setter
    def memory_reservation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056977b44c4ed3fa31e3ba946afd94abe6c89612ca6d838e856f473b4343cb1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryReservation", value)

    @builtins.property
    @jsii.member(jsii_name="memoryShares")
    def memory_shares(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryShares"))

    @memory_shares.setter
    def memory_shares(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a78d6ec3bd4e28f0e49f8f02aaac0115cd00f38fc2d9a2df58426292f950f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryShares", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fa6bd760231bdaff8457ed65c942cbb95b4024905554e14e584aca97fbdd56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d082338b9979a8e65565bacfed0e8ef156802a10dcfdb335906998a33be0742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkDhcpWaitSeconds")
    def network_dhcp_wait_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "networkDhcpWaitSeconds"))

    @network_dhcp_wait_seconds.setter
    def network_dhcp_wait_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3522199e33ece4006e724549afd67cb6dcfedad8a5c72bfd5bc24e3508233e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkDhcpWaitSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bbe4490d16672756fe45cd6e237284d75ef70c7a808c6fd612df7acff4239a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2abcaba02546eed580cf7e8ed15560761c04f2d806c469a0f52b5c3885bc37de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value)

    @builtins.property
    @jsii.member(jsii_name="placementPolicyId")
    def placement_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "placementPolicyId"))

    @placement_policy_id.setter
    def placement_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3acf3e2374eac8f49fefe038b0088feecc19fa770a14439c34251c27404b33c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="powerOn")
    def power_on(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "powerOn"))

    @power_on.setter
    def power_on(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d90b9764354ddce6bcd8c566efc4ecc8b1241c447e479e644402148d80bcd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "powerOn", value)

    @builtins.property
    @jsii.member(jsii_name="preventUpdatePowerOff")
    def prevent_update_power_off(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventUpdatePowerOff"))

    @prevent_update_power_off.setter
    def prevent_update_power_off(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105677873d137677bee33540ae876c98d74c51c816f4578329ef74c112c48801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventUpdatePowerOff", value)

    @builtins.property
    @jsii.member(jsii_name="securityTags")
    def security_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityTags"))

    @security_tags.setter
    def security_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69774cf41219ba39fc709167729abe1abf8e9124a99b6d2eec96fbf829684e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityTags", value)

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyId")
    def sizing_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingPolicyId"))

    @sizing_policy_id.setter
    def sizing_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a62721aa9313045121819d404bccfd27e9d1fcec295be7d8253b24a8a2c0f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfile"))

    @storage_profile.setter
    def storage_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d49a52cb1c816b0d52a406963ea3865edfe106c435ff5f3f366db6c9802091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfile", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d0ec25093799ce8a3670cb443ae3a01617271a22194a00f76a76ab7ac98fb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="vappName")
    def vapp_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappName"))

    @vapp_name.setter
    def vapp_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0c7cb588b1f0c8962806b728664d8a039d454111a641f51a1dd87b759e25fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappName", value)

    @builtins.property
    @jsii.member(jsii_name="vappTemplateId")
    def vapp_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappTemplateId"))

    @vapp_template_id.setter
    def vapp_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a130a0cffdf2e00b7857fe33d4a8e19e117f8a0edfa66e2d69189ba75e7e957b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappTemplateId", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb8fc204ed906d39c22f7f5943aae0b455fd0138cc75fb102088d36bbad8fab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)

    @builtins.property
    @jsii.member(jsii_name="vmNameInTemplate")
    def vm_name_in_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmNameInTemplate"))

    @vm_name_in_template.setter
    def vm_name_in_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9866b7cf2be1d023770199fa03f39cc1173b8affc67558e04b226ef24098ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmNameInTemplate", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmBootOptions",
    jsii_struct_bases=[],
    name_mapping={
        "boot_delay": "bootDelay",
        "boot_retry_delay": "bootRetryDelay",
        "boot_retry_enabled": "bootRetryEnabled",
        "efi_secure_boot": "efiSecureBoot",
        "enter_bios_setup_on_next_boot": "enterBiosSetupOnNextBoot",
    },
)
class VappVmBootOptions:
    def __init__(
        self,
        *,
        boot_delay: typing.Optional[jsii.Number] = None,
        boot_retry_delay: typing.Optional[jsii.Number] = None,
        boot_retry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        efi_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enter_bios_setup_on_next_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param boot_delay: Number of milliseconds to wait between powering-on and booting the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_delay VappVm#boot_delay}
        :param boot_retry_delay: Delay in milliseconds before a boot retry. Only works if 'boot_retry_enabled' is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_retry_delay VappVm#boot_retry_delay}
        :param boot_retry_enabled: If set to true, a VM that fails to boot will try again after the 'boot_retry_delay' time period has expired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_retry_enabled VappVm#boot_retry_enabled}
        :param efi_secure_boot: If set to true, enables EFI Secure Boot for the VM. Can only be changed when the VM is powered off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#efi_secure_boot VappVm#efi_secure_boot}
        :param enter_bios_setup_on_next_boot: If set to true, the VM will enter BIOS setup on next boot. If a VM is powered on, the field will be set to ``false`` by VCD and Terraform will return a non-empty plan Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#enter_bios_setup_on_next_boot VappVm#enter_bios_setup_on_next_boot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655f39ff0147b2d63186ada3907f78911441f00263045e6219fff7315ef82dee)
            check_type(argname="argument boot_delay", value=boot_delay, expected_type=type_hints["boot_delay"])
            check_type(argname="argument boot_retry_delay", value=boot_retry_delay, expected_type=type_hints["boot_retry_delay"])
            check_type(argname="argument boot_retry_enabled", value=boot_retry_enabled, expected_type=type_hints["boot_retry_enabled"])
            check_type(argname="argument efi_secure_boot", value=efi_secure_boot, expected_type=type_hints["efi_secure_boot"])
            check_type(argname="argument enter_bios_setup_on_next_boot", value=enter_bios_setup_on_next_boot, expected_type=type_hints["enter_bios_setup_on_next_boot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_delay is not None:
            self._values["boot_delay"] = boot_delay
        if boot_retry_delay is not None:
            self._values["boot_retry_delay"] = boot_retry_delay
        if boot_retry_enabled is not None:
            self._values["boot_retry_enabled"] = boot_retry_enabled
        if efi_secure_boot is not None:
            self._values["efi_secure_boot"] = efi_secure_boot
        if enter_bios_setup_on_next_boot is not None:
            self._values["enter_bios_setup_on_next_boot"] = enter_bios_setup_on_next_boot

    @builtins.property
    def boot_delay(self) -> typing.Optional[jsii.Number]:
        '''Number of milliseconds to wait between powering-on and booting the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_delay VappVm#boot_delay}
        '''
        result = self._values.get("boot_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_retry_delay(self) -> typing.Optional[jsii.Number]:
        '''Delay in milliseconds before a boot retry. Only works if 'boot_retry_enabled' is set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_retry_delay VappVm#boot_retry_delay}
        '''
        result = self._values.get("boot_retry_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_retry_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, a VM that fails to boot will try again after the 'boot_retry_delay' time period has expired.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_retry_enabled VappVm#boot_retry_enabled}
        '''
        result = self._values.get("boot_retry_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def efi_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, enables EFI Secure Boot for the VM.

        Can only be changed when the VM is powered off.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#efi_secure_boot VappVm#efi_secure_boot}
        '''
        result = self._values.get("efi_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enter_bios_setup_on_next_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the VM will enter BIOS setup on next boot.

        If a VM is powered on, the field will be set to ``false`` by VCD and Terraform will return a non-empty plan

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#enter_bios_setup_on_next_boot VappVm#enter_bios_setup_on_next_boot}
        '''
        result = self._values.get("enter_bios_setup_on_next_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmBootOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmBootOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmBootOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f1728bc23e6d9dd11cd1e414b19c819735c0a5a3e5d129fd8866ee098e75593)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDelay")
    def reset_boot_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDelay", []))

    @jsii.member(jsii_name="resetBootRetryDelay")
    def reset_boot_retry_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootRetryDelay", []))

    @jsii.member(jsii_name="resetBootRetryEnabled")
    def reset_boot_retry_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootRetryEnabled", []))

    @jsii.member(jsii_name="resetEfiSecureBoot")
    def reset_efi_secure_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEfiSecureBoot", []))

    @jsii.member(jsii_name="resetEnterBiosSetupOnNextBoot")
    def reset_enter_bios_setup_on_next_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterBiosSetupOnNextBoot", []))

    @builtins.property
    @jsii.member(jsii_name="bootDelayInput")
    def boot_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="bootRetryDelayInput")
    def boot_retry_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootRetryDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="bootRetryEnabledInput")
    def boot_retry_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bootRetryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="efiSecureBootInput")
    def efi_secure_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "efiSecureBootInput"))

    @builtins.property
    @jsii.member(jsii_name="enterBiosSetupOnNextBootInput")
    def enter_bios_setup_on_next_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enterBiosSetupOnNextBootInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDelay")
    def boot_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDelay"))

    @boot_delay.setter
    def boot_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38916c8dad9674dc547ed6c6d3342a62df97727d56bfb7a9c7f13257103b45d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDelay", value)

    @builtins.property
    @jsii.member(jsii_name="bootRetryDelay")
    def boot_retry_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootRetryDelay"))

    @boot_retry_delay.setter
    def boot_retry_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0cee689f649525f9309c4b8593acb76a27a4c16558acc1da3630ce4dcb46c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootRetryDelay", value)

    @builtins.property
    @jsii.member(jsii_name="bootRetryEnabled")
    def boot_retry_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bootRetryEnabled"))

    @boot_retry_enabled.setter
    def boot_retry_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5305fd9d020a34130d969a66f722ea6742e53193acc9a3378d4d8a4ee554217a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootRetryEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="efiSecureBoot")
    def efi_secure_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "efiSecureBoot"))

    @efi_secure_boot.setter
    def efi_secure_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4c615cd5a5c67a43d9e64574a1674929002a9ebcb5f459f675596432a7ca8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "efiSecureBoot", value)

    @builtins.property
    @jsii.member(jsii_name="enterBiosSetupOnNextBoot")
    def enter_bios_setup_on_next_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enterBiosSetupOnNextBoot"))

    @enter_bios_setup_on_next_boot.setter
    def enter_bios_setup_on_next_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6169ecd46c91d9aa4aa47fbee4a51195e0d579cbaa543804e1cc954be631371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterBiosSetupOnNextBoot", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VappVmBootOptions]:
        return typing.cast(typing.Optional[VappVmBootOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VappVmBootOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a9a7d606937e342c28007263dc70575b07e43a5f00c7b7b3bcf970511afdbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmConfig",
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
        "vapp_name": "vappName",
        "accept_all_eulas": "acceptAllEulas",
        "boot_image": "bootImage",
        "boot_image_id": "bootImageId",
        "boot_options": "bootOptions",
        "catalog_name": "catalogName",
        "computer_name": "computerName",
        "consolidate_disks_on_create": "consolidateDisksOnCreate",
        "copy_from_vm_id": "copyFromVmId",
        "cpu_cores": "cpuCores",
        "cpu_hot_add_enabled": "cpuHotAddEnabled",
        "cpu_limit": "cpuLimit",
        "cpu_priority": "cpuPriority",
        "cpu_reservation": "cpuReservation",
        "cpus": "cpus",
        "cpu_shares": "cpuShares",
        "customization": "customization",
        "description": "description",
        "disk": "disk",
        "expose_hardware_virtualization": "exposeHardwareVirtualization",
        "firmware": "firmware",
        "guest_properties": "guestProperties",
        "hardware_version": "hardwareVersion",
        "href": "href",
        "id": "id",
        "memory": "memory",
        "memory_hot_add_enabled": "memoryHotAddEnabled",
        "memory_limit": "memoryLimit",
        "memory_priority": "memoryPriority",
        "memory_reservation": "memoryReservation",
        "memory_shares": "memoryShares",
        "metadata": "metadata",
        "metadata_entry": "metadataEntry",
        "network": "network",
        "network_dhcp_wait_seconds": "networkDhcpWaitSeconds",
        "org": "org",
        "os_type": "osType",
        "override_template_disk": "overrideTemplateDisk",
        "placement_policy_id": "placementPolicyId",
        "power_on": "powerOn",
        "prevent_update_power_off": "preventUpdatePowerOff",
        "security_tags": "securityTags",
        "set_extra_config": "setExtraConfig",
        "sizing_policy_id": "sizingPolicyId",
        "storage_profile": "storageProfile",
        "template_name": "templateName",
        "vapp_template_id": "vappTemplateId",
        "vdc": "vdc",
        "vm_name_in_template": "vmNameInTemplate",
    },
)
class VappVmConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        vapp_name: builtins.str,
        accept_all_eulas: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        boot_image: typing.Optional[builtins.str] = None,
        boot_image_id: typing.Optional[builtins.str] = None,
        boot_options: typing.Optional[typing.Union[VappVmBootOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        catalog_name: typing.Optional[builtins.str] = None,
        computer_name: typing.Optional[builtins.str] = None,
        consolidate_disks_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        copy_from_vm_id: typing.Optional[builtins.str] = None,
        cpu_cores: typing.Optional[jsii.Number] = None,
        cpu_hot_add_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_limit: typing.Optional[jsii.Number] = None,
        cpu_priority: typing.Optional[builtins.str] = None,
        cpu_reservation: typing.Optional[jsii.Number] = None,
        cpus: typing.Optional[jsii.Number] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        customization: typing.Optional[typing.Union["VappVmCustomization", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        expose_hardware_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        firmware: typing.Optional[builtins.str] = None,
        guest_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        hardware_version: typing.Optional[builtins.str] = None,
        href: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_hot_add_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        memory_priority: typing.Optional[builtins.str] = None,
        memory_reservation: typing.Optional[jsii.Number] = None,
        memory_shares: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_dhcp_wait_seconds: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        override_template_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmOverrideTemplateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement_policy_id: typing.Optional[builtins.str] = None,
        power_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_update_power_off: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        set_extra_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VappVmSetExtraConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sizing_policy_id: typing.Optional[builtins.str] = None,
        storage_profile: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
        vapp_template_id: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        vm_name_in_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: A name for the VM, unique within the vApp. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#name VappVm#name}
        :param vapp_name: The vApp this VM belongs to - Required, unless it is a standalone VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vapp_name VappVm#vapp_name}
        :param accept_all_eulas: Automatically accept EULA if OVA has it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#accept_all_eulas VappVm#accept_all_eulas}
        :param boot_image: Media name to add as boot image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_image VappVm#boot_image}
        :param boot_image_id: The URN of the media to use as boot image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_image_id VappVm#boot_image_id}
        :param boot_options: boot_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_options VappVm#boot_options}
        :param catalog_name: The catalog name in which to find the given vApp Template or media for boot_image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#catalog_name VappVm#catalog_name}
        :param computer_name: Computer name to assign to this virtual machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#computer_name VappVm#computer_name}
        :param consolidate_disks_on_create: Consolidates disks during creation and allows to change disk size using 'override_template_disk' in fast provisioned VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#consolidate_disks_on_create VappVm#consolidate_disks_on_create}
        :param copy_from_vm_id: Source VM that should be copied from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#copy_from_vm_id VappVm#copy_from_vm_id}
        :param cpu_cores: The number of cores per socket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_cores VappVm#cpu_cores}
        :param cpu_hot_add_enabled: True if the virtual machine supports addition of virtual CPUs while powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_hot_add_enabled VappVm#cpu_hot_add_enabled}
        :param cpu_limit: The limit for how much of CPU can be consumed on the underlying virtualization infrastructure. This is only valid when the resource allocation is not unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_limit VappVm#cpu_limit}
        :param cpu_priority: Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_priority VappVm#cpu_priority}
        :param cpu_reservation: The amount of MHz reservation on the underlying virtualization infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_reservation VappVm#cpu_reservation}
        :param cpus: The number of virtual CPUs to allocate to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpus VappVm#cpus}
        :param cpu_shares: Custom priority for the resource. This is a read-only, unless the ``cpu_priority`` is CUSTOM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_shares VappVm#cpu_shares}
        :param customization: customization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#customization VappVm#customization}
        :param description: The VM description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#description VappVm#description}
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#disk VappVm#disk}
        :param expose_hardware_virtualization: Expose hardware-assisted CPU virtualization to guest OS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#expose_hardware_virtualization VappVm#expose_hardware_virtualization}
        :param firmware: Firmware of the VM. Can be either EFI or BIOS, availabilitydepending on the os_type argument. If unset, is set to 'bios' by default. Changing the value when ``power_on`` is set to true, will cause a reboot of the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#firmware VappVm#firmware}
        :param guest_properties: Key/value settings for guest properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#guest_properties VappVm#guest_properties}
        :param hardware_version: Virtual Hardware Version (e.g.``vmx-14``, ``vmx-13``, ``vmx-12``, etc.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#hardware_version VappVm#hardware_version}
        :param href: VM Hyper Reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#href VappVm#href}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#id VappVm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param memory: The amount of RAM (in MB) to allocate to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory VappVm#memory}
        :param memory_hot_add_enabled: True if the virtual machine supports addition of memory while powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_hot_add_enabled VappVm#memory_hot_add_enabled}
        :param memory_limit: The limit for how much of memory can be consumed on the underlying virtualization infrastructure. This is only valid when the resource allocation is not unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_limit VappVm#memory_limit}
        :param memory_priority: Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_priority VappVm#memory_priority}
        :param memory_reservation: The amount of RAM (in MB) reservation on the underlying virtualization infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_reservation VappVm#memory_reservation}
        :param memory_shares: Custom priority for the resource. This is a read-only, unless the ``memory_priority`` is CUSTOM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_shares VappVm#memory_shares}
        :param metadata: Key value map of metadata to assign to this VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#metadata VappVm#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#metadata_entry VappVm#metadata_entry}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#network VappVm#network}
        :param network_dhcp_wait_seconds: Optional number of seconds to try and wait for DHCP IP (valid for 'network' block only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#network_dhcp_wait_seconds VappVm#network_dhcp_wait_seconds}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#org VappVm#org}
        :param os_type: Operating System type. Possible values can be found in documentation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#os_type VappVm#os_type}
        :param override_template_disk: override_template_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#override_template_disk VappVm#override_template_disk}
        :param placement_policy_id: VM placement policy ID. Has to be assigned to Org VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#placement_policy_id VappVm#placement_policy_id}
        :param power_on: A boolean value stating if this VM should be powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#power_on VappVm#power_on}
        :param prevent_update_power_off: True if the update of resource should fail when virtual machine power off needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#prevent_update_power_off VappVm#prevent_update_power_off}
        :param security_tags: Security tags to assign to this VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#security_tags VappVm#security_tags}
        :param set_extra_config: set_extra_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#set_extra_config VappVm#set_extra_config}
        :param sizing_policy_id: VM sizing policy ID. Has to be assigned to Org VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#sizing_policy_id VappVm#sizing_policy_id}
        :param storage_profile: Storage profile to override the default one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#storage_profile VappVm#storage_profile}
        :param template_name: The name of the vApp Template to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#template_name VappVm#template_name}
        :param vapp_template_id: The URN of the vApp Template to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vapp_template_id VappVm#vapp_template_id}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vdc VappVm#vdc}
        :param vm_name_in_template: The name of the VM in vApp Template to use. In cases when vApp template has more than one VM Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vm_name_in_template VappVm#vm_name_in_template}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(boot_options, dict):
            boot_options = VappVmBootOptions(**boot_options)
        if isinstance(customization, dict):
            customization = VappVmCustomization(**customization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5b7cc359649e1da25ffb423e375d54684be6544c08ffce7578ed772b598605)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vapp_name", value=vapp_name, expected_type=type_hints["vapp_name"])
            check_type(argname="argument accept_all_eulas", value=accept_all_eulas, expected_type=type_hints["accept_all_eulas"])
            check_type(argname="argument boot_image", value=boot_image, expected_type=type_hints["boot_image"])
            check_type(argname="argument boot_image_id", value=boot_image_id, expected_type=type_hints["boot_image_id"])
            check_type(argname="argument boot_options", value=boot_options, expected_type=type_hints["boot_options"])
            check_type(argname="argument catalog_name", value=catalog_name, expected_type=type_hints["catalog_name"])
            check_type(argname="argument computer_name", value=computer_name, expected_type=type_hints["computer_name"])
            check_type(argname="argument consolidate_disks_on_create", value=consolidate_disks_on_create, expected_type=type_hints["consolidate_disks_on_create"])
            check_type(argname="argument copy_from_vm_id", value=copy_from_vm_id, expected_type=type_hints["copy_from_vm_id"])
            check_type(argname="argument cpu_cores", value=cpu_cores, expected_type=type_hints["cpu_cores"])
            check_type(argname="argument cpu_hot_add_enabled", value=cpu_hot_add_enabled, expected_type=type_hints["cpu_hot_add_enabled"])
            check_type(argname="argument cpu_limit", value=cpu_limit, expected_type=type_hints["cpu_limit"])
            check_type(argname="argument cpu_priority", value=cpu_priority, expected_type=type_hints["cpu_priority"])
            check_type(argname="argument cpu_reservation", value=cpu_reservation, expected_type=type_hints["cpu_reservation"])
            check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
            check_type(argname="argument cpu_shares", value=cpu_shares, expected_type=type_hints["cpu_shares"])
            check_type(argname="argument customization", value=customization, expected_type=type_hints["customization"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            check_type(argname="argument expose_hardware_virtualization", value=expose_hardware_virtualization, expected_type=type_hints["expose_hardware_virtualization"])
            check_type(argname="argument firmware", value=firmware, expected_type=type_hints["firmware"])
            check_type(argname="argument guest_properties", value=guest_properties, expected_type=type_hints["guest_properties"])
            check_type(argname="argument hardware_version", value=hardware_version, expected_type=type_hints["hardware_version"])
            check_type(argname="argument href", value=href, expected_type=type_hints["href"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument memory_hot_add_enabled", value=memory_hot_add_enabled, expected_type=type_hints["memory_hot_add_enabled"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
            check_type(argname="argument memory_priority", value=memory_priority, expected_type=type_hints["memory_priority"])
            check_type(argname="argument memory_reservation", value=memory_reservation, expected_type=type_hints["memory_reservation"])
            check_type(argname="argument memory_shares", value=memory_shares, expected_type=type_hints["memory_shares"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_entry", value=metadata_entry, expected_type=type_hints["metadata_entry"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_dhcp_wait_seconds", value=network_dhcp_wait_seconds, expected_type=type_hints["network_dhcp_wait_seconds"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument override_template_disk", value=override_template_disk, expected_type=type_hints["override_template_disk"])
            check_type(argname="argument placement_policy_id", value=placement_policy_id, expected_type=type_hints["placement_policy_id"])
            check_type(argname="argument power_on", value=power_on, expected_type=type_hints["power_on"])
            check_type(argname="argument prevent_update_power_off", value=prevent_update_power_off, expected_type=type_hints["prevent_update_power_off"])
            check_type(argname="argument security_tags", value=security_tags, expected_type=type_hints["security_tags"])
            check_type(argname="argument set_extra_config", value=set_extra_config, expected_type=type_hints["set_extra_config"])
            check_type(argname="argument sizing_policy_id", value=sizing_policy_id, expected_type=type_hints["sizing_policy_id"])
            check_type(argname="argument storage_profile", value=storage_profile, expected_type=type_hints["storage_profile"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument vapp_template_id", value=vapp_template_id, expected_type=type_hints["vapp_template_id"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
            check_type(argname="argument vm_name_in_template", value=vm_name_in_template, expected_type=type_hints["vm_name_in_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vapp_name": vapp_name,
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
        if accept_all_eulas is not None:
            self._values["accept_all_eulas"] = accept_all_eulas
        if boot_image is not None:
            self._values["boot_image"] = boot_image
        if boot_image_id is not None:
            self._values["boot_image_id"] = boot_image_id
        if boot_options is not None:
            self._values["boot_options"] = boot_options
        if catalog_name is not None:
            self._values["catalog_name"] = catalog_name
        if computer_name is not None:
            self._values["computer_name"] = computer_name
        if consolidate_disks_on_create is not None:
            self._values["consolidate_disks_on_create"] = consolidate_disks_on_create
        if copy_from_vm_id is not None:
            self._values["copy_from_vm_id"] = copy_from_vm_id
        if cpu_cores is not None:
            self._values["cpu_cores"] = cpu_cores
        if cpu_hot_add_enabled is not None:
            self._values["cpu_hot_add_enabled"] = cpu_hot_add_enabled
        if cpu_limit is not None:
            self._values["cpu_limit"] = cpu_limit
        if cpu_priority is not None:
            self._values["cpu_priority"] = cpu_priority
        if cpu_reservation is not None:
            self._values["cpu_reservation"] = cpu_reservation
        if cpus is not None:
            self._values["cpus"] = cpus
        if cpu_shares is not None:
            self._values["cpu_shares"] = cpu_shares
        if customization is not None:
            self._values["customization"] = customization
        if description is not None:
            self._values["description"] = description
        if disk is not None:
            self._values["disk"] = disk
        if expose_hardware_virtualization is not None:
            self._values["expose_hardware_virtualization"] = expose_hardware_virtualization
        if firmware is not None:
            self._values["firmware"] = firmware
        if guest_properties is not None:
            self._values["guest_properties"] = guest_properties
        if hardware_version is not None:
            self._values["hardware_version"] = hardware_version
        if href is not None:
            self._values["href"] = href
        if id is not None:
            self._values["id"] = id
        if memory is not None:
            self._values["memory"] = memory
        if memory_hot_add_enabled is not None:
            self._values["memory_hot_add_enabled"] = memory_hot_add_enabled
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if memory_priority is not None:
            self._values["memory_priority"] = memory_priority
        if memory_reservation is not None:
            self._values["memory_reservation"] = memory_reservation
        if memory_shares is not None:
            self._values["memory_shares"] = memory_shares
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_entry is not None:
            self._values["metadata_entry"] = metadata_entry
        if network is not None:
            self._values["network"] = network
        if network_dhcp_wait_seconds is not None:
            self._values["network_dhcp_wait_seconds"] = network_dhcp_wait_seconds
        if org is not None:
            self._values["org"] = org
        if os_type is not None:
            self._values["os_type"] = os_type
        if override_template_disk is not None:
            self._values["override_template_disk"] = override_template_disk
        if placement_policy_id is not None:
            self._values["placement_policy_id"] = placement_policy_id
        if power_on is not None:
            self._values["power_on"] = power_on
        if prevent_update_power_off is not None:
            self._values["prevent_update_power_off"] = prevent_update_power_off
        if security_tags is not None:
            self._values["security_tags"] = security_tags
        if set_extra_config is not None:
            self._values["set_extra_config"] = set_extra_config
        if sizing_policy_id is not None:
            self._values["sizing_policy_id"] = sizing_policy_id
        if storage_profile is not None:
            self._values["storage_profile"] = storage_profile
        if template_name is not None:
            self._values["template_name"] = template_name
        if vapp_template_id is not None:
            self._values["vapp_template_id"] = vapp_template_id
        if vdc is not None:
            self._values["vdc"] = vdc
        if vm_name_in_template is not None:
            self._values["vm_name_in_template"] = vm_name_in_template

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
        '''A name for the VM, unique within the vApp.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#name VappVm#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vapp_name(self) -> builtins.str:
        '''The vApp this VM belongs to - Required, unless it is a standalone VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vapp_name VappVm#vapp_name}
        '''
        result = self._values.get("vapp_name")
        assert result is not None, "Required property 'vapp_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_all_eulas(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically accept EULA if OVA has it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#accept_all_eulas VappVm#accept_all_eulas}
        '''
        result = self._values.get("accept_all_eulas")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def boot_image(self) -> typing.Optional[builtins.str]:
        '''Media name to add as boot image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_image VappVm#boot_image}
        '''
        result = self._values.get("boot_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_image_id(self) -> typing.Optional[builtins.str]:
        '''The URN of the media to use as boot image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_image_id VappVm#boot_image_id}
        '''
        result = self._values.get("boot_image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_options(self) -> typing.Optional[VappVmBootOptions]:
        '''boot_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#boot_options VappVm#boot_options}
        '''
        result = self._values.get("boot_options")
        return typing.cast(typing.Optional[VappVmBootOptions], result)

    @builtins.property
    def catalog_name(self) -> typing.Optional[builtins.str]:
        '''The catalog name in which to find the given vApp Template or media for boot_image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#catalog_name VappVm#catalog_name}
        '''
        result = self._values.get("catalog_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def computer_name(self) -> typing.Optional[builtins.str]:
        '''Computer name to assign to this virtual machine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#computer_name VappVm#computer_name}
        '''
        result = self._values.get("computer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consolidate_disks_on_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Consolidates disks during creation and allows to change disk size using 'override_template_disk' in fast provisioned VDCs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#consolidate_disks_on_create VappVm#consolidate_disks_on_create}
        '''
        result = self._values.get("consolidate_disks_on_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def copy_from_vm_id(self) -> typing.Optional[builtins.str]:
        '''Source VM that should be copied from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#copy_from_vm_id VappVm#copy_from_vm_id}
        '''
        result = self._values.get("copy_from_vm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_cores(self) -> typing.Optional[jsii.Number]:
        '''The number of cores per socket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_cores VappVm#cpu_cores}
        '''
        result = self._values.get("cpu_cores")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_hot_add_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the virtual machine supports addition of virtual CPUs while powered on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_hot_add_enabled VappVm#cpu_hot_add_enabled}
        '''
        result = self._values.get("cpu_hot_add_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_limit(self) -> typing.Optional[jsii.Number]:
        '''The limit for how much of CPU can be consumed on the underlying virtualization infrastructure.

        This is only valid when the resource allocation is not unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_limit VappVm#cpu_limit}
        '''
        result = self._values.get("cpu_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_priority(self) -> typing.Optional[builtins.str]:
        '''Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_priority VappVm#cpu_priority}
        '''
        result = self._values.get("cpu_priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''The amount of MHz reservation on the underlying virtualization infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_reservation VappVm#cpu_reservation}
        '''
        result = self._values.get("cpu_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of virtual CPUs to allocate to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpus VappVm#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_shares(self) -> typing.Optional[jsii.Number]:
        '''Custom priority for the resource. This is a read-only, unless the ``cpu_priority`` is CUSTOM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#cpu_shares VappVm#cpu_shares}
        '''
        result = self._values.get("cpu_shares")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def customization(self) -> typing.Optional["VappVmCustomization"]:
        '''customization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#customization VappVm#customization}
        '''
        result = self._values.get("customization")
        return typing.cast(typing.Optional["VappVmCustomization"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The VM description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#description VappVm#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmDisk"]]]:
        '''disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#disk VappVm#disk}
        '''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmDisk"]]], result)

    @builtins.property
    def expose_hardware_virtualization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Expose hardware-assisted CPU virtualization to guest OS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#expose_hardware_virtualization VappVm#expose_hardware_virtualization}
        '''
        result = self._values.get("expose_hardware_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def firmware(self) -> typing.Optional[builtins.str]:
        '''Firmware of the VM.

        Can be either EFI or BIOS, availabilitydepending on the os_type argument. If unset, is set to 'bios' by default. Changing the value when ``power_on`` is set to true, will cause a reboot of the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#firmware VappVm#firmware}
        '''
        result = self._values.get("firmware")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key/value settings for guest properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#guest_properties VappVm#guest_properties}
        '''
        result = self._values.get("guest_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def hardware_version(self) -> typing.Optional[builtins.str]:
        '''Virtual Hardware Version (e.g.``vmx-14``, ``vmx-13``, ``vmx-12``, etc.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#hardware_version VappVm#hardware_version}
        '''
        result = self._values.get("hardware_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def href(self) -> typing.Optional[builtins.str]:
        '''VM Hyper Reference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#href VappVm#href}
        '''
        result = self._values.get("href")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#id VappVm#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''The amount of RAM (in MB) to allocate to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory VappVm#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_hot_add_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the virtual machine supports addition of memory while powered on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_hot_add_enabled VappVm#memory_hot_add_enabled}
        '''
        result = self._values.get("memory_hot_add_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''The limit for how much of memory can be consumed on the underlying virtualization infrastructure.

        This is only valid when the resource allocation is not unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_limit VappVm#memory_limit}
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_priority(self) -> typing.Optional[builtins.str]:
        '''Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_priority VappVm#memory_priority}
        '''
        result = self._values.get("memory_priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        '''The amount of RAM (in MB) reservation on the underlying virtualization infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_reservation VappVm#memory_reservation}
        '''
        result = self._values.get("memory_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_shares(self) -> typing.Optional[jsii.Number]:
        '''Custom priority for the resource. This is a read-only, unless the ``memory_priority`` is CUSTOM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#memory_shares VappVm#memory_shares}
        '''
        result = self._values.get("memory_shares")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key value map of metadata to assign to this VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#metadata VappVm#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmMetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#metadata_entry VappVm#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmMetadataEntry"]]], result)

    @builtins.property
    def network(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmNetwork"]]]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#network VappVm#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmNetwork"]]], result)

    @builtins.property
    def network_dhcp_wait_seconds(self) -> typing.Optional[jsii.Number]:
        '''Optional number of seconds to try and wait for DHCP IP (valid for 'network' block only).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#network_dhcp_wait_seconds VappVm#network_dhcp_wait_seconds}
        '''
        result = self._values.get("network_dhcp_wait_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#org VappVm#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Operating System type. Possible values can be found in documentation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#os_type VappVm#os_type}
        '''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_template_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmOverrideTemplateDisk"]]]:
        '''override_template_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#override_template_disk VappVm#override_template_disk}
        '''
        result = self._values.get("override_template_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmOverrideTemplateDisk"]]], result)

    @builtins.property
    def placement_policy_id(self) -> typing.Optional[builtins.str]:
        '''VM placement policy ID. Has to be assigned to Org VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#placement_policy_id VappVm#placement_policy_id}
        '''
        result = self._values.get("placement_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def power_on(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean value stating if this VM should be powered on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#power_on VappVm#power_on}
        '''
        result = self._values.get("power_on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_update_power_off(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the update of resource should fail when virtual machine power off needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#prevent_update_power_off VappVm#prevent_update_power_off}
        '''
        result = self._values.get("prevent_update_power_off")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Security tags to assign to this VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#security_tags VappVm#security_tags}
        '''
        result = self._values.get("security_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def set_extra_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmSetExtraConfig"]]]:
        '''set_extra_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#set_extra_config VappVm#set_extra_config}
        '''
        result = self._values.get("set_extra_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VappVmSetExtraConfig"]]], result)

    @builtins.property
    def sizing_policy_id(self) -> typing.Optional[builtins.str]:
        '''VM sizing policy ID. Has to be assigned to Org VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#sizing_policy_id VappVm#sizing_policy_id}
        '''
        result = self._values.get("sizing_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_profile(self) -> typing.Optional[builtins.str]:
        '''Storage profile to override the default one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#storage_profile VappVm#storage_profile}
        '''
        result = self._values.get("storage_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the vApp Template to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#template_name VappVm#template_name}
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vapp_template_id(self) -> typing.Optional[builtins.str]:
        '''The URN of the vApp Template to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vapp_template_id VappVm#vapp_template_id}
        '''
        result = self._values.get("vapp_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vdc VappVm#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_name_in_template(self) -> typing.Optional[builtins.str]:
        '''The name of the VM in vApp Template to use.

        In cases when vApp template has more than one VM

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#vm_name_in_template VappVm#vm_name_in_template}
        '''
        result = self._values.get("vm_name_in_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmCustomization",
    jsii_struct_bases=[],
    name_mapping={
        "admin_password": "adminPassword",
        "allow_local_admin_password": "allowLocalAdminPassword",
        "auto_generate_password": "autoGeneratePassword",
        "change_sid": "changeSid",
        "enabled": "enabled",
        "force": "force",
        "initscript": "initscript",
        "join_domain": "joinDomain",
        "join_domain_account_ou": "joinDomainAccountOu",
        "join_domain_name": "joinDomainName",
        "join_domain_password": "joinDomainPassword",
        "join_domain_user": "joinDomainUser",
        "join_org_domain": "joinOrgDomain",
        "must_change_password_on_first_login": "mustChangePasswordOnFirstLogin",
        "number_of_auto_logons": "numberOfAutoLogons",
    },
)
class VappVmCustomization:
    def __init__(
        self,
        *,
        admin_password: typing.Optional[builtins.str] = None,
        allow_local_admin_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_generate_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        change_sid: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        initscript: typing.Optional[builtins.str] = None,
        join_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        join_domain_account_ou: typing.Optional[builtins.str] = None,
        join_domain_name: typing.Optional[builtins.str] = None,
        join_domain_password: typing.Optional[builtins.str] = None,
        join_domain_user: typing.Optional[builtins.str] = None,
        join_org_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        must_change_password_on_first_login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        number_of_auto_logons: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param admin_password: Manually specify admin password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#admin_password VappVm#admin_password}
        :param allow_local_admin_password: Allow local administrator password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#allow_local_admin_password VappVm#allow_local_admin_password}
        :param auto_generate_password: Auto generate password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#auto_generate_password VappVm#auto_generate_password}
        :param change_sid: 'true' value will change SID. Applicable only for Windows VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#change_sid VappVm#change_sid}
        :param enabled: 'true' value will enable guest customization. It may occur on first boot or when 'force' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#enabled VappVm#enabled}
        :param force: 'true' value will cause the VM to reboot on every 'apply' operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#force VappVm#force}
        :param initscript: Script to run on initial boot or with customization.force=true set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#initscript VappVm#initscript}
        :param join_domain: Enable this VM to join a domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain VappVm#join_domain}
        :param join_domain_account_ou: Account organizational unit for domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_account_ou VappVm#join_domain_account_ou}
        :param join_domain_name: Custom domain name for join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_name VappVm#join_domain_name}
        :param join_domain_password: Password for custom domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_password VappVm#join_domain_password}
        :param join_domain_user: Username for custom domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_user VappVm#join_domain_user}
        :param join_org_domain: Use organization's domain for joining. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_org_domain VappVm#join_org_domain}
        :param must_change_password_on_first_login: Require Administrator to change password on first login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#must_change_password_on_first_login VappVm#must_change_password_on_first_login}
        :param number_of_auto_logons: Number of times to log on automatically. '0' - disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#number_of_auto_logons VappVm#number_of_auto_logons}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f98fbc7fff461ff2a23072f8794ac5d81d9ada72fa7ec17cdced480fc087586)
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument allow_local_admin_password", value=allow_local_admin_password, expected_type=type_hints["allow_local_admin_password"])
            check_type(argname="argument auto_generate_password", value=auto_generate_password, expected_type=type_hints["auto_generate_password"])
            check_type(argname="argument change_sid", value=change_sid, expected_type=type_hints["change_sid"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument initscript", value=initscript, expected_type=type_hints["initscript"])
            check_type(argname="argument join_domain", value=join_domain, expected_type=type_hints["join_domain"])
            check_type(argname="argument join_domain_account_ou", value=join_domain_account_ou, expected_type=type_hints["join_domain_account_ou"])
            check_type(argname="argument join_domain_name", value=join_domain_name, expected_type=type_hints["join_domain_name"])
            check_type(argname="argument join_domain_password", value=join_domain_password, expected_type=type_hints["join_domain_password"])
            check_type(argname="argument join_domain_user", value=join_domain_user, expected_type=type_hints["join_domain_user"])
            check_type(argname="argument join_org_domain", value=join_org_domain, expected_type=type_hints["join_org_domain"])
            check_type(argname="argument must_change_password_on_first_login", value=must_change_password_on_first_login, expected_type=type_hints["must_change_password_on_first_login"])
            check_type(argname="argument number_of_auto_logons", value=number_of_auto_logons, expected_type=type_hints["number_of_auto_logons"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if allow_local_admin_password is not None:
            self._values["allow_local_admin_password"] = allow_local_admin_password
        if auto_generate_password is not None:
            self._values["auto_generate_password"] = auto_generate_password
        if change_sid is not None:
            self._values["change_sid"] = change_sid
        if enabled is not None:
            self._values["enabled"] = enabled
        if force is not None:
            self._values["force"] = force
        if initscript is not None:
            self._values["initscript"] = initscript
        if join_domain is not None:
            self._values["join_domain"] = join_domain
        if join_domain_account_ou is not None:
            self._values["join_domain_account_ou"] = join_domain_account_ou
        if join_domain_name is not None:
            self._values["join_domain_name"] = join_domain_name
        if join_domain_password is not None:
            self._values["join_domain_password"] = join_domain_password
        if join_domain_user is not None:
            self._values["join_domain_user"] = join_domain_user
        if join_org_domain is not None:
            self._values["join_org_domain"] = join_org_domain
        if must_change_password_on_first_login is not None:
            self._values["must_change_password_on_first_login"] = must_change_password_on_first_login
        if number_of_auto_logons is not None:
            self._values["number_of_auto_logons"] = number_of_auto_logons

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''Manually specify admin password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#admin_password VappVm#admin_password}
        '''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_local_admin_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow local administrator password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#allow_local_admin_password VappVm#allow_local_admin_password}
        '''
        result = self._values.get("allow_local_admin_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_generate_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Auto generate password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#auto_generate_password VappVm#auto_generate_password}
        '''
        result = self._values.get("auto_generate_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def change_sid(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        ''''true' value will change SID. Applicable only for Windows VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#change_sid VappVm#change_sid}
        '''
        result = self._values.get("change_sid")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        ''''true' value will enable guest customization. It may occur on first boot or when 'force' is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#enabled VappVm#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        ''''true' value will cause the VM to reboot on every 'apply' operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#force VappVm#force}
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def initscript(self) -> typing.Optional[builtins.str]:
        '''Script to run on initial boot or with customization.force=true set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#initscript VappVm#initscript}
        '''
        result = self._values.get("initscript")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable this VM to join a domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain VappVm#join_domain}
        '''
        result = self._values.get("join_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def join_domain_account_ou(self) -> typing.Optional[builtins.str]:
        '''Account organizational unit for domain name join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_account_ou VappVm#join_domain_account_ou}
        '''
        result = self._values.get("join_domain_account_ou")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_domain_name(self) -> typing.Optional[builtins.str]:
        '''Custom domain name for join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_name VappVm#join_domain_name}
        '''
        result = self._values.get("join_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_domain_password(self) -> typing.Optional[builtins.str]:
        '''Password for custom domain name join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_password VappVm#join_domain_password}
        '''
        result = self._values.get("join_domain_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_domain_user(self) -> typing.Optional[builtins.str]:
        '''Username for custom domain name join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_domain_user VappVm#join_domain_user}
        '''
        result = self._values.get("join_domain_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_org_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use organization's domain for joining.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#join_org_domain VappVm#join_org_domain}
        '''
        result = self._values.get("join_org_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def must_change_password_on_first_login(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require Administrator to change password on first login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#must_change_password_on_first_login VappVm#must_change_password_on_first_login}
        '''
        result = self._values.get("must_change_password_on_first_login")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def number_of_auto_logons(self) -> typing.Optional[jsii.Number]:
        '''Number of times to log on automatically. '0' - disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#number_of_auto_logons VappVm#number_of_auto_logons}
        '''
        result = self._values.get("number_of_auto_logons")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmCustomization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmCustomizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmCustomizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73f9350fbf56abd1c147fadea2f232201d643ea62a1b1b60a8abbfd93690bff2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminPassword")
    def reset_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPassword", []))

    @jsii.member(jsii_name="resetAllowLocalAdminPassword")
    def reset_allow_local_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowLocalAdminPassword", []))

    @jsii.member(jsii_name="resetAutoGeneratePassword")
    def reset_auto_generate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoGeneratePassword", []))

    @jsii.member(jsii_name="resetChangeSid")
    def reset_change_sid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeSid", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetForce")
    def reset_force(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForce", []))

    @jsii.member(jsii_name="resetInitscript")
    def reset_initscript(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitscript", []))

    @jsii.member(jsii_name="resetJoinDomain")
    def reset_join_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJoinDomain", []))

    @jsii.member(jsii_name="resetJoinDomainAccountOu")
    def reset_join_domain_account_ou(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJoinDomainAccountOu", []))

    @jsii.member(jsii_name="resetJoinDomainName")
    def reset_join_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJoinDomainName", []))

    @jsii.member(jsii_name="resetJoinDomainPassword")
    def reset_join_domain_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJoinDomainPassword", []))

    @jsii.member(jsii_name="resetJoinDomainUser")
    def reset_join_domain_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJoinDomainUser", []))

    @jsii.member(jsii_name="resetJoinOrgDomain")
    def reset_join_org_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJoinOrgDomain", []))

    @jsii.member(jsii_name="resetMustChangePasswordOnFirstLogin")
    def reset_must_change_password_on_first_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMustChangePasswordOnFirstLogin", []))

    @jsii.member(jsii_name="resetNumberOfAutoLogons")
    def reset_number_of_auto_logons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfAutoLogons", []))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="allowLocalAdminPasswordInput")
    def allow_local_admin_password_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowLocalAdminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="autoGeneratePasswordInput")
    def auto_generate_password_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoGeneratePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="changeSidInput")
    def change_sid_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "changeSidInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="forceInput")
    def force_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceInput"))

    @builtins.property
    @jsii.member(jsii_name="initscriptInput")
    def initscript_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initscriptInput"))

    @builtins.property
    @jsii.member(jsii_name="joinDomainAccountOuInput")
    def join_domain_account_ou_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "joinDomainAccountOuInput"))

    @builtins.property
    @jsii.member(jsii_name="joinDomainInput")
    def join_domain_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "joinDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="joinDomainNameInput")
    def join_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "joinDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="joinDomainPasswordInput")
    def join_domain_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "joinDomainPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="joinDomainUserInput")
    def join_domain_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "joinDomainUserInput"))

    @builtins.property
    @jsii.member(jsii_name="joinOrgDomainInput")
    def join_org_domain_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "joinOrgDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="mustChangePasswordOnFirstLoginInput")
    def must_change_password_on_first_login_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mustChangePasswordOnFirstLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfAutoLogonsInput")
    def number_of_auto_logons_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfAutoLogonsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0dd16cf8b7c7dfe67c0a30530b4748b83b466532783ba6340f0d5a7f52b861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value)

    @builtins.property
    @jsii.member(jsii_name="allowLocalAdminPassword")
    def allow_local_admin_password(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowLocalAdminPassword"))

    @allow_local_admin_password.setter
    def allow_local_admin_password(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97604b8b6bb27432bca74a0d63da0f0687a603ad875655cc4dd093aa9ec0a883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowLocalAdminPassword", value)

    @builtins.property
    @jsii.member(jsii_name="autoGeneratePassword")
    def auto_generate_password(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoGeneratePassword"))

    @auto_generate_password.setter
    def auto_generate_password(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c09fd0ec0035d77a90b763051f48ad3ff0282395d0dd00dde43eba87615a2a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoGeneratePassword", value)

    @builtins.property
    @jsii.member(jsii_name="changeSid")
    def change_sid(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "changeSid"))

    @change_sid.setter
    def change_sid(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7861e2f06b4f7312ecf76ca55ec5697e8eb4c75737e00d3f4ae7f47b4ee10e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeSid", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__9e8718e32a5fd240c185b806f3096d4b14b4c5fb51eadfce2434303bfd0b1b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="force")
    def force(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "force"))

    @force.setter
    def force(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1dc8dee24dd276f62ba9758b96210f34463869d276512fc4d99ca668d31b5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "force", value)

    @builtins.property
    @jsii.member(jsii_name="initscript")
    def initscript(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initscript"))

    @initscript.setter
    def initscript(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5e0e4c3f8aa0e60e2158562aa2768562b8f0d53fef257d024d285c092eedb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initscript", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomain")
    def join_domain(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "joinDomain"))

    @join_domain.setter
    def join_domain(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1da6ac6daeab567502bc095bf378980065a11464ead1513f06b087831ba5e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomain", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomainAccountOu")
    def join_domain_account_ou(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "joinDomainAccountOu"))

    @join_domain_account_ou.setter
    def join_domain_account_ou(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6145b3830aecaf0b984fa8aa6315d43084ca08ee5c0dbbe847921e48d1028bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomainAccountOu", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomainName")
    def join_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "joinDomainName"))

    @join_domain_name.setter
    def join_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63aa3db089682b25cf4b7f9fc476a52908c3430d32bfc8220b5011a8136df2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomainName", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomainPassword")
    def join_domain_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "joinDomainPassword"))

    @join_domain_password.setter
    def join_domain_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c907a48e18207875782dcad61af863d6f61eaa58abf9a4f4266a67092a1b0cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomainPassword", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomainUser")
    def join_domain_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "joinDomainUser"))

    @join_domain_user.setter
    def join_domain_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05422e74a31171a871c9e42516a4b6c4fa25d14bcc9f8e0966781123532f2886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomainUser", value)

    @builtins.property
    @jsii.member(jsii_name="joinOrgDomain")
    def join_org_domain(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "joinOrgDomain"))

    @join_org_domain.setter
    def join_org_domain(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a2e05b2b5bf7051a21861fdce9030647b00da97034a28600b85cdf3951a10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinOrgDomain", value)

    @builtins.property
    @jsii.member(jsii_name="mustChangePasswordOnFirstLogin")
    def must_change_password_on_first_login(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mustChangePasswordOnFirstLogin"))

    @must_change_password_on_first_login.setter
    def must_change_password_on_first_login(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b507951d2a5fb832f18ce96d06e045a830a852630fdb2422e6e93d060e214fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mustChangePasswordOnFirstLogin", value)

    @builtins.property
    @jsii.member(jsii_name="numberOfAutoLogons")
    def number_of_auto_logons(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfAutoLogons"))

    @number_of_auto_logons.setter
    def number_of_auto_logons(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ebbd10bb807cb80e4b819e15ef63253d7a6d2a46b01eef6bff1d8133f6adce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfAutoLogons", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VappVmCustomization]:
        return typing.cast(typing.Optional[VappVmCustomization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VappVmCustomization]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312c52eb92a56098c51064d7119b1020e3f4d8ed95a5bf8b8ada59049a51c540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmDisk",
    jsii_struct_bases=[],
    name_mapping={
        "bus_number": "busNumber",
        "name": "name",
        "unit_number": "unitNumber",
    },
)
class VappVmDisk:
    def __init__(
        self,
        *,
        bus_number: builtins.str,
        name: builtins.str,
        unit_number: builtins.str,
    ) -> None:
        '''
        :param bus_number: Bus number on which to place the disk controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#bus_number VappVm#bus_number}
        :param name: Independent disk name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#name VappVm#name}
        :param unit_number: Unit number (slot) on the bus specified by BusNumber. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#unit_number VappVm#unit_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec57188dd7b329ea418e7b5693e9cca1b7cdc98cfc60884500f1cae133b9b5a)
            check_type(argname="argument bus_number", value=bus_number, expected_type=type_hints["bus_number"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument unit_number", value=unit_number, expected_type=type_hints["unit_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bus_number": bus_number,
            "name": name,
            "unit_number": unit_number,
        }

    @builtins.property
    def bus_number(self) -> builtins.str:
        '''Bus number on which to place the disk controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#bus_number VappVm#bus_number}
        '''
        result = self._values.get("bus_number")
        assert result is not None, "Required property 'bus_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Independent disk name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#name VappVm#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unit_number(self) -> builtins.str:
        '''Unit number (slot) on the bus specified by BusNumber.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#unit_number VappVm#unit_number}
        '''
        result = self._values.get("unit_number")
        assert result is not None, "Required property 'unit_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba520b7468243e8411b913ea101de24c763dae39d75cbe995ad1e6ff93b396ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappVmDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc58b330d2f18778da37e8628448dcc6c6903aa3864722cbd02a174c7f8fac07)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappVmDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1de09c4c1a6156c55d26325e80c0e1a5877dcc21f3f1b9343a8b84568aafeb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b549c2587cd54be985c9fef9c187d05a133565d5e5e7bbd8cdd333b2d9677a31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf519f6b473e67b694b7a3589ff5c0aefbb441153a1686e8959d451ac9528d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01482854897559d50c9d817eac441ceee6142c00e33c9f8c279325c8c5d0941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappVmDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffca42de243a280cde5d39595e60c683af868e0b9bbb84898522b26ca12173f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="sizeInMb")
    def size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInMb"))

    @builtins.property
    @jsii.member(jsii_name="busNumberInput")
    def bus_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "busNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="unitNumberInput")
    def unit_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="busNumber")
    def bus_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "busNumber"))

    @bus_number.setter
    def bus_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6f1114bc4f164dcc34a0f5363fb3519b8fc662fe49a2e546a190b715395152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busNumber", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b27c50e04c6d7172fa78c1d77cb0d6034bd54434268c1f6a7356bbee17c2bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="unitNumber")
    def unit_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unitNumber"))

    @unit_number.setter
    def unit_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8024cbc2f20e0626bffe7db8ac207b29e83a89a86dd158d4a33a23da90efa3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unitNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bede96a64ef9673b9cae30a3fa42aeceb8734aef911fcef0ebc1cd9f821ea5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmExtraConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class VappVmExtraConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmExtraConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmExtraConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmExtraConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__303ade64fd680fdd129b6c95d44589541e61ca8f80b2eecab033dade7365d44d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappVmExtraConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0433ad355ee8833b7c68ee4a9a01c6d9cb0d3a4334994cac52037f68ddfc714)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappVmExtraConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a7315bc3b26e933e941cd5f6e032d9a040e3991835c60f08e8b5bb67a18039)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dc1feada94b2e21a9f541efc8e0c36b040f7f58c6c4ed2a3cd01c31a3a38b49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60b69778e2f5113fd991a51ed14cac56b96e938a684021e4e582e12a6a087401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class VappVmExtraConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmExtraConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec5bf4dcecb92c363892c8ab85b542283d2809c3739eb551201e15dcac0f7087)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "required"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VappVmExtraConfig]:
        return typing.cast(typing.Optional[VappVmExtraConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VappVmExtraConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd14da6b061d3881e8971ce4e7579c53a093df7587b927a152903a6c5f2d97de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmInternalDisk",
    jsii_struct_bases=[],
    name_mapping={},
)
class VappVmInternalDisk:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmInternalDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmInternalDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmInternalDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__144a9cc0a2eb1eb21d01032f60cfd62fa2c37ea962b65e9ae8896acdc250b05c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappVmInternalDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0fcd1b57c4475bd101562d9cc848c891a0147c6630388d7ab11377e4afeaa1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappVmInternalDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41b6e04522e0dc9f4f465d138a30032661c500d6b550f7dca3e908b41743f47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__897215fab192725f997c95634e337a52f0980497282d52c68c045380379bdfea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02e7f0423575a0cc853db07d80e1bf539504def93d147109b5b6b060c375d34d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class VappVmInternalDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmInternalDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96a39e81bafcf37cf4b35a291af965e6bfe8b7abbb9462602fea7a82b0ca4b4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="busNumber")
    def bus_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "busNumber"))

    @builtins.property
    @jsii.member(jsii_name="busType")
    def bus_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "busType"))

    @builtins.property
    @jsii.member(jsii_name="diskId")
    def disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskId"))

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @builtins.property
    @jsii.member(jsii_name="sizeInMb")
    def size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInMb"))

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfile"))

    @builtins.property
    @jsii.member(jsii_name="thinProvisioned")
    def thin_provisioned(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "thinProvisioned"))

    @builtins.property
    @jsii.member(jsii_name="unitNumber")
    def unit_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unitNumber"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VappVmInternalDisk]:
        return typing.cast(typing.Optional[VappVmInternalDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VappVmInternalDisk]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3ddbfc481e3e87e416dd63bfaa1e8edf8fc791c294f04dc67fdad0f1b06d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "is_system": "isSystem",
        "key": "key",
        "type": "type",
        "user_access": "userAccess",
        "value": "value",
    },
)
class VappVmMetadataEntry:
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
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#is_system VappVm#is_system}
        :param key: Key of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#key VappVm#key}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#type VappVm#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#user_access VappVm#user_access}
        :param value: Value of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#value VappVm#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681921f9ad60ff6b504b0a0018191f1ca0b7d2b0766552796df034c864f13694)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#is_system VappVm#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#key VappVm#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#type VappVm#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#user_access VappVm#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#value VappVm#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmMetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmMetadataEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74937286fec50e7c18e4daa68c627670e40c25d87ec34eb0a7d83c9c38abe261)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappVmMetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6e66ffa7c340d09752b50c8769b2604cb3f436018c840c52911e3605065a09)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappVmMetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a9bc1d043b36fb0d79fda216bff17cae4e858bb7ed5fc04a202fea4a8c1e12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2de5b4354886498c38ccbf6d045df26f6a9354f2989bf68a683830e70cb05d43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b28f527ad71d94d857e295c2b3d88f9da89f72619097837764f78f50f826b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmMetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmMetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmMetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe9bca2b8b5e2d69da2b77b824d43064efc6160be4d3da7cfd4be4b6d5997ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappVmMetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmMetadataEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bac020863c1a318606d46c4ddc0831d5a471e05bc480c1923fe7ae41fee78c96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb24c0c40fd321d2af9e7d3abcf556d70d231e294dff86b2844b82052028b1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b186be1bef9696e4dd7c40d8bb2869caf8732ae2e0e7922fbcf30ff6beb2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9a53d4c5ff312ef9a5a9e7cccf336be860aa3874c3ec080832651f8d684fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4f423c875b78ca1f9a2c0efbb8cfd8d23cefbc9e2492aa61ee8521a72d11be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2f9df4b96839891310b6446fa3e4df1ecaead6a2a99cf5d3dfe0e970c16659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmMetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmMetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmMetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567b565ff9e73daaaada6f7d32e46702e2983498da7e16a08d69d57773893286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "ip_allocation_mode": "ipAllocationMode",
        "type": "type",
        "adapter_type": "adapterType",
        "connected": "connected",
        "ip": "ip",
        "is_primary": "isPrimary",
        "mac": "mac",
        "name": "name",
        "secondary_ip": "secondaryIp",
        "secondary_ip_allocation_mode": "secondaryIpAllocationMode",
    },
)
class VappVmNetwork:
    def __init__(
        self,
        *,
        ip_allocation_mode: builtins.str,
        type: builtins.str,
        adapter_type: typing.Optional[builtins.str] = None,
        connected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip: typing.Optional[builtins.str] = None,
        is_primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mac: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        secondary_ip: typing.Optional[builtins.str] = None,
        secondary_ip_allocation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_allocation_mode: IP address allocation mode. One of POOL, DHCP, MANUAL, NONE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#ip_allocation_mode VappVm#ip_allocation_mode}
        :param type: Network type to use: 'vapp', 'org' or 'none'. Use 'vapp' for vApp network, 'org' to attach Org VDC network. 'none' for empty NIC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#type VappVm#type}
        :param adapter_type: Network card adapter type. (e.g. 'E1000', 'E1000E', 'SRIOVETHERNETCARD', 'VMXNET3', 'PCNet32'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#adapter_type VappVm#adapter_type}
        :param connected: It defines if NIC is connected or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#connected VappVm#connected}
        :param ip: IP of the VM. Settings depend on ``ip_allocation_mode``. Omitted or empty for DHCP, POOL, NONE. Required for MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#ip VappVm#ip}
        :param is_primary: Set to true if network interface should be primary. First network card in the list will be primary by default Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#is_primary VappVm#is_primary}
        :param mac: Mac address of network interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#mac VappVm#mac}
        :param name: Name of the network this VM should connect to. Always required except for ``type`` ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#name VappVm#name}
        :param secondary_ip: Secondary (IPv6) IP of the VM. Settings depend on ``secondary_ip_allocation_mode``. Omitted or empty for DHCP, POOL, NONE. Required for MANUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#secondary_ip VappVm#secondary_ip}
        :param secondary_ip_allocation_mode: Secondary (IPv6) IP address allocation mode. One of POOL, DHCP, MANUAL, NONE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#secondary_ip_allocation_mode VappVm#secondary_ip_allocation_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd038b1d9a96d297c996d1c50eb2995803ff2807cfba78551d849ea411d3931b)
            check_type(argname="argument ip_allocation_mode", value=ip_allocation_mode, expected_type=type_hints["ip_allocation_mode"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument adapter_type", value=adapter_type, expected_type=type_hints["adapter_type"])
            check_type(argname="argument connected", value=connected, expected_type=type_hints["connected"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument is_primary", value=is_primary, expected_type=type_hints["is_primary"])
            check_type(argname="argument mac", value=mac, expected_type=type_hints["mac"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secondary_ip", value=secondary_ip, expected_type=type_hints["secondary_ip"])
            check_type(argname="argument secondary_ip_allocation_mode", value=secondary_ip_allocation_mode, expected_type=type_hints["secondary_ip_allocation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_allocation_mode": ip_allocation_mode,
            "type": type,
        }
        if adapter_type is not None:
            self._values["adapter_type"] = adapter_type
        if connected is not None:
            self._values["connected"] = connected
        if ip is not None:
            self._values["ip"] = ip
        if is_primary is not None:
            self._values["is_primary"] = is_primary
        if mac is not None:
            self._values["mac"] = mac
        if name is not None:
            self._values["name"] = name
        if secondary_ip is not None:
            self._values["secondary_ip"] = secondary_ip
        if secondary_ip_allocation_mode is not None:
            self._values["secondary_ip_allocation_mode"] = secondary_ip_allocation_mode

    @builtins.property
    def ip_allocation_mode(self) -> builtins.str:
        '''IP address allocation mode. One of POOL, DHCP, MANUAL, NONE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#ip_allocation_mode VappVm#ip_allocation_mode}
        '''
        result = self._values.get("ip_allocation_mode")
        assert result is not None, "Required property 'ip_allocation_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Network type to use: 'vapp', 'org' or 'none'.

        Use 'vapp' for vApp network, 'org' to attach Org VDC network. 'none' for empty NIC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#type VappVm#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def adapter_type(self) -> typing.Optional[builtins.str]:
        '''Network card adapter type. (e.g. 'E1000', 'E1000E', 'SRIOVETHERNETCARD', 'VMXNET3', 'PCNet32').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#adapter_type VappVm#adapter_type}
        '''
        result = self._values.get("adapter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connected(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''It defines if NIC is connected or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#connected VappVm#connected}
        '''
        result = self._values.get("connected")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip(self) -> typing.Optional[builtins.str]:
        '''IP of the VM. Settings depend on ``ip_allocation_mode``. Omitted or empty for DHCP, POOL, NONE. Required for MANUAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#ip VappVm#ip}
        '''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true if network interface should be primary.

        First network card in the list will be primary by default

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#is_primary VappVm#is_primary}
        '''
        result = self._values.get("is_primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mac(self) -> typing.Optional[builtins.str]:
        '''Mac address of network interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#mac VappVm#mac}
        '''
        result = self._values.get("mac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the network this VM should connect to. Always required except for ``type`` ``NONE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#name VappVm#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_ip(self) -> typing.Optional[builtins.str]:
        '''Secondary (IPv6) IP of the VM.

        Settings depend on ``secondary_ip_allocation_mode``. Omitted or empty for DHCP, POOL, NONE. Required for MANUAL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#secondary_ip VappVm#secondary_ip}
        '''
        result = self._values.get("secondary_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_ip_allocation_mode(self) -> typing.Optional[builtins.str]:
        '''Secondary (IPv6) IP address allocation mode. One of POOL, DHCP, MANUAL, NONE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#secondary_ip_allocation_mode VappVm#secondary_ip_allocation_mode}
        '''
        result = self._values.get("secondary_ip_allocation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79abe42c64e22daf4fa6eac44fcf116d3e0d2f87eb15a8a1021af75b59a088a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappVmNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0ef2d8a41015b1005568a6c664e2d2de806bfe39f69673d07a3ea321a8ee14)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappVmNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1797aaeddfbf9f87b7b6d6fb22062b595347d0d2dca2eb84cb18f43a0d8559cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15d2ffe5894ee05174ebb7c699dac628abdeb25944c794767706dce4cbab72e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f15bea3c8750a19664e381cacdefeb418ff6e47da6d8c25b558109cf08a09e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ef74c7704396a0a56636b80ebac9f9687aeb34f29c966235adfd201647d689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappVmNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c0ae35a9a518ccfaca696bc7d8197e27462713d51fba6a2ab6d3edb8ee84a19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdapterType")
    def reset_adapter_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdapterType", []))

    @jsii.member(jsii_name="resetConnected")
    def reset_connected(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnected", []))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

    @jsii.member(jsii_name="resetIsPrimary")
    def reset_is_primary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsPrimary", []))

    @jsii.member(jsii_name="resetMac")
    def reset_mac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMac", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSecondaryIp")
    def reset_secondary_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryIp", []))

    @jsii.member(jsii_name="resetSecondaryIpAllocationMode")
    def reset_secondary_ip_allocation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryIpAllocationMode", []))

    @builtins.property
    @jsii.member(jsii_name="adapterTypeInput")
    def adapter_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adapterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectedInput")
    def connected_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "connectedInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAllocationModeInput")
    def ip_allocation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAllocationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="isPrimaryInput")
    def is_primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPrimaryInput"))

    @builtins.property
    @jsii.member(jsii_name="macInput")
    def mac_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpAllocationModeInput")
    def secondary_ip_allocation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryIpAllocationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpInput")
    def secondary_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryIpInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="adapterType")
    def adapter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adapterType"))

    @adapter_type.setter
    def adapter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83707b6b0e2b68d657b5fa30345be24952ba304a76e4531c1253ad039f62d7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adapterType", value)

    @builtins.property
    @jsii.member(jsii_name="connected")
    def connected(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "connected"))

    @connected.setter
    def connected(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0003bd9de88c21c3c0f136ebcfa24b6c6ab94f736f224f7cd3496602e432bf75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connected", value)

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed20186b017e726a99d4535e9ea165b3ddb685cbcd75206ff935993f8a277f25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value)

    @builtins.property
    @jsii.member(jsii_name="ipAllocationMode")
    def ip_allocation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAllocationMode"))

    @ip_allocation_mode.setter
    def ip_allocation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ed49dc6c22d125be9bcb05d670c0bb443e71a8119466ec5a840b229fbb5759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAllocationMode", value)

    @builtins.property
    @jsii.member(jsii_name="isPrimary")
    def is_primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPrimary"))

    @is_primary.setter
    def is_primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e799ac89bc196bb260bd4768b10e016e780e22d6f0878b175bf1c3fbf567f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPrimary", value)

    @builtins.property
    @jsii.member(jsii_name="mac")
    def mac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mac"))

    @mac.setter
    def mac(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565538afe4a3503a23c993db10fc0db901043a9784fc95c0dad6b87893b952cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mac", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44ee55dca281080c9ed72f54ad392a9b0c266e9942638bcf47348215d5b2fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="secondaryIp")
    def secondary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryIp"))

    @secondary_ip.setter
    def secondary_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b807583e8d4bae88b69ea20d3544f1450039af799a7e90bfa573f5c03247287a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIp", value)

    @builtins.property
    @jsii.member(jsii_name="secondaryIpAllocationMode")
    def secondary_ip_allocation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryIpAllocationMode"))

    @secondary_ip_allocation_mode.setter
    def secondary_ip_allocation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654899a7796ac5d31231f842e255681f457f8436cd8fbb040acb7fd04a273ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIpAllocationMode", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91816fb7fd83eb2c994722119357c40800431afb8f3bfce5cb289bca2f07288f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8127b400e52c5c93c136c7bbf38d1cfe1a611ffe6fc65802154941c27bb76b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmOverrideTemplateDisk",
    jsii_struct_bases=[],
    name_mapping={
        "bus_number": "busNumber",
        "bus_type": "busType",
        "size_in_mb": "sizeInMb",
        "unit_number": "unitNumber",
        "iops": "iops",
        "storage_profile": "storageProfile",
    },
)
class VappVmOverrideTemplateDisk:
    def __init__(
        self,
        *,
        bus_number: jsii.Number,
        bus_type: builtins.str,
        size_in_mb: jsii.Number,
        unit_number: jsii.Number,
        iops: typing.Optional[jsii.Number] = None,
        storage_profile: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bus_number: The number of the SCSI or IDE controller itself. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#bus_number VappVm#bus_number}
        :param bus_type: The type of disk controller. Possible values: ide, parallel( LSI Logic Parallel SCSI), sas(LSI Logic SAS (SCSI)), paravirtual(Paravirtual (SCSI)), sata, nvme Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#bus_type VappVm#bus_type}
        :param size_in_mb: The size of the disk in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#size_in_mb VappVm#size_in_mb}
        :param unit_number: The device number on the SCSI or IDE controller of the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#unit_number VappVm#unit_number}
        :param iops: Specifies the IOPS for the disk. Default is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#iops VappVm#iops}
        :param storage_profile: Storage profile to override the VM default one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#storage_profile VappVm#storage_profile}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d7e12df5cee8333936ef5f9915cd85e30b7b63ab969a390ff54423bf30b7e6)
            check_type(argname="argument bus_number", value=bus_number, expected_type=type_hints["bus_number"])
            check_type(argname="argument bus_type", value=bus_type, expected_type=type_hints["bus_type"])
            check_type(argname="argument size_in_mb", value=size_in_mb, expected_type=type_hints["size_in_mb"])
            check_type(argname="argument unit_number", value=unit_number, expected_type=type_hints["unit_number"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument storage_profile", value=storage_profile, expected_type=type_hints["storage_profile"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bus_number": bus_number,
            "bus_type": bus_type,
            "size_in_mb": size_in_mb,
            "unit_number": unit_number,
        }
        if iops is not None:
            self._values["iops"] = iops
        if storage_profile is not None:
            self._values["storage_profile"] = storage_profile

    @builtins.property
    def bus_number(self) -> jsii.Number:
        '''The number of the SCSI or IDE controller itself.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#bus_number VappVm#bus_number}
        '''
        result = self._values.get("bus_number")
        assert result is not None, "Required property 'bus_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def bus_type(self) -> builtins.str:
        '''The type of disk controller.

        Possible values: ide, parallel( LSI Logic Parallel SCSI), sas(LSI Logic SAS (SCSI)), paravirtual(Paravirtual (SCSI)), sata, nvme

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#bus_type VappVm#bus_type}
        '''
        result = self._values.get("bus_type")
        assert result is not None, "Required property 'bus_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size_in_mb(self) -> jsii.Number:
        '''The size of the disk in MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#size_in_mb VappVm#size_in_mb}
        '''
        result = self._values.get("size_in_mb")
        assert result is not None, "Required property 'size_in_mb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def unit_number(self) -> jsii.Number:
        '''The device number on the SCSI or IDE controller of the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#unit_number VappVm#unit_number}
        '''
        result = self._values.get("unit_number")
        assert result is not None, "Required property 'unit_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''Specifies the IOPS for the disk. Default is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#iops VappVm#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_profile(self) -> typing.Optional[builtins.str]:
        '''Storage profile to override the VM default one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#storage_profile VappVm#storage_profile}
        '''
        result = self._values.get("storage_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmOverrideTemplateDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmOverrideTemplateDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmOverrideTemplateDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50e565d24b370e21793bc771af613acf2c3630071639e1080e993c398c9a9ed5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappVmOverrideTemplateDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee723b59ac0ac50c4eceaf05cad4d759d25410fc480426b9e242a24d41f0ab10)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappVmOverrideTemplateDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80546da2c5f7e2b59218fd9ea27866a25ed52cafc1ed867622dc3acc94da1a16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14c1cc018d08b8d26b8f7f507255f2c6ef6a9870f1131e5cf2b02cdbb6801909)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb474b7069dfc023ac367996cae49228ed52dee4f7a0fe0f19337591050d75e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmOverrideTemplateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmOverrideTemplateDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmOverrideTemplateDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f0f7e9059d70897bbcee8a42c5d313cf710fb102f20e0d46b56216529de654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappVmOverrideTemplateDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmOverrideTemplateDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13ce056405fe52cbb49913beacfa7fa30659ac1ea2c8155073851ab3c6560c91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIops")
    def reset_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIops", []))

    @jsii.member(jsii_name="resetStorageProfile")
    def reset_storage_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageProfile", []))

    @builtins.property
    @jsii.member(jsii_name="busNumberInput")
    def bus_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "busNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="busTypeInput")
    def bus_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "busTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="iopsInput")
    def iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iopsInput"))

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
    @jsii.member(jsii_name="busNumber")
    def bus_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "busNumber"))

    @bus_number.setter
    def bus_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a22d36fb3ac37c78d92fd8e7457f635586c75f13cac490ab4a4a5330893edfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busNumber", value)

    @builtins.property
    @jsii.member(jsii_name="busType")
    def bus_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "busType"))

    @bus_type.setter
    def bus_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180d75b129ade11c61083489a8c2de2792bb90248a12bb667c29bd4467e3d5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busType", value)

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @iops.setter
    def iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c0da1ea2daf317d98fa82b320f1bb0637a9db05c84ead96dc55ba7464d7147a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value)

    @builtins.property
    @jsii.member(jsii_name="sizeInMb")
    def size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInMb"))

    @size_in_mb.setter
    def size_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880864d80c0b6e368678494f0e277c115a1f13eb9508bb7e4165d0679de3e716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInMb", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfile"))

    @storage_profile.setter
    def storage_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b46980c9e0e1787be47419c5d184d738a2b8ee1c75808e7009b74ea5233782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfile", value)

    @builtins.property
    @jsii.member(jsii_name="unitNumber")
    def unit_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unitNumber"))

    @unit_number.setter
    def unit_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2952d6396af18f79d47f271cc86cfd96340df8ace83a3e9c9bff07f2adc5acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unitNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmOverrideTemplateDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmOverrideTemplateDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmOverrideTemplateDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a61ff0b78aeec22ff9d9d06902fce3def13021fefb959992559ed39383865d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vappVm.VappVmSetExtraConfig",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class VappVmSetExtraConfig:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: The key of the extra configuration item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#key VappVm#key}
        :param value: The value of the extra configuration item. Leaving the ``value`` field empty will result in the item deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#value VappVm#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e97801156ee8ce2b8db25ed2e349ccd9dc16dabbed20aa57ce5b637d8fb003c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the extra configuration item.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#key VappVm#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the extra configuration item. Leaving the ``value`` field empty will result in the item deletion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vapp_vm#value VappVm#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VappVmSetExtraConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VappVmSetExtraConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmSetExtraConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5496037da5b219601fcd7a148c6512a3e329edb0ff38ce1a8edd05f3807f7614)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VappVmSetExtraConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa749c927cbc3a29e75f254b6be1b1e7e3faadc9b26ef3c0e11279cc28b11d35)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VappVmSetExtraConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c5cad5e8695f2bb909e07373ee1903c49c6fb07053838199263f48e091c3ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a5287d80c3712ab531605ac9dadc5699c851880c5a244fccf997a7fb92465d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__936261751ff08b2b529cc6cf1bf3cbd7b78f36c2881d240e3cb5f6450b6d029c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmSetExtraConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmSetExtraConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmSetExtraConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec94865093ab783bd1d8094710478dee7e3d2739fbbf28830fdbbd786f58388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VappVmSetExtraConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vappVm.VappVmSetExtraConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7efbe640100cba4528ff05fa1f3bcea780d1368350d28780cde2e6c4264222bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b037250ea15adfeb90a21f73a9dca50d36eb72e6cea38d26ea45106cf5b89a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01c2bdfa3d081d7b00260623fd8537a6358ced2c360356844577edd56701bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmSetExtraConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmSetExtraConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmSetExtraConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ae52b14567eb019f65cf4f761919c5c816a0d7f0223c0ddc1644103c11509c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VappVm",
    "VappVmBootOptions",
    "VappVmBootOptionsOutputReference",
    "VappVmConfig",
    "VappVmCustomization",
    "VappVmCustomizationOutputReference",
    "VappVmDisk",
    "VappVmDiskList",
    "VappVmDiskOutputReference",
    "VappVmExtraConfig",
    "VappVmExtraConfigList",
    "VappVmExtraConfigOutputReference",
    "VappVmInternalDisk",
    "VappVmInternalDiskList",
    "VappVmInternalDiskOutputReference",
    "VappVmMetadataEntry",
    "VappVmMetadataEntryList",
    "VappVmMetadataEntryOutputReference",
    "VappVmNetwork",
    "VappVmNetworkList",
    "VappVmNetworkOutputReference",
    "VappVmOverrideTemplateDisk",
    "VappVmOverrideTemplateDiskList",
    "VappVmOverrideTemplateDiskOutputReference",
    "VappVmSetExtraConfig",
    "VappVmSetExtraConfigList",
    "VappVmSetExtraConfigOutputReference",
]

publication.publish()

def _typecheckingstub__b761d3283e39573700f0cc2d03f356fc8564c81cb1932738e8b11f9482d3fb98(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    vapp_name: builtins.str,
    accept_all_eulas: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    boot_image: typing.Optional[builtins.str] = None,
    boot_image_id: typing.Optional[builtins.str] = None,
    boot_options: typing.Optional[typing.Union[VappVmBootOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    catalog_name: typing.Optional[builtins.str] = None,
    computer_name: typing.Optional[builtins.str] = None,
    consolidate_disks_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    copy_from_vm_id: typing.Optional[builtins.str] = None,
    cpu_cores: typing.Optional[jsii.Number] = None,
    cpu_hot_add_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_limit: typing.Optional[jsii.Number] = None,
    cpu_priority: typing.Optional[builtins.str] = None,
    cpu_reservation: typing.Optional[jsii.Number] = None,
    cpus: typing.Optional[jsii.Number] = None,
    cpu_shares: typing.Optional[jsii.Number] = None,
    customization: typing.Optional[typing.Union[VappVmCustomization, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    expose_hardware_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    firmware: typing.Optional[builtins.str] = None,
    guest_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    hardware_version: typing.Optional[builtins.str] = None,
    href: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_hot_add_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
    memory_priority: typing.Optional[builtins.str] = None,
    memory_reservation: typing.Optional[jsii.Number] = None,
    memory_shares: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_dhcp_wait_seconds: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    override_template_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmOverrideTemplateDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement_policy_id: typing.Optional[builtins.str] = None,
    power_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_update_power_off: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    set_extra_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmSetExtraConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sizing_policy_id: typing.Optional[builtins.str] = None,
    storage_profile: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
    vapp_template_id: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
    vm_name_in_template: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__80db4eaf3326c46ee0b456c88a2c413399b7fc0b108495aaf72660c4dc587524(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e67874cbf716ceb441b3873fc4d79db03606f7d8e08224106080165459d1266(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cfc4aa6b73f714fc188d711d0015132671ec6d987a06dd4757d53e26ce23a0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmMetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cd3fef6979f7e79eedf5841b9a4a4fedbce1123a4acf322181a0a043dd9b8d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f045761e24d6995180b90d0a320f44ef2e2a1021cbd138a0aa67a09cbcd51085(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmOverrideTemplateDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13622ae8f2fb177c44317c1dc21376716288b503c63b663b216259de527df7c5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmSetExtraConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4392299d19c63d727e2875682bf72ede984bf5b48e25bcb4341310c2c13df8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925508e393ac3fa746a7eb516700317cac2db0865ca97589cd9306e548791677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02bee797d6e214bc8bdb05b905017f613bc3338ee60a5601d6fb3556a5e7e70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3502768eccaffe0c9b627c40cf4dc83e120b2ae62e1402de974b555f38515f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231a4d0933c961e94f29e29d4dd6f6f4f82078c9bc9c6a757aad34d7b5c8db89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7dee32eb35b7dbc71860ae4abfca1739875a47eb2abc9a86e2b35b3bfef6ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64d0d01a029822caebdf3da00dca8ba2e9b9cb7c4cd545b7973e52d06edd7db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2b8dc7b794bf83e1237c401339cacfe05050219a454bf7de8bf7a77f2d9c94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6b40be4f791a6d7f8a5904afecb4b6b2c3996f3ddcc68a98a3bd0fb63be78f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90a95620112768bb43008e835301aa5dfacb050f3246b926d76dfe91df6479f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1e108f7b019f9d54d02c6822e2a5d4ee40375275727a450b7c5852b0c12990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77458c019284910145482fd73eed4299e0d483d34615f13eaaf0ac93fa37ac8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ad1fc0e223fe293ac3d8d830ad84fe7e309683d60a010aeae0ea74379077be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11c7a7e8c93ab7240f571eae49292bd94ffd8773172df44d10e399a9dba0fda(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a472b1bac4aa1e94f14f93b21c6c3dee70fa1c0dbec5c8a3d41f85d1cde436a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394818d6c1ee800aac41f9fd6920f4649315932aa219f01e337634ca56bb0d6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c18e1b7002006a4b8515ae1892c0195a76875e4b82523515af061f3576e3d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a489319a9b5c4d226004ff2795ad1b593c000e2f53e89d59de6c738d53208df(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5b3e592b4eb1368c91f73fb4403bd70810e99bf36b0c0939d1c055f5c72723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8ff23804e87cd342d58d1ca09d50383e5d496204d50a79b0d482ea2bed947c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c4acb87a1b9cb834157a5a3c614b59442c3907cf09786388645f597445955e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0157496020119b7ecb146067a27448a214216b220a517751204ba0f3950f4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e950e021a52182ae0444d46800860bb75f95556afb9bc6513a199cc3cd16c43d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542cbbd7962f015092ee3ef944fee41f53478baf95c2a9b62f0956898b7bfbdd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531f72707f72912eace0c26e0314b34643d50c84749fa04ba14745ee16ec310d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056977b44c4ed3fa31e3ba946afd94abe6c89612ca6d838e856f473b4343cb1f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a78d6ec3bd4e28f0e49f8f02aaac0115cd00f38fc2d9a2df58426292f950f2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fa6bd760231bdaff8457ed65c942cbb95b4024905554e14e584aca97fbdd56(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d082338b9979a8e65565bacfed0e8ef156802a10dcfdb335906998a33be0742(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3522199e33ece4006e724549afd67cb6dcfedad8a5c72bfd5bc24e3508233e07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bbe4490d16672756fe45cd6e237284d75ef70c7a808c6fd612df7acff4239a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abcaba02546eed580cf7e8ed15560761c04f2d806c469a0f52b5c3885bc37de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3acf3e2374eac8f49fefe038b0088feecc19fa770a14439c34251c27404b33c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d90b9764354ddce6bcd8c566efc4ecc8b1241c447e479e644402148d80bcd8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105677873d137677bee33540ae876c98d74c51c816f4578329ef74c112c48801(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69774cf41219ba39fc709167729abe1abf8e9124a99b6d2eec96fbf829684e2d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a62721aa9313045121819d404bccfd27e9d1fcec295be7d8253b24a8a2c0f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d49a52cb1c816b0d52a406963ea3865edfe106c435ff5f3f366db6c9802091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d0ec25093799ce8a3670cb443ae3a01617271a22194a00f76a76ab7ac98fb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0c7cb588b1f0c8962806b728664d8a039d454111a641f51a1dd87b759e25fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a130a0cffdf2e00b7857fe33d4a8e19e117f8a0edfa66e2d69189ba75e7e957b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8fc204ed906d39c22f7f5943aae0b455fd0138cc75fb102088d36bbad8fab4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9866b7cf2be1d023770199fa03f39cc1173b8affc67558e04b226ef24098ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655f39ff0147b2d63186ada3907f78911441f00263045e6219fff7315ef82dee(
    *,
    boot_delay: typing.Optional[jsii.Number] = None,
    boot_retry_delay: typing.Optional[jsii.Number] = None,
    boot_retry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    efi_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enter_bios_setup_on_next_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1728bc23e6d9dd11cd1e414b19c819735c0a5a3e5d129fd8866ee098e75593(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38916c8dad9674dc547ed6c6d3342a62df97727d56bfb7a9c7f13257103b45d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0cee689f649525f9309c4b8593acb76a27a4c16558acc1da3630ce4dcb46c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5305fd9d020a34130d969a66f722ea6742e53193acc9a3378d4d8a4ee554217a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4c615cd5a5c67a43d9e64574a1674929002a9ebcb5f459f675596432a7ca8a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6169ecd46c91d9aa4aa47fbee4a51195e0d579cbaa543804e1cc954be631371(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a9a7d606937e342c28007263dc70575b07e43a5f00c7b7b3bcf970511afdbd(
    value: typing.Optional[VappVmBootOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5b7cc359649e1da25ffb423e375d54684be6544c08ffce7578ed772b598605(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    vapp_name: builtins.str,
    accept_all_eulas: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    boot_image: typing.Optional[builtins.str] = None,
    boot_image_id: typing.Optional[builtins.str] = None,
    boot_options: typing.Optional[typing.Union[VappVmBootOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    catalog_name: typing.Optional[builtins.str] = None,
    computer_name: typing.Optional[builtins.str] = None,
    consolidate_disks_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    copy_from_vm_id: typing.Optional[builtins.str] = None,
    cpu_cores: typing.Optional[jsii.Number] = None,
    cpu_hot_add_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_limit: typing.Optional[jsii.Number] = None,
    cpu_priority: typing.Optional[builtins.str] = None,
    cpu_reservation: typing.Optional[jsii.Number] = None,
    cpus: typing.Optional[jsii.Number] = None,
    cpu_shares: typing.Optional[jsii.Number] = None,
    customization: typing.Optional[typing.Union[VappVmCustomization, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    expose_hardware_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    firmware: typing.Optional[builtins.str] = None,
    guest_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    hardware_version: typing.Optional[builtins.str] = None,
    href: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_hot_add_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
    memory_priority: typing.Optional[builtins.str] = None,
    memory_reservation: typing.Optional[jsii.Number] = None,
    memory_shares: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_dhcp_wait_seconds: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    override_template_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmOverrideTemplateDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement_policy_id: typing.Optional[builtins.str] = None,
    power_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_update_power_off: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    set_extra_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VappVmSetExtraConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sizing_policy_id: typing.Optional[builtins.str] = None,
    storage_profile: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
    vapp_template_id: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
    vm_name_in_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f98fbc7fff461ff2a23072f8794ac5d81d9ada72fa7ec17cdced480fc087586(
    *,
    admin_password: typing.Optional[builtins.str] = None,
    allow_local_admin_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_generate_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    change_sid: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    initscript: typing.Optional[builtins.str] = None,
    join_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    join_domain_account_ou: typing.Optional[builtins.str] = None,
    join_domain_name: typing.Optional[builtins.str] = None,
    join_domain_password: typing.Optional[builtins.str] = None,
    join_domain_user: typing.Optional[builtins.str] = None,
    join_org_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    must_change_password_on_first_login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    number_of_auto_logons: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f9350fbf56abd1c147fadea2f232201d643ea62a1b1b60a8abbfd93690bff2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0dd16cf8b7c7dfe67c0a30530b4748b83b466532783ba6340f0d5a7f52b861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97604b8b6bb27432bca74a0d63da0f0687a603ad875655cc4dd093aa9ec0a883(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c09fd0ec0035d77a90b763051f48ad3ff0282395d0dd00dde43eba87615a2a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7861e2f06b4f7312ecf76ca55ec5697e8eb4c75737e00d3f4ae7f47b4ee10e82(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8718e32a5fd240c185b806f3096d4b14b4c5fb51eadfce2434303bfd0b1b51(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dc8dee24dd276f62ba9758b96210f34463869d276512fc4d99ca668d31b5d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5e0e4c3f8aa0e60e2158562aa2768562b8f0d53fef257d024d285c092eedb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1da6ac6daeab567502bc095bf378980065a11464ead1513f06b087831ba5e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6145b3830aecaf0b984fa8aa6315d43084ca08ee5c0dbbe847921e48d1028bfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63aa3db089682b25cf4b7f9fc476a52908c3430d32bfc8220b5011a8136df2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c907a48e18207875782dcad61af863d6f61eaa58abf9a4f4266a67092a1b0cc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05422e74a31171a871c9e42516a4b6c4fa25d14bcc9f8e0966781123532f2886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a2e05b2b5bf7051a21861fdce9030647b00da97034a28600b85cdf3951a10c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b507951d2a5fb832f18ce96d06e045a830a852630fdb2422e6e93d060e214fcb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ebbd10bb807cb80e4b819e15ef63253d7a6d2a46b01eef6bff1d8133f6adce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312c52eb92a56098c51064d7119b1020e3f4d8ed95a5bf8b8ada59049a51c540(
    value: typing.Optional[VappVmCustomization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec57188dd7b329ea418e7b5693e9cca1b7cdc98cfc60884500f1cae133b9b5a(
    *,
    bus_number: builtins.str,
    name: builtins.str,
    unit_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba520b7468243e8411b913ea101de24c763dae39d75cbe995ad1e6ff93b396ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc58b330d2f18778da37e8628448dcc6c6903aa3864722cbd02a174c7f8fac07(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1de09c4c1a6156c55d26325e80c0e1a5877dcc21f3f1b9343a8b84568aafeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b549c2587cd54be985c9fef9c187d05a133565d5e5e7bbd8cdd333b2d9677a31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf519f6b473e67b694b7a3589ff5c0aefbb441153a1686e8959d451ac9528d7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01482854897559d50c9d817eac441ceee6142c00e33c9f8c279325c8c5d0941(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffca42de243a280cde5d39595e60c683af868e0b9bbb84898522b26ca12173f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6f1114bc4f164dcc34a0f5363fb3519b8fc662fe49a2e546a190b715395152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b27c50e04c6d7172fa78c1d77cb0d6034bd54434268c1f6a7356bbee17c2bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8024cbc2f20e0626bffe7db8ac207b29e83a89a86dd158d4a33a23da90efa3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bede96a64ef9673b9cae30a3fa42aeceb8734aef911fcef0ebc1cd9f821ea5d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303ade64fd680fdd129b6c95d44589541e61ca8f80b2eecab033dade7365d44d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0433ad355ee8833b7c68ee4a9a01c6d9cb0d3a4334994cac52037f68ddfc714(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a7315bc3b26e933e941cd5f6e032d9a040e3991835c60f08e8b5bb67a18039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc1feada94b2e21a9f541efc8e0c36b040f7f58c6c4ed2a3cd01c31a3a38b49(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b69778e2f5113fd991a51ed14cac56b96e938a684021e4e582e12a6a087401(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5bf4dcecb92c363892c8ab85b542283d2809c3739eb551201e15dcac0f7087(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd14da6b061d3881e8971ce4e7579c53a093df7587b927a152903a6c5f2d97de(
    value: typing.Optional[VappVmExtraConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144a9cc0a2eb1eb21d01032f60cfd62fa2c37ea962b65e9ae8896acdc250b05c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0fcd1b57c4475bd101562d9cc848c891a0147c6630388d7ab11377e4afeaa1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41b6e04522e0dc9f4f465d138a30032661c500d6b550f7dca3e908b41743f47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897215fab192725f997c95634e337a52f0980497282d52c68c045380379bdfea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e7f0423575a0cc853db07d80e1bf539504def93d147109b5b6b060c375d34d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a39e81bafcf37cf4b35a291af965e6bfe8b7abbb9462602fea7a82b0ca4b4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3ddbfc481e3e87e416dd63bfaa1e8edf8fc791c294f04dc67fdad0f1b06d22(
    value: typing.Optional[VappVmInternalDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681921f9ad60ff6b504b0a0018191f1ca0b7d2b0766552796df034c864f13694(
    *,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74937286fec50e7c18e4daa68c627670e40c25d87ec34eb0a7d83c9c38abe261(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6e66ffa7c340d09752b50c8769b2604cb3f436018c840c52911e3605065a09(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a9bc1d043b36fb0d79fda216bff17cae4e858bb7ed5fc04a202fea4a8c1e12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de5b4354886498c38ccbf6d045df26f6a9354f2989bf68a683830e70cb05d43(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b28f527ad71d94d857e295c2b3d88f9da89f72619097837764f78f50f826b11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe9bca2b8b5e2d69da2b77b824d43064efc6160be4d3da7cfd4be4b6d5997ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmMetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac020863c1a318606d46c4ddc0831d5a471e05bc480c1923fe7ae41fee78c96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb24c0c40fd321d2af9e7d3abcf556d70d231e294dff86b2844b82052028b1ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b186be1bef9696e4dd7c40d8bb2869caf8732ae2e0e7922fbcf30ff6beb2ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9a53d4c5ff312ef9a5a9e7cccf336be860aa3874c3ec080832651f8d684fc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4f423c875b78ca1f9a2c0efbb8cfd8d23cefbc9e2492aa61ee8521a72d11be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2f9df4b96839891310b6446fa3e4df1ecaead6a2a99cf5d3dfe0e970c16659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567b565ff9e73daaaada6f7d32e46702e2983498da7e16a08d69d57773893286(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmMetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd038b1d9a96d297c996d1c50eb2995803ff2807cfba78551d849ea411d3931b(
    *,
    ip_allocation_mode: builtins.str,
    type: builtins.str,
    adapter_type: typing.Optional[builtins.str] = None,
    connected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip: typing.Optional[builtins.str] = None,
    is_primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mac: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    secondary_ip: typing.Optional[builtins.str] = None,
    secondary_ip_allocation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79abe42c64e22daf4fa6eac44fcf116d3e0d2f87eb15a8a1021af75b59a088a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0ef2d8a41015b1005568a6c664e2d2de806bfe39f69673d07a3ea321a8ee14(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1797aaeddfbf9f87b7b6d6fb22062b595347d0d2dca2eb84cb18f43a0d8559cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15d2ffe5894ee05174ebb7c699dac628abdeb25944c794767706dce4cbab72e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f15bea3c8750a19664e381cacdefeb418ff6e47da6d8c25b558109cf08a09e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ef74c7704396a0a56636b80ebac9f9687aeb34f29c966235adfd201647d689(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0ae35a9a518ccfaca696bc7d8197e27462713d51fba6a2ab6d3edb8ee84a19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83707b6b0e2b68d657b5fa30345be24952ba304a76e4531c1253ad039f62d7bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0003bd9de88c21c3c0f136ebcfa24b6c6ab94f736f224f7cd3496602e432bf75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed20186b017e726a99d4535e9ea165b3ddb685cbcd75206ff935993f8a277f25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ed49dc6c22d125be9bcb05d670c0bb443e71a8119466ec5a840b229fbb5759(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e799ac89bc196bb260bd4768b10e016e780e22d6f0878b175bf1c3fbf567f2d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565538afe4a3503a23c993db10fc0db901043a9784fc95c0dad6b87893b952cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44ee55dca281080c9ed72f54ad392a9b0c266e9942638bcf47348215d5b2fe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b807583e8d4bae88b69ea20d3544f1450039af799a7e90bfa573f5c03247287a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654899a7796ac5d31231f842e255681f457f8436cd8fbb040acb7fd04a273ec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91816fb7fd83eb2c994722119357c40800431afb8f3bfce5cb289bca2f07288f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8127b400e52c5c93c136c7bbf38d1cfe1a611ffe6fc65802154941c27bb76b67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmNetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d7e12df5cee8333936ef5f9915cd85e30b7b63ab969a390ff54423bf30b7e6(
    *,
    bus_number: jsii.Number,
    bus_type: builtins.str,
    size_in_mb: jsii.Number,
    unit_number: jsii.Number,
    iops: typing.Optional[jsii.Number] = None,
    storage_profile: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e565d24b370e21793bc771af613acf2c3630071639e1080e993c398c9a9ed5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee723b59ac0ac50c4eceaf05cad4d759d25410fc480426b9e242a24d41f0ab10(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80546da2c5f7e2b59218fd9ea27866a25ed52cafc1ed867622dc3acc94da1a16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c1cc018d08b8d26b8f7f507255f2c6ef6a9870f1131e5cf2b02cdbb6801909(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb474b7069dfc023ac367996cae49228ed52dee4f7a0fe0f19337591050d75e9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f0f7e9059d70897bbcee8a42c5d313cf710fb102f20e0d46b56216529de654(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmOverrideTemplateDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ce056405fe52cbb49913beacfa7fa30659ac1ea2c8155073851ab3c6560c91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a22d36fb3ac37c78d92fd8e7457f635586c75f13cac490ab4a4a5330893edfe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180d75b129ade11c61083489a8c2de2792bb90248a12bb667c29bd4467e3d5cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0da1ea2daf317d98fa82b320f1bb0637a9db05c84ead96dc55ba7464d7147a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880864d80c0b6e368678494f0e277c115a1f13eb9508bb7e4165d0679de3e716(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b46980c9e0e1787be47419c5d184d738a2b8ee1c75808e7009b74ea5233782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2952d6396af18f79d47f271cc86cfd96340df8ace83a3e9c9bff07f2adc5acb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a61ff0b78aeec22ff9d9d06902fce3def13021fefb959992559ed39383865d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmOverrideTemplateDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e97801156ee8ce2b8db25ed2e349ccd9dc16dabbed20aa57ce5b637d8fb003c(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5496037da5b219601fcd7a148c6512a3e329edb0ff38ce1a8edd05f3807f7614(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa749c927cbc3a29e75f254b6be1b1e7e3faadc9b26ef3c0e11279cc28b11d35(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c5cad5e8695f2bb909e07373ee1903c49c6fb07053838199263f48e091c3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a5287d80c3712ab531605ac9dadc5699c851880c5a244fccf997a7fb92465d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936261751ff08b2b529cc6cf1bf3cbd7b78f36c2881d240e3cb5f6450b6d029c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec94865093ab783bd1d8094710478dee7e3d2739fbbf28830fdbbd786f58388(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VappVmSetExtraConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7efbe640100cba4528ff05fa1f3bcea780d1368350d28780cde2e6c4264222bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b037250ea15adfeb90a21f73a9dca50d36eb72e6cea38d26ea45106cf5b89a83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01c2bdfa3d081d7b00260623fd8537a6358ced2c360356844577edd56701bea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ae52b14567eb019f65cf4f761919c5c816a0d7f0223c0ddc1644103c11509c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VappVmSetExtraConfig]],
) -> None:
    """Type checking stubs"""
    pass
