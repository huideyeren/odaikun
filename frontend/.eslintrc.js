let rules = {
  'max-len': ['error', 80, 2, { ignoreUrls: true }],
  'no-console': [0],
  'no-restricted-syntax': 'off',
  'no-continue': 'off',
  'no-underscore-dangle': 'off',
  'import/extensions': 'off',
  'import/no-unresolved': 'off',
  'operator-linebreak': 'off',
  'implicit-arrow-linebreak': 'off',
  'react/destructuring-assignment': 'off',
  'jsx-a11y/click-events-have-key-events': 'off',
  'jsx-a11y/no-static-element-interactions': 'off',
  'react/jsx-one-expression-per-line': 'off',
  'react/jsx-filename-extension': [2, { extensions: ['.ts', '.tsx'] }],
  'lines-between-class-members': [
    'error',
    'always',
    { exceptAfterSingleLine: true },
  ],
  'prettier/prettier': [
    'error',
    {
      singleQuote: true,
      trailingComma: 'es5',
    },
  ],
  'no-unused-vars': 'warn',
  'func-names': 'off',
  'no-process-exit': 'off',
  'object-shorthand': 'off',
  'class-methods-use-this': 'off',
  'import/prefer-default-export': 'warn',
  'prefer-promise-reject-errors': 'warn',
  'import/no-extraneous-dependencies': 'warn',
  'react/jsx-props-no-spreading': "warn",
  'no-param-reassign': "warn",
  'import/prefer-default-export': 'warn',
  'no-shadow': 'warn',
  'jsx-a11y/anchor-is-valid': 'warn'
};

module.exports = {
  extends: ['airbnb', 'plugin:prettier/recommended', 'prettier/react'],
  parser: 'babel-eslint',
  rules,
  env: {
    browser: true,
    commonjs: true,
    node: true,
    jest: true,
    es6: true,
  },
  plugins: ['react', 'react-hooks', 'jsx-a11y'],
  settings: {
    ecmascript: 6,
    jsx: true,
    'import/resolver': {
      node: {
        paths: ['src'],
      },
    },
    'import/parsers': {
      '@typescript-eslint/parser': ['.ts', '.tsx'],
    },
    react: {
      pragma: 'React',
      version: '16.8',
    },
  },
};
