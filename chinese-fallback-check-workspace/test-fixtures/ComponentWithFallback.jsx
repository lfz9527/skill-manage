import React from 'react';
import { combinedLanguageSelector } from '../../utils/ReduxUtils';

const TestComponent = ({ language }) => {
  // P0: 逻辑运算符中文兜底
  const title = language.pageTitle || '页面标题';
  const subtitle = language.subtitle ?? '默认副标题';

  // P3: JSX 中文硬编码（同一文件已使用 i18n）
  return (
    <div>
      <h1>{title}</h1>
      <h2>{subtitle}</h2>
      <p>{language.description || '这是默认描述文本'}</p>
      <span>保存成功</span>
      <button>{language.confirm || '确认'}</button>
    </div>
  );
};

export default TestComponent;
