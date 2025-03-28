'''
# `vcd_network_pool`

Refer to the Terraform Registry for docs: [`vcd_network_pool`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool).
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


class NetworkPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkPool.NetworkPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool vcd_network_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network_provider_id: builtins.str,
        type: builtins.str,
        backing: typing.Optional[typing.Union["NetworkPoolBacking", typing.Dict[builtins.str, typing.Any]]] = None,
        backing_selection_constraint: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool vcd_network_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of network pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        :param network_provider_id: Id of the network provider (either vCenter or NSX-T manager). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#network_provider_id NetworkPool#network_provider_id}
        :param type: Type of the network pool (one of ``GENEVE``, ``VLAN``, ``PORTGROUP_BACKED``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#type NetworkPool#type}
        :param backing: backing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#backing NetworkPool#backing}
        :param backing_selection_constraint: Defines how backing components are accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#backing_selection_constraint NetworkPool#backing_selection_constraint}
        :param description: Description of the network pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#description NetworkPool#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#id NetworkPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908e11d107985487bbadae213671ece0a78402c85607475cc1c624da25c71e22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkPoolConfig(
            name=name,
            network_provider_id=network_provider_id,
            type=type,
            backing=backing,
            backing_selection_constraint=backing_selection_constraint,
            description=description,
            id=id,
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
        '''Generates CDKTF code for importing a NetworkPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkPool to import.
        :param import_from_id: The id of the existing NetworkPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17a439fad1aea37a09a4af38549b3ba9c53acdf0a9b53912c1cb6d5a7b69632)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBacking")
    def put_backing(
        self,
        *,
        distributed_switch: typing.Optional[typing.Union["NetworkPoolBackingDistributedSwitch", typing.Dict[builtins.str, typing.Any]]] = None,
        port_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkPoolBackingPortGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        range_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkPoolBackingRangeId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        transport_zone: typing.Optional[typing.Union["NetworkPoolBackingTransportZone", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distributed_switch: distributed_switch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#distributed_switch NetworkPool#distributed_switch}
        :param port_group: port_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#port_group NetworkPool#port_group}
        :param range_id: range_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#range_id NetworkPool#range_id}
        :param transport_zone: transport_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#transport_zone NetworkPool#transport_zone}
        '''
        value = NetworkPoolBacking(
            distributed_switch=distributed_switch,
            port_group=port_group,
            range_id=range_id,
            transport_zone=transport_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putBacking", [value]))

    @jsii.member(jsii_name="resetBacking")
    def reset_backing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBacking", []))

    @jsii.member(jsii_name="resetBackingSelectionConstraint")
    def reset_backing_selection_constraint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackingSelectionConstraint", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="backing")
    def backing(self) -> "NetworkPoolBackingOutputReference":
        return typing.cast("NetworkPoolBackingOutputReference", jsii.get(self, "backing"))

    @builtins.property
    @jsii.member(jsii_name="networkProviderName")
    def network_provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkProviderName"))

    @builtins.property
    @jsii.member(jsii_name="networkProviderType")
    def network_provider_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkProviderType"))

    @builtins.property
    @jsii.member(jsii_name="promiscuousMode")
    def promiscuous_mode(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "promiscuousMode"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="totalBackingsCount")
    def total_backings_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalBackingsCount"))

    @builtins.property
    @jsii.member(jsii_name="usedBackingsCount")
    def used_backings_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedBackingsCount"))

    @builtins.property
    @jsii.member(jsii_name="backingInput")
    def backing_input(self) -> typing.Optional["NetworkPoolBacking"]:
        return typing.cast(typing.Optional["NetworkPoolBacking"], jsii.get(self, "backingInput"))

    @builtins.property
    @jsii.member(jsii_name="backingSelectionConstraintInput")
    def backing_selection_constraint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backingSelectionConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkProviderIdInput")
    def network_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="backingSelectionConstraint")
    def backing_selection_constraint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backingSelectionConstraint"))

    @backing_selection_constraint.setter
    def backing_selection_constraint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0dc33002f35836b604470c8deb6ea7a43ea0e1642b7b59ed2df4c15f6f7261e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backingSelectionConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a37f2204667312776301a4a5e7b6506429f90d8b4eb3e7401a6d2194b37540d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da44a2aeae19449c356eb1547893e2730d87843b0cce7b9359641bd9a4b07e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4991b21e44f42a89ff7b4e720323d493913dd7273d448e56d8b1f751384fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkProviderId")
    def network_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkProviderId"))

    @network_provider_id.setter
    def network_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174657d5703e2f02a40848c8da1d7bcc26f8a1e29d8a2f7aa891bb4644d6a368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5980924c42abfce698abfe11667b79401afadc23d1def3cc22fa04b96806a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="vcd.networkPool.NetworkPoolBacking",
    jsii_struct_bases=[],
    name_mapping={
        "distributed_switch": "distributedSwitch",
        "port_group": "portGroup",
        "range_id": "rangeId",
        "transport_zone": "transportZone",
    },
)
class NetworkPoolBacking:
    def __init__(
        self,
        *,
        distributed_switch: typing.Optional[typing.Union["NetworkPoolBackingDistributedSwitch", typing.Dict[builtins.str, typing.Any]]] = None,
        port_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkPoolBackingPortGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        range_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkPoolBackingRangeId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        transport_zone: typing.Optional[typing.Union["NetworkPoolBackingTransportZone", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distributed_switch: distributed_switch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#distributed_switch NetworkPool#distributed_switch}
        :param port_group: port_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#port_group NetworkPool#port_group}
        :param range_id: range_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#range_id NetworkPool#range_id}
        :param transport_zone: transport_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#transport_zone NetworkPool#transport_zone}
        '''
        if isinstance(distributed_switch, dict):
            distributed_switch = NetworkPoolBackingDistributedSwitch(**distributed_switch)
        if isinstance(transport_zone, dict):
            transport_zone = NetworkPoolBackingTransportZone(**transport_zone)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99acd2637946e7aaa75734e17cead520e93c60ff7468b43e78db75fc62ff841d)
            check_type(argname="argument distributed_switch", value=distributed_switch, expected_type=type_hints["distributed_switch"])
            check_type(argname="argument port_group", value=port_group, expected_type=type_hints["port_group"])
            check_type(argname="argument range_id", value=range_id, expected_type=type_hints["range_id"])
            check_type(argname="argument transport_zone", value=transport_zone, expected_type=type_hints["transport_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if distributed_switch is not None:
            self._values["distributed_switch"] = distributed_switch
        if port_group is not None:
            self._values["port_group"] = port_group
        if range_id is not None:
            self._values["range_id"] = range_id
        if transport_zone is not None:
            self._values["transport_zone"] = transport_zone

    @builtins.property
    def distributed_switch(
        self,
    ) -> typing.Optional["NetworkPoolBackingDistributedSwitch"]:
        '''distributed_switch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#distributed_switch NetworkPool#distributed_switch}
        '''
        result = self._values.get("distributed_switch")
        return typing.cast(typing.Optional["NetworkPoolBackingDistributedSwitch"], result)

    @builtins.property
    def port_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkPoolBackingPortGroup"]]]:
        '''port_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#port_group NetworkPool#port_group}
        '''
        result = self._values.get("port_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkPoolBackingPortGroup"]]], result)

    @builtins.property
    def range_id(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkPoolBackingRangeId"]]]:
        '''range_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#range_id NetworkPool#range_id}
        '''
        result = self._values.get("range_id")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkPoolBackingRangeId"]]], result)

    @builtins.property
    def transport_zone(self) -> typing.Optional["NetworkPoolBackingTransportZone"]:
        '''transport_zone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#transport_zone NetworkPool#transport_zone}
        '''
        result = self._values.get("transport_zone")
        return typing.cast(typing.Optional["NetworkPoolBackingTransportZone"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkPoolBacking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.networkPool.NetworkPoolBackingDistributedSwitch",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class NetworkPoolBackingDistributedSwitch:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Backing name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1539372a5e4b18f85f4f0c0f9a19639b7701956e3a52ba6109506ce1efb12f8c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Backing name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkPoolBackingDistributedSwitch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkPoolBackingDistributedSwitchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkPool.NetworkPoolBackingDistributedSwitchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcd7c4980a1016187d24b573df210aba9f5e058e9679254e9793662e4b0a4211)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9117b3cc6e1705afff360fcd34ba76325f9159f791ebef9c056a2cca7d516f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkPoolBackingDistributedSwitch]:
        return typing.cast(typing.Optional[NetworkPoolBackingDistributedSwitch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkPoolBackingDistributedSwitch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6452d3c547429dbf4204f0f5dd7fdf5e40be97ae8bd1b8adfac6c7eed3ff8189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkPoolBackingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkPool.NetworkPoolBackingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49b92c9f9b60bc7e0dd104ccc225f720260bcdc6eb8e14f4b452abbc2bfc19e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDistributedSwitch")
    def put_distributed_switch(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Backing name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        value = NetworkPoolBackingDistributedSwitch(name=name)

        return typing.cast(None, jsii.invoke(self, "putDistributedSwitch", [value]))

    @jsii.member(jsii_name="putPortGroup")
    def put_port_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkPoolBackingPortGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a301e5b40ab62ffe7d78ae8e020fa7af143d8392879766073d9bed2e6f6ff0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPortGroup", [value]))

    @jsii.member(jsii_name="putRangeId")
    def put_range_id(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkPoolBackingRangeId", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b14e0ac2d5a031ffbf8f4540308191ee8b8cd3f2a91cfce9c07f768d0f63319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRangeId", [value]))

    @jsii.member(jsii_name="putTransportZone")
    def put_transport_zone(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Backing name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        value = NetworkPoolBackingTransportZone(name=name)

        return typing.cast(None, jsii.invoke(self, "putTransportZone", [value]))

    @jsii.member(jsii_name="resetDistributedSwitch")
    def reset_distributed_switch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistributedSwitch", []))

    @jsii.member(jsii_name="resetPortGroup")
    def reset_port_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortGroup", []))

    @jsii.member(jsii_name="resetRangeId")
    def reset_range_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeId", []))

    @jsii.member(jsii_name="resetTransportZone")
    def reset_transport_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransportZone", []))

    @builtins.property
    @jsii.member(jsii_name="distributedSwitch")
    def distributed_switch(self) -> NetworkPoolBackingDistributedSwitchOutputReference:
        return typing.cast(NetworkPoolBackingDistributedSwitchOutputReference, jsii.get(self, "distributedSwitch"))

    @builtins.property
    @jsii.member(jsii_name="portGroup")
    def port_group(self) -> "NetworkPoolBackingPortGroupList":
        return typing.cast("NetworkPoolBackingPortGroupList", jsii.get(self, "portGroup"))

    @builtins.property
    @jsii.member(jsii_name="rangeId")
    def range_id(self) -> "NetworkPoolBackingRangeIdList":
        return typing.cast("NetworkPoolBackingRangeIdList", jsii.get(self, "rangeId"))

    @builtins.property
    @jsii.member(jsii_name="transportZone")
    def transport_zone(self) -> "NetworkPoolBackingTransportZoneOutputReference":
        return typing.cast("NetworkPoolBackingTransportZoneOutputReference", jsii.get(self, "transportZone"))

    @builtins.property
    @jsii.member(jsii_name="distributedSwitchInput")
    def distributed_switch_input(
        self,
    ) -> typing.Optional[NetworkPoolBackingDistributedSwitch]:
        return typing.cast(typing.Optional[NetworkPoolBackingDistributedSwitch], jsii.get(self, "distributedSwitchInput"))

    @builtins.property
    @jsii.member(jsii_name="portGroupInput")
    def port_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkPoolBackingPortGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkPoolBackingPortGroup"]]], jsii.get(self, "portGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeIdInput")
    def range_id_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkPoolBackingRangeId"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkPoolBackingRangeId"]]], jsii.get(self, "rangeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="transportZoneInput")
    def transport_zone_input(
        self,
    ) -> typing.Optional["NetworkPoolBackingTransportZone"]:
        return typing.cast(typing.Optional["NetworkPoolBackingTransportZone"], jsii.get(self, "transportZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkPoolBacking]:
        return typing.cast(typing.Optional[NetworkPoolBacking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NetworkPoolBacking]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2448a2b9e303629392be3e4b408da250f03bbe59a0ebaac363e5eb5ce699a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkPool.NetworkPoolBackingPortGroup",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class NetworkPoolBackingPortGroup:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Backing name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23acdc442f53257e26765f407062c1a0c4790cec8909758ee3c9e4f0c5a7082e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Backing name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkPoolBackingPortGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkPoolBackingPortGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkPool.NetworkPoolBackingPortGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe9f50a808b439b9b62717756033dc013ed9f14fe8ea8a46d820b4a3b2621b19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkPoolBackingPortGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2f1afb80bea7011f42815b1d6406a6249f6c35da956c51fff6a972914c4c20)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkPoolBackingPortGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306be7ffe0e863fe783026169354665d7b374badddc993bd34b8a5f882ed2b97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99c59d80b0146bdffbb6417aba868ab881a322c105240d766ace3f3504ea0041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c49417455c060209a18e6714e5c01ac2fbccc44fb07eaedf8883d5d18730a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkPoolBackingPortGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkPoolBackingPortGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkPoolBackingPortGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7dd0dc568ac26132858d32b302bbd5cc5e915e67bd2deb59537948935d6251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkPoolBackingPortGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkPool.NetworkPoolBackingPortGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49986f5698078a394b1807cff81f10cc872bf24b86c9efb48ed2b353cd46cc2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7151bf9e89828de242cf84b0d97f6468ff8624254263bb0a48a6f87d0fc17329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkPoolBackingPortGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkPoolBackingPortGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkPoolBackingPortGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470de11f68090e131eedb3389b2bbddc47ec76e4012a7ebadaf7573e081adb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkPool.NetworkPoolBackingRangeId",
    jsii_struct_bases=[],
    name_mapping={"end_id": "endId", "start_id": "startId"},
)
class NetworkPoolBackingRangeId:
    def __init__(self, *, end_id: jsii.Number, start_id: jsii.Number) -> None:
        '''
        :param end_id: End of the IDs range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#end_id NetworkPool#end_id}
        :param start_id: Start of the IDs range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#start_id NetworkPool#start_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3904f3ac68b10a75311545d0552e9e275240dfe3b10299ffb850c97aee2e46ed)
            check_type(argname="argument end_id", value=end_id, expected_type=type_hints["end_id"])
            check_type(argname="argument start_id", value=start_id, expected_type=type_hints["start_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_id": end_id,
            "start_id": start_id,
        }

    @builtins.property
    def end_id(self) -> jsii.Number:
        '''End of the IDs range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#end_id NetworkPool#end_id}
        '''
        result = self._values.get("end_id")
        assert result is not None, "Required property 'end_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_id(self) -> jsii.Number:
        '''Start of the IDs range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#start_id NetworkPool#start_id}
        '''
        result = self._values.get("start_id")
        assert result is not None, "Required property 'start_id' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkPoolBackingRangeId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkPoolBackingRangeIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkPool.NetworkPoolBackingRangeIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88a4f6a5dfe43618b1fc51a62755bb0eed85eb4fab649b5ec7e00a1a06ceb0d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkPoolBackingRangeIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3da7bac5727eecab638f04090275fd2d845ba59f8be0d6a476928717b32aab2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkPoolBackingRangeIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c520eb9c44f1038c68c5a119a1cd3926dfcfee929fd7eba09465bd23b831cab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccdbd32349732d08dfa42ddc0366a8fcdcbd2338e1d9e8152ac30afa7bd44283)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1747024e873d958719e6d8278964f675471016331742f179af9a1668fa4ba428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkPoolBackingRangeId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkPoolBackingRangeId]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkPoolBackingRangeId]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da7c3471911e414e88927e906f1a36a7da20318cac742bdc227f0a08d2fcaa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkPoolBackingRangeIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkPool.NetworkPoolBackingRangeIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5eb4fbfb435e5495c3b52f96af168d7ab2783b0ec05805143f6e30cd127d456)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endIdInput")
    def end_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endIdInput"))

    @builtins.property
    @jsii.member(jsii_name="startIdInput")
    def start_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startIdInput"))

    @builtins.property
    @jsii.member(jsii_name="endId")
    def end_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endId"))

    @end_id.setter
    def end_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0366201468cc590ca554637dea1b19d72c24c7d0c731c664041eef818a2666f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endId", value)

    @builtins.property
    @jsii.member(jsii_name="startId")
    def start_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startId"))

    @start_id.setter
    def start_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2d9ea6aa45de4bc19ce69e0be7e0e0c0a41307675c5c4d5aac0cd9499ba01e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkPoolBackingRangeId]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkPoolBackingRangeId]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkPoolBackingRangeId]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f281c54f1db69c9b675182ce6ea390163536ea7fd837a467b295509893b099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkPool.NetworkPoolBackingTransportZone",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class NetworkPoolBackingTransportZone:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Backing name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__789cd0d323be09aaa093032cb3db30569916042b248fc5dd79b859c211fa6b04)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Backing name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkPoolBackingTransportZone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkPoolBackingTransportZoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.networkPool.NetworkPoolBackingTransportZoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b69b1b6050dad37ce9cea4e924887d9f3d2b5c4f620ebf82cf07f97980158f70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528fae0abcef0383582f8806b672a18b7cb9700f6eae3644d7b7572b0a1d3f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkPoolBackingTransportZone]:
        return typing.cast(typing.Optional[NetworkPoolBackingTransportZone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkPoolBackingTransportZone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48cf1bb3b94f3d7b1af500c8601aed5d456b67f9ba7c923bb3a6b40add66bc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.networkPool.NetworkPoolConfig",
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
        "network_provider_id": "networkProviderId",
        "type": "type",
        "backing": "backing",
        "backing_selection_constraint": "backingSelectionConstraint",
        "description": "description",
        "id": "id",
    },
)
class NetworkPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        network_provider_id: builtins.str,
        type: builtins.str,
        backing: typing.Optional[typing.Union[NetworkPoolBacking, typing.Dict[builtins.str, typing.Any]]] = None,
        backing_selection_constraint: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of network pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        :param network_provider_id: Id of the network provider (either vCenter or NSX-T manager). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#network_provider_id NetworkPool#network_provider_id}
        :param type: Type of the network pool (one of ``GENEVE``, ``VLAN``, ``PORTGROUP_BACKED``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#type NetworkPool#type}
        :param backing: backing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#backing NetworkPool#backing}
        :param backing_selection_constraint: Defines how backing components are accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#backing_selection_constraint NetworkPool#backing_selection_constraint}
        :param description: Description of the network pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#description NetworkPool#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#id NetworkPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backing, dict):
            backing = NetworkPoolBacking(**backing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89795c264b345b162742c2051a571509a4b973d2111f1f58fcf4f7a3452914b2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_provider_id", value=network_provider_id, expected_type=type_hints["network_provider_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument backing", value=backing, expected_type=type_hints["backing"])
            check_type(argname="argument backing_selection_constraint", value=backing_selection_constraint, expected_type=type_hints["backing_selection_constraint"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network_provider_id": network_provider_id,
            "type": type,
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
        if backing is not None:
            self._values["backing"] = backing
        if backing_selection_constraint is not None:
            self._values["backing_selection_constraint"] = backing_selection_constraint
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id

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
        '''Name of network pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#name NetworkPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_provider_id(self) -> builtins.str:
        '''Id of the network provider (either vCenter or NSX-T manager).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#network_provider_id NetworkPool#network_provider_id}
        '''
        result = self._values.get("network_provider_id")
        assert result is not None, "Required property 'network_provider_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of the network pool (one of ``GENEVE``, ``VLAN``, ``PORTGROUP_BACKED``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#type NetworkPool#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backing(self) -> typing.Optional[NetworkPoolBacking]:
        '''backing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#backing NetworkPool#backing}
        '''
        result = self._values.get("backing")
        return typing.cast(typing.Optional[NetworkPoolBacking], result)

    @builtins.property
    def backing_selection_constraint(self) -> typing.Optional[builtins.str]:
        '''Defines how backing components are accepted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#backing_selection_constraint NetworkPool#backing_selection_constraint}
        '''
        result = self._values.get("backing_selection_constraint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the network pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#description NetworkPool#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/network_pool#id NetworkPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NetworkPool",
    "NetworkPoolBacking",
    "NetworkPoolBackingDistributedSwitch",
    "NetworkPoolBackingDistributedSwitchOutputReference",
    "NetworkPoolBackingOutputReference",
    "NetworkPoolBackingPortGroup",
    "NetworkPoolBackingPortGroupList",
    "NetworkPoolBackingPortGroupOutputReference",
    "NetworkPoolBackingRangeId",
    "NetworkPoolBackingRangeIdList",
    "NetworkPoolBackingRangeIdOutputReference",
    "NetworkPoolBackingTransportZone",
    "NetworkPoolBackingTransportZoneOutputReference",
    "NetworkPoolConfig",
]

publication.publish()

def _typecheckingstub__908e11d107985487bbadae213671ece0a78402c85607475cc1c624da25c71e22(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network_provider_id: builtins.str,
    type: builtins.str,
    backing: typing.Optional[typing.Union[NetworkPoolBacking, typing.Dict[builtins.str, typing.Any]]] = None,
    backing_selection_constraint: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d17a439fad1aea37a09a4af38549b3ba9c53acdf0a9b53912c1cb6d5a7b69632(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0dc33002f35836b604470c8deb6ea7a43ea0e1642b7b59ed2df4c15f6f7261e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a37f2204667312776301a4a5e7b6506429f90d8b4eb3e7401a6d2194b37540d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da44a2aeae19449c356eb1547893e2730d87843b0cce7b9359641bd9a4b07e03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4991b21e44f42a89ff7b4e720323d493913dd7273d448e56d8b1f751384fc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174657d5703e2f02a40848c8da1d7bcc26f8a1e29d8a2f7aa891bb4644d6a368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5980924c42abfce698abfe11667b79401afadc23d1def3cc22fa04b96806a91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99acd2637946e7aaa75734e17cead520e93c60ff7468b43e78db75fc62ff841d(
    *,
    distributed_switch: typing.Optional[typing.Union[NetworkPoolBackingDistributedSwitch, typing.Dict[builtins.str, typing.Any]]] = None,
    port_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkPoolBackingPortGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    range_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkPoolBackingRangeId, typing.Dict[builtins.str, typing.Any]]]]] = None,
    transport_zone: typing.Optional[typing.Union[NetworkPoolBackingTransportZone, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1539372a5e4b18f85f4f0c0f9a19639b7701956e3a52ba6109506ce1efb12f8c(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd7c4980a1016187d24b573df210aba9f5e058e9679254e9793662e4b0a4211(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9117b3cc6e1705afff360fcd34ba76325f9159f791ebef9c056a2cca7d516f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6452d3c547429dbf4204f0f5dd7fdf5e40be97ae8bd1b8adfac6c7eed3ff8189(
    value: typing.Optional[NetworkPoolBackingDistributedSwitch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b92c9f9b60bc7e0dd104ccc225f720260bcdc6eb8e14f4b452abbc2bfc19e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a301e5b40ab62ffe7d78ae8e020fa7af143d8392879766073d9bed2e6f6ff0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkPoolBackingPortGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b14e0ac2d5a031ffbf8f4540308191ee8b8cd3f2a91cfce9c07f768d0f63319(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkPoolBackingRangeId, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2448a2b9e303629392be3e4b408da250f03bbe59a0ebaac363e5eb5ce699a0b(
    value: typing.Optional[NetworkPoolBacking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23acdc442f53257e26765f407062c1a0c4790cec8909758ee3c9e4f0c5a7082e(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9f50a808b439b9b62717756033dc013ed9f14fe8ea8a46d820b4a3b2621b19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2f1afb80bea7011f42815b1d6406a6249f6c35da956c51fff6a972914c4c20(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306be7ffe0e863fe783026169354665d7b374badddc993bd34b8a5f882ed2b97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c59d80b0146bdffbb6417aba868ab881a322c105240d766ace3f3504ea0041(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c49417455c060209a18e6714e5c01ac2fbccc44fb07eaedf8883d5d18730a11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7dd0dc568ac26132858d32b302bbd5cc5e915e67bd2deb59537948935d6251(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkPoolBackingPortGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49986f5698078a394b1807cff81f10cc872bf24b86c9efb48ed2b353cd46cc2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7151bf9e89828de242cf84b0d97f6468ff8624254263bb0a48a6f87d0fc17329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470de11f68090e131eedb3389b2bbddc47ec76e4012a7ebadaf7573e081adb62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkPoolBackingPortGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3904f3ac68b10a75311545d0552e9e275240dfe3b10299ffb850c97aee2e46ed(
    *,
    end_id: jsii.Number,
    start_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a4f6a5dfe43618b1fc51a62755bb0eed85eb4fab649b5ec7e00a1a06ceb0d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3da7bac5727eecab638f04090275fd2d845ba59f8be0d6a476928717b32aab2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c520eb9c44f1038c68c5a119a1cd3926dfcfee929fd7eba09465bd23b831cab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdbd32349732d08dfa42ddc0366a8fcdcbd2338e1d9e8152ac30afa7bd44283(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1747024e873d958719e6d8278964f675471016331742f179af9a1668fa4ba428(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da7c3471911e414e88927e906f1a36a7da20318cac742bdc227f0a08d2fcaa7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkPoolBackingRangeId]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5eb4fbfb435e5495c3b52f96af168d7ab2783b0ec05805143f6e30cd127d456(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0366201468cc590ca554637dea1b19d72c24c7d0c731c664041eef818a2666f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2d9ea6aa45de4bc19ce69e0be7e0e0c0a41307675c5c4d5aac0cd9499ba01e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f281c54f1db69c9b675182ce6ea390163536ea7fd837a467b295509893b099(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkPoolBackingRangeId]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789cd0d323be09aaa093032cb3db30569916042b248fc5dd79b859c211fa6b04(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69b1b6050dad37ce9cea4e924887d9f3d2b5c4f620ebf82cf07f97980158f70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528fae0abcef0383582f8806b672a18b7cb9700f6eae3644d7b7572b0a1d3f37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48cf1bb3b94f3d7b1af500c8601aed5d456b67f9ba7c923bb3a6b40add66bc67(
    value: typing.Optional[NetworkPoolBackingTransportZone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89795c264b345b162742c2051a571509a4b973d2111f1f58fcf4f7a3452914b2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network_provider_id: builtins.str,
    type: builtins.str,
    backing: typing.Optional[typing.Union[NetworkPoolBacking, typing.Dict[builtins.str, typing.Any]]] = None,
    backing_selection_constraint: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
