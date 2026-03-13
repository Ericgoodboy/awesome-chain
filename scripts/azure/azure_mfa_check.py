import os
import asyncio
from typing import List, Dict
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

    async def fetch(self) -> List[Dict]:
        """
        拉取所有用户信息 (使用官方 SDK)
        :return: 用户字典列表
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
                        'displayName': user.display_name
                    })

                # 处理分页 (如果有下一页)
                # 虽然 SDK 提供了分页迭代器，但手动处理 next_link 也是常见做法
                # 这里为了演示清晰，展示获取所有数据的逻辑
                # 注意：在实际生产中，如果有大量用户，建议使用迭代器逐条处理
                while response and response.odata_next_link:
                    response = await self.client.users.with_url(response.odata_next_link).get(request_configuration=request_config)
                    if response and response.value:
                        for user in response.value:
                            users_list.append({
                                'id': user.id,
                                'userPrincipalName': user.user_principal_name,
                                'displayName': user.display_name
                            })

        except Exception as e:
            print(f"拉取用户失败: {e}")

        print(f"成功拉取 {len(users_list)} 个用户。")
        return users_list

    async def check(self, user_list: List[Dict]) -> List[Dict]:
        """
        检查用户 MFA 状态 (使用官方 SDK)
        :param user_list: fetch 返回的用户列表
        :return: 未开启 MFA 的用户列表
        """
        print("开始通过 SDK 检查 MFA 状态...")
        no_mfa_users = []
        for user in user_list:
            user_id = user['id']
            
            try:
                # 调用 authentication methods 端点
                methods_response = await self.client.users.by_user_id(user_id).authentication.methods.get()
                
                if methods_response and methods_response.value:
                    has_mfa = False
                    for method in methods_response.value:
                        # 获取 OData 类型，例如 "#microsoft.graph.passwordAuthenticationMethod"
                        # SDK 返回的是对象，我们可以检查 odata_type 属性
                        # 注意：不同版本的 SDK 属性名可能略有不同，通常为 odata_type 或 @odata.type
                        
                        # 简单判断：如果不是密码方法，则视为 MFA 方法
                        # 常见 MFA 类型: microsoftAuthenticatorAuthenticationMethod, phoneAuthenticationMethod 等
                        
                        # 获取类型字符串
                        od_type = getattr(method, 'odata_type', None) or getattr(method, '@odata.type', None)
                        
                        if od_type and "#microsoft.graph.passwordAuthenticationMethod" not in od_type:
                            print(f"未知认证方法类型: {od_type}")
                            has_mfa = True
                            break
                        else: 
                            print(f"未知认证方法类型: {od_type}")
                    
                    if not has_mfa:
                        no_mfa_users.append({
                            'name': user['displayName'],
                            'email': user['userPrincipalName'],
                            'reason': "仅密码或无认证方法"
                        })
                else:
                    # 无任何认证方法
                    no_mfa_users.append({
                        'name': user['displayName'],
                        'email': user['userPrincipalName'],
                        'reason': "无认证方法"
                    })

            except Exception as e:
                print(f"检查用户 {user['userPrincipalName']} 时出错: {e}")

        return no_mfa_users

# ================= 使用示例 =================
async def main():
    try:
        # 实例化
        inspector = AzureMFAInspector()
        
        # 拉取数据
        users = await inspector.fetch()
        
        # 检查状态
        if users:
            result = await inspector.check(users[:100])
            
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