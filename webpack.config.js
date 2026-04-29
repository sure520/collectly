const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');

module.exports = (env, argv) => {
  const isDev = argv.mode !== 'production';

  return {
    mode: isDev ? 'development' : 'production',
    entry: './src/index.tsx',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: 'bundle.js'
    },
    module: {
      rules: [
        {
          test: /\.(ts|tsx|js|jsx)$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: [
                [
                  '@babel/preset-react',
                  {
                    runtime: 'automatic',
                    development: isDev
                  }
                ],
                '@babel/preset-env',
                '@babel/preset-typescript'
              ]
            }
          }
        },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader', 'postcss-loader']
        }
      ]
    },
    resolve: {
      extensions: ['.ts', '.tsx', '.js', '.jsx']
    },
    devServer: {
      port: 3266,
      allowedHosts: ['all', '.alibaba-inc.com'],
      historyApiFallback: {
        index: '/index.html',
        rewrites: [
          { from: /^\/_p\/\d+\//, to: '/index.html' }
        ]
      },
      client: {
        webSocketURL: {
          hostname: '0.0.0.0',
          pathname: '/ws',
          port: 3266
        },
        overlay: {
          errors: true,
          warnings: false
        }
      },
      webSocketServer: false
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: './index.html',
        inject: 'body'
      }),
      new webpack.DefinePlugin({
        'process.env': JSON.stringify(process.env || {}),
        'process.env.REACT_APP_API_BASE_URL': JSON.stringify(process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api'),
      })
    ]
  };
};
