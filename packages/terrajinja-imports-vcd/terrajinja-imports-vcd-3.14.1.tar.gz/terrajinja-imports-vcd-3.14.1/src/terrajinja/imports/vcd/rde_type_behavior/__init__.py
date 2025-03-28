'''
# `vcd_rde_type_behavior`

Refer to the Terraform Registry for docs: [`vcd_rde_type_behavior`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior).
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


class RdeTypeBehavior(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.rdeTypeBehavior.RdeTypeBehavior",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior vcd_rde_type_behavior}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        rde_interface_behavior_id: builtins.str,
        rde_type_id: builtins.str,
        always_update_secure_execution_properties: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        execution: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_json: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior vcd_rde_type_behavior} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param rde_interface_behavior_id: The ID of the original RDE Interface Behavior to override. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#rde_interface_behavior_id RdeTypeBehavior#rde_interface_behavior_id}
        :param rde_type_id: The ID of the RDE Type that owns the Behavior override. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#rde_type_id RdeTypeBehavior#rde_type_id}
        :param always_update_secure_execution_properties: Useful to update execution properties marked with *secure* and *internal*,as these are not retrievable from VCD, so they are not saved in state. Setting this to 'true' will make the Providerto ask for updates whenever there is a secure property in the execution of the Behavior Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#always_update_secure_execution_properties RdeTypeBehavior#always_update_secure_execution_properties}
        :param description: The description of the contract of the overridden Behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#description RdeTypeBehavior#description}
        :param execution: Execution map of the Behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#execution RdeTypeBehavior#execution}
        :param execution_json: Execution of the Behavior in JSON format, that allows to define complex Behavior executions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#execution_json RdeTypeBehavior#execution_json}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#id RdeTypeBehavior#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bacb4af2c74d41fda43ba397d1ae757c39113dbb305632128082209ea5e517)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RdeTypeBehaviorConfig(
            rde_interface_behavior_id=rde_interface_behavior_id,
            rde_type_id=rde_type_id,
            always_update_secure_execution_properties=always_update_secure_execution_properties,
            description=description,
            execution=execution,
            execution_json=execution_json,
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
        '''Generates CDKTF code for importing a RdeTypeBehavior resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RdeTypeBehavior to import.
        :param import_from_id: The id of the existing RdeTypeBehavior that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RdeTypeBehavior to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d28bdaf1e33b3878cf6d537667bc756fc8dcdc9cc72e3af38a2908008ae07d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlwaysUpdateSecureExecutionProperties")
    def reset_always_update_secure_execution_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysUpdateSecureExecutionProperties", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExecution")
    def reset_execution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecution", []))

    @jsii.member(jsii_name="resetExecutionJson")
    def reset_execution_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionJson", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @builtins.property
    @jsii.member(jsii_name="alwaysUpdateSecureExecutionPropertiesInput")
    def always_update_secure_execution_properties_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alwaysUpdateSecureExecutionPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="executionInput")
    def execution_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "executionInput"))

    @builtins.property
    @jsii.member(jsii_name="executionJsonInput")
    def execution_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="rdeInterfaceBehaviorIdInput")
    def rde_interface_behavior_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdeInterfaceBehaviorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="rdeTypeIdInput")
    def rde_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysUpdateSecureExecutionProperties")
    def always_update_secure_execution_properties(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alwaysUpdateSecureExecutionProperties"))

    @always_update_secure_execution_properties.setter
    def always_update_secure_execution_properties(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a305a3f0a4037eb96a942a9fd98bdbce198bc1125aad4e0ec85fcef9212e5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysUpdateSecureExecutionProperties", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4f5c328ab3427775bd41c6e719fa31087dde60405b2ea5468c281781eddc56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="execution")
    def execution(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "execution"))

    @execution.setter
    def execution(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1f64966d80be81b108b0b0c8669d6a0a972b7af36b94678da451792e96e683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "execution", value)

    @builtins.property
    @jsii.member(jsii_name="executionJson")
    def execution_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionJson"))

    @execution_json.setter
    def execution_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf1922c31e8138f09c7b5d1b0eae22a703f370c39137a2bed40dfbe9dff4e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionJson", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf2b864a56e08ee695ee66f4b0405677737e94bfbac62d658fb40e92f28f4af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="rdeInterfaceBehaviorId")
    def rde_interface_behavior_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdeInterfaceBehaviorId"))

    @rde_interface_behavior_id.setter
    def rde_interface_behavior_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dedf5ada3437ce3baa33bcea79fb83141060800b4043c917253b302fc5df298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdeInterfaceBehaviorId", value)

    @builtins.property
    @jsii.member(jsii_name="rdeTypeId")
    def rde_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdeTypeId"))

    @rde_type_id.setter
    def rde_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d503f0ff1011ccaf4afcd439cc991183b347b2fc88b0b0d9903af607100141d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdeTypeId", value)


@jsii.data_type(
    jsii_type="vcd.rdeTypeBehavior.RdeTypeBehaviorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "rde_interface_behavior_id": "rdeInterfaceBehaviorId",
        "rde_type_id": "rdeTypeId",
        "always_update_secure_execution_properties": "alwaysUpdateSecureExecutionProperties",
        "description": "description",
        "execution": "execution",
        "execution_json": "executionJson",
        "id": "id",
    },
)
class RdeTypeBehaviorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rde_interface_behavior_id: builtins.str,
        rde_type_id: builtins.str,
        always_update_secure_execution_properties: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        execution: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_json: typing.Optional[builtins.str] = None,
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
        :param rde_interface_behavior_id: The ID of the original RDE Interface Behavior to override. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#rde_interface_behavior_id RdeTypeBehavior#rde_interface_behavior_id}
        :param rde_type_id: The ID of the RDE Type that owns the Behavior override. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#rde_type_id RdeTypeBehavior#rde_type_id}
        :param always_update_secure_execution_properties: Useful to update execution properties marked with *secure* and *internal*,as these are not retrievable from VCD, so they are not saved in state. Setting this to 'true' will make the Providerto ask for updates whenever there is a secure property in the execution of the Behavior Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#always_update_secure_execution_properties RdeTypeBehavior#always_update_secure_execution_properties}
        :param description: The description of the contract of the overridden Behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#description RdeTypeBehavior#description}
        :param execution: Execution map of the Behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#execution RdeTypeBehavior#execution}
        :param execution_json: Execution of the Behavior in JSON format, that allows to define complex Behavior executions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#execution_json RdeTypeBehavior#execution_json}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#id RdeTypeBehavior#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e746396c00dd080b7bbf40175ee5f15fce01eca699c22a22c11f064e8393c10)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument rde_interface_behavior_id", value=rde_interface_behavior_id, expected_type=type_hints["rde_interface_behavior_id"])
            check_type(argname="argument rde_type_id", value=rde_type_id, expected_type=type_hints["rde_type_id"])
            check_type(argname="argument always_update_secure_execution_properties", value=always_update_secure_execution_properties, expected_type=type_hints["always_update_secure_execution_properties"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
            check_type(argname="argument execution_json", value=execution_json, expected_type=type_hints["execution_json"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rde_interface_behavior_id": rde_interface_behavior_id,
            "rde_type_id": rde_type_id,
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
        if always_update_secure_execution_properties is not None:
            self._values["always_update_secure_execution_properties"] = always_update_secure_execution_properties
        if description is not None:
            self._values["description"] = description
        if execution is not None:
            self._values["execution"] = execution
        if execution_json is not None:
            self._values["execution_json"] = execution_json
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
    def rde_interface_behavior_id(self) -> builtins.str:
        '''The ID of the original RDE Interface Behavior to override.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#rde_interface_behavior_id RdeTypeBehavior#rde_interface_behavior_id}
        '''
        result = self._values.get("rde_interface_behavior_id")
        assert result is not None, "Required property 'rde_interface_behavior_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rde_type_id(self) -> builtins.str:
        '''The ID of the RDE Type that owns the Behavior override.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#rde_type_id RdeTypeBehavior#rde_type_id}
        '''
        result = self._values.get("rde_type_id")
        assert result is not None, "Required property 'rde_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_update_secure_execution_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Useful to update execution properties marked with *secure* and *internal*,as these are not retrievable from VCD, so they are not saved in state.

        Setting this to 'true' will make the Providerto ask for updates whenever there is a secure property in the execution of the Behavior

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#always_update_secure_execution_properties RdeTypeBehavior#always_update_secure_execution_properties}
        '''
        result = self._values.get("always_update_secure_execution_properties")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the contract of the overridden Behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#description RdeTypeBehavior#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Execution map of the Behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#execution RdeTypeBehavior#execution}
        '''
        result = self._values.get("execution")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_json(self) -> typing.Optional[builtins.str]:
        '''Execution of the Behavior in JSON format, that allows to define complex Behavior executions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#execution_json RdeTypeBehavior#execution_json}
        '''
        result = self._values.get("execution_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/rde_type_behavior#id RdeTypeBehavior#id}.

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
        return "RdeTypeBehaviorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RdeTypeBehavior",
    "RdeTypeBehaviorConfig",
]

publication.publish()

def _typecheckingstub__73bacb4af2c74d41fda43ba397d1ae757c39113dbb305632128082209ea5e517(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    rde_interface_behavior_id: builtins.str,
    rde_type_id: builtins.str,
    always_update_secure_execution_properties: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    execution: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_json: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b9d28bdaf1e33b3878cf6d537667bc756fc8dcdc9cc72e3af38a2908008ae07d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a305a3f0a4037eb96a942a9fd98bdbce198bc1125aad4e0ec85fcef9212e5fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4f5c328ab3427775bd41c6e719fa31087dde60405b2ea5468c281781eddc56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1f64966d80be81b108b0b0c8669d6a0a972b7af36b94678da451792e96e683(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf1922c31e8138f09c7b5d1b0eae22a703f370c39137a2bed40dfbe9dff4e2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf2b864a56e08ee695ee66f4b0405677737e94bfbac62d658fb40e92f28f4af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dedf5ada3437ce3baa33bcea79fb83141060800b4043c917253b302fc5df298(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d503f0ff1011ccaf4afcd439cc991183b347b2fc88b0b0d9903af607100141d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e746396c00dd080b7bbf40175ee5f15fce01eca699c22a22c11f064e8393c10(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rde_interface_behavior_id: builtins.str,
    rde_type_id: builtins.str,
    always_update_secure_execution_properties: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    execution: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_json: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
