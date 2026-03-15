import os
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv
# 官方 SDK 引入
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.user import User
from msgraph.generated.models.authentication_method import AuthenticationMethod
from msgraph.generated.users.users_request_builder import UsersRequestBuilder, RequestConfiguration, QueryParameters
load_dotenv()

class AzureMFAInspector:
    def __init__(self):
        """
        初始化 SDK 客户端，从环境变量读取配置
        """
        self.tenant_id = os.environ.get("AZURE_TENANT_ID")
        self.client_id = os.environ.get("AZURE_CLIENT_ID")
        self.client_secret = os.environ.get("AZURE_CLIENT_SECRET")

        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError("请设置环境变量: AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET")

        # 1. 使用 azure-identity 创建凭据对象
        self.credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        # 2. 初始化 Graph Service Client
        # scopes 设置为默认即可
        self.client = GraphServiceClient(self.credential, scopes=["https://graph.microsoft.com/.default"])

    async def fetch(self) -> Dict[str, Any]:
        """
        拉取所有用户信息及其认证方法 (使用官方 SDK)
        :return: 包含用户列表的字典，每个用户包含认证方法
        """
        print("正在通过 SDK 拉取用户列表...")
        users_list = []

        try:
            # 发起请求，只获取必要的字段
            # SDK 会自动处理分页
            request_config = RequestConfiguration()
            request_config.query_parameters = QueryParameters()
            request_config.query_parameters.select = ['id', 'userPrincipalName', 'displayName']
            response = await self.client.users.get(request_configuration=request_config)

            # 遍历当前页
            if response and response.value:
                for user in response.value:
                    users_list.append({
                        'id': user.id,
                        'userPrincipalName': user.user_principal_name,
                        'displayName': user.display_name,
                        'auth_methods': []  # 初始化为空，后面填充
                    })

                # 处理分页 (如果有下一页)
                while response and response.odata_next_link:
                    response = await self.client.users.with_url(response.odata_next_link).get(request_configuration=request_config)
                    if response and response.value:
                        for user in response.value:
                            users_list.append({
                                'id': user.id,
                                'userPrincipalName': user.user_principal_name,
                                'displayName': user.display_name,
                                'auth_methods': []
                            })

        except Exception as e:
            print(f"拉取用户失败: {e}")

        print(f"成功拉取 {len(users_list)} 个用户。开始获取认证方法...")

        # 为每个用户获取认证方法
        for user in users_list:
            user_id = user['id']
            try:
                methods_response = await self.client.users.by_user_id(user_id).authentication.methods.get()
                if methods_response and methods_response.value:
                    auth_methods = []
                    for method in methods_response.value:
                        od_type = getattr(method, 'odata_type', None) or getattr(method, '@odata.type', None)
                        if od_type:
                            auth_methods.append(od_type)
                    user['auth_methods'] = auth_methods
                else:
                    user['auth_methods'] = []  # 无认证方法
            except Exception as e:
                print(f"获取用户 {user['userPrincipalName']} 的认证方法时出错: {e}")
                user['auth_methods'] = []

        return {'users': users_list}

    async def check(self, data: Dict[str, Any]) -> List[Dict]:
        """
        检查用户 MFA 状态 (基于 fetch 拉取的数据)
        :param data: fetch 返回的字典，包含 users 列表
        :return: 未开启 MFA 的用户列表
        """
        print("开始检查 MFA 状态...")
        no_mfa_users = []
        users = data.get('users', [])
        for user in users:
            auth_methods = user.get('auth_methods', [])
            has_mfa = False
            # 检查是否存在非密码认证方法
            for method_type in auth_methods:
                if method_type and "#microsoft.graph.passwordAuthenticationMethod" not in method_type:
                    # 发现 MFA 方法
                    has_mfa = True
                    break

            if not has_mfa:
                reason = "仅密码或无认证方法" if auth_methods else "无认证方法"
                no_mfa_users.append({
                    'name': user['displayName'],
                    'email': user['userPrincipalName'],
                    'reason': reason
                })

        return no_mfa_users

# ================= 使用示例 =================
async def main():
    try:
        # 实例化
        inspector = AzureMFAInspector()

        # 拉取数据
        data = await inspector.fetch()

        # 检查状态
        if data and data.get('users'):
            # 只检查前100个用户（测试用）
            users_to_check = data['users'][:100]
            result = await inspector.check({'users': users_to_check})

            print("\n" + "="*30)
            if result:
                print(f"发现 {len(result)} 个用户未开启 MFA：")
                for u in result:
                    print(f"  - 姓名: {u['name']:<15} | 邮箱: {u['email']}")
            else:
                print("所有用户均已配置 MFA。")
            print("="*30)

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())