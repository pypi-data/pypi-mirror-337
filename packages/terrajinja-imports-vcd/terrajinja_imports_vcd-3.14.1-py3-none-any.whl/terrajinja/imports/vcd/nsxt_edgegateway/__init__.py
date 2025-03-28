'''
# `vcd_nsxt_edgegateway`

Refer to the Terraform Registry for docs: [`vcd_nsxt_edgegateway`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway).
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


class NsxtEdgegateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway vcd_nsxt_edgegateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        external_network_id: builtins.str,
        name: builtins.str,
        dedicate_external_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployment_mode: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        edge_cluster_id: typing.Optional[builtins.str] = None,
        external_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayExternalNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_count_read_limit: typing.Optional[jsii.Number] = None,
        non_distributed_routing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        owner_id: typing.Optional[builtins.str] = None,
        starting_vdc_id: typing.Optional[builtins.str] = None,
        subnet: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnet_with_ip_count: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnetWithIpCount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnet_with_total_ip_count: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnetWithTotalIpCount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        total_allocated_ip_count: typing.Optional[jsii.Number] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway vcd_nsxt_edgegateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param external_network_id: External network ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#external_network_id NsxtEdgegateway#external_network_id}
        :param name: Edge Gateway name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#name NsxtEdgegateway#name}
        :param dedicate_external_network: Dedicating the External Network will enable Route Advertisement for this Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#dedicate_external_network NsxtEdgegateway#dedicate_external_network}
        :param deployment_mode: Edge Gateway deployment mode. One of 'DISTRIBUTED_ONLY', 'ACTIVE_STANDBY'. Default 'ACTIVE_STANDBY'. VCD 10.6+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#deployment_mode NsxtEdgegateway#deployment_mode}
        :param description: Edge Gateway description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#description NsxtEdgegateway#description}
        :param edge_cluster_id: Select specific NSX-T Edge Cluster. Will be inherited from external network if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#edge_cluster_id NsxtEdgegateway#edge_cluster_id}
        :param external_network: external_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#external_network NsxtEdgegateway#external_network}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#id NsxtEdgegateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_count_read_limit: How many maximum IPs should be reported in 'used_ipcount' and 'unused_ip_count'. Default 1000000, 0 - unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#ip_count_read_limit NsxtEdgegateway#ip_count_read_limit}
        :param non_distributed_routing_enabled: A flag indicating whether non-distributed routing is enabled or not (``false`` by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#non_distributed_routing_enabled NsxtEdgegateway#non_distributed_routing_enabled}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#org NsxtEdgegateway#org}
        :param owner_id: ID of VDC or VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#owner_id NsxtEdgegateway#owner_id}
        :param starting_vdc_id: Optional ID of starting VDC if the 'owner_id' is a VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#starting_vdc_id NsxtEdgegateway#starting_vdc_id}
        :param subnet: subnet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet NsxtEdgegateway#subnet}
        :param subnet_with_ip_count: subnet_with_ip_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet_with_ip_count NsxtEdgegateway#subnet_with_ip_count}
        :param subnet_with_total_ip_count: subnet_with_total_ip_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet_with_total_ip_count NsxtEdgegateway#subnet_with_total_ip_count}
        :param total_allocated_ip_count: Total number of IP addresses allocated for this gateway from Tier0 uplink. Can be set with 'subnet_with_total_ip_count' definitions only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#total_allocated_ip_count NsxtEdgegateway#total_allocated_ip_count}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#vdc NsxtEdgegateway#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af7007c1deff40a29e2ab5795031e9059c76bfdc76078be56c6a203de69a1c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtEdgegatewayConfig(
            external_network_id=external_network_id,
            name=name,
            dedicate_external_network=dedicate_external_network,
            deployment_mode=deployment_mode,
            description=description,
            edge_cluster_id=edge_cluster_id,
            external_network=external_network,
            id=id,
            ip_count_read_limit=ip_count_read_limit,
            non_distributed_routing_enabled=non_distributed_routing_enabled,
            org=org,
            owner_id=owner_id,
            starting_vdc_id=starting_vdc_id,
            subnet=subnet,
            subnet_with_ip_count=subnet_with_ip_count,
            subnet_with_total_ip_count=subnet_with_total_ip_count,
            total_allocated_ip_count=total_allocated_ip_count,
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
        '''Generates CDKTF code for importing a NsxtEdgegateway resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtEdgegateway to import.
        :param import_from_id: The id of the existing NsxtEdgegateway that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtEdgegateway to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9982187174db93b41ef9a5f3b6bb396fc4e30dda46b09559d109693321e674e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExternalNetwork")
    def put_external_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayExternalNetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e15bafcfae00519b853c6e10f97d466fbbe3ee5245d311a05f8008e724ca99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExternalNetwork", [value]))

    @jsii.member(jsii_name="putSubnet")
    def put_subnet(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c286d07c62a9c58aeb32eec55d30df15a9322ecf0dff782f7bf1d0b62ec86c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubnet", [value]))

    @jsii.member(jsii_name="putSubnetWithIpCount")
    def put_subnet_with_ip_count(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnetWithIpCount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81276c8c6ce18992f02f25d3da08574ca6999ffc4dbda2e5195c6976c7c16535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubnetWithIpCount", [value]))

    @jsii.member(jsii_name="putSubnetWithTotalIpCount")
    def put_subnet_with_total_ip_count(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnetWithTotalIpCount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05e6f0ffb24b35e0c89c4cc980a86245e1b77bc8a7118143042113451140022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubnetWithTotalIpCount", [value]))

    @jsii.member(jsii_name="resetDedicateExternalNetwork")
    def reset_dedicate_external_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicateExternalNetwork", []))

    @jsii.member(jsii_name="resetDeploymentMode")
    def reset_deployment_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentMode", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEdgeClusterId")
    def reset_edge_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeClusterId", []))

    @jsii.member(jsii_name="resetExternalNetwork")
    def reset_external_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalNetwork", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpCountReadLimit")
    def reset_ip_count_read_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpCountReadLimit", []))

    @jsii.member(jsii_name="resetNonDistributedRoutingEnabled")
    def reset_non_distributed_routing_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonDistributedRoutingEnabled", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOwnerId")
    def reset_owner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnerId", []))

    @jsii.member(jsii_name="resetStartingVdcId")
    def reset_starting_vdc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingVdcId", []))

    @jsii.member(jsii_name="resetSubnet")
    def reset_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnet", []))

    @jsii.member(jsii_name="resetSubnetWithIpCount")
    def reset_subnet_with_ip_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetWithIpCount", []))

    @jsii.member(jsii_name="resetSubnetWithTotalIpCount")
    def reset_subnet_with_total_ip_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetWithTotalIpCount", []))

    @jsii.member(jsii_name="resetTotalAllocatedIpCount")
    def reset_total_allocated_ip_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalAllocatedIpCount", []))

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
    @jsii.member(jsii_name="externalNetwork")
    def external_network(self) -> "NsxtEdgegatewayExternalNetworkList":
        return typing.cast("NsxtEdgegatewayExternalNetworkList", jsii.get(self, "externalNetwork"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkAllocatedIpCount")
    def external_network_allocated_ip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalNetworkAllocatedIpCount"))

    @builtins.property
    @jsii.member(jsii_name="primaryIp")
    def primary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryIp"))

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> "NsxtEdgegatewaySubnetList":
        return typing.cast("NsxtEdgegatewaySubnetList", jsii.get(self, "subnet"))

    @builtins.property
    @jsii.member(jsii_name="subnetWithIpCount")
    def subnet_with_ip_count(self) -> "NsxtEdgegatewaySubnetWithIpCountList":
        return typing.cast("NsxtEdgegatewaySubnetWithIpCountList", jsii.get(self, "subnetWithIpCount"))

    @builtins.property
    @jsii.member(jsii_name="subnetWithTotalIpCount")
    def subnet_with_total_ip_count(self) -> "NsxtEdgegatewaySubnetWithTotalIpCountList":
        return typing.cast("NsxtEdgegatewaySubnetWithTotalIpCountList", jsii.get(self, "subnetWithTotalIpCount"))

    @builtins.property
    @jsii.member(jsii_name="unusedIpCount")
    def unused_ip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unusedIpCount"))

    @builtins.property
    @jsii.member(jsii_name="usedIpCount")
    def used_ip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedIpCount"))

    @builtins.property
    @jsii.member(jsii_name="useIpSpaces")
    def use_ip_spaces(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "useIpSpaces"))

    @builtins.property
    @jsii.member(jsii_name="dedicateExternalNetworkInput")
    def dedicate_external_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dedicateExternalNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentModeInput")
    def deployment_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentModeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeClusterIdInput")
    def edge_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkIdInput")
    def external_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkInput")
    def external_network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayExternalNetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayExternalNetwork"]]], jsii.get(self, "externalNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipCountReadLimitInput")
    def ip_count_read_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ipCountReadLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nonDistributedRoutingEnabledInput")
    def non_distributed_routing_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nonDistributedRoutingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerIdInput")
    def owner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="startingVdcIdInput")
    def starting_vdc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingVdcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetInput")
    def subnet_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnet"]]], jsii.get(self, "subnetInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetWithIpCountInput")
    def subnet_with_ip_count_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetWithIpCount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetWithIpCount"]]], jsii.get(self, "subnetWithIpCountInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetWithTotalIpCountInput")
    def subnet_with_total_ip_count_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetWithTotalIpCount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetWithTotalIpCount"]]], jsii.get(self, "subnetWithTotalIpCountInput"))

    @builtins.property
    @jsii.member(jsii_name="totalAllocatedIpCountInput")
    def total_allocated_ip_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "totalAllocatedIpCountInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicateExternalNetwork")
    def dedicate_external_network(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dedicateExternalNetwork"))

    @dedicate_external_network.setter
    def dedicate_external_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30df805d2264b8fb56ed2ac195725e844226d7044aa85a4904979c3fc8d96b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicateExternalNetwork", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentMode")
    def deployment_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentMode"))

    @deployment_mode.setter
    def deployment_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540209be126dbf3d89e128e459f812fbd3e9bd1f6e5d879b532e216145c0d6b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentMode", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21c7dc8e608ef21fa52d0c8a5f903bafd3244b4fdfcf8a923d30f59e02db24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edgeClusterId")
    def edge_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeClusterId"))

    @edge_cluster_id.setter
    def edge_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef76cf46b78662422841c6e6b8ead232bfb5885f08c5c936a46dde8321c3544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="externalNetworkId")
    def external_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalNetworkId"))

    @external_network_id.setter
    def external_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f52179477194db2a75d3c1e36309d16454b4638cff6506e2175d22df9f2fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5516d36e7caabb7a000a50bb4897b6762522444879bd5832e952d28aa9562f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipCountReadLimit")
    def ip_count_read_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ipCountReadLimit"))

    @ip_count_read_limit.setter
    def ip_count_read_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0cee2424b076745dc66449414afa05f0e5fe242e224c9e4c225057c5e13cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCountReadLimit", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd68705ab98871c6df15ab6eb7b40303f548ddcc6031db8de65cb77a1010da86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nonDistributedRoutingEnabled")
    def non_distributed_routing_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nonDistributedRoutingEnabled"))

    @non_distributed_routing_enabled.setter
    def non_distributed_routing_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdc323296d16deb184786be22f2e68f7f5b1d01b7afecd07ee5ad1ca6b0dfdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonDistributedRoutingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466296c679564ea14ad1f55f349a1cf7772dd34f7066be114a88a798aa1422ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="ownerId")
    def owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerId"))

    @owner_id.setter
    def owner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493e2e7469e13e61ae7c2c4793d94049b628f308f6e3ef8fb2783471f6ef2c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerId", value)

    @builtins.property
    @jsii.member(jsii_name="startingVdcId")
    def starting_vdc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingVdcId"))

    @starting_vdc_id.setter
    def starting_vdc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ba31679e3ec299ef86de34cdb5932cc7030affde6af34f7ef33a77a528c2d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingVdcId", value)

    @builtins.property
    @jsii.member(jsii_name="totalAllocatedIpCount")
    def total_allocated_ip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalAllocatedIpCount"))

    @total_allocated_ip_count.setter
    def total_allocated_ip_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623582a75652d8183546e33fd15ea89f2d7ca06e62cf9288ccb65d10bff7f28b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalAllocatedIpCount", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0485fff554a236026865969299799e71d94507d68971c2d6072c89b37747b006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewayConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "external_network_id": "externalNetworkId",
        "name": "name",
        "dedicate_external_network": "dedicateExternalNetwork",
        "deployment_mode": "deploymentMode",
        "description": "description",
        "edge_cluster_id": "edgeClusterId",
        "external_network": "externalNetwork",
        "id": "id",
        "ip_count_read_limit": "ipCountReadLimit",
        "non_distributed_routing_enabled": "nonDistributedRoutingEnabled",
        "org": "org",
        "owner_id": "ownerId",
        "starting_vdc_id": "startingVdcId",
        "subnet": "subnet",
        "subnet_with_ip_count": "subnetWithIpCount",
        "subnet_with_total_ip_count": "subnetWithTotalIpCount",
        "total_allocated_ip_count": "totalAllocatedIpCount",
        "vdc": "vdc",
    },
)
class NsxtEdgegatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        external_network_id: builtins.str,
        name: builtins.str,
        dedicate_external_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployment_mode: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        edge_cluster_id: typing.Optional[builtins.str] = None,
        external_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewayExternalNetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_count_read_limit: typing.Optional[jsii.Number] = None,
        non_distributed_routing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        owner_id: typing.Optional[builtins.str] = None,
        starting_vdc_id: typing.Optional[builtins.str] = None,
        subnet: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnet_with_ip_count: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnetWithIpCount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnet_with_total_ip_count: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnetWithTotalIpCount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        total_allocated_ip_count: typing.Optional[jsii.Number] = None,
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
        :param external_network_id: External network ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#external_network_id NsxtEdgegateway#external_network_id}
        :param name: Edge Gateway name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#name NsxtEdgegateway#name}
        :param dedicate_external_network: Dedicating the External Network will enable Route Advertisement for this Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#dedicate_external_network NsxtEdgegateway#dedicate_external_network}
        :param deployment_mode: Edge Gateway deployment mode. One of 'DISTRIBUTED_ONLY', 'ACTIVE_STANDBY'. Default 'ACTIVE_STANDBY'. VCD 10.6+. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#deployment_mode NsxtEdgegateway#deployment_mode}
        :param description: Edge Gateway description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#description NsxtEdgegateway#description}
        :param edge_cluster_id: Select specific NSX-T Edge Cluster. Will be inherited from external network if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#edge_cluster_id NsxtEdgegateway#edge_cluster_id}
        :param external_network: external_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#external_network NsxtEdgegateway#external_network}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#id NsxtEdgegateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_count_read_limit: How many maximum IPs should be reported in 'used_ipcount' and 'unused_ip_count'. Default 1000000, 0 - unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#ip_count_read_limit NsxtEdgegateway#ip_count_read_limit}
        :param non_distributed_routing_enabled: A flag indicating whether non-distributed routing is enabled or not (``false`` by default). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#non_distributed_routing_enabled NsxtEdgegateway#non_distributed_routing_enabled}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#org NsxtEdgegateway#org}
        :param owner_id: ID of VDC or VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#owner_id NsxtEdgegateway#owner_id}
        :param starting_vdc_id: Optional ID of starting VDC if the 'owner_id' is a VDC Group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#starting_vdc_id NsxtEdgegateway#starting_vdc_id}
        :param subnet: subnet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet NsxtEdgegateway#subnet}
        :param subnet_with_ip_count: subnet_with_ip_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet_with_ip_count NsxtEdgegateway#subnet_with_ip_count}
        :param subnet_with_total_ip_count: subnet_with_total_ip_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet_with_total_ip_count NsxtEdgegateway#subnet_with_total_ip_count}
        :param total_allocated_ip_count: Total number of IP addresses allocated for this gateway from Tier0 uplink. Can be set with 'subnet_with_total_ip_count' definitions only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#total_allocated_ip_count NsxtEdgegateway#total_allocated_ip_count}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#vdc NsxtEdgegateway#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5009a1f6b9e27719cbf2691823104dc436e9f8d5c747400be2cdd5169023e85)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument external_network_id", value=external_network_id, expected_type=type_hints["external_network_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dedicate_external_network", value=dedicate_external_network, expected_type=type_hints["dedicate_external_network"])
            check_type(argname="argument deployment_mode", value=deployment_mode, expected_type=type_hints["deployment_mode"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_cluster_id", value=edge_cluster_id, expected_type=type_hints["edge_cluster_id"])
            check_type(argname="argument external_network", value=external_network, expected_type=type_hints["external_network"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_count_read_limit", value=ip_count_read_limit, expected_type=type_hints["ip_count_read_limit"])
            check_type(argname="argument non_distributed_routing_enabled", value=non_distributed_routing_enabled, expected_type=type_hints["non_distributed_routing_enabled"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
            check_type(argname="argument starting_vdc_id", value=starting_vdc_id, expected_type=type_hints["starting_vdc_id"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument subnet_with_ip_count", value=subnet_with_ip_count, expected_type=type_hints["subnet_with_ip_count"])
            check_type(argname="argument subnet_with_total_ip_count", value=subnet_with_total_ip_count, expected_type=type_hints["subnet_with_total_ip_count"])
            check_type(argname="argument total_allocated_ip_count", value=total_allocated_ip_count, expected_type=type_hints["total_allocated_ip_count"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "external_network_id": external_network_id,
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
        if dedicate_external_network is not None:
            self._values["dedicate_external_network"] = dedicate_external_network
        if deployment_mode is not None:
            self._values["deployment_mode"] = deployment_mode
        if description is not None:
            self._values["description"] = description
        if edge_cluster_id is not None:
            self._values["edge_cluster_id"] = edge_cluster_id
        if external_network is not None:
            self._values["external_network"] = external_network
        if id is not None:
            self._values["id"] = id
        if ip_count_read_limit is not None:
            self._values["ip_count_read_limit"] = ip_count_read_limit
        if non_distributed_routing_enabled is not None:
            self._values["non_distributed_routing_enabled"] = non_distributed_routing_enabled
        if org is not None:
            self._values["org"] = org
        if owner_id is not None:
            self._values["owner_id"] = owner_id
        if starting_vdc_id is not None:
            self._values["starting_vdc_id"] = starting_vdc_id
        if subnet is not None:
            self._values["subnet"] = subnet
        if subnet_with_ip_count is not None:
            self._values["subnet_with_ip_count"] = subnet_with_ip_count
        if subnet_with_total_ip_count is not None:
            self._values["subnet_with_total_ip_count"] = subnet_with_total_ip_count
        if total_allocated_ip_count is not None:
            self._values["total_allocated_ip_count"] = total_allocated_ip_count
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
    def external_network_id(self) -> builtins.str:
        '''External network ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#external_network_id NsxtEdgegateway#external_network_id}
        '''
        result = self._values.get("external_network_id")
        assert result is not None, "Required property 'external_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Edge Gateway name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#name NsxtEdgegateway#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dedicate_external_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Dedicating the External Network will enable Route Advertisement for this Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#dedicate_external_network NsxtEdgegateway#dedicate_external_network}
        '''
        result = self._values.get("dedicate_external_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deployment_mode(self) -> typing.Optional[builtins.str]:
        '''Edge Gateway deployment mode. One of 'DISTRIBUTED_ONLY', 'ACTIVE_STANDBY'. Default 'ACTIVE_STANDBY'. VCD 10.6+.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#deployment_mode NsxtEdgegateway#deployment_mode}
        '''
        result = self._values.get("deployment_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Edge Gateway description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#description NsxtEdgegateway#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_cluster_id(self) -> typing.Optional[builtins.str]:
        '''Select specific NSX-T Edge Cluster. Will be inherited from external network if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#edge_cluster_id NsxtEdgegateway#edge_cluster_id}
        '''
        result = self._values.get("edge_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_network(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayExternalNetwork"]]]:
        '''external_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#external_network NsxtEdgegateway#external_network}
        '''
        result = self._values.get("external_network")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewayExternalNetwork"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#id NsxtEdgegateway#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_count_read_limit(self) -> typing.Optional[jsii.Number]:
        '''How many maximum IPs should be reported in 'used_ipcount' and 'unused_ip_count'. Default 1000000, 0 - unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#ip_count_read_limit NsxtEdgegateway#ip_count_read_limit}
        '''
        result = self._values.get("ip_count_read_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def non_distributed_routing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag indicating whether non-distributed routing is enabled or not (``false`` by default).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#non_distributed_routing_enabled NsxtEdgegateway#non_distributed_routing_enabled}
        '''
        result = self._values.get("non_distributed_routing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#org NsxtEdgegateway#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_id(self) -> typing.Optional[builtins.str]:
        '''ID of VDC or VDC Group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#owner_id NsxtEdgegateway#owner_id}
        '''
        result = self._values.get("owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starting_vdc_id(self) -> typing.Optional[builtins.str]:
        '''Optional ID of starting VDC if the 'owner_id' is a VDC Group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#starting_vdc_id NsxtEdgegateway#starting_vdc_id}
        '''
        result = self._values.get("starting_vdc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnet"]]]:
        '''subnet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet NsxtEdgegateway#subnet}
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnet"]]], result)

    @builtins.property
    def subnet_with_ip_count(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetWithIpCount"]]]:
        '''subnet_with_ip_count block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet_with_ip_count NsxtEdgegateway#subnet_with_ip_count}
        '''
        result = self._values.get("subnet_with_ip_count")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetWithIpCount"]]], result)

    @builtins.property
    def subnet_with_total_ip_count(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetWithTotalIpCount"]]]:
        '''subnet_with_total_ip_count block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#subnet_with_total_ip_count NsxtEdgegateway#subnet_with_total_ip_count}
        '''
        result = self._values.get("subnet_with_total_ip_count")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetWithTotalIpCount"]]], result)

    @builtins.property
    def total_allocated_ip_count(self) -> typing.Optional[jsii.Number]:
        '''Total number of IP addresses allocated for this gateway from Tier0 uplink. Can be set with 'subnet_with_total_ip_count' definitions only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#total_allocated_ip_count NsxtEdgegateway#total_allocated_ip_count}
        '''
        result = self._values.get("total_allocated_ip_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#vdc NsxtEdgegateway#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewayExternalNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_ip_count": "allocatedIpCount",
        "external_network_id": "externalNetworkId",
        "gateway": "gateway",
        "prefix_length": "prefixLength",
        "primary_ip": "primaryIp",
    },
)
class NsxtEdgegatewayExternalNetwork:
    def __init__(
        self,
        *,
        allocated_ip_count: jsii.Number,
        external_network_id: builtins.str,
        gateway: builtins.str,
        prefix_length: jsii.Number,
        primary_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_count: Number of allocated IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#allocated_ip_count NsxtEdgegateway#allocated_ip_count}
        :param external_network_id: NSX-T Segment backed External Network ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#external_network_id NsxtEdgegateway#external_network_id}
        :param gateway: Gateway IP Address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#gateway NsxtEdgegateway#gateway}
        :param prefix_length: Prefix length for a subnet (e.g. 24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#prefix_length NsxtEdgegateway#prefix_length}
        :param primary_ip: Primary IP address for the Edge Gateway - will be auto-assigned if not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#primary_ip NsxtEdgegateway#primary_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797ff0d8a166b95bb5ade4b7af6a4f0206e64434cc09c372d3ec0ba621448850)
            check_type(argname="argument allocated_ip_count", value=allocated_ip_count, expected_type=type_hints["allocated_ip_count"])
            check_type(argname="argument external_network_id", value=external_network_id, expected_type=type_hints["external_network_id"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
            check_type(argname="argument primary_ip", value=primary_ip, expected_type=type_hints["primary_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocated_ip_count": allocated_ip_count,
            "external_network_id": external_network_id,
            "gateway": gateway,
            "prefix_length": prefix_length,
        }
        if primary_ip is not None:
            self._values["primary_ip"] = primary_ip

    @builtins.property
    def allocated_ip_count(self) -> jsii.Number:
        '''Number of allocated IPs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#allocated_ip_count NsxtEdgegateway#allocated_ip_count}
        '''
        result = self._values.get("allocated_ip_count")
        assert result is not None, "Required property 'allocated_ip_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def external_network_id(self) -> builtins.str:
        '''NSX-T Segment backed External Network ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#external_network_id NsxtEdgegateway#external_network_id}
        '''
        result = self._values.get("external_network_id")
        assert result is not None, "Required property 'external_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway(self) -> builtins.str:
        '''Gateway IP Address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#gateway NsxtEdgegateway#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_length(self) -> jsii.Number:
        '''Prefix length for a subnet (e.g. 24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#prefix_length NsxtEdgegateway#prefix_length}
        '''
        result = self._values.get("prefix_length")
        assert result is not None, "Required property 'prefix_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def primary_ip(self) -> typing.Optional[builtins.str]:
        '''Primary IP address for the Edge Gateway - will be auto-assigned if not defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#primary_ip NsxtEdgegateway#primary_ip}
        '''
        result = self._values.get("primary_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewayExternalNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtEdgegatewayExternalNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewayExternalNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a58765204cb2ee004946b13de5a889669a5138421610b553ec5db9732a9fac4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtEdgegatewayExternalNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7d09454ab528dea6c5cf5cdde2c8bb726eb7cc3ec708d5b9fb7b2ed754038d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtEdgegatewayExternalNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6ef08e73c8bf296da1fa776a57568fa8c4ca7b9d53090433afbd212ce7c319)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f361a19d715be5f529b35793d0f2672ba8fc9df30c42cd638b32b6457c8a210)
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
            type_hints = typing.get_type_hints(_typecheckingstub__052bdbabc6d59275dd0f912d594d68349b99c998a7edfa5d66a419c852caa895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayExternalNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayExternalNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayExternalNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec86e971216dbb41aeae39a192c6103bbf13587f23cdd0a85bca31be5d3c827f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewayExternalNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewayExternalNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b22f737a7d70f00251a7f32375170c9ae5ad8e2831c4aaa40bb59a822b555958)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPrimaryIp")
    def reset_primary_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryIp", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpCountInput")
    def allocated_ip_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocatedIpCountInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkIdInput")
    def external_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryIpInput")
    def primary_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryIpInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpCount")
    def allocated_ip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocatedIpCount"))

    @allocated_ip_count.setter
    def allocated_ip_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fbfb0ccd7257013b6335d1035760d55731c0f5d0213f04e66fcf6dd54a9cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedIpCount", value)

    @builtins.property
    @jsii.member(jsii_name="externalNetworkId")
    def external_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalNetworkId"))

    @external_network_id.setter
    def external_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c3d73179361db23dc17fcf92790a38dc8325360c89d1edd7d165831906d356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27fc4240e39f6e71c2ff32769eb3a6454a5ea2743a39a2c713c82dee337730b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00800cd08dc394fce7e2014aa1d85f762d6f937cee93605f0a214f42dc1274c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="primaryIp")
    def primary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryIp"))

    @primary_ip.setter
    def primary_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368a8dc161381088e8dcd76103b8200e7738dd08b54561c6fcf52f0f4d0a1304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryIp", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayExternalNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayExternalNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayExternalNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba6f6199ed7be4ffaedd19528fc20cfc287fdb8cece0e589380b0b13218f5fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnet",
    jsii_struct_bases=[],
    name_mapping={
        "gateway": "gateway",
        "prefix_length": "prefixLength",
        "allocated_ips": "allocatedIps",
        "primary_ip": "primaryIp",
    },
)
class NsxtEdgegatewaySubnet:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        prefix_length: jsii.Number,
        allocated_ips: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtEdgegatewaySubnetAllocatedIps", typing.Dict[builtins.str, typing.Any]]]]] = None,
        primary_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway: Gateway address for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#gateway NsxtEdgegateway#gateway}
        :param prefix_length: Prefix length for a subnet (e.g. 24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#prefix_length NsxtEdgegateway#prefix_length}
        :param allocated_ips: allocated_ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#allocated_ips NsxtEdgegateway#allocated_ips}
        :param primary_ip: Primary IP address for the edge gateway - will be auto-assigned if not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#primary_ip NsxtEdgegateway#primary_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3636eeb86114634685c502e73e34777dedea6702fb5bbcddbbf35ebc1600792d)
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
            check_type(argname="argument allocated_ips", value=allocated_ips, expected_type=type_hints["allocated_ips"])
            check_type(argname="argument primary_ip", value=primary_ip, expected_type=type_hints["primary_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway": gateway,
            "prefix_length": prefix_length,
        }
        if allocated_ips is not None:
            self._values["allocated_ips"] = allocated_ips
        if primary_ip is not None:
            self._values["primary_ip"] = primary_ip

    @builtins.property
    def gateway(self) -> builtins.str:
        '''Gateway address for a subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#gateway NsxtEdgegateway#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_length(self) -> jsii.Number:
        '''Prefix length for a subnet (e.g. 24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#prefix_length NsxtEdgegateway#prefix_length}
        '''
        result = self._values.get("prefix_length")
        assert result is not None, "Required property 'prefix_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def allocated_ips(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetAllocatedIps"]]]:
        '''allocated_ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#allocated_ips NsxtEdgegateway#allocated_ips}
        '''
        result = self._values.get("allocated_ips")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtEdgegatewaySubnetAllocatedIps"]]], result)

    @builtins.property
    def primary_ip(self) -> typing.Optional[builtins.str]:
        '''Primary IP address for the edge gateway - will be auto-assigned if not defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#primary_ip NsxtEdgegateway#primary_ip}
        '''
        result = self._values.get("primary_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewaySubnet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetAllocatedIps",
    jsii_struct_bases=[],
    name_mapping={"end_address": "endAddress", "start_address": "startAddress"},
)
class NsxtEdgegatewaySubnetAllocatedIps:
    def __init__(
        self,
        *,
        end_address: builtins.str,
        start_address: builtins.str,
    ) -> None:
        '''
        :param end_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#end_address NsxtEdgegateway#end_address}.
        :param start_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#start_address NsxtEdgegateway#start_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ed952c3b0792276cba0b493279df9b867441f181fcaab42576539fdaa53d3b)
            check_type(argname="argument end_address", value=end_address, expected_type=type_hints["end_address"])
            check_type(argname="argument start_address", value=start_address, expected_type=type_hints["start_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_address": end_address,
            "start_address": start_address,
        }

    @builtins.property
    def end_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#end_address NsxtEdgegateway#end_address}.'''
        result = self._values.get("end_address")
        assert result is not None, "Required property 'end_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#start_address NsxtEdgegateway#start_address}.'''
        result = self._values.get("start_address")
        assert result is not None, "Required property 'start_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewaySubnetAllocatedIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtEdgegatewaySubnetAllocatedIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetAllocatedIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3aec765c8c6022e13e7911ab56516b3e857095e168b7f612d36c3250722829c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtEdgegatewaySubnetAllocatedIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa1ff1806f7106b629bc2d91a1392a5dd169ba0edd7645055787b95bb3d9aa3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtEdgegatewaySubnetAllocatedIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1e8cfe3c1625814974cb2195a05d27a4db374f9f16cd8593cd6db27dbc95eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd4d869625824556addc8396ea1420e4d1505e48ac54a1ebf9bad41ebbb2eb6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72b5c57083cb1944de30e9d59e5bd0adba11f35a6ac3d9bc6b50891b03e87729)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetAllocatedIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetAllocatedIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetAllocatedIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a05832ec5f4dc094a240da1a0797d02bc582080a13d9b3c4fbd3497e76cf12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewaySubnetAllocatedIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetAllocatedIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de86ae4b2366fd6770628f3a6b12cc026656fcc8549095981920924c40e20554)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__243432b3bf25d298ed03325f58cdc61773b73cfd9077a556cfb611002404461e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endAddress", value)

    @builtins.property
    @jsii.member(jsii_name="startAddress")
    def start_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAddress"))

    @start_address.setter
    def start_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded5f8554e536a5936e0abfcc479cd100aed42e7ebb996efb0ec1dd789b28461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetAllocatedIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetAllocatedIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetAllocatedIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a65addfc6a2ce82892dbd16e9e82c6bc0c7ace1ca59bc3f3000e3d9010466ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewaySubnetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd184c0cff1784809afcc9bd3902a207a5aab215bdab22d7c68573429c4eac3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NsxtEdgegatewaySubnetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04006d98e13c2bd541946c4615e464881e0c6da6557027d380ecec0a5ce63333)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtEdgegatewaySubnetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b999f1aec0e0428503745d20bad613cfb44b71305e4a2d28e0632178117304)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4da4c36120f9607c904b306137dc9cf351785a1b24ac38f897187e20db0c50ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__667a6a9319b1fec1a0c8fbfa33f11012416e44dbfe5fefe7affbeeb755af7157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134f4355acfd26ae6e2714336f9f0f351f45b1e20d622c151085c4d993b3b8d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewaySubnetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b540bdfdf689401749fd195a04bcbe3aa71b8e7d90b63a04ed8886c4596dd4e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAllocatedIps")
    def put_allocated_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetAllocatedIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac7963fc57c0dbf98860229f9b831f4e0e0fc54c30854c8485b46d1e4a85bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllocatedIps", [value]))

    @jsii.member(jsii_name="resetAllocatedIps")
    def reset_allocated_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedIps", []))

    @jsii.member(jsii_name="resetPrimaryIp")
    def reset_primary_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryIp", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedIps")
    def allocated_ips(self) -> NsxtEdgegatewaySubnetAllocatedIpsList:
        return typing.cast(NsxtEdgegatewaySubnetAllocatedIpsList, jsii.get(self, "allocatedIps"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpsInput")
    def allocated_ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetAllocatedIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetAllocatedIps]]], jsii.get(self, "allocatedIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryIpInput")
    def primary_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryIpInput"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8ca732652a6e4693293f226fe69df3d19b5766f070c5749a793bcda6e20f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24185e15eb7681c7d3a43c4d65e12c332721404102c21f7b76d205fec6a2e2f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="primaryIp")
    def primary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryIp"))

    @primary_ip.setter
    def primary_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e33703c7ad6670236b4c64d7db0575867cad3452b3b2dd7854f2000bd6db84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryIp", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8691ea84c38689a47f9e03b8636c60a1e918391e83ad1f492a4775b6aaea21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetWithIpCount",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_ip_count": "allocatedIpCount",
        "gateway": "gateway",
        "prefix_length": "prefixLength",
        "primary_ip": "primaryIp",
    },
)
class NsxtEdgegatewaySubnetWithIpCount:
    def __init__(
        self,
        *,
        allocated_ip_count: jsii.Number,
        gateway: builtins.str,
        prefix_length: jsii.Number,
        primary_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_count: Number of IP addresses to allocate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#allocated_ip_count NsxtEdgegateway#allocated_ip_count}
        :param gateway: Gateway address for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#gateway NsxtEdgegateway#gateway}
        :param prefix_length: Prefix length for a subnet (e.g. 24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#prefix_length NsxtEdgegateway#prefix_length}
        :param primary_ip: Primary IP address for the edge gateway - will be auto-assigned if not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#primary_ip NsxtEdgegateway#primary_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf22f6ec0e72c9f3696867c5e0029b0f1e57ba993e268eaee400febd99013273)
            check_type(argname="argument allocated_ip_count", value=allocated_ip_count, expected_type=type_hints["allocated_ip_count"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
            check_type(argname="argument primary_ip", value=primary_ip, expected_type=type_hints["primary_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocated_ip_count": allocated_ip_count,
            "gateway": gateway,
            "prefix_length": prefix_length,
        }
        if primary_ip is not None:
            self._values["primary_ip"] = primary_ip

    @builtins.property
    def allocated_ip_count(self) -> jsii.Number:
        '''Number of IP addresses to allocate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#allocated_ip_count NsxtEdgegateway#allocated_ip_count}
        '''
        result = self._values.get("allocated_ip_count")
        assert result is not None, "Required property 'allocated_ip_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def gateway(self) -> builtins.str:
        '''Gateway address for a subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#gateway NsxtEdgegateway#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_length(self) -> jsii.Number:
        '''Prefix length for a subnet (e.g. 24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#prefix_length NsxtEdgegateway#prefix_length}
        '''
        result = self._values.get("prefix_length")
        assert result is not None, "Required property 'prefix_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def primary_ip(self) -> typing.Optional[builtins.str]:
        '''Primary IP address for the edge gateway - will be auto-assigned if not defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#primary_ip NsxtEdgegateway#primary_ip}
        '''
        result = self._values.get("primary_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewaySubnetWithIpCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtEdgegatewaySubnetWithIpCountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetWithIpCountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2194fe31ea4af94a28451b5ec68943661f1fc69d08a0c757760d689460a3cd41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtEdgegatewaySubnetWithIpCountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f238188db88f869eadefb015b34d3b41f888ad65a8fef802352a7f53c4bfb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtEdgegatewaySubnetWithIpCountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5de986e3346772204222f7e4a800cbd48f5c2273894b5e0e33d4fe111bd0c6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44891c218e1e22dda361b06f0a8839f425bb228351349f442b954490da991800)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d396561862717e96fc466ba7e2dec850f7d454321e8dbd48a08d78418a24b677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetWithIpCount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetWithIpCount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetWithIpCount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4ba2f225cc39ca90c8b8eec3446f06ec07a1c005e597651a2439e75063e6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewaySubnetWithIpCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetWithIpCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__519cd864fe54071b711a9cfd04c25522c616c7e4a55fd40367585f2c2d5119b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPrimaryIp")
    def reset_primary_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryIp", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpCountInput")
    def allocated_ip_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocatedIpCountInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryIpInput")
    def primary_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryIpInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpCount")
    def allocated_ip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocatedIpCount"))

    @allocated_ip_count.setter
    def allocated_ip_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5cfe1604aab958f0c775a1e2cfeb0840ef076f05d25aaf640ad4a3b2c51999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedIpCount", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df1e26356eeb0ec2f75caed2b3038aa798a71d4551d1c1e9a682a7910f29136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1311ca73b74d54c486bbb67e0f8ad26e7a1c2fe299a0fd1642692d40bbae54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="primaryIp")
    def primary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryIp"))

    @primary_ip.setter
    def primary_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c6007e6a415ce8060d1e8a0e7c7a774dcf03b6d28f04c3963c8a84bb9d8826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryIp", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetWithIpCount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetWithIpCount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetWithIpCount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbd458ac13f4534c19d922cb58f255bf5d3328b24ad736b4e837e6c5aadf681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetWithTotalIpCount",
    jsii_struct_bases=[],
    name_mapping={
        "gateway": "gateway",
        "prefix_length": "prefixLength",
        "primary_ip": "primaryIp",
    },
)
class NsxtEdgegatewaySubnetWithTotalIpCount:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        prefix_length: jsii.Number,
        primary_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway: Gateway address for a subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#gateway NsxtEdgegateway#gateway}
        :param prefix_length: Prefix length for a subnet (e.g. 24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#prefix_length NsxtEdgegateway#prefix_length}
        :param primary_ip: Primary IP address for the edge gateway - will be auto-assigned if not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#primary_ip NsxtEdgegateway#primary_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363d988eea5d09c0c5a5ff367403cd92fd7e3ff249ef30cd45255293dc4c5b51)
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument prefix_length", value=prefix_length, expected_type=type_hints["prefix_length"])
            check_type(argname="argument primary_ip", value=primary_ip, expected_type=type_hints["primary_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway": gateway,
            "prefix_length": prefix_length,
        }
        if primary_ip is not None:
            self._values["primary_ip"] = primary_ip

    @builtins.property
    def gateway(self) -> builtins.str:
        '''Gateway address for a subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#gateway NsxtEdgegateway#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_length(self) -> jsii.Number:
        '''Prefix length for a subnet (e.g. 24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#prefix_length NsxtEdgegateway#prefix_length}
        '''
        result = self._values.get("prefix_length")
        assert result is not None, "Required property 'prefix_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def primary_ip(self) -> typing.Optional[builtins.str]:
        '''Primary IP address for the edge gateway - will be auto-assigned if not defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_edgegateway#primary_ip NsxtEdgegateway#primary_ip}
        '''
        result = self._values.get("primary_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtEdgegatewaySubnetWithTotalIpCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtEdgegatewaySubnetWithTotalIpCountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetWithTotalIpCountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c4422e498fd88f63e48ac26d5a48d3ce611d3bf834e223234eba9c958804f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtEdgegatewaySubnetWithTotalIpCountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2982bc166907dd4e3559f656468117824471f346658134a284680f003604f65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtEdgegatewaySubnetWithTotalIpCountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3117b495401b2ef6e94b9e4c922d721a6ebd32be2a3f15161f25b4c1b3e8bb49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8212d5294242e64a6173bd514712e3f81c044231b7e5222a18c21e247566b0c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13c0245058debbdec3c7ce8c3486fb05dd188992a60d2bec27477b816bb3e1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetWithTotalIpCount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetWithTotalIpCount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetWithTotalIpCount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ec8f63eb5c3328e7ab93f9e8d95081b1c21d6d7d4a443d53e94a904dcc87d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtEdgegatewaySubnetWithTotalIpCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtEdgegateway.NsxtEdgegatewaySubnetWithTotalIpCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__def13f017a1eba9a75d4337bc3642967995dfa9c7c94adcdda6285f6c19c3a28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPrimaryIp")
    def reset_primary_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryIp", []))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixLengthInput")
    def prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "prefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryIpInput")
    def primary_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryIpInput"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a6dd47c310955ae96b47c5c6887f567d4547caedf828cb24f7e95380620aa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="prefixLength")
    def prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "prefixLength"))

    @prefix_length.setter
    def prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d269c4c41025939f76c53912aa364969eaa6c3930fbe5955e2a4a99cf2ab818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="primaryIp")
    def primary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryIp"))

    @primary_ip.setter
    def primary_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83fcf9941d8f8ba846f2bf44a0c8900a0fccaa8dd1e916c6394cd1c0cb4f950c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryIp", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetWithTotalIpCount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetWithTotalIpCount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetWithTotalIpCount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f6443a6b72b0832e4929892138ea9c56f24fae664145d4a451ed98f63b977f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtEdgegateway",
    "NsxtEdgegatewayConfig",
    "NsxtEdgegatewayExternalNetwork",
    "NsxtEdgegatewayExternalNetworkList",
    "NsxtEdgegatewayExternalNetworkOutputReference",
    "NsxtEdgegatewaySubnet",
    "NsxtEdgegatewaySubnetAllocatedIps",
    "NsxtEdgegatewaySubnetAllocatedIpsList",
    "NsxtEdgegatewaySubnetAllocatedIpsOutputReference",
    "NsxtEdgegatewaySubnetList",
    "NsxtEdgegatewaySubnetOutputReference",
    "NsxtEdgegatewaySubnetWithIpCount",
    "NsxtEdgegatewaySubnetWithIpCountList",
    "NsxtEdgegatewaySubnetWithIpCountOutputReference",
    "NsxtEdgegatewaySubnetWithTotalIpCount",
    "NsxtEdgegatewaySubnetWithTotalIpCountList",
    "NsxtEdgegatewaySubnetWithTotalIpCountOutputReference",
]

publication.publish()

def _typecheckingstub__1af7007c1deff40a29e2ab5795031e9059c76bfdc76078be56c6a203de69a1c6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    external_network_id: builtins.str,
    name: builtins.str,
    dedicate_external_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployment_mode: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    edge_cluster_id: typing.Optional[builtins.str] = None,
    external_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayExternalNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_count_read_limit: typing.Optional[jsii.Number] = None,
    non_distributed_routing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    owner_id: typing.Optional[builtins.str] = None,
    starting_vdc_id: typing.Optional[builtins.str] = None,
    subnet: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subnet_with_ip_count: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetWithIpCount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subnet_with_total_ip_count: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetWithTotalIpCount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    total_allocated_ip_count: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__f9982187174db93b41ef9a5f3b6bb396fc4e30dda46b09559d109693321e674e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e15bafcfae00519b853c6e10f97d466fbbe3ee5245d311a05f8008e724ca99(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayExternalNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c286d07c62a9c58aeb32eec55d30df15a9322ecf0dff782f7bf1d0b62ec86c8c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81276c8c6ce18992f02f25d3da08574ca6999ffc4dbda2e5195c6976c7c16535(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetWithIpCount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05e6f0ffb24b35e0c89c4cc980a86245e1b77bc8a7118143042113451140022(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetWithTotalIpCount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30df805d2264b8fb56ed2ac195725e844226d7044aa85a4904979c3fc8d96b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540209be126dbf3d89e128e459f812fbd3e9bd1f6e5d879b532e216145c0d6b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21c7dc8e608ef21fa52d0c8a5f903bafd3244b4fdfcf8a923d30f59e02db24f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef76cf46b78662422841c6e6b8ead232bfb5885f08c5c936a46dde8321c3544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f52179477194db2a75d3c1e36309d16454b4638cff6506e2175d22df9f2fec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5516d36e7caabb7a000a50bb4897b6762522444879bd5832e952d28aa9562f2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0cee2424b076745dc66449414afa05f0e5fe242e224c9e4c225057c5e13cdb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd68705ab98871c6df15ab6eb7b40303f548ddcc6031db8de65cb77a1010da86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdc323296d16deb184786be22f2e68f7f5b1d01b7afecd07ee5ad1ca6b0dfdc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466296c679564ea14ad1f55f349a1cf7772dd34f7066be114a88a798aa1422ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493e2e7469e13e61ae7c2c4793d94049b628f308f6e3ef8fb2783471f6ef2c9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ba31679e3ec299ef86de34cdb5932cc7030affde6af34f7ef33a77a528c2d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623582a75652d8183546e33fd15ea89f2d7ca06e62cf9288ccb65d10bff7f28b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0485fff554a236026865969299799e71d94507d68971c2d6072c89b37747b006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5009a1f6b9e27719cbf2691823104dc436e9f8d5c747400be2cdd5169023e85(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    external_network_id: builtins.str,
    name: builtins.str,
    dedicate_external_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployment_mode: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    edge_cluster_id: typing.Optional[builtins.str] = None,
    external_network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewayExternalNetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_count_read_limit: typing.Optional[jsii.Number] = None,
    non_distributed_routing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    owner_id: typing.Optional[builtins.str] = None,
    starting_vdc_id: typing.Optional[builtins.str] = None,
    subnet: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subnet_with_ip_count: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetWithIpCount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subnet_with_total_ip_count: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetWithTotalIpCount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    total_allocated_ip_count: typing.Optional[jsii.Number] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797ff0d8a166b95bb5ade4b7af6a4f0206e64434cc09c372d3ec0ba621448850(
    *,
    allocated_ip_count: jsii.Number,
    external_network_id: builtins.str,
    gateway: builtins.str,
    prefix_length: jsii.Number,
    primary_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58765204cb2ee004946b13de5a889669a5138421610b553ec5db9732a9fac4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7d09454ab528dea6c5cf5cdde2c8bb726eb7cc3ec708d5b9fb7b2ed754038d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6ef08e73c8bf296da1fa776a57568fa8c4ca7b9d53090433afbd212ce7c319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f361a19d715be5f529b35793d0f2672ba8fc9df30c42cd638b32b6457c8a210(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052bdbabc6d59275dd0f912d594d68349b99c998a7edfa5d66a419c852caa895(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec86e971216dbb41aeae39a192c6103bbf13587f23cdd0a85bca31be5d3c827f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewayExternalNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22f737a7d70f00251a7f32375170c9ae5ad8e2831c4aaa40bb59a822b555958(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fbfb0ccd7257013b6335d1035760d55731c0f5d0213f04e66fcf6dd54a9cbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c3d73179361db23dc17fcf92790a38dc8325360c89d1edd7d165831906d356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fc4240e39f6e71c2ff32769eb3a6454a5ea2743a39a2c713c82dee337730b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00800cd08dc394fce7e2014aa1d85f762d6f937cee93605f0a214f42dc1274c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368a8dc161381088e8dcd76103b8200e7738dd08b54561c6fcf52f0f4d0a1304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba6f6199ed7be4ffaedd19528fc20cfc287fdb8cece0e589380b0b13218f5fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewayExternalNetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3636eeb86114634685c502e73e34777dedea6702fb5bbcddbbf35ebc1600792d(
    *,
    gateway: builtins.str,
    prefix_length: jsii.Number,
    allocated_ips: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetAllocatedIps, typing.Dict[builtins.str, typing.Any]]]]] = None,
    primary_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ed952c3b0792276cba0b493279df9b867441f181fcaab42576539fdaa53d3b(
    *,
    end_address: builtins.str,
    start_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3aec765c8c6022e13e7911ab56516b3e857095e168b7f612d36c3250722829c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa1ff1806f7106b629bc2d91a1392a5dd169ba0edd7645055787b95bb3d9aa3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1e8cfe3c1625814974cb2195a05d27a4db374f9f16cd8593cd6db27dbc95eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4d869625824556addc8396ea1420e4d1505e48ac54a1ebf9bad41ebbb2eb6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b5c57083cb1944de30e9d59e5bd0adba11f35a6ac3d9bc6b50891b03e87729(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a05832ec5f4dc094a240da1a0797d02bc582080a13d9b3c4fbd3497e76cf12d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetAllocatedIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de86ae4b2366fd6770628f3a6b12cc026656fcc8549095981920924c40e20554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243432b3bf25d298ed03325f58cdc61773b73cfd9077a556cfb611002404461e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded5f8554e536a5936e0abfcc479cd100aed42e7ebb996efb0ec1dd789b28461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a65addfc6a2ce82892dbd16e9e82c6bc0c7ace1ca59bc3f3000e3d9010466ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetAllocatedIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd184c0cff1784809afcc9bd3902a207a5aab215bdab22d7c68573429c4eac3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04006d98e13c2bd541946c4615e464881e0c6da6557027d380ecec0a5ce63333(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b999f1aec0e0428503745d20bad613cfb44b71305e4a2d28e0632178117304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da4c36120f9607c904b306137dc9cf351785a1b24ac38f897187e20db0c50ce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667a6a9319b1fec1a0c8fbfa33f11012416e44dbfe5fefe7affbeeb755af7157(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134f4355acfd26ae6e2714336f9f0f351f45b1e20d622c151085c4d993b3b8d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b540bdfdf689401749fd195a04bcbe3aa71b8e7d90b63a04ed8886c4596dd4e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac7963fc57c0dbf98860229f9b831f4e0e0fc54c30854c8485b46d1e4a85bcb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtEdgegatewaySubnetAllocatedIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8ca732652a6e4693293f226fe69df3d19b5766f070c5749a793bcda6e20f9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24185e15eb7681c7d3a43c4d65e12c332721404102c21f7b76d205fec6a2e2f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e33703c7ad6670236b4c64d7db0575867cad3452b3b2dd7854f2000bd6db84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8691ea84c38689a47f9e03b8636c60a1e918391e83ad1f492a4775b6aaea21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf22f6ec0e72c9f3696867c5e0029b0f1e57ba993e268eaee400febd99013273(
    *,
    allocated_ip_count: jsii.Number,
    gateway: builtins.str,
    prefix_length: jsii.Number,
    primary_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2194fe31ea4af94a28451b5ec68943661f1fc69d08a0c757760d689460a3cd41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f238188db88f869eadefb015b34d3b41f888ad65a8fef802352a7f53c4bfb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5de986e3346772204222f7e4a800cbd48f5c2273894b5e0e33d4fe111bd0c6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44891c218e1e22dda361b06f0a8839f425bb228351349f442b954490da991800(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d396561862717e96fc466ba7e2dec850f7d454321e8dbd48a08d78418a24b677(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4ba2f225cc39ca90c8b8eec3446f06ec07a1c005e597651a2439e75063e6cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetWithIpCount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519cd864fe54071b711a9cfd04c25522c616c7e4a55fd40367585f2c2d5119b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5cfe1604aab958f0c775a1e2cfeb0840ef076f05d25aaf640ad4a3b2c51999(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df1e26356eeb0ec2f75caed2b3038aa798a71d4551d1c1e9a682a7910f29136(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1311ca73b74d54c486bbb67e0f8ad26e7a1c2fe299a0fd1642692d40bbae54(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c6007e6a415ce8060d1e8a0e7c7a774dcf03b6d28f04c3963c8a84bb9d8826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbd458ac13f4534c19d922cb58f255bf5d3328b24ad736b4e837e6c5aadf681(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetWithIpCount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363d988eea5d09c0c5a5ff367403cd92fd7e3ff249ef30cd45255293dc4c5b51(
    *,
    gateway: builtins.str,
    prefix_length: jsii.Number,
    primary_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c4422e498fd88f63e48ac26d5a48d3ce611d3bf834e223234eba9c958804f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2982bc166907dd4e3559f656468117824471f346658134a284680f003604f65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3117b495401b2ef6e94b9e4c922d721a6ebd32be2a3f15161f25b4c1b3e8bb49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8212d5294242e64a6173bd514712e3f81c044231b7e5222a18c21e247566b0c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c0245058debbdec3c7ce8c3486fb05dd188992a60d2bec27477b816bb3e1f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ec8f63eb5c3328e7ab93f9e8d95081b1c21d6d7d4a443d53e94a904dcc87d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtEdgegatewaySubnetWithTotalIpCount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def13f017a1eba9a75d4337bc3642967995dfa9c7c94adcdda6285f6c19c3a28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a6dd47c310955ae96b47c5c6887f567d4547caedf828cb24f7e95380620aa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d269c4c41025939f76c53912aa364969eaa6c3930fbe5955e2a4a99cf2ab818(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83fcf9941d8f8ba846f2bf44a0c8900a0fccaa8dd1e916c6394cd1c0cb4f950c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f6443a6b72b0832e4929892138ea9c56f24fae664145d4a451ed98f63b977f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtEdgegatewaySubnetWithTotalIpCount]],
) -> None:
    """Type checking stubs"""
    pass
