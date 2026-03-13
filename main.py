#!/usr/bin/env python3
"""
Awesome Chain CLI

Command-line interface for Awesome Chain framework.
"""

import argparse
import sys
from typing import Optional

sys.path.insert(0, '.')
from src.awesome_chain import Agent, ToolRegistry, SkillManager
from src.awesome_chain.prompt import util


def main():
    # Create agent
    agent = Agent()
    content = """
    {}
    用户输入如下：
    {}
    
    """
    prompt_dict = util.load_prompt('native')
    prompt = prompt_dict['system']
    user_content = """
    【规则名称】：Azure控制台用户未启用多因素认证（MFA）
【风险等级】：Base: 10.0, Net: 1.0, IAM: 2.0, Res: 1.5, Score: 30.0, Level: High
【规则描述】：Azure Active Directory (Azure AD) 是微软的云身份和访问管理服务，多因素认证（MFA）是保护用户账户安全的关键防线。此规则检查所有具有 Azure 门户访问权限的用户是否已强制启用 MFA。在仅依赖密码的传统认证模式下，一旦密码因钓鱼、撞库或恶意软件而泄露，攻击者即可直接登录您的云控制台，如同内部员工一样操作核心业务资产。
【潜在后果】：
攻击者可利用窃取的凭证登录 Azure 门户，全面接管您的云环境。这可能导致核心数据库（如 Azure SQL）被窃取或勒索加密，虚拟机被部署为“矿机”产生高额账单，甚至删除所有资源导致业务彻底停摆。黑客通过网络钓鱼或暗网购买获取员工密码后，直接登录 Azure 门户。随后，他们会创建隐蔽的管理员后门账户，修改网络安全组以暴露内部服务，并最终横向移动到存储账户和数据库，实现自动化脱库和持久化控制。

【修复建议】：
1. 登录到 Azure 门户 (https://portal.azure.com)。 2. 导航到 “Azure Active Directory” -> “用户”。 3. 在顶部菜单中选择 “Per-user MFA”。 4. 在新打开的页面 (https://account.activedirectory.windowsazure.com/usermanagement/mfasettings.aspx) 中，找到多重身份验证状态为 “已禁用” 的用户。 5. 选中该用户或多个用户，并在右侧的管理菜单中选择 “启用” 来强制开启MFA。

注意事项：为用户启用 MFA 后，他们下次登录时将被要求设置额外的验证方式（如手机应用、短信或电话）。建议在启用前提前通知相关用户，以确保平稳过渡。对于拥有管理员角色的用户，强烈建议使用条件访问策略（Conditional Access Policy）来强制执行MFA，以获得更灵活和强大的安全控制。
    """
    result = agent.run(content.format(prompt, user_content))
    print("\n" + result)

main()