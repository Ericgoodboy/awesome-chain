#!/usr/bin/env python3
"""
Azure存储帐户共享密钥访问检查脚本

检查Azure存储帐户是否启用了“共享密钥授权”。
共享密钥是永久有效的静态凭证，一旦泄露，相当于交出了整个存储帐户的最高管理权限。
在现代云应用中，推荐使用有时效性、可精细化授权的 Azure AD 凭证和共享访问签名 (SAS) 进行访问，以遵循最小权限原则。

风险等级：High
"""

import os
import sys
from typing import List, Dict
from dotenv import load_dotenv

# Azure SDK 引入
try:
    from azure.identity import ClientSecretCredential
    from azure.mgmt.storage import StorageManagementClient
    from azure.mgmt.resource import ResourceManagementClient
    from azure.core.exceptions import HttpResponseError
except ImportError as e:
    print(f"缺少Azure SDK依赖，请安装: pip install azure-identity azure-mgmt-storage azure-mgmt-resource")
    print(f"错误详情: {e}")
    sys.exit(1)

load_dotenv()

class StorageAccountSharedKeyInspector:
    def __init__(self):
        """
        初始化 Azure SDK 客户端，从环境变量读取配置
        """
        self.tenant_id = os.environ.get("AZURE_TENANT_ID")
        self.client_id = os.environ.get("AZURE_CLIENT_ID")
        self.client_secret = os.environ.get("AZURE_CLIENT_SECRET")
        self.subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

        if not all([self.tenant_id, self.client_id, self.client_secret, self.subscription_id]):
            raise ValueError(
                "请设置环境变量: AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_SUBSCRIPTION_ID"
            )

        # 1. 使用 azure-identity 创建凭据对象
        self.credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        # 2. 初始化 Storage Management Client
        self.storage_client = StorageManagementClient(
            credential=self.credential,
            subscription_id=self.subscription_id
        )

        # 3. 初始化 Resource Management Client（用于获取资源组）
        self.resource_client = ResourceManagementClient(
            credential=self.credential,
            subscription_id=self.subscription_id
        )

    def fetch(self) -> List[Dict]:
        """
        获取所有存储帐户信息
        :return: 存储帐户字典列表
        """
        print("正在获取存储帐户列表...")
        storage_accounts = []

        try:
            # 获取所有存储帐户（跨所有资源组）
            accounts = self.storage_client.storage_accounts.list()

            for account in accounts:
                # 解析资源组名称（从ID中提取）
                # ID格式: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{name}
                id_parts = account.id.split('/')
                resource_group_name = id_parts[4] if len(id_parts) > 4 else "未知"

                storage_accounts.append({
                    'id': account.id,
                    'name': account.name,
                    'resource_group': resource_group_name,
                    'location': account.location,
                    'sku': account.sku.name if account.sku else '未知',
                    'properties': account
                })

        except HttpResponseError as e:
            print(f"获取存储帐户失败: {e.message}")
        except Exception as e:
            print(f"获取存储帐户时发生意外错误: {e}")

        print(f"成功获取 {len(storage_accounts)} 个存储帐户。")
        return storage_accounts

    def check(self, storage_accounts: List[Dict]) -> List[Dict]:
        """
        检查存储帐户是否启用了共享密钥访问
        :param storage_accounts: fetch 返回的存储帐户列表
        :return: 启用共享密钥访问的存储帐户列表（存在风险）
        """
        print("开始检查共享密钥访问设置...")
        risky_accounts = []

        for account in storage_accounts:
            account_name = account['name']
            resource_group = account['resource_group']

            try:
                # 获取存储帐户的详细配置（包括allow_shared_key_access属性）
                # 注意：不同版本的SDK属性名可能不同
                account_properties = account['properties']

                # 检查 allow_shared_key_access 属性
                # 在较新版本的SDK中，该属性可能在account_properties.allow_shared_key_access
                # 或在account_properties.enable_shared_key_access
                allow_shared_key = None

                # 方法1：直接访问属性
                if hasattr(account_properties, 'allow_shared_key_access'):
                    allow_shared_key = account_properties.allow_shared_key_access
                elif hasattr(account_properties, 'enable_shared_key_access'):
                    allow_shared_key = account_properties.enable_shared_key_access
                # 方法2：通过additional_properties（如果SDK版本较旧）
                elif hasattr(account_properties, 'additional_properties'):
                    additional = account_properties.additional_properties
                    if additional:
                        allow_shared_key = additional.get('allowSharedKeyAccess')

                # 如果属性为None或True，则视为启用（存在风险）
                # 根据Azure文档，None通常表示默认启用（旧帐户）
                is_risky = False
                reason = ""

                if allow_shared_key is None:
                    is_risky = True
                    reason = "allow_shared_key_access属性未设置（可能默认启用）"
                elif allow_shared_key is True:
                    is_risky = True
                    reason = "allow_shared_key_access已启用"
                elif allow_shared_key is False:
                    is_risky = False
                    reason = "allow_shared_key_access已禁用（安全）"
                else:
                    # 未知值
                    is_risky = True
                    reason = f"allow_shared_key_access未知值: {allow_shared_key}"

                if is_risky:
                    risky_accounts.append({
                        'name': account_name,
                        'resource_group': resource_group,
                        'id': account['id'],
                        'location': account['location'],
                        'reason': reason,
                        'allow_shared_key_access': allow_shared_key
                    })
                    print(f"  发现风险帐户: {account_name} ({resource_group}) - {reason}")
                else:
                    print(f"  安全帐户: {account_name} ({resource_group}) - {reason}")

            except Exception as e:
                print(f"检查存储帐户 {account_name} 时出错: {e}")
                # 将出错帐户视为风险帐户（需要人工检查）
                risky_accounts.append({
                    'name': account_name,
                    'resource_group': resource_group,
                    'id': account['id'],
                    'location': account['location'],
                    'reason': f"检查时出错: {e}",
                    'allow_shared_key_access': None
                })

        return risky_accounts

    def generate_fix_instructions(self, risky_account: Dict) -> str:
        """
        生成修复指令
        :param risky_account: 风险帐户信息
        :return: 修复指令字符串
        """
        subscription_id = self.subscription_id
        resource_group = risky_account['resource_group']
        account_name = risky_account['name']

        instructions = f"""
## 存储帐户: {account_name}
- 资源组: {resource_group}
- 位置: {risky_account['location']}
- 风险原因: {risky_account['reason']}

## 修复步骤:
1. 登录到 Azure 门户，导航到"存储帐户"服务。
2. 点击目标存储帐户 {account_name}。
3. 在左侧菜单的"设置"部分，选择"配置"。
4. 在主窗格中，找到"允许存储帐户密钥访问"选项，并将其设置为"已禁用"。
5. 单击"保存"。

直接链接: https://portal.azure.com/#resource/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Storage/storageAccounts/{account_name}/configuration

## Azure CLI 修复命令:
```bash
# 禁用共享密钥访问
az storage account update \\
  --resource-group {resource_group} \\
  --name {account_name} \\
  --allow-shared-key-access false

# 验证设置
az storage account show \\
  --resource-group {resource_group} \\
  --name {account_name} \\
  --query "allowSharedKeyAccess"
```

## 注意事项:
- 禁用共享密钥授权前，请务必全面排查并修改所有依赖此密钥进行访问的应用程序或服务。
- 建议将认证方式迁移至基于 Azure Active Directory 的 RBAC 或使用有时效性的共享访问签名 (SAS)。
- 测试应用功能确保业务不受影响。
"""
        return instructions


