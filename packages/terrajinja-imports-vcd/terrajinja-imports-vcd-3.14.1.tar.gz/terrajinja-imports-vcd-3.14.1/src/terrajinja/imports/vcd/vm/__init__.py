'''
# `vcd_vm`

Refer to the Terraform Registry for docs: [`vcd_vm`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm).
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


class Vm(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.Vm",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm vcd_vm}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        accept_all_eulas: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        boot_image: typing.Optional[builtins.str] = None,
        boot_image_id: typing.Optional[builtins.str] = None,
        boot_options: typing.Optional[typing.Union["VmBootOptions", typing.Dict[builtins.str, typing.Any]]] = None,
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
        customization: typing.Optional[typing.Union["VmCustomization", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_dhcp_wait_seconds: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        override_template_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmOverrideTemplateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement_policy_id: typing.Optional[builtins.str] = None,
        power_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_update_power_off: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        set_extra_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmSetExtraConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sizing_policy_id: typing.Optional[builtins.str] = None,
        storage_profile: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
        vapp_name: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm vcd_vm} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A name for the VM, unique within the vApp. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#name Vm#name}
        :param accept_all_eulas: Automatically accept EULA if OVA has it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#accept_all_eulas Vm#accept_all_eulas}
        :param boot_image: Media name to add as boot image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_image Vm#boot_image}
        :param boot_image_id: The URN of the media to use as boot image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_image_id Vm#boot_image_id}
        :param boot_options: boot_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_options Vm#boot_options}
        :param catalog_name: The catalog name in which to find the given vApp Template or media for boot_image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#catalog_name Vm#catalog_name}
        :param computer_name: Computer name to assign to this virtual machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#computer_name Vm#computer_name}
        :param consolidate_disks_on_create: Consolidates disks during creation and allows to change disk size using 'override_template_disk' in fast provisioned VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#consolidate_disks_on_create Vm#consolidate_disks_on_create}
        :param copy_from_vm_id: Source VM that should be copied from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#copy_from_vm_id Vm#copy_from_vm_id}
        :param cpu_cores: The number of cores per socket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_cores Vm#cpu_cores}
        :param cpu_hot_add_enabled: True if the virtual machine supports addition of virtual CPUs while powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_hot_add_enabled Vm#cpu_hot_add_enabled}
        :param cpu_limit: The limit for how much of CPU can be consumed on the underlying virtualization infrastructure. This is only valid when the resource allocation is not unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_limit Vm#cpu_limit}
        :param cpu_priority: Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_priority Vm#cpu_priority}
        :param cpu_reservation: The amount of MHz reservation on the underlying virtualization infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_reservation Vm#cpu_reservation}
        :param cpus: The number of virtual CPUs to allocate to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpus Vm#cpus}
        :param cpu_shares: Custom priority for the resource. This is a read-only, unless the ``cpu_priority`` is CUSTOM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_shares Vm#cpu_shares}
        :param customization: customization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#customization Vm#customization}
        :param description: The VM description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#description Vm#description}
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#disk Vm#disk}
        :param expose_hardware_virtualization: Expose hardware-assisted CPU virtualization to guest OS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#expose_hardware_virtualization Vm#expose_hardware_virtualization}
        :param firmware: Firmware of the VM. Can be either EFI or BIOS, availabilitydepending on the os_type argument. If unset, is set to 'bios' by default. Changing the value when ``power_on`` is set to true, will cause a reboot of the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#firmware Vm#firmware}
        :param guest_properties: Key/value settings for guest properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#guest_properties Vm#guest_properties}
        :param hardware_version: Virtual Hardware Version (e.g.``vmx-14``, ``vmx-13``, ``vmx-12``, etc.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#hardware_version Vm#hardware_version}
        :param href: VM Hyper Reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#href Vm#href}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#id Vm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param memory: The amount of RAM (in MB) to allocate to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory Vm#memory}
        :param memory_hot_add_enabled: True if the virtual machine supports addition of memory while powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_hot_add_enabled Vm#memory_hot_add_enabled}
        :param memory_limit: The limit for how much of memory can be consumed on the underlying virtualization infrastructure. This is only valid when the resource allocation is not unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_limit Vm#memory_limit}
        :param memory_priority: Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_priority Vm#memory_priority}
        :param memory_reservation: The amount of RAM (in MB) reservation on the underlying virtualization infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_reservation Vm#memory_reservation}
        :param memory_shares: Custom priority for the resource. This is a read-only, unless the ``memory_priority`` is CUSTOM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_shares Vm#memory_shares}
        :param metadata: Key value map of metadata to assign to this VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#metadata Vm#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#metadata_entry Vm#metadata_entry}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#network Vm#network}
        :param network_dhcp_wait_seconds: Optional number of seconds to try and wait for DHCP IP (valid for 'network' block only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#network_dhcp_wait_seconds Vm#network_dhcp_wait_seconds}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#org Vm#org}
        :param os_type: Operating System type. Possible values can be found in documentation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#os_type Vm#os_type}
        :param override_template_disk: override_template_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#override_template_disk Vm#override_template_disk}
        :param placement_policy_id: VM placement policy ID. Has to be assigned to Org VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#placement_policy_id Vm#placement_policy_id}
        :param power_on: A boolean value stating if this VM should be powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#power_on Vm#power_on}
        :param prevent_update_power_off: True if the update of resource should fail when virtual machine power off needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#prevent_update_power_off Vm#prevent_update_power_off}
        :param security_tags: Security tags to assign to this VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#security_tags Vm#security_tags}
        :param set_extra_config: set_extra_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#set_extra_config Vm#set_extra_config}
        :param sizing_policy_id: VM sizing policy ID. Has to be assigned to Org VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#sizing_policy_id Vm#sizing_policy_id}
        :param storage_profile: Storage profile to override the default one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#storage_profile Vm#storage_profile}
        :param template_name: The name of the vApp Template to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#template_name Vm#template_name}
        :param vapp_name: The vApp this VM belongs to - Required, unless it is a standalone VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vapp_name Vm#vapp_name}
        :param vapp_template_id: The URN of the vApp Template to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vapp_template_id Vm#vapp_template_id}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vdc Vm#vdc}
        :param vm_name_in_template: The name of the VM in vApp Template to use. In cases when vApp template has more than one VM Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vm_name_in_template Vm#vm_name_in_template}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc50c0fa60f0c8bb5d10f4dadfd9290cc78ea9d8d18c648ada4b784f3dabd3d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VmConfig(
            name=name,
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
            vapp_name=vapp_name,
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
        '''Generates CDKTF code for importing a Vm resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Vm to import.
        :param import_from_id: The id of the existing Vm that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Vm to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6c9779d97e9abc580fe2ee4ff5f6d42b4a7cff1ae0a93bf79350300b6f8651)
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
        :param boot_delay: Number of milliseconds to wait between powering-on and booting the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_delay Vm#boot_delay}
        :param boot_retry_delay: Delay in milliseconds before a boot retry. Only works if 'boot_retry_enabled' is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_retry_delay Vm#boot_retry_delay}
        :param boot_retry_enabled: If set to true, a VM that fails to boot will try again after the 'boot_retry_delay' time period has expired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_retry_enabled Vm#boot_retry_enabled}
        :param efi_secure_boot: If set to true, enables EFI Secure Boot for the VM. Can only be changed when the VM is powered off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#efi_secure_boot Vm#efi_secure_boot}
        :param enter_bios_setup_on_next_boot: If set to true, the VM will enter BIOS setup on next boot. If a VM is powered on, the field will be set to ``false`` by VCD and Terraform will return a non-empty plan Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#enter_bios_setup_on_next_boot Vm#enter_bios_setup_on_next_boot}
        '''
        value = VmBootOptions(
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
        :param admin_password: Manually specify admin password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#admin_password Vm#admin_password}
        :param allow_local_admin_password: Allow local administrator password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#allow_local_admin_password Vm#allow_local_admin_password}
        :param auto_generate_password: Auto generate password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#auto_generate_password Vm#auto_generate_password}
        :param change_sid: 'true' value will change SID. Applicable only for Windows VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#change_sid Vm#change_sid}
        :param enabled: 'true' value will enable guest customization. It may occur on first boot or when 'force' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#enabled Vm#enabled}
        :param force: 'true' value will cause the VM to reboot on every 'apply' operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#force Vm#force}
        :param initscript: Script to run on initial boot or with customization.force=true set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#initscript Vm#initscript}
        :param join_domain: Enable this VM to join a domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain Vm#join_domain}
        :param join_domain_account_ou: Account organizational unit for domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_account_ou Vm#join_domain_account_ou}
        :param join_domain_name: Custom domain name for join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_name Vm#join_domain_name}
        :param join_domain_password: Password for custom domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_password Vm#join_domain_password}
        :param join_domain_user: Username for custom domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_user Vm#join_domain_user}
        :param join_org_domain: Use organization's domain for joining. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_org_domain Vm#join_org_domain}
        :param must_change_password_on_first_login: Require Administrator to change password on first login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#must_change_password_on_first_login Vm#must_change_password_on_first_login}
        :param number_of_auto_logons: Number of times to log on automatically. '0' - disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#number_of_auto_logons Vm#number_of_auto_logons}
        '''
        value = VmCustomization(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec60ba25b4ffde125cb2555b8dc37ecc57f790ad7fa68d077b16b9a5892ef1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisk", [value]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmMetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beaf7abd77d1eb255eee6972c918510db69002de3a61fb1b53ebb71a0008e77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmNetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37845dcdfca62db80c0b61e95583586ca22263da2d7ee502bdab544a0c0172e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putOverrideTemplateDisk")
    def put_override_template_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmOverrideTemplateDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de20850974a745e75d10680db95af512be5ed540295a520b1779aa6e1695dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOverrideTemplateDisk", [value]))

    @jsii.member(jsii_name="putSetExtraConfig")
    def put_set_extra_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmSetExtraConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66cdd386609fc7789da5e4069ca9fa074b292eeecccc5e0b8efba0175b1bcae)
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

    @jsii.member(jsii_name="resetVappName")
    def reset_vapp_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVappName", []))

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
    def boot_options(self) -> "VmBootOptionsOutputReference":
        return typing.cast("VmBootOptionsOutputReference", jsii.get(self, "bootOptions"))

    @builtins.property
    @jsii.member(jsii_name="customization")
    def customization(self) -> "VmCustomizationOutputReference":
        return typing.cast("VmCustomizationOutputReference", jsii.get(self, "customization"))

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> "VmDiskList":
        return typing.cast("VmDiskList", jsii.get(self, "disk"))

    @builtins.property
    @jsii.member(jsii_name="extraConfig")
    def extra_config(self) -> "VmExtraConfigList":
        return typing.cast("VmExtraConfigList", jsii.get(self, "extraConfig"))

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
    def internal_disk(self) -> "VmInternalDiskList":
        return typing.cast("VmInternalDiskList", jsii.get(self, "internalDisk"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "VmMetadataEntryList":
        return typing.cast("VmMetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "VmNetworkList":
        return typing.cast("VmNetworkList", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="overrideTemplateDisk")
    def override_template_disk(self) -> "VmOverrideTemplateDiskList":
        return typing.cast("VmOverrideTemplateDiskList", jsii.get(self, "overrideTemplateDisk"))

    @builtins.property
    @jsii.member(jsii_name="setExtraConfig")
    def set_extra_config(self) -> "VmSetExtraConfigList":
        return typing.cast("VmSetExtraConfigList", jsii.get(self, "setExtraConfig"))

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
    def boot_options_input(self) -> typing.Optional["VmBootOptions"]:
        return typing.cast(typing.Optional["VmBootOptions"], jsii.get(self, "bootOptionsInput"))

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
    def customization_input(self) -> typing.Optional["VmCustomization"]:
        return typing.cast(typing.Optional["VmCustomization"], jsii.get(self, "customizationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmDisk"]]], jsii.get(self, "diskInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmMetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmMetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmNetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmNetwork"]]], jsii.get(self, "networkInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmOverrideTemplateDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmOverrideTemplateDisk"]]], jsii.get(self, "overrideTemplateDiskInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmSetExtraConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmSetExtraConfig"]]], jsii.get(self, "setExtraConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6709bb2ea497ab1450b479ab9911e5d0eafe36cb25c9afcb8a5cce455ac0a06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptAllEulas", value)

    @builtins.property
    @jsii.member(jsii_name="bootImage")
    def boot_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootImage"))

    @boot_image.setter
    def boot_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289a86392a6ea9955e01976ec0547cad84a651a769e790359e98151411ee9bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootImage", value)

    @builtins.property
    @jsii.member(jsii_name="bootImageId")
    def boot_image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootImageId"))

    @boot_image_id.setter
    def boot_image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c13a27f7b8454d56ab2d62bc575b59e05eaabf622106e6a1bf623f73e15a720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootImageId", value)

    @builtins.property
    @jsii.member(jsii_name="catalogName")
    def catalog_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogName"))

    @catalog_name.setter
    def catalog_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c063894febc4654ef085a2afd0a86dd014e8245f5c24611c99105169e3fc8ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalogName", value)

    @builtins.property
    @jsii.member(jsii_name="computerName")
    def computer_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computerName"))

    @computer_name.setter
    def computer_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b5c8ea11125936b756caa57f13f19f54c69bdccc6ad45400109b786f652afe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70bcdb8216ab0b316b965abd47ffaf91c7003eeefe5d581bb9afe1c0b3243378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consolidateDisksOnCreate", value)

    @builtins.property
    @jsii.member(jsii_name="copyFromVmId")
    def copy_from_vm_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyFromVmId"))

    @copy_from_vm_id.setter
    def copy_from_vm_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55096a3ae23e6124ebf06127fb1522885e490491589776e6b4b87f907968804f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyFromVmId", value)

    @builtins.property
    @jsii.member(jsii_name="cpuCores")
    def cpu_cores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCores"))

    @cpu_cores.setter
    def cpu_cores(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346ff2caafeb5f5158f742f8bd26f5a6eee3b01f85d9e4c16f3f37452694036d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__630b7133e3f0e3303e691b699ba8f2350e6c60f2883534088b39083bdf58acd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuHotAddEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cpuLimit")
    def cpu_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuLimit"))

    @cpu_limit.setter
    def cpu_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714acb7d1e06990ec2119a7016fb38b159a1c04a789b7fb2c3e2d304956dc80d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuLimit", value)

    @builtins.property
    @jsii.member(jsii_name="cpuPriority")
    def cpu_priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuPriority"))

    @cpu_priority.setter
    def cpu_priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ce4df7f2cc51befb1ba6d66e6678aec4636fbbf561a2a46e9ca0caf2e9ee3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuPriority", value)

    @builtins.property
    @jsii.member(jsii_name="cpuReservation")
    def cpu_reservation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuReservation"))

    @cpu_reservation.setter
    def cpu_reservation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333f69c03d434f15f68c55d8154ac84f86dc1b61a42bcbf7008615906546095f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuReservation", value)

    @builtins.property
    @jsii.member(jsii_name="cpus")
    def cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpus"))

    @cpus.setter
    def cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c8710627cf32e1f033b96386f3cbbe7abf9cee88ee173accea37837d91c7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value)

    @builtins.property
    @jsii.member(jsii_name="cpuShares")
    def cpu_shares(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuShares"))

    @cpu_shares.setter
    def cpu_shares(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc1635f591721089756cfbb6d49d3e0eecb58b6bd36d72dbd361a50a7922f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuShares", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd34f3a2653d2720a16f44b946bcdd7293d57657c4c5d2aa0068c56dac45fa9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d57c24022c6966d9abc61df56d197fb4432c9724b02f475e51b802337c04722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposeHardwareVirtualization", value)

    @builtins.property
    @jsii.member(jsii_name="firmware")
    def firmware(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firmware"))

    @firmware.setter
    def firmware(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3e6bfbf003c279dfbbd6ae5b80ad289454e0a55a74626e04964ecfa95ca706)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a38aeba05b5cbc4e74297d6ce4499d9b8bea0dccf387e38aac2004ded0cd5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestProperties", value)

    @builtins.property
    @jsii.member(jsii_name="hardwareVersion")
    def hardware_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hardwareVersion"))

    @hardware_version.setter
    def hardware_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b69465ae9ec1fbc5c37a1695be0d123a3adbdc781eaec90ad246bb50f94dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hardwareVersion", value)

    @builtins.property
    @jsii.member(jsii_name="href")
    def href(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "href"))

    @href.setter
    def href(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af4df116afa30c78e06eab34969ee3900ab2e015020eebcecadc5637c73bcb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "href", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0663c4bf638ae494ad5a19faad47dda6bfefd8e5442e64b542aaf9527a88f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1867759059a3aeff677beb759e892eb0316ff08a183dc428f450958962bf1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f7105a854c7beaadfede27686bd34fc3d524aa5535bc6c3455cc7f948836a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryHotAddEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryLimit"))

    @memory_limit.setter
    def memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a2ed894a16255a796aca3188347e770684ba22c543455040990320692a6197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryLimit", value)

    @builtins.property
    @jsii.member(jsii_name="memoryPriority")
    def memory_priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memoryPriority"))

    @memory_priority.setter
    def memory_priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b804be14f84cd8ba1d7f85ef6a488cf6ea84446d195095bf9c23184d91b0fcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryPriority", value)

    @builtins.property
    @jsii.member(jsii_name="memoryReservation")
    def memory_reservation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryReservation"))

    @memory_reservation.setter
    def memory_reservation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852e78fc5ede024b0a976a385cbdb888bc66403d4505b9bd1b58c805960bbf26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryReservation", value)

    @builtins.property
    @jsii.member(jsii_name="memoryShares")
    def memory_shares(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryShares"))

    @memory_shares.setter
    def memory_shares(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12e7d804946ea397dcf368a6c74dee3eedf67030402a70bdb52e2c1e36d6301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryShares", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae90cd8a849034670d8fe3f5aca308fe17713901ecf8829f1ce71a9015c96df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35283c91782f60f08fc0a6313959c9b2f21858de975a2979be8d10beea269d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkDhcpWaitSeconds")
    def network_dhcp_wait_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "networkDhcpWaitSeconds"))

    @network_dhcp_wait_seconds.setter
    def network_dhcp_wait_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af97b6146fcc78b5300c4296233d251d66c0ce477db0eead8dcaaa3941400e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkDhcpWaitSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a2b0d2921481e8d6a8dd60bb456a374fdabe470d416c4cca23babd0e189d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd491a5fbe951221366797d376759d2ebff8740d452fe39cb250be64d3e0b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value)

    @builtins.property
    @jsii.member(jsii_name="placementPolicyId")
    def placement_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "placementPolicyId"))

    @placement_policy_id.setter
    def placement_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b022eca3937822c903e735598a133c74028f6fa4cfb492fcb908abc615b3144)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4782b026e20d198781d1ac9cd3f546ab64a6b6d2bf6f69c8595981d570285e81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e70a0158c54b19ede6cda6697e8276eddac539c0e768627342d51bfbfcb69bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventUpdatePowerOff", value)

    @builtins.property
    @jsii.member(jsii_name="securityTags")
    def security_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityTags"))

    @security_tags.setter
    def security_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1dd74dddcced3f1b74187f6191f9b5818e66d9b8cac64e567232072bd5c5673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityTags", value)

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyId")
    def sizing_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingPolicyId"))

    @sizing_policy_id.setter
    def sizing_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548e728ad4ac977fc8ec0c61cec23f4901883d2c0301965e2bd8ff27bd1f7168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfile"))

    @storage_profile.setter
    def storage_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8148e737bd1dab36948542f9bdf2edcba69de288e7277f665a66a38f8db2bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfile", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd188949bd9c16c09fc6917ba616606a89c8b2cac60e9a90e0170c26e8df40a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="vappName")
    def vapp_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappName"))

    @vapp_name.setter
    def vapp_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb6ff6992a282d6b537f7eba063a4a790a0dc8a32981749a292e2deea723cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappName", value)

    @builtins.property
    @jsii.member(jsii_name="vappTemplateId")
    def vapp_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappTemplateId"))

    @vapp_template_id.setter
    def vapp_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03859f9e50d053c47c7d66f974ca2545955d3abf13af0b0d825aa815921a98a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappTemplateId", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b6ec2f8419807ddc93bc714ce893c69c50cff9fdae6c4f6215fd92caa38356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)

    @builtins.property
    @jsii.member(jsii_name="vmNameInTemplate")
    def vm_name_in_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmNameInTemplate"))

    @vm_name_in_template.setter
    def vm_name_in_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260266724b0684a96ccf40c4420154d212e6ab27c91e423ee7de7586c067d2bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmNameInTemplate", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmBootOptions",
    jsii_struct_bases=[],
    name_mapping={
        "boot_delay": "bootDelay",
        "boot_retry_delay": "bootRetryDelay",
        "boot_retry_enabled": "bootRetryEnabled",
        "efi_secure_boot": "efiSecureBoot",
        "enter_bios_setup_on_next_boot": "enterBiosSetupOnNextBoot",
    },
)
class VmBootOptions:
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
        :param boot_delay: Number of milliseconds to wait between powering-on and booting the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_delay Vm#boot_delay}
        :param boot_retry_delay: Delay in milliseconds before a boot retry. Only works if 'boot_retry_enabled' is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_retry_delay Vm#boot_retry_delay}
        :param boot_retry_enabled: If set to true, a VM that fails to boot will try again after the 'boot_retry_delay' time period has expired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_retry_enabled Vm#boot_retry_enabled}
        :param efi_secure_boot: If set to true, enables EFI Secure Boot for the VM. Can only be changed when the VM is powered off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#efi_secure_boot Vm#efi_secure_boot}
        :param enter_bios_setup_on_next_boot: If set to true, the VM will enter BIOS setup on next boot. If a VM is powered on, the field will be set to ``false`` by VCD and Terraform will return a non-empty plan Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#enter_bios_setup_on_next_boot Vm#enter_bios_setup_on_next_boot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1787233c36bec13fcd2909bcf8222805d3d3e4b1c95283db1fb682c8670a3213)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_delay Vm#boot_delay}
        '''
        result = self._values.get("boot_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_retry_delay(self) -> typing.Optional[jsii.Number]:
        '''Delay in milliseconds before a boot retry. Only works if 'boot_retry_enabled' is set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_retry_delay Vm#boot_retry_delay}
        '''
        result = self._values.get("boot_retry_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_retry_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, a VM that fails to boot will try again after the 'boot_retry_delay' time period has expired.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_retry_enabled Vm#boot_retry_enabled}
        '''
        result = self._values.get("boot_retry_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def efi_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, enables EFI Secure Boot for the VM.

        Can only be changed when the VM is powered off.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#efi_secure_boot Vm#efi_secure_boot}
        '''
        result = self._values.get("efi_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enter_bios_setup_on_next_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the VM will enter BIOS setup on next boot.

        If a VM is powered on, the field will be set to ``false`` by VCD and Terraform will return a non-empty plan

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#enter_bios_setup_on_next_boot Vm#enter_bios_setup_on_next_boot}
        '''
        result = self._values.get("enter_bios_setup_on_next_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmBootOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmBootOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmBootOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__944b6de4b9b35c03e42bc1ada62b1ca5d667198cf59b3b70d90439188af158f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9927f4c0a300cd01b4d9dc9e0002af451c88e05a809e0be6a9940d68b91cb6a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDelay", value)

    @builtins.property
    @jsii.member(jsii_name="bootRetryDelay")
    def boot_retry_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootRetryDelay"))

    @boot_retry_delay.setter
    def boot_retry_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb3709f439c3369bad31f4f6331f3cc0101d33486e58a1fa15f40445bca4ed4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__203f7045f71fc1fc8bb0806689b7428be696972e0228b8807fb4c348a9656dc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1745512cf20135a1bcf1adccb471f67f512b8be0792ba8b2edfd0b3416f64b46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67d3a53a7579f9fc4a7172cf32979f61f546ace7e12785be50094b015693afeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterBiosSetupOnNextBoot", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmBootOptions]:
        return typing.cast(typing.Optional[VmBootOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmBootOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880537f7c3a0b69b80e8cc39efba55e0375faf108cc96e2047c5d5e232801aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmConfig",
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
        "vapp_name": "vappName",
        "vapp_template_id": "vappTemplateId",
        "vdc": "vdc",
        "vm_name_in_template": "vmNameInTemplate",
    },
)
class VmConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        accept_all_eulas: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        boot_image: typing.Optional[builtins.str] = None,
        boot_image_id: typing.Optional[builtins.str] = None,
        boot_options: typing.Optional[typing.Union[VmBootOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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
        customization: typing.Optional[typing.Union["VmCustomization", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_dhcp_wait_seconds: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        override_template_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmOverrideTemplateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement_policy_id: typing.Optional[builtins.str] = None,
        power_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_update_power_off: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        set_extra_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmSetExtraConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sizing_policy_id: typing.Optional[builtins.str] = None,
        storage_profile: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
        vapp_name: typing.Optional[builtins.str] = None,
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
        :param name: A name for the VM, unique within the vApp. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#name Vm#name}
        :param accept_all_eulas: Automatically accept EULA if OVA has it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#accept_all_eulas Vm#accept_all_eulas}
        :param boot_image: Media name to add as boot image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_image Vm#boot_image}
        :param boot_image_id: The URN of the media to use as boot image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_image_id Vm#boot_image_id}
        :param boot_options: boot_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_options Vm#boot_options}
        :param catalog_name: The catalog name in which to find the given vApp Template or media for boot_image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#catalog_name Vm#catalog_name}
        :param computer_name: Computer name to assign to this virtual machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#computer_name Vm#computer_name}
        :param consolidate_disks_on_create: Consolidates disks during creation and allows to change disk size using 'override_template_disk' in fast provisioned VDCs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#consolidate_disks_on_create Vm#consolidate_disks_on_create}
        :param copy_from_vm_id: Source VM that should be copied from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#copy_from_vm_id Vm#copy_from_vm_id}
        :param cpu_cores: The number of cores per socket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_cores Vm#cpu_cores}
        :param cpu_hot_add_enabled: True if the virtual machine supports addition of virtual CPUs while powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_hot_add_enabled Vm#cpu_hot_add_enabled}
        :param cpu_limit: The limit for how much of CPU can be consumed on the underlying virtualization infrastructure. This is only valid when the resource allocation is not unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_limit Vm#cpu_limit}
        :param cpu_priority: Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_priority Vm#cpu_priority}
        :param cpu_reservation: The amount of MHz reservation on the underlying virtualization infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_reservation Vm#cpu_reservation}
        :param cpus: The number of virtual CPUs to allocate to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpus Vm#cpus}
        :param cpu_shares: Custom priority for the resource. This is a read-only, unless the ``cpu_priority`` is CUSTOM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_shares Vm#cpu_shares}
        :param customization: customization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#customization Vm#customization}
        :param description: The VM description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#description Vm#description}
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#disk Vm#disk}
        :param expose_hardware_virtualization: Expose hardware-assisted CPU virtualization to guest OS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#expose_hardware_virtualization Vm#expose_hardware_virtualization}
        :param firmware: Firmware of the VM. Can be either EFI or BIOS, availabilitydepending on the os_type argument. If unset, is set to 'bios' by default. Changing the value when ``power_on`` is set to true, will cause a reboot of the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#firmware Vm#firmware}
        :param guest_properties: Key/value settings for guest properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#guest_properties Vm#guest_properties}
        :param hardware_version: Virtual Hardware Version (e.g.``vmx-14``, ``vmx-13``, ``vmx-12``, etc.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#hardware_version Vm#hardware_version}
        :param href: VM Hyper Reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#href Vm#href}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#id Vm#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param memory: The amount of RAM (in MB) to allocate to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory Vm#memory}
        :param memory_hot_add_enabled: True if the virtual machine supports addition of memory while powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_hot_add_enabled Vm#memory_hot_add_enabled}
        :param memory_limit: The limit for how much of memory can be consumed on the underlying virtualization infrastructure. This is only valid when the resource allocation is not unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_limit Vm#memory_limit}
        :param memory_priority: Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_priority Vm#memory_priority}
        :param memory_reservation: The amount of RAM (in MB) reservation on the underlying virtualization infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_reservation Vm#memory_reservation}
        :param memory_shares: Custom priority for the resource. This is a read-only, unless the ``memory_priority`` is CUSTOM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_shares Vm#memory_shares}
        :param metadata: Key value map of metadata to assign to this VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#metadata Vm#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#metadata_entry Vm#metadata_entry}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#network Vm#network}
        :param network_dhcp_wait_seconds: Optional number of seconds to try and wait for DHCP IP (valid for 'network' block only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#network_dhcp_wait_seconds Vm#network_dhcp_wait_seconds}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#org Vm#org}
        :param os_type: Operating System type. Possible values can be found in documentation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#os_type Vm#os_type}
        :param override_template_disk: override_template_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#override_template_disk Vm#override_template_disk}
        :param placement_policy_id: VM placement policy ID. Has to be assigned to Org VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#placement_policy_id Vm#placement_policy_id}
        :param power_on: A boolean value stating if this VM should be powered on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#power_on Vm#power_on}
        :param prevent_update_power_off: True if the update of resource should fail when virtual machine power off needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#prevent_update_power_off Vm#prevent_update_power_off}
        :param security_tags: Security tags to assign to this VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#security_tags Vm#security_tags}
        :param set_extra_config: set_extra_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#set_extra_config Vm#set_extra_config}
        :param sizing_policy_id: VM sizing policy ID. Has to be assigned to Org VDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#sizing_policy_id Vm#sizing_policy_id}
        :param storage_profile: Storage profile to override the default one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#storage_profile Vm#storage_profile}
        :param template_name: The name of the vApp Template to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#template_name Vm#template_name}
        :param vapp_name: The vApp this VM belongs to - Required, unless it is a standalone VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vapp_name Vm#vapp_name}
        :param vapp_template_id: The URN of the vApp Template to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vapp_template_id Vm#vapp_template_id}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vdc Vm#vdc}
        :param vm_name_in_template: The name of the VM in vApp Template to use. In cases when vApp template has more than one VM Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vm_name_in_template Vm#vm_name_in_template}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(boot_options, dict):
            boot_options = VmBootOptions(**boot_options)
        if isinstance(customization, dict):
            customization = VmCustomization(**customization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97ec5f4557a2f7e364a4ab6347de541632471654e3a1d8e2f2a31a4caba7a59)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
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
            check_type(argname="argument vapp_name", value=vapp_name, expected_type=type_hints["vapp_name"])
            check_type(argname="argument vapp_template_id", value=vapp_template_id, expected_type=type_hints["vapp_template_id"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
            check_type(argname="argument vm_name_in_template", value=vm_name_in_template, expected_type=type_hints["vm_name_in_template"])
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
        if vapp_name is not None:
            self._values["vapp_name"] = vapp_name
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#name Vm#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_all_eulas(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically accept EULA if OVA has it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#accept_all_eulas Vm#accept_all_eulas}
        '''
        result = self._values.get("accept_all_eulas")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def boot_image(self) -> typing.Optional[builtins.str]:
        '''Media name to add as boot image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_image Vm#boot_image}
        '''
        result = self._values.get("boot_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_image_id(self) -> typing.Optional[builtins.str]:
        '''The URN of the media to use as boot image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_image_id Vm#boot_image_id}
        '''
        result = self._values.get("boot_image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_options(self) -> typing.Optional[VmBootOptions]:
        '''boot_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#boot_options Vm#boot_options}
        '''
        result = self._values.get("boot_options")
        return typing.cast(typing.Optional[VmBootOptions], result)

    @builtins.property
    def catalog_name(self) -> typing.Optional[builtins.str]:
        '''The catalog name in which to find the given vApp Template or media for boot_image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#catalog_name Vm#catalog_name}
        '''
        result = self._values.get("catalog_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def computer_name(self) -> typing.Optional[builtins.str]:
        '''Computer name to assign to this virtual machine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#computer_name Vm#computer_name}
        '''
        result = self._values.get("computer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consolidate_disks_on_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Consolidates disks during creation and allows to change disk size using 'override_template_disk' in fast provisioned VDCs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#consolidate_disks_on_create Vm#consolidate_disks_on_create}
        '''
        result = self._values.get("consolidate_disks_on_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def copy_from_vm_id(self) -> typing.Optional[builtins.str]:
        '''Source VM that should be copied from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#copy_from_vm_id Vm#copy_from_vm_id}
        '''
        result = self._values.get("copy_from_vm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_cores(self) -> typing.Optional[jsii.Number]:
        '''The number of cores per socket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_cores Vm#cpu_cores}
        '''
        result = self._values.get("cpu_cores")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_hot_add_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the virtual machine supports addition of virtual CPUs while powered on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_hot_add_enabled Vm#cpu_hot_add_enabled}
        '''
        result = self._values.get("cpu_hot_add_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_limit(self) -> typing.Optional[jsii.Number]:
        '''The limit for how much of CPU can be consumed on the underlying virtualization infrastructure.

        This is only valid when the resource allocation is not unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_limit Vm#cpu_limit}
        '''
        result = self._values.get("cpu_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_priority(self) -> typing.Optional[builtins.str]:
        '''Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_priority Vm#cpu_priority}
        '''
        result = self._values.get("cpu_priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''The amount of MHz reservation on the underlying virtualization infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_reservation Vm#cpu_reservation}
        '''
        result = self._values.get("cpu_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of virtual CPUs to allocate to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpus Vm#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_shares(self) -> typing.Optional[jsii.Number]:
        '''Custom priority for the resource. This is a read-only, unless the ``cpu_priority`` is CUSTOM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#cpu_shares Vm#cpu_shares}
        '''
        result = self._values.get("cpu_shares")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def customization(self) -> typing.Optional["VmCustomization"]:
        '''customization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#customization Vm#customization}
        '''
        result = self._values.get("customization")
        return typing.cast(typing.Optional["VmCustomization"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The VM description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#description Vm#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmDisk"]]]:
        '''disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#disk Vm#disk}
        '''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmDisk"]]], result)

    @builtins.property
    def expose_hardware_virtualization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Expose hardware-assisted CPU virtualization to guest OS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#expose_hardware_virtualization Vm#expose_hardware_virtualization}
        '''
        result = self._values.get("expose_hardware_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def firmware(self) -> typing.Optional[builtins.str]:
        '''Firmware of the VM.

        Can be either EFI or BIOS, availabilitydepending on the os_type argument. If unset, is set to 'bios' by default. Changing the value when ``power_on`` is set to true, will cause a reboot of the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#firmware Vm#firmware}
        '''
        result = self._values.get("firmware")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key/value settings for guest properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#guest_properties Vm#guest_properties}
        '''
        result = self._values.get("guest_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def hardware_version(self) -> typing.Optional[builtins.str]:
        '''Virtual Hardware Version (e.g.``vmx-14``, ``vmx-13``, ``vmx-12``, etc.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#hardware_version Vm#hardware_version}
        '''
        result = self._values.get("hardware_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def href(self) -> typing.Optional[builtins.str]:
        '''VM Hyper Reference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#href Vm#href}
        '''
        result = self._values.get("href")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#id Vm#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''The amount of RAM (in MB) to allocate to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory Vm#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_hot_add_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the virtual machine supports addition of memory while powered on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_hot_add_enabled Vm#memory_hot_add_enabled}
        '''
        result = self._values.get("memory_hot_add_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''The limit for how much of memory can be consumed on the underlying virtualization infrastructure.

        This is only valid when the resource allocation is not unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_limit Vm#memory_limit}
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_priority(self) -> typing.Optional[builtins.str]:
        '''Pre-determined relative priorities according to which the non-reserved portion of this resource is made available to the virtualized workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_priority Vm#memory_priority}
        '''
        result = self._values.get("memory_priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        '''The amount of RAM (in MB) reservation on the underlying virtualization infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_reservation Vm#memory_reservation}
        '''
        result = self._values.get("memory_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_shares(self) -> typing.Optional[jsii.Number]:
        '''Custom priority for the resource. This is a read-only, unless the ``memory_priority`` is CUSTOM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#memory_shares Vm#memory_shares}
        '''
        result = self._values.get("memory_shares")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key value map of metadata to assign to this VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#metadata Vm#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmMetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#metadata_entry Vm#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmMetadataEntry"]]], result)

    @builtins.property
    def network(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmNetwork"]]]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#network Vm#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmNetwork"]]], result)

    @builtins.property
    def network_dhcp_wait_seconds(self) -> typing.Optional[jsii.Number]:
        '''Optional number of seconds to try and wait for DHCP IP (valid for 'network' block only).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#network_dhcp_wait_seconds Vm#network_dhcp_wait_seconds}
        '''
        result = self._values.get("network_dhcp_wait_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#org Vm#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Operating System type. Possible values can be found in documentation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#os_type Vm#os_type}
        '''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_template_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmOverrideTemplateDisk"]]]:
        '''override_template_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#override_template_disk Vm#override_template_disk}
        '''
        result = self._values.get("override_template_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmOverrideTemplateDisk"]]], result)

    @builtins.property
    def placement_policy_id(self) -> typing.Optional[builtins.str]:
        '''VM placement policy ID. Has to be assigned to Org VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#placement_policy_id Vm#placement_policy_id}
        '''
        result = self._values.get("placement_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def power_on(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean value stating if this VM should be powered on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#power_on Vm#power_on}
        '''
        result = self._values.get("power_on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_update_power_off(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the update of resource should fail when virtual machine power off needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#prevent_update_power_off Vm#prevent_update_power_off}
        '''
        result = self._values.get("prevent_update_power_off")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Security tags to assign to this VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#security_tags Vm#security_tags}
        '''
        result = self._values.get("security_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def set_extra_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmSetExtraConfig"]]]:
        '''set_extra_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#set_extra_config Vm#set_extra_config}
        '''
        result = self._values.get("set_extra_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmSetExtraConfig"]]], result)

    @builtins.property
    def sizing_policy_id(self) -> typing.Optional[builtins.str]:
        '''VM sizing policy ID. Has to be assigned to Org VDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#sizing_policy_id Vm#sizing_policy_id}
        '''
        result = self._values.get("sizing_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_profile(self) -> typing.Optional[builtins.str]:
        '''Storage profile to override the default one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#storage_profile Vm#storage_profile}
        '''
        result = self._values.get("storage_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the vApp Template to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#template_name Vm#template_name}
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vapp_name(self) -> typing.Optional[builtins.str]:
        '''The vApp this VM belongs to - Required, unless it is a standalone VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vapp_name Vm#vapp_name}
        '''
        result = self._values.get("vapp_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vapp_template_id(self) -> typing.Optional[builtins.str]:
        '''The URN of the vApp Template to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vapp_template_id Vm#vapp_template_id}
        '''
        result = self._values.get("vapp_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vdc Vm#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_name_in_template(self) -> typing.Optional[builtins.str]:
        '''The name of the VM in vApp Template to use.

        In cases when vApp template has more than one VM

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#vm_name_in_template Vm#vm_name_in_template}
        '''
        result = self._values.get("vm_name_in_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.vm.VmCustomization",
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
class VmCustomization:
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
        :param admin_password: Manually specify admin password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#admin_password Vm#admin_password}
        :param allow_local_admin_password: Allow local administrator password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#allow_local_admin_password Vm#allow_local_admin_password}
        :param auto_generate_password: Auto generate password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#auto_generate_password Vm#auto_generate_password}
        :param change_sid: 'true' value will change SID. Applicable only for Windows VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#change_sid Vm#change_sid}
        :param enabled: 'true' value will enable guest customization. It may occur on first boot or when 'force' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#enabled Vm#enabled}
        :param force: 'true' value will cause the VM to reboot on every 'apply' operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#force Vm#force}
        :param initscript: Script to run on initial boot or with customization.force=true set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#initscript Vm#initscript}
        :param join_domain: Enable this VM to join a domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain Vm#join_domain}
        :param join_domain_account_ou: Account organizational unit for domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_account_ou Vm#join_domain_account_ou}
        :param join_domain_name: Custom domain name for join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_name Vm#join_domain_name}
        :param join_domain_password: Password for custom domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_password Vm#join_domain_password}
        :param join_domain_user: Username for custom domain name join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_user Vm#join_domain_user}
        :param join_org_domain: Use organization's domain for joining. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_org_domain Vm#join_org_domain}
        :param must_change_password_on_first_login: Require Administrator to change password on first login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#must_change_password_on_first_login Vm#must_change_password_on_first_login}
        :param number_of_auto_logons: Number of times to log on automatically. '0' - disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#number_of_auto_logons Vm#number_of_auto_logons}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fbdf9bf22e4846ab420ebf679ff5fe301bbf774502b8f0ae6566598aab5cbfa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#admin_password Vm#admin_password}
        '''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_local_admin_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow local administrator password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#allow_local_admin_password Vm#allow_local_admin_password}
        '''
        result = self._values.get("allow_local_admin_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_generate_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Auto generate password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#auto_generate_password Vm#auto_generate_password}
        '''
        result = self._values.get("auto_generate_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def change_sid(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        ''''true' value will change SID. Applicable only for Windows VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#change_sid Vm#change_sid}
        '''
        result = self._values.get("change_sid")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        ''''true' value will enable guest customization. It may occur on first boot or when 'force' is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#enabled Vm#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        ''''true' value will cause the VM to reboot on every 'apply' operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#force Vm#force}
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def initscript(self) -> typing.Optional[builtins.str]:
        '''Script to run on initial boot or with customization.force=true set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#initscript Vm#initscript}
        '''
        result = self._values.get("initscript")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable this VM to join a domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain Vm#join_domain}
        '''
        result = self._values.get("join_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def join_domain_account_ou(self) -> typing.Optional[builtins.str]:
        '''Account organizational unit for domain name join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_account_ou Vm#join_domain_account_ou}
        '''
        result = self._values.get("join_domain_account_ou")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_domain_name(self) -> typing.Optional[builtins.str]:
        '''Custom domain name for join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_name Vm#join_domain_name}
        '''
        result = self._values.get("join_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_domain_password(self) -> typing.Optional[builtins.str]:
        '''Password for custom domain name join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_password Vm#join_domain_password}
        '''
        result = self._values.get("join_domain_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_domain_user(self) -> typing.Optional[builtins.str]:
        '''Username for custom domain name join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_domain_user Vm#join_domain_user}
        '''
        result = self._values.get("join_domain_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_org_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use organization's domain for joining.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#join_org_domain Vm#join_org_domain}
        '''
        result = self._values.get("join_org_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def must_change_password_on_first_login(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require Administrator to change password on first login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#must_change_password_on_first_login Vm#must_change_password_on_first_login}
        '''
        result = self._values.get("must_change_password_on_first_login")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def number_of_auto_logons(self) -> typing.Optional[jsii.Number]:
        '''Number of times to log on automatically. '0' - disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#number_of_auto_logons Vm#number_of_auto_logons}
        '''
        result = self._values.get("number_of_auto_logons")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmCustomization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmCustomizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmCustomizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d03b7d34ed9c7dd435b1308a2fc97744f6d88a841e2c5d398179f8912e36e710)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0067a2f4ccfe71481776f45f82360b4a8efdb86ecc4f8f5a5b6e555e0bc3d563)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aedff9ce51bffecbf56678d8616cb938c34ac1e291e52c653627268c84149cac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c73d09811ac946ed3aa68f9ec59fdbfa22ef6d7587128f72f1b791bb22f8e82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f04a9621d55f36ffa394c9b8d3b01d33c63a75d0cef26f333f92eb55e0e2093d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a84766aa5736eb949b867b3abb1a756b6527c17e7de0820d4f272d95123117cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09e71c917648ecd90088c98118276c458a68ec3c1386db42ada9903ca6739bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "force", value)

    @builtins.property
    @jsii.member(jsii_name="initscript")
    def initscript(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initscript"))

    @initscript.setter
    def initscript(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c5f8dc2ba2810ef556da722c7e82e3af826ea878776ca536fc081cc9a1561f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1acb4c3921ec42e700013872973a407ad4ac32b206b5712358ed9c07da87bb82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomain", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomainAccountOu")
    def join_domain_account_ou(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "joinDomainAccountOu"))

    @join_domain_account_ou.setter
    def join_domain_account_ou(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7c365708fa3d63526df5b2d0b6596bc5d52cd060bf0fcb1a390c3f3ee73efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomainAccountOu", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomainName")
    def join_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "joinDomainName"))

    @join_domain_name.setter
    def join_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfb04e29629f22692e1b3a7a3dd99bebfad2dc24cb7eec8897fc851c2951548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomainName", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomainPassword")
    def join_domain_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "joinDomainPassword"))

    @join_domain_password.setter
    def join_domain_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e50a718a36761a7cd2e69c7d552ddf5777239dbd43f0b08e3b2b0f3e93dc79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "joinDomainPassword", value)

    @builtins.property
    @jsii.member(jsii_name="joinDomainUser")
    def join_domain_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "joinDomainUser"))

    @join_domain_user.setter
    def join_domain_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0370d52c9aa97ec635b53a126759bea8ea6463551b9c50a1a8dfe309638bbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd5e1900ae0c735acdd13ea2f94c87baa77e10c59b95c14532a48404545f70a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__734261e9eb5516773d25362d374ff4bb17a32374a960a1b5e67b2c8d8d905edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mustChangePasswordOnFirstLogin", value)

    @builtins.property
    @jsii.member(jsii_name="numberOfAutoLogons")
    def number_of_auto_logons(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfAutoLogons"))

    @number_of_auto_logons.setter
    def number_of_auto_logons(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acae17b6f2753ace4dce6fc318bd1262647249ebdc501b85525f318f5b2863de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfAutoLogons", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmCustomization]:
        return typing.cast(typing.Optional[VmCustomization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmCustomization]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584f0ab3f24c629690774bc8748a0dbde0b8368c126d47e405278baf17c0a87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmDisk",
    jsii_struct_bases=[],
    name_mapping={
        "bus_number": "busNumber",
        "name": "name",
        "unit_number": "unitNumber",
    },
)
class VmDisk:
    def __init__(
        self,
        *,
        bus_number: builtins.str,
        name: builtins.str,
        unit_number: builtins.str,
    ) -> None:
        '''
        :param bus_number: Bus number on which to place the disk controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#bus_number Vm#bus_number}
        :param name: Independent disk name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#name Vm#name}
        :param unit_number: Unit number (slot) on the bus specified by BusNumber. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#unit_number Vm#unit_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14f998621dffd3e1dd43e41d05675f17a19ff2edd7d0c2aa6210606fdfa2339)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#bus_number Vm#bus_number}
        '''
        result = self._values.get("bus_number")
        assert result is not None, "Required property 'bus_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Independent disk name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#name Vm#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unit_number(self) -> builtins.str:
        '''Unit number (slot) on the bus specified by BusNumber.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#unit_number Vm#unit_number}
        '''
        result = self._values.get("unit_number")
        assert result is not None, "Required property 'unit_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f9c5d8fc834dd8ba8e996174d0baf1e31c1dcb24169656669b57c4a983767c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b11171f4a38803cf920f6b7a348c6d5297313cb62f02513a8c0b3c349951c27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3380eed25dfe19acb1082219cc903eb0f93dde7b3b86a22f8034c60647e419ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd0b1b9750eaeb415911ec9a0f0f82e9cc76ab83b14a9a15e91d4455c4698c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acdaf20c2c72b9c24ab4ebdc776fe9d318e02bb03fdf8579a56a44aaddf8d6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52960c440b6e6722ec5158bbc8d42730e54d1c23d533a6d59ba34b4ce4e919fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VmDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c636913fc87215dac3968cf9fb2c43ec73bf1598f3216c4a059b2c7f2c79045)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdbe8631e2b90e0e0698aff74d4a3857978ad6344b02e43670be1254baf4924b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busNumber", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ff84055edcf5eedc0136acd238c8c4337ec256ffca055049582322fcaee77c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="unitNumber")
    def unit_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unitNumber"))

    @unit_number.setter
    def unit_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6c624f471d2377834a2bcb1c832de807041272f5fe3a97a787d1df7c2d16ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unitNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30647efc0db772ecbabbae33a12432bbdba9504b1e291bb72d6c2746053db5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmExtraConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class VmExtraConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmExtraConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmExtraConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmExtraConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fdcf02a6b2456a450644abc22e652a43532c2b2df85dc15bf056ae83cb63da1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmExtraConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26e6b82c0e3ce63a746b0ba2cbfdfae4344387bd38c2542fd47a0abc09e7a4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmExtraConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b43c132fc7041b64432e8354b71685af81c49b95fec881cc1c74f09935460e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e35647158e3544ef1ee5548ad363c48b47e2862f9514137098343672362346bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69f8c0a47febad7d6a9ed09bccbcd93e7a1e428375e1ee1ff76f977df7912a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class VmExtraConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmExtraConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f5413db5853dc316a58cbd69627a674892dc8d6b94d277056805f50698ea420)
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
    def internal_value(self) -> typing.Optional[VmExtraConfig]:
        return typing.cast(typing.Optional[VmExtraConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmExtraConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4105b7aed0cf06b4b75c915540a60cbd90ade96366d7eeeca6304654f2382c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmInternalDisk",
    jsii_struct_bases=[],
    name_mapping={},
)
class VmInternalDisk:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmInternalDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmInternalDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmInternalDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83cd43f78b1a47bc0e78c3021c9b8fe6d984ce6209b2133ae436da66cfe24292)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmInternalDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85649f770165c7a14803650c216dba2296e7bdf738dd1554c55f78568fba1ec6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmInternalDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54aa5efae47df11c8c30bb521a004d6752db8484fb652f78b2050c96edb6408b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0cf40ad1dfcf74a8f80a18f29ede61a2951a8df830f138f22c838cda3f6975b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13f76682087ef52bf86f42d1db5999bc232f41eb70654536ea1696289f7fc9ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class VmInternalDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmInternalDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4714eacd18a811ac0ffbe7e2cdac7beab23b3c3d59c005c1785b34e4188e597)
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
    def internal_value(self) -> typing.Optional[VmInternalDisk]:
        return typing.cast(typing.Optional[VmInternalDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VmInternalDisk]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240fb387443e01a43b000c73abd9b1e157bb9440743f29e60094ea998fbad553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "is_system": "isSystem",
        "key": "key",
        "type": "type",
        "user_access": "userAccess",
        "value": "value",
    },
)
class VmMetadataEntry:
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
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#is_system Vm#is_system}
        :param key: Key of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#key Vm#key}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#type Vm#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#user_access Vm#user_access}
        :param value: Value of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#value Vm#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0279750f8e7866c69365f7a43e351366831b679484c3488e02011f0f5ec0680)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#is_system Vm#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#key Vm#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#type Vm#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#user_access Vm#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#value Vm#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmMetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmMetadataEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e4861ea661a18b10a89e8e4cfcc561aab941c34ef4866b3d132f2e4e19f6fd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmMetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2617b134f1083042613de3c3dc22dd6b37df2dcaa7d2f321eba18b65c056744c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmMetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2704328ea4315323fe3c916a18c21a6daa3d5b1d01194081d8f092654c240118)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ad539d0e72fd59435237ff55ed49b6cfe4459cb7d1d3131c8072825964f795)
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
            type_hints = typing.get_type_hints(_typecheckingstub__361fae3baf5f1bab36a9634cb81d14a41e894ba0a1a205abe8f59e08eaee23a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmMetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmMetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmMetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5bd0ddc0a22c94b68ea325db4b2a08fd0dd3659780b97232bcca4343e541e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VmMetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmMetadataEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__332679cc31ef68746548b2de928e0c53f5ed704fd872932df05e1a79cdd10823)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c578c79af472d247a4aaa126297eddc5956ca111ffc8234a1ad526e7858f893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b4eecaa7a94bfbe8fed06891f7d9e4000d152e80c8f9f4f77f44f6716334ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6342bfd1b44cbd5c7de9c601f30ab881e97bb028fe5620e374a64eec2c6eb2f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b9cf1e7a1e4fd96e907acf314d637b75db9a5ecc9af03cea3f8f87dfb61d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1925c5c56cef763455220c0eabbc7fdde6bdc99526e783c63fe2a00f539b8d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmMetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmMetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmMetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7555d6146093dec340bbfec6cbb7a8708ac8a0e9d9697a88166e97b3e003ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmNetwork",
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
class VmNetwork:
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
        :param ip_allocation_mode: IP address allocation mode. One of POOL, DHCP, MANUAL, NONE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#ip_allocation_mode Vm#ip_allocation_mode}
        :param type: Network type to use: 'vapp', 'org' or 'none'. Use 'vapp' for vApp network, 'org' to attach Org VDC network. 'none' for empty NIC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#type Vm#type}
        :param adapter_type: Network card adapter type. (e.g. 'E1000', 'E1000E', 'SRIOVETHERNETCARD', 'VMXNET3', 'PCNet32'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#adapter_type Vm#adapter_type}
        :param connected: It defines if NIC is connected or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#connected Vm#connected}
        :param ip: IP of the VM. Settings depend on ``ip_allocation_mode``. Omitted or empty for DHCP, POOL, NONE. Required for MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#ip Vm#ip}
        :param is_primary: Set to true if network interface should be primary. First network card in the list will be primary by default Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#is_primary Vm#is_primary}
        :param mac: Mac address of network interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#mac Vm#mac}
        :param name: Name of the network this VM should connect to. Always required except for ``type`` ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#name Vm#name}
        :param secondary_ip: Secondary (IPv6) IP of the VM. Settings depend on ``secondary_ip_allocation_mode``. Omitted or empty for DHCP, POOL, NONE. Required for MANUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#secondary_ip Vm#secondary_ip}
        :param secondary_ip_allocation_mode: Secondary (IPv6) IP address allocation mode. One of POOL, DHCP, MANUAL, NONE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#secondary_ip_allocation_mode Vm#secondary_ip_allocation_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0587503595b897910d2fa9692113062efeaca128956bc5ba2b9cebc76996803)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#ip_allocation_mode Vm#ip_allocation_mode}
        '''
        result = self._values.get("ip_allocation_mode")
        assert result is not None, "Required property 'ip_allocation_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Network type to use: 'vapp', 'org' or 'none'.

        Use 'vapp' for vApp network, 'org' to attach Org VDC network. 'none' for empty NIC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#type Vm#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def adapter_type(self) -> typing.Optional[builtins.str]:
        '''Network card adapter type. (e.g. 'E1000', 'E1000E', 'SRIOVETHERNETCARD', 'VMXNET3', 'PCNet32').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#adapter_type Vm#adapter_type}
        '''
        result = self._values.get("adapter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connected(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''It defines if NIC is connected or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#connected Vm#connected}
        '''
        result = self._values.get("connected")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip(self) -> typing.Optional[builtins.str]:
        '''IP of the VM. Settings depend on ``ip_allocation_mode``. Omitted or empty for DHCP, POOL, NONE. Required for MANUAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#ip Vm#ip}
        '''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true if network interface should be primary.

        First network card in the list will be primary by default

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#is_primary Vm#is_primary}
        '''
        result = self._values.get("is_primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mac(self) -> typing.Optional[builtins.str]:
        '''Mac address of network interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#mac Vm#mac}
        '''
        result = self._values.get("mac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the network this VM should connect to. Always required except for ``type`` ``NONE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#name Vm#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_ip(self) -> typing.Optional[builtins.str]:
        '''Secondary (IPv6) IP of the VM.

        Settings depend on ``secondary_ip_allocation_mode``. Omitted or empty for DHCP, POOL, NONE. Required for MANUAL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#secondary_ip Vm#secondary_ip}
        '''
        result = self._values.get("secondary_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_ip_allocation_mode(self) -> typing.Optional[builtins.str]:
        '''Secondary (IPv6) IP address allocation mode. One of POOL, DHCP, MANUAL, NONE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#secondary_ip_allocation_mode Vm#secondary_ip_allocation_mode}
        '''
        result = self._values.get("secondary_ip_allocation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ca0010f62f4879205fd527961a83bb71c6d3af638896a51148467511ea8b64b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd65d3d52dff9b912c511498e883719a465cd54ca0d6191f4e9942c7eebb78a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc1ff6733df5a6a720f8485bee1d0b9167a4a6f3b091b3693624d1e7f7a071c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c6b0753ed301185479826e74a95934db13cb274c2138d3bfb32bcc9588e0bf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc859bffb717b7e86c7340103e3f8325836ed198c8dd73c362176742096496f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f1670596aca1d916966c12d0b8b0b8f63aa75022779efda6f292e1b75b093c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VmNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9990794bd1a4caef88e8effb7fd4ba154cc7b60229702deb7d8442f86b60ce8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48ad14415fdb80ffc9dc7cd92ec8ab2de83aa5e5d836b886c0cbab39c371eb07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ffe33ac874a8fb508323cb8335a52dde08b6659eadbc4f8fe8eed14f05028f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connected", value)

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60787da38b1e39c0a4ea2a66fa3e2c7ba95c1bc0166386e931fda37878b78a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value)

    @builtins.property
    @jsii.member(jsii_name="ipAllocationMode")
    def ip_allocation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAllocationMode"))

    @ip_allocation_mode.setter
    def ip_allocation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea96ceb26227eaedcf34fc02e065c0d865779be3f7a50d924d26776c17c6766)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e18a98a7604e4c7fef51223d36b740c0ebb83595e7a63807c7a3d399d615827c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPrimary", value)

    @builtins.property
    @jsii.member(jsii_name="mac")
    def mac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mac"))

    @mac.setter
    def mac(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a37269daaacf36fc56ee471bac12494c758d3cf13d76ffea5617b2c887dd47f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mac", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb90d014fce576b8cc76590666e4fbd86d64f660ed86da7666747297b24b294c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="secondaryIp")
    def secondary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryIp"))

    @secondary_ip.setter
    def secondary_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3caafe86a98fccf8d93740691d6411f1121de06734637eab8d63b2e81497455f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIp", value)

    @builtins.property
    @jsii.member(jsii_name="secondaryIpAllocationMode")
    def secondary_ip_allocation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryIpAllocationMode"))

    @secondary_ip_allocation_mode.setter
    def secondary_ip_allocation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92529d196084c966287acffb69ba009f3a2fd205305535727a3f8c06d89eed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIpAllocationMode", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f466202fc726c893442b7ad68ca9209e97941c0381f341c283af8a85b1c1e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5676ba1c05dc7f106516e9c1d5f98aca0f1364cdcd8ec437619f75b2ea52d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmOverrideTemplateDisk",
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
class VmOverrideTemplateDisk:
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
        :param bus_number: The number of the SCSI or IDE controller itself. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#bus_number Vm#bus_number}
        :param bus_type: The type of disk controller. Possible values: ide, parallel( LSI Logic Parallel SCSI), sas(LSI Logic SAS (SCSI)), paravirtual(Paravirtual (SCSI)), sata, nvme Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#bus_type Vm#bus_type}
        :param size_in_mb: The size of the disk in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#size_in_mb Vm#size_in_mb}
        :param unit_number: The device number on the SCSI or IDE controller of the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#unit_number Vm#unit_number}
        :param iops: Specifies the IOPS for the disk. Default is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#iops Vm#iops}
        :param storage_profile: Storage profile to override the VM default one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#storage_profile Vm#storage_profile}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54431dfca999d59b79a98f62b48ace879953ae5655be2c3c8b4e2b09d6738fec)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#bus_number Vm#bus_number}
        '''
        result = self._values.get("bus_number")
        assert result is not None, "Required property 'bus_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def bus_type(self) -> builtins.str:
        '''The type of disk controller.

        Possible values: ide, parallel( LSI Logic Parallel SCSI), sas(LSI Logic SAS (SCSI)), paravirtual(Paravirtual (SCSI)), sata, nvme

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#bus_type Vm#bus_type}
        '''
        result = self._values.get("bus_type")
        assert result is not None, "Required property 'bus_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size_in_mb(self) -> jsii.Number:
        '''The size of the disk in MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#size_in_mb Vm#size_in_mb}
        '''
        result = self._values.get("size_in_mb")
        assert result is not None, "Required property 'size_in_mb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def unit_number(self) -> jsii.Number:
        '''The device number on the SCSI or IDE controller of the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#unit_number Vm#unit_number}
        '''
        result = self._values.get("unit_number")
        assert result is not None, "Required property 'unit_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''Specifies the IOPS for the disk. Default is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#iops Vm#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_profile(self) -> typing.Optional[builtins.str]:
        '''Storage profile to override the VM default one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#storage_profile Vm#storage_profile}
        '''
        result = self._values.get("storage_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmOverrideTemplateDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmOverrideTemplateDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmOverrideTemplateDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a9c922fc2e85a93e3a80bee8322ee08516a8de4c95d4c400c9c645415fcc1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmOverrideTemplateDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670bc2fb602691a7441847de1a344ac58a7f7ad395c24149787b89e75d25e384)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmOverrideTemplateDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd798ed28ffa2fc5177034a0301e482d38da248b3df6182e70c190fab95a538c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b0a2a178ba76c30ee3fa9effca10fce66d79834c00ec95acfa37df841bf005d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e7737f9c5a0ae8c19b1426718511a93a326e3dfb3baad6eaa3d76ce76d4cd2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmOverrideTemplateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmOverrideTemplateDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmOverrideTemplateDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7ce34649d485e9d2461551c9088be33cc80f05872c5bdbaddc081e20365b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VmOverrideTemplateDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmOverrideTemplateDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab575bfef66decaa2f0a62f534a62a1b7f6b8eb9b2f3cc40bf8627c0421185a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5856fded2c124d21b70cfc7c0aaa94d9da818113c61fe172ba658b4759c9c8a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busNumber", value)

    @builtins.property
    @jsii.member(jsii_name="busType")
    def bus_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "busType"))

    @bus_type.setter
    def bus_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990acc45d6c581dae12abe42a4fc3724ade2775c38144c8e104a0784e1ec699e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "busType", value)

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @iops.setter
    def iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141e60921717b5f53ccab186ef5f8007675c81409f4675980e1ff1078d524e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value)

    @builtins.property
    @jsii.member(jsii_name="sizeInMb")
    def size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInMb"))

    @size_in_mb.setter
    def size_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879a3cd6cfa03297b75a5fab31ed830e390d739be20da188d44190c4c8905bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInMb", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfile"))

    @storage_profile.setter
    def storage_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeff081184308340096d1d523e060c028bf8a815c63aa475494da58272a0a6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfile", value)

    @builtins.property
    @jsii.member(jsii_name="unitNumber")
    def unit_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unitNumber"))

    @unit_number.setter
    def unit_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2f801f34d89c963a2d95deecebdf254672e91d0421e4e996366a1122c20404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unitNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmOverrideTemplateDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmOverrideTemplateDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmOverrideTemplateDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8e2e98c3fda62036fc831aa0465073a1ab5047765f3a3c40b8d60f23830a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.vm.VmSetExtraConfig",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class VmSetExtraConfig:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: The key of the extra configuration item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#key Vm#key}
        :param value: The value of the extra configuration item. Leaving the ``value`` field empty will result in the item deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#value Vm#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0aaa354dd9b568a5531e7a257447192372f4f7fe776f5885c785e4b73e971cb)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the extra configuration item.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#key Vm#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the extra configuration item. Leaving the ``value`` field empty will result in the item deletion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/vm#value Vm#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmSetExtraConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmSetExtraConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmSetExtraConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd766b960899f6d6e9c1645b3a819ea358e932f88aa8dd8dc87da90bafc94f41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmSetExtraConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24782b58ddf128711c4713f38dcaa3961c179fd8dca6ebf2b90c4cbbc0f4079a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmSetExtraConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5afefb82c0a22d5dcffbf812c34b2e531435e401a3d542888d7fd71a7e52bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3823dbfdf889a29c1fb149d38f907efc4e7bf511983a56c4e6cc54ecc80c1de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5f7872964b9ec59ae7b3edb2ceb524227e7130f5b6098098f6a3758d1f21437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmSetExtraConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmSetExtraConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmSetExtraConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee80a7110d5fc6d537bae36c0dbbe92caf2e9d67ddf3f802b265091725493d9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VmSetExtraConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.vm.VmSetExtraConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b39d1cd879daa21f1b5d7de98f913d8bb2e676aa2c96d7aa9cd912f9f43bd25d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4ccaf51d5997f6fe775ff505c0a698f55786b6032d5c29d6e7133cd3bec02b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509bdb3a1ce2b56ae2d9680ce6d5b7e061ee2d01cba5ef30459a60577718ca31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmSetExtraConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmSetExtraConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmSetExtraConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6dc815c04ed5f8e39e2d3fc0be3c6839f67441e388fa4613af68a2fabe3fa62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Vm",
    "VmBootOptions",
    "VmBootOptionsOutputReference",
    "VmConfig",
    "VmCustomization",
    "VmCustomizationOutputReference",
    "VmDisk",
    "VmDiskList",
    "VmDiskOutputReference",
    "VmExtraConfig",
    "VmExtraConfigList",
    "VmExtraConfigOutputReference",
    "VmInternalDisk",
    "VmInternalDiskList",
    "VmInternalDiskOutputReference",
    "VmMetadataEntry",
    "VmMetadataEntryList",
    "VmMetadataEntryOutputReference",
    "VmNetwork",
    "VmNetworkList",
    "VmNetworkOutputReference",
    "VmOverrideTemplateDisk",
    "VmOverrideTemplateDiskList",
    "VmOverrideTemplateDiskOutputReference",
    "VmSetExtraConfig",
    "VmSetExtraConfigList",
    "VmSetExtraConfigOutputReference",
]

publication.publish()

def _typecheckingstub__dc50c0fa60f0c8bb5d10f4dadfd9290cc78ea9d8d18c648ada4b784f3dabd3d5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    accept_all_eulas: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    boot_image: typing.Optional[builtins.str] = None,
    boot_image_id: typing.Optional[builtins.str] = None,
    boot_options: typing.Optional[typing.Union[VmBootOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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
    customization: typing.Optional[typing.Union[VmCustomization, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
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
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_dhcp_wait_seconds: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    override_template_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmOverrideTemplateDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement_policy_id: typing.Optional[builtins.str] = None,
    power_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_update_power_off: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    set_extra_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmSetExtraConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sizing_policy_id: typing.Optional[builtins.str] = None,
    storage_profile: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
    vapp_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3f6c9779d97e9abc580fe2ee4ff5f6d42b4a7cff1ae0a93bf79350300b6f8651(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec60ba25b4ffde125cb2555b8dc37ecc57f790ad7fa68d077b16b9a5892ef1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beaf7abd77d1eb255eee6972c918510db69002de3a61fb1b53ebb71a0008e77f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmMetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37845dcdfca62db80c0b61e95583586ca22263da2d7ee502bdab544a0c0172e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de20850974a745e75d10680db95af512be5ed540295a520b1779aa6e1695dd7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmOverrideTemplateDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66cdd386609fc7789da5e4069ca9fa074b292eeecccc5e0b8efba0175b1bcae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmSetExtraConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6709bb2ea497ab1450b479ab9911e5d0eafe36cb25c9afcb8a5cce455ac0a06a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289a86392a6ea9955e01976ec0547cad84a651a769e790359e98151411ee9bd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c13a27f7b8454d56ab2d62bc575b59e05eaabf622106e6a1bf623f73e15a720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c063894febc4654ef085a2afd0a86dd014e8245f5c24611c99105169e3fc8ffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b5c8ea11125936b756caa57f13f19f54c69bdccc6ad45400109b786f652afe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70bcdb8216ab0b316b965abd47ffaf91c7003eeefe5d581bb9afe1c0b3243378(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55096a3ae23e6124ebf06127fb1522885e490491589776e6b4b87f907968804f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346ff2caafeb5f5158f742f8bd26f5a6eee3b01f85d9e4c16f3f37452694036d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630b7133e3f0e3303e691b699ba8f2350e6c60f2883534088b39083bdf58acd4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714acb7d1e06990ec2119a7016fb38b159a1c04a789b7fb2c3e2d304956dc80d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ce4df7f2cc51befb1ba6d66e6678aec4636fbbf561a2a46e9ca0caf2e9ee3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333f69c03d434f15f68c55d8154ac84f86dc1b61a42bcbf7008615906546095f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c8710627cf32e1f033b96386f3cbbe7abf9cee88ee173accea37837d91c7ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc1635f591721089756cfbb6d49d3e0eecb58b6bd36d72dbd361a50a7922f49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd34f3a2653d2720a16f44b946bcdd7293d57657c4c5d2aa0068c56dac45fa9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d57c24022c6966d9abc61df56d197fb4432c9724b02f475e51b802337c04722(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3e6bfbf003c279dfbbd6ae5b80ad289454e0a55a74626e04964ecfa95ca706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a38aeba05b5cbc4e74297d6ce4499d9b8bea0dccf387e38aac2004ded0cd5d8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b69465ae9ec1fbc5c37a1695be0d123a3adbdc781eaec90ad246bb50f94dd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af4df116afa30c78e06eab34969ee3900ab2e015020eebcecadc5637c73bcb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0663c4bf638ae494ad5a19faad47dda6bfefd8e5442e64b542aaf9527a88f56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1867759059a3aeff677beb759e892eb0316ff08a183dc428f450958962bf1b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7105a854c7beaadfede27686bd34fc3d524aa5535bc6c3455cc7f948836a89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a2ed894a16255a796aca3188347e770684ba22c543455040990320692a6197(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b804be14f84cd8ba1d7f85ef6a488cf6ea84446d195095bf9c23184d91b0fcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852e78fc5ede024b0a976a385cbdb888bc66403d4505b9bd1b58c805960bbf26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12e7d804946ea397dcf368a6c74dee3eedf67030402a70bdb52e2c1e36d6301(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae90cd8a849034670d8fe3f5aca308fe17713901ecf8829f1ce71a9015c96df(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35283c91782f60f08fc0a6313959c9b2f21858de975a2979be8d10beea269d68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af97b6146fcc78b5300c4296233d251d66c0ce477db0eead8dcaaa3941400e4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a2b0d2921481e8d6a8dd60bb456a374fdabe470d416c4cca23babd0e189d94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd491a5fbe951221366797d376759d2ebff8740d452fe39cb250be64d3e0b25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b022eca3937822c903e735598a133c74028f6fa4cfb492fcb908abc615b3144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4782b026e20d198781d1ac9cd3f546ab64a6b6d2bf6f69c8595981d570285e81(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70a0158c54b19ede6cda6697e8276eddac539c0e768627342d51bfbfcb69bf9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1dd74dddcced3f1b74187f6191f9b5818e66d9b8cac64e567232072bd5c5673(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548e728ad4ac977fc8ec0c61cec23f4901883d2c0301965e2bd8ff27bd1f7168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8148e737bd1dab36948542f9bdf2edcba69de288e7277f665a66a38f8db2bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd188949bd9c16c09fc6917ba616606a89c8b2cac60e9a90e0170c26e8df40a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb6ff6992a282d6b537f7eba063a4a790a0dc8a32981749a292e2deea723cb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03859f9e50d053c47c7d66f974ca2545955d3abf13af0b0d825aa815921a98a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b6ec2f8419807ddc93bc714ce893c69c50cff9fdae6c4f6215fd92caa38356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260266724b0684a96ccf40c4420154d212e6ab27c91e423ee7de7586c067d2bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1787233c36bec13fcd2909bcf8222805d3d3e4b1c95283db1fb682c8670a3213(
    *,
    boot_delay: typing.Optional[jsii.Number] = None,
    boot_retry_delay: typing.Optional[jsii.Number] = None,
    boot_retry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    efi_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enter_bios_setup_on_next_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944b6de4b9b35c03e42bc1ada62b1ca5d667198cf59b3b70d90439188af158f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9927f4c0a300cd01b4d9dc9e0002af451c88e05a809e0be6a9940d68b91cb6a0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb3709f439c3369bad31f4f6331f3cc0101d33486e58a1fa15f40445bca4ed4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203f7045f71fc1fc8bb0806689b7428be696972e0228b8807fb4c348a9656dc5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1745512cf20135a1bcf1adccb471f67f512b8be0792ba8b2edfd0b3416f64b46(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d3a53a7579f9fc4a7172cf32979f61f546ace7e12785be50094b015693afeb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880537f7c3a0b69b80e8cc39efba55e0375faf108cc96e2047c5d5e232801aa2(
    value: typing.Optional[VmBootOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97ec5f4557a2f7e364a4ab6347de541632471654e3a1d8e2f2a31a4caba7a59(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    accept_all_eulas: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    boot_image: typing.Optional[builtins.str] = None,
    boot_image_id: typing.Optional[builtins.str] = None,
    boot_options: typing.Optional[typing.Union[VmBootOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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
    customization: typing.Optional[typing.Union[VmCustomization, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
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
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_dhcp_wait_seconds: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    override_template_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmOverrideTemplateDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement_policy_id: typing.Optional[builtins.str] = None,
    power_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_update_power_off: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    set_extra_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmSetExtraConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sizing_policy_id: typing.Optional[builtins.str] = None,
    storage_profile: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
    vapp_name: typing.Optional[builtins.str] = None,
    vapp_template_id: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
    vm_name_in_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbdf9bf22e4846ab420ebf679ff5fe301bbf774502b8f0ae6566598aab5cbfa(
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

def _typecheckingstub__d03b7d34ed9c7dd435b1308a2fc97744f6d88a841e2c5d398179f8912e36e710(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0067a2f4ccfe71481776f45f82360b4a8efdb86ecc4f8f5a5b6e555e0bc3d563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedff9ce51bffecbf56678d8616cb938c34ac1e291e52c653627268c84149cac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c73d09811ac946ed3aa68f9ec59fdbfa22ef6d7587128f72f1b791bb22f8e82(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04a9621d55f36ffa394c9b8d3b01d33c63a75d0cef26f333f92eb55e0e2093d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84766aa5736eb949b867b3abb1a756b6527c17e7de0820d4f272d95123117cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e71c917648ecd90088c98118276c458a68ec3c1386db42ada9903ca6739bda(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c5f8dc2ba2810ef556da722c7e82e3af826ea878776ca536fc081cc9a1561f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acb4c3921ec42e700013872973a407ad4ac32b206b5712358ed9c07da87bb82(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7c365708fa3d63526df5b2d0b6596bc5d52cd060bf0fcb1a390c3f3ee73efc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfb04e29629f22692e1b3a7a3dd99bebfad2dc24cb7eec8897fc851c2951548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e50a718a36761a7cd2e69c7d552ddf5777239dbd43f0b08e3b2b0f3e93dc79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0370d52c9aa97ec635b53a126759bea8ea6463551b9c50a1a8dfe309638bbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5e1900ae0c735acdd13ea2f94c87baa77e10c59b95c14532a48404545f70a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734261e9eb5516773d25362d374ff4bb17a32374a960a1b5e67b2c8d8d905edf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acae17b6f2753ace4dce6fc318bd1262647249ebdc501b85525f318f5b2863de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584f0ab3f24c629690774bc8748a0dbde0b8368c126d47e405278baf17c0a87e(
    value: typing.Optional[VmCustomization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14f998621dffd3e1dd43e41d05675f17a19ff2edd7d0c2aa6210606fdfa2339(
    *,
    bus_number: builtins.str,
    name: builtins.str,
    unit_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9c5d8fc834dd8ba8e996174d0baf1e31c1dcb24169656669b57c4a983767c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b11171f4a38803cf920f6b7a348c6d5297313cb62f02513a8c0b3c349951c27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3380eed25dfe19acb1082219cc903eb0f93dde7b3b86a22f8034c60647e419ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd0b1b9750eaeb415911ec9a0f0f82e9cc76ab83b14a9a15e91d4455c4698c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdaf20c2c72b9c24ab4ebdc776fe9d318e02bb03fdf8579a56a44aaddf8d6fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52960c440b6e6722ec5158bbc8d42730e54d1c23d533a6d59ba34b4ce4e919fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c636913fc87215dac3968cf9fb2c43ec73bf1598f3216c4a059b2c7f2c79045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbe8631e2b90e0e0698aff74d4a3857978ad6344b02e43670be1254baf4924b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ff84055edcf5eedc0136acd238c8c4337ec256ffca055049582322fcaee77c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6c624f471d2377834a2bcb1c832de807041272f5fe3a97a787d1df7c2d16ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30647efc0db772ecbabbae33a12432bbdba9504b1e291bb72d6c2746053db5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdcf02a6b2456a450644abc22e652a43532c2b2df85dc15bf056ae83cb63da1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26e6b82c0e3ce63a746b0ba2cbfdfae4344387bd38c2542fd47a0abc09e7a4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b43c132fc7041b64432e8354b71685af81c49b95fec881cc1c74f09935460e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35647158e3544ef1ee5548ad363c48b47e2862f9514137098343672362346bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f8c0a47febad7d6a9ed09bccbcd93e7a1e428375e1ee1ff76f977df7912a38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5413db5853dc316a58cbd69627a674892dc8d6b94d277056805f50698ea420(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4105b7aed0cf06b4b75c915540a60cbd90ade96366d7eeeca6304654f2382c8(
    value: typing.Optional[VmExtraConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83cd43f78b1a47bc0e78c3021c9b8fe6d984ce6209b2133ae436da66cfe24292(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85649f770165c7a14803650c216dba2296e7bdf738dd1554c55f78568fba1ec6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54aa5efae47df11c8c30bb521a004d6752db8484fb652f78b2050c96edb6408b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0cf40ad1dfcf74a8f80a18f29ede61a2951a8df830f138f22c838cda3f6975b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f76682087ef52bf86f42d1db5999bc232f41eb70654536ea1696289f7fc9ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4714eacd18a811ac0ffbe7e2cdac7beab23b3c3d59c005c1785b34e4188e597(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240fb387443e01a43b000c73abd9b1e157bb9440743f29e60094ea998fbad553(
    value: typing.Optional[VmInternalDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0279750f8e7866c69365f7a43e351366831b679484c3488e02011f0f5ec0680(
    *,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4861ea661a18b10a89e8e4cfcc561aab941c34ef4866b3d132f2e4e19f6fd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2617b134f1083042613de3c3dc22dd6b37df2dcaa7d2f321eba18b65c056744c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2704328ea4315323fe3c916a18c21a6daa3d5b1d01194081d8f092654c240118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ad539d0e72fd59435237ff55ed49b6cfe4459cb7d1d3131c8072825964f795(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361fae3baf5f1bab36a9634cb81d14a41e894ba0a1a205abe8f59e08eaee23a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5bd0ddc0a22c94b68ea325db4b2a08fd0dd3659780b97232bcca4343e541e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmMetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332679cc31ef68746548b2de928e0c53f5ed704fd872932df05e1a79cdd10823(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c578c79af472d247a4aaa126297eddc5956ca111ffc8234a1ad526e7858f893(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b4eecaa7a94bfbe8fed06891f7d9e4000d152e80c8f9f4f77f44f6716334ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6342bfd1b44cbd5c7de9c601f30ab881e97bb028fe5620e374a64eec2c6eb2f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b9cf1e7a1e4fd96e907acf314d637b75db9a5ecc9af03cea3f8f87dfb61d27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1925c5c56cef763455220c0eabbc7fdde6bdc99526e783c63fe2a00f539b8d60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7555d6146093dec340bbfec6cbb7a8708ac8a0e9d9697a88166e97b3e003ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmMetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0587503595b897910d2fa9692113062efeaca128956bc5ba2b9cebc76996803(
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

def _typecheckingstub__9ca0010f62f4879205fd527961a83bb71c6d3af638896a51148467511ea8b64b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd65d3d52dff9b912c511498e883719a465cd54ca0d6191f4e9942c7eebb78a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc1ff6733df5a6a720f8485bee1d0b9167a4a6f3b091b3693624d1e7f7a071c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6b0753ed301185479826e74a95934db13cb274c2138d3bfb32bcc9588e0bf1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc859bffb717b7e86c7340103e3f8325836ed198c8dd73c362176742096496f8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f1670596aca1d916966c12d0b8b0b8f63aa75022779efda6f292e1b75b093c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9990794bd1a4caef88e8effb7fd4ba154cc7b60229702deb7d8442f86b60ce8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ad14415fdb80ffc9dc7cd92ec8ab2de83aa5e5d836b886c0cbab39c371eb07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffe33ac874a8fb508323cb8335a52dde08b6659eadbc4f8fe8eed14f05028f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60787da38b1e39c0a4ea2a66fa3e2c7ba95c1bc0166386e931fda37878b78a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea96ceb26227eaedcf34fc02e065c0d865779be3f7a50d924d26776c17c6766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18a98a7604e4c7fef51223d36b740c0ebb83595e7a63807c7a3d399d615827c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a37269daaacf36fc56ee471bac12494c758d3cf13d76ffea5617b2c887dd47f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb90d014fce576b8cc76590666e4fbd86d64f660ed86da7666747297b24b294c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caafe86a98fccf8d93740691d6411f1121de06734637eab8d63b2e81497455f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92529d196084c966287acffb69ba009f3a2fd205305535727a3f8c06d89eed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f466202fc726c893442b7ad68ca9209e97941c0381f341c283af8a85b1c1e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5676ba1c05dc7f106516e9c1d5f98aca0f1364cdcd8ec437619f75b2ea52d8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmNetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54431dfca999d59b79a98f62b48ace879953ae5655be2c3c8b4e2b09d6738fec(
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

def _typecheckingstub__d8a9c922fc2e85a93e3a80bee8322ee08516a8de4c95d4c400c9c645415fcc1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670bc2fb602691a7441847de1a344ac58a7f7ad395c24149787b89e75d25e384(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd798ed28ffa2fc5177034a0301e482d38da248b3df6182e70c190fab95a538c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0a2a178ba76c30ee3fa9effca10fce66d79834c00ec95acfa37df841bf005d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7737f9c5a0ae8c19b1426718511a93a326e3dfb3baad6eaa3d76ce76d4cd2a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7ce34649d485e9d2461551c9088be33cc80f05872c5bdbaddc081e20365b90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmOverrideTemplateDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab575bfef66decaa2f0a62f534a62a1b7f6b8eb9b2f3cc40bf8627c0421185a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5856fded2c124d21b70cfc7c0aaa94d9da818113c61fe172ba658b4759c9c8a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990acc45d6c581dae12abe42a4fc3724ade2775c38144c8e104a0784e1ec699e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141e60921717b5f53ccab186ef5f8007675c81409f4675980e1ff1078d524e9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879a3cd6cfa03297b75a5fab31ed830e390d739be20da188d44190c4c8905bc8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeff081184308340096d1d523e060c028bf8a815c63aa475494da58272a0a6f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2f801f34d89c963a2d95deecebdf254672e91d0421e4e996366a1122c20404(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8e2e98c3fda62036fc831aa0465073a1ab5047765f3a3c40b8d60f23830a2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmOverrideTemplateDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0aaa354dd9b568a5531e7a257447192372f4f7fe776f5885c785e4b73e971cb(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd766b960899f6d6e9c1645b3a819ea358e932f88aa8dd8dc87da90bafc94f41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24782b58ddf128711c4713f38dcaa3961c179fd8dca6ebf2b90c4cbbc0f4079a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5afefb82c0a22d5dcffbf812c34b2e531435e401a3d542888d7fd71a7e52bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3823dbfdf889a29c1fb149d38f907efc4e7bf511983a56c4e6cc54ecc80c1de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f7872964b9ec59ae7b3edb2ceb524227e7130f5b6098098f6a3758d1f21437(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee80a7110d5fc6d537bae36c0dbbe92caf2e9d67ddf3f802b265091725493d9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmSetExtraConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39d1cd879daa21f1b5d7de98f913d8bb2e676aa2c96d7aa9cd912f9f43bd25d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ccaf51d5997f6fe775ff505c0a698f55786b6032d5c29d6e7133cd3bec02b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509bdb3a1ce2b56ae2d9680ce6d5b7e061ee2d01cba5ef30459a60577718ca31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6dc815c04ed5f8e39e2d3fc0be3c6839f67441e388fa4613af68a2fabe3fa62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmSetExtraConfig]],
) -> None:
    """Type checking stubs"""
    pass
