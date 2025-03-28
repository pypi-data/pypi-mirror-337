'''
# `provider`

Refer to the Terraform Registry for docs: [`vcd`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs).
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


class VcdProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.provider.VcdProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs vcd}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        org: builtins.str,
        url: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        allow_api_token_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_service_account_token_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_unverified_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_token: typing.Optional[builtins.str] = None,
        api_token_file: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        ignore_metadata_changes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VcdProviderIgnoreMetadataChanges", typing.Dict[builtins.str, typing.Any]]]]] = None,
        import_separator: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging_file: typing.Optional[builtins.str] = None,
        max_retry_timeout: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        saml_adfs_cookie: typing.Optional[builtins.str] = None,
        saml_adfs_rpt_id: typing.Optional[builtins.str] = None,
        service_account_token_file: typing.Optional[builtins.str] = None,
        sysorg: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs vcd} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param org: The VCD Org for API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#org VcdProvider#org}
        :param url: The VCD url for VCD API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#url VcdProvider#url}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#alias VcdProvider#alias}
        :param allow_api_token_file: Set this to true if you understand the security risks of using API token files and would like to suppress the warnings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_api_token_file VcdProvider#allow_api_token_file}
        :param allow_service_account_token_file: Set this to true if you understand the security risks of using Service Account token files and would like to suppress the warnings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_service_account_token_file VcdProvider#allow_service_account_token_file}
        :param allow_unverified_ssl: If set, VCDClient will permit unverifiable SSL certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_unverified_ssl VcdProvider#allow_unverified_ssl}
        :param api_token: The API token used instead of username/password for VCD API operations. (Requires VCD 10.3.1+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#api_token VcdProvider#api_token}
        :param api_token_file: The API token file instead of username/password for VCD API operations. (Requires VCD 10.3.1+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#api_token_file VcdProvider#api_token_file}
        :param auth_type: 'integrated', 'saml_adfs', 'token', 'api_token', 'api_token_file' and 'service_account_token_file' are supported. 'integrated' is default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#auth_type VcdProvider#auth_type}
        :param ignore_metadata_changes: ignore_metadata_changes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#ignore_metadata_changes VcdProvider#ignore_metadata_changes}
        :param import_separator: Defines the import separation string to be used with 'terraform import'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#import_separator VcdProvider#import_separator}
        :param logging: If set, it will enable logging of API requests and responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#logging VcdProvider#logging}
        :param logging_file: Defines the full name of the logging file for API calls (requires 'logging'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#logging_file VcdProvider#logging_file}
        :param max_retry_timeout: Max num seconds to wait for successful response when operating on resources within vCloud (defaults to 60). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#max_retry_timeout VcdProvider#max_retry_timeout}
        :param password: The user password for VCD API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#password VcdProvider#password}
        :param saml_adfs_cookie: Allows to specify custom cookie for ADFS server lookup. '{{.Org}}' is replaced by real Org - e.g. 'sso-preferred=yes; sso_redirect_org={{.Org}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#saml_adfs_cookie VcdProvider#saml_adfs_cookie}
        :param saml_adfs_rpt_id: Allows to specify custom Relaying Party Trust Identifier for auth_type=saml_adfs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#saml_adfs_rpt_id VcdProvider#saml_adfs_rpt_id}
        :param service_account_token_file: The Service Account API token file instead of username/password for VCD API operations. (Requires VCD 10.4.0+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#service_account_token_file VcdProvider#service_account_token_file}
        :param sysorg: The VCD Org for user authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#sysorg VcdProvider#sysorg}
        :param token: The token used instead of username/password for VCD API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#token VcdProvider#token}
        :param user: The user name for VCD API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#user VcdProvider#user}
        :param vdc: The VDC for API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#vdc VcdProvider#vdc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e77e314ff0ea30d6fc8caf7f566cd9cdff220ebbfd6fef80c46f8739d2897b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VcdProviderConfig(
            org=org,
            url=url,
            alias=alias,
            allow_api_token_file=allow_api_token_file,
            allow_service_account_token_file=allow_service_account_token_file,
            allow_unverified_ssl=allow_unverified_ssl,
            api_token=api_token,
            api_token_file=api_token_file,
            auth_type=auth_type,
            ignore_metadata_changes=ignore_metadata_changes,
            import_separator=import_separator,
            logging=logging,
            logging_file=logging_file,
            max_retry_timeout=max_retry_timeout,
            password=password,
            saml_adfs_cookie=saml_adfs_cookie,
            saml_adfs_rpt_id=saml_adfs_rpt_id,
            service_account_token_file=service_account_token_file,
            sysorg=sysorg,
            token=token,
            user=user,
            vdc=vdc,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a VcdProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VcdProvider to import.
        :param import_from_id: The id of the existing VcdProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VcdProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb6e96beca4f867792c5a602269985487bc734fff11a083702265df860a2178)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAllowApiTokenFile")
    def reset_allow_api_token_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowApiTokenFile", []))

    @jsii.member(jsii_name="resetAllowServiceAccountTokenFile")
    def reset_allow_service_account_token_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowServiceAccountTokenFile", []))

    @jsii.member(jsii_name="resetAllowUnverifiedSsl")
    def reset_allow_unverified_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowUnverifiedSsl", []))

    @jsii.member(jsii_name="resetApiToken")
    def reset_api_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiToken", []))

    @jsii.member(jsii_name="resetApiTokenFile")
    def reset_api_token_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiTokenFile", []))

    @jsii.member(jsii_name="resetAuthType")
    def reset_auth_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthType", []))

    @jsii.member(jsii_name="resetIgnoreMetadataChanges")
    def reset_ignore_metadata_changes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreMetadataChanges", []))

    @jsii.member(jsii_name="resetImportSeparator")
    def reset_import_separator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportSeparator", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetLoggingFile")
    def reset_logging_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingFile", []))

    @jsii.member(jsii_name="resetMaxRetryTimeout")
    def reset_max_retry_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetryTimeout", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetSamlAdfsCookie")
    def reset_saml_adfs_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlAdfsCookie", []))

    @jsii.member(jsii_name="resetSamlAdfsRptId")
    def reset_saml_adfs_rpt_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlAdfsRptId", []))

    @jsii.member(jsii_name="resetServiceAccountTokenFile")
    def reset_service_account_token_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountTokenFile", []))

    @jsii.member(jsii_name="resetSysorg")
    def reset_sysorg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSysorg", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

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
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="allowApiTokenFileInput")
    def allow_api_token_file_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowApiTokenFileInput"))

    @builtins.property
    @jsii.member(jsii_name="allowServiceAccountTokenFileInput")
    def allow_service_account_token_file_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowServiceAccountTokenFileInput"))

    @builtins.property
    @jsii.member(jsii_name="allowUnverifiedSslInput")
    def allow_unverified_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowUnverifiedSslInput"))

    @builtins.property
    @jsii.member(jsii_name="apiTokenFileInput")
    def api_token_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenFileInput"))

    @builtins.property
    @jsii.member(jsii_name="apiTokenInput")
    def api_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreMetadataChangesInput")
    def ignore_metadata_changes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VcdProviderIgnoreMetadataChanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VcdProviderIgnoreMetadataChanges"]]], jsii.get(self, "ignoreMetadataChangesInput"))

    @builtins.property
    @jsii.member(jsii_name="importSeparatorInput")
    def import_separator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importSeparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingFileInput")
    def logging_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingFileInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetryTimeoutInput")
    def max_retry_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="samlAdfsCookieInput")
    def saml_adfs_cookie_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlAdfsCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="samlAdfsRptIdInput")
    def saml_adfs_rpt_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlAdfsRptIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountTokenFileInput")
    def service_account_token_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountTokenFileInput"))

    @builtins.property
    @jsii.member(jsii_name="sysorgInput")
    def sysorg_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sysorgInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07570ec945e73c84c535738d6d75c0770d5f7fc3b041775e1fb5359cc52ca70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="allowApiTokenFile")
    def allow_api_token_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowApiTokenFile"))

    @allow_api_token_file.setter
    def allow_api_token_file(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0dd004414979d11184817c4cc370827283024bc6deb5c5438c557e1d7ea4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowApiTokenFile", value)

    @builtins.property
    @jsii.member(jsii_name="allowServiceAccountTokenFile")
    def allow_service_account_token_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowServiceAccountTokenFile"))

    @allow_service_account_token_file.setter
    def allow_service_account_token_file(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fc2d0667ece09203bca688109b1d3cfc9460b5dd0cb675631eb74205979504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowServiceAccountTokenFile", value)

    @builtins.property
    @jsii.member(jsii_name="allowUnverifiedSsl")
    def allow_unverified_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowUnverifiedSsl"))

    @allow_unverified_ssl.setter
    def allow_unverified_ssl(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0e361e7860aa8e07812d8b2cca766d010e3bed03995e9cd9da09ba225f6a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowUnverifiedSsl", value)

    @builtins.property
    @jsii.member(jsii_name="apiToken")
    def api_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiToken"))

    @api_token.setter
    def api_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6defc60ccd8a02ae5424ca0b60088031c68768b059633bc67d68f966ca20d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiToken", value)

    @builtins.property
    @jsii.member(jsii_name="apiTokenFile")
    def api_token_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenFile"))

    @api_token_file.setter
    def api_token_file(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5027cc8a886b6eae6119496a44355e27296f3a838a857617e87310eed0027cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiTokenFile", value)

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1686e18d8fffb070b8c9ebb1d1041e2c12de5e4fc82f6abed7024d57556c1b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreMetadataChanges")
    def ignore_metadata_changes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VcdProviderIgnoreMetadataChanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VcdProviderIgnoreMetadataChanges"]]], jsii.get(self, "ignoreMetadataChanges"))

    @ignore_metadata_changes.setter
    def ignore_metadata_changes(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VcdProviderIgnoreMetadataChanges"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c827bbefebc269a99949ee1ea5d987248f7e1ba32bd00f42d53a08fc0e38fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreMetadataChanges", value)

    @builtins.property
    @jsii.member(jsii_name="importSeparator")
    def import_separator(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importSeparator"))

    @import_separator.setter
    def import_separator(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a356f62519a16267be8be58778e69150be3e9c04f09244309e002e77a966f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importSeparator", value)

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logging"))

    @logging.setter
    def logging(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caab41d2b3bc669a755a497e98efc730d7be0d1b23101aba10e35ac72336ac91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="loggingFile")
    def logging_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingFile"))

    @logging_file.setter
    def logging_file(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f170ad3e18bc21f7c8c4c4e3eb4419d20b7358a2e3eb76c561e30a46900f638e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingFile", value)

    @builtins.property
    @jsii.member(jsii_name="maxRetryTimeout")
    def max_retry_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetryTimeout"))

    @max_retry_timeout.setter
    def max_retry_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f15c1a6b9149ee0ae715a10e44a409b3a90b72314c3e731a8cae8ad4104f566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "org"))

    @org.setter
    def org(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b9e90cc9c6fc83df6ca4584f0d4d20136824bf6c76d6bad72d99685c72c451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684994fc87bb2f04bf390932f3ec296812b9ca4521c9452f7614892b85af5c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="samlAdfsCookie")
    def saml_adfs_cookie(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlAdfsCookie"))

    @saml_adfs_cookie.setter
    def saml_adfs_cookie(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0e98e42d725286654425915549adabfef4fc0ecbaa7257bde7d39e85031b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlAdfsCookie", value)

    @builtins.property
    @jsii.member(jsii_name="samlAdfsRptId")
    def saml_adfs_rpt_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlAdfsRptId"))

    @saml_adfs_rpt_id.setter
    def saml_adfs_rpt_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19d84db2d34c748a796c5e8cfef4024243d8e9e694106fd84446c4f6c23f9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlAdfsRptId", value)

    @builtins.property
    @jsii.member(jsii_name="serviceAccountTokenFile")
    def service_account_token_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountTokenFile"))

    @service_account_token_file.setter
    def service_account_token_file(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287ff6d0b7b8784db9bba7aca50c43a0d1332da2eb01294213b3df0216a08103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountTokenFile", value)

    @builtins.property
    @jsii.member(jsii_name="sysorg")
    def sysorg(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sysorg"))

    @sysorg.setter
    def sysorg(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783eb78d9d0b48f46468b97d0b40c41b767e7d24d1d77663083fadd0182a7631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sysorg", value)

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7938c225912bab745d2c56d46cf52758090292fe7acec119bbfe71f89305382d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "url"))

    @url.setter
    def url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc548b738cce551280ecedb18d395cd776919d1521d9c0096d76fb933082426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "user"))

    @user.setter
    def user(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25aa21aa4caecccd42a830d3d01d6337256a20f12aa710d03a34ebf1ba89f667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733d00d8cf606f01af1d8a1691aa84142f57a5f6ee70838b89adbd4851a5e6e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.provider.VcdProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "org": "org",
        "url": "url",
        "alias": "alias",
        "allow_api_token_file": "allowApiTokenFile",
        "allow_service_account_token_file": "allowServiceAccountTokenFile",
        "allow_unverified_ssl": "allowUnverifiedSsl",
        "api_token": "apiToken",
        "api_token_file": "apiTokenFile",
        "auth_type": "authType",
        "ignore_metadata_changes": "ignoreMetadataChanges",
        "import_separator": "importSeparator",
        "logging": "logging",
        "logging_file": "loggingFile",
        "max_retry_timeout": "maxRetryTimeout",
        "password": "password",
        "saml_adfs_cookie": "samlAdfsCookie",
        "saml_adfs_rpt_id": "samlAdfsRptId",
        "service_account_token_file": "serviceAccountTokenFile",
        "sysorg": "sysorg",
        "token": "token",
        "user": "user",
        "vdc": "vdc",
    },
)
class VcdProviderConfig:
    def __init__(
        self,
        *,
        org: builtins.str,
        url: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        allow_api_token_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_service_account_token_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_unverified_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_token: typing.Optional[builtins.str] = None,
        api_token_file: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        ignore_metadata_changes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VcdProviderIgnoreMetadataChanges", typing.Dict[builtins.str, typing.Any]]]]] = None,
        import_separator: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging_file: typing.Optional[builtins.str] = None,
        max_retry_timeout: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        saml_adfs_cookie: typing.Optional[builtins.str] = None,
        saml_adfs_rpt_id: typing.Optional[builtins.str] = None,
        service_account_token_file: typing.Optional[builtins.str] = None,
        sysorg: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param org: The VCD Org for API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#org VcdProvider#org}
        :param url: The VCD url for VCD API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#url VcdProvider#url}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#alias VcdProvider#alias}
        :param allow_api_token_file: Set this to true if you understand the security risks of using API token files and would like to suppress the warnings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_api_token_file VcdProvider#allow_api_token_file}
        :param allow_service_account_token_file: Set this to true if you understand the security risks of using Service Account token files and would like to suppress the warnings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_service_account_token_file VcdProvider#allow_service_account_token_file}
        :param allow_unverified_ssl: If set, VCDClient will permit unverifiable SSL certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_unverified_ssl VcdProvider#allow_unverified_ssl}
        :param api_token: The API token used instead of username/password for VCD API operations. (Requires VCD 10.3.1+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#api_token VcdProvider#api_token}
        :param api_token_file: The API token file instead of username/password for VCD API operations. (Requires VCD 10.3.1+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#api_token_file VcdProvider#api_token_file}
        :param auth_type: 'integrated', 'saml_adfs', 'token', 'api_token', 'api_token_file' and 'service_account_token_file' are supported. 'integrated' is default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#auth_type VcdProvider#auth_type}
        :param ignore_metadata_changes: ignore_metadata_changes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#ignore_metadata_changes VcdProvider#ignore_metadata_changes}
        :param import_separator: Defines the import separation string to be used with 'terraform import'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#import_separator VcdProvider#import_separator}
        :param logging: If set, it will enable logging of API requests and responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#logging VcdProvider#logging}
        :param logging_file: Defines the full name of the logging file for API calls (requires 'logging'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#logging_file VcdProvider#logging_file}
        :param max_retry_timeout: Max num seconds to wait for successful response when operating on resources within vCloud (defaults to 60). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#max_retry_timeout VcdProvider#max_retry_timeout}
        :param password: The user password for VCD API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#password VcdProvider#password}
        :param saml_adfs_cookie: Allows to specify custom cookie for ADFS server lookup. '{{.Org}}' is replaced by real Org - e.g. 'sso-preferred=yes; sso_redirect_org={{.Org}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#saml_adfs_cookie VcdProvider#saml_adfs_cookie}
        :param saml_adfs_rpt_id: Allows to specify custom Relaying Party Trust Identifier for auth_type=saml_adfs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#saml_adfs_rpt_id VcdProvider#saml_adfs_rpt_id}
        :param service_account_token_file: The Service Account API token file instead of username/password for VCD API operations. (Requires VCD 10.4.0+). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#service_account_token_file VcdProvider#service_account_token_file}
        :param sysorg: The VCD Org for user authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#sysorg VcdProvider#sysorg}
        :param token: The token used instead of username/password for VCD API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#token VcdProvider#token}
        :param user: The user name for VCD API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#user VcdProvider#user}
        :param vdc: The VDC for API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#vdc VcdProvider#vdc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13e4989bdb198f331a97dfc77c4992947344833d779c1a3bc875e8641e623d9)
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allow_api_token_file", value=allow_api_token_file, expected_type=type_hints["allow_api_token_file"])
            check_type(argname="argument allow_service_account_token_file", value=allow_service_account_token_file, expected_type=type_hints["allow_service_account_token_file"])
            check_type(argname="argument allow_unverified_ssl", value=allow_unverified_ssl, expected_type=type_hints["allow_unverified_ssl"])
            check_type(argname="argument api_token", value=api_token, expected_type=type_hints["api_token"])
            check_type(argname="argument api_token_file", value=api_token_file, expected_type=type_hints["api_token_file"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument ignore_metadata_changes", value=ignore_metadata_changes, expected_type=type_hints["ignore_metadata_changes"])
            check_type(argname="argument import_separator", value=import_separator, expected_type=type_hints["import_separator"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument logging_file", value=logging_file, expected_type=type_hints["logging_file"])
            check_type(argname="argument max_retry_timeout", value=max_retry_timeout, expected_type=type_hints["max_retry_timeout"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument saml_adfs_cookie", value=saml_adfs_cookie, expected_type=type_hints["saml_adfs_cookie"])
            check_type(argname="argument saml_adfs_rpt_id", value=saml_adfs_rpt_id, expected_type=type_hints["saml_adfs_rpt_id"])
            check_type(argname="argument service_account_token_file", value=service_account_token_file, expected_type=type_hints["service_account_token_file"])
            check_type(argname="argument sysorg", value=sysorg, expected_type=type_hints["sysorg"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "org": org,
            "url": url,
        }
        if alias is not None:
            self._values["alias"] = alias
        if allow_api_token_file is not None:
            self._values["allow_api_token_file"] = allow_api_token_file
        if allow_service_account_token_file is not None:
            self._values["allow_service_account_token_file"] = allow_service_account_token_file
        if allow_unverified_ssl is not None:
            self._values["allow_unverified_ssl"] = allow_unverified_ssl
        if api_token is not None:
            self._values["api_token"] = api_token
        if api_token_file is not None:
            self._values["api_token_file"] = api_token_file
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if ignore_metadata_changes is not None:
            self._values["ignore_metadata_changes"] = ignore_metadata_changes
        if import_separator is not None:
            self._values["import_separator"] = import_separator
        if logging is not None:
            self._values["logging"] = logging
        if logging_file is not None:
            self._values["logging_file"] = logging_file
        if max_retry_timeout is not None:
            self._values["max_retry_timeout"] = max_retry_timeout
        if password is not None:
            self._values["password"] = password
        if saml_adfs_cookie is not None:
            self._values["saml_adfs_cookie"] = saml_adfs_cookie
        if saml_adfs_rpt_id is not None:
            self._values["saml_adfs_rpt_id"] = saml_adfs_rpt_id
        if service_account_token_file is not None:
            self._values["service_account_token_file"] = service_account_token_file
        if sysorg is not None:
            self._values["sysorg"] = sysorg
        if token is not None:
            self._values["token"] = token
        if user is not None:
            self._values["user"] = user
        if vdc is not None:
            self._values["vdc"] = vdc

    @builtins.property
    def org(self) -> builtins.str:
        '''The VCD Org for API operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#org VcdProvider#org}
        '''
        result = self._values.get("org")
        assert result is not None, "Required property 'org' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The VCD url for VCD API operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#url VcdProvider#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#alias VcdProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_api_token_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set this to true if you understand the security risks of using API token files and would like to suppress the warnings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_api_token_file VcdProvider#allow_api_token_file}
        '''
        result = self._values.get("allow_api_token_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_service_account_token_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set this to true if you understand the security risks of using Service Account token files and would like to suppress the warnings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_service_account_token_file VcdProvider#allow_service_account_token_file}
        '''
        result = self._values.get("allow_service_account_token_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_unverified_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, VCDClient will permit unverifiable SSL certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#allow_unverified_ssl VcdProvider#allow_unverified_ssl}
        '''
        result = self._values.get("allow_unverified_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def api_token(self) -> typing.Optional[builtins.str]:
        '''The API token used instead of username/password for VCD API operations. (Requires VCD 10.3.1+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#api_token VcdProvider#api_token}
        '''
        result = self._values.get("api_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_token_file(self) -> typing.Optional[builtins.str]:
        '''The API token file instead of username/password for VCD API operations. (Requires VCD 10.3.1+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#api_token_file VcdProvider#api_token_file}
        '''
        result = self._values.get("api_token_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        ''''integrated', 'saml_adfs', 'token', 'api_token', 'api_token_file' and 'service_account_token_file' are supported. 'integrated' is default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#auth_type VcdProvider#auth_type}
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_metadata_changes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VcdProviderIgnoreMetadataChanges"]]]:
        '''ignore_metadata_changes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#ignore_metadata_changes VcdProvider#ignore_metadata_changes}
        '''
        result = self._values.get("ignore_metadata_changes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VcdProviderIgnoreMetadataChanges"]]], result)

    @builtins.property
    def import_separator(self) -> typing.Optional[builtins.str]:
        '''Defines the import separation string to be used with 'terraform import'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#import_separator VcdProvider#import_separator}
        '''
        result = self._values.get("import_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, it will enable logging of API requests and responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#logging VcdProvider#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def logging_file(self) -> typing.Optional[builtins.str]:
        '''Defines the full name of the logging file for API calls (requires 'logging').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#logging_file VcdProvider#logging_file}
        '''
        result = self._values.get("logging_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_retry_timeout(self) -> typing.Optional[jsii.Number]:
        '''Max num seconds to wait for successful response when operating on resources within vCloud (defaults to 60).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#max_retry_timeout VcdProvider#max_retry_timeout}
        '''
        result = self._values.get("max_retry_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The user password for VCD API operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#password VcdProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_adfs_cookie(self) -> typing.Optional[builtins.str]:
        '''Allows to specify custom cookie for ADFS server lookup.

        '{{.Org}}' is replaced by real Org -  e.g. 'sso-preferred=yes; sso_redirect_org={{.Org}}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#saml_adfs_cookie VcdProvider#saml_adfs_cookie}
        '''
        result = self._values.get("saml_adfs_cookie")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_adfs_rpt_id(self) -> typing.Optional[builtins.str]:
        '''Allows to specify custom Relaying Party Trust Identifier for auth_type=saml_adfs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#saml_adfs_rpt_id VcdProvider#saml_adfs_rpt_id}
        '''
        result = self._values.get("saml_adfs_rpt_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_token_file(self) -> typing.Optional[builtins.str]:
        '''The Service Account API token file instead of username/password for VCD API operations. (Requires VCD 10.4.0+).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#service_account_token_file VcdProvider#service_account_token_file}
        '''
        result = self._values.get("service_account_token_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sysorg(self) -> typing.Optional[builtins.str]:
        '''The VCD Org for user authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#sysorg VcdProvider#sysorg}
        '''
        result = self._values.get("sysorg")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''The token used instead of username/password for VCD API operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#token VcdProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''The user name for VCD API operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#user VcdProvider#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The VDC for API operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#vdc VcdProvider#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VcdProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.provider.VcdProviderIgnoreMetadataChanges",
    jsii_struct_bases=[],
    name_mapping={
        "conflict_action": "conflictAction",
        "key_regex": "keyRegex",
        "resource_name": "resourceName",
        "resource_type": "resourceType",
        "value_regex": "valueRegex",
    },
)
class VcdProviderIgnoreMetadataChanges:
    def __init__(
        self,
        *,
        conflict_action: typing.Optional[builtins.str] = None,
        key_regex: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        value_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conflict_action: One of 'error', 'warn' or 'none'. Configures whether a conflict between this ignored metadata block and the metadata entries set in Terraform should fail, warn or do nothing. Defaults to 'error' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#conflict_action VcdProvider#conflict_action}
        :param key_regex: Regular expression of the metadata entry keys to ignore. Either ``key_regex`` or ``value_regex`` is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#key_regex VcdProvider#key_regex}
        :param resource_name: Ignores metadata from the specific entity in VCD named like this argument. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#resource_name VcdProvider#resource_name}
        :param resource_type: Ignores metadata from the specific resource type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#resource_type VcdProvider#resource_type}
        :param value_regex: Regular expression of the metadata entry values to ignore. Either ``key_regex`` or ``value_regex`` is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#value_regex VcdProvider#value_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6953f40b5e711272e937994507090f2bd77781de406276ace525a4930f88ceb)
            check_type(argname="argument conflict_action", value=conflict_action, expected_type=type_hints["conflict_action"])
            check_type(argname="argument key_regex", value=key_regex, expected_type=type_hints["key_regex"])
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument value_regex", value=value_regex, expected_type=type_hints["value_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conflict_action is not None:
            self._values["conflict_action"] = conflict_action
        if key_regex is not None:
            self._values["key_regex"] = key_regex
        if resource_name is not None:
            self._values["resource_name"] = resource_name
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if value_regex is not None:
            self._values["value_regex"] = value_regex

    @builtins.property
    def conflict_action(self) -> typing.Optional[builtins.str]:
        '''One of 'error', 'warn' or 'none'.

        Configures whether a conflict between this ignored metadata block and the metadata entries set in Terraform should fail, warn or do nothing. Defaults to 'error'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#conflict_action VcdProvider#conflict_action}
        '''
        result = self._values.get("conflict_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression of the metadata entry keys to ignore. Either ``key_regex`` or ``value_regex`` is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#key_regex VcdProvider#key_regex}
        '''
        result = self._values.get("key_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_name(self) -> typing.Optional[builtins.str]:
        '''Ignores metadata from the specific entity in VCD named like this argument.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#resource_name VcdProvider#resource_name}
        '''
        result = self._values.get("resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Ignores metadata from the specific resource type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#resource_type VcdProvider#resource_type}
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression of the metadata entry values to ignore. Either ``key_regex`` or ``value_regex`` is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs#value_regex VcdProvider#value_regex}
        '''
        result = self._values.get("value_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VcdProviderIgnoreMetadataChanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "VcdProvider",
    "VcdProviderConfig",
    "VcdProviderIgnoreMetadataChanges",
]

publication.publish()

def _typecheckingstub__5e77e314ff0ea30d6fc8caf7f566cd9cdff220ebbfd6fef80c46f8739d2897b2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    org: builtins.str,
    url: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    allow_api_token_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_service_account_token_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_unverified_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    api_token: typing.Optional[builtins.str] = None,
    api_token_file: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    ignore_metadata_changes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VcdProviderIgnoreMetadataChanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    import_separator: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging_file: typing.Optional[builtins.str] = None,
    max_retry_timeout: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    saml_adfs_cookie: typing.Optional[builtins.str] = None,
    saml_adfs_rpt_id: typing.Optional[builtins.str] = None,
    service_account_token_file: typing.Optional[builtins.str] = None,
    sysorg: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb6e96beca4f867792c5a602269985487bc734fff11a083702265df860a2178(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07570ec945e73c84c535738d6d75c0770d5f7fc3b041775e1fb5359cc52ca70(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0dd004414979d11184817c4cc370827283024bc6deb5c5438c557e1d7ea4b4(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fc2d0667ece09203bca688109b1d3cfc9460b5dd0cb675631eb74205979504(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0e361e7860aa8e07812d8b2cca766d010e3bed03995e9cd9da09ba225f6a4b(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6defc60ccd8a02ae5424ca0b60088031c68768b059633bc67d68f966ca20d9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5027cc8a886b6eae6119496a44355e27296f3a838a857617e87310eed0027cf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1686e18d8fffb070b8c9ebb1d1041e2c12de5e4fc82f6abed7024d57556c1b3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c827bbefebc269a99949ee1ea5d987248f7e1ba32bd00f42d53a08fc0e38fc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VcdProviderIgnoreMetadataChanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a356f62519a16267be8be58778e69150be3e9c04f09244309e002e77a966f61(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caab41d2b3bc669a755a497e98efc730d7be0d1b23101aba10e35ac72336ac91(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f170ad3e18bc21f7c8c4c4e3eb4419d20b7358a2e3eb76c561e30a46900f638e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f15c1a6b9149ee0ae715a10e44a409b3a90b72314c3e731a8cae8ad4104f566(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b9e90cc9c6fc83df6ca4584f0d4d20136824bf6c76d6bad72d99685c72c451(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684994fc87bb2f04bf390932f3ec296812b9ca4521c9452f7614892b85af5c00(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0e98e42d725286654425915549adabfef4fc0ecbaa7257bde7d39e85031b61(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19d84db2d34c748a796c5e8cfef4024243d8e9e694106fd84446c4f6c23f9df(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287ff6d0b7b8784db9bba7aca50c43a0d1332da2eb01294213b3df0216a08103(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783eb78d9d0b48f46468b97d0b40c41b767e7d24d1d77663083fadd0182a7631(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7938c225912bab745d2c56d46cf52758090292fe7acec119bbfe71f89305382d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc548b738cce551280ecedb18d395cd776919d1521d9c0096d76fb933082426(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25aa21aa4caecccd42a830d3d01d6337256a20f12aa710d03a34ebf1ba89f667(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733d00d8cf606f01af1d8a1691aa84142f57a5f6ee70838b89adbd4851a5e6e9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13e4989bdb198f331a97dfc77c4992947344833d779c1a3bc875e8641e623d9(
    *,
    org: builtins.str,
    url: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    allow_api_token_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_service_account_token_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_unverified_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    api_token: typing.Optional[builtins.str] = None,
    api_token_file: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    ignore_metadata_changes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VcdProviderIgnoreMetadataChanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    import_separator: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging_file: typing.Optional[builtins.str] = None,
    max_retry_timeout: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    saml_adfs_cookie: typing.Optional[builtins.str] = None,
    saml_adfs_rpt_id: typing.Optional[builtins.str] = None,
    service_account_token_file: typing.Optional[builtins.str] = None,
    sysorg: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6953f40b5e711272e937994507090f2bd77781de406276ace525a4930f88ceb(
    *,
    conflict_action: typing.Optional[builtins.str] = None,
    key_regex: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    value_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
