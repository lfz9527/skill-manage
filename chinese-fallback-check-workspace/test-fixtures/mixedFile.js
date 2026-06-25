import { SPEECH_COMMANDS } from '../config/VoiceCommand';

// 这是语音命令配置数据，中文是领域数据，非兜底
const DEFAULT_COMMANDS = {
  forward: '前进',
  backward: '后退',
  left: '左转',
  right: '右转',
};

export function parseVoiceCommand(input) {
  // P0 兜底：逻辑运算符中文回退
  const command = input || '未识别命令';
  return DEFAULT_COMMANDS[command] || '未知指令';
}

export function getCommandLabel(cmd, lang) {
  // P1 兜底：三元表达式中文回退
  return lang === 'cn' ? cmd : 'Unknown';
}
