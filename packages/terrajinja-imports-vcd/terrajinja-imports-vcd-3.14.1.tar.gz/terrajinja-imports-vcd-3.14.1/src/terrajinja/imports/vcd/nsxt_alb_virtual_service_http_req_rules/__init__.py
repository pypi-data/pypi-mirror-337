'''
# `vcd_nsxt_alb_virtual_service_http_req_rules`

Refer to the Terraform Registry for docs: [`vcd_nsxt_alb_virtual_service_http_req_rules`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules).
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


class NsxtAlbVirtualServiceHttpReqRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules vcd_nsxt_alb_virtual_service_http_req_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRule", typing.Dict[builtins.str, typing.Any]]]],
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
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules vcd_nsxt_alb_virtual_service_http_req_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#rule NsxtAlbVirtualServiceHttpReqRules#rule}
        :param virtual_service_id: NSX-T ALB Virtual Service ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#virtual_service_id NsxtAlbVirtualServiceHttpReqRules#virtual_service_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#id NsxtAlbVirtualServiceHttpReqRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81bf14091006234e0d88fb09de46ee4fe289147e8c940d5a0933844b4cf7552c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtAlbVirtualServiceHttpReqRulesConfig(
            rule=rule,
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
        '''Generates CDKTF code for importing a NsxtAlbVirtualServiceHttpReqRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtAlbVirtualServiceHttpReqRules to import.
        :param import_from_id: The id of the existing NsxtAlbVirtualServiceHttpReqRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtAlbVirtualServiceHttpReqRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72149f7b4a0d0df0445c97df24d29e08049ab752b33d30cfb8ebfd9636291a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7efcb0fe6f854f792f90d993ea6ab3b4421e6efcfb931e65e65027b92185897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

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
    def rule(self) -> "NsxtAlbVirtualServiceHttpReqRulesRuleList":
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRule"]]], jsii.get(self, "ruleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__52bcc99970feb03c802d0bbd69f75260ff7a7b04fe833260bed0257893ada15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="virtualServiceId")
    def virtual_service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceId"))

    @virtual_service_id.setter
    def virtual_service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72dab1a8ab0bde6005a7b9b62195b1cd525683751527e4adfdbfc0d751b127b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceId", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "rule": "rule",
        "virtual_service_id": "virtualServiceId",
        "id": "id",
    },
)
class NsxtAlbVirtualServiceHttpReqRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRule", typing.Dict[builtins.str, typing.Any]]]],
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
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#rule NsxtAlbVirtualServiceHttpReqRules#rule}
        :param virtual_service_id: NSX-T ALB Virtual Service ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#virtual_service_id NsxtAlbVirtualServiceHttpReqRules#virtual_service_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#id NsxtAlbVirtualServiceHttpReqRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a20e6bbca4726ca462d27992e33d27939b7b5dbd906e23f3ec8952455189f5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument virtual_service_id", value=virtual_service_id, expected_type=type_hints["virtual_service_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
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
    def rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#rule NsxtAlbVirtualServiceHttpReqRules#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRule"]], result)

    @builtins.property
    def virtual_service_id(self) -> builtins.str:
        '''NSX-T ALB Virtual Service ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#virtual_service_id NsxtAlbVirtualServiceHttpReqRules#virtual_service_id}
        '''
        result = self._values.get("virtual_service_id")
        assert result is not None, "Required property 'virtual_service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#id NsxtAlbVirtualServiceHttpReqRules#id}.

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
        return "NsxtAlbVirtualServiceHttpReqRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRule",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "match_criteria": "matchCriteria",
        "name": "name",
        "active": "active",
        "logging": "logging",
    },
)
class NsxtAlbVirtualServiceHttpReqRulesRule:
    def __init__(
        self,
        *,
        actions: typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleActions", typing.Dict[builtins.str, typing.Any]],
        match_criteria: typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#actions NsxtAlbVirtualServiceHttpReqRules#actions}
        :param match_criteria: match_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#match_criteria NsxtAlbVirtualServiceHttpReqRules#match_criteria}
        :param name: Name of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        :param active: Defines if the rule is active or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#active NsxtAlbVirtualServiceHttpReqRules#active}
        :param logging: Defines whether to enable logging with headers on rule match or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#logging NsxtAlbVirtualServiceHttpReqRules#logging}
        '''
        if isinstance(actions, dict):
            actions = NsxtAlbVirtualServiceHttpReqRulesRuleActions(**actions)
        if isinstance(match_criteria, dict):
            match_criteria = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria(**match_criteria)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2555247980b22da56ed1e9a5bcfe9564df4746b92bbbcacc74c774263cc306)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument match_criteria", value=match_criteria, expected_type=type_hints["match_criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "match_criteria": match_criteria,
            "name": name,
        }
        if active is not None:
            self._values["active"] = active
        if logging is not None:
            self._values["logging"] = logging

    @builtins.property
    def actions(self) -> "NsxtAlbVirtualServiceHttpReqRulesRuleActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#actions NsxtAlbVirtualServiceHttpReqRules#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleActions", result)

    @builtins.property
    def match_criteria(self) -> "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria":
        '''match_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#match_criteria NsxtAlbVirtualServiceHttpReqRules#match_criteria}
        '''
        result = self._values.get("match_criteria")
        assert result is not None, "Required property 'match_criteria' is missing"
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines if the rule is active or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#active NsxtAlbVirtualServiceHttpReqRules#active}
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether to enable logging with headers on rule match or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#logging NsxtAlbVirtualServiceHttpReqRules#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "modify_header": "modifyHeader",
        "redirect": "redirect",
        "rewrite_url": "rewriteUrl",
    },
)
class NsxtAlbVirtualServiceHttpReqRulesRuleActions:
    def __init__(
        self,
        *,
        modify_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redirect: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        rewrite_url: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param modify_header: modify_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#modify_header NsxtAlbVirtualServiceHttpReqRules#modify_header}
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#redirect NsxtAlbVirtualServiceHttpReqRules#redirect}
        :param rewrite_url: rewrite_url block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#rewrite_url NsxtAlbVirtualServiceHttpReqRules#rewrite_url}
        '''
        if isinstance(redirect, dict):
            redirect = NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect(**redirect)
        if isinstance(rewrite_url, dict):
            rewrite_url = NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl(**rewrite_url)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247ecc80d5c4a1f0402162b9de1d28a958fac55ac36cfeedd3a57be0e8e4a2ee)
            check_type(argname="argument modify_header", value=modify_header, expected_type=type_hints["modify_header"])
            check_type(argname="argument redirect", value=redirect, expected_type=type_hints["redirect"])
            check_type(argname="argument rewrite_url", value=rewrite_url, expected_type=type_hints["rewrite_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if modify_header is not None:
            self._values["modify_header"] = modify_header
        if redirect is not None:
            self._values["redirect"] = redirect
        if rewrite_url is not None:
            self._values["rewrite_url"] = rewrite_url

    @builtins.property
    def modify_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader"]]]:
        '''modify_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#modify_header NsxtAlbVirtualServiceHttpReqRules#modify_header}
        '''
        result = self._values.get("modify_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader"]]], result)

    @builtins.property
    def redirect(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect"]:
        '''redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#redirect NsxtAlbVirtualServiceHttpReqRules#redirect}
        '''
        result = self._values.get("redirect")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect"], result)

    @builtins.property
    def rewrite_url(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl"]:
        '''rewrite_url block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#rewrite_url NsxtAlbVirtualServiceHttpReqRules#rewrite_url}
        '''
        result = self._values.get("rewrite_url")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name", "value": "value"},
)
class NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: One of the following HTTP header actions. Options - ADD, REMOVE, REPLACE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#action NsxtAlbVirtualServiceHttpReqRules#action}
        :param name: HTTP header name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        :param value: HTTP header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#value NsxtAlbVirtualServiceHttpReqRules#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0a50d50b8721f8b54e8bd399054d8398f763ecc245980b2110d53e0e76a144)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def action(self) -> builtins.str:
        '''One of the following HTTP header actions. Options - ADD, REMOVE, REPLACE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#action NsxtAlbVirtualServiceHttpReqRules#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''HTTP header name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''HTTP header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#value NsxtAlbVirtualServiceHttpReqRules#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cba12c0c5205ac37e56105f6fab0dd862d7c5a4f87d120ab8e089a9e70981169)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0f63ffd8f3d299c660b8c4c302f170977e60f5d52d1c6d6c6eb4a987538917)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42b02b58fa41fb40504188602ad0ff0ad97058dffd1971ce1dd4facc72194de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ce5204b67fa8fadc4b07e20668cfc49fcd537397b8239deeb163868c12d6b58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e2a3ca6763d58158f4faf838ba886bd5846ffadbe2ad1ffdee8a10fa081ac78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140123200f3ad9a0d3442483fd838d7bd904e1f7f5d3f7f166413a83194b1b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2289d253195cc4a61d1e651bc1e3f098c1628ab7b4ae81aac5333df19abe56c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524de7827433dd38fa9c83027f8f2b4a5ed4fd7d9c2eac953f55b1ddea0721d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af42b24238e6f6c7f7c570920520b2bfab512a9323135f38e21b1bd38582ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d690564f19a09989926ab96a75a4a4d6661aa4d42a9ba14ca8d5f2fdb3aa9a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531789d21cd0ddf2ea81a5ba12af40ee8cdb79d6778e085be5c31f330975ffa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__103d783f23a36673c978f74174720bf8507f05d0423fc37c7ba25a4841c8bf10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putModifyHeader")
    def put_modify_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350fa2c33df7b3ccb8c4e27d9880d9596b7285aa9a6acee965b44812a5317c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putModifyHeader", [value]))

    @jsii.member(jsii_name="putRedirect")
    def put_redirect(
        self,
        *,
        protocol: builtins.str,
        status_code: jsii.Number,
        host: typing.Optional[builtins.str] = None,
        keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol: HTTP or HTTPS protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#protocol NsxtAlbVirtualServiceHttpReqRules#protocol}
        :param status_code: One of the redirect status codes - 301, 302, 307. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#status_code NsxtAlbVirtualServiceHttpReqRules#status_code}
        :param host: Host to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#host NsxtAlbVirtualServiceHttpReqRules#host}
        :param keep_query: Should the query part be preserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#keep_query NsxtAlbVirtualServiceHttpReqRules#keep_query}
        :param path: Path to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#path NsxtAlbVirtualServiceHttpReqRules#path}
        :param port: Port to which redirect the request. Default is 80 for HTTP and 443 for HTTPS protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#port NsxtAlbVirtualServiceHttpReqRules#port}
        '''
        value = NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect(
            protocol=protocol,
            status_code=status_code,
            host=host,
            keep_query=keep_query,
            path=path,
            port=port,
        )

        return typing.cast(None, jsii.invoke(self, "putRedirect", [value]))

    @jsii.member(jsii_name="putRewriteUrl")
    def put_rewrite_url(
        self,
        *,
        existing_path: builtins.str,
        host_header: builtins.str,
        keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param existing_path: Path to use for the rewritten URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#existing_path NsxtAlbVirtualServiceHttpReqRules#existing_path}
        :param host_header: Host to use for the rewritten URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#host_header NsxtAlbVirtualServiceHttpReqRules#host_header}
        :param keep_query: Whether or not to keep the existing query string when rewriting the URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#keep_query NsxtAlbVirtualServiceHttpReqRules#keep_query}
        :param query: Query string to use or append to the existing query string in the rewritten URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#query NsxtAlbVirtualServiceHttpReqRules#query}
        '''
        value = NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl(
            existing_path=existing_path,
            host_header=host_header,
            keep_query=keep_query,
            query=query,
        )

        return typing.cast(None, jsii.invoke(self, "putRewriteUrl", [value]))

    @jsii.member(jsii_name="resetModifyHeader")
    def reset_modify_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifyHeader", []))

    @jsii.member(jsii_name="resetRedirect")
    def reset_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirect", []))

    @jsii.member(jsii_name="resetRewriteUrl")
    def reset_rewrite_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewriteUrl", []))

    @builtins.property
    @jsii.member(jsii_name="modifyHeader")
    def modify_header(
        self,
    ) -> NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList:
        return typing.cast(NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList, jsii.get(self, "modifyHeader"))

    @builtins.property
    @jsii.member(jsii_name="redirect")
    def redirect(
        self,
    ) -> "NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference", jsii.get(self, "redirect"))

    @builtins.property
    @jsii.member(jsii_name="rewriteUrl")
    def rewrite_url(
        self,
    ) -> "NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference", jsii.get(self, "rewriteUrl"))

    @builtins.property
    @jsii.member(jsii_name="modifyHeaderInput")
    def modify_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]]], jsii.get(self, "modifyHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectInput")
    def redirect_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect"], jsii.get(self, "redirectInput"))

    @builtins.property
    @jsii.member(jsii_name="rewriteUrlInput")
    def rewrite_url_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl"], jsii.get(self, "rewriteUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActions]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f210fc8169ce5aae653540aacce516355cb2075a07cf8ccdd501f1d38b8503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "status_code": "statusCode",
        "host": "host",
        "keep_query": "keepQuery",
        "path": "path",
        "port": "port",
    },
)
class NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect:
    def __init__(
        self,
        *,
        protocol: builtins.str,
        status_code: jsii.Number,
        host: typing.Optional[builtins.str] = None,
        keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol: HTTP or HTTPS protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#protocol NsxtAlbVirtualServiceHttpReqRules#protocol}
        :param status_code: One of the redirect status codes - 301, 302, 307. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#status_code NsxtAlbVirtualServiceHttpReqRules#status_code}
        :param host: Host to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#host NsxtAlbVirtualServiceHttpReqRules#host}
        :param keep_query: Should the query part be preserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#keep_query NsxtAlbVirtualServiceHttpReqRules#keep_query}
        :param path: Path to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#path NsxtAlbVirtualServiceHttpReqRules#path}
        :param port: Port to which redirect the request. Default is 80 for HTTP and 443 for HTTPS protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#port NsxtAlbVirtualServiceHttpReqRules#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b7a3ea52fac9f7cb5603a5c98eb6dbc798e559e14f0a627af0b3284f226317f)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument keep_query", value=keep_query, expected_type=type_hints["keep_query"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "protocol": protocol,
            "status_code": status_code,
        }
        if host is not None:
            self._values["host"] = host
        if keep_query is not None:
            self._values["keep_query"] = keep_query
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def protocol(self) -> builtins.str:
        '''HTTP or HTTPS protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#protocol NsxtAlbVirtualServiceHttpReqRules#protocol}
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status_code(self) -> jsii.Number:
        '''One of the redirect status codes - 301, 302, 307.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#status_code NsxtAlbVirtualServiceHttpReqRules#status_code}
        '''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host to which redirect the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#host NsxtAlbVirtualServiceHttpReqRules#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the query part be preserved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#keep_query NsxtAlbVirtualServiceHttpReqRules#keep_query}
        '''
        result = self._values.get("keep_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to which redirect the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#path NsxtAlbVirtualServiceHttpReqRules#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Port to which redirect the request. Default is 80 for HTTP and 443 for HTTPS protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#port NsxtAlbVirtualServiceHttpReqRules#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12cfe3d4d7d16ffe49e71bd2a9ddb6e4a55b96e0314efbbbd2a54f47a60e46b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetKeepQuery")
    def reset_keep_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepQuery", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="keepQueryInput")
    def keep_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592c2d0365fe0d3290b3b4f467c4c0e8dab23e6ab308eb48639e6ab2b8994df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="keepQuery")
    def keep_query(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepQuery"))

    @keep_query.setter
    def keep_query(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a797b3e398bc35806c89560bffc2d68b133d9b09344d31e262b3bf8c389f163c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepQuery", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce68b9a953cc2012ff017439bfd45cf210b9ddce4a638b1474c0fec162877005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0efc0183c5bd87033e3ab290423323a7f7ed894e2bc673678c554f1db380358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569faba5618504ba7150799db5fd17a79c4fb02893d910bf267e6877b73ae0ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f6e44820c8a8805431328af9c127ffd7a5ff9063542857d1e55b1f8d662f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997d84a8a23ffe830ecdc3edd278e0c7aa1bc6d6edd598498639d8be662601c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl",
    jsii_struct_bases=[],
    name_mapping={
        "existing_path": "existingPath",
        "host_header": "hostHeader",
        "keep_query": "keepQuery",
        "query": "query",
    },
)
class NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl:
    def __init__(
        self,
        *,
        existing_path: builtins.str,
        host_header: builtins.str,
        keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param existing_path: Path to use for the rewritten URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#existing_path NsxtAlbVirtualServiceHttpReqRules#existing_path}
        :param host_header: Host to use for the rewritten URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#host_header NsxtAlbVirtualServiceHttpReqRules#host_header}
        :param keep_query: Whether or not to keep the existing query string when rewriting the URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#keep_query NsxtAlbVirtualServiceHttpReqRules#keep_query}
        :param query: Query string to use or append to the existing query string in the rewritten URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#query NsxtAlbVirtualServiceHttpReqRules#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c4cf92adbe54074075ec817e58f172b9ee3cf218039f292510293faf0f9a83)
            check_type(argname="argument existing_path", value=existing_path, expected_type=type_hints["existing_path"])
            check_type(argname="argument host_header", value=host_header, expected_type=type_hints["host_header"])
            check_type(argname="argument keep_query", value=keep_query, expected_type=type_hints["keep_query"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "existing_path": existing_path,
            "host_header": host_header,
        }
        if keep_query is not None:
            self._values["keep_query"] = keep_query
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def existing_path(self) -> builtins.str:
        '''Path to use for the rewritten URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#existing_path NsxtAlbVirtualServiceHttpReqRules#existing_path}
        '''
        result = self._values.get("existing_path")
        assert result is not None, "Required property 'existing_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_header(self) -> builtins.str:
        '''Host to use for the rewritten URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#host_header NsxtAlbVirtualServiceHttpReqRules#host_header}
        '''
        result = self._values.get("host_header")
        assert result is not None, "Required property 'host_header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keep_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to keep the existing query string when rewriting the URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#keep_query NsxtAlbVirtualServiceHttpReqRules#keep_query}
        '''
        result = self._values.get("keep_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Query string to use or append to the existing query string in the rewritten URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#query NsxtAlbVirtualServiceHttpReqRules#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__583efc00b89e892ea51a1231e3fbf5a34bf5f52dbb83a9f5c63e932706663020)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeepQuery")
    def reset_keep_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepQuery", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="existingPathInput")
    def existing_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "existingPathInput"))

    @builtins.property
    @jsii.member(jsii_name="hostHeaderInput")
    def host_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="keepQueryInput")
    def keep_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="existingPath")
    def existing_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "existingPath"))

    @existing_path.setter
    def existing_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39d8cc04ac8301e1b6aa161637d554312680b317805d2863dd1004d8f193f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "existingPath", value)

    @builtins.property
    @jsii.member(jsii_name="hostHeader")
    def host_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostHeader"))

    @host_header.setter
    def host_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2ba3a554f416be1cf047ffe79a49350540113914c1fa456a7ebaae8daef7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostHeader", value)

    @builtins.property
    @jsii.member(jsii_name="keepQuery")
    def keep_query(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepQuery"))

    @keep_query.setter
    def keep_query(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0198b8433e88b7cd1252c4519cde8116bac2fdc1c8ba26df99b02184309c47d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepQuery", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c95e680bbf94e3aa363e8eb974a3f9a1795403f0c98749b5b05f174072173d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5d25607f249a189b4aa63d1322e39b5026d9a852e6ba2affecd3eb34742842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpReqRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b104e8647548a9116594d9630753d8e2ec17e566a6a2197fae378f3ab9707411)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpReqRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d21cfa99c45ea9932a2641987ad1800abc76b12dc000d0207cd24f5e355f7c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172d59e872c31baffee70a49e8fc86e98d7779fac83910ca177f06d5911d336f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a48bfe14b554ebb37ae797a03288d9df0828f541a4f9f18c29e08041b25f692)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c7a2ee747f7ee4fcacc517648c8c1417356dd360f16260ef71d540a0e914376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59cf19749697bb0e035648fae0bd37893215b0d951f5c3b42cb27a6ee9c34b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "client_ip_address": "clientIpAddress",
        "cookie": "cookie",
        "http_methods": "httpMethods",
        "path": "path",
        "protocol_type": "protocolType",
        "query": "query",
        "request_headers": "requestHeaders",
        "service_ports": "servicePorts",
    },
)
class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria:
    def __init__(
        self,
        *,
        client_ip_address: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        cookie: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_methods: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath", typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_ports: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip_address: client_ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#client_ip_address NsxtAlbVirtualServiceHttpReqRules#client_ip_address}
        :param cookie: cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#cookie NsxtAlbVirtualServiceHttpReqRules#cookie}
        :param http_methods: http_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#http_methods NsxtAlbVirtualServiceHttpReqRules#http_methods}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#path NsxtAlbVirtualServiceHttpReqRules#path}
        :param protocol_type: Protocol to match - 'HTTP' or 'HTTPS'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#protocol_type NsxtAlbVirtualServiceHttpReqRules#protocol_type}
        :param query: HTTP request query strings to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#query NsxtAlbVirtualServiceHttpReqRules#query}
        :param request_headers: request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#request_headers NsxtAlbVirtualServiceHttpReqRules#request_headers}
        :param service_ports: service_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#service_ports NsxtAlbVirtualServiceHttpReqRules#service_ports}
        '''
        if isinstance(client_ip_address, dict):
            client_ip_address = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress(**client_ip_address)
        if isinstance(cookie, dict):
            cookie = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie(**cookie)
        if isinstance(http_methods, dict):
            http_methods = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods(**http_methods)
        if isinstance(path, dict):
            path = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath(**path)
        if isinstance(service_ports, dict):
            service_ports = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts(**service_ports)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821752d0baa87316e03fec01c4829f7d873bc8dace66e591363abfbab4e6f422)
            check_type(argname="argument client_ip_address", value=client_ip_address, expected_type=type_hints["client_ip_address"])
            check_type(argname="argument cookie", value=cookie, expected_type=type_hints["cookie"])
            check_type(argname="argument http_methods", value=http_methods, expected_type=type_hints["http_methods"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument request_headers", value=request_headers, expected_type=type_hints["request_headers"])
            check_type(argname="argument service_ports", value=service_ports, expected_type=type_hints["service_ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_ip_address is not None:
            self._values["client_ip_address"] = client_ip_address
        if cookie is not None:
            self._values["cookie"] = cookie
        if http_methods is not None:
            self._values["http_methods"] = http_methods
        if path is not None:
            self._values["path"] = path
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if query is not None:
            self._values["query"] = query
        if request_headers is not None:
            self._values["request_headers"] = request_headers
        if service_ports is not None:
            self._values["service_ports"] = service_ports

    @builtins.property
    def client_ip_address(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress"]:
        '''client_ip_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#client_ip_address NsxtAlbVirtualServiceHttpReqRules#client_ip_address}
        '''
        result = self._values.get("client_ip_address")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress"], result)

    @builtins.property
    def cookie(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie"]:
        '''cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#cookie NsxtAlbVirtualServiceHttpReqRules#cookie}
        '''
        result = self._values.get("cookie")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie"], result)

    @builtins.property
    def http_methods(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods"]:
        '''http_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#http_methods NsxtAlbVirtualServiceHttpReqRules#http_methods}
        '''
        result = self._values.get("http_methods")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods"], result)

    @builtins.property
    def path(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#path NsxtAlbVirtualServiceHttpReqRules#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath"], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''Protocol to match - 'HTTP' or 'HTTPS'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#protocol_type NsxtAlbVirtualServiceHttpReqRules#protocol_type}
        '''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HTTP request query strings to match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#query NsxtAlbVirtualServiceHttpReqRules#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def request_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders"]]]:
        '''request_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#request_headers NsxtAlbVirtualServiceHttpReqRules#request_headers}
        '''
        result = self._values.get("request_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders"]]], result)

    @builtins.property
    def service_ports(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts"]:
        '''service_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#service_ports NsxtAlbVirtualServiceHttpReqRules#service_ports}
        '''
        result = self._values.get("service_ports")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "ip_addresses": "ipAddresses"},
)
class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        ip_addresses: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param ip_addresses: A set of IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#ip_addresses NsxtAlbVirtualServiceHttpReqRules#ip_addresses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114dad572b16e4391d289731f08e9015ad32db69b95205758db64c7828743812)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "ip_addresses": ip_addresses,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_addresses(self) -> typing.List[builtins.str]:
        '''A set of IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#ip_addresses NsxtAlbVirtualServiceHttpReqRules#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        assert result is not None, "Required property 'ip_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8736ce2d39ac2df1856afa006d55a17421d7570b9334a90225279f33882589c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a43d3d0fc146ad10b8f4b0a9f5b12a756fad2adce1ffb7faceb63410c0d3e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6e7636cb3663b25eb8440fe8ea5a5dc2a58210010e309f381a3c02db0b066f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8e615268fca8263e264adb3b0a08753f0f37299e7ea85d43cc530b8d89bf93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "name": "name", "value": "value"},
)
class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param criteria: Criteria to use for matching cookies in the HTTP request. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param name: Name of the HTTP cookie whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        :param value: String values to match for an HTTP cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#value NsxtAlbVirtualServiceHttpReqRules#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6e7a788559aaaa51b4a005ba94d6330b4c87e2669e9ca72e374ede75e2f5fa)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "name": name,
            "value": value,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for matching cookies in the HTTP request.

        Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the HTTP cookie whose value is to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''String values to match for an HTTP cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#value NsxtAlbVirtualServiceHttpReqRules#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1992f84fda1876fcbdc992490dc250d6ae2753f6ce33ef6eeb79de066fed52bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e908659cfb95e84e04031dce9da1047a5ed8f808c9f06d5a8ca1e22acbd9ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c488658c406f689a413406908ef704b73c5e73c5393d3366a55c3fd3ab0459f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740e9fe772a214b17187e022db3f9951f441d3aaaa19cb58bb68550e7ce85a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc6f94c7105a94805f3c20055709d198d8b554a3e0a8df51c19f6f9976e741f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "methods": "methods"},
)
class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        methods: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param methods: HTTP methods to match. Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#methods NsxtAlbVirtualServiceHttpReqRules#methods}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a537e69d351a21541a759d39d5c4c902e9dc6263f33d1f24c4cf25478c52864)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "methods": methods,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def methods(self) -> typing.List[builtins.str]:
        '''HTTP methods to match.

        Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#methods NsxtAlbVirtualServiceHttpReqRules#methods}
        '''
        result = self._values.get("methods")
        assert result is not None, "Required property 'methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a893ef4de837be92333f7d941bdb172cb66b757f285b7d03bb0a755672c7592)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f6c98044336616a5cc88b5714651e7fd9171546a972dd14148ed37112faf5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84e8c4065dcd79e83d6a76150100503ed9b8291a2790fd3c0739436716289e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39701de264221891e883db084986d12f45e6598bcf65daa6c704979a76e430d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe8d87c02f6d091d02e85be6712b7c816ee3cee0c4fc2b40dbad0ae2c46ae80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientIpAddress")
    def put_client_ip_address(
        self,
        *,
        criteria: builtins.str,
        ip_addresses: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param ip_addresses: A set of IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#ip_addresses NsxtAlbVirtualServiceHttpReqRules#ip_addresses}
        '''
        value = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress(
            criteria=criteria, ip_addresses=ip_addresses
        )

        return typing.cast(None, jsii.invoke(self, "putClientIpAddress", [value]))

    @jsii.member(jsii_name="putCookie")
    def put_cookie(
        self,
        *,
        criteria: builtins.str,
        name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param criteria: Criteria to use for matching cookies in the HTTP request. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param name: Name of the HTTP cookie whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        :param value: String values to match for an HTTP cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#value NsxtAlbVirtualServiceHttpReqRules#value}
        '''
        value_ = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie(
            criteria=criteria, name=name, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putCookie", [value_]))

    @jsii.member(jsii_name="putHttpMethods")
    def put_http_methods(
        self,
        *,
        criteria: builtins.str,
        methods: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param methods: HTTP methods to match. Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#methods NsxtAlbVirtualServiceHttpReqRules#methods}
        '''
        value = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods(
            criteria=criteria, methods=methods
        )

        return typing.cast(None, jsii.invoke(self, "putHttpMethods", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(
        self,
        *,
        criteria: builtins.str,
        paths: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching the path in the HTTP request URI. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param paths: String values to match the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#paths NsxtAlbVirtualServiceHttpReqRules#paths}
        '''
        value = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath(
            criteria=criteria, paths=paths
        )

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putRequestHeaders")
    def put_request_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684f3ad667324ed7379e8e70630d3a19568d55791330485529fff6f376916d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaders", [value]))

    @jsii.member(jsii_name="putServicePorts")
    def put_service_ports(
        self,
        *,
        criteria: builtins.str,
        ports: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param ports: A set of TCP ports. Allowed values are 1-65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#ports NsxtAlbVirtualServiceHttpReqRules#ports}
        '''
        value = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts(
            criteria=criteria, ports=ports
        )

        return typing.cast(None, jsii.invoke(self, "putServicePorts", [value]))

    @jsii.member(jsii_name="resetClientIpAddress")
    def reset_client_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientIpAddress", []))

    @jsii.member(jsii_name="resetCookie")
    def reset_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookie", []))

    @jsii.member(jsii_name="resetHttpMethods")
    def reset_http_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethods", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetProtocolType")
    def reset_protocol_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolType", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetRequestHeaders")
    def reset_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaders", []))

    @jsii.member(jsii_name="resetServicePorts")
    def reset_service_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePorts", []))

    @builtins.property
    @jsii.member(jsii_name="clientIpAddress")
    def client_ip_address(
        self,
    ) -> NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference, jsii.get(self, "clientIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="cookie")
    def cookie(
        self,
    ) -> NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference, jsii.get(self, "cookie"))

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(
        self,
    ) -> NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference, jsii.get(self, "httpMethods"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(
        self,
    ) -> "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(
        self,
    ) -> "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList":
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList", jsii.get(self, "requestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="servicePorts")
    def service_ports(
        self,
    ) -> "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference", jsii.get(self, "servicePorts"))

    @builtins.property
    @jsii.member(jsii_name="clientIpAddressInput")
    def client_ip_address_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress], jsii.get(self, "clientIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieInput")
    def cookie_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie], jsii.get(self, "cookieInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodsInput")
    def http_methods_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods], jsii.get(self, "httpMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath"], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolTypeInput")
    def protocol_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersInput")
    def request_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders"]]], jsii.get(self, "requestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePortsInput")
    def service_ports_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts"], jsii.get(self, "servicePortsInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolType"))

    @protocol_type.setter
    def protocol_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42aad28817739af466f6a08ca28a3430871b51d7ea8a58a44b89d2c44a12e0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "query"))

    @query.setter
    def query(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb54749976ebf4dfa5bccf796ba2bf473cfec892d0d9e1e8587642e38a0c0c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8aa30ac02f38fc67c6d6fa9fcfb5a4b25a81558797c04ecd27b68c181440d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "paths": "paths"},
)
class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        paths: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching the path in the HTTP request URI. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param paths: String values to match the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#paths NsxtAlbVirtualServiceHttpReqRules#paths}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96d9d4f7d75cebb0c84f88e504c6320a3046893cc3b98454ac1026d4cf3f95f)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "paths": paths,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for matching the path in the HTTP request URI.

        Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''String values to match the path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#paths NsxtAlbVirtualServiceHttpReqRules#paths}
        '''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbb2bc459d04eefdcec470ae6d504d1cf3542daaff132c621e3a5cbc610b3cfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f40e8a34b3c08b45845d83159e354458184d183bea5948e99b82a9c297201b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0f251723080ed853cc2da2577d9033ed5318940575c631aec56b5c7c735271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8eba5fa1b013ca72749aebbe75c3cab8b1c8bd9f1bcc7ebd22292f3ecb1ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "name": "name", "values": "values"},
)
class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching headers and cookies in the HTTP request amd response. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param name: Name of the HTTP header whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        :param values: String values to match for an HTTP header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#values NsxtAlbVirtualServiceHttpReqRules#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373c36ba2568c62f2002027bd1c3ffd608cb72c85b3fae3c89a5864148045be7)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "name": name,
            "values": values,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for matching headers and cookies in the HTTP request amd response.

        Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the HTTP header whose value is to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#name NsxtAlbVirtualServiceHttpReqRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''String values to match for an HTTP header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#values NsxtAlbVirtualServiceHttpReqRules#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f4a20df618de3a54755a5aa27cce169a5bb3757014bb66d938134bf9794861e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba9eb871272e71b5f9948ec07dafc36007b7890bd2b36217e3e4643713ebb2d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f8048913b08f37342ecd86cbe9e60c2444e9bcf37e1c1a5f8080e52db6372c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5da9f25fcdb4aeab81dbcbced2ef7f6befa6ce2d5c60d4fa9823bc6687012b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5d1e4a46a73a869d41fd51c6855f56da0d62990fde6449c823c273c6ffd9d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abef442bcac123004bd10b09d42a0fa0730a1999b30e97436d957225e6345ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c8a7590b62f2f4df6ea0226b687ada102252dd654a5bba758d30ad7895fc70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce198c7bd54964d67af2639e2f69ed0beda26a827d9c41530bdc157c5722dd3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8a3d85988debec651115fbc11ad02481fc1bb90fe0b73b24a42fad11db444b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f984c2c693e082fc02a3b82905df2ff2fded1796301aa261c2c9153731c6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd482bb0fd1958ebe691184de33525fa52aced2e4a0957b87a4ba890e20a0b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "ports": "ports"},
)
class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        ports: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        :param ports: A set of TCP ports. Allowed values are 1-65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#ports NsxtAlbVirtualServiceHttpReqRules#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fcb623a14e1a68d7830b4706b00e44e6245e2b35ce8057ad7d6aab706d738bc)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "ports": ports,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#criteria NsxtAlbVirtualServiceHttpReqRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.List[jsii.Number]:
        '''A set of TCP ports. Allowed values are 1-65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#ports NsxtAlbVirtualServiceHttpReqRules#ports}
        '''
        result = self._values.get("ports")
        assert result is not None, "Required property 'ports' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67b49ea3cb58257e46148b0a056b2efd323adc5c6c652f8ce0e3de4616c3dc88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6287ca46857016e8d2ff69a61d436784b270e482e02c29922ab64a60eca01c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e320197d1f0f29cbd40043d2657862a31667fbe5a98b4e8bbb93b41d85f324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0217fd64fac41635c5d5714e7adc67614b55e1890353336989e701d9503b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpReqRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpReqRules.NsxtAlbVirtualServiceHttpReqRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8474b50825601ec5e05bfafd37ebc6a0e13784c637205132d2e9f6fa0fa1745e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        modify_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        redirect: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
        rewrite_url: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param modify_header: modify_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#modify_header NsxtAlbVirtualServiceHttpReqRules#modify_header}
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#redirect NsxtAlbVirtualServiceHttpReqRules#redirect}
        :param rewrite_url: rewrite_url block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#rewrite_url NsxtAlbVirtualServiceHttpReqRules#rewrite_url}
        '''
        value = NsxtAlbVirtualServiceHttpReqRulesRuleActions(
            modify_header=modify_header, redirect=redirect, rewrite_url=rewrite_url
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putMatchCriteria")
    def put_match_criteria(
        self,
        *,
        client_ip_address: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
        cookie: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie, typing.Dict[builtins.str, typing.Any]]] = None,
        http_methods: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath, typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_ports: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip_address: client_ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#client_ip_address NsxtAlbVirtualServiceHttpReqRules#client_ip_address}
        :param cookie: cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#cookie NsxtAlbVirtualServiceHttpReqRules#cookie}
        :param http_methods: http_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#http_methods NsxtAlbVirtualServiceHttpReqRules#http_methods}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#path NsxtAlbVirtualServiceHttpReqRules#path}
        :param protocol_type: Protocol to match - 'HTTP' or 'HTTPS'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#protocol_type NsxtAlbVirtualServiceHttpReqRules#protocol_type}
        :param query: HTTP request query strings to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#query NsxtAlbVirtualServiceHttpReqRules#query}
        :param request_headers: request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#request_headers NsxtAlbVirtualServiceHttpReqRules#request_headers}
        :param service_ports: service_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_req_rules#service_ports NsxtAlbVirtualServiceHttpReqRules#service_ports}
        '''
        value = NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria(
            client_ip_address=client_ip_address,
            cookie=cookie,
            http_methods=http_methods,
            path=path,
            protocol_type=protocol_type,
            query=query,
            request_headers=request_headers,
            service_ports=service_ports,
        )

        return typing.cast(None, jsii.invoke(self, "putMatchCriteria", [value]))

    @jsii.member(jsii_name="resetActive")
    def reset_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActive", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> NsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="matchCriteria")
    def match_criteria(
        self,
    ) -> NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference, jsii.get(self, "matchCriteria"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActions]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="activeInput")
    def active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="matchCriteriaInput")
    def match_criteria_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria], jsii.get(self, "matchCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "active"))

    @active.setter
    def active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129b00a7e7462d36c10f56c1290f40a64026daa62342ba1c01d7143999042592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value)

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logging"))

    @logging.setter
    def logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91d8dbdbe03bd2e99924bf58d9b605c330edf63ff738bbaedfc9e359f2eac26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6a05a01f28d4c8d3f0b91bdc53ce85045c6136d913f1c43d1a3b2407fa9691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ecea58dbdcf76126748a176aeff0995b6370de3e8b7e8c4a19df103504b954d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtAlbVirtualServiceHttpReqRules",
    "NsxtAlbVirtualServiceHttpReqRulesConfig",
    "NsxtAlbVirtualServiceHttpReqRulesRule",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActions",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderList",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeaderOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActionsOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirectOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl",
    "NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrlOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleList",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddressOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookieOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethodsOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPathOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersList",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeadersOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts",
    "NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePortsOutputReference",
    "NsxtAlbVirtualServiceHttpReqRulesRuleOutputReference",
]

publication.publish()

def _typecheckingstub__81bf14091006234e0d88fb09de46ee4fe289147e8c940d5a0933844b4cf7552c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRule, typing.Dict[builtins.str, typing.Any]]]],
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

def _typecheckingstub__f72149f7b4a0d0df0445c97df24d29e08049ab752b33d30cfb8ebfd9636291a4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7efcb0fe6f854f792f90d993ea6ab3b4421e6efcfb931e65e65027b92185897(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bcc99970feb03c802d0bbd69f75260ff7a7b04fe833260bed0257893ada15a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72dab1a8ab0bde6005a7b9b62195b1cd525683751527e4adfdbfc0d751b127b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a20e6bbca4726ca462d27992e33d27939b7b5dbd906e23f3ec8952455189f5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRule, typing.Dict[builtins.str, typing.Any]]]],
    virtual_service_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2555247980b22da56ed1e9a5bcfe9564df4746b92bbbcacc74c774263cc306(
    *,
    actions: typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActions, typing.Dict[builtins.str, typing.Any]],
    match_criteria: typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247ecc80d5c4a1f0402162b9de1d28a958fac55ac36cfeedd3a57be0e8e4a2ee(
    *,
    modify_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redirect: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    rewrite_url: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0a50d50b8721f8b54e8bd399054d8398f763ecc245980b2110d53e0e76a144(
    *,
    action: builtins.str,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba12c0c5205ac37e56105f6fab0dd862d7c5a4f87d120ab8e089a9e70981169(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0f63ffd8f3d299c660b8c4c302f170977e60f5d52d1c6d6c6eb4a987538917(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42b02b58fa41fb40504188602ad0ff0ad97058dffd1971ce1dd4facc72194de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce5204b67fa8fadc4b07e20668cfc49fcd537397b8239deeb163868c12d6b58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2a3ca6763d58158f4faf838ba886bd5846ffadbe2ad1ffdee8a10fa081ac78(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140123200f3ad9a0d3442483fd838d7bd904e1f7f5d3f7f166413a83194b1b15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2289d253195cc4a61d1e651bc1e3f098c1628ab7b4ae81aac5333df19abe56c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524de7827433dd38fa9c83027f8f2b4a5ed4fd7d9c2eac953f55b1ddea0721d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af42b24238e6f6c7f7c570920520b2bfab512a9323135f38e21b1bd38582ed2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d690564f19a09989926ab96a75a4a4d6661aa4d42a9ba14ca8d5f2fdb3aa9a45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531789d21cd0ddf2ea81a5ba12af40ee8cdb79d6778e085be5c31f330975ffa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103d783f23a36673c978f74174720bf8507f05d0423fc37c7ba25a4841c8bf10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350fa2c33df7b3ccb8c4e27d9880d9596b7285aa9a6acee965b44812a5317c96(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleActionsModifyHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f210fc8169ce5aae653540aacce516355cb2075a07cf8ccdd501f1d38b8503(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7a3ea52fac9f7cb5603a5c98eb6dbc798e559e14f0a627af0b3284f226317f(
    *,
    protocol: builtins.str,
    status_code: jsii.Number,
    host: typing.Optional[builtins.str] = None,
    keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cfe3d4d7d16ffe49e71bd2a9ddb6e4a55b96e0314efbbbd2a54f47a60e46b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592c2d0365fe0d3290b3b4f467c4c0e8dab23e6ab308eb48639e6ab2b8994df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a797b3e398bc35806c89560bffc2d68b133d9b09344d31e262b3bf8c389f163c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce68b9a953cc2012ff017439bfd45cf210b9ddce4a638b1474c0fec162877005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0efc0183c5bd87033e3ab290423323a7f7ed894e2bc673678c554f1db380358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569faba5618504ba7150799db5fd17a79c4fb02893d910bf267e6877b73ae0ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f6e44820c8a8805431328af9c127ffd7a5ff9063542857d1e55b1f8d662f79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997d84a8a23ffe830ecdc3edd278e0c7aa1bc6d6edd598498639d8be662601c3(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c4cf92adbe54074075ec817e58f172b9ee3cf218039f292510293faf0f9a83(
    *,
    existing_path: builtins.str,
    host_header: builtins.str,
    keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583efc00b89e892ea51a1231e3fbf5a34bf5f52dbb83a9f5c63e932706663020(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39d8cc04ac8301e1b6aa161637d554312680b317805d2863dd1004d8f193f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2ba3a554f416be1cf047ffe79a49350540113914c1fa456a7ebaae8daef7a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0198b8433e88b7cd1252c4519cde8116bac2fdc1c8ba26df99b02184309c47d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c95e680bbf94e3aa363e8eb974a3f9a1795403f0c98749b5b05f174072173d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5d25607f249a189b4aa63d1322e39b5026d9a852e6ba2affecd3eb34742842(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleActionsRewriteUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b104e8647548a9116594d9630753d8e2ec17e566a6a2197fae378f3ab9707411(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d21cfa99c45ea9932a2641987ad1800abc76b12dc000d0207cd24f5e355f7c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172d59e872c31baffee70a49e8fc86e98d7779fac83910ca177f06d5911d336f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a48bfe14b554ebb37ae797a03288d9df0828f541a4f9f18c29e08041b25f692(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7a2ee747f7ee4fcacc517648c8c1417356dd360f16260ef71d540a0e914376(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59cf19749697bb0e035648fae0bd37893215b0d951f5c3b42cb27a6ee9c34b49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821752d0baa87316e03fec01c4829f7d873bc8dace66e591363abfbab4e6f422(
    *,
    client_ip_address: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    cookie: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    http_methods: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath, typing.Dict[builtins.str, typing.Any]]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    query: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_ports: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114dad572b16e4391d289731f08e9015ad32db69b95205758db64c7828743812(
    *,
    criteria: builtins.str,
    ip_addresses: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8736ce2d39ac2df1856afa006d55a17421d7570b9334a90225279f33882589c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a43d3d0fc146ad10b8f4b0a9f5b12a756fad2adce1ffb7faceb63410c0d3e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6e7636cb3663b25eb8440fe8ea5a5dc2a58210010e309f381a3c02db0b066f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8e615268fca8263e264adb3b0a08753f0f37299e7ea85d43cc530b8d89bf93(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaClientIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6e7a788559aaaa51b4a005ba94d6330b4c87e2669e9ca72e374ede75e2f5fa(
    *,
    criteria: builtins.str,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1992f84fda1876fcbdc992490dc250d6ae2753f6ce33ef6eeb79de066fed52bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e908659cfb95e84e04031dce9da1047a5ed8f808c9f06d5a8ca1e22acbd9ed5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c488658c406f689a413406908ef704b73c5e73c5393d3366a55c3fd3ab0459f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740e9fe772a214b17187e022db3f9951f441d3aaaa19cb58bb68550e7ce85a23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc6f94c7105a94805f3c20055709d198d8b554a3e0a8df51c19f6f9976e741f(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a537e69d351a21541a759d39d5c4c902e9dc6263f33d1f24c4cf25478c52864(
    *,
    criteria: builtins.str,
    methods: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a893ef4de837be92333f7d941bdb172cb66b757f285b7d03bb0a755672c7592(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f6c98044336616a5cc88b5714651e7fd9171546a972dd14148ed37112faf5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84e8c4065dcd79e83d6a76150100503ed9b8291a2790fd3c0739436716289e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39701de264221891e883db084986d12f45e6598bcf65daa6c704979a76e430d(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaHttpMethods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe8d87c02f6d091d02e85be6712b7c816ee3cee0c4fc2b40dbad0ae2c46ae80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684f3ad667324ed7379e8e70630d3a19568d55791330485529fff6f376916d8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42aad28817739af466f6a08ca28a3430871b51d7ea8a58a44b89d2c44a12e0e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb54749976ebf4dfa5bccf796ba2bf473cfec892d0d9e1e8587642e38a0c0c28(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8aa30ac02f38fc67c6d6fa9fcfb5a4b25a81558797c04ecd27b68c181440d7(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96d9d4f7d75cebb0c84f88e504c6320a3046893cc3b98454ac1026d4cf3f95f(
    *,
    criteria: builtins.str,
    paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb2bc459d04eefdcec470ae6d504d1cf3542daaff132c621e3a5cbc610b3cfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f40e8a34b3c08b45845d83159e354458184d183bea5948e99b82a9c297201b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0f251723080ed853cc2da2577d9033ed5318940575c631aec56b5c7c735271(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8eba5fa1b013ca72749aebbe75c3cab8b1c8bd9f1bcc7ebd22292f3ecb1ce9(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373c36ba2568c62f2002027bd1c3ffd608cb72c85b3fae3c89a5864148045be7(
    *,
    criteria: builtins.str,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4a20df618de3a54755a5aa27cce169a5bb3757014bb66d938134bf9794861e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba9eb871272e71b5f9948ec07dafc36007b7890bd2b36217e3e4643713ebb2d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f8048913b08f37342ecd86cbe9e60c2444e9bcf37e1c1a5f8080e52db6372c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5da9f25fcdb4aeab81dbcbced2ef7f6befa6ce2d5c60d4fa9823bc6687012b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5d1e4a46a73a869d41fd51c6855f56da0d62990fde6449c823c273c6ffd9d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abef442bcac123004bd10b09d42a0fa0730a1999b30e97436d957225e6345ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c8a7590b62f2f4df6ea0226b687ada102252dd654a5bba758d30ad7895fc70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce198c7bd54964d67af2639e2f69ed0beda26a827d9c41530bdc157c5722dd3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8a3d85988debec651115fbc11ad02481fc1bb90fe0b73b24a42fad11db444b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f984c2c693e082fc02a3b82905df2ff2fded1796301aa261c2c9153731c6b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd482bb0fd1958ebe691184de33525fa52aced2e4a0957b87a4ba890e20a0b94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaRequestHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fcb623a14e1a68d7830b4706b00e44e6245e2b35ce8057ad7d6aab706d738bc(
    *,
    criteria: builtins.str,
    ports: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b49ea3cb58257e46148b0a056b2efd323adc5c6c652f8ce0e3de4616c3dc88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6287ca46857016e8d2ff69a61d436784b270e482e02c29922ab64a60eca01c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e320197d1f0f29cbd40043d2657862a31667fbe5a98b4e8bbb93b41d85f324(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0217fd64fac41635c5d5714e7adc67614b55e1890353336989e701d9503b20(
    value: typing.Optional[NsxtAlbVirtualServiceHttpReqRulesRuleMatchCriteriaServicePorts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8474b50825601ec5e05bfafd37ebc6a0e13784c637205132d2e9f6fa0fa1745e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129b00a7e7462d36c10f56c1290f40a64026daa62342ba1c01d7143999042592(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91d8dbdbe03bd2e99924bf58d9b605c330edf63ff738bbaedfc9e359f2eac26(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6a05a01f28d4c8d3f0b91bdc53ce85045c6136d913f1c43d1a3b2407fa9691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecea58dbdcf76126748a176aeff0995b6370de3e8b7e8c4a19df103504b954d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpReqRulesRule]],
) -> None:
    """Type checking stubs"""
    pass