def main():
    """主函数"""
    try:
        # 实例化检查器
        inspector = StorageAccountSharedKeyInspector()

        # 获取存储帐户
        accounts = inspector.fetch()

        if not accounts:
            print("未找到存储帐户，或没有访问权限。")
            return

        # 检查风险
        risky_accounts = inspector.check(accounts)

        # 输出结果
        print("\n" + "="*60)
        if risky_accounts:
            print(f"发现 {len(risky_accounts)} 个存储帐户启用了共享密钥访问（存在风险）:")
            for i, acc in enumerate(risky_accounts, 1):
                print(f"\n{i}. {acc['name']} (资源组: {acc['resource_group']})")
                print(f"   位置: {acc['location']}")
                print(f"   风险原因: {acc['reason']}")
                print(f"   allow_shared_key_access: {acc['allow_shared_key_access']}")

            # 为第一个风险帐户生成详细修复指令
            if risky_accounts:
                print("\n" + "="*60)
                print("修复指令示例:")
                print(inspector.generate_fix_instructions(risky_accounts[0]))
        else:
            print("所有存储帐户均已禁用共享密钥访问（安全）。")
        print("="*60)

    except ValueError as e:
        print(f"配置错误: {e}")
        print("\n请设置以下环境变量:")
        print("  AZURE_TENANT_ID: Azure租户ID")
        print("  AZURE_CLIENT_ID: 应用客户端ID")
        print("  AZURE_CLIENT_SECRET: 客户端密钥")
        print("  AZURE_SUBSCRIPTION_ID: Azure订阅ID")
        print("\n可以在 .env 文件中设置这些变量。")
    except Exception as e:
        print(f"运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()