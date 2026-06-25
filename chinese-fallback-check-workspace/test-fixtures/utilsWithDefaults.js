// P2: 函数默认参数中文兜底
export function showMessage(msg = '操作成功') {
  console.log(msg);
}

export function createUser(name = '未命名用户', role = '普通用户') {
  return { name, role };
}

export const formatDate = (date, format = '默认格式') => {
  return date.toLocaleDateString();
};

// P1: 三元表达式中文回退
export function getDisplayName(user) {
  return user.nickname ? user.nickname : '匿名用户';
}

export function getStatusText(code) {
  return code === 0 ? '成功' : '未知错误';
}
