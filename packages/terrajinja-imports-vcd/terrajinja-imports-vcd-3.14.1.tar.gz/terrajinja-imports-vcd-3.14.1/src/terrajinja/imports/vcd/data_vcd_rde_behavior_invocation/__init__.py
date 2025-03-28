'''
# `data_vcd_rde_behavior_invocation`

Refer to the Terraform Registry for docs: [`data_vcd_rde_behavior_invocation`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation).
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


class DataVcdRdeBehaviorInvocation(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdRdeBehaviorInvocation.DataVcdRdeBehaviorInvocation",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation vcd_rde_behavior_invocation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        behavior_id: builtins.str,
        rde_id: builtins.str,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        arguments_json: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        invoke_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_json: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation vcd_rde_behavior_invocation} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param behavior_id: The ID of either a RDE Interface Behavior or RDE Type Behavior to be invoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#behavior_id DataVcdRdeBehaviorInvocation#behavior_id}
        :param rde_id: The ID of the RDE for which the Behavior will be invoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#rde_id DataVcdRdeBehaviorInvocation#rde_id}
        :param arguments: The arguments to be passed to the invoked Behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#arguments DataVcdRdeBehaviorInvocation#arguments}
        :param arguments_json: The arguments to be passed to the invoked Behavior, as a JSON string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#arguments_json DataVcdRdeBehaviorInvocation#arguments_json}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#id DataVcdRdeBehaviorInvocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param invoke_on_refresh: If 'true', invokes the Behavior on every refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#invoke_on_refresh DataVcdRdeBehaviorInvocation#invoke_on_refresh}
        :param metadata: Metadata to be passed to the invoked Behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#metadata DataVcdRdeBehaviorInvocation#metadata}
        :param metadata_json: Metadata to be passed to the invoked Behavior, as a JSON string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#metadata_json DataVcdRdeBehaviorInvocation#metadata_json}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09da8eb0a7ac72294dc3ba0486aeb657ca8720239339ec81a1da6038342fd61a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataVcdRdeBehaviorInvocationConfig(
            behavior_id=behavior_id,
            rde_id=rde_id,
            arguments=arguments,
            arguments_json=arguments_json,
            id=id,
            invoke_on_refresh=invoke_on_refresh,
            metadata=metadata,
            metadata_json=metadata_json,
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
        '''Generates CDKTF code for importing a DataVcdRdeBehaviorInvocation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataVcdRdeBehaviorInvocation to import.
        :param import_from_id: The id of the existing DataVcdRdeBehaviorInvocation that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataVcdRdeBehaviorInvocation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba89b07aeade64ce737ea4770d595db6c64413a6c2183a2efa5de0f268944b6e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetArgumentsJson")
    def reset_arguments_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgumentsJson", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInvokeOnRefresh")
    def reset_invoke_on_refresh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvokeOnRefresh", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataJson")
    def reset_metadata_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataJson", []))

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
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "argumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="argumentsJsonInput")
    def arguments_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argumentsJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="behaviorIdInput")
    def behavior_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="invokeOnRefreshInput")
    def invoke_on_refresh_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invokeOnRefreshInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataJsonInput")
    def metadata_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="rdeIdInput")
    def rde_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "arguments"))

    @arguments.setter
    def arguments(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cbeed7ddff70456eede309b8929b6156de70dae4e210e9d0564be6b0b0a89f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arguments", value)

    @builtins.property
    @jsii.member(jsii_name="argumentsJson")
    def arguments_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argumentsJson"))

    @arguments_json.setter
    def arguments_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f176dfba70fb9bba7b894cd42fd68137ea7958ced443b1326d957d5b275a167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argumentsJson", value)

    @builtins.property
    @jsii.member(jsii_name="behaviorId")
    def behavior_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behaviorId"))

    @behavior_id.setter
    def behavior_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352fb4dbc247b2414f1cd02a6eda2499eeaddbc09aaa1158bdc660e48f0fb1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behaviorId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4183179bfd033d9a9510d83769c37e8b8064023d12a8d31241c665a7e2bfe9be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="invokeOnRefresh")
    def invoke_on_refresh(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invokeOnRefresh"))

    @invoke_on_refresh.setter
    def invoke_on_refresh(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679a0a15aa4ac70cc86462a432351c8a6bd716185c217aa9c7d53d2c6b5bb94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invokeOnRefresh", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299838423f6af4abc894ae050e7c5ffe858ba754867ec2e712932600b9f5242e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="metadataJson")
    def metadata_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataJson"))

    @metadata_json.setter
    def metadata_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22208b0fe436119880e29bb09fa97dcc8d341a7906fe5abc72800057bc2d009f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataJson", value)

    @builtins.property
    @jsii.member(jsii_name="rdeId")
    def rde_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdeId"))

    @rde_id.setter
    def rde_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac54f47ebe27c879534abf3450056082269521aa3c011f88d0afcfd1efbb8930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdeId", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdRdeBehaviorInvocation.DataVcdRdeBehaviorInvocationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "behavior_id": "behaviorId",
        "rde_id": "rdeId",
        "arguments": "arguments",
        "arguments_json": "argumentsJson",
        "id": "id",
        "invoke_on_refresh": "invokeOnRefresh",
        "metadata": "metadata",
        "metadata_json": "metadataJson",
    },
)
class DataVcdRdeBehaviorInvocationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        behavior_id: builtins.str,
        rde_id: builtins.str,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        arguments_json: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        invoke_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param behavior_id: The ID of either a RDE Interface Behavior or RDE Type Behavior to be invoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#behavior_id DataVcdRdeBehaviorInvocation#behavior_id}
        :param rde_id: The ID of the RDE for which the Behavior will be invoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#rde_id DataVcdRdeBehaviorInvocation#rde_id}
        :param arguments: The arguments to be passed to the invoked Behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#arguments DataVcdRdeBehaviorInvocation#arguments}
        :param arguments_json: The arguments to be passed to the invoked Behavior, as a JSON string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#arguments_json DataVcdRdeBehaviorInvocation#arguments_json}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#id DataVcdRdeBehaviorInvocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param invoke_on_refresh: If 'true', invokes the Behavior on every refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#invoke_on_refresh DataVcdRdeBehaviorInvocation#invoke_on_refresh}
        :param metadata: Metadata to be passed to the invoked Behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#metadata DataVcdRdeBehaviorInvocation#metadata}
        :param metadata_json: Metadata to be passed to the invoked Behavior, as a JSON string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#metadata_json DataVcdRdeBehaviorInvocation#metadata_json}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573136980a8c778b88352bb2032a7c3c438ea25496cb5a0f09e9c35c319d2ef7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument behavior_id", value=behavior_id, expected_type=type_hints["behavior_id"])
            check_type(argname="argument rde_id", value=rde_id, expected_type=type_hints["rde_id"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument arguments_json", value=arguments_json, expected_type=type_hints["arguments_json"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument invoke_on_refresh", value=invoke_on_refresh, expected_type=type_hints["invoke_on_refresh"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_json", value=metadata_json, expected_type=type_hints["metadata_json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior_id": behavior_id,
            "rde_id": rde_id,
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
        if arguments is not None:
            self._values["arguments"] = arguments
        if arguments_json is not None:
            self._values["arguments_json"] = arguments_json
        if id is not None:
            self._values["id"] = id
        if invoke_on_refresh is not None:
            self._values["invoke_on_refresh"] = invoke_on_refresh
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_json is not None:
            self._values["metadata_json"] = metadata_json

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
    def behavior_id(self) -> builtins.str:
        '''The ID of either a RDE Interface Behavior or RDE Type Behavior to be invoked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#behavior_id DataVcdRdeBehaviorInvocation#behavior_id}
        '''
        result = self._values.get("behavior_id")
        assert result is not None, "Required property 'behavior_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rde_id(self) -> builtins.str:
        '''The ID of the RDE for which the Behavior will be invoked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#rde_id DataVcdRdeBehaviorInvocation#rde_id}
        '''
        result = self._values.get("rde_id")
        assert result is not None, "Required property 'rde_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The arguments to be passed to the invoked Behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#arguments DataVcdRdeBehaviorInvocation#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def arguments_json(self) -> typing.Optional[builtins.str]:
        '''The arguments to be passed to the invoked Behavior, as a JSON string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#arguments_json DataVcdRdeBehaviorInvocation#arguments_json}
        '''
        result = self._values.get("arguments_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#id DataVcdRdeBehaviorInvocation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invoke_on_refresh(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', invokes the Behavior on every refresh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#invoke_on_refresh DataVcdRdeBehaviorInvocation#invoke_on_refresh}
        '''
        result = self._values.get("invoke_on_refresh")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata to be passed to the invoked Behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#metadata DataVcdRdeBehaviorInvocation#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_json(self) -> typing.Optional[builtins.str]:
        '''Metadata to be passed to the invoked Behavior, as a JSON string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/rde_behavior_invocation#metadata_json DataVcdRdeBehaviorInvocation#metadata_json}
        '''
        result = self._values.get("metadata_json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdRdeBehaviorInvocationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataVcdRdeBehaviorInvocation",
    "DataVcdRdeBehaviorInvocationConfig",
]

publication.publish()

def _typecheckingstub__09da8eb0a7ac72294dc3ba0486aeb657ca8720239339ec81a1da6038342fd61a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    behavior_id: builtins.str,
    rde_id: builtins.str,
    arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    arguments_json: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    invoke_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_json: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ba89b07aeade64ce737ea4770d595db6c64413a6c2183a2efa5de0f268944b6e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cbeed7ddff70456eede309b8929b6156de70dae4e210e9d0564be6b0b0a89f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f176dfba70fb9bba7b894cd42fd68137ea7958ced443b1326d957d5b275a167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352fb4dbc247b2414f1cd02a6eda2499eeaddbc09aaa1158bdc660e48f0fb1fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4183179bfd033d9a9510d83769c37e8b8064023d12a8d31241c665a7e2bfe9be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679a0a15aa4ac70cc86462a432351c8a6bd716185c217aa9c7d53d2c6b5bb94d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299838423f6af4abc894ae050e7c5ffe858ba754867ec2e712932600b9f5242e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22208b0fe436119880e29bb09fa97dcc8d341a7906fe5abc72800057bc2d009f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac54f47ebe27c879534abf3450056082269521aa3c011f88d0afcfd1efbb8930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573136980a8c778b88352bb2032a7c3c438ea25496cb5a0f09e9c35c319d2ef7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    behavior_id: builtins.str,
    rde_id: builtins.str,
    arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    arguments_json: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    invoke_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
