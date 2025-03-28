'''
# `vcd_catalog_vapp_template`

Refer to the Terraform Registry for docs: [`vcd_catalog_vapp_template`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template).
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


class CatalogVappTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template vcd_catalog_vapp_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        catalog_id: builtins.str,
        name: builtins.str,
        capture_vapp: typing.Optional[typing.Union["CatalogVappTemplateCaptureVapp", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lease: typing.Optional[typing.Union["CatalogVappTemplateLease", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CatalogVappTemplateMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        org: typing.Optional[builtins.str] = None,
        ova_path: typing.Optional[builtins.str] = None,
        ovf_url: typing.Optional[builtins.str] = None,
        upload_piece_size: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template vcd_catalog_vapp_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param catalog_id: ID of the Catalog where to upload the OVA file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#catalog_id CatalogVappTemplate#catalog_id}
        :param name: vApp Template name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#name CatalogVappTemplate#name}
        :param capture_vapp: capture_vapp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#capture_vapp CatalogVappTemplate#capture_vapp}
        :param description: Description of the vApp Template. Not to be used with ``ovf_url`` when target OVA has a description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#description CatalogVappTemplate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#id CatalogVappTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lease: lease block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#lease CatalogVappTemplate#lease}
        :param metadata: Key and value pairs for the metadata of this vApp Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#metadata CatalogVappTemplate#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#metadata_entry CatalogVappTemplate#metadata_entry}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#org CatalogVappTemplate#org}
        :param ova_path: Absolute or relative path to OVA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#ova_path CatalogVappTemplate#ova_path}
        :param ovf_url: URL of OVF file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#ovf_url CatalogVappTemplate#ovf_url}
        :param upload_piece_size: Size of upload file piece size in megabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#upload_piece_size CatalogVappTemplate#upload_piece_size}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4c2e681d11e868da0b30a38977cc26310b5adca55c4f4b72e707ea595ebc9f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CatalogVappTemplateConfig(
            catalog_id=catalog_id,
            name=name,
            capture_vapp=capture_vapp,
            description=description,
            id=id,
            lease=lease,
            metadata=metadata,
            metadata_entry=metadata_entry,
            org=org,
            ova_path=ova_path,
            ovf_url=ovf_url,
            upload_piece_size=upload_piece_size,
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
        '''Generates CDKTF code for importing a CatalogVappTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CatalogVappTemplate to import.
        :param import_from_id: The id of the existing CatalogVappTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CatalogVappTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115fc1fec6ebf240a6eb2f3b21734fead872048c3489ca04887a64c363c12d68)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCaptureVapp")
    def put_capture_vapp(
        self,
        *,
        copy_tpm_on_instantiate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        customize_on_instantiate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_catalog_item_id: typing.Optional[builtins.str] = None,
        source_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param copy_tpm_on_instantiate: Defines if Trusted Platform Module should be copied (false) or created (true). Default 'false'. VCD 10.4.2+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#copy_tpm_on_instantiate CatalogVappTemplate#copy_tpm_on_instantiate}
        :param customize_on_instantiate: Marks if instantiating applies customization settings ('true'). Default is 'false` - create an identical copy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#customize_on_instantiate CatalogVappTemplate#customize_on_instantiate}
        :param overwrite_catalog_item_id: An existing catalog item ID to overwrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#overwrite_catalog_item_id CatalogVappTemplate#overwrite_catalog_item_id}
        :param source_id: Source vApp ID (can be a vApp ID or 'vapp_id' field of standalone VM 'vcd_vm'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#source_id CatalogVappTemplate#source_id}
        '''
        value = CatalogVappTemplateCaptureVapp(
            copy_tpm_on_instantiate=copy_tpm_on_instantiate,
            customize_on_instantiate=customize_on_instantiate,
            overwrite_catalog_item_id=overwrite_catalog_item_id,
            source_id=source_id,
        )

        return typing.cast(None, jsii.invoke(self, "putCaptureVapp", [value]))

    @jsii.member(jsii_name="putLease")
    def put_lease(self, *, storage_lease_in_sec: jsii.Number) -> None:
        '''
        :param storage_lease_in_sec: How long the vApp template is available before being automatically deleted or marked as expired. 0 means never expires (or expires at the maximum limit provided by the parent Org) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#storage_lease_in_sec CatalogVappTemplate#storage_lease_in_sec}
        '''
        value = CatalogVappTemplateLease(storage_lease_in_sec=storage_lease_in_sec)

        return typing.cast(None, jsii.invoke(self, "putLease", [value]))

    @jsii.member(jsii_name="putMetadataEntry")
    def put_metadata_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CatalogVappTemplateMetadataEntry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f8192e3f5ccb9a243f6b5737ef3744ac7ee8ce4b9f40c5fe04208ddcfd9d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataEntry", [value]))

    @jsii.member(jsii_name="resetCaptureVapp")
    def reset_capture_vapp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptureVapp", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLease")
    def reset_lease(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLease", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataEntry")
    def reset_metadata_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataEntry", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOvaPath")
    def reset_ova_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOvaPath", []))

    @jsii.member(jsii_name="resetOvfUrl")
    def reset_ovf_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOvfUrl", []))

    @jsii.member(jsii_name="resetUploadPieceSize")
    def reset_upload_piece_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUploadPieceSize", []))

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
    @jsii.member(jsii_name="captureVapp")
    def capture_vapp(self) -> "CatalogVappTemplateCaptureVappOutputReference":
        return typing.cast("CatalogVappTemplateCaptureVappOutputReference", jsii.get(self, "captureVapp"))

    @builtins.property
    @jsii.member(jsii_name="catalogItemId")
    def catalog_item_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogItemId"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="inheritedMetadata")
    def inherited_metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "inheritedMetadata"))

    @builtins.property
    @jsii.member(jsii_name="lease")
    def lease(self) -> "CatalogVappTemplateLeaseOutputReference":
        return typing.cast("CatalogVappTemplateLeaseOutputReference", jsii.get(self, "lease"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntry")
    def metadata_entry(self) -> "CatalogVappTemplateMetadataEntryList":
        return typing.cast("CatalogVappTemplateMetadataEntryList", jsii.get(self, "metadataEntry"))

    @builtins.property
    @jsii.member(jsii_name="vdcId")
    def vdc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcId"))

    @builtins.property
    @jsii.member(jsii_name="vmNames")
    def vm_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vmNames"))

    @builtins.property
    @jsii.member(jsii_name="captureVappInput")
    def capture_vapp_input(self) -> typing.Optional["CatalogVappTemplateCaptureVapp"]:
        return typing.cast(typing.Optional["CatalogVappTemplateCaptureVapp"], jsii.get(self, "captureVappInput"))

    @builtins.property
    @jsii.member(jsii_name="catalogIdInput")
    def catalog_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="leaseInput")
    def lease_input(self) -> typing.Optional["CatalogVappTemplateLease"]:
        return typing.cast(typing.Optional["CatalogVappTemplateLease"], jsii.get(self, "leaseInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataEntryInput")
    def metadata_entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CatalogVappTemplateMetadataEntry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CatalogVappTemplateMetadataEntry"]]], jsii.get(self, "metadataEntryInput"))

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
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="ovaPathInput")
    def ova_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ovaPathInput"))

    @builtins.property
    @jsii.member(jsii_name="ovfUrlInput")
    def ovf_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ovfUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="uploadPieceSizeInput")
    def upload_piece_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "uploadPieceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogId"))

    @catalog_id.setter
    def catalog_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4f71a75177c9498efaddc4a013165c5ce7884563cac0d0fd9016d052277bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalogId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e3a9d65e162d98164dc68e86a06f468a41695181272b7fabb723d90423accb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce1b038c033b794515895eebe23af57649440c25c0a88782a26a114ff8c8208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0796757eabc22a396c8f8c53f4db020d0de5165bd3a256cb708d325267bd6ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d503936d67927b4a655fc93f98ec4caebc8c19328e1bd4e91043539768bbe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbba600bbfff8f6c8880a6d7da808d9d3cde6c332cbe8c5b2fd2ec8e056d19d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="ovaPath")
    def ova_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ovaPath"))

    @ova_path.setter
    def ova_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a77c815a3045b5e41df04ca9bc44b99af0a9e4a8cc93ff62c5b07579514578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ovaPath", value)

    @builtins.property
    @jsii.member(jsii_name="ovfUrl")
    def ovf_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ovfUrl"))

    @ovf_url.setter
    def ovf_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0f6e29f2e8a796b3be2a16eb81cec13e853b860c478b316726d18e4e6c17cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ovfUrl", value)

    @builtins.property
    @jsii.member(jsii_name="uploadPieceSize")
    def upload_piece_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "uploadPieceSize"))

    @upload_piece_size.setter
    def upload_piece_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6b81894c6818443421d07da1904384064404afa69dce60ed9d546d7fc1bd0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadPieceSize", value)


@jsii.data_type(
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplateCaptureVapp",
    jsii_struct_bases=[],
    name_mapping={
        "copy_tpm_on_instantiate": "copyTpmOnInstantiate",
        "customize_on_instantiate": "customizeOnInstantiate",
        "overwrite_catalog_item_id": "overwriteCatalogItemId",
        "source_id": "sourceId",
    },
)
class CatalogVappTemplateCaptureVapp:
    def __init__(
        self,
        *,
        copy_tpm_on_instantiate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        customize_on_instantiate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overwrite_catalog_item_id: typing.Optional[builtins.str] = None,
        source_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param copy_tpm_on_instantiate: Defines if Trusted Platform Module should be copied (false) or created (true). Default 'false'. VCD 10.4.2+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#copy_tpm_on_instantiate CatalogVappTemplate#copy_tpm_on_instantiate}
        :param customize_on_instantiate: Marks if instantiating applies customization settings ('true'). Default is 'false` - create an identical copy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#customize_on_instantiate CatalogVappTemplate#customize_on_instantiate}
        :param overwrite_catalog_item_id: An existing catalog item ID to overwrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#overwrite_catalog_item_id CatalogVappTemplate#overwrite_catalog_item_id}
        :param source_id: Source vApp ID (can be a vApp ID or 'vapp_id' field of standalone VM 'vcd_vm'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#source_id CatalogVappTemplate#source_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f9eef0c5c82830df184776653f8b20ad5ee11e00c7592cda97a8df960c82fb)
            check_type(argname="argument copy_tpm_on_instantiate", value=copy_tpm_on_instantiate, expected_type=type_hints["copy_tpm_on_instantiate"])
            check_type(argname="argument customize_on_instantiate", value=customize_on_instantiate, expected_type=type_hints["customize_on_instantiate"])
            check_type(argname="argument overwrite_catalog_item_id", value=overwrite_catalog_item_id, expected_type=type_hints["overwrite_catalog_item_id"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if copy_tpm_on_instantiate is not None:
            self._values["copy_tpm_on_instantiate"] = copy_tpm_on_instantiate
        if customize_on_instantiate is not None:
            self._values["customize_on_instantiate"] = customize_on_instantiate
        if overwrite_catalog_item_id is not None:
            self._values["overwrite_catalog_item_id"] = overwrite_catalog_item_id
        if source_id is not None:
            self._values["source_id"] = source_id

    @builtins.property
    def copy_tpm_on_instantiate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines if Trusted Platform Module should be copied (false) or created (true). Default 'false'. VCD 10.4.2+.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#copy_tpm_on_instantiate CatalogVappTemplate#copy_tpm_on_instantiate}
        '''
        result = self._values.get("copy_tpm_on_instantiate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def customize_on_instantiate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Marks if instantiating applies customization settings ('true'). Default is 'false` - create an identical copy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#customize_on_instantiate CatalogVappTemplate#customize_on_instantiate}
        '''
        result = self._values.get("customize_on_instantiate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def overwrite_catalog_item_id(self) -> typing.Optional[builtins.str]:
        '''An existing catalog item ID to overwrite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#overwrite_catalog_item_id CatalogVappTemplate#overwrite_catalog_item_id}
        '''
        result = self._values.get("overwrite_catalog_item_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_id(self) -> typing.Optional[builtins.str]:
        '''Source vApp ID (can be a vApp ID or 'vapp_id' field of standalone VM 'vcd_vm').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#source_id CatalogVappTemplate#source_id}
        '''
        result = self._values.get("source_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CatalogVappTemplateCaptureVapp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CatalogVappTemplateCaptureVappOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplateCaptureVappOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f583abb35f3e1b17e7646ba370a6c708e8a645c6cf4dd4fc14f7288394bed7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCopyTpmOnInstantiate")
    def reset_copy_tpm_on_instantiate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTpmOnInstantiate", []))

    @jsii.member(jsii_name="resetCustomizeOnInstantiate")
    def reset_customize_on_instantiate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomizeOnInstantiate", []))

    @jsii.member(jsii_name="resetOverwriteCatalogItemId")
    def reset_overwrite_catalog_item_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteCatalogItemId", []))

    @jsii.member(jsii_name="resetSourceId")
    def reset_source_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceId", []))

    @builtins.property
    @jsii.member(jsii_name="copyTpmOnInstantiateInput")
    def copy_tpm_on_instantiate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTpmOnInstantiateInput"))

    @builtins.property
    @jsii.member(jsii_name="customizeOnInstantiateInput")
    def customize_on_instantiate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customizeOnInstantiateInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteCatalogItemIdInput")
    def overwrite_catalog_item_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overwriteCatalogItemIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIdInput")
    def source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTpmOnInstantiate")
    def copy_tpm_on_instantiate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTpmOnInstantiate"))

    @copy_tpm_on_instantiate.setter
    def copy_tpm_on_instantiate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfb1c771ae90fc7b6b2b2a15392029d5eb142bf28cedd763aac3deb0611f37be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTpmOnInstantiate", value)

    @builtins.property
    @jsii.member(jsii_name="customizeOnInstantiate")
    def customize_on_instantiate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customizeOnInstantiate"))

    @customize_on_instantiate.setter
    def customize_on_instantiate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459f7794eb64c82ccaae88df6df7aed11cd606ed390fccb10866c19bb7219c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customizeOnInstantiate", value)

    @builtins.property
    @jsii.member(jsii_name="overwriteCatalogItemId")
    def overwrite_catalog_item_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overwriteCatalogItemId"))

    @overwrite_catalog_item_id.setter
    def overwrite_catalog_item_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06482abace35b6cb326a177308de9109715578ad5791330660c9162826a343a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteCatalogItemId", value)

    @builtins.property
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceId"))

    @source_id.setter
    def source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c434fc557b99d4ec98b285fa10d3ab199cdb04fe850e4fe680f73bb0e9ce6f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CatalogVappTemplateCaptureVapp]:
        return typing.cast(typing.Optional[CatalogVappTemplateCaptureVapp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CatalogVappTemplateCaptureVapp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3315e2069ba9b13e679e0e2e4cce7a751669e180d4c698997f274b429d2fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "catalog_id": "catalogId",
        "name": "name",
        "capture_vapp": "captureVapp",
        "description": "description",
        "id": "id",
        "lease": "lease",
        "metadata": "metadata",
        "metadata_entry": "metadataEntry",
        "org": "org",
        "ova_path": "ovaPath",
        "ovf_url": "ovfUrl",
        "upload_piece_size": "uploadPieceSize",
    },
)
class CatalogVappTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        catalog_id: builtins.str,
        name: builtins.str,
        capture_vapp: typing.Optional[typing.Union[CatalogVappTemplateCaptureVapp, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lease: typing.Optional[typing.Union["CatalogVappTemplateLease", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CatalogVappTemplateMetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        org: typing.Optional[builtins.str] = None,
        ova_path: typing.Optional[builtins.str] = None,
        ovf_url: typing.Optional[builtins.str] = None,
        upload_piece_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param catalog_id: ID of the Catalog where to upload the OVA file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#catalog_id CatalogVappTemplate#catalog_id}
        :param name: vApp Template name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#name CatalogVappTemplate#name}
        :param capture_vapp: capture_vapp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#capture_vapp CatalogVappTemplate#capture_vapp}
        :param description: Description of the vApp Template. Not to be used with ``ovf_url`` when target OVA has a description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#description CatalogVappTemplate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#id CatalogVappTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lease: lease block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#lease CatalogVappTemplate#lease}
        :param metadata: Key and value pairs for the metadata of this vApp Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#metadata CatalogVappTemplate#metadata}
        :param metadata_entry: metadata_entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#metadata_entry CatalogVappTemplate#metadata_entry}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#org CatalogVappTemplate#org}
        :param ova_path: Absolute or relative path to OVA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#ova_path CatalogVappTemplate#ova_path}
        :param ovf_url: URL of OVF file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#ovf_url CatalogVappTemplate#ovf_url}
        :param upload_piece_size: Size of upload file piece size in megabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#upload_piece_size CatalogVappTemplate#upload_piece_size}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capture_vapp, dict):
            capture_vapp = CatalogVappTemplateCaptureVapp(**capture_vapp)
        if isinstance(lease, dict):
            lease = CatalogVappTemplateLease(**lease)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d737f9a4feafd206076a661f2ae3e94f4ab7fa5c6aeb93781d56c18a41725b42)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument capture_vapp", value=capture_vapp, expected_type=type_hints["capture_vapp"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lease", value=lease, expected_type=type_hints["lease"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_entry", value=metadata_entry, expected_type=type_hints["metadata_entry"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument ova_path", value=ova_path, expected_type=type_hints["ova_path"])
            check_type(argname="argument ovf_url", value=ovf_url, expected_type=type_hints["ovf_url"])
            check_type(argname="argument upload_piece_size", value=upload_piece_size, expected_type=type_hints["upload_piece_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "catalog_id": catalog_id,
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
        if capture_vapp is not None:
            self._values["capture_vapp"] = capture_vapp
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if lease is not None:
            self._values["lease"] = lease
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_entry is not None:
            self._values["metadata_entry"] = metadata_entry
        if org is not None:
            self._values["org"] = org
        if ova_path is not None:
            self._values["ova_path"] = ova_path
        if ovf_url is not None:
            self._values["ovf_url"] = ovf_url
        if upload_piece_size is not None:
            self._values["upload_piece_size"] = upload_piece_size

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
    def catalog_id(self) -> builtins.str:
        '''ID of the Catalog where to upload the OVA file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#catalog_id CatalogVappTemplate#catalog_id}
        '''
        result = self._values.get("catalog_id")
        assert result is not None, "Required property 'catalog_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''vApp Template name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#name CatalogVappTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capture_vapp(self) -> typing.Optional[CatalogVappTemplateCaptureVapp]:
        '''capture_vapp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#capture_vapp CatalogVappTemplate#capture_vapp}
        '''
        result = self._values.get("capture_vapp")
        return typing.cast(typing.Optional[CatalogVappTemplateCaptureVapp], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the vApp Template. Not to be used with ``ovf_url`` when target OVA has a description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#description CatalogVappTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#id CatalogVappTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lease(self) -> typing.Optional["CatalogVappTemplateLease"]:
        '''lease block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#lease CatalogVappTemplate#lease}
        '''
        result = self._values.get("lease")
        return typing.cast(typing.Optional["CatalogVappTemplateLease"], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key and value pairs for the metadata of this vApp Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#metadata CatalogVappTemplate#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CatalogVappTemplateMetadataEntry"]]]:
        '''metadata_entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#metadata_entry CatalogVappTemplate#metadata_entry}
        '''
        result = self._values.get("metadata_entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CatalogVappTemplateMetadataEntry"]]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#org CatalogVappTemplate#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ova_path(self) -> typing.Optional[builtins.str]:
        '''Absolute or relative path to OVA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#ova_path CatalogVappTemplate#ova_path}
        '''
        result = self._values.get("ova_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ovf_url(self) -> typing.Optional[builtins.str]:
        '''URL of OVF file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#ovf_url CatalogVappTemplate#ovf_url}
        '''
        result = self._values.get("ovf_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_piece_size(self) -> typing.Optional[jsii.Number]:
        '''Size of upload file piece size in megabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#upload_piece_size CatalogVappTemplate#upload_piece_size}
        '''
        result = self._values.get("upload_piece_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CatalogVappTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplateLease",
    jsii_struct_bases=[],
    name_mapping={"storage_lease_in_sec": "storageLeaseInSec"},
)
class CatalogVappTemplateLease:
    def __init__(self, *, storage_lease_in_sec: jsii.Number) -> None:
        '''
        :param storage_lease_in_sec: How long the vApp template is available before being automatically deleted or marked as expired. 0 means never expires (or expires at the maximum limit provided by the parent Org) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#storage_lease_in_sec CatalogVappTemplate#storage_lease_in_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de587284ccb28111267700ddc5fd217f2f2189e59e21f75f65f0fa0a0d692e1e)
            check_type(argname="argument storage_lease_in_sec", value=storage_lease_in_sec, expected_type=type_hints["storage_lease_in_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_lease_in_sec": storage_lease_in_sec,
        }

    @builtins.property
    def storage_lease_in_sec(self) -> jsii.Number:
        '''How long the vApp template is available before being automatically deleted or marked as expired.

        0 means never expires (or expires at the maximum limit provided by the parent Org)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#storage_lease_in_sec CatalogVappTemplate#storage_lease_in_sec}
        '''
        result = self._values.get("storage_lease_in_sec")
        assert result is not None, "Required property 'storage_lease_in_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CatalogVappTemplateLease(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CatalogVappTemplateLeaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplateLeaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b3c144612330ad1b3c54f5b2d2002268f3e444385d66f1a57e82da32aa96e1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="storageLeaseInSecInput")
    def storage_lease_in_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageLeaseInSecInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLeaseInSec")
    def storage_lease_in_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageLeaseInSec"))

    @storage_lease_in_sec.setter
    def storage_lease_in_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d566eb77a61d1f1e675e28882684cdbf0a4bbfbe87dec92fe276f2acba1f39df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageLeaseInSec", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CatalogVappTemplateLease]:
        return typing.cast(typing.Optional[CatalogVappTemplateLease], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CatalogVappTemplateLease]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f214f2038ffbd6aa64a474a53780606b6f0bfcd1fccd357f413520041d889a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplateMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "is_system": "isSystem",
        "key": "key",
        "type": "type",
        "user_access": "userAccess",
        "value": "value",
    },
)
class CatalogVappTemplateMetadataEntry:
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
        :param is_system: Domain for this metadata entry. true, if it belongs to SYSTEM. false, if it belongs to GENERAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#is_system CatalogVappTemplate#is_system}
        :param key: Key of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#key CatalogVappTemplate#key}
        :param type: Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#type CatalogVappTemplate#type}
        :param user_access: User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#user_access CatalogVappTemplate#user_access}
        :param value: Value of this metadata entry. Required if the metadata entry is not empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#value CatalogVappTemplate#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b5c4c509ec4f39c1e77251560ce8c89ab976472fd6594a9ca7c542cb44993d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#is_system CatalogVappTemplate#is_system}
        '''
        result = self._values.get("is_system")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#key CatalogVappTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of this metadata entry. One of: 'MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue', 'MetadataDateTimeValue'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#type CatalogVappTemplate#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access(self) -> typing.Optional[builtins.str]:
        '''User access level for this metadata entry. One of: 'READWRITE', 'READONLY', 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#user_access CatalogVappTemplate#user_access}
        '''
        result = self._values.get("user_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of this metadata entry. Required if the metadata entry is not empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/catalog_vapp_template#value CatalogVappTemplate#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CatalogVappTemplateMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CatalogVappTemplateMetadataEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplateMetadataEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea2cc9657b9a5da4898e02df978e7726620a17e4c17b3307d50de796dcccac32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CatalogVappTemplateMetadataEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ddec04c48453db8c84f589620335a61ef1b13a138a7633f8568969bdb41ee3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CatalogVappTemplateMetadataEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d037c802e57a76d3a795515af48fb2cdd1a4a99fa63a5239d785ffccb87f36a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__229026bb86c80cf9e07f6145f44122430f52bc146ef9da345d9fc992a2c7de73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a6eaa4c30bd834612f8b0eb2904b7f8f370ec5fc88c87182a0a014b71b923ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CatalogVappTemplateMetadataEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CatalogVappTemplateMetadataEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CatalogVappTemplateMetadataEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a26f583755b7541daf3c71fcf63f3aea24db05062fe98e1e3f5058b6978e7a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CatalogVappTemplateMetadataEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.catalogVappTemplate.CatalogVappTemplateMetadataEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e64ee9ab2b742b600de3b2ee11eb457b0398f741fa2749fdc75b4c8ce5b6f5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c755be01afac22dafda5b887e82cf6344cdca5644c621492d3670cdc84e702aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSystem", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcdfe325d41f84cb2231d5544a426b6445df71fdd8f34df3a83572f5f1f3af75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cd7a32222dedfb4038470063ff5dbae12d008dd86538976cc57d26e648057f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userAccess")
    def user_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAccess"))

    @user_access.setter
    def user_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d51ad899d61ad4225dabaddbba2e3876732910e82666ce2300a0a3762a4f1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAccess", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00aaabc7c2167939804d1af3a7218c0a377970cd0359bd43b4feaced873497b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CatalogVappTemplateMetadataEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CatalogVappTemplateMetadataEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CatalogVappTemplateMetadataEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc0f31ad78e94d3f09e05bfbcdcbc49158d8a9b471791bfb18d70f5ad2be58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CatalogVappTemplate",
    "CatalogVappTemplateCaptureVapp",
    "CatalogVappTemplateCaptureVappOutputReference",
    "CatalogVappTemplateConfig",
    "CatalogVappTemplateLease",
    "CatalogVappTemplateLeaseOutputReference",
    "CatalogVappTemplateMetadataEntry",
    "CatalogVappTemplateMetadataEntryList",
    "CatalogVappTemplateMetadataEntryOutputReference",
]

publication.publish()

def _typecheckingstub__fd4c2e681d11e868da0b30a38977cc26310b5adca55c4f4b72e707ea595ebc9f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    catalog_id: builtins.str,
    name: builtins.str,
    capture_vapp: typing.Optional[typing.Union[CatalogVappTemplateCaptureVapp, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lease: typing.Optional[typing.Union[CatalogVappTemplateLease, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CatalogVappTemplateMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org: typing.Optional[builtins.str] = None,
    ova_path: typing.Optional[builtins.str] = None,
    ovf_url: typing.Optional[builtins.str] = None,
    upload_piece_size: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__115fc1fec6ebf240a6eb2f3b21734fead872048c3489ca04887a64c363c12d68(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f8192e3f5ccb9a243f6b5737ef3744ac7ee8ce4b9f40c5fe04208ddcfd9d13(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CatalogVappTemplateMetadataEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4f71a75177c9498efaddc4a013165c5ce7884563cac0d0fd9016d052277bf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e3a9d65e162d98164dc68e86a06f468a41695181272b7fabb723d90423accb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce1b038c033b794515895eebe23af57649440c25c0a88782a26a114ff8c8208(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0796757eabc22a396c8f8c53f4db020d0de5165bd3a256cb708d325267bd6ab7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d503936d67927b4a655fc93f98ec4caebc8c19328e1bd4e91043539768bbe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbba600bbfff8f6c8880a6d7da808d9d3cde6c332cbe8c5b2fd2ec8e056d19d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a77c815a3045b5e41df04ca9bc44b99af0a9e4a8cc93ff62c5b07579514578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0f6e29f2e8a796b3be2a16eb81cec13e853b860c478b316726d18e4e6c17cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6b81894c6818443421d07da1904384064404afa69dce60ed9d546d7fc1bd0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f9eef0c5c82830df184776653f8b20ad5ee11e00c7592cda97a8df960c82fb(
    *,
    copy_tpm_on_instantiate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    customize_on_instantiate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    overwrite_catalog_item_id: typing.Optional[builtins.str] = None,
    source_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f583abb35f3e1b17e7646ba370a6c708e8a645c6cf4dd4fc14f7288394bed7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb1c771ae90fc7b6b2b2a15392029d5eb142bf28cedd763aac3deb0611f37be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459f7794eb64c82ccaae88df6df7aed11cd606ed390fccb10866c19bb7219c42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06482abace35b6cb326a177308de9109715578ad5791330660c9162826a343a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c434fc557b99d4ec98b285fa10d3ab199cdb04fe850e4fe680f73bb0e9ce6f74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3315e2069ba9b13e679e0e2e4cce7a751669e180d4c698997f274b429d2fcb(
    value: typing.Optional[CatalogVappTemplateCaptureVapp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d737f9a4feafd206076a661f2ae3e94f4ab7fa5c6aeb93781d56c18a41725b42(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    catalog_id: builtins.str,
    name: builtins.str,
    capture_vapp: typing.Optional[typing.Union[CatalogVappTemplateCaptureVapp, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lease: typing.Optional[typing.Union[CatalogVappTemplateLease, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CatalogVappTemplateMetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org: typing.Optional[builtins.str] = None,
    ova_path: typing.Optional[builtins.str] = None,
    ovf_url: typing.Optional[builtins.str] = None,
    upload_piece_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de587284ccb28111267700ddc5fd217f2f2189e59e21f75f65f0fa0a0d692e1e(
    *,
    storage_lease_in_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3c144612330ad1b3c54f5b2d2002268f3e444385d66f1a57e82da32aa96e1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d566eb77a61d1f1e675e28882684cdbf0a4bbfbe87dec92fe276f2acba1f39df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f214f2038ffbd6aa64a474a53780606b6f0bfcd1fccd357f413520041d889a68(
    value: typing.Optional[CatalogVappTemplateLease],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b5c4c509ec4f39c1e77251560ce8c89ab976472fd6594a9ca7c542cb44993d(
    *,
    is_system: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_access: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2cc9657b9a5da4898e02df978e7726620a17e4c17b3307d50de796dcccac32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ddec04c48453db8c84f589620335a61ef1b13a138a7633f8568969bdb41ee3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d037c802e57a76d3a795515af48fb2cdd1a4a99fa63a5239d785ffccb87f36a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229026bb86c80cf9e07f6145f44122430f52bc146ef9da345d9fc992a2c7de73(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6eaa4c30bd834612f8b0eb2904b7f8f370ec5fc88c87182a0a014b71b923ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a26f583755b7541daf3c71fcf63f3aea24db05062fe98e1e3f5058b6978e7a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CatalogVappTemplateMetadataEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e64ee9ab2b742b600de3b2ee11eb457b0398f741fa2749fdc75b4c8ce5b6f5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c755be01afac22dafda5b887e82cf6344cdca5644c621492d3670cdc84e702aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcdfe325d41f84cb2231d5544a426b6445df71fdd8f34df3a83572f5f1f3af75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cd7a32222dedfb4038470063ff5dbae12d008dd86538976cc57d26e648057f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d51ad899d61ad4225dabaddbba2e3876732910e82666ce2300a0a3762a4f1ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00aaabc7c2167939804d1af3a7218c0a377970cd0359bd43b4feaced873497b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc0f31ad78e94d3f09e05bfbcdcbc49158d8a9b471791bfb18d70f5ad2be58f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CatalogVappTemplateMetadataEntry]],
) -> None:
    """Type checking stubs"""
    pass
