'''
# `vcd_org_vdc_nsxt_network_profile`

Refer to the Terraform Registry for docs: [`vcd_org_vdc_nsxt_network_profile`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile).
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


class OrgVdcNsxtNetworkProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgVdcNsxtNetworkProfile.OrgVdcNsxtNetworkProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile vcd_org_vdc_nsxt_network_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_cluster_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        vapp_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        vdc_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile vcd_org_vdc_nsxt_network_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_cluster_id: ID of NSX-T Edge Cluster (provider vApp networking services and DHCP capability for Isolated networks). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#edge_cluster_id OrgVdcNsxtNetworkProfile#edge_cluster_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#id OrgVdcNsxtNetworkProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#org OrgVdcNsxtNetworkProfile#org}
        :param vapp_networks_default_segment_profile_template_id: Default NSX-T Segment Profile for vApp networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vapp_networks_default_segment_profile_template_id OrgVdcNsxtNetworkProfile#vapp_networks_default_segment_profile_template_id}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vdc OrgVdcNsxtNetworkProfile#vdc}
        :param vdc_networks_default_segment_profile_template_id: Default NSX-T Segment Profile for Org VDC networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vdc_networks_default_segment_profile_template_id OrgVdcNsxtNetworkProfile#vdc_networks_default_segment_profile_template_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34e42ab787b1543b2cd1db130519f7e823d766e0d825b30b31dea8517c67fbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrgVdcNsxtNetworkProfileConfig(
            edge_cluster_id=edge_cluster_id,
            id=id,
            org=org,
            vapp_networks_default_segment_profile_template_id=vapp_networks_default_segment_profile_template_id,
            vdc=vdc,
            vdc_networks_default_segment_profile_template_id=vdc_networks_default_segment_profile_template_id,
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
        '''Generates CDKTF code for importing a OrgVdcNsxtNetworkProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrgVdcNsxtNetworkProfile to import.
        :param import_from_id: The id of the existing OrgVdcNsxtNetworkProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrgVdcNsxtNetworkProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26dd8bd7be8552ff0bea65a05635ceaf258cced655e0d571ed2979a837752ce6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetEdgeClusterId")
    def reset_edge_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeClusterId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetVappNetworksDefaultSegmentProfileTemplateId")
    def reset_vapp_networks_default_segment_profile_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVappNetworksDefaultSegmentProfileTemplateId", []))

    @jsii.member(jsii_name="resetVdc")
    def reset_vdc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdc", []))

    @jsii.member(jsii_name="resetVdcNetworksDefaultSegmentProfileTemplateId")
    def reset_vdc_networks_default_segment_profile_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdcNetworksDefaultSegmentProfileTemplateId", []))

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
    @jsii.member(jsii_name="edgeClusterIdInput")
    def edge_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="vappNetworksDefaultSegmentProfileTemplateIdInput")
    def vapp_networks_default_segment_profile_template_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vappNetworksDefaultSegmentProfileTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcNetworksDefaultSegmentProfileTemplateIdInput")
    def vdc_networks_default_segment_profile_template_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcNetworksDefaultSegmentProfileTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeClusterId")
    def edge_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeClusterId"))

    @edge_cluster_id.setter
    def edge_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ebfb9d43343763433994bdc9efb5b6261d210e023aac3b0cb08c7df847c1f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04afd4d11750e849e18d93dc10c1763f9a47510f00971137fd19da2f1dc6c19a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876d28c681ece68514bb556b1df995ca9ad6abfd42d92c6a2d95d89a05b00308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="vappNetworksDefaultSegmentProfileTemplateId")
    def vapp_networks_default_segment_profile_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vappNetworksDefaultSegmentProfileTemplateId"))

    @vapp_networks_default_segment_profile_template_id.setter
    def vapp_networks_default_segment_profile_template_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e506ba34c79957abca575aed4c8607da33afc3ecf0161b5959a3252ea9a1d1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vappNetworksDefaultSegmentProfileTemplateId", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8effed0a63cd86be21d32cd3bada23b8bfd951e0e60ab3e94a1bdcc804b40e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)

    @builtins.property
    @jsii.member(jsii_name="vdcNetworksDefaultSegmentProfileTemplateId")
    def vdc_networks_default_segment_profile_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcNetworksDefaultSegmentProfileTemplateId"))

    @vdc_networks_default_segment_profile_template_id.setter
    def vdc_networks_default_segment_profile_template_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123746c492f07769470f6e12da3e12812f6f4355df86c72a049b6df36e2799c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdcNetworksDefaultSegmentProfileTemplateId", value)


