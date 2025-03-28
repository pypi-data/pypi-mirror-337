'''
# `vcd_subscribed_catalog`

Refer to the Terraform Registry for docs: [`vcd_subscribed_catalog`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog).
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


class SubscribedCatalog(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.subscribedCatalog.SubscribedCatalog",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog vcd_subscribed_catalog}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        subscription_url: builtins.str,
        cancel_failed_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        make_local_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        storage_profile_id: typing.Optional[builtins.str] = None,
        store_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subscription_password: typing.Optional[builtins.str] = None,
        sync_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_all_media_items: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_all_vapp_templates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_catalog: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_media_items: typing.Optional[typing.Sequence[builtins.str]] = None,
        sync_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_vapp_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog vcd_subscribed_catalog} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#name SubscribedCatalog#name}
        :param subscription_url: The URL to subscribe to the external catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#subscription_url SubscribedCatalog#subscription_url}
        :param cancel_failed_tasks: When true, the subscribed catalog will attempt canceling failed tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#cancel_failed_tasks SubscribedCatalog#cancel_failed_tasks}
        :param delete_force: When destroying use delete_force=True with delete_recursive=True to remove a catalog and any objects it contains, regardless of their state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#delete_force SubscribedCatalog#delete_force}
        :param delete_recursive: When destroying use delete_recursive=True to remove the catalog and any objects it contains that are in a state that normally allows removal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#delete_recursive SubscribedCatalog#delete_recursive}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#id SubscribedCatalog#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param make_local_copy: If true, subscription to a catalog creates a local copy of all items. Defaults to false, which does not create a local copy of catalog items unless a sync operation is performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#make_local_copy SubscribedCatalog#make_local_copy}
        :param org: The name of organization to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#org SubscribedCatalog#org}
        :param storage_profile_id: Optional storage profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#storage_profile_id SubscribedCatalog#storage_profile_id}
        :param store_tasks: If true, saves list of tasks to file for later update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#store_tasks SubscribedCatalog#store_tasks}
        :param subscription_password: An optional password to access the catalog. Only ASCII characters are allowed in a valid password. Passing in six asterisks '******' indicates to keep current password. Passing in null or empty string indicates to remove password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#subscription_password SubscribedCatalog#subscription_password}
        :param sync_all: If true, synchronise this catalog and all items. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all SubscribedCatalog#sync_all}
        :param sync_all_media_items: If true, synchronises all media items. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all_media_items SubscribedCatalog#sync_all_media_items}
        :param sync_all_vapp_templates: If true, synchronises all vApp templates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all_vapp_templates SubscribedCatalog#sync_all_vapp_templates}
        :param sync_catalog: If true, synchronise this catalog. This operation fetches the list of items. If ``make_local_copy`` is set, it also fetches the items data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_catalog SubscribedCatalog#sync_catalog}
        :param sync_media_items: Synchronises media items from this list of names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_media_items SubscribedCatalog#sync_media_items}
        :param sync_on_refresh: Boolean value that shows if sync should be performed on every refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_on_refresh SubscribedCatalog#sync_on_refresh}
        :param sync_vapp_templates: Synchronises vApp templates from this list of names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_vapp_templates SubscribedCatalog#sync_vapp_templates}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1107765539600a2812e0c3a316891c5ffa234249eafd87a14fff75c1141d35)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SubscribedCatalogConfig(
            name=name,
            subscription_url=subscription_url,
            cancel_failed_tasks=cancel_failed_tasks,
            delete_force=delete_force,
            delete_recursive=delete_recursive,
            id=id,
            make_local_copy=make_local_copy,
            org=org,
            storage_profile_id=storage_profile_id,
            store_tasks=store_tasks,
            subscription_password=subscription_password,
            sync_all=sync_all,
            sync_all_media_items=sync_all_media_items,
            sync_all_vapp_templates=sync_all_vapp_templates,
            sync_catalog=sync_catalog,
            sync_media_items=sync_media_items,
            sync_on_refresh=sync_on_refresh,
            sync_vapp_templates=sync_vapp_templates,
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
        '''Generates CDKTF code for importing a SubscribedCatalog resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SubscribedCatalog to import.
        :param import_from_id: The id of the existing SubscribedCatalog that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SubscribedCatalog to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7893e9d1c39be501fb7c153d314be856bab9f4cee1f87bf98ab304058fde06b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCancelFailedTasks")
    def reset_cancel_failed_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCancelFailedTasks", []))

    @jsii.member(jsii_name="resetDeleteForce")
    def reset_delete_force(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteForce", []))

    @jsii.member(jsii_name="resetDeleteRecursive")
    def reset_delete_recursive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRecursive", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMakeLocalCopy")
    def reset_make_local_copy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMakeLocalCopy", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetStorageProfileId")
    def reset_storage_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageProfileId", []))

    @jsii.member(jsii_name="resetStoreTasks")
    def reset_store_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoreTasks", []))

    @jsii.member(jsii_name="resetSubscriptionPassword")
    def reset_subscription_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriptionPassword", []))

    @jsii.member(jsii_name="resetSyncAll")
    def reset_sync_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncAll", []))

    @jsii.member(jsii_name="resetSyncAllMediaItems")
    def reset_sync_all_media_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncAllMediaItems", []))

    @jsii.member(jsii_name="resetSyncAllVappTemplates")
    def reset_sync_all_vapp_templates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncAllVappTemplates", []))

    @jsii.member(jsii_name="resetSyncCatalog")
    def reset_sync_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncCatalog", []))

    @jsii.member(jsii_name="resetSyncMediaItems")
    def reset_sync_media_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncMediaItems", []))

    @jsii.member(jsii_name="resetSyncOnRefresh")
    def reset_sync_on_refresh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncOnRefresh", []))

    @jsii.member(jsii_name="resetSyncVappTemplates")
    def reset_sync_vapp_templates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncVappTemplates", []))

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
    @jsii.member(jsii_name="catalogVersion")
    def catalog_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "catalogVersion"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="failedTasks")
    def failed_tasks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "failedTasks"))

    @builtins.property
    @jsii.member(jsii_name="href")
    def href(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "href"))

    @builtins.property
    @jsii.member(jsii_name="isLocal")
    def is_local(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isLocal"))

    @builtins.property
    @jsii.member(jsii_name="isPublished")
    def is_published(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isPublished"))

    @builtins.property
    @jsii.member(jsii_name="isShared")
    def is_shared(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isShared"))

    @builtins.property
    @jsii.member(jsii_name="mediaItemList")
    def media_item_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mediaItemList"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="numberOfMedia")
    def number_of_media(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfMedia"))

    @builtins.property
    @jsii.member(jsii_name="numberOfVappTemplates")
    def number_of_vapp_templates(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfVappTemplates"))

    @builtins.property
    @jsii.member(jsii_name="ownerName")
    def owner_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerName"))

    @builtins.property
    @jsii.member(jsii_name="publishSubscriptionType")
    def publish_subscription_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publishSubscriptionType"))

    @builtins.property
    @jsii.member(jsii_name="runningTasks")
    def running_tasks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "runningTasks"))

    @builtins.property
    @jsii.member(jsii_name="tasksFileName")
    def tasks_file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tasksFileName"))

    @builtins.property
    @jsii.member(jsii_name="vappTemplateList")
    def vapp_template_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vappTemplateList"))

    @builtins.property
    @jsii.member(jsii_name="cancelFailedTasksInput")
    def cancel_failed_tasks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cancelFailedTasksInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteForceInput")
    def delete_force_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteForceInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRecursiveInput")
    def delete_recursive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteRecursiveInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="makeLocalCopyInput")
    def make_local_copy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "makeLocalCopyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileIdInput")
    def storage_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storeTasksInput")
    def store_tasks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storeTasksInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionPasswordInput")
    def subscription_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionUrlInput")
    def subscription_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="syncAllInput")
    def sync_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncAllInput"))

    @builtins.property
    @jsii.member(jsii_name="syncAllMediaItemsInput")
    def sync_all_media_items_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncAllMediaItemsInput"))

    @builtins.property
    @jsii.member(jsii_name="syncAllVappTemplatesInput")
    def sync_all_vapp_templates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncAllVappTemplatesInput"))

    @builtins.property
    @jsii.member(jsii_name="syncCatalogInput")
    def sync_catalog_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncCatalogInput"))

    @builtins.property
    @jsii.member(jsii_name="syncMediaItemsInput")
    def sync_media_items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "syncMediaItemsInput"))

    @builtins.property
    @jsii.member(jsii_name="syncOnRefreshInput")
    def sync_on_refresh_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncOnRefreshInput"))

    @builtins.property
    @jsii.member(jsii_name="syncVappTemplatesInput")
    def sync_vapp_templates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "syncVappTemplatesInput"))

    @builtins.property
    @jsii.member(jsii_name="cancelFailedTasks")
    def cancel_failed_tasks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cancelFailedTasks"))

    @cancel_failed_tasks.setter
    def cancel_failed_tasks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f894617c4b0d07497501e8c337bd60c94a8099dbee9e88f8f7f0a58a87443734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cancelFailedTasks", value)

    @builtins.property
    @jsii.member(jsii_name="deleteForce")
    def delete_force(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteForce"))

    @delete_force.setter
    def delete_force(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47d6b5d2491dd0fc4dd3553bf8ced74badadf386282adc58e96150c4313c7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteForce", value)

    @builtins.property
    @jsii.member(jsii_name="deleteRecursive")
    def delete_recursive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteRecursive"))

    @delete_recursive.setter
    def delete_recursive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512f2c90ab086cf61618db309c8eec3242d062a65234597658c16e6fb46aae21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRecursive", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22fa3fa223959eda2a646882a78e23acf398f4a31bdd714d854f00874b4492d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="makeLocalCopy")
    def make_local_copy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "makeLocalCopy"))

    @make_local_copy.setter
    def make_local_copy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a90cd85ce2f175b0f659ac705e117cd593e815cf85b90096474d7778aaac48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "makeLocalCopy", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11bf5faed1ed26f980d6e4ac2a79ff9b64bd985fd9348afdfed7ea9c00cfca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3240f40a1c2cfff946d0d64574a1c4b6a9f42aa4ece24a5c57164ee86ca0d64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfileId")
    def storage_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfileId"))

    @storage_profile_id.setter
    def storage_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc4e36ba7a73aa8f1d0420aa4cf3b0a0a40606e374c0e9fbcd7883097d617b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="storeTasks")
    def store_tasks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "storeTasks"))

    @store_tasks.setter
    def store_tasks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9082d1f56d60f0384db5130c928c36d4d7708685d7fc9db3ba9740a21d7bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeTasks", value)

    @builtins.property
    @jsii.member(jsii_name="subscriptionPassword")
    def subscription_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionPassword"))

    @subscription_password.setter
    def subscription_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c75a1709d750fcdc32bcd4c8b2c9babd8bb5c20e1624eb933ae995cf1a2057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionPassword", value)

    @builtins.property
    @jsii.member(jsii_name="subscriptionUrl")
    def subscription_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionUrl"))

    @subscription_url.setter
    def subscription_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e1f88aee91f8339faaac7296a8d943704d86e7f3d6dd01737035e371812ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="syncAll")
    def sync_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncAll"))

    @sync_all.setter
    def sync_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce10b49cd6145c84c28003157cb6652fa22f394497562672ae16296bcbab5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncAll", value)

    @builtins.property
    @jsii.member(jsii_name="syncAllMediaItems")
    def sync_all_media_items(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncAllMediaItems"))

    @sync_all_media_items.setter
    def sync_all_media_items(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71c2942b9674cd528958ca5e2131a08b2e13587d0d3e7e975dfc67470a3dae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncAllMediaItems", value)

    @builtins.property
    @jsii.member(jsii_name="syncAllVappTemplates")
    def sync_all_vapp_templates(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncAllVappTemplates"))

    @sync_all_vapp_templates.setter
    def sync_all_vapp_templates(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f724258d1d1299142f22c1865c043389008841616a9341568a3ae918b030f94b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncAllVappTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="syncCatalog")
    def sync_catalog(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncCatalog"))

    @sync_catalog.setter
    def sync_catalog(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314f638b948a27bfe7e42e60119c3308a9a0f8375dede69bb7582ca819aa14c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncCatalog", value)

    @builtins.property
    @jsii.member(jsii_name="syncMediaItems")
    def sync_media_items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "syncMediaItems"))

    @sync_media_items.setter
    def sync_media_items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcf9a50d5f6f69ecd8cbeaa21f7a06a3be49fc1316ddbfcfb77250270a8c568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncMediaItems", value)

    @builtins.property
    @jsii.member(jsii_name="syncOnRefresh")
    def sync_on_refresh(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncOnRefresh"))

    @sync_on_refresh.setter
    def sync_on_refresh(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ccedb323665067dc88dc86c981b04c687e7ce3dbbd85e10d0b839fabd677a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncOnRefresh", value)

    @builtins.property
    @jsii.member(jsii_name="syncVappTemplates")
    def sync_vapp_templates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "syncVappTemplates"))

    @sync_vapp_templates.setter
    def sync_vapp_templates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120fbb0addd3f62a777069e00816f10d50f1a3c4c37697a5421e0f89b0dd8864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncVappTemplates", value)


@jsii.data_type(
    jsii_type="vcd.subscribedCatalog.SubscribedCatalogConfig",
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
        "subscription_url": "subscriptionUrl",
        "cancel_failed_tasks": "cancelFailedTasks",
        "delete_force": "deleteForce",
        "delete_recursive": "deleteRecursive",
        "id": "id",
        "make_local_copy": "makeLocalCopy",
        "org": "org",
        "storage_profile_id": "storageProfileId",
        "store_tasks": "storeTasks",
        "subscription_password": "subscriptionPassword",
        "sync_all": "syncAll",
        "sync_all_media_items": "syncAllMediaItems",
        "sync_all_vapp_templates": "syncAllVappTemplates",
        "sync_catalog": "syncCatalog",
        "sync_media_items": "syncMediaItems",
        "sync_on_refresh": "syncOnRefresh",
        "sync_vapp_templates": "syncVappTemplates",
    },
)
class SubscribedCatalogConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        subscription_url: builtins.str,
        cancel_failed_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        make_local_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        storage_profile_id: typing.Optional[builtins.str] = None,
        store_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subscription_password: typing.Optional[builtins.str] = None,
        sync_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_all_media_items: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_all_vapp_templates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_catalog: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_media_items: typing.Optional[typing.Sequence[builtins.str]] = None,
        sync_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_vapp_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#name SubscribedCatalog#name}
        :param subscription_url: The URL to subscribe to the external catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#subscription_url SubscribedCatalog#subscription_url}
        :param cancel_failed_tasks: When true, the subscribed catalog will attempt canceling failed tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#cancel_failed_tasks SubscribedCatalog#cancel_failed_tasks}
        :param delete_force: When destroying use delete_force=True with delete_recursive=True to remove a catalog and any objects it contains, regardless of their state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#delete_force SubscribedCatalog#delete_force}
        :param delete_recursive: When destroying use delete_recursive=True to remove the catalog and any objects it contains that are in a state that normally allows removal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#delete_recursive SubscribedCatalog#delete_recursive}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#id SubscribedCatalog#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param make_local_copy: If true, subscription to a catalog creates a local copy of all items. Defaults to false, which does not create a local copy of catalog items unless a sync operation is performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#make_local_copy SubscribedCatalog#make_local_copy}
        :param org: The name of organization to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#org SubscribedCatalog#org}
        :param storage_profile_id: Optional storage profile ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#storage_profile_id SubscribedCatalog#storage_profile_id}
        :param store_tasks: If true, saves list of tasks to file for later update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#store_tasks SubscribedCatalog#store_tasks}
        :param subscription_password: An optional password to access the catalog. Only ASCII characters are allowed in a valid password. Passing in six asterisks '******' indicates to keep current password. Passing in null or empty string indicates to remove password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#subscription_password SubscribedCatalog#subscription_password}
        :param sync_all: If true, synchronise this catalog and all items. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all SubscribedCatalog#sync_all}
        :param sync_all_media_items: If true, synchronises all media items. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all_media_items SubscribedCatalog#sync_all_media_items}
        :param sync_all_vapp_templates: If true, synchronises all vApp templates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all_vapp_templates SubscribedCatalog#sync_all_vapp_templates}
        :param sync_catalog: If true, synchronise this catalog. This operation fetches the list of items. If ``make_local_copy`` is set, it also fetches the items data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_catalog SubscribedCatalog#sync_catalog}
        :param sync_media_items: Synchronises media items from this list of names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_media_items SubscribedCatalog#sync_media_items}
        :param sync_on_refresh: Boolean value that shows if sync should be performed on every refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_on_refresh SubscribedCatalog#sync_on_refresh}
        :param sync_vapp_templates: Synchronises vApp templates from this list of names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_vapp_templates SubscribedCatalog#sync_vapp_templates}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affcf21c51820e7dad7373300e14f9260ffe7a17491a54b32c15abe165caef40)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subscription_url", value=subscription_url, expected_type=type_hints["subscription_url"])
            check_type(argname="argument cancel_failed_tasks", value=cancel_failed_tasks, expected_type=type_hints["cancel_failed_tasks"])
            check_type(argname="argument delete_force", value=delete_force, expected_type=type_hints["delete_force"])
            check_type(argname="argument delete_recursive", value=delete_recursive, expected_type=type_hints["delete_recursive"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument make_local_copy", value=make_local_copy, expected_type=type_hints["make_local_copy"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument storage_profile_id", value=storage_profile_id, expected_type=type_hints["storage_profile_id"])
            check_type(argname="argument store_tasks", value=store_tasks, expected_type=type_hints["store_tasks"])
            check_type(argname="argument subscription_password", value=subscription_password, expected_type=type_hints["subscription_password"])
            check_type(argname="argument sync_all", value=sync_all, expected_type=type_hints["sync_all"])
            check_type(argname="argument sync_all_media_items", value=sync_all_media_items, expected_type=type_hints["sync_all_media_items"])
            check_type(argname="argument sync_all_vapp_templates", value=sync_all_vapp_templates, expected_type=type_hints["sync_all_vapp_templates"])
            check_type(argname="argument sync_catalog", value=sync_catalog, expected_type=type_hints["sync_catalog"])
            check_type(argname="argument sync_media_items", value=sync_media_items, expected_type=type_hints["sync_media_items"])
            check_type(argname="argument sync_on_refresh", value=sync_on_refresh, expected_type=type_hints["sync_on_refresh"])
            check_type(argname="argument sync_vapp_templates", value=sync_vapp_templates, expected_type=type_hints["sync_vapp_templates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "subscription_url": subscription_url,
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
        if cancel_failed_tasks is not None:
            self._values["cancel_failed_tasks"] = cancel_failed_tasks
        if delete_force is not None:
            self._values["delete_force"] = delete_force
        if delete_recursive is not None:
            self._values["delete_recursive"] = delete_recursive
        if id is not None:
            self._values["id"] = id
        if make_local_copy is not None:
            self._values["make_local_copy"] = make_local_copy
        if org is not None:
            self._values["org"] = org
        if storage_profile_id is not None:
            self._values["storage_profile_id"] = storage_profile_id
        if store_tasks is not None:
            self._values["store_tasks"] = store_tasks
        if subscription_password is not None:
            self._values["subscription_password"] = subscription_password
        if sync_all is not None:
            self._values["sync_all"] = sync_all
        if sync_all_media_items is not None:
            self._values["sync_all_media_items"] = sync_all_media_items
        if sync_all_vapp_templates is not None:
            self._values["sync_all_vapp_templates"] = sync_all_vapp_templates
        if sync_catalog is not None:
            self._values["sync_catalog"] = sync_catalog
        if sync_media_items is not None:
            self._values["sync_media_items"] = sync_media_items
        if sync_on_refresh is not None:
            self._values["sync_on_refresh"] = sync_on_refresh
        if sync_vapp_templates is not None:
            self._values["sync_vapp_templates"] = sync_vapp_templates

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
        '''The name of the catalog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#name SubscribedCatalog#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscription_url(self) -> builtins.str:
        '''The URL to subscribe to the external catalog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#subscription_url SubscribedCatalog#subscription_url}
        '''
        result = self._values.get("subscription_url")
        assert result is not None, "Required property 'subscription_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cancel_failed_tasks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the subscribed catalog will attempt canceling failed tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#cancel_failed_tasks SubscribedCatalog#cancel_failed_tasks}
        '''
        result = self._values.get("cancel_failed_tasks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When destroying use delete_force=True with delete_recursive=True to remove a catalog and any objects it contains, regardless of their state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#delete_force SubscribedCatalog#delete_force}
        '''
        result = self._values.get("delete_force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_recursive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When destroying use delete_recursive=True to remove the catalog and any objects it contains that are in a state that normally allows removal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#delete_recursive SubscribedCatalog#delete_recursive}
        '''
        result = self._values.get("delete_recursive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#id SubscribedCatalog#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def make_local_copy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, subscription to a catalog creates a local copy of all items.

        Defaults to false, which does not create a local copy of catalog items unless a sync operation is performed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#make_local_copy SubscribedCatalog#make_local_copy}
        '''
        result = self._values.get("make_local_copy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#org SubscribedCatalog#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_profile_id(self) -> typing.Optional[builtins.str]:
        '''Optional storage profile ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#storage_profile_id SubscribedCatalog#storage_profile_id}
        '''
        result = self._values.get("storage_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def store_tasks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, saves list of tasks to file for later update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#store_tasks SubscribedCatalog#store_tasks}
        '''
        result = self._values.get("store_tasks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subscription_password(self) -> typing.Optional[builtins.str]:
        '''An optional password to access the catalog.

        Only ASCII characters are allowed in a valid password. Passing in six asterisks '******' indicates to keep current password. Passing in null or empty string indicates to remove password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#subscription_password SubscribedCatalog#subscription_password}
        '''
        result = self._values.get("subscription_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, synchronise this catalog and all items.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all SubscribedCatalog#sync_all}
        '''
        result = self._values.get("sync_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_all_media_items(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, synchronises all media items.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all_media_items SubscribedCatalog#sync_all_media_items}
        '''
        result = self._values.get("sync_all_media_items")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_all_vapp_templates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, synchronises all vApp templates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_all_vapp_templates SubscribedCatalog#sync_all_vapp_templates}
        '''
        result = self._values.get("sync_all_vapp_templates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_catalog(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, synchronise this catalog.

        This operation fetches the list of items. If ``make_local_copy`` is set, it also fetches the items data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_catalog SubscribedCatalog#sync_catalog}
        '''
        result = self._values.get("sync_catalog")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_media_items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Synchronises media items from this list of names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_media_items SubscribedCatalog#sync_media_items}
        '''
        result = self._values.get("sync_media_items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sync_on_refresh(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean value that shows if sync should be performed on every refresh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_on_refresh SubscribedCatalog#sync_on_refresh}
        '''
        result = self._values.get("sync_on_refresh")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_vapp_templates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Synchronises vApp templates from this list of names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/subscribed_catalog#sync_vapp_templates SubscribedCatalog#sync_vapp_templates}
        '''
        result = self._values.get("sync_vapp_templates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscribedCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SubscribedCatalog",
    "SubscribedCatalogConfig",
]

publication.publish()

def _typecheckingstub__5c1107765539600a2812e0c3a316891c5ffa234249eafd87a14fff75c1141d35(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    subscription_url: builtins.str,
    cancel_failed_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    make_local_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    storage_profile_id: typing.Optional[builtins.str] = None,
    store_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subscription_password: typing.Optional[builtins.str] = None,
    sync_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_all_media_items: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_all_vapp_templates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_catalog: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_media_items: typing.Optional[typing.Sequence[builtins.str]] = None,
    sync_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_vapp_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__e7893e9d1c39be501fb7c153d314be856bab9f4cee1f87bf98ab304058fde06b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f894617c4b0d07497501e8c337bd60c94a8099dbee9e88f8f7f0a58a87443734(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47d6b5d2491dd0fc4dd3553bf8ced74badadf386282adc58e96150c4313c7eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512f2c90ab086cf61618db309c8eec3242d062a65234597658c16e6fb46aae21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22fa3fa223959eda2a646882a78e23acf398f4a31bdd714d854f00874b4492d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a90cd85ce2f175b0f659ac705e117cd593e815cf85b90096474d7778aaac48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11bf5faed1ed26f980d6e4ac2a79ff9b64bd985fd9348afdfed7ea9c00cfca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3240f40a1c2cfff946d0d64574a1c4b6a9f42aa4ece24a5c57164ee86ca0d64c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc4e36ba7a73aa8f1d0420aa4cf3b0a0a40606e374c0e9fbcd7883097d617b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9082d1f56d60f0384db5130c928c36d4d7708685d7fc9db3ba9740a21d7bed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c75a1709d750fcdc32bcd4c8b2c9babd8bb5c20e1624eb933ae995cf1a2057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e1f88aee91f8339faaac7296a8d943704d86e7f3d6dd01737035e371812ce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce10b49cd6145c84c28003157cb6652fa22f394497562672ae16296bcbab5b0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71c2942b9674cd528958ca5e2131a08b2e13587d0d3e7e975dfc67470a3dae2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f724258d1d1299142f22c1865c043389008841616a9341568a3ae918b030f94b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314f638b948a27bfe7e42e60119c3308a9a0f8375dede69bb7582ca819aa14c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcf9a50d5f6f69ecd8cbeaa21f7a06a3be49fc1316ddbfcfb77250270a8c568(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ccedb323665067dc88dc86c981b04c687e7ce3dbbd85e10d0b839fabd677a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120fbb0addd3f62a777069e00816f10d50f1a3c4c37697a5421e0f89b0dd8864(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affcf21c51820e7dad7373300e14f9260ffe7a17491a54b32c15abe165caef40(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    subscription_url: builtins.str,
    cancel_failed_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_recursive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    make_local_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    storage_profile_id: typing.Optional[builtins.str] = None,
    store_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subscription_password: typing.Optional[builtins.str] = None,
    sync_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_all_media_items: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_all_vapp_templates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_catalog: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_media_items: typing.Optional[typing.Sequence[builtins.str]] = None,
    sync_on_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_vapp_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
