'''
# `vcd_lb_app_profile`

Refer to the Terraform Registry for docs: [`vcd_lb_app_profile`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile).
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


class LbAppProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.lbAppProfile.LbAppProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile vcd_lb_app_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway: builtins.str,
        name: builtins.str,
        type: builtins.str,
        cookie_mode: typing.Optional[builtins.str] = None,
        cookie_name: typing.Optional[builtins.str] = None,
        enable_pool_side_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ssl_passthrough: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration: typing.Optional[jsii.Number] = None,
        http_redirect_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insert_x_forwarded_http_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        persistence_mechanism: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile vcd_lb_app_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway: Edge gateway name in which the LB Application Profile is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#edge_gateway LbAppProfile#edge_gateway}
        :param name: Unique LB Application Profile name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#name LbAppProfile#name}
        :param type: Protocol type used to send requests to the server. One of 'tcp', 'udp', 'http' org 'https'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#type LbAppProfile#type}
        :param cookie_mode: The mode by which the cookie should be inserted. One of 'insert', 'prefix', or 'appsession'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#cookie_mode LbAppProfile#cookie_mode}
        :param cookie_name: Used to uniquely identify the session the first time a client accesses the site. The load balancer refers to this cookie when connecting subsequent requests in the session, so that they all go to the same virtual server. Only applies for persistence_mechanism 'cookie' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#cookie_name LbAppProfile#cookie_name}
        :param enable_pool_side_ssl: Enable to define the certificate, CAs, or CRLs used to authenticate the load balancer from the server side. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#enable_pool_side_ssl LbAppProfile#enable_pool_side_ssl}
        :param enable_ssl_passthrough: Enable SSL authentication to be passed through to the virtual server. Otherwise SSL authentication takes place at the destination address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#enable_ssl_passthrough LbAppProfile#enable_ssl_passthrough}
        :param expiration: Length of time in seconds that persistence stays in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#expiration LbAppProfile#expiration}
        :param http_redirect_url: The URL to which traffic that arrives at the destination address should be redirected. Only applies for types 'http' and 'https' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#http_redirect_url LbAppProfile#http_redirect_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#id LbAppProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insert_x_forwarded_http_header: Enables 'X-Forwarded-For' header for identifying the originating IP address of a client connecting to a Web server through the load balancer. Only applies for types HTTP and HTTPS Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#insert_x_forwarded_http_header LbAppProfile#insert_x_forwarded_http_header}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#org LbAppProfile#org}
        :param persistence_mechanism: Persistence mechanism for the profile. One of 'cookie', 'ssl-sessionid', 'sourceip'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#persistence_mechanism LbAppProfile#persistence_mechanism}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#vdc LbAppProfile#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3eaec9ec48ce17ba0d5a4f17cd187d2a87e15457a569d481ad788fc03c8d5b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LbAppProfileConfig(
            edge_gateway=edge_gateway,
            name=name,
            type=type,
            cookie_mode=cookie_mode,
            cookie_name=cookie_name,
            enable_pool_side_ssl=enable_pool_side_ssl,
            enable_ssl_passthrough=enable_ssl_passthrough,
            expiration=expiration,
            http_redirect_url=http_redirect_url,
            id=id,
            insert_x_forwarded_http_header=insert_x_forwarded_http_header,
            org=org,
            persistence_mechanism=persistence_mechanism,
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
        '''Generates CDKTF code for importing a LbAppProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LbAppProfile to import.
        :param import_from_id: The id of the existing LbAppProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LbAppProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38fdf5d9d704a1b0c627b161ad135ddbef71ba821248679982d12e2af581539)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCookieMode")
    def reset_cookie_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookieMode", []))

    @jsii.member(jsii_name="resetCookieName")
    def reset_cookie_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookieName", []))

    @jsii.member(jsii_name="resetEnablePoolSideSsl")
    def reset_enable_pool_side_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePoolSideSsl", []))

    @jsii.member(jsii_name="resetEnableSslPassthrough")
    def reset_enable_ssl_passthrough(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSslPassthrough", []))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetHttpRedirectUrl")
    def reset_http_redirect_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRedirectUrl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInsertXForwardedHttpHeader")
    def reset_insert_x_forwarded_http_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsertXForwardedHttpHeader", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetPersistenceMechanism")
    def reset_persistence_mechanism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistenceMechanism", []))

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
    @jsii.member(jsii_name="cookieModeInput")
    def cookie_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cookieModeInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieNameInput")
    def cookie_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cookieNameInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayInput")
    def edge_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePoolSideSslInput")
    def enable_pool_side_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePoolSideSslInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSslPassthroughInput")
    def enable_ssl_passthrough_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSslPassthroughInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRedirectUrlInput")
    def http_redirect_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpRedirectUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insertXForwardedHttpHeaderInput")
    def insert_x_forwarded_http_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insertXForwardedHttpHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="persistenceMechanismInput")
    def persistence_mechanism_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "persistenceMechanismInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieMode")
    def cookie_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieMode"))

    @cookie_mode.setter
    def cookie_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60da498e648b77ad7c6998856dfa23dcd3a3f4c8772b9ff5ed3c89d6564f5467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieMode", value)

    @builtins.property
    @jsii.member(jsii_name="cookieName")
    def cookie_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieName"))

    @cookie_name.setter
    def cookie_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33744ec912ca0cad70a00e10054ec65ec08aae2d5016f35507717a1bbdbe4ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieName", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGateway")
    def edge_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGateway"))

    @edge_gateway.setter
    def edge_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdef9c8ffe1d45652fe804b582e7118be529cea1c452662c0e613c2db033c070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGateway", value)

    @builtins.property
    @jsii.member(jsii_name="enablePoolSideSsl")
    def enable_pool_side_ssl(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePoolSideSsl"))

    @enable_pool_side_ssl.setter
    def enable_pool_side_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1658a588c1eb42cbccbe303b87f187d4de2440c7c9d1a549058b4910da6572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePoolSideSsl", value)

    @builtins.property
    @jsii.member(jsii_name="enableSslPassthrough")
    def enable_ssl_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSslPassthrough"))

    @enable_ssl_passthrough.setter
    def enable_ssl_passthrough(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e5259b258a617b372797a1e6505bbd554b6cf4a541477fb880e56df0d46725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSslPassthrough", value)

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c654fde51897d249953d35bda0782c7ac2ebc7b68c99d7d00300c1673d1d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value)

    @builtins.property
    @jsii.member(jsii_name="httpRedirectUrl")
    def http_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpRedirectUrl"))

    @http_redirect_url.setter
    def http_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9566543af847f1ee943ecb41dd2fcc6a361b59adef8e0d2090743d533f753f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9fc6ace7ac0cacbdb3c631d17c03b28c5658ce21d75e998416fd111a6f538c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="insertXForwardedHttpHeader")
    def insert_x_forwarded_http_header(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insertXForwardedHttpHeader"))

    @insert_x_forwarded_http_header.setter
    def insert_x_forwarded_http_header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7f72589dd8fde5f24d44f7de82151b3bcbefe04a768fc28276a77d1505cf48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insertXForwardedHttpHeader", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4605949d35482360e81e95869269d3a9f54527ecd6a90083c20281d31108f3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7957f532c355e91af071d3af3aef34a9b853549f4705ccc25706ba6b9ee5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="persistenceMechanism")
    def persistence_mechanism(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "persistenceMechanism"))

    @persistence_mechanism.setter
    def persistence_mechanism(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177fa47e47668dcc33fd35c6e005b3848fcd7e9b067ea77104ad3720a59d95ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "persistenceMechanism", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db6396c75500ec8a3b0fd9fc97f2b9e8363fb6a7faec1e1258ea0bc2e7f0892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e893e8fa0e59b290a4a0e328da8c3ebc6fea1889c3a923a2d8b66950dacb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.lbAppProfile.LbAppProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "edge_gateway": "edgeGateway",
        "name": "name",
        "type": "type",
        "cookie_mode": "cookieMode",
        "cookie_name": "cookieName",
        "enable_pool_side_ssl": "enablePoolSideSsl",
        "enable_ssl_passthrough": "enableSslPassthrough",
        "expiration": "expiration",
        "http_redirect_url": "httpRedirectUrl",
        "id": "id",
        "insert_x_forwarded_http_header": "insertXForwardedHttpHeader",
        "org": "org",
        "persistence_mechanism": "persistenceMechanism",
        "vdc": "vdc",
    },
)
class LbAppProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        edge_gateway: builtins.str,
        name: builtins.str,
        type: builtins.str,
        cookie_mode: typing.Optional[builtins.str] = None,
        cookie_name: typing.Optional[builtins.str] = None,
        enable_pool_side_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ssl_passthrough: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration: typing.Optional[jsii.Number] = None,
        http_redirect_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insert_x_forwarded_http_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        persistence_mechanism: typing.Optional[builtins.str] = None,
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
        :param edge_gateway: Edge gateway name in which the LB Application Profile is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#edge_gateway LbAppProfile#edge_gateway}
        :param name: Unique LB Application Profile name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#name LbAppProfile#name}
        :param type: Protocol type used to send requests to the server. One of 'tcp', 'udp', 'http' org 'https'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#type LbAppProfile#type}
        :param cookie_mode: The mode by which the cookie should be inserted. One of 'insert', 'prefix', or 'appsession'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#cookie_mode LbAppProfile#cookie_mode}
        :param cookie_name: Used to uniquely identify the session the first time a client accesses the site. The load balancer refers to this cookie when connecting subsequent requests in the session, so that they all go to the same virtual server. Only applies for persistence_mechanism 'cookie' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#cookie_name LbAppProfile#cookie_name}
        :param enable_pool_side_ssl: Enable to define the certificate, CAs, or CRLs used to authenticate the load balancer from the server side. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#enable_pool_side_ssl LbAppProfile#enable_pool_side_ssl}
        :param enable_ssl_passthrough: Enable SSL authentication to be passed through to the virtual server. Otherwise SSL authentication takes place at the destination address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#enable_ssl_passthrough LbAppProfile#enable_ssl_passthrough}
        :param expiration: Length of time in seconds that persistence stays in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#expiration LbAppProfile#expiration}
        :param http_redirect_url: The URL to which traffic that arrives at the destination address should be redirected. Only applies for types 'http' and 'https' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#http_redirect_url LbAppProfile#http_redirect_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#id LbAppProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insert_x_forwarded_http_header: Enables 'X-Forwarded-For' header for identifying the originating IP address of a client connecting to a Web server through the load balancer. Only applies for types HTTP and HTTPS Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#insert_x_forwarded_http_header LbAppProfile#insert_x_forwarded_http_header}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#org LbAppProfile#org}
        :param persistence_mechanism: Persistence mechanism for the profile. One of 'cookie', 'ssl-sessionid', 'sourceip'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#persistence_mechanism LbAppProfile#persistence_mechanism}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#vdc LbAppProfile#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb273e54f983cf98a0a88b0efee0b709ffd0cdf175c311793ebd3e9583d0bb5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway", value=edge_gateway, expected_type=type_hints["edge_gateway"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument cookie_mode", value=cookie_mode, expected_type=type_hints["cookie_mode"])
            check_type(argname="argument cookie_name", value=cookie_name, expected_type=type_hints["cookie_name"])
            check_type(argname="argument enable_pool_side_ssl", value=enable_pool_side_ssl, expected_type=type_hints["enable_pool_side_ssl"])
            check_type(argname="argument enable_ssl_passthrough", value=enable_ssl_passthrough, expected_type=type_hints["enable_ssl_passthrough"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument http_redirect_url", value=http_redirect_url, expected_type=type_hints["http_redirect_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insert_x_forwarded_http_header", value=insert_x_forwarded_http_header, expected_type=type_hints["insert_x_forwarded_http_header"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument persistence_mechanism", value=persistence_mechanism, expected_type=type_hints["persistence_mechanism"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway": edge_gateway,
            "name": name,
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
        if cookie_mode is not None:
            self._values["cookie_mode"] = cookie_mode
        if cookie_name is not None:
            self._values["cookie_name"] = cookie_name
        if enable_pool_side_ssl is not None:
            self._values["enable_pool_side_ssl"] = enable_pool_side_ssl
        if enable_ssl_passthrough is not None:
            self._values["enable_ssl_passthrough"] = enable_ssl_passthrough
        if expiration is not None:
            self._values["expiration"] = expiration
        if http_redirect_url is not None:
            self._values["http_redirect_url"] = http_redirect_url
        if id is not None:
            self._values["id"] = id
        if insert_x_forwarded_http_header is not None:
            self._values["insert_x_forwarded_http_header"] = insert_x_forwarded_http_header
        if org is not None:
            self._values["org"] = org
        if persistence_mechanism is not None:
            self._values["persistence_mechanism"] = persistence_mechanism
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
    def edge_gateway(self) -> builtins.str:
        '''Edge gateway name in which the LB Application Profile is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#edge_gateway LbAppProfile#edge_gateway}
        '''
        result = self._values.get("edge_gateway")
        assert result is not None, "Required property 'edge_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Unique LB Application Profile name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#name LbAppProfile#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Protocol type used to send requests to the server. One of 'tcp', 'udp', 'http' org 'https'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#type LbAppProfile#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cookie_mode(self) -> typing.Optional[builtins.str]:
        '''The mode by which the cookie should be inserted. One of 'insert', 'prefix', or 'appsession'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#cookie_mode LbAppProfile#cookie_mode}
        '''
        result = self._values.get("cookie_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cookie_name(self) -> typing.Optional[builtins.str]:
        '''Used to uniquely identify the session the first time a client accesses the site.

        The load balancer refers to this cookie when connecting subsequent requests in the session, so that they all go to the same virtual server. Only applies for persistence_mechanism 'cookie'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#cookie_name LbAppProfile#cookie_name}
        '''
        result = self._values.get("cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_pool_side_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable to define the certificate, CAs, or CRLs used to authenticate the load balancer from the server side.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#enable_pool_side_ssl LbAppProfile#enable_pool_side_ssl}
        '''
        result = self._values.get("enable_pool_side_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_ssl_passthrough(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable SSL authentication to be passed through to the virtual server.

        Otherwise SSL authentication takes place at the destination address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#enable_ssl_passthrough LbAppProfile#enable_ssl_passthrough}
        '''
        result = self._values.get("enable_ssl_passthrough")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expiration(self) -> typing.Optional[jsii.Number]:
        '''Length of time in seconds that persistence stays in effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#expiration LbAppProfile#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_redirect_url(self) -> typing.Optional[builtins.str]:
        '''The URL to which traffic that arrives at the destination address should be redirected.

        Only applies for types 'http' and 'https'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#http_redirect_url LbAppProfile#http_redirect_url}
        '''
        result = self._values.get("http_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#id LbAppProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insert_x_forwarded_http_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables 'X-Forwarded-For' header for identifying the originating IP address of a client connecting to a Web server through the load balancer.

        Only applies for types HTTP and HTTPS

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#insert_x_forwarded_http_header LbAppProfile#insert_x_forwarded_http_header}
        '''
        result = self._values.get("insert_x_forwarded_http_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#org LbAppProfile#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistence_mechanism(self) -> typing.Optional[builtins.str]:
        '''Persistence mechanism for the profile. One of 'cookie', 'ssl-sessionid', 'sourceip'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#persistence_mechanism LbAppProfile#persistence_mechanism}
        '''
        result = self._values.get("persistence_mechanism")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/lb_app_profile#vdc LbAppProfile#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbAppProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LbAppProfile",
    "LbAppProfileConfig",
]

publication.publish()

def _typecheckingstub__c3eaec9ec48ce17ba0d5a4f17cd187d2a87e15457a569d481ad788fc03c8d5b4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway: builtins.str,
    name: builtins.str,
    type: builtins.str,
    cookie_mode: typing.Optional[builtins.str] = None,
    cookie_name: typing.Optional[builtins.str] = None,
    enable_pool_side_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ssl_passthrough: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expiration: typing.Optional[jsii.Number] = None,
    http_redirect_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insert_x_forwarded_http_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    persistence_mechanism: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__f38fdf5d9d704a1b0c627b161ad135ddbef71ba821248679982d12e2af581539(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60da498e648b77ad7c6998856dfa23dcd3a3f4c8772b9ff5ed3c89d6564f5467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33744ec912ca0cad70a00e10054ec65ec08aae2d5016f35507717a1bbdbe4ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdef9c8ffe1d45652fe804b582e7118be529cea1c452662c0e613c2db033c070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1658a588c1eb42cbccbe303b87f187d4de2440c7c9d1a549058b4910da6572(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e5259b258a617b372797a1e6505bbd554b6cf4a541477fb880e56df0d46725(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c654fde51897d249953d35bda0782c7ac2ebc7b68c99d7d00300c1673d1d52(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9566543af847f1ee943ecb41dd2fcc6a361b59adef8e0d2090743d533f753f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9fc6ace7ac0cacbdb3c631d17c03b28c5658ce21d75e998416fd111a6f538c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7f72589dd8fde5f24d44f7de82151b3bcbefe04a768fc28276a77d1505cf48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4605949d35482360e81e95869269d3a9f54527ecd6a90083c20281d31108f3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7957f532c355e91af071d3af3aef34a9b853549f4705ccc25706ba6b9ee5d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177fa47e47668dcc33fd35c6e005b3848fcd7e9b067ea77104ad3720a59d95ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db6396c75500ec8a3b0fd9fc97f2b9e8363fb6a7faec1e1258ea0bc2e7f0892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e893e8fa0e59b290a4a0e328da8c3ebc6fea1889c3a923a2d8b66950dacb9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb273e54f983cf98a0a88b0efee0b709ffd0cdf175c311793ebd3e9583d0bb5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway: builtins.str,
    name: builtins.str,
    type: builtins.str,
    cookie_mode: typing.Optional[builtins.str] = None,
    cookie_name: typing.Optional[builtins.str] = None,
    enable_pool_side_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ssl_passthrough: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expiration: typing.Optional[jsii.Number] = None,
    http_redirect_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insert_x_forwarded_http_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    persistence_mechanism: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
