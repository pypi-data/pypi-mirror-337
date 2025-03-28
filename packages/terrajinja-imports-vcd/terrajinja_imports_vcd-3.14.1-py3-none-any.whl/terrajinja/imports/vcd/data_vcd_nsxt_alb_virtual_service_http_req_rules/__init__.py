'''
# `data_vcd_nsxt_alb_virtual_service_http_req_rules`

Refer to the Terraform Registry for docs: [`data_vcd_nsxt_alb_virtual_service_http_req_rules`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules).
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


class DataVcdNsxtAlbVirtualServiceHttpReqRules(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules vcd_nsxt_alb_virtual_service_http_req_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        virtual_service_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules vcd_nsxt_alb_virtual_service_http_req_rules} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param virtual_service_id: NSX-T ALB Virtual Service ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules#virtual_service_id DataVcdNsxtAlbVirtualServiceHttpReqRules#virtual_service_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules#id DataVcdNsxtAlbVirtualServiceHttpReqRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a6df64b625578221a03c419d4eb7d260ac2daca0dd492a1fd7f09cfc6b2a8cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataVcdNsxtAlbVirtualServiceHttpReqRulesConfig(
            virtual_service_id=virtual_service_id,
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
        '''Generates CDKTF code for importing a DataVcdNsxtAlbVirtualServiceHttpReqRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataVcdNsxtAlbVirtualServiceHttpReqRules to import.
        :param import_from_id: The id of the existing DataVcdNsxtAlbVirtualServiceHttpReqRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataVcdNsxtAlbVirtualServiceHttpReqRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e954ab9b4ef3413ad6eca8185f946efc2a6e7377a81354ed3193d00d912d061)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
    @jsii.member(jsii_name="rule")
    def rule(self) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleList":
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceIdInput")
    def virtual_service_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualServiceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52011b689316818dcb4a1e258a91e1fdf107fbe0cbd2a2fd4c8fa1005ff85817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="virtualServiceId")
    def virtual_service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceId"))

    @virtual_service_id.setter
    def virtual_service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f797c4411e92fec94ab38e691e75b0d9ab773154ded38f4c4cb902ceae64fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceId", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "virtual_service_id": "virtualServiceId",
        "id": "id",
    },
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        virtual_service_id: builtins.str,
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
        :param virtual_service_id: NSX-T ALB Virtual Service ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules#virtual_service_id DataVcdNsxtAlbVirtualServiceHttpReqRules#virtual_service_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules#id DataVcdNsxtAlbVirtualServiceHttpReqRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30dfa71932680e10825d220590a798cc97d3d32f9fceb06f0c9afffcdd23d35d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument virtual_service_id", value=virtual_service_id, expected_type=type_hints["virtual_service_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service_id": virtual_service_id,
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
    def virtual_service_id(self) -> builtins.str:
        '''NSX-T ALB Virtual Service ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules#virtual_service_id DataVcdNsxtAlbVirtualServiceHttpReqRules#virtual_service_id}
        '''
        result = self._values.get("virtual_service_id")
        assert result is not None, "Required property 'virtual_service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/data-sources/nsxt_alb_virtual_service_http_req_rules#id DataVcdNsxtAlbVirtualServiceHttpReqRules#id}.

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
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRule",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8728c322537e832a2ddb05b5d60f91638fa6ac51d93ea2cf41c5c9fffcecdd3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5b71a7dc3d05e08bcb2c6cf678a53808826de4e194ccfefb68df3556b7d37a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f3b407b797648492bb0f1a2e845fc1a2b4ed879a3c0fe66b801f6e32151f7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d90a7332aa17fdca4a40f16241271bc88a4a558a38ea140f910d31a6bd3e7c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26bd8e48972703b543a3eefa969b2a1d8c043dd83cf6b1bca0a57c05a3c218d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0ceac2052b2fbc34ec2cdc21dc228a08eb9bf7ce3d35f4b0f11ca7e47955eab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c3b87dd38b7396f03f46a74f595d2e2b66f31ac273aec75b5c1a0ca2912312)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d4ca3fe4ad19f20e749412c57bd2548d10c1c60f7055b9845a226283de0efa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be183f03a4c1dbff6557dbdae796e9c7bd667c21f96b97acee8d7b66716e7051)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2429ff06c1d43b5c2c67aa3200040f9967e7fa1812bb2efc8d10087dbb3ed9f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bfaa5aa96aefab9a953fda31bbb08fe934efaf8d19f3d0f6a51a6787a3ffc01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f9dc339f660938bdc0ae091df1f149ce15168d92492e4efc7f9a4453ca130b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a67b617fe6e444d37210aebd1c9549ba55eda46ef4dbf7e6ad4a051631f7b0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modifyHeader")
    def modify_header(
        self,
    ) -> DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList:
        return typing.cast(DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList, jsii.get(self, "modifyHeader"))

    @builtins.property
    @jsii.member(jsii_name="redirect")
    def redirect(
        self,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectList":
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectList", jsii.get(self, "redirect"))

    @builtins.property
    @jsii.member(jsii_name="rewriteUrl")
    def rewrite_url(
        self,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlList":
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlList", jsii.get(self, "rewriteUrl"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActions]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46081b498f5a38e80e94ba139b3a78fbc94056db5e99b92185aa78511ef86d85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78c37f6152b9f4a6474764ba2aa9c278835293e4e766b040c1057c932e91cd80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c44294c2d45be0cf389b6762ccdf31e763025a48b762368e0d0ef3772f9a265)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c0d4965fa52d7ce5d2e5dc4189dc8d988b9169dcfeb7a5fcd1f5508c85b9c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fd4177df627f3ab5d05b27a7a1f12615742a031de753296295dd016b09b554d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49f59c92730be90df94c1372c48c81afef682151a329fbeeeaa7a059cca3d9f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c5f7e81951a6ccd432512d9b152711e203e75d53f0a2145f8190f55ef1b5282)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="keepQuery")
    def keep_query(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "keepQuery"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af3a36e9723efff3ea10507fa7e81303f119e88680d4222f16e2ae4122917d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed41f2fbbcd5cf60899cabfde1279c73bf7efaa66e1619e6ed38dc0993d08a56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d35ef14f453df4ba0c68ce07e7327d38e2d625f80f84e7adb4da664734f7de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958a86b368365f369fcfc0139907a097f2e7d72656f3f9f4d41dff4a7bc8a09c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8ae95c5f9b03b5c380f110be15cf3193a28bdcbae772e7a75b3fa4054e8df34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__434702be78660f5ba0036cc032f0625d4b03ca77c1aabcbc871f6d6f2513c734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8c8882cc853af7547140accd818cf65fd6c2fbd105802a2b3ed15b1b8f69b7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="existingPath")
    def existing_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "existingPath"))

    @builtins.property
    @jsii.member(jsii_name="hostHeader")
    def host_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostHeader"))

    @builtins.property
    @jsii.member(jsii_name="keepQuery")
    def keep_query(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "keepQuery"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77cc93e387dcc8804f581fc3e47dfa59c3464c1034de4a80b79e79f3a0795fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2493d467a2df6ed0c14532776297219d79e5848de337a48480f63e28f1931d50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3642577a2d0e3024d3aa1eab5858ebc3384330e8e0d3db40a6372f845ce0264)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590cc709dbea46336f220a6194edc19dc985577c7a5af8ad0453e080e4ad4a61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c734326ca4173ed99528872db2edb1d9c03c223194009bb7deac0b230d3a310)
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
            type_hints = typing.get_type_hints(_typecheckingstub__251438806b733093c5750062f3b1ff1062236e7e041b23d4654733dc161e877f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cef89e3816c85d1541a38834262bea4874dd9d81043d236634d8176a2706105)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f62c552102165aef1c280961ff6309b0386f51826f47dfced9a4db02b0fae7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7588281dae5b7bfbaaad4314f0e39246f0cc785540917b500de9bbc5c21a6ff9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98d7c4635fa64dfa37b85e5e0f6778de5afc16ce4b33d5725fe69090a027ede2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3642accdc7867057c90d8e720e194626ee1d1cc21f9791098446648f9c8821a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ed56f9b35a72f14b6451be2b639f625590269378799ae2896ac7796c6493e7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2653c916881526ed1656ae0a21d3d9e944e00f128a045a1b69c148eb7ebecb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9212094ab919f75c21d42ea06429de4e7da6435fa63bbbc438d06c77c3e3bacf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d827870c09af15a04803f01594829c628ae21334a653b781a84d00099187ec5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64e36918c1e726b8d6792d3b98972848abe8ad07cb468cfbdbf98e551535edd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41ec122070540be8ef98f8f05762ad1e4e69ef1c4355b182af6fb45cb185b4d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97a4408bfa9cab29a85b490d43af4854dfab50afad4ac0afaee02fbc19d208bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c648197de4ee8c2cedeae77d96886aa9661f4a3d29990523c602014b766ab1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b99ecd44a6bec3bc536455695bb853f4bbba4a79ee2bc182c3aed5acfb44bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86ca198b084525303bd03792b988d6e92004c39b129f51612832c3317abf3921)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba948a1749fe221cdf4c3fc5e52be57a242552edd72aec3f4b5f57fb5a1e889)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d03a9a3aa94f5bc7fc63bbacb9830ca757502d233eea7f4a6e219b1a1595b22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b463c161a865ca0d06cf8f64fd423faa6e58b2e4de8b31267703ee74d4a6eaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a999647c315359cffcf373d860a38762411d4a7aab89f3707b046ac2fefcb67c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6797c4c725c8e9b2843da6d787f31586817632f6ef8bb88c952ada9aa1109e11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97c3a56bc4d7dbcf5f2ea685089f945237715b4e25c1de70809cd14c8a53d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93696e3b6d134b38b1b0f5c69363e35419a1fb8080e37c0c497090247425be3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e550d8af552c2296c04da0956754fa73ba3d7bf77d143077d48886177cdc4f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4789b862f3c049e32d4c68038031eed68d46290cb1ef7164aff07babc152b0d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70a8ba24732100a60c32d9b36c45843e89d2554285beee373d7ebcb76e81e2e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba27429db1220f10985aa886e253ef4105e928c331b7c8448b0d88dcbdf9e01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d4a54d34b189570c02ca728b04da53f1b1a0611d451c2b5975e165f77a59caa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientIpAddress")
    def client_ip_address(
        self,
    ) -> DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressList:
        return typing.cast(DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressList, jsii.get(self, "clientIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="cookie")
    def cookie(
        self,
    ) -> DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieList:
        return typing.cast(DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieList, jsii.get(self, "cookie"))

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(
        self,
    ) -> DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsList:
        return typing.cast(DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsList, jsii.get(self, "httpMethods"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(
        self,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathList":
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathList", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolType"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(
        self,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList":
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList", jsii.get(self, "requestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="servicePorts")
    def service_ports(
        self,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsList":
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsList", jsii.get(self, "servicePorts"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0d1b676e9f6051edc3929d7a4dbf69a983a113de1610aa4bebe67c22ba0038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf8efdcf4cda15c8dc945a8c6e36aa5d9a43f85156e7990ea6ce9cf5cfbb7979)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716b89db21bf94820b9164c1f6b2018526843ef57ca75738bd5c66189d039dfc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17369e5f1344e05b0e10994938db62542b36c20cd57d599aa53fedc1866158a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86b27e29a59bcc37ab6daa81365a6b99e625d3b70bad32f1be7f2a79b17a24fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f64e274d152c44820a9880942210cffeeb49da2ba3e32b85724f5885807a6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ce188c94c397a83c7f51d37594dec74f1d03581ce74e5ae58acb7f9a3697bfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c22b73a4978e6e4e40fcff28cceed397b1d81165cd95073c12d34f7c4966144b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a9a8b07f63764e7fc619867186a4674105593bdbfd16b661bd32ecba5cc282b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e02f8b9fe2def8bbff5b0c08c3c77a8793bdbdcfa6653576c2b4d15ea091751)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3c5a36d66ddce1f59740d6baf8181dc59de42c2c7f28c69d2fe2708e17c7b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__399e59c030329f8532619bfd02c763e2efcf46a9b9b598be631e92c1c2c03943)
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
            type_hints = typing.get_type_hints(_typecheckingstub__068a7a2503e617a8d9909b8c6457ee8db4093e768fdf22258400298338a90c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bbd01822c81614165c87a4e55a571ddf35000b6ed126cb13bcc524ebd2895b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e93389b21d8931a7d6514b23b5c3ca4335775ae0daa126109f5630f21e2efc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__997866268611f6d3553fce580d3f475d8f68dfb188a1a49d34e066b9e73a78ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8c3a5613d60dcca1632a4983db6ad849b35cd805e26cf2c3c6580d04431447)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a51605b359340d6f4599bb1e536b0b5d03404fd79a33ce30ab5b2e7d1d4526)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a6917f03c7d9d79d76b5c3e5eab734041fd4932116b2a653812b0a719057c56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0717c0824155a1301fe6e3eebb370ffdce96b76f7731a94416ad7223d66b047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76b597ba6cb68999d763c2dff28134d6f059b2597aac11fd025847316d5c1314)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dfac2e5174649624753f4e61bccf88e2b7674df99cf6ad19ce7dda2cae084bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.dataVcdNsxtAlbVirtualServiceHttpReqRules.DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0015e33990665eb440e4ebc6245cec615e1eace92c5a5d06bb8e445ab0c64d0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsList:
        return typing.cast(DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsList, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "active"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="matchCriteria")
    def match_criteria(
        self,
    ) -> DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaList:
        return typing.cast(DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaList, jsii.get(self, "matchCriteria"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRule]:
        return typing.cast(typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f35b566f5d819ebacc7943015bad11e1ac515ece1f28f72fcba76d2184da69f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataVcdNsxtAlbVirtualServiceHttpReqRules",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesConfig",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRule",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActions",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsList",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference",
    "DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleOutputReference",
]

publication.publish()

def _typecheckingstub__4a6df64b625578221a03c419d4eb7d260ac2daca0dd492a1fd7f09cfc6b2a8cc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    virtual_service_id: builtins.str,
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

def _typecheckingstub__9e954ab9b4ef3413ad6eca8185f946efc2a6e7377a81354ed3193d00d912d061(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52011b689316818dcb4a1e258a91e1fdf107fbe0cbd2a2fd4c8fa1005ff85817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f797c4411e92fec94ab38e691e75b0d9ab773154ded38f4c4cb902ceae64fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30dfa71932680e10825d220590a798cc97d3d32f9fceb06f0c9afffcdd23d35d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    virtual_service_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8728c322537e832a2ddb05b5d60f91638fa6ac51d93ea2cf41c5c9fffcecdd3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5b71a7dc3d05e08bcb2c6cf678a53808826de4e194ccfefb68df3556b7d37a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f3b407b797648492bb0f1a2e845fc1a2b4ed879a3c0fe66b801f6e32151f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d90a7332aa17fdca4a40f16241271bc88a4a558a38ea140f910d31a6bd3e7c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bd8e48972703b543a3eefa969b2a1d8c043dd83cf6b1bca0a57c05a3c218d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ceac2052b2fbc34ec2cdc21dc228a08eb9bf7ce3d35f4b0f11ca7e47955eab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c3b87dd38b7396f03f46a74f595d2e2b66f31ac273aec75b5c1a0ca2912312(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d4ca3fe4ad19f20e749412c57bd2548d10c1c60f7055b9845a226283de0efa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be183f03a4c1dbff6557dbdae796e9c7bd667c21f96b97acee8d7b66716e7051(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2429ff06c1d43b5c2c67aa3200040f9967e7fa1812bb2efc8d10087dbb3ed9f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfaa5aa96aefab9a953fda31bbb08fe934efaf8d19f3d0f6a51a6787a3ffc01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f9dc339f660938bdc0ae091df1f149ce15168d92492e4efc7f9a4453ca130b(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a67b617fe6e444d37210aebd1c9549ba55eda46ef4dbf7e6ad4a051631f7b0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46081b498f5a38e80e94ba139b3a78fbc94056db5e99b92185aa78511ef86d85(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c37f6152b9f4a6474764ba2aa9c278835293e4e766b040c1057c932e91cd80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c44294c2d45be0cf389b6762ccdf31e763025a48b762368e0d0ef3772f9a265(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c0d4965fa52d7ce5d2e5dc4189dc8d988b9169dcfeb7a5fcd1f5508c85b9c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd4177df627f3ab5d05b27a7a1f12615742a031de753296295dd016b09b554d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f59c92730be90df94c1372c48c81afef682151a329fbeeeaa7a059cca3d9f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5f7e81951a6ccd432512d9b152711e203e75d53f0a2145f8190f55ef1b5282(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af3a36e9723efff3ea10507fa7e81303f119e88680d4222f16e2ae4122917d3(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed41f2fbbcd5cf60899cabfde1279c73bf7efaa66e1619e6ed38dc0993d08a56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d35ef14f453df4ba0c68ce07e7327d38e2d625f80f84e7adb4da664734f7de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958a86b368365f369fcfc0139907a097f2e7d72656f3f9f4d41dff4a7bc8a09c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ae95c5f9b03b5c380f110be15cf3193a28bdcbae772e7a75b3fa4054e8df34(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434702be78660f5ba0036cc032f0625d4b03ca77c1aabcbc871f6d6f2513c734(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c8882cc853af7547140accd818cf65fd6c2fbd105802a2b3ed15b1b8f69b7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77cc93e387dcc8804f581fc3e47dfa59c3464c1034de4a80b79e79f3a0795fb(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2493d467a2df6ed0c14532776297219d79e5848de337a48480f63e28f1931d50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3642577a2d0e3024d3aa1eab5858ebc3384330e8e0d3db40a6372f845ce0264(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590cc709dbea46336f220a6194edc19dc985577c7a5af8ad0453e080e4ad4a61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c734326ca4173ed99528872db2edb1d9c03c223194009bb7deac0b230d3a310(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251438806b733093c5750062f3b1ff1062236e7e041b23d4654733dc161e877f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cef89e3816c85d1541a38834262bea4874dd9d81043d236634d8176a2706105(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f62c552102165aef1c280961ff6309b0386f51826f47dfced9a4db02b0fae7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7588281dae5b7bfbaaad4314f0e39246f0cc785540917b500de9bbc5c21a6ff9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d7c4635fa64dfa37b85e5e0f6778de5afc16ce4b33d5725fe69090a027ede2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3642accdc7867057c90d8e720e194626ee1d1cc21f9791098446648f9c8821a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed56f9b35a72f14b6451be2b639f625590269378799ae2896ac7796c6493e7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2653c916881526ed1656ae0a21d3d9e944e00f128a045a1b69c148eb7ebecb3(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9212094ab919f75c21d42ea06429de4e7da6435fa63bbbc438d06c77c3e3bacf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d827870c09af15a04803f01594829c628ae21334a653b781a84d00099187ec5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64e36918c1e726b8d6792d3b98972848abe8ad07cb468cfbdbf98e551535edd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ec122070540be8ef98f8f05762ad1e4e69ef1c4355b182af6fb45cb185b4d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a4408bfa9cab29a85b490d43af4854dfab50afad4ac0afaee02fbc19d208bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c648197de4ee8c2cedeae77d96886aa9661f4a3d29990523c602014b766ab1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b99ecd44a6bec3bc536455695bb853f4bbba4a79ee2bc182c3aed5acfb44bd(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ca198b084525303bd03792b988d6e92004c39b129f51612832c3317abf3921(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba948a1749fe221cdf4c3fc5e52be57a242552edd72aec3f4b5f57fb5a1e889(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d03a9a3aa94f5bc7fc63bbacb9830ca757502d233eea7f4a6e219b1a1595b22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b463c161a865ca0d06cf8f64fd423faa6e58b2e4de8b31267703ee74d4a6eaf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a999647c315359cffcf373d860a38762411d4a7aab89f3707b046ac2fefcb67c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6797c4c725c8e9b2843da6d787f31586817632f6ef8bb88c952ada9aa1109e11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97c3a56bc4d7dbcf5f2ea685089f945237715b4e25c1de70809cd14c8a53d03(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93696e3b6d134b38b1b0f5c69363e35419a1fb8080e37c0c497090247425be3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e550d8af552c2296c04da0956754fa73ba3d7bf77d143077d48886177cdc4f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4789b862f3c049e32d4c68038031eed68d46290cb1ef7164aff07babc152b0d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a8ba24732100a60c32d9b36c45843e89d2554285beee373d7ebcb76e81e2e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba27429db1220f10985aa886e253ef4105e928c331b7c8448b0d88dcbdf9e01f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4a54d34b189570c02ca728b04da53f1b1a0611d451c2b5975e165f77a59caa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0d1b676e9f6051edc3929d7a4dbf69a983a113de1610aa4bebe67c22ba0038(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8efdcf4cda15c8dc945a8c6e36aa5d9a43f85156e7990ea6ce9cf5cfbb7979(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716b89db21bf94820b9164c1f6b2018526843ef57ca75738bd5c66189d039dfc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17369e5f1344e05b0e10994938db62542b36c20cd57d599aa53fedc1866158a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b27e29a59bcc37ab6daa81365a6b99e625d3b70bad32f1be7f2a79b17a24fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f64e274d152c44820a9880942210cffeeb49da2ba3e32b85724f5885807a6d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce188c94c397a83c7f51d37594dec74f1d03581ce74e5ae58acb7f9a3697bfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22b73a4978e6e4e40fcff28cceed397b1d81165cd95073c12d34f7c4966144b(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9a8b07f63764e7fc619867186a4674105593bdbfd16b661bd32ecba5cc282b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e02f8b9fe2def8bbff5b0c08c3c77a8793bdbdcfa6653576c2b4d15ea091751(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3c5a36d66ddce1f59740d6baf8181dc59de42c2c7f28c69d2fe2708e17c7b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399e59c030329f8532619bfd02c763e2efcf46a9b9b598be631e92c1c2c03943(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068a7a2503e617a8d9909b8c6457ee8db4093e768fdf22258400298338a90c80(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbd01822c81614165c87a4e55a571ddf35000b6ed126cb13bcc524ebd2895b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e93389b21d8931a7d6514b23b5c3ca4335775ae0daa126109f5630f21e2efc0(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997866268611f6d3553fce580d3f475d8f68dfb188a1a49d34e066b9e73a78ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8c3a5613d60dcca1632a4983db6ad849b35cd805e26cf2c3c6580d04431447(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a51605b359340d6f4599bb1e536b0b5d03404fd79a33ce30ab5b2e7d1d4526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6917f03c7d9d79d76b5c3e5eab734041fd4932116b2a653812b0a719057c56(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0717c0824155a1301fe6e3eebb370ffdce96b76f7731a94416ad7223d66b047(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b597ba6cb68999d763c2dff28134d6f059b2597aac11fd025847316d5c1314(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfac2e5174649624753f4e61bccf88e2b7674df99cf6ad19ce7dda2cae084bd(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0015e33990665eb440e4ebc6245cec615e1eace92c5a5d06bb8e445ab0c64d0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35b566f5d819ebacc7943015bad11e1ac515ece1f28f72fcba76d2184da69f2(
    value: typing.Optional[DataVcdNsxtAlbVirtualServiceHttpReqRulesRule],
) -> None:
    """Type checking stubs"""
    pass
