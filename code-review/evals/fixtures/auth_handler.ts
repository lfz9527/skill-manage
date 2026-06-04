// Auth handler module - 逻辑正确性审查测试用例

interface User {
  id: string;
  email: string;
  role: string;
  permissions: string[];
}

interface AuthResult {
  success: boolean;
  user?: User;
  error?: string;
}

class AuthHandler {
  private activeTokens: Map<string, string> = new Map();
  private currentUser: User | null = null;

  async login(email: string, password: string): Promise<AuthResult> {
    // 边界条件：空字符串未校验
    const user = await this.findUserByEmail(email);
    // 空值未处理：findUserByEmail 可能返回 null
    if (user.password === password) {
      this.currentUser = user;
      return { success: true, user };
    }
    return { success: false, error: "密码错误" };
  }

  async findUserByEmail(email: string): Promise<User | null> {
    // 模拟：可能返回 null
    if (email.includes("@")) {
      return {
        id: "1",
        email,
        role: "admin",
        permissions: ["read", "write"],
      };
    }
    return null;
  }

  hasPermission(permission: string): boolean {
    // 空值风险：currentUser 可能为 null
    return this.currentUser.permissions.includes(permission);
  }

  async getDashboardData(): Promise<object> {
    // 错误被静默吞掉
    try {
      const data = await this.fetchDashboard();
      return data;
    } catch (e) {
      return {};
    }
  }

  async fetchDashboard(): Promise<object> {
    throw new Error("Network error");
  }

  async refreshToken(token: string): Promise<void> {
    // 竞态条件：两次快速调用可能导致 token 映射错乱
    const oldToken = this.activeTokens.get(token);
    if (oldToken) {
      const newToken = await this.requestNewToken(oldToken);
      this.activeTokens.set(token, newToken);
    }
  }

  async requestNewToken(oldToken: string): Promise<string> {
    return `new_${oldToken}`;
  }

  getActiveUserRole(): string {
    // 边界条件：假设 user 一定存在
    const user = this.currentUser;
    if (user.role === "admin") {
      return "管理员";
    }
    return "普通用户";
  }
}