@jsii.data_type(
    jsii_type="vcd.orgVdcNsxtNetworkProfile.OrgVdcNsxtNetworkProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "edge_cluster_id": "edgeClusterId",
        "id": "id",
        "org": "org",
        "vapp_networks_default_segment_profile_template_id": "vappNetworksDefaultSegmentProfileTemplateId",
        "vdc": "vdc",
        "vdc_networks_default_segment_profile_template_id": "vdcNetworksDefaultSegmentProfileTemplateId",
    },
)
class OrgVdcNsxtNetworkProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        edge_cluster_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        vapp_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        vdc_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param edge_cluster_id: ID of NSX-T Edge Cluster (provider vApp networking services and DHCP capability for Isolated networks). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#edge_cluster_id OrgVdcNsxtNetworkProfile#edge_cluster_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#id OrgVdcNsxtNetworkProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#org OrgVdcNsxtNetworkProfile#org}
        :param vapp_networks_default_segment_profile_template_id: Default NSX-T Segment Profile for vApp networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vapp_networks_default_segment_profile_template_id OrgVdcNsxtNetworkProfile#vapp_networks_default_segment_profile_template_id}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vdc OrgVdcNsxtNetworkProfile#vdc}
        :param vdc_networks_default_segment_profile_template_id: Default NSX-T Segment Profile for Org VDC networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vdc_networks_default_segment_profile_template_id OrgVdcNsxtNetworkProfile#vdc_networks_default_segment_profile_template_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7cc2048c876436a37e4a0a73d8d39fd45e5468a3612f10d3d6764ca3ce5eb4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_cluster_id", value=edge_cluster_id, expected_type=type_hints["edge_cluster_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument vapp_networks_default_segment_profile_template_id", value=vapp_networks_default_segment_profile_template_id, expected_type=type_hints["vapp_networks_default_segment_profile_template_id"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
            check_type(argname="argument vdc_networks_default_segment_profile_template_id", value=vdc_networks_default_segment_profile_template_id, expected_type=type_hints["vdc_networks_default_segment_profile_template_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if edge_cluster_id is not None:
            self._values["edge_cluster_id"] = edge_cluster_id
        if id is not None:
            self._values["id"] = id
        if org is not None:
            self._values["org"] = org
        if vapp_networks_default_segment_profile_template_id is not None:
            self._values["vapp_networks_default_segment_profile_template_id"] = vapp_networks_default_segment_profile_template_id
        if vdc is not None:
            self._values["vdc"] = vdc
        if vdc_networks_default_segment_profile_template_id is not None:
            self._values["vdc_networks_default_segment_profile_template_id"] = vdc_networks_default_segment_profile_template_id

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
    def edge_cluster_id(self) -> typing.Optional[builtins.str]:
        '''ID of NSX-T Edge Cluster (provider vApp networking services and DHCP capability for Isolated networks).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#edge_cluster_id OrgVdcNsxtNetworkProfile#edge_cluster_id}
        '''
        result = self._values.get("edge_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#id OrgVdcNsxtNetworkProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#org OrgVdcNsxtNetworkProfile#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vapp_networks_default_segment_profile_template_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Default NSX-T Segment Profile for vApp networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vapp_networks_default_segment_profile_template_id OrgVdcNsxtNetworkProfile#vapp_networks_default_segment_profile_template_id}
        '''
        result = self._values.get("vapp_networks_default_segment_profile_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vdc OrgVdcNsxtNetworkProfile#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc_networks_default_segment_profile_template_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Default NSX-T Segment Profile for Org VDC networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_vdc_nsxt_network_profile#vdc_networks_default_segment_profile_template_id OrgVdcNsxtNetworkProfile#vdc_networks_default_segment_profile_template_id}
        '''
        result = self._values.get("vdc_networks_default_segment_profile_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgVdcNsxtNetworkProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OrgVdcNsxtNetworkProfile",
    "OrgVdcNsxtNetworkProfileConfig",
]

publication.publish()

def _typecheckingstub__d34e42ab787b1543b2cd1db130519f7e823d766e0d825b30b31dea8517c67fbf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_cluster_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    vapp_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
    vdc_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__26dd8bd7be8552ff0bea65a05635ceaf258cced655e0d571ed2979a837752ce6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ebfb9d43343763433994bdc9efb5b6261d210e023aac3b0cb08c7df847c1f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04afd4d11750e849e18d93dc10c1763f9a47510f00971137fd19da2f1dc6c19a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876d28c681ece68514bb556b1df995ca9ad6abfd42d92c6a2d95d89a05b00308(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e506ba34c79957abca575aed4c8607da33afc3ecf0161b5959a3252ea9a1d1d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8effed0a63cd86be21d32cd3bada23b8bfd951e0e60ab3e94a1bdcc804b40e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123746c492f07769470f6e12da3e12812f6f4355df86c72a049b6df36e2799c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7cc2048c876436a37e4a0a73d8d39fd45e5468a3612f10d3d6764ca3ce5eb4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_cluster_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    vapp_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
    vdc_networks_default_segment_profile_template_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
